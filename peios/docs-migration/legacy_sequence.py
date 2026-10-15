"""Bounded conversion of mac80211's WebSequenceDiagrams source to Mermaid."""
import re
from legacy_text import escape, fence, sha, article_content


def convert(text):
    lines=text.splitlines();comments=[];events=[];out=['sequenceDiagram'];stack=[];i=0
    while i<len(lines):
        s=lines[i].strip();i+=1
        if not s:continue
        if s.startswith('#'):
            if s[1:].strip():comments.append(s[1:].strip())
            continue
        if s.startswith('participant '):
            name=s.split()[1];events.append(['participant',name]);out.append('    '+s)
        elif s.startswith('alt '):
            events.append(['alt',s[4:]]);stack.append('alt');out.append('    '+s)
        elif s.startswith('else '):
            if not stack:raise ValueError('else outside alt')
            events.append(['else',s[5:]]);out.append('    '+s)
        elif s=='end':
            if not stack:raise ValueError('unmatched end')
            stack.pop();events.append(['end']);out.append('    end')
        elif re.match(r'^\w+->\w+:',s):
            m=re.fullmatch(r'(\w+)->(\w+):\s*(.*)',s)
            events.append(['message',m[1],m[2],m[3]])
            out.append(f'    {m[1]}->>{m[2]}: {m[3]}')
        elif s.startswith('note '):
            if ':' in s:target,label=s[5:].split(':',1);label=label.strip()
            else:
                target=s[5:];parts=[]
                while i<len(lines) and lines[i].strip()!='end note':parts.append(lines[i].strip());i+=1
                if i==len(lines):raise ValueError('unclosed note')
                i+=1;label='<br/>'.join(parts)
            events.append(['note',target,label]);out.append('    Note '+target+': '+label)
        else:raise ValueError('unsupported sequence syntax: '+s)
    if stack:raise ValueError('unclosed alt')
    return '\n'.join(out)+'\n',comments,events


def render(text):
    mermaid,comments,events=convert(text)
    return escape('\n'.join(comments))+'\n\n'+fence(mermaid,'mermaid')+'\n',dict(
        kind='websequence-to-mermaid',mermaid_sha256=sha(mermaid),events=events,
        source_lines=len(text.splitlines()),comments=comments)


def verify(root,page,markdown,rendered_html=None):
    from markdown_it import MarkdownIt
    from verify import Visible,normal
    text=(root/page['source']).read_text();mermaid,comments,events=convert(text)
    if sha(text)!=page['source_sha256'] or sha(markdown)!=page['current_output_sha256']:
        raise ValueError('sequence baseline changed')
    record=page['legacy_text']
    if events!=record['events'] or sha(mermaid)!=record['mermaid_sha256']:raise ValueError('sequence events changed')
    md=MarkdownIt('commonmark',{'html':True});body=markdown.split('---\n',2)[2]
    diagrams=[t.content for t in md.parse(body) if t.type=='fence' and t.info=='mermaid']
    if diagrams!=[mermaid]:raise ValueError('sequence diagram differs from source events')
    visible=Visible();visible.feed(article_content(rendered_html,page['source_title']) if rendered_html is not None else md.render(body))
    if normal('\n'.join(comments)+'\n'+mermaid)!=normal(''.join(visible.text)):
        raise ValueError('sequence text not preserved in HTML')
    return {'articles':1,'legacy_text_articles':1,'source_lines':len(text.splitlines()),
            'sequence_diagrams':1,'sequence_events':len(events)}
