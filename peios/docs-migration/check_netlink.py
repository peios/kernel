#!/usr/bin/env python3
"""Check every Netlink wrapper, plugin response and rendered source element.

The supplied mapping is a staging copy: generator dependency baselines are
refreshed only after successful content and completeness checks.
"""
import argparse
import json
from pathlib import Path
from check_generators import check
from netlink_references import check_rendered, verify_wrapper


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--kernel-root',type=Path,required=True)
    ap.add_argument('--plugin',type=Path,required=True)
    ap.add_argument('--docs',type=Path,required=True)
    ap.add_argument('--site',type=Path,required=True)
    ap.add_argument('--mapping',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args();mapping=json.loads(a.mapping.read_text())
    pages=[p for p in mapping['pages'] if p.get('generated_reference',{}).get('kind')=='netlink-yaml']
    for page in pages:
        verify_wrapper(a.kernel_root,page,(a.docs/Path(page['destination']).relative_to('docs')).read_text())
    rendered=check_rendered(a.kernel_root,a.plugin,a.site,pages,complete=True)
    if rendered['errors']:raise ValueError('\n'.join(rendered['errors']))
    plugin=check(a.kernel_root,a.plugin,a.site,{'pages':pages},a.out)
    report={'rendered':rendered,'plugin':plugin,'complete_specification_inventory':len(pages)}
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    a.mapping.write_text(json.dumps(mapping,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
