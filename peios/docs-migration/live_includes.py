"""Live include annotations and independent preservation checks."""
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
from docutils import nodes
from convert import fence
from markdown_it import MarkdownIt

ROOT=None


def annotate(node,path,options,line):
    if ROOT is None or not path.is_relative_to(ROOT):raise ValueError('live include outside kernel tree')
    record={'path':str(path.relative_to(ROOT)), 'options':{k:str(v) if v is not None else '' for k,v in options.items()},
            'source_line':line,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    node['live_include']=record
    return node


def markdown(record):
    body='\n'.join(':'+k+':'+(' '+v if v else '') for k,v in record['options'].items())
    return fence(body,'{kernel-include} '+record['path'])


def records(tree):
    return [n['live_include'] for n in tree.findall(nodes.Element) if n.get('live_include')]


def csv_owner(node):
    while node is not None:
        if isinstance(node,nodes.Element) and 'csv' in node.get('live_include',{}).get('options',{}):return node
        node=node.parent
    return None


def csv_values(record):
    text=(ROOT/record['path']).read_text(encoding=record['options'].get('encoding','utf-8'))
    return [[c.strip() for c in row] for row in csv.reader(io.StringIO(text),skipinitialspace=True) if row]


def evaluate(items):
    directory=Path(os.environ.get('KERNEL_INCLUDE_PLUGIN_DIR',ROOT/'tools/docs/trail-kernel-doc'))
    blocks=[dict(id=str(i),file='preservation-check',line=r.get('source_line') or 1,reference='kernel/check',
                 argument=r['path'],options=r['options'],body='') for i,r in enumerate(items)]
    run=subprocess.run(['python3',str(directory/'trail-kernel-include'),'--srctree',str(ROOT)],
        input=json.dumps({'protocol':1,'blocks':blocks}),capture_output=True,text=True,
        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
    if run.returncode:raise ValueError(run.stderr)
    result=json.loads(run.stdout)
    if len(result['blocks'])!=len(items):raise ValueError('include plugin result count changed')
    for i,b in enumerate(result['blocks']):
        if b['id']!=str(i) or 'error' in b:raise ValueError(str(b))
    return result


def expand(body,expected):
    """Check every fence against the RST declaration before evaluating it."""
    tokens=[t for t in MarkdownIt('commonmark',{'html':True}).parse(body) if t.type=='fence' and t.info.startswith('{kernel-include}') and not re.search(r'^:generate-cross-refs:',t.content,re.M)]
    if len(tokens)!=len(expected):raise ValueError('live include count differs from source')
    for token,r in zip(tokens,expected):
        if token.info!='{kernel-include} '+r['path']:raise ValueError('live include path differs from source')
        parsed={}
        for line in token.content.splitlines():
            if not line.strip():continue
            m=re.fullmatch(r':([\w-]+):\s*(.*)',line)
            if not m or m[1] in parsed:raise ValueError('invalid live include options')
            parsed[m[1]]=m[2]
        if parsed!=r['options']:raise ValueError('live include options differ from source')
    if not tokens:return body
    result=evaluate(expected)
    pieces=body.split('\n');lines=[s+'\n' for s in pieces[:-1]]+[pieces[-1]]
    for token,block in reversed(list(zip(tokens,result['blocks']))):
        start,end=token.map;prefix=lines[start].split('`',1)[0]
        rendered=block['markdown'].rstrip('\n').split('\n')
        lines[start:end]=[prefix+line+'\n' for line in rendered]
    return ''.join(lines)
