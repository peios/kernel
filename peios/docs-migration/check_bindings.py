#!/usr/bin/env python3
"""Independently check binding schemas, wrapper coverage and rendered references."""
import argparse
from collections import Counter
import html
import json
from pathlib import Path
import sys


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for name in ['kernel-root','plugin','docs','mapping','out']:ap.add_argument('--'+name,type=Path,required=True)
    ap.add_argument('--site',type=Path);ap.add_argument('--oracle-deps',type=Path)
    ap.add_argument('--complete',action='store_true')
    a=ap.parse_args();sys.path[:0]=[str(a.plugin/'.deps'),str(a.plugin)]
    if a.oracle_deps:sys.path.insert(0,str(a.oracle_deps))
    from ruamel.yaml import YAML
    from markdown_it import MarkdownIt
    from binding_schema import Registry
    from binding_markdown import Renderer
    from binding_references import verify_wrapper,check_document
    oracle=YAML(typ='safe',pure=True);oracle.version=(1,2)
    registry=Registry(a.kernel_root,a.plugin/'schema-library/dtschema-2026.9/schemas')
    mapping=json.loads(a.mapping.read_text());pages=[p for p in mapping['pages'] if p.get('generated_reference',{}).get('kind')=='device-tree-binding']
    owners={registry.requested(p['source']).path:p for p in pages}
    if len(owners)!=len(pages):raise ValueError('duplicate binding wrappers')
    if a.complete:
        roots=[d for d in registry.by_path.values() if d.path.is_relative_to(registry.directory)]
        expected=set().union(*(registry.closure(d) for d in roots))
        if set(owners)!=expected:raise ValueError('wrapper inventory differs from kernel bindings and required shared definitions')
    refs={path:page['reference'] for path,page in owners.items()};counts=Counter();errors=[]
    from check_generators import dependency
    for group in mapping.get('dependency_groups',{}).values():
        for recorded in group['dependencies']:
            name=recorded['path']
            path=a.plugin/Path(name).relative_to('tools/docs/trail-kernel-doc') if name.startswith('tools/docs/trail-kernel-doc/') else a.kernel_root/name
            baseline={k:v for k,v in recorded.items() if k!='membership_only'}
            if dependency(a.kernel_root,a.plugin,path)!=baseline:
                errors.append({'source':name,'error':'shared dependency baseline changed'})
    a.out.mkdir(parents=True,exist_ok=True)
    md=MarkdownIt('commonmark',{'html':True})
    for i,(path,page) in enumerate(owners.items()):
        try:
            doc=registry.by_path[path];markdown=(a.docs/Path(page['destination']).relative_to('docs')).read_text()
            verify_wrapper(a.kernel_root,page,markdown,a.plugin)
            expected=[dependency(a.kernel_root,a.plugin,p) for p in sorted(registry.closure(doc))]
            if page.get('generator_dependencies')!=expected:raise ValueError('transitive source dependency baseline changed')
            parsed=oracle.load(doc.text)
            if a.site:output=(a.site/page['reference']/'index.html').read_text()
            else:output='<h1>'+html.escape(page['source_title'])+'</h1>'+md.render(Renderer(registry,doc,refs).render())
            counts.update(check_document(doc,parsed,output,page,registry,refs))
        except Exception as error:errors.append({'source':page['source'],'error':str(error)})
        if i%500==0:print(f'Checked {i+1}/{len(owners)}; errors {len(errors)}',flush=True)
    result={'counts':dict(counts),'errors':errors,'complete_inventory':a.complete,
            'independent_parser':'ruamel.yaml 0.18.16, YAML 1.2, pure Python',
            'rendered_site':str(a.site) if a.site else None}
    (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'counts':dict(counts),'error_count':len(errors),'first_errors':errors[:8]}))
    if errors:raise SystemExit(1)


if __name__=='__main__':main()
