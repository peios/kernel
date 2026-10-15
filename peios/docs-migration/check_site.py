#!/usr/bin/env python3
"""Check built HTML for duplicate IDs and broken local links/fragments."""
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote,urlsplit


class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.ids=set();self.links=[];self.errors=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'id' in attrs:
            if attrs['id'] in self.ids:self.errors.append('duplicate ID '+attrs['id'])
            self.ids.add(attrs['id'])
        if tag=='a' and 'href' in attrs:self.links.append(attrs['href'])
        if tag in ('img','script') and 'src' in attrs:self.links.append(attrs['src'])


def check(root):
    root=root.resolve();pages={};errors=[];count=0;targets={}
    for p in root.rglob('*.html'):
        page=Page(p.read_text());pages[p]=page
        errors.extend(str(p.relative_to(root))+': '+e for e in page.errors)
    for p,page in pages.items():
        for href in page.links:
            u=urlsplit(href)
            if u.scheme or u.netloc:continue
            path=unquote(u.path)
            # The site is an immutable build snapshot. Shared navigation repeats
            # the same destinations hundreds of thousands of times; resolve and
            # stat each destination once, while still checking every fragment.
            key=(root if path.startswith('/') else p.parent if path else p,path)
            if key not in targets:
                target=(root/path.lstrip('/') if path.startswith('/') else p.parent/path) if path else p
                if target.is_dir():target=target/'index.html'
                target=target.resolve();targets[key]=(target,target.exists())
            target,exists=targets[key]
            if not exists:errors.append(str(p.relative_to(root))+': missing '+href)
            elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:
                errors.append(str(p.relative_to(root))+': missing fragment '+href)
            count+=1
    return {'html_pages':len(pages),'local_links_and_assets':count,'errors':errors}


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('site',type=Path);args=ap.parse_args()
    result=check(args.site);print(json.dumps(result,indent=2));raise SystemExit(bool(result['errors']))
