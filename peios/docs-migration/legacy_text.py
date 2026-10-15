"""One-way legacy text import with a complete source-line disposition.

Recognize headings and simple lists; retain spacing-sensitive examples as
literal blocks. Never run this over maintained articles. Every source line is
accounted for, including whitespace and presentation-only title decorations.
"""
import hashlib
import html
import re
from collections import Counter
from pathlib import Path

from markdown_it import MarkdownIt

EXTRA = ['leds/well-known-leds.txt', 'admin-guide/spkguide.txt',
         'networking/mac80211-auth-assoc-deauth.txt', 'filesystems/propagate_umount.txt',
         'filesystems/path-lookup.txt', 'RCU/RTFP.txt', 'arch/powerpc/kasan.txt',
         'litmus-tests/README', 'virt/kvm/devices/README']
TITLES = {'leds/well-known-leds.txt': 'Well-known LED names',
          'admin-guide/spkguide.txt': "The Speakup User's Guide",
          'networking/mac80211-auth-assoc-deauth.txt': 'mac80211 authentication and association flows',
          'filesystems/propagate_umount.txt': 'Notes on propagate_umount()',
          'filesystems/path-lookup.txt': 'Path walking and name lookup locking',
          'RCU/RTFP.txt': 'Read the Fscking Papers!',
          'arch/powerpc/kasan.txt': 'KASAN on PowerPC',
          'litmus-tests/README': 'Litmus tests',
          'virt/kvm/devices/README': 'KVM device bindings',
          'devicetree/bindings/clock/clock-bindings.txt': 'Clock bindings',
          'devicetree/bindings/iio/mount-matrix.txt': 'IIO mount matrix',
          'devicetree/bindings/powerpc/fsl/srio-rmu.txt': 'Freescale RapidIO message unit'}
MARKER = re.compile(r'^(\s*)([-+*]|\d+[.)])\s+(.*)$')
RULE = re.compile(r'^\s*([=~_\-])\1{2,}\s*$')


def inventory(root):
    return sorted([str(p.relative_to(root/'Documentation'))
                   for p in (root/'Documentation/devicetree').rglob('*.txt')] + EXTRA)


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def escape(text):
    # Treat text as text, never as HTML, a directive, an image or a math fence.
    text=re.sub(r'([\\`*\[\]_])', r'\\\1', html.escape(text, quote=False))
    return re.sub(r'^(\s*)([#>+\-]|\d+[.)])(?=\s)',lambda m:m[1]+re.sub(r'([#>+\-.)])',r'\\\1',m[2]),text,flags=re.M)


def fence(text, language='text'):
    ticks='`'*max(3, 1+max([len(x) for x in re.findall(r'`+',text)] or [0]))
    return ticks+language+'\n'+text+('' if text.endswith('\n') else '\n')+ticks


def title_for(source, lines):
    if source in TITLES:return TITLES[source]
    for i,line in enumerate(lines):
        text=line.strip()
        if not text or RULE.fullmatch(text) or 'SPDX-License-Identifier:' in text or text.startswith('/*'):continue
        if source.startswith('devicetree/') and (re.match(r'^(This |See |Every |For discussion)',text) or (i+1<len(lines) and lines[i+1].strip() and not RULE.fullmatch(lines[i+1]) and not text.startswith('* '))):
            return Path(source).stem.replace('-',' ').replace('_',' ').capitalize()+' bindings'
        return re.sub(r'^\*\s+', '', text)
    raise ValueError(source+': no title')


def brace_delta(text):
    # DTS quoted strings and comments can contain braces.
    text=re.sub(r'/\*.*?\*/|//[^\n]*|"(?:\\.|[^"\\])*"', '', text, flags=re.S)
    return text.count('{')-text.count('}')


