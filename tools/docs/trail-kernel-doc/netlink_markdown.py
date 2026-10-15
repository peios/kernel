# SPDX-License-Identifier: GPL-2.0
"""Strict Markdown output for the kernel's generated Netlink RST.

Protocol semantics remain in YnlDocGenerator. Docutils handles RST structure;
unhandled nodes and unresolved references fail instead of dropping content.
"""
import io
import re

from docutils import nodes
from docutils.core import publish_doctree
from docutils.parsers.rst import roles


class Reference(nodes.Inline, nodes.TextElement):
    pass


def reference_role(name, rawtext, text, lineno, inliner, options=None, content=None):
    match = re.fullmatch(r'(.*?)\s*<([^<>]+)>', text)
    caption, target = match.groups() if match else ('', text)
    return [Reference(rawtext, caption, target=target)], []


def escape(value):
    return re.sub(r'([\\`*_\[\]<>|~!&#$])', r'\\\1', value)


def code(value):
    fence = '`' * (max((len(m[0]) for m in re.finditer(r'`+', value)), default=0) + 1)
    pad = ' ' if value.startswith(('`', ' ')) or value.endswith(('`', ' ')) else ''
    return fence + pad + value + pad + fence


def literal(value):
    fence = '`' * max(3, 1 + max((len(m[0]) for m in re.finditer(r'`+', value)), default=0))
    return fence + 'text\n' + value + '\n' + fence


def parse(rst, source):
    roles.register_local_role('ref', reference_role)
    # Sphinx's parser_yaml removes these source-position markers before RST
    # parsing too. Leaving them in would terminate nested field-list bodies.
    rst = re.sub(r'^\.\. LINENO \d+\n', '', rst, flags=re.M)
    diagnostics = io.StringIO()
    tree = publish_doctree(rst, source_path=source, settings_overrides={
        'file_insertion_enabled': False, 'raw_enabled': False,
        'halt_level': 5, 'report_level': 2, 'warning_stream': diagnostics,
        'doctitle_xform': True,
    })
    if diagnostics.getvalue().strip():
        raise ValueError(diagnostics.getvalue().strip())
    return tree


class Renderer:
    def __init__(self, tree):
        self.tree = tree
        self.emitted = set()
        self.labels = {}
        for node in tree.findall(nodes.Element):
            ids = node.get('ids', [])
            if not ids:
                continue
            title = next((c.astext() for c in node.children if isinstance(c, nodes.title)), None)
            for name in node.get('names', []):
                named_id = nodes.make_id(name)
                self.labels[nodes.fully_normalize_name(name)] = (named_id if named_id in ids else ids[0], title or name)

    def anchors(self, node):
        result = []
        for anchor in node.get('ids', []):
            if anchor in self.emitted:
                continue
            if not re.fullmatch(r'[a-zA-Z0-9_.:-]+', anchor):
                raise ValueError('unexpected RST anchor: ' + anchor)
            self.emitted.add(anchor)
            result.append(f'<a id="rst-{anchor}"></a>')
        return '\n'.join(result)

    def inline(self, node):
        if isinstance(node, nodes.Text):
            return escape(str(node))
        text = ''.join(self.inline(c) for c in node.children)
        if isinstance(node, Reference):
            target = nodes.fully_normalize_name(node['target'])
            if target not in self.labels:
                raise ValueError('unresolved Netlink reference: ' + node['target'])
            anchor, title = self.labels[target]
            return f'[{text or escape(title)}](#rst-{anchor})'
        if isinstance(node, nodes.literal):
            return code(node.astext())
        if isinstance(node, nodes.strong):
            return '**' + text + '**'
        if isinstance(node, (nodes.emphasis, nodes.title_reference)):
            return '*' + text + '*'
        if isinstance(node, nodes.reference):
            target = node.get('refuri') or ('#rst-' + node['refid'] if node.get('refid') else None)
            if target is None:
                raise ValueError('unresolved RST hyperlink: ' + node.astext())
            return f'[{text}](<{target}>)'
        if isinstance(node, nodes.target):
            return self.anchors(node)
        raise ValueError('unsupported Netlink inline node: ' + node.tagname)

    def children(self, node, depth):
        return '\n\n'.join(part for c in node.children if (part := self.block(c, depth)))

    def block(self, node, depth=1):
        if isinstance(node, nodes.document):
            # The wrapper owns the document title; retain its source labels.
            return self.anchors(node) + '\n\n' + '\n\n'.join(
                part for c in node.children if not isinstance(c, nodes.title)
                and (part := self.block(c, depth)))
        if isinstance(node, nodes.section):
            return self.anchors(node) + '\n\n' + self.children(node, depth + 1)
        if isinstance(node, (nodes.title, nodes.subtitle)):
            level = 2 if isinstance(node, nodes.subtitle) else depth
            return self.anchors(node) + '\n\n' + '#' * min(level, 6) + ' ' + ''.join(self.inline(c) for c in node.children)
        if isinstance(node, nodes.paragraph):
            return self.anchors(node) + '\n\n' + ''.join(self.inline(c) for c in node.children)
        if isinstance(node, nodes.literal_block):
            return literal(node.astext())
        if isinstance(node, (nodes.bullet_list, nodes.enumerated_list)):
            result = []
            for i, item in enumerate(node.children, node.get('start', 1)):
                marker = f'{i}. ' if isinstance(node, nodes.enumerated_list) else '- '
                content = self.children(item, depth).strip().split('\n')
                result.append(marker + content[0] + '\n' + '\n'.join(' '*len(marker)+s if s else '' for s in content[1:]))
            return '\n\n'.join(result)
        if isinstance(node, nodes.field_list):
            result = []
            for field in node.children:
                key, value = field.children
                content = self.children(value, depth).strip()
                title = '**' + ''.join(self.inline(c) for c in key.children) + '**'
                if content:
                    result.append('- ' + title + ':\n\n' + '\n'.join('  '+s if s else '' for s in content.split('\n')))
                else:
                    result.append('- ' + title)
            return '\n\n'.join(result)
        if isinstance(node, nodes.definition_list):
            return '\n\n'.join(self.block(c, depth) for c in node.children)
        if isinstance(node, nodes.definition_list_item):
            term = node.children[0]
            definition = node.children[-1]
            if len(node.children) != 2:
                raise ValueError('unsupported definition classifier')
            title = ''.join(self.inline(c) for c in term.children)
            if not any(term.findall(nodes.strong)):
                title = '**' + title + '**'
            return title + '\n\n' + self.children(definition, depth)
        if isinstance(node, nodes.block_quote):
            return '\n'.join('> '+s if s else '>' for s in self.children(node, depth).split('\n'))
        if isinstance(node, nodes.target):
            return self.anchors(node)
        if isinstance(node, nodes.topic) and 'contents' in node.get('classes', []):
            return ''  # Trail supplies navigation from the generated headings.
        if isinstance(node, nodes.comment):
            if node.astext().startswith('SPDX-License-Identifier:'):
                return '<!-- ' + node.astext() + ' -->'
            if node.astext().startswith(('LINENO ', 'NOTE: This document was auto-generated.')):
                return ''
            raise ValueError('unrecognised generated comment: ' + node.astext())
        if isinstance(node, nodes.system_message) and node['level'] < 2:
            return ''
        if isinstance(node, nodes.transition):
            return '---'
        raise ValueError('unsupported Netlink block node: ' + node.tagname)


def render(rst, source):
    tree = parse(rst, source)
    return Renderer(tree).block(tree)
