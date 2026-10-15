# SPDX-License-Identifier: GPL-2.0
"""Load authored DT schemas without flattening conditions or following the network."""
from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path
import re
from urllib.parse import unquote, urldefrag, urljoin

import yaml

HERE=Path(__file__).resolve().parent
LIBRARY=HERE/'schema-library/dtschema-2026.9/schemas'


class Loader(yaml.CSafeLoader):
    pass


# The bindings declare YAML 1.2, not YAML 1.1's yes/no/on/off or dates.
Loader.yaml_implicit_resolvers=deepcopy(yaml.CSafeLoader.yaml_implicit_resolvers)
for c,entries in Loader.yaml_implicit_resolvers.items():
    Loader.yaml_implicit_resolvers[c]=[(tag,rx) for tag,rx in entries if tag not in
        ('tag:yaml.org,2002:bool','tag:yaml.org,2002:timestamp','tag:yaml.org,2002:int')]
Loader.add_implicit_resolver('tag:yaml.org,2002:bool',re.compile(r'^(?:true|false|True|False|TRUE|FALSE)$'),list('tTfF'))
Loader.add_implicit_resolver('tag:yaml.org,2002:int',re.compile(r'^[-+]?(?:0[xX][0-9a-fA-F_]+|0[oO][0-7_]+|0[bB][01_]+|[0-9][0-9_]*)$'),list('-+0123456789'))


def integer(loader,node):
    value=loader.construct_scalar(node).replace('_','');digits=value.lstrip('-+')
    return int(value,0 if digits.lower().startswith(('0x','0o','0b')) else 10)


def mapping(loader,node):
    result={}
    for key_node,value_node in node.value:
        key=loader.construct_object(key_node)
        if not isinstance(key,str):raise ValueError('schema mapping key is not a string')
        if key in result:raise ValueError('duplicate YAML key: '+key)
        result[key]=loader.construct_object(value_node)
    return result


Loader.add_constructor('tag:yaml.org,2002:int',integer)
Loader.add_constructor('tag:yaml.org,2002:map',mapping)


def pointer(parent,key):
    return parent+'/'+str(key).replace('~','~0').replace('/','~1')


def anchor(ptr):
    return 'dt-root' if ptr=='' else 'dt-'+hashlib.sha256(ptr.encode()).hexdigest()[:20]


def nodes(value,ptr='',parents=()):
    if isinstance(value,(dict,list)):
        if id(value) in parents:raise ValueError('recursive YAML alias')
        parents=(*parents,id(value))
    yield ptr,value
    if isinstance(value,dict):
        for key,child in value.items():yield from nodes(child,pointer(ptr,key),parents)
    elif isinstance(value,list):
        for i,child in enumerate(value):yield from nodes(child,pointer(ptr,i),parents)
    elif not isinstance(value,(str,int,float,bool,type(None))) or isinstance(value,float) and not math.isfinite(value):
        raise ValueError('non-JSON schema value at '+ptr)


def comments(text):
    """YAML comments outside scalar tokens, including inline comments.

    Scalar token ranges exclude comments but include quoted # and literal DTS
    blocks. Thus #address-cells and example comments remain example contents.
    """
    spans=sorted((t.start_mark.index,t.end_mark.index) for t in yaml.scan(text,Loader=Loader)
                 if isinstance(t,yaml.tokens.ScalarToken))
    result=[];j=0;offset=0
    for line_number,line in enumerate(text.splitlines(keepends=True),1):
        for match in re.finditer('#',line):
            pos=offset+match.start()
            while j<len(spans) and spans[j][1]<=pos:j+=1
            if j<len(spans) and spans[j][0]<=pos<spans[j][1]:continue
            result.append({'line':line_number,'text':line[match.start()+1:].rstrip('\r\n')});break
        offset+=len(line)
    return result


class Document:
    def __init__(self,path):
        self.path=path.resolve();self.text=path.read_text()
        self.data=yaml.load(self.text,Loader=Loader)
        if not isinstance(self.data,dict) or not isinstance(self.data.get('$id'),str) or not isinstance(self.data.get('title'),str):
            raise ValueError(str(path)+': schema needs $id and title')
        self.uri=urldefrag(self.data['$id'])[0]
        if not self.uri.startswith('http://devicetree.org/schemas/'):
            raise ValueError(str(path)+': unexpected schema namespace')
        self.index=dict(nodes(self.data));self.comments=comments(self.text)
        self.refs=[(p,v) for p,v in self.index.items() if p.endswith('/$ref')]
        for p,v in self.index.items():
            if p.endswith('/$id') and p!='/\u0024id':raise ValueError('nested schema $id is unsupported')
        ids=[anchor(p) for p in self.index]
        if len(ids)!=len(set(ids)):raise ValueError('schema anchor collision')


class Registry:
    def __init__(self,root,library=LIBRARY):
        self.root=root.resolve();self.directory=(self.root/'Documentation/devicetree/bindings').resolve()
        self.library=library.resolve();self.by_path={};self.by_uri={}
        for directory in (self.directory,self.library):
            for path in sorted(directory.rglob('*.yaml')):
                if not path.resolve().is_relative_to(directory):raise ValueError('schema symlink escapes library')
                doc=Document(path)
                if doc.uri in self.by_uri:raise ValueError('duplicate schema identifier: '+doc.uri)
                self.by_path[doc.path]=doc;self.by_uri[doc.uri]=doc

    def requested(self,argument):
        name=Path(argument)
        if name.is_absolute() or '..' in name.parts:raise ValueError('schema path must be kernel-relative without traversal')
        if argument.startswith('tools/docs/trail-kernel-doc/schema-library/'):
            path=(HERE/Path(argument).relative_to('tools/docs/trail-kernel-doc')).resolve()
        else:path=(self.root/name).resolve()
        if path not in self.by_path:raise ValueError('expected a registered binding or shared-library YAML file')
        return self.by_path[path]

    def resolve(self,doc,reference):
        if not isinstance(reference,str):raise ValueError('$ref must be a string')
        uri,fragment=urldefrag(urljoin(doc.uri,reference));ptr=unquote(fragment)
        if uri not in self.by_uri:raise ValueError('unresolved schema reference: '+reference+' in '+doc.uri)
        target=self.by_uri[uri]
        if ptr and not ptr.startswith('/'):raise ValueError('unsupported named schema fragment: '+reference)
        if ptr not in target.index:raise ValueError('unresolved schema pointer: '+reference+' in '+doc.uri)
        return target,ptr

    def closure(self,doc):
        visited=set();pending=[doc]
        while pending:
            current=pending.pop()
            if current.path in visited:continue
            visited.add(current.path)
            pending.extend(self.resolve(current,ref)[0] for _,ref in current.refs)
        return visited

    def source(self,doc):
        if doc.path.is_relative_to(self.directory):return str(doc.path.relative_to(self.root))
        return 'tools/docs/trail-kernel-doc/schema-library/dtschema-2026.9/schemas/'+str(doc.path.relative_to(self.library))