def heading_at(lines, i, source):
    s=lines[i].strip()
    if not s:return None
    if i+1<len(lines) and RULE.fullmatch(lines[i+1]) and not RULE.fullmatch(s):
        level=3 if source=='filesystems/path-lookup.txt' and lines[i+1].lstrip().startswith('-') else 2
        return s,level,2
    if source=='leds/well-known-leds.txt' and re.match(r'^\*+ ',s):
        mark,text=s.split(' ',1);return text,len(mark)+1,1
    if source.startswith('devicetree/') and len(s)<100 and s.endswith(':') and not MARKER.match(s) and not any(c in s for c in '{}=') and (i==0 or not lines[i-1].strip()) and len(s.split())<=9 and not s.startswith(('//','/*')):
        return s,2,1
    if source=='admin-guide/spkguide.txt' and (re.match(r'^\d+(?:\.\d+)*\.\s+\S',s) or s in ('Preface','GNU Free Documentation License') or s.startswith('ADDENDUM:')):
        return s,min(5,2+len(re.match(r'^[\d.]*',s)[0].rstrip('.').split('.'))-1),1
    if source=='filesystems/propagate_umount.txt' and re.match(r'^\t\t[A-Z]',lines[i]) and (i==0 or not lines[i-1].strip()) and (i+1==len(lines) or not lines[i+1].strip()):
        return s,2,1
    return None


def is_code_start(line, source):
    s=line.strip()
    if re.match(r'^@\w+\{',s):return True
    if source.startswith('devicetree/'):
        return bool(re.match(r'^(?:[\w,&/@.+-]+\s*:?\s*)?[^\s]*\s*\{\s*(?://.*)?$',s)
                    or re.match(r'^[\w,#.+-]+\s*=\s*',s)
                    or s.startswith(('#include ', '/dts-v1/', '/memreserve/', '};')))
    return bool(re.match(r'^(?:\$ |# (?:echo|modprobe)|linux speakup\.|(?:echo|cat|modprobe|speakupconf|talkwith)\s)',s))


def parse(source, text):
    lines=text.splitlines(keepends=True);title=title_for(source,lines);blocks=[];i=0
    def add(kind,start,end,**kw):
        blocks.append(dict(kind=kind,start=start+1,end=end,**kw))
    title_used=False
    while i<len(lines):
        s=lines[i].strip()
        if not s:
            j=i+1
            while j<len(lines) and not lines[j].strip():j+=1
            add('blank',i,j);i=j;continue
        if s=='-*- org -*-':add('modeline',i,i+1);i+=1;continue
        # Keep SPDX/copyright/license text visible and in the source checks.
        clean=re.sub(r'^\*\s+', '',s)
        if not title_used and clean.lower()==title.lower():
            j=i+1
            if j<len(lines) and RULE.fullmatch(lines[j]):j+=1
            add('title',i,j,text=clean);title_used=True;i=j;continue
        if RULE.fullmatch(s):
            add('rule',i,i+1);i+=1;continue
        h=heading_at(lines,i,source)
        if h:
            label,level,n=h;add('heading',i,i+n,text=label,level=level);i+=n;continue
        # BibTeX is data: retain entries, including blank lines, verbatim.
        if re.match(r'^@\w+\{',s):
            j=i+1
            while j<len(lines) and not re.match(r'^@\w+\{',lines[j].strip()):j+=1
            while j>i+1 and not lines[j-1].strip():j-=1
            add('literal',i,j,language='bibtex');i=j;continue
        if is_code_start(lines[i],source):
            j=i+1;depth=brace_delta(lines[i])
            while j<len(lines):
                if depth<=0 and not lines[j].strip():break
                if depth<=0 and not is_code_start(lines[j],source) and not lines[j][0].isspace() and not lines[j].strip().startswith(('};','/*','//','*')):break
                depth+=brace_delta(lines[j]);j+=1
            add('literal',i,j,language='dts' if source.startswith('devicetree/') else 'text');i=j;continue
        if lines[i].startswith(('\t','    ')) and not MARKER.match(lines[i]):
            j=i+1
            while j<len(lines) and lines[j].strip() and lines[j][0].isspace():j+=1
            add('literal',i,j,language='text');i=j;continue
        if source=='leds/well-known-leds.txt' and re.match(r'^(Good|Legacy):',s):
            j=i+1
            while j<len(lines) and re.match(r'^(Good|Legacy):',lines[j]):j+=1
            add('lines',i,j);i=j;continue
        # A simple list's continuations stay with the item. Complex examples
        # embedded in lists use a literal block so indentation cannot be lost.
        if MARKER.match(lines[i]):
            j=i+1
            while j<len(lines) and lines[j].strip() and not heading_at(lines,j,source):j+=1
            raw=lines[i:j]
            markers=[MARKER.match(x) for x in raw if MARKER.match(x)]
            indents={len(m[1].expandtabs()) for m in markers}
            if len(indents)>1 or any(is_code_start(x,source) for x in raw[1:]):
                add('literal',i,j,language='text')
            else:add('list',i,j)
            i=j;continue
        j=i+1
        while j<len(lines) and lines[j].strip() and not heading_at(lines,j,source) and not MARKER.match(lines[j]) and not is_code_start(lines[j],source) and not lines[j].startswith(('\t','    ')):j+=1
        raw=lines[i:j]
        # Preserve aligned tables, ASCII figures, and indented pseudocode.
        aligned=sum(bool(re.search(r'\S(?:\t+| {3,})\S',x)) for x in raw)
        indented=all(x[:1].isspace() for x in raw)
        drawing=any(re.search(r'(?:[-+|]{4,}|\+[-=]{2,}\+|[|].*[|])',x) for x in raw)
        kind='literal' if aligned>=2 or indented or drawing else 'prose'
        if source=='admin-guide/spkguide.txt' and s.startswith(('For Speakup','Copyright (c)')):kind='linebreaks'
        add(kind,i,j,**({'language':'text'} if kind=='literal' else {}));i=j
    return title,blocks


