"""Bounded RST constructs for the one-way import, never runtime generators."""
import re
from pathlib import Path
from docutils import nodes
from docutils.parsers.rst import Directive, directives, roles
from docutils.parsers.rst.directives.tables import CSVTable
from convert import XRef, xref_role
import live_includes

ROOT = None


def audit(directive, kind, **details):
    document = directive.state.document
    document.setdefault('migration_decisions', []).append(dict(
        kind=kind, source=document.current_source, line=directive.lineno, **details))


class WebRaw(Directive):
    required_arguments = 1
    has_content = True

    def run(self):
        # Only the complete, inspected set of LaTeX layout commands is omitted.
        allowed = {r'\footnotesize', r'\normalsize', r'\scriptsize', r'\small',
                   r'\tiny', r'\begingroup', r'\endgroup',
                   r'\setlength{\tabcolsep}{2pt}', r'\renewcommand\thesection*',
                   r'\renewcommand\thesubsection*'}
        text = '\n'.join(self.content)
        if self.arguments != ['latex'] or any(s.strip() not in allowed for s in self.content if s.strip()):
            raise self.error('raw content requires explicit review')
        audit(self, 'omit-latex-layout', content=text)
        return [nodes.comment('', 'Source LaTeX layout: ' + text)]


class WebConditional(Directive):
    required_arguments = 1
    final_argument_whitespace = True
    has_content = True

    def run(self):
        expressions = {"builder != 'latex'": True, "builder == 'latex'": False,
                       'rustdoc and html': False, 'not rustdoc and html': True}
        expression = self.arguments[0]
        if expression not in expressions:
            raise self.error('unreviewed web condition: ' + expression)
        enabled = expressions[expression]
        audit(self, 'web-condition', expression=expression, included=enabled,
              content='\n'.join(self.content))
        node = nodes.container()
        if enabled:
            self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class LocalCSV(CSVTable):
    def run(self):
        if 'url' in self.options:
            raise self.error('remote CSV input is not allowed')
        if 'file' not in self.options:
            return super().run()
        current = Path(self.state_machine.get_source_and_line(self.lineno)[0])
        path = (current.parent / self.options['file']).resolve()
        if ROOT is None or not path.is_relative_to(ROOT) or not path.is_file():
            raise self.error('CSV input missing or outside kernel tree')
        settings = self.state.document.settings
        previous = settings.file_insertion_enabled
        settings.file_insertion_enabled = True
        try:
            result=super().run()
            allowed={'file','header-rows','widths','encoding'}
            if set(self.options)-allowed or self.arguments or self.content:
                raise self.error('file-backed CSV options need live-include review')
            options={'csv':'','header-rows':self.options.get('header-rows',0)}
            if 'encoding' in self.options:options['encoding']=self.options['encoding']
            for node in result:
                if isinstance(node,nodes.table):live_includes.annotate(node,path,options,self.lineno)
            return result
        finally:
            settings.file_insertion_enabled = previous


class Glossary(Directive):
    has_content = True
    option_spec = {'sorted': directives.flag}

    def run(self):
        node = nodes.container()
        self.state.nested_parse(self.content, self.content_offset, node)
        # Sphinx accepts a blank line between a glossary term and definition.
        # Docutils calls that a paragraph followed by a block quote.
        children=list(node.children);node.children=[];i=0
        while i<len(children):
            child=children[i]
            if isinstance(child,nodes.paragraph) and i+1<len(children) and isinstance(children[i+1],nodes.block_quote):
                term=nodes.term();term.extend(child.children)
                definition=nodes.definition();definition.extend(children[i+1].children)
                listing=nodes.definition_list();item=nodes.definition_list_item()
                item.extend([term,definition]);listing+=item;node+=listing;i+=2
            else:node+=child;i+=1
        if not all(isinstance(c, (nodes.definition_list, nodes.comment)) for c in node.children):
            raise self.error('glossary is not a definition list')
        for term in node.findall(nodes.term):
            name = nodes.fully_normalize_name(term.astext())
            ident = 'term-' + nodes.make_id(name)
            term['ids'].append(ident)
            term['names'].append(name)
        if 'sorted' in self.options:
            for listing in node.findall(nodes.definition_list):
                listing.children.sort(key=lambda item: item.children[0].astext().casefold())
        return [node]


