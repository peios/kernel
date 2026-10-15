# SPDX-License-Identifier: GPL-2.0
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'.deps'))
from binding_schema import Document,Registry,Loader,anchor,pointer
from binding_markdown import Renderer
import yaml


class BindingTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.bindings=self.root/'Documentation/devicetree/bindings';self.bindings.mkdir(parents=True)
        self.library=self.root/'library';self.library.mkdir()
    def tearDown(self):self.tmp.cleanup()
    def doc(self,name,body):
        p=self.bindings/name;p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text('$id: http://devicetree.org/schemas/'+name+'#\n$schema: http://devicetree.org/meta-schemas/core.yaml#\ntitle: Test binding\n'+body)
        return p
    def registry(self):return Registry(self.root,self.library)
    def test_yaml_12_strings_numbers_and_duplicate_rejection(self):
        data=yaml.load('a: on\nb: yes\nc: 012\nd: 0x20\ne: true\nf: 2026-01-01\n',Loader=Loader)
        self.assertEqual(data,dict(a='on',b='yes',c=12,d=32,e=True,f='2026-01-01'))
        with self.assertRaisesRegex(ValueError,'duplicate'):yaml.load('a: 1\na: 2',Loader=Loader)
    def test_unsafe_yaml_and_non_json_values_fail(self):
        with self.assertRaises(yaml.YAMLError):yaml.load('!!python/object/apply:os.system [echo bad]',Loader=Loader)
        p=self.doc('bad.yaml','default: .inf\n')
        with self.assertRaisesRegex(ValueError,'non-JSON'):Document(p)
    def test_comments_do_not_steal_hashes_from_examples_or_strings(self):
        p=self.doc('one.yaml','description: "# not a comment" # real note\nexamples:\n  - |\n    node { #address-cells = <1>; }; // # literal\n')
        doc=Document(p);self.assertEqual([c['text'] for c in doc.comments],[' real note'])
    def test_relative_refs_pointer_escapes_and_cycles(self):
        a=self.doc('dir/a.yaml','allOf:\n  - $ref: ../b.yaml#/$defs/a~1b~0c\n')
        b=self.doc('b.yaml','$defs:\n  a/b~c:\n    $ref: dir/a.yaml#\n')
        r=self.registry();target,ptr=r.resolve(r.by_path[a],'../b.yaml#/$defs/a~1b~0c')
        self.assertEqual(target.path,b);self.assertIn(ptr,target.index);self.assertEqual(r.closure(r.by_path[a]),{a,b})
    def test_missing_files_pointers_and_remote_refs_fail(self):
        p=self.doc('one.yaml','properties: {}\n');r=self.registry();d=r.by_path[p]
        for ref in ['absent.yaml','#/properties/nope','https://evil.example/schema.yaml']:
            with self.assertRaises(ValueError):r.resolve(d,ref)
    def test_invalid_paths_and_symlink_escape_fail(self):
        self.doc('one.yaml','properties: {}\n');r=self.registry()
        for path in ['/etc/passwd','Documentation/devicetree/bindings/../bindings/one.yaml','Documentation/devicetree/bindings/no.yaml']:
            with self.assertRaises(ValueError):r.requested(path)
        outside=self.root/'outside.yaml';outside.write_text('x: 1');(self.bindings/'escape.yaml').symlink_to(outside)
        with self.assertRaisesRegex(ValueError,'symlink'):self.registry()
    def test_condition_structure_and_false_properties_are_explicit(self):
        p=self.doc('one.yaml','properties:\n  foo: false\nif:\n  required: [mode]\nthen:\n  required: [foo]\nelse:\n  properties:\n    bar: true\noneOf:\n  - required: [a]\n  - required: [b]\n')
        r=self.registry();out=Renderer(r,r.by_path[p],{p:'kernel/test'}).render()
        for phrase in ['Not permitted by this property rule','When the condition matches','When the condition does not match','Exactly one of these rules must match','not listed as required here']:
            self.assertIn(phrase,out)
        self.assertLess(out.index('When the condition matches'),out.index('When the condition does not match'))
    def test_unknown_keyword_and_missing_wrapper_fail(self):
        p=self.doc('one.yaml','futureKeyword: true\n');r=self.registry()
        with self.assertRaisesRegex(ValueError,'unsupported'):Renderer(r,r.by_path[p],{p:'kernel/test'}).render()
        self.doc('one.yaml','$ref: two.yaml#\n');self.doc('two.yaml','properties: {}\n');r=self.registry()
        with self.assertRaisesRegex(ValueError,'missing Trail wrapper'):Renderer(r,r.by_path[p],{p:'kernel/test'}).render()
    def test_example_and_description_markup_is_escaped(self):
        p=self.doc('one.yaml','description: "<script>bad</script> & text"\nexamples:\n  - |\n    node {\n      value = <1>;\n    };\n')
        r=self.registry();out=Renderer(r,r.by_path[p],{p:'kernel/test'}).render()
        self.assertNotIn('<script>',out);self.assertIn('&lt;script&gt;',out);self.assertIn('value = &lt;1&gt;',out)
        self.assertIn('};\n</code></pre>',out)
    def test_dependencies_keep_original_pointers(self):
        p=self.doc('one.yaml','dependencies:\n  foo: [bar, baz]\n');r=self.registry();out=Renderer(r,r.by_path[p],{p:'kernel/test'}).render()
        self.assertIn('id="'+anchor('/dependencies/foo/0')+'"',out)
        self.assertIn('applies when this property is present',out)
    def test_protocol_and_source_changes_refresh(self):
        p=self.doc('one.yaml','description: original\n')
        block={'id':'one','reference':'kernel/test','argument':'Documentation/devicetree/bindings/one.yaml','options':{},'body':''}
        def run(blocks):
            result=subprocess.run([sys.executable,str(HERE/'trail-kernel-binding'),'--srctree',str(self.root)],input=json.dumps({'protocol':1,'blocks':blocks}),text=True,capture_output=True,check=True)
            self.assertEqual(result.stderr,'');return json.loads(result.stdout)
        first=run([block]);self.assertIn(str(p),first['depends_on']);self.assertIn(str(self.bindings),first['depends_on'])
        self.assertIn('original',first['blocks'][0]['markdown'])
        p.write_text(p.read_text().replace('original','updated'))
        second=run([block]);self.assertIn('updated',second['blocks'][0]['markdown'])
        bad={**block,'id':'bad','body':'unsupported'};response=run([block,bad]);self.assertIn('error',response['blocks'][1]);self.assertIn('markdown',response['blocks'][0])
    def test_duplicate_schema_ids_fail(self):
        p=self.doc('one.yaml','properties: {}\n');(self.bindings/'two.yaml').write_text(p.read_text())
        with self.assertRaisesRegex(ValueError,'duplicate schema identifier'):self.registry()


if __name__=='__main__':unittest.main()
