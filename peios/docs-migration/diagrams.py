"""Bounded DOT-to-Mermaid rewrite used only at migration time.

Preserves visible nodes, directed edges, labels, port routing, colours and
clusters. Graphviz positioning hints are deliberately replaced by Mermaid's
layout. Unsupported semantic attributes fail rather than disappearing.
"""
import hashlib
import html
import re
from collections.abc import Mapping
import pydot


def unquote(value):
    value = str(value)
    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    return value.replace('\\"', '"').replace('\\n', '\n').replace('\\l', '\n').replace('\\r', '\n')


def label(value):
    # Mermaid entity escaping, with explicit HTML line breaks.
    return '<br/>'.join(''.join(f'#{ord(c)};' if c in '"&<>|#`' else c for c in line.strip()) for line in value.splitlines())


def normalize_dot(text):
    # Pydot does not accept Graphviz's semicolon attribute separators or commas
    # between members of endpoint sets. Change separators only outside strings.
    parts=re.split(r'("(?:\\.|[^"\\])*")', text)
    for i in range(0,len(parts),2):
        parts[i]=re.sub(r'\{(\w+(?:,\s*\w+)+)\}',lambda m:'{'+m[1].replace(',',';')+'}',parts[i])
    text=''.join(parts)
    result=[];quoted=False;escaped=False;bracket=0
    for c in text:
        if c=='"' and not escaped:quoted=not quoted
        if not quoted:
            if c=='[':bracket+=1
            elif c==']':bracket-=1
            elif c==';' and bracket:c=','
        result.append(c)
        escaped=(c=='\\' and not escaped)
    return ''.join(result)