class SourceCode(Directive):
    optional_arguments = 1
    has_content = True
    option_spec = {'caption': directives.unchanged, 'emphasize-lines': directives.unchanged,
                   'name': directives.unchanged, 'class': directives.class_option}

    def run(self):
        self.assert_has_content()
        text = '\n'.join(self.content)
        node = nodes.literal_block(text, text, classes=['code', self.arguments[0] if self.arguments else 'text'])
        node.line = self.lineno
        self.add_name(node)
        result = []
        if 'caption' in self.options:
            caption = nodes.caption()
            children, messages = self.state.inline_text(self.options['caption'], self.lineno)
            caption.extend(children)
            result.extend([caption, *messages])
        if 'emphasize-lines' in self.options:
            value = self.options['emphasize-lines']
            if not re.fullmatch(r'\d+(?:-\d+)?(?:\s*,\s*\d+(?:-\d+)?)*', value):
                raise self.error('invalid emphasize-lines')
            audit(self, 'code-emphasis-deferred', lines=value)
        return result + [node]


class Namespace(Directive):
    optional_arguments = 1
    def run(self):
        stack = self.state.document.setdefault('c_namespaces', [''])
        if self.name == 'c:namespace-pop':
            if len(stack) < 2:
                raise self.error('C namespace stack underflow')
            stack.pop()
        elif self.name == 'c:namespace-push':
            stack.append(self.arguments[0])
        else:
            stack[:] = [self.arguments[0] if self.arguments else '']
        return [nodes.comment('', self.name + ': ' + '::'.join(filter(None, stack)))]


def declaration_anchor(kind, signature):
    """Extract only supported declaration forms; reject rather than misidentify."""
    signature = signature.replace('\\\n', ' ').strip().rstrip(';')
    if kind in ('struct', 'union', 'enum'):
        match = re.fullmatch(r'(?:(?:struct|union|enum)\s+)?([A-Za-z_]\w*)', signature)
        if match:
            return 'c-' + kind + '-' + match[1]
    elif kind == 'function':
        match = re.match(r'^[\w\s*]+?\b([A-Za-z_]\w*)\s*\(', signature)
        if match:
            return 'c-' + match[1]
    elif kind == 'macro':
        match = re.match(r'^([A-Za-z_]\w*)(?:\s*\(|$)', signature)
        if match:
            return 'c-' + match[1]
    elif kind in ('type', 'var'):
        match = re.fullmatch(r'([A-Za-z_]\w*)', signature)
        if match:
            return 'c-' + match[1]
        # Actual tagged types have separate anchors; typedef declarations use
        # their alias, including function-pointer typedefs.
        match = re.fullmatch(r'(struct|union|enum)\s+([A-Za-z_]\w*)', signature)
        if match:
            return 'c-' + match[1] + '-' + match[2]
        match = re.fullmatch(r'typedef\s+.+\(\s*\*\s*(\w+)\s*\)\s*\(.*\)', signature)
        if match:
            return 'c-' + match[1]
        match = re.fullmatch(r'[\w\s*]+?\b([A-Za-z_]\w*)(?:\s*\[[\d\s]*\])?', signature)
        if match:
            return 'c-' + match[1]
    raise ValueError('C declaration needs anchor review: ' + kind + ' ' + signature)


def configure(root):
    global ROOT
    ROOT = root.resolve()


for name, cls in [('raw', WebRaw), ('only', WebConditional), ('ifconfig', WebConditional),
                  ('csv-table', LocalCSV), ('glossary', Glossary), ('code-block', SourceCode),
                  ('c:namespace', Namespace), ('c:namespace-push', Namespace), ('c:namespace-pop', Namespace)]:
    directives.register_directive(name, cls)
roles.register_local_role('term', xref_role)
