"""Check generated tables, ABI metadata, maintainer fields and header entries."""
import json
import sys
import re
from pathlib import Path
from html.parser import HTMLParser
from collections import Counter
import argparse
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--kernel-root',type=Path,required=True)
ap.add_argument('--plugin',type=Path,required=True)
ap.add_argument('--site',type=Path,required=True)
ap.add_argument('--mapping',type=Path,required=True)
ap.add_argument('--report',type=Path,required=True)
a=ap.parse_args();R=a.kernel_root
sys.path[:0]=[str(R/'tools/lib/python'),str(a.plugin),str(Path(__file__).parent)]
from feat.parse_features import ParseFeature
from abi.abi_parser import AbiParser
from kdoc.parse_data_structs import ParseDataStructs
from verify import Visible,normal
import abi_markdown
import maintainers_markdown
import uapi_markdown
mapping=json.loads(a.mapping.read_text());count=Counter()
def article(page):
    return (a.site/page['reference']/'index.html').read_text().split('<article class="article-body"',1)[1].split('>',1)[1].split('</article>',1)[0]
def visible(html):
    p=Visible();p.feed(html);return normal(''.join(p.text))
class Rows(HTMLParser):
    def __init__(self,html):super().__init__();self.rows=[];self.row=None;self.cell=None;self.feed(html)
    def handle_starttag(self,tag,attrs):
        if tag=='tr':self.row=[]
        if tag in ('td','th'):self.cell=[]
        if tag=='br' and self.cell is not None:self.cell.append(' ')
    def handle_data(self,text):
        if self.cell is not None:self.cell.append(text)
    def handle_endtag(self,tag):
        if tag in ('td','th') and self.cell is not None:self.row.append(normal(''.join(self.cell)));self.cell=None
        if tag=='tr' and self.row is not None:self.rows.append(self.row);self.row=None
feat=ParseFeature(str(R/'Documentation/features'),False,False).parse()
abi=AbiParser(str(R/'Documentation/ABI'));abi.parse_abi();views=abi_markdown.AbiMarkdown(abi)
for page in mapping['pages']:
    for record in page.get('generated',[]):
        html=article(page);plain=visible(html);plugin=record['plugin'];opts=record['options']
        if plugin=='kernel-feat':
            rows=Rows(html).rows
            arch=opts.get('arch')
            for name,f in feat.items():
                if arch:
                    if arch not in f['table']:continue
                    status=f['table'][arch];status='Not compatible' if status=='---' else status
                    expected=list(map(normal,[f['subsys'],name,f['kconfig'],status,f['description']]))
                    assert expected in rows,(page['source'],expected)
                else:
                    row=next(row for row in rows if row[0]==normal(name))
                    assert row[1:3]==[normal(f['kconfig']),normal(f['description'])]
                    for architecture,status in f['table'].items():assert architecture in row[3] and ('Not compatible' if status=='---' else status) in row[3]
                count['feature_rows']+=1
        elif plugin=='kernel-abi':
            level=record['argument']
            for key,e in abi.data.items():
                if e.get('path')!=level:continue
                isfile=e.get('type')=='File'
                if isfile and 'no-files' in opts or not isfile and 'no-symbols' in opts:continue
                if level=='README':assert plain;count['abi_readmes']+=1;continue
                anchor='id="'+views.anchors[key]+'"';assert html.count(anchor)==1,anchor
                part=html.split(anchor,1)[1]
                part=re.split(r'<h[24]\b',part,maxsplit=1)[0];text=visible(part)
                for name in e['what']:
                    expected=name.replace('ABI file ','File ',1) if isfile else name
                    assert normal(expected) in text,(level,expected)
                if not isfile:
                    for field in ('date','kernelversion','contact'):
                        if e.get(field):assert normal(e[field]) in text,(key,field);count['abi_metadata_fields']+=1
                    if e.get('description','').strip():assert 'No description.' not in text
                count['abi_files' if isfile else 'abi_symbols']+=1
        elif plugin=='kernel-maintainers':
            source=(R/'MAINTAINERS').read_text();seen=Counter()
            for match in re.finditer(r'^([^\n]+)\n((?:[A-Z]:[^\n]*\n)+)',source,re.M):
                name,fields=match.groups();base=maintainers_markdown.anchor(normal(name));seen[base]+=1;anchor=base+('-'+str(seen[base]) if seen[base]>1 else '')
                token='id="'+anchor+'"';assert html.count(token)==1,anchor
                part=html.split(token,1)[1].split('<h4',1)[0];text=visible(part)
                assert normal(name) in text
                for field in fields.splitlines():
                    assert normal(field[2:]) in text,(name,field)
                    count['maintainer_fields']+=1
                count['maintainer_entries']+=1
        elif plugin=='kernel-include':
            parser=ParseDataStructs();parser.parse_file(str(R/record['argument']),str(R/opts['exception-file']))
            for entries in parser.symbols.values():
                for name,(_,line) in entries.items():
                    assert normal(name) in plain and normal(record['argument']+', line '+str(line+1)) in plain,(record['argument'],name)
                    count['uapi_symbols']+=1
            count['uapi_headers']+=1
a.report.write_text(json.dumps({'counts':dict(count),'errors':[]},indent=2)+'\n');print(json.dumps(dict(count)))
