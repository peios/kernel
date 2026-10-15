#!/usr/bin/env python3
"""Map an upstream Git diff to imported Trail pages; never modify either tree."""
import argparse
import json
from pathlib import Path
import subprocess


def changes(root, mapping, old, new):
    command = ['git', '-C', str(root)]
    old = subprocess.check_output(command + ['rev-parse', '--verify', old + '^{commit}'], text=True).strip()
    new = subprocess.check_output(command + ['rev-parse', '--verify', new + '^{commit}'], text=True).strip()
    tokens = subprocess.check_output(command + ['diff', '--name-status', '-z', '-M', old, new, '--']).decode().split('\0')
    tokens = iter(tokens[:-1])
    mapped = {};directories={};membership_directories={}
    for page in mapping['pages']:
        dependencies = page.get('source_dependencies', []) + page.get('plugin_dependencies', []) + page.get('include_plugin_dependencies',[]) + page.get('generator_dependencies',[]) + page.get('assets',[]) + page.get('diagrams',[])
        for d in dependencies:
            if d.get('kind')=='directory':directories.setdefault(d['path'].rstrip('/')+'/',set()).add(page['destination'])
        for source in {page['source'], *(d['path'] for d in page['kernel_doc']), *(d['path'] for d in dependencies), *(d['upstream_path'] for d in dependencies+page['kernel_doc'] if 'upstream_path' in d)}:
            mapped.setdefault(source, []).append(page['destination'])
    destinations={p['destination'] for p in mapping['pages']}
    for group in mapping.get('dependency_groups',{}).values():
        owners=set(group['destinations'])
        if not owners<=destinations:raise ValueError('dependency group refers to an unknown destination')
        for dependency in group['dependencies']:
            path=dependency['path']
            mapped.setdefault(path,[]).extend(owners)
            if dependency.get('kind')=='directory':
                target=membership_directories if dependency.get('membership_only') else directories
                target.setdefault(path.rstrip('/')+'/',set()).update(owners)
    if mapping.get('source_index'):
        mapped[mapping['source_index']] = [mapping['index_destination']]
    report = []
    accounted={p['source']:p for p in mapping.get('non_article_sources',[])}
    for status in tokens:
        paths = [next(tokens)]
        if status.startswith(('R', 'C')):
            paths.append(next(tokens))
        destinations = sorted({d for p in paths for d in mapped.get(p, [])})
        destinations=sorted(set(destinations)|{d for p in paths for prefix,ds in directories.items() if p.startswith(prefix) and not any(part.startswith('.') for part in p[len(prefix):].split('/')) for d in ds})
        if status[0] in 'ADRCT':
            destinations=sorted(set(destinations)|{d for p in paths for prefix,ds in membership_directories.items() if p.startswith(prefix) and not any(part.startswith('.') for part in p[len(prefix):].split('/')) for d in ds})
        if destinations or any(p.startswith('Documentation/') for p in paths):
            entry={'status': status, 'sources': paths, 'destinations': destinations,
                   'disposition': 'review mapped pages' if destinations else 'unmapped documentation; classify'}
            storage={p:mapping['source_storage'][p] for p in paths if p in mapping.get('source_storage',{})}
            if storage:
                entry['source_storage']=storage
                if not destinations:entry['disposition']='review recorded source storage decision'
            decisions=[accounted[p] for p in paths if p in accounted]
            if decisions:
                entry['non_article_sources']=decisions
                if not destinations:entry['disposition']='review recorded non-article disposition'
            report.append(entry)
    return {'old': old, 'new': new, 'changes': report}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kernel-root', type=Path, required=True)
    parser.add_argument('--mapping', type=Path, default=Path(__file__).with_name('source-map.json'))
    parser.add_argument('--old', help='Defaults to the recorded upstream baseline')
    parser.add_argument('--new', required=True)
    args = parser.parse_args()
    mapping = json.loads(args.mapping.read_text())
    print(json.dumps(changes(args.kernel_root, mapping, args.old or mapping['upstream_commit'], args.new), indent=2))
