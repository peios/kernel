#!/usr/bin/env python3
"""One-way RST import into a NEW staging directory, never over edited Trail pages."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import html
import io
import json
from pathlib import Path
import re
import subprocess
import sys

from docutils import nodes
from docutils.core import publish_doctree
from docutils.parsers.rst import Directive, directives, roles


class KernelDoc(nodes.General, nodes.Element):
    pass


class XRef(nodes.Inline, nodes.TextElement):
    pass


class Toc(nodes.General, nodes.Element):
    pass


class KernelDirective(Directive):
    required_arguments = 1
    final_argument_whitespace = False
    has_content = False
    option_spec = {name: directives.unchanged for name in (
        'export', 'internal', 'doc', 'identifiers', 'functions', 'no-identifiers')}

    def run(self):
        node = KernelDoc(path=self.arguments[0], options={k: v or '' for k, v in self.options.items()})
        node.line = self.lineno
        return [node]


class TocDirective(Directive):
    has_content = True
    option_spec = {'maxdepth': directives.nonnegative_int}

    def run(self):
        return [Toc(entries=list(self.content))]


def xref_role(name, rawtext, text, lineno, inliner, options=None, content=None):
    return [XRef(rawtext, text, kind=name)], []


def c_role(name, rawtext, text, lineno, inliner, options=None, content=None):
    if name == 'c:func' and not text.endswith('()'):
        text += '()'
    return [nodes.literal(rawtext, text)], []


directives.register_directive('kernel-doc', KernelDirective)
directives.register_directive('toctree', TocDirective)
for role in ('ref', 'doc'):
    roles.register_local_role(role, xref_role)
for role in ('func', 'macro', 'type', 'struct', 'union', 'enum', 'var', 'member', 'data'):
    roles.register_local_role('c:' + role, c_role)


def parse(path, text=None):
    warnings = io.StringIO()
    tree = publish_doctree(path.read_text() if text is None else text, source_path=str(path), settings_overrides={
        'warning_stream': warnings, 'halt_level': 5, 'report_level': 2,
        'file_insertion_enabled': False, 'raw_enabled': False,
        'docinfo_xform': False, 'syntax_highlight': 'none',
    })
    problems = [n.astext() for n in tree.findall(nodes.system_message) if n['level'] >= 2]
    if problems:
        raise ValueError('\n'.join(problems))
    return tree


def quote(text):
    return json.dumps(text, ensure_ascii=False)


def escape(text):
    # Escape Markdown syntax, including accidental HTML and entities. Literal
    # blocks and inline literals bypass this function entirely.
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    # Escaping only the first/last underscore in a run leaves the inner pair
    # able to open emphasis (for example __attribute__). Escape every one.
    return re.sub(r'[\\`*_\[\]{}#!|~]', lambda m: '\\' + m.group(), text)


def code(text):
    width = max((len(m.group()) for m in re.finditer(r'`+', text)), default=0) + 1
    tick = '`' * width
    pad = ' ' if text.startswith(('`', ' ')) or text.endswith(('`', ' ')) else ''
    return tick + pad + text + pad + tick


def fence(text, info='text'):
    width = max(3, max((len(m.group()) + 1 for m in re.finditer(r'`+', text)), default=0))
    tick = '`' * width
    return f'{tick}{info}\n{text}\n{tick}'


def indent(text, prefix):
    # Form feeds and other control characters in literal source excerpts are
    # content, not newline separators (str.splitlines() would discard them).
    return '\n'.join(prefix + line if line else prefix.rstrip() for line in text.split('\n'))


def roman(number):
    if not 0 < number < 4000:
        raise ValueError('Roman list number outside supported range')
    result = ''
    for value, symbol in ((1000,'m'),(900,'cm'),(500,'d'),(400,'cd'),(100,'c'),
                          (90,'xc'),(50,'l'),(40,'xl'),(10,'x'),(9,'ix'),(5,'v'),(4,'iv'),(1,'i')):
        while number >= value:
            result += symbol
            number -= value
    return result


class Writer:
    def __init__(self, source, targets, labels, upstream):
        self.source, self.targets, self.labels, self.upstream = source, targets, labels, upstream
        self.external_docs = set()
        self.sections = []
        self.emitted_ids = set()
        self.unquote_lines = set(targets[source].get('unquote_lines', []))
        self.code_languages = dict(targets[source].get('code_languages', {}))

    def fail(self, node, message):
        raise ValueError(f'{self.source}:{node.line or "?"}: {message}')

    def anchors(self, node):
        result = []
        for ident in node.get('ids', []):
            if ident not in self.emitted_ids:
                self.emitted_ids.add(ident)
                # Prefix ALL source anchors, avoiding collisions with Trail's
                # automatically generated heading anchors.
                result.append(f'<a id="rst-{html.escape(ident, quote=True)}"></a>')
        return '\n'.join(result)

    def doc_link(self, path):
        if path.startswith('Documentation/'):
            rel = path[len('Documentation/'):]
        else:
            rel = str(Path(self.source).parent / path)
        if rel in self.targets:
            return '~' + self.targets[rel]['reference']
        self.external_docs.add(rel)
        return f'https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/{rel}?id={self.upstream}'

    def prose(self, text):
        # Link bare documentation filenames as well as explicit RST references.
        pattern = r'(?<![\w/])(?:Documentation/[\w./-]+\.(?:rst|txt)|[\w-]+\.rst)(?!\w)'
        parts, end = [], 0
        for m in re.finditer(pattern, text):
            parts.extend((escape(text[end:m.start()]), f'[{escape(m.group())}]({self.doc_link(m.group())})'))
            end = m.end()
        parts.append(escape(text[end:]))
        return ''.join(parts)

    def inline(self, node):
        if isinstance(node, nodes.Text):
            return self.prose(node.astext())
        if isinstance(node, (nodes.literal, nodes.title_reference)):
            return code(node.astext())
        if isinstance(node, XRef):
            text = node.astext()
            match = re.fullmatch(r'(.+)\s+<([^>]+)>', text)
            caption, target = match.groups() if match else (text, text)
            if node['kind'] == 'ref':
                match_label = self.labels.get(self.source, {}).get(target)
                if match_label is None:
                    candidates = [v[target] for v in self.labels.values() if target in v]
                    if len(candidates) == 1:
                        match_label = candidates[0]
                if match_label is None:
                    self.fail(node, f'unresolved :ref: {target}')
                ref, anchor, title = match_label
                caption = caption if match else title
                return f'[{escape(caption)}](~{ref}#rst-{anchor})'
            path = target if target.endswith('.rst') else target + '.rst'
            return f'[{escape(caption)}]({self.doc_link(path)})'
        children = lambda: ''.join(self.inline(c) for c in node.children)
        if isinstance(node, nodes.emphasis):
            return '*' + children() + '*'
        if isinstance(node, nodes.strong):
            return '**' + children() + '**'
        if isinstance(node, nodes.reference):
            dest = node.get('refuri')
            if dest is None:
                dest = '#rst-' + node['refid']
            elif dest.endswith(('.rst', '.txt')) and '://' not in dest:
                dest = self.doc_link(dest)
            return f'[{children()}](<{dest}>)'
        if isinstance(node, nodes.footnote_reference):
            return f'[{children()}](#rst-{node["refid"]})'
        if isinstance(node, nodes.target):
            return self.anchors(node)
        self.fail(node, f'unsupported inline node {node.tagname}')

    def html_inline(self, node):
        if isinstance(node, nodes.Text):
            return html.escape(node.astext())
        if isinstance(node, nodes.literal):
            return '<code>' + html.escape(node.astext()) + '</code>'
        if isinstance(node, (nodes.emphasis, nodes.strong)):
            tag = 'em' if isinstance(node, nodes.emphasis) else 'strong'
            return f'<{tag}>' + ''.join(self.html_inline(c) for c in node.children) + f'</{tag}>'
        if isinstance(node, nodes.footnote_reference):
            return f'<a href="#rst-{node["refid"]}">{html.escape(node.astext())}</a>'
        self.fail(node, f'unsupported table inline node {node.tagname}')

    def table(self, node):
        # HTML preserves headerless tables and row/column spans without
        # manufacturing headings. Table cell syntax is deliberately bounded.
        result = ['<table>']
        for group in node.children:
            if not isinstance(group, nodes.tgroup):
                self.fail(group, 'unsupported table child')
            for part in group.children:
                if isinstance(part, nodes.colspec):
                    continue
                if not isinstance(part, (nodes.thead, nodes.tbody)):
                    self.fail(part, 'unsupported table group')
                tag = 'thead' if isinstance(part, nodes.thead) else 'tbody'
                result.append(f'<{tag}>')
                for row in part.children:
                    result.append('<tr>')
                    for cell in row.children:
                        celltag = 'th' if tag == 'thead' else 'td'
                        attrs = ''.join(f' {attr}="{cell[key]+1}"' for key, attr in (
                            ('morecols', 'colspan'), ('morerows', 'rowspan')) if key in cell)
                        contents = []
                        for child in cell.children:
                            if not isinstance(child, nodes.paragraph):
                                self.fail(child, 'unsupported table cell block')
                            contents.append('<p>' + ''.join(self.html_inline(c) for c in child.children) + '</p>')
                        result.append(f'<{celltag}{attrs}>' + ''.join(contents) + f'</{celltag}>')
                    result.append('</tr>')
                result.append(f'</{tag}>')
        return '\n'.join(result + ['</table>'])

    def blocks(self, children, depth=1):
        return '\n\n'.join(filter(None, (self.block(c, depth) for c in children)))

    def block(self, node, depth=1):
        if isinstance(node, nodes.document):
            return self.blocks(node.children, depth)
        if isinstance(node, nodes.section):
            heading = node.children[0]
            anchors = self.anchors(node)
            self.sections.append({'source_line': node.line, 'title': heading.astext(),
                                  'anchors': ['rst-' + i for i in node['ids']]})
            if depth + 1 > 6:
                self.fail(node, 'heading deeper than Markdown supports')
            return '\n\n'.join(filter(None, [anchors, '#' * (depth+1) + ' ' + self.inline_children(heading),
                                              self.blocks(node.children[1:], depth+1)]))
        if isinstance(node, nodes.title):
            return ''  # document title lives in Trail frontmatter
        if isinstance(node, nodes.paragraph):
            return self.inline_children(node)
        if isinstance(node, nodes.literal_block):
            return fence(node.astext(), self.code_languages.pop(str(node.line), 'text'))
        if isinstance(node, KernelDoc):
            options = '\n'.join(':' + k + ':' + (' ' + ' '.join(re.sub(r'\\\s*(?:\n|$)', ' ', v).split()) if v else '')
                                for k, v in node['options'].items())
            return fence(options, '{kernel-doc} ' + node['path'])
        if isinstance(node, (nodes.bullet_list, nodes.enumerated_list)):
            if isinstance(node, nodes.enumerated_list) and node['enumtype'] not in ('arabic', 'lowerroman'):
                self.fail(node, 'non-arabic enumeration needs explicit treatment')
            items = []
            for i, child in enumerate(node.children, node.get('start', 1)):
                marker = '- ' if isinstance(node, nodes.bullet_list) else f'{i}. '
                content = self.blocks(child.children, depth)
                if node.get('enumtype') == 'lowerroman':
                    marker = '- '
                    content = '**' + node['prefix'] + roman(i) + node['suffix'] + '** ' + content
                lines = content.splitlines()
                items.append(marker + lines[0] + ('\n' + indent('\n'.join(lines[1:]), ' ' * len(marker)) if len(lines)>1 else ''))
            return '\n\n'.join(items)
        if isinstance(node, nodes.definition_list):
            items = []
            for item in node.children:
                if len(item.children) != 2 or not isinstance(item.children[0], nodes.term):
                    self.fail(item, 'unsupported definition list shape')
                term, definition = item.children
                items.append('- **' + self.inline_children(term) + '**\n\n' + indent(self.blocks(definition.children, depth), '  '))
            return '\n\n'.join(items)
        if isinstance(node, nodes.field_list):
            return '\n\n'.join('**' + self.inline_children(f.children[0]) + ':** ' +
                               self.blocks(f.children[1].children, depth) for f in node.children)
        if isinstance(node, nodes.block_quote):
            if node.line in self.unquote_lines:
                self.unquote_lines.remove(node.line)
                return self.blocks(node.children, depth)
            return indent(self.blocks(node.children, depth), '> ')
        if isinstance(node, nodes.note):
            return '> [!NOTE]\n>\n' + indent(self.blocks(node.children, depth), '> ')
        if isinstance(node, nodes.transition):
            return '---'
        if isinstance(node, nodes.comment):
            if '-->' in node.astext():
                self.fail(node, 'comment contains HTML comment terminator')
            return '<!-- ' + node.astext() + ' -->'
        if isinstance(node, nodes.target):
            return self.anchors(node)
        if isinstance(node, nodes.table):
            return self.table(node)
        if isinstance(node, nodes.footnote):
            return self.anchors(node) + '\n\n**[' + node.children[0].astext() + ']** ' + self.blocks(node.children[1:], depth)
        if isinstance(node, Toc):
            return ''  # separately checked against the batch inventory
        if isinstance(node, nodes.system_message) and node['level'] < 2:
            return ''  # parser information, not authored content
        self.fail(node, f'unsupported block node {node.tagname}')

    def inline_children(self, node):
        return ''.join(self.inline(c) for c in node.children)


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()


def convert(root, plan_path, output):
    plan = json.loads(plan_path.read_text())
    if output.exists():
        raise ValueError(f'refusing to overwrite {output}; generate into a new staging directory')
    source_root = root / 'docs-to-translate'
    upstream = git(root, 'rev-parse', plan['upstream_ref'] + '^{commit}')
    trees = {p: parse(source_root / p) for p in plan['pages']}
    index = parse(source_root / plan['index'])
    entries = [entry.strip() + '.rst' for toc in index.findall(Toc) for entry in toc['entries'] if entry.strip()]
    expected = {str(Path(plan['index']).parent / entry) for entry in entries}
    if expected != set(trees):
        raise ValueError('plan must cover exactly the source toctree')
    actual = {str(p.relative_to(source_root)) for p in (source_root / plan['index']).parent.glob('*.rst')}
    if actual != set(trees) | {plan['index']}:
        raise ValueError('unmapped source documents in batch')
    targets = plan['pages']
    labels = {}
    for source, tree in trees.items():
        labels[source] = {}
        for node in tree.findall(nodes.Element):
            for i, name in enumerate(node.get('names', [])):
                if not node.get('ids'):
                    continue
                title = node.children[0].astext() if isinstance(node, nodes.section) else name
                ident = node['ids'][i] if len(node['ids']) == len(node['names']) else node['ids'][0]
                labels[source][name] = (targets[source]['reference'], ident, title)
    generated, mappings = {}, []
    for source, tree in trees.items():
        item = targets[source]
        writer = Writer(source, targets, labels, upstream)
        body = writer.anchors(tree) + '\n\n' + writer.block(tree)
        if writer.unquote_lines:
            raise ValueError(f'{source}: stale unquote line selections {writer.unquote_lines}')
        if writer.code_languages:
            raise ValueError(f'{source}: stale code language selections {writer.code_languages}')
        title = item.get('title') or next(tree.findall(nodes.title)).astext()
        header = '\n'.join(['---', 'title: ' + quote(title), 'type: ' + item['type'],
                             'description: ' + quote(item['description']), '---'])
        content = header + '\n\n' + body.strip() + '\n'
        generated[item['destination']] = content
        mappings.append({
            'source': 'Documentation/' + source,
            'source_sha256': hashlib.sha256((source_root/source).read_bytes()).hexdigest(),
            'source_title': next(tree.findall(nodes.title)).astext(),
            'destination': 'docs/' + item['destination'], 'reference': item['reference'],
            'initial_output_sha256': hashlib.sha256(content.encode()).hexdigest(),
            'sections': writer.sections,
            'labels': {name: '#rst-' + val[1] for name, val in labels[source].items()},
            'editorial_layout': {'unquoted_source_lines': item.get('unquote_lines', []),
                                 'code_languages': item.get('code_languages', {})},
            'external_documentation': sorted(writer.external_docs),
            'kernel_doc': [{'path': n['path'], 'options': n['options'], 'source_line': n.line,
                            'source_sha256': hashlib.sha256((root/n['path']).read_bytes()).hexdigest()}
                           for n in tree.findall(KernelDoc)],
            'node_counts': dict(Counter(n.tagname for n in tree.findall())),
            'status': 'converted; editorial review required',
        })
    for name, text in generated.items():
        dest = output / 'docs' / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text)
    manifest = {'schema': 1, 'upstream_commit': upstream, 'kernel_commit': git(root, 'rev-parse', 'HEAD'),
                'source_index': 'Documentation/' + plan['index'],
                'index_destination': plan.get('index_destination'),
                'source_index_sha256': hashlib.sha256((source_root/plan['index']).read_bytes()).hexdigest(),
                'pages': mappings}
    (output/'source-map.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
    print(f'Converted {len(generated)} articles into {output}; original sources unchanged.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kernel-root', type=Path, required=True)
    parser.add_argument('--plan', type=Path, default=Path(__file__).with_name('locking-plan.json'))
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    try:
        convert(args.kernel_root.resolve(), args.plan, args.out)
    except (ValueError, KeyError) as error:
        parser.exit(1, str(error) + '\n')


if __name__ == '__main__':
    main()
