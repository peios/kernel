"""Verify live source excerpts and standalone figures in the residual import."""
import hashlib
import re
from pathlib import Path
from markdown_it import MarkdownIt

def sha(data):return hashlib.sha256(data).hexdigest()

def comment_notes(text):
    """Extract the MultiSound README before its second shell header."""
    lines=text.splitlines(keepends=True)
    end=next(i for i,line in enumerate(lines[1:],1) if line.startswith('#!/bin/sh'))
    selected=lines[1:end]
    if any(line.strip() and not line.startswith('#') for line in selected):raise ValueError('unexpected code inside commented README')
    return ''.join(re.sub(r'^# ? ?', '',line) for line in selected)

def verify(root,page,markdown,rendered_html=None):
    source=root/page.get('runtime_source',page['source']);record=page['supplementary_source']
    if sha(source.read_bytes())!=page['source_sha256']:raise ValueError('supplementary source baseline changed')
    if sha(markdown.encode())!=page['current_output_sha256']:raise ValueError('maintained supplementary article changed')
    tokens=MarkdownIt('commonmark',{'html':True}).parse(markdown.split('---\n',2)[2])
    fences=[t for t in tokens if t.type=='fence'];kind=record['kind']
    if kind=='live-source':
        includes=[t for t in fences if t.info.startswith('{')]
        if len(includes)!=1 or includes[0].info!='{kernel-include} '+page.get('runtime_source',page['source']) or includes[0].content!=':language: '+record['language']+'\n':
            raise ValueError('source excerpt must include the complete original without slicing')
        extra_code=[]
        if 'comment_notes' in record:
            from legacy_text import expected_text
            notes=comment_notes(source.read_text());blocks=record['comment_notes']['blocks'];lines=notes.splitlines(keepends=True)
            if sha(notes.encode())!=record['comment_notes']['source_sha256']:raise ValueError('commented README changed')
            nextline=1
            for block in blocks:
                if block['start']!=nextline or block['end']<block['start']:raise ValueError('README line disposition gap')
                nextline=block['end']+1
                if block['kind']=='literal':
                    code=''.join(lines[block['start']-1:block['end']]);extra_code.append(code if code.endswith('\n') else code+'\n')
            if nextline!=len(lines)+1:raise ValueError('README line disposition incomplete')
        if rendered_html is not None:
            from check_rendered_preservation import Rendered
            from legacy_text import article_content
            rendered=Rendered();rendered.feed(article_content(rendered_html,page['source_title']))
            if rendered.code_blocks!=extra_code+[source.read_text()+'\n']:raise ValueError('source excerpt whitespace or contents changed')
            if 'comment_notes' in record:
                from verify import Visible,normal
                section=re.search(r'<h2[^>]*id="driver-notes"[^>]*>.*?</h2>(.*?)<h2[^>]*id="original-source-and-utility-archive"',rendered_html,re.S)
                if not section:raise ValueError('readable README section missing')
                visible=Visible();visible.feed(article_content('<h1>'+page['source_title']+'</h1>'+section[1],page['source_title']))
                if normal(''.join(visible.text))!=normal(expected_text(notes,blocks)):raise ValueError('readable README text changed')
    elif kind=='mermaid':
        if len(fences)!=1 or fences[0].info!='mermaid' or sha(fences[0].content.encode())!=page['diagrams'][0]['mermaid_sha256']:
            raise ValueError('reviewed Mermaid changed')
        if rendered_html is not None and 'class="mermaid"' not in rendered_html:raise ValueError('missing rendered diagram')
    elif kind=='image':
        from html.parser import HTMLParser
        class Images(HTMLParser):
            def __init__(self):super().__init__();self.paths=[]
            def handle_starttag(self,tag,attrs):
                if tag=='img':self.paths.append(dict(attrs).get('src'))
        if rendered_html is not None:
            images=Images();images.feed(rendered_html)
            if not any(Path(p).name==Path(page['assets'][0]['destination']).name for p in images.paths):raise ValueError('missing standalone image')
    else:raise ValueError('unknown supplementary kind')
    return {'articles':1,'supplementary_articles':1,kind:1}
