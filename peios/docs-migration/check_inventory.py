#!/usr/bin/env python3
"""Fail when any Documentation file lacks a reviewed, hash-pinned disposition."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

FIELDS=('source_dependencies','plugin_dependencies','include_plugin_dependencies','generator_dependencies','kernel_doc','assets','diagrams')
DISPOSITIONS={'translated article','supporting input','excluded translation','retained tooling','retained metadata','redirect','retained artwork','included-fragment','navigation-only','empty-source','sphinx-navigation-template'}

def files(root,skip_output=False):
    result={}
    for p in sorted((root/'Documentation').rglob('*')):
        if skip_output and p.is_relative_to(root/'Documentation/output'):continue
        if not (p.is_file() or p.is_symlink()):continue
        row={'source':str(p.relative_to(root)),'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
        if p.is_symlink():row['symlink_target']=str(p.readlink())
        result[row['source']]=row
    return result

def ownership(mapping):
    result={}
    def add(source,destination,role):result.setdefault(source,[]).append({'destination':destination,'role':role})
    for page in mapping['pages']:
        add(page['source'],page['destination'],'article')
        for field in FIELDS:
            for d in page.get(field,[]):
                if 'path' in d and d.get('kind')!='directory':add(d.get('upstream_path',d['path']),page['destination'],field)
    if mapping.get('source_index'):add(mapping['source_index'],mapping['index_destination'],'navigation source')
    return {source:sorted({(r['destination'],r['role']) for r in rows}) for source,rows in result.items()}

def check(root,mapping,inventory):
    if inventory.get('layout')=='tooling-and-trail':
        return check_storage(root,mapping,inventory)
    actual=files(root);records={r['source']:r for r in inventory['sources']};errors=[];counts=Counter()
    if len(records)!=len(inventory['sources']):errors.append('duplicate inventory source')
    for source in sorted(set(actual)-set(records)):errors.append('unclassified source: '+source)
    for source in sorted(set(records)-set(actual)):errors.append('removed source: '+source)
    owners=ownership(mapping);destinations={p['destination'] for p in mapping['pages']}
    for source,row in records.items():
        counts[row['disposition']]+=1
        if row['disposition'] not in DISPOSITIONS:errors.append('unknown disposition: '+source)
        if not row.get('reason'):errors.append('missing disposition reason: '+source)
        if source not in actual:continue
        for key in ['source_sha256','symlink_target']:
            if row.get(key)!=actual[source].get(key):errors.append('changed source '+key+': '+source)
        expected=[list(pair) for pair in owners.get(source,[])]
        if row.get('owners',[])!=expected:errors.append('source ownership changed: '+source)
        for destination in row.get('related_articles',[]):
            if destination not in destinations:errors.append('missing related article: '+destination)
        if row['disposition']=='translated article' and not any(role=='article' for _,role in expected):errors.append('article disposition without mapped article: '+source)
        if row['disposition']=='supporting input' and not expected:errors.append('supporting disposition without owner: '+source)
        if row['disposition']=='excluded translation' and not source.startswith('Documentation/translations/'):errors.append('invalid translation exclusion: '+source)
    return {'files':len(actual),'dispositions':dict(counts),'errors':errors}

def check_storage(root,mapping,inventory):
    """Validate the reviewed post-migration layout, retaining original provenance."""
    actual=files(root,skip_output=True);records={r['source']:r for r in inventory['sources']}
    errors=[];counts=Counter();owners=ownership(mapping)
    if len(records)!=len(inventory['sources']):errors.append('duplicate inventory source')
    expected=set();moved=set()
    for source,row in records.items():
        storage=row.get('storage',{});action=storage.get('action');counts[action]+=1
        if 'source_storage' in mapping and mapping['source_storage'].get(source)!=storage:errors.append('source map storage differs from inventory: '+source)
        if action not in ('keep','move','remove'):
            errors.append('unknown storage action: '+source);continue
        if not storage.get('reason'):errors.append('missing storage reason: '+source)
        if row.get('owners',[])!=[list(p) for p in owners.get(source,[])]:errors.append('source ownership changed: '+source)
        if action=='remove':
            if source in actual:errors.append('removed upstream source reintroduced: '+source)
            continue
        path=storage.get('path','');target=root/path
        if not path or not target.resolve().is_relative_to(root.resolve()):
            errors.append('invalid storage path: '+source);continue
        if action=='keep':
            expected.add(source)
            if path!=source:errors.append('retained source relocated: '+source)
        else:
            moved.add(path)
            if not path.startswith('docs/sources/'):errors.append('moved input outside docs: '+source)
            if source in actual:errors.append('duplicate upstream source: '+source)
        if not target.is_file():errors.append('missing maintained input: '+path);continue
        if hashlib.sha256(target.read_bytes()).hexdigest()!=storage.get('current_sha256',row['source_sha256']):errors.append('maintained input changed: '+path)
        if target.is_symlink() and str(target.readlink())!=row.get('symlink_target'):errors.append('changed symlink: '+path)
    for source in sorted(set(actual)-expected):
        if source not in records:errors.append('unclassified source: '+source)
    for entry in inventory.get('maintained_inputs',[]):
        path=entry['path'];moved.add(path);target=root/path
        if not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest()!=entry['sha256']:errors.append('maintained input changed: '+path)
    for p in (root/'docs/sources').rglob('*'):
        if p.is_file() and str(p.relative_to(root)) not in moved:errors.append('unclassified maintained input: '+str(p.relative_to(root)))
    return {'files':len(actual),'original_files':len(records),'storage':dict(counts),'errors':errors}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--kernel-root',type=Path,required=True);p.add_argument('--mapping',type=Path,required=True);p.add_argument('--inventory',type=Path,required=True)
    a=p.parse_args();result=check(a.kernel_root,json.loads(a.mapping.read_text()),json.loads(a.inventory.read_text()));print(json.dumps(result,indent=2));raise SystemExit(bool(result['errors']))