def list_items(raw):
    items=[]
    for line in raw.splitlines():
        match=MARKER.match(line)
        if match:items.append((match[2],match[3]))
        else:
            if not items:raise ValueError('list continuation without item')
            mark,value=items[-1];items[-1]=(mark,value+'\n'+line.strip())
    return items


def inline(text, source, targets, links):
    # Only turn existing, unambiguous documentation paths into links. Keep
    # source labels unchanged; unresolved historical references remain text.
    pattern=r'(?<![\w/])(?:Documentation/|(?:\.\./)*)(?:[\w,./+@-]+\.(?:txt|rst|yaml)|[\w,./+@-]*/README)(?![\w/])'
    out=[];cursor=0
    for m in re.finditer(pattern,text):
        name=m[0];candidate=name.removeprefix('Documentation/')
        choices=[candidate] if name.startswith('Documentation/') else [str(Path(source).parent/candidate),candidate]
        import posixpath
        found=next((posixpath.normpath(p) for p in choices if posixpath.normpath(p) in targets),None)
        if found is None:continue
        target=targets[found];url=target.get('source_url') or '~'+target['reference']
        out.append(escape(text[cursor:m.start()]));out.append('['+escape(name)+'](<'+url+'>)')
        links.append({'source_text':name,'source':found,'target':url});cursor=m.end()
    out.append(escape(text[cursor:]));return ''.join(out)