def convert(text):
    graphs=pydot.graph_from_dot_data(normalize_dot(text))
    if not graphs or len(graphs)!=1:raise ValueError('expected one DOT graph')
    graph=graphs[0];ns={};edges=[];groups=[];members={};omitted=[]
    def attrs(obj):return {k:unquote(v) for k,v in obj.get_attributes().items()}
    def node(name,defaults,group):
        name=unquote(name)
        if name not in ns:ns[name]=dict(defaults)
        if group is not None and name not in members:members[name]=group
        return name
    def endpoint(value,defaults,group):
        if isinstance(value,Mapping):
            if value.get('edges') or value.get('subgraphs'):raise ValueError('complex endpoint subgraph')
            return [(node(k,defaults,group),'') for k in value['nodes']]
        match=re.fullmatch(r'("(?:\\.|[^"\\])*"|[^:]+)(?::(.+))?',value)
        if not match:raise ValueError('unsupported endpoint '+str(value))
        return [(node(match[1],defaults,group),unquote(match[2] or ''))]
    def walk(g,nd,ed,parent=None):
        nd=dict(nd);ed=dict(ed);gid=parent
        if g!=graph and unquote(g.get_name()).startswith('cluster'):
            gid=len(groups);groups.append({'id':gid,'parent':parent,**attrs(g)})
        entries=sorted(g.get_nodes()+g.get_edges()+g.get_subgraphs(),key=lambda x:x.obj_dict.get('sequence',0))
        for obj in entries:
            if isinstance(obj,pydot.Subgraph):walk(obj,nd,ed,gid)
            elif isinstance(obj,pydot.Node):
                name=unquote(obj.get_name());a=attrs(obj)
                if name=='node':nd.update(a)
                elif name=='edge':ed.update(a)
                elif name=='graph':
                    if gid is not None:groups[gid].update(a)
                elif name.strip() and name!='\\n':ns[node(name,nd,gid)].update(a)
            else:
                a={**ed,**attrs(obj)}
                for source,sp in endpoint(obj.get_source(),nd,gid):
                    for dest,dp in endpoint(obj.get_destination(),nd,gid):edges.append((source,sp,dest,dp,a))
    walk(graph,{}, {})
    allowed_node=set('label shape style fillcolor bgcolor color fontcolor colorscheme fontsize fontname width height fixedsize margin penwidth peripheries pos ordering group'.split())
    allowed_edge=set('label xlabel headlabel taillabel style dir color fontcolor fontsize fontname penwidth minlen constraint weight arrowhead arrowtail arrowsize lhead ltail headport tailport'.split())
    allowed_group=set('id parent label labelloc rankdir rank style fillcolor color fontcolor fontsize fontname margin penwidth'.split())
    for name,a in ns.items():
        if set(a)-allowed_node:raise ValueError(f'unsupported node attributes: {set(a)-allowed_node}')
    for *_,a in edges:
        if set(a)-allowed_edge:raise ValueError(f'unsupported edge attributes: {set(a)-allowed_edge}')
        if any(a.get(k) not in (None,'normal','none') for k in ('arrowhead','arrowtail')):raise ValueError('special arrow shape')
    for a in groups:
        if set(a)-allowed_group:raise ValueError(f'unsupported cluster attributes: {set(a)-allowed_group}')
    palette=['#7fc97f','#beaed4','#fdc086','#ffff99']
    def color(value,a):
        if a.get('colorscheme')=='accent4' and value.isdigit():return palette[int(value)-1]
        if not re.fullmatch(r'#[0-9a-fA-F]{3,8}|[a-zA-Z]+',value):raise ValueError('unsupported colour '+value)
        return value
    ports={};names={};visible={}
    for name,a in ns.items():
        if 'invis' in a.get('style',''):omitted.append('invisible node '+name);continue
        text_label=a.get('label',name).replace('\\N',name)
        if text_label.startswith('<') and text_label.endswith('>'):raise ValueError('HTML DOT label needs review')
        shape=a.get('shape','ellipse')
        if shape=='point':text_label=''
        ports[name]={p:re.sub(r'[{}]','',v).strip() for p,v in re.findall(r'<([^>]+)>\s*([^|{}]*)',text_label)}
        if shape.lower() in ('record','mrecord'):
            text_label=re.sub(r'<([^>]+)>\s*', 'pad ', text_label)
            text_label=re.sub(r'[{}]', '', text_label)
            text_label=re.sub(r'\s*\|\s*','\n',text_label).strip()
        names[name]='n'+str(len(names));visible[name]={**a,'text':text_label}
    direction=unquote(graph.get_rankdir() or 'TB')
    if direction not in ('TB','BT','LR','RL'):raise ValueError('bad direction')
    lines=['flowchart '+direction]
    def declaration(name):
        a=visible[name];shape=a.get('shape','ellipse').lower();text_label='"'+(label(a['text']) or '#160;')+'"'
        forms={'box':('[',']'),'rect':('[',']'),'rectangle':('[',']'),'record':('[',']'),'mrecord':('[',']'),
               'diamond':('{','}'),'ellipse':('([','])'),'oval':('([','])'),'circle':('((', '))'),
               'doublecircle':('(((', ')))'),'point':('((', '))'),'cylinder':('[(', ')]'),'plaintext':('[',']'),'plain':('[',']')}
        if shape not in forms:raise ValueError('unsupported shape '+shape)
        left,right=forms[shape];return names[name]+left+text_label+right
    def emit_group(gid,level):
        prefix='  '*level
        for name in visible:
            if members.get(name)==gid:lines.append(prefix+declaration(name))
        for group in groups:
            if group['parent']==gid:
                lines.append(prefix+f'subgraph g{group["id"]}["'+(label(group.get('label','')) or '#160;')+'"]')
                if group.get('rankdir'):lines.append(prefix+'  direction '+group['rankdir'])
                emit_group(group['id'],level+1);lines.append(prefix+'end')
    emit_group(None,1)
    semantic_edges=[];edge_styles=[]
    for source,sp,dest,dp,a in edges:
        if 'invis' in a.get('style',''):omitted.append('invisible edge '+source+' -> '+dest);continue
        if source not in visible or dest not in visible:raise ValueError('visible edge attached to invisible node')
        texts=[a[k] for k in ('taillabel','label','xlabel','headlabel') if a.get(k)]
        def port(name,p):
            if not p:return ''
            p=p.split(':')[0]
            if p in ports.get(name,{}):return ports[name][p]
            if p in ('n','ne','e','se','s','sw','w','nw','c','_'):return ''
            raise ValueError('unknown port '+name+':'+p)
        ps,pd=port(source,sp or a.get('tailport','')),port(dest,dp or a.get('headport',''))
        if ps and pd:texts.append('pad '+ps+' → pad '+pd)
        elif ps:texts.append('from pad '+ps)
        elif pd:texts.append('to pad '+pd)
        direction=a.get('dir','forward' if graph.get_type()=='digraph' else 'none')
        start,end=names[source],names[dest]
        if direction=='back':start,end=end,start
        if direction not in ('back','forward','both','none'):raise ValueError('unknown direction')
        arrow='<-->' if direction=='both' else '---' if direction=='none' or a.get('arrowhead')=='none' else '-->'
        text_label='|"'+label('\n'.join(texts))+'"|' if texts else ''
        lines.append('  '+start+' '+arrow+text_label+' '+end)
        styles=[]
        if 'dashed' in a.get('style',''):styles.append('stroke-dasharray:6 4')
        if 'dotted' in a.get('style',''):styles.append('stroke-dasharray:2 3')
        if 'bold' in a.get('style',''):styles.append('stroke-width:3px')
        if a.get('color'):styles.append('stroke:'+color(a['color'],a))
        if a.get('fontcolor'):styles.append('color:'+color(a['fontcolor'],a))
        if styles:edge_styles.append(f'  linkStyle {len(semantic_edges)} '+','.join(styles))
        semantic_edges.append({'source':source,'source_port':sp,'destination':dest,'destination_port':dp,'attributes':a})
    for name,a in visible.items():
        styles=[]
        if a.get('fillcolor'):styles.append('fill:'+color(a['fillcolor'],a))
        if a.get('color'):styles.append('stroke:'+color(a['color'],a))
        if a.get('fontcolor'):styles.append('color:'+color(a['fontcolor'],a))
        if a.get('fillcolor') and not a.get('fontcolor'):styles.append('color:#111')
        if a.get('shape')=='plaintext':styles.extend(['fill:transparent','stroke:transparent'])
        if a.get('shape')=='point':styles.extend(['fill:#333','stroke:#333'])
        if 'dashed' in a.get('style',''):styles.append('stroke-dasharray:6 4')
        if styles:lines.append('  style '+names[name]+' '+','.join(styles))
    for group in groups:
        styles=[]
        if group.get('fillcolor'):styles.append('fill:'+color(group['fillcolor'],group))
        if group.get('color'):styles.append('stroke:'+color(group['color'],group))
        if 'dashed' in group.get('style',''):styles.append('stroke-dasharray:6 4')
        if styles:lines.append('  style g'+str(group['id'])+' '+','.join(styles))
    lines+=edge_styles
    output='\n'.join(lines)+'\n'
    return output,{'source_sha256':hashlib.sha256(text.encode()).hexdigest(),
        'mermaid_sha256':hashlib.sha256(output.encode()).hexdigest(),
        'nodes':visible,'edges':semantic_edges,'layout_only_omissions':omitted}
