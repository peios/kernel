#!/usr/bin/env python3
"""Stage routine RST imports; reject unsupported constructs without losing sources.

This extends the bounded Locking writer, not the maintained articles. Every
run writes a NEW output directory. Failed pages remain in the source queue.
"""
import argparse
from collections import Counter, defaultdict
import fnmatch
import hashlib
import html
import importlib.util
import json
import os
from pathlib import Path
import posixpath
import re
import signal
import subprocess
import sys
import xml.etree.ElementTree as ET

from docutils import nodes
from docutils.parsers.rst import Directive, directives, roles
from docutils.parsers.rst.directives.misc import Include
from docutils.parsers.rst.directives.misc import Class
from docutils.parsers.rst.directives.images import Figure
from markdown_it import MarkdownIt
from convert import Writer, KernelDoc, Toc, XRef, parse as parse_rst, escape, code, fence, indent, quote, git, roman
from verify import Visible, normal
import diagrams
import live_includes
import generated as generators


class Navigation(Directive):
    has_content = True
    option_spec = {k: directives.unchanged for k in ('maxdepth', 'caption', 'name', 'numbered')}
    option_spec.update({k: directives.flag for k in ('glob', 'hidden', 'titlesonly', 'includehidden', 'reversed')})

    def run(self):
        return [Toc(entries=list(self.content), options=self.options)]


class Metadata(Directive):
    required_arguments = 1
    final_argument_whitespace = True
    def run(self):
        return [nodes.comment('', self.name + ': ' + self.arguments[0])]


KERNEL_ROOT = None
EXPLICIT_LABELS = defaultdict(set)


class LocalInclude(Include):
    """Allow source includes, confined to the kernel tree or Docutils entities."""
    def run(self):
        path=self.arguments[0]
        options=dict(self.options)
        if 'code' in options:
            # Language affects highlighting, not the bytes included from the
            # file. Use the literal reader so its EOF newline stays intact.
            self.options.pop('code');self.options['literal']=None
        if path not in ('<isonum.txt>','<isopub.txt>','<isoamsa.txt>','<isotech.txt>'):
            current=Path(self.state_machine.get_source_and_line(self.lineno)[0])
            target=(current.parent/path).resolve()
            if KERNEL_ROOT is None or not target.is_relative_to(KERNEL_ROOT):
                raise self.error('include outside the kernel source tree')
        settings=self.state.document.settings
        old=settings.file_insertion_enabled
        settings.file_insertion_enabled=True
        try:
            result=super().run()
            if 'literal' in options or 'code' in options:
                allowed={'literal','code','encoding','tab-width','start-line','end-line','start-after','end-before','name','class'}
                if set(options)-allowed:raise self.error('unsupported live include option')
                opts={k:v for k,v in options.items() if k in allowed-{'literal','code','name','class'}}
                opts.setdefault('tab-width',self.state.document.settings.tab_width)
                if 'code' in options:opts['language']=options['code']
                for node in result:
                    if isinstance(node,nodes.literal_block):live_includes.annotate(node,target,opts,self.lineno)
            return result
        finally:settings.file_insertion_enabled=old


class LiteralInclude(LocalInclude):
    option_spec={**LocalInclude.option_spec,'language':directives.unchanged}
    def run(self):
        language=self.options.pop('language',None)
        self.options['literal']=None
        result=super().run()
        for node in result:
            if isinstance(node,nodes.literal_block) and language:node['live_include']['options']['language']=language
        return result


class KernelInclude(LocalInclude):
    def run(self):
        if not any(k in self.options for k in ('literal','code')):raise self.error('nonliteral kernel-include awaits header plugin')
        self.arguments[0]=str(KERNEL_ROOT/self.arguments[0])
        return super().run()


class Declaration(Directive):
    required_arguments=1
    final_argument_whitespace=True
    has_content=True
    option_spec={'noindex':directives.flag,'no-index':directives.flag}
    def run(self):
        # Preserve a hand-written declaration as C, with its nested prose.
        # These are static source declarations, not kernel-doc plugin calls.
        node=nodes.container()
        if not any(k in self.options for k in ('noindex','no-index')):
            node['c_anchor']=constructs.declaration_anchor(self.name.split(':')[1],self.arguments[0])
            node['c_signature']=self.arguments[0]
            node['c_namespace']='::'.join(filter(None,self.state.document.get('c_namespaces',[])))
            node.line=self.lineno
        literal=nodes.literal_block(self.arguments[0],self.arguments[0],classes=['code','c'])
        literal.line=self.lineno
        node+=literal
        self.state.nested_parse(self.content,self.content_offset,node)
        return [node]


class SeeAlso(Directive):
    has_content=True
    def run(self):
        node=nodes.admonition();node+=nodes.title('','See also')
        self.state.nested_parse(self.content,self.content_offset,node)
        return [node]


class Diagram(nodes.General, nodes.Element):
    pass


class EmbeddedSVG(nodes.General, nodes.Element):
    pass


class KernelRender(Directive):
    required_arguments=1
    has_content=True
    option_spec={k:directives.unchanged for k in ('alt','caption','name','width','height','align')}
    def finish(self,node):
        node.line=self.lineno
        self.add_name(node)
        if self.options.get('caption'):
            caption=nodes.caption()
            children,messages=self.state.inline_text(self.options['caption'],self.lineno)
            caption.extend(children);node+=caption;node.extend(messages)
        return [node]

    def run(self):
        if self.arguments[0]=='SVG':
            text='\n'.join(self.content)+'\n'
            svg=ET.fromstring(text)
            allowed={'svg','line','polygon'}
            if any(e.tag.split('}')[-1] not in allowed or any(k.lower().startswith('on') or k in ('href','{http://www.w3.org/1999/xlink}href') for k in e.attrib) for e in svg.iter()):
                raise self.error('embedded SVG needs review')
            return self.finish(EmbeddedSVG(svg=text,options=self.options))
        if self.arguments[0]!='DOT':raise self.error('non-DOT kernel-render needs review')
        node=Diagram(dot='\n'.join(self.content),options=self.options)
        return self.finish(node)


