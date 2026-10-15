#!/usr/bin/env python3
"""Add relative redirects from former RST URLs without replacing Trail output."""
import argparse
import html
import json
import os
from pathlib import Path

def write(root,out):
    mapping=json.loads((root/'peios/docs-migration/source-map.json').read_text())
    count=0
    for page in mapping['pages']:
        source=Path(page['source'])
        if source.suffix!='.rst' or source.parts[0]!='Documentation':continue
        destination=out/source.relative_to('Documentation').with_suffix('.html')
        target=out/page['reference']/'index.html'
        if not target.is_file():raise ValueError('build Trail before generating redirects: '+str(target))
        if destination==out/'index.html':continue
        link=html.escape(os.path.relpath(target,destination.parent),quote=True)
        content=f'<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url={link}"><a href="{link}">Read the maintained Peios documentation</a>\n'
        if destination.exists() and destination.read_text()!=content:raise ValueError('refusing to replace existing output: '+str(destination))
        destination.parent.mkdir(parents=True,exist_ok=True);destination.write_text(content);count+=1
    return count

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--kernel-root',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();print(json.dumps({'redirects':write(a.kernel_root,a.out)}))
