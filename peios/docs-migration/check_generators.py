#!/usr/bin/env python3
"""Validate delivered generator requests and record file/directory dependencies."""
import argparse
from collections import defaultdict
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
from html import unescape

def directory_entries(path):
    return sorted(str(p.relative_to(path)) for p in path.rglob('*') if p.is_file() and not any(c.startswith('.') for c in p.relative_to(path).parts))

def dependency(root,plugin,path):
    p=Path(path).resolve()
    if p.is_relative_to(root):rel=str(p.relative_to(root))
    elif p.is_relative_to(plugin):rel='tools/docs/trail-kernel-doc/'+str(p.relative_to(plugin))
    else:raise ValueError('unexpected dependency '+str(p))
    if p.is_dir():
        entries=directory_entries(p)
        return {'path':rel,'kind':'directory','entries':entries,'source_sha256':hashlib.sha256(json.dumps(entries,separators=(',',':')).encode()).hexdigest()}
    return {'path':rel,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

def check(root,plugin,site,mapping,out):
    anchors={};groups=defaultdict(list);owners={}
    for page in mapping['pages']:
        html=(site/page['reference']/'index.html').read_text()
        article=html.split('<article class="article-body"',1)[1].split('</article>',1)[0]
        anchors[page['reference']]=[unescape(v) for v in re.findall(r'\bid="([^"]+)"',article)]
        for item in page.get('generated',[]):
            block={'id':str(len(owners)),'file':page['destination'],'line':item['source_line'] or 1,'reference':page['reference'],'argument':item['argument'],'options':item['options'],'body':''}
            groups[item['plugin']].append(block);owners[block['id']]=page
    report={};out.mkdir(exist_ok=True)
    for name,blocks in groups.items():
        request={'protocol':1,'blocks':blocks}
        if name=='kernel-include':request['anchors']=anchors
        result=subprocess.run(['python3',str(plugin/('trail-'+name)),'--srctree',str(root)],input=json.dumps(request),text=True,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
        if result.returncode:raise ValueError(result.stderr)
        response=json.loads(result.stdout)
        assert [b['id'] for b in response['blocks']]==[b['id'] for b in blocks]
        assert all('error' not in b for b in response['blocks']),response['blocks']
        if name=='kernel-include' and result.stderr.strip():raise ValueError('UAPI diagnostics: '+result.stderr)
        deps=[dependency(root,plugin,p) for p in response['depends_on']]
        if name=='kernel-binding':
            import sys
            sys.path[:0]=[str(plugin/'.deps'),str(plugin)]
            from binding_schema import Registry
            registry=Registry(root)
            shared=[d for d,p in zip(deps,response['depends_on']) if Path(p).resolve() not in registry.by_path]
            for d in shared:
                if d.get('kind')=='directory':d['membership_only']=True
            mapping.setdefault('dependency_groups',{})['device-tree-bindings']={
                'dependencies':shared,'destinations':sorted({owners[b['id']]['destination'] for b in blocks})}
            for block in blocks:
                doc=registry.requested(block['argument'])
                owners[block['id']]['generator_dependencies']=[dependency(root,plugin,p) for p in sorted(registry.closure(doc))]
        else:
            for block in blocks:owners[block['id']]['generator_dependencies']=deps
        (out/(name+'.json')).write_text(json.dumps({'request':request,'response':response,'stderr':result.stderr},indent=2)+'\n')
        report[name]={'blocks':len(blocks),'pages':len({b['file'] for b in blocks}),'dependencies':len(deps),'directory_dependencies':[d['path'] for d in deps if d.get('kind')=='directory'],'warnings':result.stderr,'errors':0}
    return report

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--kernel-root',type=Path,required=True);ap.add_argument('--plugin',type=Path,required=True);ap.add_argument('--site',type=Path,required=True);ap.add_argument('--mapping',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args();mapping=json.loads(a.mapping.read_text());result=check(a.kernel_root,a.plugin,a.site,mapping,a.out)
    a.mapping.write_text(json.dumps(mapping,indent=2)+'\n');(a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:{a:b for a,b in v.items() if a!='warnings'} for k,v in result.items()}))
