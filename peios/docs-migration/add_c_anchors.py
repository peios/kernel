#!/usr/bin/env python3
"""Stage anchor-only additions to mapped articles without regenerating prose."""
import argparse
import hashlib
import json
from pathlib import Path
import re
from docutils import nodes
from bulk import configure, parse
from convert import fence


def augment(root, mapping, out):
    configure(root)
    out.mkdir(parents=True,exist_ok=False)
    changed=[];declarations=0
    for page in mapping['pages']:
        source=root/page['source']
        if not re.search(r'^\s*\.\. c:(?:function|macro|type|struct|union|enum|var)::',source.read_text(),re.M):continue
        tree=parse(source)
        entries=[n for n in tree.findall(nodes.container) if n.get('c_anchor')]
        if not entries:continue
        destination=root/page['destination'];original=destination.read_text();text=original
        if hashlib.sha256(original.encode()).hexdigest()!=page['current_output_sha256']:
            raise ValueError('article changed since mapping baseline: '+str(destination))
        records=[];seen=set()
        for n in entries:
            anchor=n['c_anchor']
            if anchor in seen:continue
            seen.add(anchor)
            signature=n['c_signature'];block=fence(signature,'c')
            if '<a id="'+anchor+'"></a>' not in text:
                if text.count(block)!=1:
                    raise ValueError('declaration needs targeted review: '+page['source']+' '+signature)
                text=text.replace(block,'<a id="'+anchor+'"></a>\n\n'+block,1)
            records.append(dict(anchor=anchor,signature=signature,namespace=n.get('c_namespace',''),source_line=n.line))
        # Removing only the added anchors must reproduce the original bytes.
        restored=text
        for record in records:
            added='<a id="'+record['anchor']+'"></a>\n\n'
            if added not in original:restored=restored.replace(added,'',1)
        if restored!=original:raise ValueError('non-anchor edit in '+page['source'])
        page['c_declarations']=records;declarations+=len(records)
        if text!=original:
            target=out/page['destination'];target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text)
            page['current_output_sha256']=hashlib.sha256(text.encode()).hexdigest()
            changed.append({'source':page['source'],'destination':page['destination'],'anchors':len(records)})
    (out/'source-map.json').write_text(json.dumps(mapping,indent=2)+'\n')
    report={'changed_articles':len(changed),'declarations':declarations,'pages':changed,'prose_unchanged':True}
    (out/'anchor-report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--kernel-root',required=True,type=Path)
    ap.add_argument('--mapping',required=True,type=Path)
    ap.add_argument('--out',required=True,type=Path)
    args=ap.parse_args()
    result=augment(args.kernel_root,json.loads(args.mapping.read_text()),args.out)
    print(json.dumps({k:v for k,v in result.items() if k!='pages'}))
