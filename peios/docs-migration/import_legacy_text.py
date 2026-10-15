#!/usr/bin/env python3
"""Stage the legacy text corpus in a NEW directory, never edit maintained pages."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

import legacy_text
import legacy_sequence
from bulk import slug
from convert import quote


def stage(root,out):
    if out.exists():raise ValueError('output exists; never regenerate maintained articles')
    out.mkdir(parents=True)
    mapping=json.loads((root/'peios/docs-migration/source-map.json').read_text())
    sources=legacy_text.inventory(root)
    old={p['source'].removeprefix('Documentation/'):p for p in mapping['pages']}
    if set(sources)&set(old):raise ValueError('legacy source already mapped; reconcile instead of importing again')
    refs={p['reference'] for p in old.values()};targets=dict(old);configs={};new=[];counts=Counter()
    for i,source in enumerate(sources):
        parts=Path(source).parts;parent=Path(source).parent
        peers=[p for s,p in old.items() if Path(s).parent==parent]
        if peers:
            base=Path(peers[0]['destination']).parent;ref=peers[0]['reference'].rsplit('/',1)[0]
        else:
            peers=[p for s,p in old.items() if Path(s).parts[0]==parts[0]]
            if peers:
                base=next(p for p in Path(peers[0]['destination']).parents if p.suffix=='.topic')
                ref='/'.join(peers[0]['reference'].split('/')[:3])
                if len(parts)>2:
                    folder=slug('/'.join(parts[1:-1]));base=base/f'{2000000+i*100}--{folder}';ref+='/'+folder
                    configs[base]='/'.join(parts[1:-1])
            elif parts[0]=='litmus-tests':
                base=Path('docs/kernel.product/300--development.antho/9000--litmus-tests.topic');ref='kernel/development/litmus-tests'
                configs[base]='Litmus tests'
            else:raise ValueError('unknown category '+source)
        name=slug(Path(source).stem)
        if ref+'/'+name in refs:name+='-legacy'
        reference=ref+'/'+name
        if reference in refs:raise ValueError('reference collision '+reference)
        # Share a new source folder, rather than creating a directory per page.
        prior=next((targets[s] for s in sources[:i] if Path(s).parent==parent),None)
        if prior:
            base=Path(prior['destination']).parent
        targets[source]={'destination':str(base/f'{4000000+i*100}--{name}.md'),'reference':reference}
        refs.add(reference)
    # Discard transient folder configs superseded by the shared directory.
    actual={Path(t['destination']).parent for s,t in targets.items() if s in sources}
    configs={p:title for p,title in configs.items() if p in actual}
    for path in (root/'Documentation').rglob('*.yaml'):
        source=str(path.relative_to(root/'Documentation'))
        if source not in targets:
            targets[source]={'source_url':'https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/'+source+'?id='+mapping['upstream_commit']}
    for source in sources:
        path=root/'Documentation'/source;text=path.read_text()
        queued=root/'docs-to-translate'/source
        if not queued.exists() or queued.read_bytes()!=path.read_bytes():raise ValueError('source queue differs: '+source)
        title=legacy_text.title_for(source,text.splitlines())
        if source=='networking/mac80211-auth-assoc-deauth.txt':
            body,record=legacy_sequence.render(text);links=[]
        else:
            title,blocks=legacy_text.parse(source,text);body,links=legacy_text.render(source,text,blocks,targets)
            record={'kind':'line-accounted-text','blocks':blocks}
        desc=('Device-tree binding reference for '+title+'.' if source.startswith('devicetree/') else 'Kernel reference: '+title+'.')
        content='---\ntitle: '+quote(title)+'\ntype: reference\ndescription: '+quote(desc)+'\n---\n\n'+body
        target=targets[source];dest=out/target['destination'];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(content)
        page=dict(source='Documentation/'+source,source_sha256=legacy_text.sha(text),source_title=title,**target,
                  initial_output_sha256=legacy_text.sha(content),current_output_sha256=legacy_text.sha(content),
                  legacy_text=record,sections=[],labels={},kernel_doc=[],source_dependencies=[],
                  external_documentation=[],assets=[],diagrams=[],resolved_references=links,
                  status='legacy text converted with source-line preservation; editorial review pending')
        result=(legacy_sequence.verify if record['kind']=='websequence-to-mermaid' else legacy_text.verify_page)(root,page,content)
        counts.update(result);new.append(page)
    for path,title in configs.items():
        p=out/path/'trail.toml';p.parent.mkdir(parents=True,exist_ok=True);p.write_text('title = '+quote(title)+'\n')
    mapping['pages'].extend(new)
    mapping['legacy_text_batch']={'articles':len(new),'source_queue_retained':True,'preservation':dict(counts)}
    for name,data in [('source-map.json',mapping),('new-pages-map.json',{'pages':new}),('preservation.json',dict(counts)),
                      ('inventory.json',{'sources':sources,'device_tree_text':sum(s.startswith('devicetree/') for s in sources),'other_text_and_readme':len(legacy_text.EXTRA)})]:
        (out/name).write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(dict(counts)))


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--kernel-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args();stage(a.kernel_root.resolve(),a.out)
