"""Source-preserving wrappers for delivered generators and Trail equations."""
import hashlib
from pathlib import Path
import re
from docutils import nodes
from docutils.parsers.rst import Directive, directives, roles
from docutils.parsers.rst.directives.body import MathBlock
from convert import fence

ROOT=None

class Generated(nodes.General,nodes.Element):
    pass

class Generator(Directive):
    required_arguments=0
    optional_arguments=2
    option_spec={k:directives.flag for k in ('no-files','no-symbols')}
    def run(self):
        options={k:'' for k in self.options}
        if self.name=='kernel-feat':
            if not 1<=len(self.arguments)<=2 or options:raise self.error('unexpected feature arguments/options')
            path=(ROOT/'Documentation'/self.arguments[0]).resolve()
            if not path.is_relative_to(ROOT) or not path.is_dir():raise self.error('missing feature directory')
            argument=str(path.relative_to(ROOT));name=self.name
            if len(self.arguments)==2:options['arch']=self.arguments[1]
        elif self.name=='kernel-abi':
            if len(self.arguments)!=1 or self.arguments[0] not in ('README','stable','testing','obsolete','removed'):raise self.error('unexpected ABI level')
            argument=self.arguments[0];name=self.name
        else:
            if self.arguments or options:raise self.error('maintainers takes no arguments/options')
            argument='';name='kernel-maintainers'
        node=Generated(plugin=name,argument=argument,options=options);node.line=self.lineno
        if name=='kernel-maintainers':
            node['ids']=['maintainers'];node['names']=['maintainers']
        return [node]

class Math(MathBlock):
    option_spec={**MathBlock.option_spec,'nowrap':directives.flag}
    def run(self):
        self.options.pop('nowrap',None)
        return super().run()

def download(name,rawtext,text,lineno,inliner,options=None,content=None):
    current=Path(inliner.document.current_source)
    match=re.fullmatch(r'(.+?)\s*<([^<>]+)>',text)
    caption,target=match.groups() if match else (text,text)
    path=(current.parent/target).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file():
        return [],[inliner.reporter.error('download target outside kernel tree or absent',line=lineno)]
    node=nodes.reference(rawtext,caption,refuri='kernel-download:'+str(path.relative_to(ROOT)))
    return [node],[]

def register(base):
    class UAPIInclude(base):
        option_spec={**base.option_spec,**{k:directives.flag for k in ('generate-cross-refs','toc','warn-broken')},'exception-file':directives.unchanged}
        def run(self):
            if 'generate-cross-refs' not in self.options:return super().run()
            allowed={'generate-cross-refs','toc','warn-broken','exception-file'}
            if set(self.options)-allowed or 'toc' not in self.options:raise self.error('unsupported UAPI options')
            path=(ROOT/self.arguments[0]).resolve()
            if not path.is_relative_to(ROOT) or not path.is_file():raise self.error('missing UAPI header')
            options={k:v or '' for k,v in self.options.items()}
            if 'exception-file' in options:
                current=Path(self.state_machine.get_source_and_line(self.lineno)[0])
                exception=(current.parent/options['exception-file']).resolve()
                if not exception.is_relative_to(ROOT) or not exception.is_file():raise self.error('missing UAPI exception file')
                options['exception-file']=str(exception.relative_to(ROOT))
            node=Generated(plugin='kernel-include',argument=str(path.relative_to(ROOT)),options=options);node.line=self.lineno
            return [node]
    directives.register_directive('kernel-include',UAPIInclude)
    for name in ('kernel-feat','kernel-abi','maintainers-include'):directives.register_directive(name,Generator)
    directives.register_directive('math',Math)
    roles.register_local_role('download',download)

def records(tree):
    return [dict(plugin=n['plugin'],argument=n['argument'],options=n['options'],source_line=n.line) for n in tree.findall(Generated)]

def markdown(n):
    return fence('\n'.join(':'+k+':'+(' '+v if v else '') for k,v in n['options'].items()),'{'+n['plugin']+'}'+(' '+n['argument'] if n['argument'] else ''))

def verify(tree,tokens):
    expected=[(n['plugin'],n['argument'],n['options']) for n in tree.findall(Generated)]
    actual=[]
    for t in tokens:
        if t.type!='fence':continue
        m=re.fullmatch(r'\{(kernel-feat|kernel-abi|kernel-maintainers|kernel-include)\}(?:\s+(.*))?',t.info)
        if not m:continue
        opts={}
        for line in t.content.splitlines():
            if not line.strip():continue
            k,v=line.strip()[1:].split(':',1);opts[k]=v.strip()
        if m[1]=='kernel-include' and 'generate-cross-refs' not in opts:continue
        actual.append((m[1],m[2] or '',opts))
    if actual!=expected:raise ValueError('generated directive path/options/order changed')
    source=[n.astext() for n in tree.findall(nodes.math_block)]
    emitted=[t.content.removesuffix('\n') for t in tokens if t.type=='fence' and t.info=='math']
    if source!=emitted:raise ValueError('display TeX changed')
    source=[n.astext() for n in tree.findall(nodes.math)]
    emitted=[]
    for t in tokens:
        children=t.children or []
        for i,c in enumerate(children):
            if c.type=='code_inline' and i and i+1<len(children) and children[i-1].content.endswith('$') and children[i+1].content.startswith('$'):emitted.append(c.content)
    if source!=emitted:raise ValueError('inline TeX changed')
    return dict(generated_blocks=len(expected),display_equations=len(list(tree.findall(nodes.math_block))),inline_equations=len(source))