def configure(root):
    global KERNEL_ROOT
    KERNEL_ROOT=root.resolve()
    live_includes.ROOT=KERNEL_ROOT
    generators.ROOT=KERNEL_ROOT
    constructs.configure(KERNEL_ROOT)
    spec=importlib.util.spec_from_file_location('kernel_rst_flat_table',root/'Documentation/sphinx/rstFlatTable.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    directives.register_directive('flat-table',module.FlatTable)
    roles.register_local_role('cspan',module.c_span)
    roles.register_local_role('rspan',module.r_span)


def literal_role(name, rawtext, text, lineno, inliner, options=None, content=None):
    return [nodes.literal(rawtext, text)], []


directives.register_directive('toctree', Navigation)
directives.register_directive('include',LocalInclude)
directives.register_directive('literalinclude',LiteralInclude)
directives.register_directive('kernel-include',KernelInclude)
directives.register_directive('kernel-figure',Figure)
directives.register_directive('kernel-render',KernelRender)
directives.register_directive('cssclass',Class)
directives.register_directive('seealso',SeeAlso)
for name in ('macro','function','type','struct','union','enum','var'):
    directives.register_directive('c:'+name,Declaration)
for name in ('tabularcolumns', 'highlight', 'c:namespace'):
    directives.register_directive(name, Metadata)
for name in ('file', 'command', 'program', 'kbd', 'menuselection', 'guilabel', 'samp', 'c:expr', 'manpage'):
    roles.register_local_role(name, literal_role)

import constructs
generators.register(KernelInclude)


def parse(path):
    text=path.read_text();repairs=[]
    repair_file=Path(__file__).with_name('source-repairs.json')
    if KERNEL_ROOT and path.is_relative_to(KERNEL_ROOT/'Documentation') and repair_file.exists():
        rel=str(path.relative_to(KERNEL_ROOT/'Documentation'))
        record=json.loads(repair_file.read_text()).get(rel)
        if record:
            if hashlib.sha256(path.read_bytes()).hexdigest()!=record['source_sha256']:
                raise ValueError('reviewed source repair needs upstream reconciliation: '+rel)
            for repair in record['repairs']:
                if text.count(repair['before'])!=repair['count']:
                    raise ValueError('source repair occurrence changed: '+rel)
                text=text.replace(repair['before'],repair['after'])
                repairs.append({'kind':'source-repair',**repair})
    tree=parse_rst(path,text)
    tree.setdefault('migration_decisions',[]).extend(repairs)
    return tree


TITLES = {
    'RCU': 'Read-copy-update (RCU)', 'scheduler': 'Scheduling', 'mm': 'Memory management',
    'core-api': 'Core APIs', 'process': 'Development process', 'kbuild': 'Build system',
    'dev-tools': 'Development tools', 'doc-guide': 'Writing documentation',
    'maintainer': 'Maintainer guidance', 'kernel-hacking': 'Kernel programming',
    'admin-guide': 'Administration', 'userspace-api': 'Userspace APIs',
    'hwmon': 'Hardware monitoring', 'driver-api': 'Driver APIs', 'arch': 'CPU architectures',
    'gpu': 'Graphics', 'fb': 'Framebuffer devices', 'iio': 'Industrial I/O',
    'PCI': 'PCI', 'usb': 'USB', 'i2c': 'I²C', 'spi': 'SPI', 'scsi': 'SCSI',
    'bpf': 'BPF', 'virt': 'Virtualisation', 'firmware-guide': 'Firmware',
    'devicetree': 'Device tree', 'w1': '1-Wire', 'wmi': 'WMI', 'hid': 'HID',
    'tee': 'Trusted execution', 'edac': 'Error detection and correction',
    'nvme': 'NVMe', 'nvdimm': 'NVDIMM', 'pcmcia': 'PCMCIA', 'mhi': 'MHI',
    'fpga': 'FPGA', 'peci': 'PECI', 'isdn': 'ISDN', 'cdrom': 'CD-ROM',
    'cpu-freq': 'CPU frequency', 'netlabel': 'Network labelling',
    'misc-devices': 'Miscellaneous devices', 'accel': 'Compute accelerators',
}
DEVELOPMENT = set('process kbuild dev-tools doc-guide maintainer kernel-hacking rust trace fault-injection livepatch'.split())
INTERNALS = set('core-api mm scheduler RCU timers accounting block filesystems networking bpf security crypto virt power cpu-freq netlabel netlink staging'.split())
ADMIN = {'admin-guide', 'tools'}
EXCLUDED = {'sphinx-includes'}
TITLE_OVERRIDES = {'admin-guide/RAS/index.rst':'Reliability, availability and serviceability',
                   'devicetree/bindings/index.rst':'Device tree bindings',
                   'arch/x86/ifs.rst':'In-Field Scan'}
ANTHOLOGIES = {
    'internals': ('200', 'Internals', 'How the kernel coordinates execution, manages resources, and implements its core subsystems.'),
    'development': ('300', 'Kernel development', 'Building, testing, debugging, and contributing to the kernel.'),
    'administration': ('400', 'Administration', 'Configuring, operating, and diagnosing kernel systems.'),
    'hardware': ('500', 'Hardware and drivers', 'Device drivers, processor architectures, firmware, and hardware interfaces.'),
    'userspace': ('600', 'Userspace interfaces', 'Kernel interfaces exposed to applications and userspace services.'),
}

# Reviewed repairs for obsolete DocBook fragment links in the RST source.
# Values are existing source section names or current plugin symbol anchors.
LEGACY_FRAGMENTS = {
    'driver-api/libata.rst': {
        '#exrec': 'eh recovery actions', '#excatATAbusErr': 'ata bus error',
        '#excatDevErr': 'ata/atapi device error (non-ncq / non-check condition)',
        '#excatHSMviolation': 'hsm violation', '#exrecReconf': 'reconfigure transport',
    },
    'driver-api/regulator.rst': {
        '#API-regulator-get': '#c-regulator_get', '#API-regulator-put': '#c-regulator_put',
        '#API-regulator-enable': '#c-regulator_enable', '#API-regulator-disable': '#c-regulator_disable',
    },
}


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def layout(source, rank, categories, folders=None):
    if source in ('index.rst','subsystem-apis.rst'):
        name='upstream-overview' if source=='index.rst' else 'subsystem-apis'
        return {'destination':'kernel.product/300--development.antho/2400--doc-guide.topic/'+str(rank)+'--'+name+'.md',
                'reference':'kernel/development/doc-guide/'+name,'type':'reference','category':'doc-guide','anthology':'development'}
    parts = Path(source).parts
    category = parts[0]
    anth = ('internals' if category in INTERNALS else 'development' if category in DEVELOPMENT
            else 'administration' if category in ADMIN else 'userspace' if category == 'userspace-api' else 'hardware')
    order, _, _ = ANTHOLOGIES[anth]
    base = f'kernel.product/{order}--{anth}.antho'
    if category in ('scheduler', 'RCU'):
        base += '/100--concurrency-and-synchronisation.shelf'
        topic_order = '200' if category == 'scheduler' else '300'
    else:
        topic_order = str(1000 + categories.index(category) * 100)
    topic_slug = slug(category)
    base += f'/{topic_order}--{topic_slug}.topic'
    ref = f'kernel/{anth}/{topic_slug}'
    # Trail topic folders have one level. Preserve deeper source ancestry in
    # the folder's slug; do not invent a sequence of nested topic hierarchies.
    if len(parts) > 2:
        folder = slug('/'.join(parts[1:-1]))
        folder_order = (folders or {}).get(str(Path(source).parent), 50000)
        base += f'/{folder_order}--{folder}'
        ref += '/' + folder
    article = slug(Path(source).stem)
    if Path(source).name=='index.rst':rank=1
    return {'destination': base + f'/{rank}--{article}.md', 'reference': ref + '/' + article,
            'type': 'reference', 'category': category, 'anthology': anth}


class BulkWriter(Writer):
    def __init__(self, source, targets, labels, upstream, all_sources, titles):
        super().__init__(source, targets, labels, upstream)
        self.all_sources, self.titles = all_sources, titles
        self.resolved_refs = []
        self.assets = {}
        self.repaired_links = {}
        self.diagrams = []
        self.c_anchors = []
        self.c_anchor_ids = set()
        self.embedded_assets = {}
        self.live_enabled=True

    def diagram(self,text,path,line=None,options=None):
        mermaid,record=diagrams.convert(text)
        record.update(path=path,source_line=line)
        self.diagrams.append(record)
        options=options or {}
        title=options.get('caption') or options.get('alt')
        return fence(mermaid.rstrip('\n'),'mermaid')+ ('\n\n'+escape(title) if title else '')

    def image(self,node):
        uri=node['uri']
        if uri.startswith(('http://','https://')):
            return '!['+escape(node.get('alt',''))+'](<'+uri+'>)'
        source=Path(node.source or str(KERNEL_ROOT/'Documentation'/self.source))
        path=(source.parent/uri).resolve()
        if KERNEL_ROOT is None or not path.is_relative_to(KERNEL_ROOT) or not path.is_file():
            self.fail(node,'image source missing or outside kernel tree: '+uri)
        if path.suffix.lower()=='.dot':
            return self.diagram(path.read_text(),str(path.relative_to(KERNEL_ROOT)),options={'alt':node.get('alt','')})
        if path.suffix.lower() not in ('.svg','.png','.jpg','.jpeg','.gif','.webp','.avif'):
            self.fail(node,'diagram rendering needs review: '+uri)
        digest=hashlib.sha256(path.read_bytes()).hexdigest()
        name='asset-'+digest[:12]+'-'+slug(path.stem)+path.suffix.lower()
        self.assets[str(path.relative_to(KERNEL_ROOT))]={'path':str(path.relative_to(KERNEL_ROOT)),
            'source_sha256':digest,'destination':str(Path(self.targets[self.source]['destination']).parent/name)}
        return '!['+escape(node.get('alt',''))+']('+name+')'

    def source_path(self, path):
        if path.startswith('Documentation/'):
            return path[len('Documentation/'):]
        if path.startswith('/'):
            return path.lstrip('/')
        return posixpath.normpath(posixpath.join(posixpath.dirname(self.source), path))

    def doc_link(self, path):
        rel = self.source_path(path)
        if rel not in self.all_sources:
            raise ValueError('missing documentation target '+rel)
        if rel in self.targets:
            return '~' + self.targets[rel]['reference']
        self.external_docs.add(rel)
        return f'https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/{rel}?id={self.upstream}'

    def prose(self,text):
        pattern=r'(?<![\w/.-])(?:Documentation/[\w./-]+\.(?:rst|txt)|[\w-]+\.rst)(?!\w)'
        parts=[];end=0
        for match in re.finditer(pattern,text):
            name=match.group();parts.append(escape(text[end:match.start()]))
            if self.source_path(name) in self.all_sources:
                parts.append('['+escape(name)+']('+self.doc_link(name)+')')
            else:parts.append(escape(name))
            end=match.end()
        return ''.join(parts)+escape(text[end:])

    def inline_children(self,node):
        parts=[self.anchors(node)]
        for child in node.children:
            rendered=self.inline(child)
            if not rendered:continue
            # Adjacent code spans otherwise merge their closing/opening ticks.
            if parts and parts[-1].endswith('`') and rendered.startswith('`'):
                parts.append('<!-- -->')
            parts.append(rendered)
        return ''.join(parts)

    def inline(self,node):
        aliases=self.anchors(node) if isinstance(node,nodes.Element) else ''
        return aliases+self.render_inline(node)

    def render_inline(self, node):
        if isinstance(node,nodes.math):return "$"+code(node.astext())+"$"
        if isinstance(node,nodes.generated):return self.inline_children(node)
        if isinstance(node,nodes.image):return self.image(node)
        if isinstance(node,nodes.target):return self.inline_children(node)
        if isinstance(node,(nodes.emphasis,nodes.strong)):
            # RST allows punctuation-adjacent emphasis that Markdown does not,
            # e.g. *ioctl()*s. Inline HTML preserves the exact source boundary.
            tag='em' if isinstance(node,nodes.emphasis) else 'strong'
            return '<'+tag+'>'+self.inline_children(node)+'</'+tag+'>'
        if isinstance(node, XRef):
            text = node.astext()
            match = re.fullmatch(r'(.+?)\s*<([^<>]+)>', text, re.S)
            caption, target = match.groups() if match else (text, text)
            caption=normal(caption);target=normal(target)
            if node['kind'] == 'doc':
                path = target if target.endswith('.rst') else target + '.rst'
                source = self.source_path(path)
                if source not in self.all_sources:
                    self.fail(node, f'missing documentation target {source}')
                caption = caption if match else self.titles.get(source, caption)
                dest = self.doc_link(path)
            else:
                target=nodes.fully_normalize_name(target)
                found = self.labels.get(self.source, {}).get(target)
                if found is None and ':' in target and node['kind']=='ref':
                    doc,section=target.rsplit(':',1)
                    found=self.labels.get(doc+'.rst',{}).get(section)
                if found is None:
                    explicit=EXPLICIT_LABELS.get(target,set())
                    candidates = [v[target] for source,v in self.labels.items() if target in v and (not explicit or source in explicit)]
                    if len(candidates) == 1:
                        found = candidates[0]
                if found is None:
                    self.fail(node, f'unresolved or ambiguous :ref: {target}')
                source, anchor, title = found
                caption = caption if match or node['kind']=='term' else title
                if source == self.source:
                    dest = '#rst-' + anchor
                elif source in self.targets:
                    dest = '~' + self.targets[source]['reference'] + ('#' if anchor.startswith('abi-file-') else '#rst-') + anchor
                else:
                    dest = self.doc_link('/' + source)
            self.resolved_refs.append({'role': node['kind'], 'source_text': text, 'caption': caption, 'target': dest})
            return f'[{escape(caption)}](<{dest}>)'
        if isinstance(node, nodes.reference):
            dest = node.get('refuri', '')
            if dest.startswith('kernel-download:'):
                path=dest.removeprefix('kernel-download:')
                return '['+self.inline_children(node)+'](https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/'+path+'?id='+self.upstream+')'
            if dest.startswith('file:'):
                name=dest.removeprefix('file:')
                candidates=[(KERNEL_ROOT/name).resolve(),(KERNEL_ROOT/'Documentation'/self.source).parent.joinpath(name).resolve()]
                path=next((p for p in candidates if p.is_relative_to(KERNEL_ROOT) and p.exists()),None)
                if path is None:self.fail(node,'missing file reference: '+dest)
                rel=str(path.relative_to(KERNEL_ROOT))
                replacement=f'https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/{rel}?id={self.upstream}'
                self.repaired_links[dest]=replacement
                return '['+escape(node.astext())+'](<'+replacement+'>)'
            repair=LEGACY_FRAGMENTS.get(self.source,{}).get(dest)
            if repair:
                replacement=repair if repair.startswith('#') else '#rst-'+self.labels[self.source][repair][1]
                self.repaired_links[dest]=replacement
                return '['+self.inline_children(node)+']('+replacement+')'
            if dest and not re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', dest) and not dest.startswith('#'):
                # Files linked from RST must not become broken relative URLs.
                path, sep, fragment = dest.partition('#')
                rel = self.source_path(path)
                if rel in self.all_sources or path.endswith(('.rst', '.txt', '.yaml')):
                    dest = self.doc_link(path)
                    # Source HTML fragments have no reliable RST-to-Trail alias.
                    if fragment:
                        self.fail(node, 'relative file link with fragment needs review')
                    return '[' + self.inline_children(node) + '](<' + dest + '>)'
                if path.endswith('.html'):
                    rst=self.source_path(path[:-5]+'.rst')
                    found=next((v for v in self.labels.get(rst,{}).values() if v[1]==fragment),None)
                    if rst in self.targets and (not fragment or found):
                        replacement='~'+self.targets[rst]['reference']+('#rst-'+fragment if fragment else '')
                        self.repaired_links[dest]=replacement
                        return '['+self.inline_children(node)+'](<'+replacement+'>)'
                source=(KERNEL_ROOT/'Documentation'/self.source).parent if KERNEL_ROOT else None
                candidate=(source/path).resolve() if source else None
                if candidate and candidate.is_relative_to(KERNEL_ROOT) and candidate.is_file() and not fragment:
                    replacement=f'https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/{candidate.relative_to(KERNEL_ROOT)}?id={self.upstream}'
                    self.repaired_links[dest]=replacement
                    return '['+self.inline_children(node)+'](<'+replacement+'>)'
                self.fail(node, f'relative asset or HTML link needs review: {dest}')
        if isinstance(node, (nodes.subscript, nodes.superscript)):
            tag = 'sub' if isinstance(node, nodes.subscript) else 'sup'
            return f'<{tag}>' + html.escape(node.astext()) + f'</{tag}>'
        if isinstance(node, nodes.abbreviation):
            return escape(node.astext())
        if isinstance(node,nodes.citation_reference):
            return '['+self.inline_children(node)+'](#rst-'+node['refid']+')'
        return super().inline(node)

    def table(self, node):
        result = [self.anchors(node), '<table>']
        for group in node.children:
            if isinstance(group, nodes.title):
                result.extend(['<caption>','',self.inline_children(group),'','</caption>'])
                continue
            if not isinstance(group, nodes.tgroup):
                self.fail(group, 'unsupported table child')
            stubs={i for i,c in enumerate(group.children) if isinstance(c,nodes.colspec) and c.get('stub')}
            occupied={};row_index=0
            for part in group.children:
                if isinstance(part, nodes.colspec):
                    continue
                if not isinstance(part, (nodes.thead, nodes.tbody)):
                    self.fail(part, 'unsupported table group')
                tag = 'thead' if isinstance(part, nodes.thead) else 'tbody'
                result.append(f'<{tag}>')
                for row in part.children:
                    result.append('<tr>')
                    column=0
                    for cell in row.children:
                        while occupied.get((row_index,column)):column+=1
                        is_stub=column in stubs
                        celltag = 'th' if tag == 'thead' or is_stub else 'td'
                        attrs = ''.join(f' {attr}="{cell[key]+1}"' for key, attr in (
                            ('morecols', 'colspan'), ('morerows', 'rowspan')) if key in cell)
                        if is_stub and tag!='thead':attrs+=' scope="row"'
                        result.extend([f'<{celltag}{attrs}>', '', self.anchors(row) if column==0 else '',self.anchors(cell),self.blocks(cell.children), '', f'</{celltag}>'])
                        for dr in range(cell.get('morerows',0)+1):
                            for dc in range(cell.get('morecols',0)+1):occupied[(row_index+dr,column+dc)]=True
                        column+=cell.get('morecols',0)+1
                    result.append('</tr>')
                    row_index+=1
                result.append(f'</{tag}>')
        return '\n'.join(result + ['</table>'])

    def block(self,node,depth=1):
        aliases=self.anchors(node) if isinstance(node,nodes.Element) else ''
        rendered=self.render_block(node,depth)
        return aliases+'\n\n'+rendered if aliases else rendered

    def render_block(self, node, depth=1):
        if isinstance(node,generators.Generated):return generators.markdown(node)
        if isinstance(node,nodes.math_block):return fence(node.astext(),"math")
        if isinstance(node,nodes.Element) and node.get('live_include') and self.live_enabled:
            return live_includes.markdown(node['live_include'])
        if isinstance(node,EmbeddedSVG):
            data=node['svg'].encode();digest=hashlib.sha256(data).hexdigest()
            name='asset-'+digest[:12]+'-embedded.svg'
            destination=str(Path(self.targets[self.source]['destination']).parent/name)
            self.embedded_assets[destination]=data
            self.assets[destination]={'path':'Documentation/'+self.source,'source_sha256':hashlib.sha256((KERNEL_ROOT/'Documentation'/self.source).read_bytes()).hexdigest(),
                'destination':destination,'asset_sha256':digest,'embedded_source_line':node.line}
            options=node['options']
            return '!['+escape(options.get('alt',''))+']('+name+')'+ ('\n\n'+self.blocks(node.children) if node.children else '')
        if isinstance(node,nodes.container) and node.get('c_anchor'):
            anchor=node['c_anchor'];prefix=''
            if anchor not in self.c_anchor_ids:
                self.c_anchor_ids.add(anchor)
                prefix='<a id="'+anchor+'"></a>\n\n'
                self.c_anchors.append({'anchor':anchor,'signature':node['c_signature'],
                                      'namespace':node.get('c_namespace',''),'source_line':node.line})
            return prefix+self.blocks(node.children,depth)
        if isinstance(node,nodes.attribution):return '— '+self.inline_children(node)
        if isinstance(node,nodes.doctest_block):return fence(node.astext(),'pycon')
        if isinstance(node,nodes.option_list):
            return '\n\n'.join('- '+code(item.children[0].astext())+'\n\n'+indent(self.blocks(item.children[1].children,depth),'  ') for item in node.children)
        if isinstance(node,nodes.title) and isinstance(node.parent,nodes.document):
            notes=list(node.findall(nodes.footnote_reference))
            if notes:
                # Frontmatter is plain text. Keep a title's live footnote links
                # immediately below it rather than losing their target aliases.
                return 'Title notes: '+', '.join(self.inline(n) for n in notes)
            return ''
        if isinstance(node,Diagram):
            options={k:v for k,v in node['options'].items() if k!='caption'}
            return self.diagram(node['dot'],'Documentation/'+self.source,node.line,options)+ ('\n\n'+self.blocks(node.children) if node.children else '')
        if isinstance(node,nodes.image):return self.image(node)
        if isinstance(node,(nodes.figure,nodes.legend)):return self.blocks(node.children,depth)
        if isinstance(node,nodes.caption):return self.inline_children(node)
        if isinstance(node,nodes.paragraph):
            # RST source wrapping is not a Markdown list or setext heading.
            text=self.inline_children(node).replace('\n',' ')
            text=re.sub(r'^(\s*\d+)([.)])(?=\s)',r'\1\\\2',text)
            text=re.sub(r'^(\s*)([-+])(?=\s|$|-)',r'\1\\\2',text)
            return text
        if isinstance(node,nodes.substitution_definition):
            # Docutils has already expanded every use in the document tree.
            return ''
        if isinstance(node,nodes.rubric):
            return '**'+self.inline_children(node)+'**'
        if isinstance(node,nodes.citation):
            return self.anchors(node)+'\n\n**['+node.children[0].astext()+']** '+self.blocks(node.children[1:],depth)
        if isinstance(node,(nodes.bullet_list,nodes.enumerated_list)):
            items=[]
            for i,child in enumerate(node.children,node.get('start',1)):
                content=self.blocks(child.children,depth)
                marker='- ' if isinstance(node,nodes.bullet_list) else str(i)+'. '
                kind=node.get('enumtype','arabic')
                if kind!='arabic':
                    if kind in ('lowerroman','upperroman'):
                        number=roman(i);number=number.upper() if kind=='upperroman' else number
                    elif kind in ('loweralpha','upperalpha') and 1<=i<=26:
                        number=chr(ord('a' if kind=='loweralpha' else 'A')+i-1)
                    else:self.fail(node,'unsupported enumeration')
                    marker='- ';content='**'+node['prefix']+number+node['suffix']+'** '+content
                # Begin with the actual block (including a fence), not a blank
                # list item: a blank item before "10." makes its four-space
                # continuation parse as indented code instead of a code fence.
                lines=(content.strip('\n') or '<!-- empty source list item -->').split('\n')
                items.append(marker+lines[0]+ ('\n'+indent('\n'.join(lines[1:]),' '*len(marker)) if len(lines)>1 else ''))
            return '\n\n'.join(items)
        if isinstance(node, Toc):
            entries = []
            options = node.get('options', {})
            for raw in node['entries']:
                raw = raw.strip()
                if not raw:
                    continue
                match = re.fullmatch(r'(.+)\s+<([^>]+)>', raw)
                caption, target = match.groups() if match else ('', raw)
                if '://' in target:
                    entries.append('- [' + escape(caption or target) + '](<' + target + '>)')
                    continue
                if target == 'self':
                    target = '/' + self.source
                if not target.endswith(('.rst', '.txt')):
                    target += '.rst'
                paths = [self.source_path(target)]
                if 'glob' in options:
                    paths = sorted(p for p in self.all_sources if fnmatch.fnmatch(p, paths[0]))
                    if not paths:
                        self.fail(node, 'empty toctree glob')
                for p in paths:
                    if p not in self.all_sources:
                        self.fail(node, f'missing toctree target {p}')
                    entries.append('- [' + escape(caption or self.titles.get(p, Path(p).stem)) + '](<' + self.doc_link('/' + p) + '>)')
            if 'reversed' in options:
                entries.reverse()
            if 'numbered' in options:
                entries=[str(i)+'. '+entry[2:] for i,entry in enumerate(entries,1)]
            prefix = '**' + escape(options['caption']) + '**\n\n' if options.get('caption') else ''
            return prefix + '\n'.join(entries)
        if isinstance(node, nodes.literal_block):
            classes = [c for c in node.get('classes', []) if c != 'code']
            return self.anchors(node) + '\n\n' + fence(node.astext(), classes[0] if len(classes) == 1 else 'text')
        if isinstance(node, nodes.Admonition):
            kind = {'warning':'WARNING', 'caution':'CAUTION', 'danger':'CAUTION', 'error':'CAUTION',
                    'important':'IMPORTANT', 'tip':'TIP', 'hint':'TIP'}.get(node.tagname, 'NOTE')
            children = list(node.children)
            title = ''
            if children and isinstance(children[0], nodes.title):
                title = '**' + self.inline_children(children.pop(0)) + '**\n\n'
            return '> [!' + kind + ']\n>\n' + indent(title + self.blocks(children, depth), '> ')
        if isinstance(node, nodes.line_block):
            def lines(block,level=0):
                result=[]
                for child in block.children:
                    if isinstance(child,nodes.line):
                        text=self.inline_children(child)
                        text=re.sub(r'^(\d+)([.)])(?=\s)',r'\1\\\2',text)
                        result.append(('&nbsp;'*4*level)+text)
                    elif isinstance(child,nodes.line_block):result.extend(lines(child,level+1))
                    else:self.fail(child,'unsupported line block child')
                return result
            return '<br>\n'.join(lines(node))
        if isinstance(node, nodes.topic):
            # contents is navigation, not source prose; Trail generates a TOC.
            if 'contents' in node.get('classes', []):
                return self.anchors(node)
            children=list(node.children)
            title=''
            if children and isinstance(children[0],nodes.title):
                title='**'+self.inline_children(children.pop(0))+'**\n\n'
            return self.anchors(node) + '\n\n' + title + self.blocks(children, depth)
        if isinstance(node, (nodes.container, nodes.compound)):
            return self.anchors(node) + '\n\n' + self.blocks(node.children, depth)
        if isinstance(node, nodes.subtitle):
            return '## ' + self.inline_children(node)
        if isinstance(node, nodes.definition_list):
            items=[]
            for item in node.children:
                if not isinstance(item.children[-1], nodes.definition):
                    self.fail(item, 'definition list without definition')
                terms=' : '.join(self.inline_children(c) for c in item.children[:-1])
                items.append('- **' + terms + '**\n\n' + indent(self.blocks(item.children[-1].children, depth), '  '))
            return '\n\n'.join(items)
        return super().block(node, depth)


def verify_page(tree, body, writer, rewrites=None):
    """Check every visible prose node and every literal block after Markdown parsing.

    Cross-reference labels are checked against their independently indexed source
    titles. Unlike the Locking verifier, no cross-reference paragraphs are skipped.
    """
    body=live_includes.expand(body,live_includes.records(tree))
    md=MarkdownIt('commonmark', {'html':True}).enable('table')
    rewrites=rewrites or {}
    visible=Visible();visible.feed(md.render(re.sub(r'\$(`+[^\n]*?`+)\$',r'\1',body)));flat=normal(''.join(visible.text))
    def expected(node):
        if isinstance(node,XRef):
            matches=[r['caption'] for r in writer.resolved_refs if r['role']==node['kind'] and r['source_text']==node.astext()]
            if not matches:raise ValueError('missing resolved reference')
            return matches[0]
        if isinstance(node,nodes.Text):return node.astext()
        return ''.join(expected(c) for c in node.children)
    counts=Counter(generators.verify(tree,md.parse(body)))
    for n in tree.findall():
        if live_includes.csv_owner(n) is not None:continue
        if any(isinstance(p,(nodes.system_message,nodes.comment,nodes.substitution_definition)) for p in ancestors(n)):
            continue
        if any(isinstance(p,nodes.topic) and 'contents' in p.get('classes',[]) for p in ancestors(n)):
            continue
        if isinstance(n,nodes.paragraph):
            if normal(rewrites.get(normal(n.astext()),expected(n))) not in flat:
                raise ValueError(f'prose preservation failed at line {n.line}: {n.astext()[:100]}')
            counts['paragraphs']+=1
        elif isinstance(n,(nodes.term,nodes.classifier,nodes.field_name,nodes.subtitle,nodes.line,nodes.rubric,nodes.caption)) or (isinstance(n,nodes.title) and not isinstance(n.parent,nodes.document) and not (isinstance(n.parent,nodes.topic) and 'contents' in n.parent.get('classes',[]))):
            if normal(rewrites.get(normal(n.astext()),expected(n))) not in flat:
                raise ValueError(f'heading/term preservation failed: {n.astext()[:100]}')
            counts['headings_and_terms']+=1
    old=[n.astext() for n in tree.findall() if isinstance(n,(nodes.literal_block,nodes.doctest_block))]
    new=[t.content.removesuffix('\n') for t in md.parse(body) if t.type in ('fence','code_block') and not t.info.startswith('{') and t.info not in ('mermaid','math')]
    if old!=new:raise ValueError('literal-block content/order changed')
    if len(list(tree.findall(nodes.table)))!=visible.counts['table']:raise ValueError('table count changed')
    images=[n for n in tree.findall(nodes.image) if not any(isinstance(a,nodes.substitution_definition) for a in ancestors(n))]
    if len([n for n in images if not n['uri'].endswith('.dot')])+len(list(tree.findall(EmbeddedSVG)))!=visible.counts['img']:raise ValueError('image count changed')
    expected_diagrams=len(list(tree.findall(Diagram)))+len([n for n in images if n['uri'].endswith('.dot')])
    rendered_diagrams=[t.content for t in md.parse(body) if t.type=='fence' and t.info=='mermaid']
    if expected_diagrams!=len(rendered_diagrams):raise ValueError('diagram count changed')
    if [hashlib.sha256(m.encode()).hexdigest() for m in rendered_diagrams]!=[d['mermaid_sha256'] for d in writer.diagrams]:raise ValueError('diagram rewrite changed')
    for n in tree.findall():
        if isinstance(n,nodes.Element) and n.get('c_anchor') and n['c_anchor'] not in visible.ids:
            raise ValueError('missing C anchor '+n['c_anchor'])
        if isinstance(n,nodes.Element) and n.get('ids') and not any(isinstance(a,(nodes.topic,nodes.substitution_definition)) for a in ancestors(n)):
            for anchor in n.get('ids',[]):
                if 'rst-'+anchor not in visible.ids:raise ValueError('missing anchor '+anchor)
    counts.update(literal_blocks=len(old),tables=visible.counts['table'],images=visible.counts['img'],diagrams=expected_diagrams)
    for record in live_includes.records(tree):
        if 'csv' not in record['options']:continue
        for row in live_includes.csv_values(record):
            for cell in row:
                if normal(cell) not in flat:raise ValueError('live CSV cell missing: '+cell)
                counts['csv_cells']+=1
    counts['live_includes']=len(live_includes.records(tree))
    return dict(counts)


def ancestors(node):
    while node.parent is not None:
        node=node.parent
        yield node


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--kernel-root',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--exclude',type=Path,help='JSON object of sources to leave queued, with reasons')
    args=ap.parse_args();root=args.kernel_root.resolve();out=args.out
    configure(root)
    if out.exists():ap.error('output already exists')
    out.mkdir(parents=True)
    old=json.loads((root/'peios/docs-migration/source-map.json').read_text())
    accounted={p['source'].removeprefix('Documentation/'):p for p in old.get('non_article_sources',[])}
    upstream=old['upstream_commit'];all_sources={str(p.relative_to(root/'Documentation')) for p in (root/'Documentation').rglob('*') if p.is_file()}
    categories=sorted({p.relative_to(root/'docs-to-translate').parts[0] for p in (root/'docs-to-translate').rglob('*.rst') if len(p.relative_to(root/'docs-to-translate').parts)>1})
    folders={name:1000000+i*100 for i,name in enumerate(sorted({str(Path(s).parent) for s in all_sources if s.endswith('.rst')}))}
    trees={};titles={};labels={};failures={};targets={};configs={}
    excluded=json.loads(args.exclude.read_text()) if args.exclude else {}
    for oldpage in old['pages']:
        source=oldpage['source'].removeprefix('Documentation/')
        targets[source]={**oldpage,'destination':oldpage['destination'].removeprefix('docs/')}
        titles[source]=oldpage['source_title']
        labels[source]={name:(source,anchor.removeprefix('#rst-').removeprefix('#'),name) for name,anchor in oldpage['labels'].items()}
    files=sorted((root/'docs-to-translate').rglob('*.rst'))
    for i,p in enumerate(files):
        source=str(p.relative_to(root/'docs-to-translate'))
        if source in targets:continue
        if source in accounted:
            if hashlib.sha256((root/'Documentation'/source).read_bytes()).hexdigest()!=accounted[source]['source_sha256']:
                failures[source]='accounted non-article source changed; review its disposition'
            continue
        if source in excluded:
            failures[source]=excluded[source];continue
        if Path(source).parts[0] in EXCLUDED:
            failures[source]='Editorial placement or source fragment: retain for review';continue
        try:
            if p.read_bytes()!=(root/'Documentation'/source).read_bytes():
                raise ValueError('queued source differs from original; needs editorial reconciliation')
            tree=parse(root/'Documentation'/source)
            title=next((n.astext() for n in tree.children if isinstance(n,nodes.title)),None)
            if not title:
                title=next((n.astext() for n in tree.findall(nodes.title)),None)
            if not title and source.endswith('/features.rst'):
                title='Feature status on '+Path(source).parts[1]+' architecture' if source.startswith('arch/') else 'Kernel feature support matrix'
            if not title and source=='process/maintainers.rst':title='Maintainers'
            if not title and source in TITLE_OVERRIDES:
                title=TITLE_OVERRIDES[source]
                tree.setdefault('migration_decisions',[]).append({'kind':'wrapper-title','title':title})
            if not title:raise ValueError('no document title; may be an included fragment')
            trees[source]=tree;titles[source]=title
            targets[source]=layout(source,(i+1)*100,categories,folders)
            labels[source]={}
            for n in tree.findall(nodes.Element):
                ids=n.get('ids',[])
                for j,name in enumerate(n.get('names',[])):
                    if ids:
                        label_title=n.children[0].astext() if isinstance(n,nodes.section) else title if isinstance(n,nodes.document) else name
                        labels[source][name]=(source,ids[j] if len(ids)==len(n['names']) else ids[0],label_title)
        except Exception as e:
            failures[source]=str(e)
        if i%250==0:print(f'Parsed {i}/{len(files)}: {len(trees)} candidates',flush=True)
    # Index explicit labels on unconverted pages as source links, avoiding a
    # cascade of exclusions merely because a neighbouring page needs a feature.
    for source in sorted(all_sources):
        if not source.endswith('.rst'):continue
        text=(root/'Documentation'/source).read_text(errors='replace')
        explicit=[nodes.fully_normalize_name(m.group(1)) for m in re.finditer(r'^\.\. _([^:]+):\s*$',text,re.M)]
        for name in explicit:EXPLICIT_LABELS[name].add(source)
        if source not in labels:labels[source]={name:(source,name,name) for name in explicit}
    if 'admin-guide/abi-testing-files.rst' in targets:
        labels['admin-guide/abi-testing-files.rst']['abi_file_testing_sysfs_class_platform_profile']=('admin-guide/abi-testing-files.rst','abi-file-testing-sysfs-class-platform-profile','sysfs-class-platform-profile')
    if 'admin-guide/abi-testing-files.rst' in targets:
        labels['admin-guide/abi-testing-files.rst']['abi_file_testing_sysfs_class_hwmon']=('admin-guide/abi-testing-files.rst','abi-file-testing-sysfs-class-hwmon','sysfs-class-hwmon')
    if 'process/maintainers.rst' in targets:
        EXPLICIT_LABELS['maintainers'].add('process/maintainers.rst')
    candidates=set(trees)
    while True:
        generated={};mappings={};rejected={};embedded={}
        refs=[t['reference'] for s,t in targets.items() if s in candidates]
        if len(refs)!=len(set(refs)):raise ValueError('destination identity collision')
        for source in sorted(candidates):
            tree=trees[source];item=targets[source]
            try:
                writer=BulkWriter(source,targets,labels,upstream,all_sources,titles)
                body=(writer.anchors(tree)+'\n\n'+writer.block(tree)).strip()+'\n'
                checked=verify_page(tree,body,writer)
                paras=[normal(n.astext()) for n in tree.findall(nodes.paragraph) if not any(isinstance(a,(nodes.field_list,nodes.Admonition,nodes.table)) for a in ancestors(n))]
                description=(paras[0][:240].rsplit(' ',1)[0]+'…' if paras and len(paras[0])>240 else paras[0] if paras else 'Reference for '+titles[source]+'.')
                content='---\ntitle: '+quote(titles[source])+'\ntype: reference\ndescription: '+quote(description)+'\n---\n\n'+body
                digest=hashlib.sha256(content.encode()).hexdigest()
                deps=[{'path':n['path'],'options':n['options'],'source_line':n.line,'source_sha256':hashlib.sha256((root/n['path']).read_bytes()).hexdigest()} for n in tree.findall(KernelDoc)]
                includes=[]
                for dep in tree.settings.record_dependencies.list:
                    path=Path(dep).resolve()
                    if path.is_relative_to(root):includes.append({'path':str(path.relative_to(root)),'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
                generated[source]=content
                embedded.update(writer.embedded_assets)
                mappings[source]={'source':'Documentation/'+source,'source_sha256':hashlib.sha256((root/'Documentation'/source).read_bytes()).hexdigest(),'source_title':titles[source],
                    'destination':'docs/'+item['destination'],'reference':item['reference'],'initial_output_sha256':digest,'current_output_sha256':digest,
                    'sections':writer.sections,'labels':{k:('#' if v[1].startswith('abi-file-') else '#rst-')+v[1] for k,v in labels[source].items()},'external_documentation':sorted(writer.external_docs),'kernel_doc':deps,
                    'source_dependencies':includes+list(writer.assets.values())+[{'path':d['path'],'source_sha256':hashlib.sha256((root/d['path']).read_bytes()).hexdigest()} for d in writer.diagrams],
                    'diagrams':writer.diagrams,'assets':list(writer.assets.values()),'resolved_references':writer.resolved_refs,'reviewed_link_replacements':writer.repaired_links,
                    'c_declarations':writer.c_anchors,'migration_decisions':tree.get('migration_decisions',[]),
                    'live_includes':live_includes.records(tree),'generated':generators.records(tree),
                    'validation':checked,'status':'mechanically converted and preservation verified; editorial review pending'}
            except Exception as e:rejected[source]=str(e)
        print(f'Rendered {len(generated)}; rejected {len(rejected)}',flush=True)
        if not rejected:break
        failures.update(rejected)
        for source in rejected:candidates.remove(source);targets.pop(source,None)
    for source,content in generated.items():
        item=targets[source];p=out/'docs'/item['destination'];p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content)
        for asset in mappings[source]['assets']:
            dest=out/'docs'/asset['destination'];dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_bytes(embedded[asset['destination']] if 'embedded_source_line' in asset else (root/asset['path']).read_bytes())
        topic=next(a for a in p.parents if a.suffix=='.topic')
        configs[topic]={'title':TITLES.get(item['category'],item['category'].replace('-',' ').capitalize())}
        if p.parent!=topic:configs[p.parent]={'title':Path(source).parent.as_posix().split('/',1)[1].replace('/',' / ')}
        anth=next(a for a in p.parents if a.suffix=='.antho')
        _,title,desc=ANTHOLOGIES[item['anthology']];configs[anth]={'title':title,'description':desc}
        for a in p.parents:
            if a.suffix=='.shelf':configs[a]={'title':'Concurrency and synchronisation'}
    for directory,config in configs.items():
        # Existing shared configuration is not replaced on installation.
        (directory/'trail.toml').write_text(''.join(k+' = '+quote(v)+'\n' for k,v in config.items()))
    old['pages'].extend(mappings[s] for s in sorted(mappings))
    old['mechanical_batch']={'converted':len(mappings),'queued':len(failures),'source_queue_retained':True,'validation':'per-page prose, literal blocks, tables and source anchors checked; full site build pending'}
    (out/'source-map.json').write_text(json.dumps(old,indent=2)+'\n')
    (out/'pending.json').write_text(json.dumps(failures,indent=2)+'\n')
    (out/'plan.json').write_text(json.dumps({s:targets[s] for s in sorted(mappings)},indent=2)+'\n')
    print(json.dumps(old['mechanical_batch']),flush=True)


if __name__=='__main__':
    main()
