import json
from pathlib import Path
import tempfile
import unittest
from markdown_it import MarkdownIt
import legacy_text as lt
import legacy_sequence as seq


class LegacyTextTests(unittest.TestCase):
    def render(self,text,source='devicetree/bindings/test.txt'):
        title,blocks=lt.parse(source,text);body,links=lt.render(source,text,blocks,{})
        return title,blocks,body

    def test_dts_tabs_and_blank_lines_remain_literal(self):
        source='Binding\n\nExample:\n\nnode {\n\treg = <1>;\n\t\n\tchild { x = <2>; };\n};\n'
        _,blocks,body=self.render(source)
        code=[t.content for t in MarkdownIt().parse(body) if t.type=='fence']
        self.assertEqual(code,['node {\n\treg = <1>;\n\t\n\tchild { x = <2>; };\n};\n'])

    def test_nested_property_list_keeps_indentation(self):
        _,_,body=self.render('Binding\n\n- property: choose\n  - nested value\n  - another value\n')
        self.assertIn('```text\n- property: choose\n  - nested value',body)

    def test_pseudocode_split_from_surrounding_prose(self):
        _,_,body=self.render('Notes on propagate_umount()\n\nDo this\n\tS = {}\n\tfor each m\n\t\tadd m\nthen continue.\n','filesystems/propagate_umount.txt')
        self.assertIn('```text\n\tS = {}\n\tfor each m\n\t\tadd m\n```',body)
        self.assertIn('then continue.',body)

    def test_escape_html_and_markdown_preserves_visible_text(self):
        from verify import Visible,normal
        text='<node> & [value] *literal* `tick` _name_ {thing}'
        rendered=Visible();rendered.feed(MarkdownIt('commonmark',{'html':True}).render(lt.escape(text)))
        self.assertEqual(normal(''.join(rendered.text)),text)
        self.assertNotIn('node',rendered.counts)

    def test_bibtex_is_not_parsed_as_prose(self):
        text='Read the Fscking Papers!\n\n@article{Key,\n title={Nested {braces}},\n\n note={A < B}\n}\n'
        _,_,body=self.render(text,'RCU/RTFP.txt')
        code=[t.content for t in MarkdownIt().parse(body) if t.type=='fence']
        self.assertEqual(code,[text.split('\n\n',1)[1]])

    def test_longer_fence_for_source_backticks(self):
        self.assertTrue(lt.fence('```\n').startswith('````text'))

    def test_line_coverage_and_rendered_mutations_fail(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p=root/'Documentation/devicetree/bindings/test.txt';p.parent.mkdir(parents=True)
            text='Binding\n\nUseful prose.\n\nExample:\n\nnode { x = <1>; };\n';p.write_text(text)
            title,blocks,body=self.render(text);md='---\ntitle: Binding\n---\n\n'+body
            page={'source':str(p.relative_to(root)),'source_sha256':lt.sha(text),'source_title':title,'current_output_sha256':lt.sha(md),'legacy_text':{'blocks':blocks}}
            lt.verify_page(root,page,md)
            html='<h1>Binding</h1>'+MarkdownIt().render(body).replace('Useful','Missing')
            with self.assertRaisesRegex(ValueError,'source text'):lt.verify_page(root,page,md,html)
            blocks[1]['start']+=1
            with self.assertRaisesRegex(ValueError,'gap or overlap'):lt.verify_page(root,page,md)

    def test_relative_links_only_resolve_existing_targets(self):
        links=[];body=lt.inline('See ../gpio/gpio.txt and missing.txt','devicetree/bindings/arm/foo.txt',{'devicetree/bindings/gpio/gpio.txt':{'reference':'kernel/hardware/gpio'}},links)
        self.assertIn('~kernel/hardware/gpio',body);self.assertEqual(len(links),1)
        self.assertIn('missing.txt',body)

    def test_no_sentence_promoted_mid_paragraph(self):
        _,blocks,_=self.render('Binding\n\nHere is a sentence\nwhich introduces some things:\nthings follow.\n')
        self.assertFalse(any(b['kind']=='heading' for b in blocks))

    def test_sequence_events_and_notes(self):
        text='participant a\nparticipant b\nalt ready\na->b: request\nnote over a,b\nfirst\nsecond\nend note\nelse wait\nb->a: retry\nend\n'
        mermaid,_,events=seq.convert(text)
        self.assertIn('Note over a,b: first<br/>second',mermaid)
        self.assertEqual([e for e in events if e[0]=='message'],[['message','a','b','request'],['message','b','a','retry']])
        with self.assertRaises(ValueError):seq.convert('end\n')
        with self.assertRaises(ValueError):seq.convert('unknown directive\n')


if __name__=='__main__':unittest.main()
