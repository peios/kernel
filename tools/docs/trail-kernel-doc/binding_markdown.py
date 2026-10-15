# SPDX-License-Identifier: GPL-2.0
"""Readable, structurally faithful views of authored device-tree schemas."""
import html
import json
import re
from binding_schema import anchor,pointer

LABELS={
 '$id':'Schema identifier', '$schema':'Schema dialect', 'title':'Title',
 'description':'Description', 'maintainers':'Maintainers', '$comment':'Schema comment',
 'properties':'Properties and child nodes', 'patternProperties':'Properties matching a name pattern',
 'required':'Required in this object', 'dependentRequired':'Requirements triggered by another property',
 'dependencies':'Property dependencies', 'dependentSchemas':'Rules triggered by another property',
 'allOf':'All of these rules must match', 'anyOf':'At least one of these rules must match',
 'oneOf':'Exactly one of these rules must match', 'not':'This rule must not match',
 'if':'Condition', 'then':'When the condition matches', 'else':'When the condition does not match',
 'select':'Automatic schema selection', '$defs':'Reusable definitions', 'definitions':'Reusable definitions',
 'additionalProperties':'Properties not matched by properties or patternProperties in this schema',
 'unevaluatedProperties':'Properties not evaluated by applicable rules',
 'additionalItems':'Array items beyond the listed positions', 'unevaluatedItems':'Array items not evaluated by applicable rules',
 'items':'Array item rules', 'prefixItems':'Rules for successive array positions', 'contains':'Rule for matching array elements',
 'propertyNames':'Rule for property names', 'type':'Value type', 'typeSize':'Integer width in bits',
 'const':'Exact value', 'enum':'Allowed values', 'default':'Default value', 'examples':'Examples',
 'minimum':'Minimum value', 'maximum':'Maximum value', 'exclusiveMinimum':'Value must be greater than',
 'exclusiveMaximum':'Value must be less than', 'multipleOf':'Multiple of',
 'minItems':'Minimum number of items', 'maxItems':'Maximum number of items', 'uniqueItems':'Items must be unique',
 'minContains':'Minimum number of matching elements', 'maxContains':'Maximum number of matching elements',
 'minLength':'Minimum string length', 'maxLength':'Maximum string length', 'pattern':'String pattern',
 'minProperties':'Minimum number of properties', 'maxProperties':'Maximum number of properties',
 'deprecated':'Deprecated', 'readOnly':'Read only', 'writeOnly':'Write only', 'format':'String format', '$ref':'Shared schema rule',
}
NAMED={'properties','patternProperties','$defs','definitions','dependencies','dependentSchemas'}
SCHEMAS={'allOf','anyOf','oneOf','not','if','then','else','select','additionalProperties','unevaluatedProperties',
         'items','prefixItems','contains','additionalItems','unevaluatedItems','propertyNames'}


def esc(value):return html.escape(str(value),quote=False)


def code(value):
    # Inline HTML still passes through Markdown's inline parser. Character
    # references keep literal backslashes, brackets and emphasis markers intact.
    return '<code>'+''.join(c if c.isalnum() or c==' ' else '&#'+str(ord(c))+';' for c in str(value))+'</code>'


def scalar(value,ptr):
    value=json.dumps(value,ensure_ascii=False,allow_nan=False)
    return '<span id="'+anchor(ptr)+'">'+code(value)+'</span>'


def mark(ptr):return '<a id="'+anchor(ptr)+'"></a>'


def heading(title,ptr,level):
    # Only a few levels go into Trail's on-page TOC. Deeper conditional rules
    # remain explicitly nested via blockquotes and named rule branches.
    return mark(ptr)+'\n\n'+('#'*min(level,6)+' ' if level<=4 else '**')+title+('**' if level>4 else '')+'\n\n'


def quote_block(text):return '\n'.join('> '+line if line else '>' for line in text.rstrip().splitlines())+'\n\n'


def description(value,ptr):
    if not isinstance(value,str):raise ValueError('description must be a string')
    chunks=re.split(r'\n\s*\n',value.strip('\n'));parts=[]
    for chunk in chunks:
        structured=any(re.match(r'^(?: {2,}|\t)',line) for line in chunk.splitlines())
        if structured:parts.append('<pre><code>'+esc(chunk)+'</code></pre>')
        else:parts.append('<p style="white-space: pre-wrap">'+esc(chunk)+'</p>')
    return '<div id="'+anchor(ptr)+'">\n'+ '\n'.join(parts)+'\n</div>\n\n'


