#!/usr/bin/env python3
"""Verify imported prose and source code against Trail's actual HTML output."""
import argparse
from collections import Counter
import json
import re
import html as html_module
from pathlib import Path
from docutils import nodes
from bulk import ancestors, configure, parse, XRef
from verify import Visible, normal
import live_includes


class Rendered(Visible):
    def __init__(self):
        super().__init__();self.code_blocks=[];self.in_pre=False;self.current=[]
    def handle_starttag(self,tag,attrs):
        super().handle_starttag(tag,attrs)
        if tag=='pre' and 'mermaid' not in dict(attrs).get('class',''):
            self.in_pre=True;self.current=[]
    def handle_endtag(self,tag):
        super().handle_endtag(tag)
        if tag=='pre' and self.in_pre:
            self.code_blocks.append(''.join(self.current));self.in_pre=False
    def handle_data(self,text):
        super().handle_data(text)
        if self.in_pre:self.current.append(text)


def check(root,site,mapping):
    configure(root);counts=Counter();errors=[]
    bindings=[p for p in mapping['pages'] if p.get('generated_reference',{}).get('kind')=='device-tree-binding']
    if bindings:
        import binding_references
        result=binding_references.check_rendered(root,root/'tools/docs/trail-kernel-doc',site,bindings)
        counts.update(result['counts']);errors.extend(result['errors'])
    for page in mapping['pages']:
        if 'supplementary_source' in page:
            import supplementary
            markdown=(root/page['destination']).read_text()
            body=(site/page['reference']/'index.html').read_text().split('<article class="article-body"',1)[1].split('>',1)[1].split('</article>',1)[0]
            try:counts.update(supplementary.verify(root,page,markdown,body))
            except ValueError as error:errors.append({'source':page['source'],'error':str(error)})
            continue
        if 'legacy_text' in page:
            import legacy_text, legacy_sequence
            markdown=(root/page['destination']).read_text()
            body=(site/page['reference']/'index.html').read_text().split('<article class="article-body"',1)[1].split('>',1)[1].split('</article>',1)[0]
            check=legacy_sequence.verify if page['legacy_text']['kind']=='websequence-to-mermaid' else legacy_text.verify_page
            try:counts.update(check(root,page,markdown,body))
            except ValueError as error:errors.append({'source':page['source'],'error':str(error)})
            continue
        if 'generated_reference' in page:
            if page['generated_reference']['kind']=='device-tree-binding':continue
            if page['generated_reference']['kind']!='netlink-yaml':raise ValueError('unknown generated reference kind')
            import netlink_references
            result=netlink_references.check_rendered(root,root/'tools/docs/trail-kernel-doc',site,[page])
            counts.update(result['counts']);errors.extend(result['errors'])
            continue
        if 'adaptation' in page:
            import adapted
            markdown=(root/page['destination']).read_text()
            try:
                counts.update(adapted.check_rendered(markdown,(site/page['reference']/'index.html').read_text()))
            except ValueError as error:
                errors.append({'source':page['source'],'error':str(error)})
            continue
        tree=parse(root/page['source'])
        html=(site/page['reference']/'index.html').read_text()
        # Navigation must not accidentally satisfy an absent article paragraph.
        html=html.split('<article class="article-body"',1)[1].split('>',1)[1].split('</article>',1)[0]
        # Verify TeX against MathML annotations, then substitute its original
        # text for paragraph comparison (visual MathML repeats/reorders tokens).
        maths=re.findall(r'<math\b.*?</math>',html,re.S)
        tex=[]
        for equation in maths:
            annotation=re.search(r'<annotation encoding="application/x-tex">(.*?)</annotation>',equation,re.S)
            if not annotation or '<merror' in equation:raise ValueError('invalid or unannotated equation')
            tex.append(html_module.unescape(annotation[1]))
        expected_tex=[n.astext() for n in tree.findall() if isinstance(n,(nodes.math,nodes.math_block))]
        if tex!=expected_tex:errors.append({'source':page['source'],'error':'rendered TeX differs from source'})
        counts['equations']+=len(tex)
        for equation,original in zip(maths,tex):html=html.replace(equation,html_module.escape(original),1)
        rendered=Rendered();rendered.feed(html);visible=normal(''.join(rendered.text))
        refs={(r['role'],r['source_text']):r['caption'] for r in page['resolved_references']}
        def expected(n):
            if isinstance(n,XRef):return refs[(n['kind'],n.astext())]
            if isinstance(n,nodes.Text):return n.astext()
            return ''.join(expected(c) for c in n.children)
        for n in tree.findall():
            if live_includes.csv_owner(n) is not None:continue
            if any(isinstance(a,(nodes.system_message,nodes.comment,nodes.substitution_definition)) or (isinstance(a,nodes.topic) and 'contents' in a.get('classes',[])) for a in ancestors(n)):continue
            if isinstance(n,(nodes.paragraph,nodes.term,nodes.classifier,nodes.field_name,nodes.subtitle,nodes.line,nodes.rubric,nodes.caption)) or (isinstance(n,nodes.title) and not isinstance(n.parent,(nodes.document,nodes.topic))):
                if normal(expected(n)) not in visible:errors.append({'source':page['source'],'line':n.line,'missing_text':n.astext()[:160]})
                counts['prose_nodes']+=1
        index=0
        for n in tree.findall():
            if not isinstance(n,(nodes.literal_block,nodes.doctest_block)):continue
            # The fence renderer adds one delimiter newline; an existing final
            # newline in the source excerpt remains part of its literal text.
            source=n.astext()
            # Generated kernel-doc examples may be interleaved with source code.
            while index<len(rendered.code_blocks) and rendered.code_blocks[index].removesuffix('\n')!=source:index+=1
            if index==len(rendered.code_blocks):
                errors.append({'source':page['source'],'line':n.line,'missing_code':source[:120]});break
            index+=1;counts['literal_blocks']+=1
        for record in live_includes.records(tree):
            if 'csv' not in record['options']:continue
            for row in live_includes.csv_values(record):
                for cell in row:
                    if normal(cell) not in visible:errors.append({'source':page['source'],'missing_csv_cell':cell})
                    counts['csv_cells']+=1
        counts['articles']+=1
    return {'counts':dict(counts),'errors':errors}


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--kernel-root',type=Path,required=True)
    ap.add_argument('--site',type=Path,required=True)
    ap.add_argument('--mapping',type=Path,required=True)
    args=ap.parse_args()
    result=check(args.kernel_root,args.site,json.loads(args.mapping.read_text()))
    print(json.dumps(result,indent=2));raise SystemExit(bool(result['errors']))
