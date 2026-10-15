"""Check maintained binding wrappers and every rendered source value."""
from collections import Counter
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_wrapper(root,page,markdown,plugin=None):
    source=page['source'];plugin=plugin or root/'tools/docs/trail-kernel-doc'
    path=plugin/Path(source).relative_to('tools/docs/trail-kernel-doc') if source.startswith('tools/docs/trail-kernel-doc/') else root/source
    if page['generated_reference']!={'kind':'device-tree-binding','argument':source}:raise ValueError('inconsistent binding wrapper')
    if sha(path)!=page['source_sha256']:raise ValueError('binding source changed; review source-map baseline')
    if hashlib.sha256(markdown.encode()).hexdigest()!=page['current_output_sha256']:raise ValueError('maintained binding wrapper changed')
    from markdown_it import MarkdownIt
    fences=[t for t in MarkdownIt().parse(markdown.split('---\n',2)[2]) if t.type=='fence']
    if len(fences)!=1 or fences[0].info!='{kernel-binding} '+source or fences[0].content.strip():raise ValueError('binding wrapper must contain exactly its source fence')
    return {'articles':1,'device_tree_binding_wrappers':1}


class Content(HTMLParser):
    """Collect source IDs, text positions and individual example bodies."""
    def __init__(self):
        super().__init__(convert_charrefs=True);self.text=[];self.ids={};self.links=[];self.example=None;self.examples={};self.length=0
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'id' in attrs:
            if attrs['id'] in self.ids:raise ValueError('duplicate rendered ID '+attrs['id'])
            self.ids[attrs['id']]=self.length
        if tag=='a' and 'href' in attrs:self.links.append(attrs['href'])
        if tag=='pre' and attrs.get('id','').startswith('dt-'):
            self.example=attrs['id'];self.examples[self.example]=[]
        if tag in ('p','div','h1','h2','h3','h4','h5','h6','li','br','pre'):self.append('\n',False)
    def handle_endtag(self,tag):
        if tag=='pre':self.example=None
        if tag in ('p','div','h1','h2','h3','h4','h5','h6','li','pre'):self.append('\n',False)
    def append(self,text,example=True):
        self.text.append(text);self.length+=len(text)
        if example and self.example is not None:self.examples[self.example].append(text)
    def handle_data(self,text):self.append(text)


def walk(value,path=''):
    yield path,value
    if isinstance(value,dict):
        for key,child in value.items():yield from walk(child,path+'/'+str(key).replace('~','~0').replace('/','~1'))
    elif isinstance(value,list):
        for i,child in enumerate(value):yield from walk(child,path+'/'+str(i))


def check_document(doc,source_data,html,page,registry,pages):
    from binding_schema import anchor
    from verify import normal
    if source_data!=doc.data:raise ValueError('independent YAML 1.2 parse differs from plugin parser')
    if page['source_title']!=source_data['title']:raise ValueError('wrapper title differs from schema')
    if '<article class="article-body"' in html:
        html=html.split('<article class="article-body"',1)[1].split('>',1)[1].split('</article>',1)[0]
    parsed=Content();parsed.feed(html);text=''.join(parsed.text);counts=Counter()
    index=dict(walk(source_data));positions=sorted((offset,key) for key,offset in parsed.ids.items() if key.startswith('dt-'))
    bounds={key:(offset,positions[i+1][0] if i+1<len(positions) else len(text)) for i,(offset,key) in enumerate(positions)}
    for ptr,value in index.items():
        ident=anchor(ptr)
        if ident not in bounds:raise ValueError('missing schema node '+ptr)
        counts['schema_nodes']+=1
        if isinstance(value,(dict,list)):continue
        if ptr=='/title':
            if normal(value) not in normal(text):raise ValueError('missing page title')
            continue
        start,end=bounds[ident];visible=normal(text[start:end])
        if ptr.rsplit('/',1)[-1]=='description':expected=normal(value)
        elif re.fullmatch(r'.*/examples/\d+',ptr) and isinstance(value,str):
            if ''.join(parsed.examples.get(ident,[]))!=value:raise ValueError('literal example changed: '+ptr)
            counts['examples']+=1;expected=normal(value)
        elif ptr.endswith('/$ref'):
            target,fragment=registry.resolve(doc,value)
            href=('#' if target.path==doc.path else '~'+pages[target.path]+'#')+anchor(fragment)
            # Trail turns ~ references into site-absolute links.
            if href not in parsed.links and href.replace('~','/',1) not in parsed.links:raise ValueError('missing reference '+ptr)
            counts['references']+=1;expected=normal(value)
        else:expected=normal(json.dumps(value,ensure_ascii=False,allow_nan=False))
        if expected not in visible:raise ValueError('source value missing at '+ptr+': '+expected[:100])
        counts['scalar_values']+=1
    for i,comment in enumerate(doc.comments):
        key='dt-comment-'+str(i)
        if key not in bounds:raise ValueError('missing source comment')
        a,b=bounds[key]
        if normal(comment['text']) not in normal(text[a:b]):raise ValueError('source comment changed')
        counts['comments']+=1
    counts['articles']+=1
    return dict(counts)


def check_rendered(root,plugin,site,pages):
    import sys
    sys.path[:0]=[str(plugin/'.deps'),str(plugin)]
    from ruamel.yaml import YAML
    from binding_schema import Registry
    oracle=YAML(typ='safe',pure=True);oracle.version=(1,2)
    registry=Registry(root)
    refs={registry.requested(p['source']).path:p['reference'] for p in pages}
    counts=Counter();errors=[]
    for page in pages:
        try:
            doc=registry.requested(page['source'])
            counts.update(check_document(doc,oracle.load(doc.text),(site/page['reference']/'index.html').read_text(),page,registry,refs))
        except Exception as error:errors.append({'source':page['source'],'error':str(error)})
    return {'counts':dict(counts),'errors':errors}
