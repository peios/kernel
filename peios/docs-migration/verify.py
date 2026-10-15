#!/usr/bin/env python3
"""Check source prose, literal blocks, tables and references survive conversion."""
import argparse
from collections import Counter
from html.parser import HTMLParser
import json
import hashlib
from pathlib import Path
import re

from docutils import nodes
from markdown_it import MarkdownIt
from convert import parse, XRef


class Visible(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text = []
        self.ids = set()
        self.links = []
        self.counts = Counter()

    def handle_starttag(self, tag, attrs):
        self.counts[tag] += 1
        attrs = dict(attrs)
        if 'id' in attrs:
            if attrs['id'] in self.ids:
                raise ValueError('duplicate anchor ' + attrs['id'])
            self.ids.add(attrs['id'])
        if tag == 'a' and 'href' in attrs:
            self.links.append(attrs['href'])
        if tag in ('p', 'li', 'pre', 'td', 'th', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self.text.append('\n')

    def handle_endtag(self, tag):
        if tag in ('p', 'li', 'pre', 'td', 'th', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self.text.append('\n')

    def handle_data(self, text):
        self.text.append(text)


def normal(text):
    return re.sub(r'\s+', ' ', text).strip()


def verify(root, site, mapping):
    bulk = None
    if any('validation' in item for item in mapping['pages']):
        import bulk
        bulk.configure(root.resolve())
    md = MarkdownIt('commonmark', {'html': True})
    pages = {}
    counts = Counter()
    errors = []
    by_source={p['source']:p for p in mapping['pages']}
    for item in mapping.get('non_article_sources',[]):
        if hashlib.sha256((root/item['source']).read_bytes()).hexdigest()!=item['source_sha256']:
            errors.append(item['source']+': non-article baseline changed')
        if item['kind']=='included-fragment':
            owners=item.get('included_by',[])
            if not owners:errors.append(item['source']+': fragment has no owner')
            for owner in owners:
                if not any(d['path']==item['source'] for d in by_source.get(owner,{}).get('source_dependencies',[])):
                    errors.append(item['source']+': missing included dependency on '+owner)
        counts['accounted_non_articles']+=1
    for item in mapping['pages']:
        if 'supplementary_source' in item:
            import supplementary
            markdown=(site/Path(item['destination']).relative_to('docs')).read_text()
            counts.update(supplementary.verify(root,item,markdown))
            visible=Visible();visible.feed(md.render(markdown.split('---\n',2)[2]));pages[item['reference']]=visible
            continue
        if 'legacy_text' in item:
            import legacy_text, legacy_sequence
            markdown=(site/Path(item['destination']).relative_to('docs')).read_text()
            check=legacy_sequence.verify if item['legacy_text']['kind']=='websequence-to-mermaid' else legacy_text.verify_page
            counts.update(check(root,item,markdown))
            visible=Visible();visible.feed(md.render(markdown.split('---\n',2)[2]))
            pages[item['reference']]=visible
            continue
        if 'generated_reference' in item:
            import netlink_references, binding_references
            markdown = (site/Path(item['destination']).relative_to('docs')).read_text()
            checker={'netlink-yaml':netlink_references,'device-tree-binding':binding_references}[item['generated_reference']['kind']]
            counts.update(checker.verify_wrapper(root, item, markdown))
            visible = Visible()
            visible.feed(md.render(markdown.split('---\n', 2)[2]))
            # Generated labels are checked against actual output by the strict
            # build and netlink_references.check_rendered.
            visible.ids.update(v.removeprefix('#') for v in item['labels'].values())
            pages[item['reference']] = visible
            continue
        if 'adaptation' in item:
            import adapted
            dest = site/Path(item['destination']).relative_to('docs')
            markdown = dest.read_text()
            counts.update(adapted.verify_page(root, item, markdown))
            visible = Visible()
            visible.feed(md.render(markdown.split('---\n', 2)[2]))
            pages[item['reference']] = visible
            continue
        source = root/'Documentation'/Path(item['source']).relative_to('Documentation')
        tree = bulk.parse(source) if bulk is not None and 'validation' in item else parse(source)
        dest = site/Path(item['destination']).relative_to('docs')
        text = dest.read_text().split('---\n', 2)[2]
        tokens = md.parse(text)
        visible = Visible()
        visible.feed(md.render(text))
        flat = normal(''.join(visible.text))
        rewrites = item.get('reviewed_text_replacements', {})
        pages[item['reference']] = visible
        if bulk is not None and 'validation' in item:
            from types import SimpleNamespace
            counts.update(bulk.verify_page(tree, text, SimpleNamespace(resolved_refs=item['resolved_references'],diagrams=item.get('diagrams',[])), rewrites))
            counts['articles'] += 1
            continue
        for para in tree.findall(nodes.paragraph):
            if isinstance(para.parent, nodes.system_message):
                continue
            if any(para.findall(XRef)):
                counts['paragraphs_with_expanded_refs_reviewed_separately'] += 1
                continue
            counts['paragraphs'] += 1
            if normal(rewrites.get(normal(para.astext()), para.astext())) not in flat:
                errors.append(f'{source.name}:{para.line}: missing or changed prose: {para.astext()[:160]}')
        for node in tree.findall():
            if isinstance(node, (nodes.term, nodes.field_name)) or (isinstance(node, nodes.title) and isinstance(node.parent, nodes.section)):
                counts['headings_and_terms'] += 1
                if normal(rewrites.get(normal(node.astext()), node.astext())) not in flat:
                    errors.append(f'{source.name}:{node.line}: missing heading or term: {node.astext()}')
        original = [n.astext() for n in tree.findall(nodes.literal_block)]
        converted = [t.content.removesuffix('\n') for t in tokens if t.type in ('fence','code_block') and not t.info.startswith('{')]
        counts['literal_blocks'] += len(original)
        if original != converted:
            errors.append(f'{source.name}: literal blocks changed ({len(original)} -> {len(converted)})')
        tables = len(list(tree.findall(nodes.table)))
        counts['tables'] += tables
        if tables != visible.counts['table']:
            errors.append(f'{source.name}: table count changed')
        for section in item['sections']:
            if not set(section['anchors']) <= visible.ids:
                errors.append(f'{source.name}: missing section anchors')
        for target in item['labels'].values():
            if target[1:] not in visible.ids:
                errors.append(f'{source.name}: missing source label {target}')
        counts['articles'] += 1
    for ref, page in pages.items():
        for link in page.links:
            if link.startswith('#'):
                target, _, anchor = ref, '#', link[1:]
            elif link.startswith('~'):
                target, _, anchor = link[1:].partition('#')
            else:
                continue
            # Source aliases can be checked before rendering. Trail-generated
            # heading and plugin anchors are checked by the strict site build.
            if target not in pages or (anchor.startswith('rst-') and anchor not in pages[target].ids):
                errors.append(f'{ref}: unresolved {link}')
    if errors:
        raise ValueError('\n'.join(errors))
    return dict(counts)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--kernel-root', type=Path, required=True)
    ap.add_argument('--site', type=Path, required=True)
    ap.add_argument('--mapping', type=Path, required=True)
    ap.add_argument('--inventory',type=Path,default=Path(__file__).with_name('source-inventory.json'))
    args = ap.parse_args()
    try:
        mapping=json.loads(args.mapping.read_text())
        if not args.inventory.exists():raise ValueError('source inventory missing: '+str(args.inventory))
        import check_inventory
        inventory=check_inventory.check(args.kernel_root,mapping,json.loads(args.inventory.read_text()))
        if inventory['errors']:raise ValueError('\n'.join(inventory['errors']))
        if json.loads(args.inventory.read_text()).get('layout')=='tooling-and-trail':
            import check_authority
            print(json.dumps(check_authority.check(args.kernel_root,args.site,mapping),indent=2))
        else:
            print(json.dumps(verify(args.kernel_root, args.site, mapping), indent=2))
    except ValueError as e:
        ap.exit(1, str(e)+'\n')
