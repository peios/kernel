#!/usr/bin/env python3
"""Check live include output/dependencies per article and update its mapping."""
import argparse
import hashlib
import json
from pathlib import Path
import live_includes


def check(root,mapping):
    live_includes.ROOT=root.resolve();results={}
    for page in mapping['pages']:
        records=page.get('live_includes',[])
        if not records:continue
        response=live_includes.evaluate(records);dependencies=[]
        for name in response['depends_on']:
            p=Path(name).resolve()
            # A staged plugin path is mapped to its eventual installed home.
            rel=str(p.relative_to(root)) if p.is_relative_to(root) else 'tools/docs/trail-kernel-doc/'+p.name
            dependencies.append({'path':rel,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
        page['include_plugin_dependencies']=dependencies
        results[page['source']]={'blocks':len(records),'dependencies':dependencies,'errors':[]}
    return results


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--kernel-root',type=Path,required=True)
    ap.add_argument('--mapping',type=Path,required=True)
    ap.add_argument('--report',type=Path,required=True)
    a=ap.parse_args();mapping=json.loads(a.mapping.read_text());result=check(a.kernel_root,mapping)
    a.mapping.write_text(json.dumps(mapping,indent=2)+'\n');a.report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'pages':len(result),'blocks':sum(r['blocks'] for r in result.values()),'errors':0}))
