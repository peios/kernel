import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from figures import Figures


class FigureTests(unittest.TestCase):
    def test_source_drift_is_a_build_error_and_dependencies_are_complete(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source=root/'source.dot';source.write_text('digraph {a -> b}')
            target=root/'replacement.mmd';target.write_text('flowchart TB\n  a --> b\n')
            registry=root/'registry.json'
            registry.write_text(json.dumps({'source.dot':{'source':'source.dot','mermaid':'replacement.mmd',
                'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest()}}))
            f=Figures(root,root);markdown,caption=f.render('source.dot',{},['Caption.'])
            self.assertIn('```mermaid',markdown);self.assertEqual(caption,'Caption.')
            self.assertTrue({str(source),str(target),str(registry)}<=f.dependencies)
            source.write_text('digraph {a -> c}')
            with self.assertRaisesRegex(ValueError,'upstream diagram changed'):f.render('source.dot',{},[])
            with self.assertRaisesRegex(ValueError,'reviewed Mermaid'):f.render('unknown.dot',{},[])
