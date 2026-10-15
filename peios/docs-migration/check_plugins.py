#!/usr/bin/env python3
"""Validate each mapped page's plugin blocks and record actual source dependencies.

Each page is evaluated separately for dependency attribution; the complete Trail
build still evaluates all pages together to validate cross-page symbol links.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import subprocess


def check(root,page):
    request={'protocol':1,'blocks':[{'id':str(i),'file':page['destination'],'line':d['source_line'] or 1,
        'reference':page['reference'],'argument':d['path'],'options':d['options'],'body':''}
        for i,d in enumerate(page['kernel_doc'])]}
    directory=Path(os.environ.get('KERNEL_DOC_PLUGIN_DIR',root/'tools/docs/trail-kernel-doc'))
    proc=subprocess.run(['python3',str(directory/'trail-kernel-doc'),'--srctree',str(root)],
        input=json.dumps(request),text=True,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
    if proc.returncode:return page['source'],{'error':proc.stderr}
    response=json.loads(proc.stdout)
    errors=[b for b in response['blocks'] if 'error' in b]
    if errors:return page['source'],{'error':errors,'warnings':proc.stderr}
    dependencies=[]
    for name in response['depends_on']:
        path=Path(name).resolve()
        if path.is_relative_to(root):rel=str(path.relative_to(root))
        elif path.is_relative_to(directory):rel='tools/docs/trail-kernel-doc/'+str(path.relative_to(directory))
        else:raise ValueError('unexpected plugin dependency '+str(path))
        dependencies.append({'path':rel,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    return page['source'],{'dependencies':dependencies,'warnings':proc.stderr,'blocks':len(request['blocks'])}


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--kernel-root',type=Path,required=True);ap.add_argument('--mapping',type=Path,required=True);ap.add_argument('--report',type=Path,required=True);args=ap.parse_args()
    root=args.kernel_root.resolve();mapping=json.loads(args.mapping.read_text())
    pages=[p for p in mapping['pages'] if p['kernel_doc']]
    with ThreadPoolExecutor(max_workers=4) as pool:
        results=dict(pool.map(lambda p:check(root,p),pages))
    args.report.write_text(json.dumps(results,indent=2)+'\n')
    for page in pages:
        result=results[page['source']]
        if 'error' not in result:page['plugin_dependencies']=result['dependencies']
    args.mapping.write_text(json.dumps(mapping,indent=2)+'\n')
    print(json.dumps({'pages':len(pages),'failed':[p for p,r in results.items() if 'error' in r],'pages_with_warnings':sum(bool(r.get('warnings')) for r in results.values())}))
    raise SystemExit(any('error' in r for r in results.values()))