def render(source,text,blocks,targets):
    lines=text.splitlines(keepends=True);parts=[];links=[]
    for b in blocks:
        raw=''.join(lines[b['start']-1:b['end']]);kind=b['kind']
        if kind in ('blank','title'):continue
        if kind=='modeline':parts.append('<!-- '+raw.strip()+' -->')
        elif kind=='rule':parts.append('---')
        elif kind=='heading':parts.append('#'*b['level']+' '+inline(b['text'],source,targets,links))
        elif kind=='literal':parts.append(fence(raw,b['language']))
        elif kind=='prose':parts.append(inline(raw.strip(),source,targets,links))
        elif kind=='linebreaks':parts.append('  \n'.join(inline(line.strip(),source,targets,links) for line in raw.splitlines()))
        elif kind=='lines':parts.append('\n'.join('- '+inline(line.strip(),source,targets,links) for line in raw.splitlines()))
        elif kind=='list':
            rows=[]
            for marker,value in list_items(raw):
                # Keep numeric labels, which sometimes name logical cases.
                prefix=marker+' ' if marker[0].isdigit() else '- '
                rows.append(prefix+inline(value,source,targets,links).replace('\n','\n'+' '*len(prefix)))
            parts.append('\n'.join(rows))
        else:raise ValueError(kind)
    return '\n\n'.join(parts)+'\n',links


def expected_text(text,blocks):
    lines=text.splitlines(keepends=True);result=[]
    for b in blocks:
        raw=''.join(lines[b['start']-1:b['end']]);kind=b['kind']
        if kind in ('blank','title','modeline','rule'):continue
        if kind=='heading':result.append(b['text'])
        elif kind=='list':result.extend(value for marker,value in list_items(raw))
        else:result.append(raw)
    return '\n'.join(result)


def article_content(rendered_html, title):
    """Remove only Trail chrome, never content, from the article element."""
    from verify import Visible,normal
    h=re.search(r'<h1\b[^>]*>(.*?)</h1>',rendered_html,re.S)
    if not h:raise ValueError('article title missing')
    v=Visible();v.feed(h[1])
    if normal(''.join(v.text))!=normal(title):raise ValueError('rendered title differs from source map')
    body=rendered_html[:h.start()]+rendered_html[h.end():]
    body=re.sub(r'<nav class="(?:crumbs|pager)"[^>]*>.*?</nav>','',body,flags=re.S)
    body=re.sub(r'<p class="article-meta"[^>]*>.*?</p>','',body,flags=re.S)
    body=re.sub(r'<a class="heading-anchor"[^>]*>.*?</a>','',body,flags=re.S)
    body=re.sub(r'<button class="copy-code"[^>]*>.*?</button>','',body,flags=re.S)
    return body


def verify_page(root,page,markdown,rendered_html=None):
    from verify import Visible,normal
    from check_rendered_preservation import Rendered
    record=page['legacy_text'];text=(root/page['source']).read_text();lines=text.splitlines(keepends=True)
    if sha(text)!=page['source_sha256']:raise ValueError('legacy source changed; reconcile baseline')
    if sha(markdown)!=page['current_output_sha256']:raise ValueError('maintained article changed; review baseline')
    blocks=record['blocks'];nextline=1
    for b in blocks:
        if b['start']!=nextline or b['end']<b['start']:raise ValueError('source line disposition gap or overlap')
        nextline=b['end']+1
    if nextline!=len(lines)+1:raise ValueError('source lines not fully accounted for')
    md=MarkdownIt('commonmark',{'html':True});body=markdown.split('---\n',2)[2]
    rendered=Rendered();rendered.feed(article_content(rendered_html,page['source_title']) if rendered_html is not None else md.render(body))
    if normal(''.join(rendered.text))!=normal(expected_text(text,blocks)):
        raise ValueError('legacy source text differs from rendered article')
    expected=[''.join(lines[b['start']-1:b['end']]) for b in blocks if b['kind']=='literal']
    expected=[s if s.endswith('\n') else s+'\n' for s in expected]
    if expected!=rendered.code_blocks:raise ValueError('legacy literal blocks differ from source')
    for b in blocks:
        if b['kind']=='title' and b['text'].lower()!=page['source_title'].lower():raise ValueError('source title lost')
    return {'articles':1,'legacy_text_articles':1,'source_lines':len(lines),'literal_blocks':len(expected),
            'prose_blocks':sum(b['kind']=='prose' for b in blocks),'headings':sum(b['kind']=='heading' for b in blocks)}
