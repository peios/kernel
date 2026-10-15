#!/usr/bin/env python3
"""Replace only copied include blocks in maintained articles, never regenerate."""
import argparse
import hashlib
import json
from pathlib import Path
import re
from types import SimpleNamespace
from docutils import nodes
from markdown_it import MarkdownIt
import bulk
import live_includes


def stage(root,mapping,out):
    bulk.configure(root);out.mkdir(parents=True,exist_ok=False);changed=[]
    for page in mapping['pages']:
        source=root/page['source']
        if not re.search(r'^\s*\.\. (include|csv-table)::',source.read_text(),re.M):continue
        tree=bulk.parse(source);items=[n for n in tree.findall(nodes.Element) if n.get('live_include')]
        if not items:continue
        original=(root/page['destination']).read_text()
        if hashlib.sha256(original.encode()).hexdigest()!=page['current_output_sha256']:raise ValueError('article changed: '+page['source'])
        header,body=original.split('---\n',2)[1:];records=live_includes.records(tree)
        rel=page['source'].removeprefix('Documentation/')
        writer=bulk.BulkWriter(rel,{rel:{'reference':page['reference'],'destination':page['destination'].removeprefix('docs/')}},{},mapping['upstream_commit'],set(),{})
        writer.live_enabled=False;edits=[]
        for node in items:
            record=node['live_include'];replacement=live_includes.markdown(record)
            if isinstance(node,nodes.table):
                old=writer.block(node).strip('\n')
                if body.count(old)!=1:raise ValueError('CSV block requires reconciliation: '+page['source'])
                body=body.replace(old,replacement,1)
                edits.append({'kind':'csv','path':record['path'],'original_block_sha256':hashlib.sha256(old.encode()).hexdigest()})
            elif isinstance(node,nodes.literal_block):
                tokens=[t for t in MarkdownIt('commonmark',{'html':True}).parse(body) if t.type=='fence' and not t.info.startswith('{') and t.content.removesuffix('\n')==node.astext()]
                if len(tokens)!=1:raise ValueError('literal block requires reconciliation: '+page['source']+' '+record['path'])
                token=tokens[0];start,end=token.map
                pieces=body.split('\n');lines=[s+'\n' for s in pieces[:-1]]+[pieces[-1]]
                prefix=lines[start].split('`',1)[0]
                old=''.join(lines[start:end]);new=''.join(prefix+s+'\n' for s in replacement.split('\n'))
                lines[start:end]=[new];body=''.join(lines)
                edits.append({'kind':'literal','path':record['path'],'original_block_sha256':hashlib.sha256(old.encode()).hexdigest()})
            else:raise ValueError('unknown include node')
        checks=bulk.verify_page(tree,body,SimpleNamespace(resolved_refs=page['resolved_references'],diagrams=page.get('diagrams',[])))
        text='---\n'+header+'---\n'+body
        destination=out/page['destination'];destination.parent.mkdir(parents=True,exist_ok=True);destination.write_text(text)
        page.update(current_output_sha256=hashlib.sha256(text.encode()).hexdigest(),live_includes=records,validation=checks)
        page.setdefault('migration_decisions',[]).append({'kind':'live-includes','edits':edits,'retained_surrounding_article':True})
        changed.append({'source':page['source'],'destination':page['destination'],'blocks':len(items)})
    (out/'source-map.json').write_text(json.dumps(mapping,indent=2)+'\n')
    report={'changed_articles':len(changed),'blocks':sum(p['blocks'] for p in changed),'pages':changed}
    (out/'retrofit-report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--kernel-root',type=Path,required=True)
    ap.add_argument('--mapping',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args();result=stage(a.kernel_root,json.loads(a.mapping.read_text()),a.out)
    print(json.dumps({k:v for k,v in result.items() if k!='pages'}))