class Renderer:
    def __init__(self,registry,doc,pages):
        self.registry=registry;self.doc=doc;self.pages=pages;self.references=[]

    def data(self,value,ptr,marked=False):
        prefix='' if marked else mark(ptr)+' '
        if isinstance(value,list):
            # Preserve item boundaries and stable targets, including an empty array.
            if not value:return prefix+code('[]')
            return prefix+', '.join(self.data(v,pointer(ptr,i)) for i,v in enumerate(value))
        if isinstance(value,dict):
            if not value:return prefix+code('{}')
            return prefix+'{ '+', '.join(code(k)+': '+self.data(v,pointer(ptr,k)) for k,v in value.items())+' }'
        return scalar(value,ptr)

    def reference(self,value,ptr):
        target,fragment=self.registry.resolve(self.doc,value)
        if target.path not in self.pages:raise ValueError('missing Trail wrapper for '+self.registry.source(target))
        href=('#' if target.path==self.doc.path else '~'+self.pages[target.path]+'#')+anchor(fragment)
        self.references.append({'pointer':ptr,'source_ref':value,'target':self.registry.source(target),'target_pointer':fragment,'href':href})
        return '<span id="'+anchor(ptr)+'">['+code(value)+'](<'+href+'>)</span>'

    def schema(self,value,ptr='',level=2,marked=False):
        out='' if marked else mark(ptr)+'\n\n'
        if isinstance(value,bool):
            explanation='This rule adds no constraints.' if value else 'This rule rejects the value.'
            return (scalar(value,ptr) if not marked else code(str(value).lower()))+' — '+explanation+'\n\n'
        if not isinstance(value,dict):raise ValueError('expected a schema object or boolean at '+ptr)
        unknown=set(value)-set(LABELS)
        if unknown:raise ValueError('unsupported schema keywords at '+ptr+': '+', '.join(sorted(unknown)))
        if not value:return out+'This rule adds no constraints.\n\n'
        for key,child in value.items():
            p=pointer(ptr,key);label=LABELS[key]+' ('+code(key)+')'
            if key=='title' and not ptr:
                # The wrapper owns the page title, independently checked against
                # the source. Keep its source-pointer target at the top of the body.
                out+=mark(p)+'\n\n';continue
            if key=='description':out+=description(child,p);continue
            if key=='$ref':out+='**'+label+':** '+self.reference(child,p)+'\n\n';continue
            if key=='examples':
                out+=heading(label,p,level)
                if not isinstance(child,list):raise ValueError('examples must be an array')
                for i,example in enumerate(child):
                    ep=pointer(p,i)
                    if not isinstance(example,str):out+=self.data(example,ep)+'\n\n';continue
                    # HTML escaping preserves the source example exactly, including
                    # its EOF newline; no Markdown fence normalization is involved.
                    out+='<pre id="'+anchor(ep)+'"><code class="language-dts">'+esc(example)+'</code></pre>\n\n'
                continue
            if key in NAMED:
                if not isinstance(child,dict):raise ValueError(key+' must be a map')
                out+=heading(label,p,level)
                for name,rule in child.items():
                    cp=pointer(p,name)
                    status=''
                    if key=='properties':status=' — required here' if name in value.get('required',[]) else ' — not listed as required here'
                    if key=='patternProperties':status=' — name matches this regular expression'
                    if key in ('dependencies','dependentSchemas'):status=' — applies when this property is present'
                    # A boolean property is a real schema leaf, so emit the same
                    # scalar anchor the fidelity checker expects.
                    out+=heading(code(name)+status,cp,level+1)
                    if key=='dependencies' and isinstance(rule,list):out+='Also requires: '+self.data(rule,cp,marked=True)+'\n\n'
                    elif isinstance(rule,bool):
                        out+=code(str(rule).lower())+' — '+('No constraints added by this property rule.' if rule else 'Not permitted by this property rule.')+'\n\n'
                    else:out+=self.schema(rule,cp,level+2,marked=True)
                continue
            if key in SCHEMAS:
                out+=heading(label,p,level)
                if isinstance(child,list):
                    for i,rule in enumerate(child):
                        cp=pointer(p,i);name=('Item '+str(i+1)) if key in ('items','prefixItems') else 'Rule '+str(i+1)
                        out+=heading(name,cp,level+1)+quote_block(self.schema(rule,cp,level+2,marked=True))
                elif isinstance(child,bool):
                    out+=code(str(child).lower())+'\n\n'
                    if key=='select':out+=('This selection rule always matches.' if child else 'Not selected automatically by this rule.')+'\n\n'
                    elif key in ('additionalProperties','unevaluatedProperties','additionalItems','unevaluatedItems'):
                        out+=('Allowed by this rule.' if child else 'Not allowed by this rule.')+'\n\n'
                    else:out+=('This rule adds no constraints.' if child else 'This rule rejects the value.')+'\n\n'
                else:out+=quote_block(self.schema(child,p,level+1,marked=True))
                continue
            out+='**'+label+':** '+self.data(child,p)+'\n\n'
        return out

    def render(self):
        result=self.schema(self.doc.data)
        if self.doc.comments:
            result+='## Source notes\n\n<details>\n<summary>Annotations retained from the schema source</summary>\n\n'
            for i,comment in enumerate(self.doc.comments):
                result+='<p id="dt-comment-'+str(i)+'"><strong>Line '+str(comment['line'])+':</strong> <span>'+esc(comment['text'])+'</span></p>\n\n'
            result+='</details>\n'
        return result
