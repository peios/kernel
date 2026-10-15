"""Source-map and rendered-content checks for live Netlink YAML references."""
from collections import Counter
import hashlib
from pathlib import Path
import re
import sys


def verify_wrapper(root, page, markdown):
    record=page['generated_reference']
    if record['kind']!='netlink-yaml' or record['argument']!=page['source']:
        raise ValueError('unknown or inconsistent generated reference')
    source=root/page['source']
    if hashlib.sha256(source.read_bytes()).hexdigest()!=page['source_sha256']:
        raise ValueError(str(source)+': source-map baseline changed; reconcile upstream update')
    if hashlib.sha256(markdown.encode()).hexdigest()!=page['current_output_sha256']:
        raise ValueError(page['destination']+': maintained wrapper changed; review baseline')
    from markdown_it import MarkdownIt
    fences=[t for t in MarkdownIt().parse(markdown.split('---\n',2)[2]) if t.type=='fence']
    if len(fences)!=1 or fences[0].info!='{kernel-netlink} '+page['source'] or fences[0].content.strip():
        raise ValueError('Netlink wrapper must contain exactly its source fence without options/body')
    return {'articles':1,'netlink_yaml_wrappers':1}


def check_rendered(root, plugin, site, pages, complete=False):
    sys.path[:0]=[str(plugin/'.deps'),str(plugin),str(root/'tools/net/ynl/pyynl/lib')]
    from docutils import nodes
    from doc_generator import YnlDocGenerator
    import netlink_markdown
    from verify import Visible,normal
    from check_rendered_preservation import Rendered
    counts=Counter();errors=[]
    if complete:
        expected={str(p.relative_to(root)) for p in (root/'Documentation/netlink/specs').glob('*.yaml')}
        actual=[p['source'] for p in pages]
        if set(actual)!=expected or len(actual)!=len(expected):
            raise ValueError('Netlink wrapper inventory differs from YAML specifications')
    try:
        for page in pages:
            tree=netlink_markdown.parse(YnlDocGenerator().parse_yaml_file(str(root/page['source'])),str(root/page['source']))
            renderer=netlink_markdown.Renderer(tree)
            document=(site/page['reference']/'index.html').read_text()
            html=document.split('<article class="article-body"',1)[1].split('>',1)[1].split('</article>',1)[0]
            visible=Rendered();visible.feed(html);flat=normal(''.join(visible.text))
            def text(node):
                if isinstance(node,netlink_markdown.Reference):
                    return node.astext() or renderer.labels[nodes.fully_normalize_name(node['target'])][1]
                if isinstance(node,nodes.Text):return str(node)
                return ''.join(text(c) for c in node.children)
            for n in tree.findall():
                owner=n.parent;in_contents=False
                while owner is not None:
                    if isinstance(owner,nodes.topic) and 'contents' in owner.get('classes',[]):in_contents=True
                    if isinstance(owner,nodes.system_message):in_contents=True
                    owner=owner.parent
                if in_contents:continue
                if isinstance(n,nodes.title) and isinstance(n.parent,nodes.document):
                    if n.astext()!=page['source_title']:errors.append(page['source']+': wrapper title changed')
                    continue
                if isinstance(n,(nodes.paragraph,nodes.title,nodes.subtitle,nodes.field_name,nodes.term)):
                    if normal(text(n)) not in flat:errors.append(page['source']+': missing generated text: '+text(n)[:120])
                    counts['generated_text_nodes']+=1
                if isinstance(n,nodes.Element) and not isinstance(n,nodes.topic):
                    for anchor in n.get('ids',[]):
                        if 'rst-'+anchor not in visible.ids:errors.append(page['source']+': missing anchor '+anchor)
                        counts['source_anchors']+=1
            expected_code=[n.astext()+'\n' for n in tree.findall(nodes.literal_block)]
            if expected_code!=visible.code_blocks:errors.append(page['source']+': literal examples changed')
            counts['literal_blocks']+=len(expected_code)
            for p in tree.findall(netlink_markdown.Reference):
                anchor=renderer.labels[nodes.fully_normalize_name(p['target'])][0]
                if '#rst-'+anchor not in visible.links:errors.append(page['source']+': missing reference link '+anchor)
                counts['generated_reference_links']+=1
            counts['netlink_yaml_wrappers']+=1
    finally:
        # The migration parser has its own unresolved-reference node type.
        from docutils.parsers.rst import roles
        from convert import xref_role
        roles.register_local_role('ref',xref_role)
    return {'counts':dict(counts),'errors':errors}
