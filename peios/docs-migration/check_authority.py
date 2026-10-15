"""Check maintained output and current runtime dependencies after source pruning.

Original source paths/hashes are provenance, not runtime requirements. Historical
conversion fidelity can still be checked against a complete baseline checkout.
"""
import hashlib
import json
from pathlib import Path

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def check(root,site,mapping):
    errors=[];seen=set();dependencies={};assets=0
    def dependency(d):
        path=d['path']
        if path in dependencies and dependencies[path]!=d['source_sha256']:
            errors.append('conflicting dependency baselines: '+path)
        dependencies[path]=d['source_sha256']
        target=root/path
        if not target.exists():errors.append('missing runtime dependency: '+path);return
        if d.get('kind')=='directory':
            from check_generators import directory_entries
            digest=hashlib.sha256(json.dumps(directory_entries(target),separators=(',',':')).encode()).hexdigest()
        else:digest=sha(target)
        if digest!=d['source_sha256']:errors.append('runtime dependency changed: '+path)
    for page in mapping['pages']+mapping.get('maintained_pages',[]):
        destination=page['destination']
        if destination in seen:errors.append('duplicate article: '+destination)
        seen.add(destination);path=site/Path(destination).relative_to('docs')
        if not path.is_file() or sha(path)!=page['current_output_sha256']:errors.append('maintained article changed: '+destination)
        for field in ('plugin_dependencies','include_plugin_dependencies','generator_dependencies'):
            for d in page.get(field,[]):
                if d['path'] not in dependencies:dependency(d)
                elif dependencies[d['path']]!=d['source_sha256']:errors.append('conflicting dependency baselines: '+d['path'])
        for asset in page.get('assets',[]):
            dest=asset['destination'];path=root/dest if dest.startswith('docs/') else site/dest
            if not path.is_file() or sha(path)!=asset.get('asset_sha256',asset['source_sha256']):errors.append('maintained asset changed: '+dest)
            assets+=1
    for group in mapping.get('dependency_groups',{}).values():
        for d in group['dependencies']:
            if d['path'] not in dependencies:dependency(d)
    if errors:raise ValueError('\n'.join(sorted(set(errors))))
    return {'mapped_articles':len(mapping['pages']),'authored_articles':len(mapping.get('maintained_pages',[])),
            'runtime_dependencies':len(dependencies),'assets':assets,'errors':0}
