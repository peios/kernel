import hashlib
import html
import json
from pathlib import Path
import sys
import tempfile
import unittest

from binding_references import verify_wrapper,check_document


class BindingPreservationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        # Works both in the installed tree and in a staged copy beside plugin/.
        here=Path(__file__).resolve().parent
        plugin=here.parent/'plugin'
        if not plugin.exists():plugin=here.parents[1]/'tools/docs/trail-kernel-doc'
        sys.path[:0]=[str(plugin/'.deps'),str(plugin)]
        from binding_schema import Registry
        from binding_markdown import Renderer
        self.source=self.root/'Documentation/devicetree/bindings/test.yaml'
        self.source.parent.mkdir(parents=True)
        self.source.write_text('$id: http://devicetree.org/schemas/test.yaml#\ntitle: Test binding\nproperties:\n  compatible:\n    pattern: \'^(a|b)\\.[0-9]+$\'\nmaintainers:\n  - \'"Name" <name@example.org>\'\nif:\n  required: [mode]\nthen:\n  properties:\n    foo: false\nexamples:\n  - |\n    test { value = <1>; };\n')
        lib=self.root/'library';lib.mkdir();self.registry=Registry(self.root,lib)
        self.doc=self.registry.by_path[self.source];self.refs={self.source:'kernel/test'}
        self.markdown='---\ntitle: Test binding\n---\n\n```{kernel-binding} Documentation/devicetree/bindings/test.yaml\n```\n'
        self.page={'source':str(self.source.relative_to(self.root)),'source_sha256':hashlib.sha256(self.source.read_bytes()).hexdigest(),
            'current_output_sha256':hashlib.sha256(self.markdown.encode()).hexdigest(),'source_title':'Test binding',
            'generated_reference':{'kind':'device-tree-binding','argument':str(self.source.relative_to(self.root))}}
        from markdown_it import MarkdownIt
        self.rendered='<h1>Test binding</h1>'+MarkdownIt('commonmark',{'html':True}).render(Renderer(self.registry,self.doc,self.refs).render())

    def test_literal_pattern_quotes_and_examples_survive_markdown(self):
        result=check_document(self.doc,self.doc.data,self.rendered,self.page,self.registry,self.refs)
        self.assertEqual(result['examples'],1)
        self.assertEqual(result['articles'],1)

    def test_checker_detects_value_example_and_anchor_loss(self):
        from binding_schema import anchor
        for damaged in [self.rendered.replace('[0-9]','[A-Z]'),self.rendered.replace('value = &lt;1&gt;','value = &lt;2&gt;'),self.rendered.replace(anchor('/then'),'missing')]:
            self.assertNotEqual(damaged,self.rendered)
            with self.assertRaises(ValueError):check_document(self.doc,self.doc.data,damaged,self.page,self.registry,self.refs)

    def test_wrapper_source_and_fence_checks(self):
        self.assertEqual(verify_wrapper(self.root,self.page,self.markdown)['device_tree_binding_wrappers'],1)
        wrong=self.markdown.replace('test.yaml','other.yaml')
        self.page['current_output_sha256']=hashlib.sha256(wrong.encode()).hexdigest()
        with self.assertRaisesRegex(ValueError,'source fence'):verify_wrapper(self.root,self.page,wrong)
        self.source.write_text('changed')
        with self.assertRaisesRegex(ValueError,'source changed'):verify_wrapper(self.root,self.page,self.markdown)


if __name__=='__main__':unittest.main()
