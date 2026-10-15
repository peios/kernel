import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from docutils import nodes
from markdown_it import MarkdownIt
import bulk
import generated

class GeneratedTests(unittest.TestCase):
    def test_uapi_paths_and_exception_files_remain_source_relative(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'Documentation').mkdir();(root/'header.h').write_text('int x;\n')
            (root/'Documentation/header.exceptions').write_text('ignore define X\n')
            p=root/'Documentation/page.rst';p.write_text('Title\n=====\n\n.. kernel-include:: header.h\n   :generate-cross-refs:\n   :toc:\n   :exception-file: header.exceptions\n')
            with patch('generated.ROOT',root):
                tree=bulk.parse(p);record=generated.records(tree)[0]
                self.assertEqual(record['options']['exception-file'],'Documentation/header.exceptions')
                self.assertEqual(record['argument'],'header.h')
                body=generated.markdown(next(tree.findall(generated.Generated)))
                generated.verify(tree,MarkdownIt().parse(body))
                with self.assertRaisesRegex(ValueError,'path/options/order'):
                    generated.verify(tree,MarkdownIt().parse(body.replace('header.h','wrong.h')))

    def test_math_preserves_tex_and_equation_boundaries(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'a.rst';p.write_text('Title\n=====\n\n.. math::\n   :nowrap:\n\n   a\\_b + \\frac{1}{2}\n\n   c\\ d\n\nInline :math:`a\\ (mod~4)`.\n')
            tree=bulk.parse(p);writer=bulk.BulkWriter('a.rst',{'a.rst':{}},{},'commit',set(),{})
            body=writer.anchors(tree)+'\n'+writer.block(tree)
            counts=bulk.verify_page(tree,body,writer)
            self.assertEqual(counts['display_equations'],2)
            self.assertEqual(counts['inline_equations'],1)
            with self.assertRaisesRegex(ValueError,'TeX changed'):
                bulk.verify_page(tree,body.replace('a\\_b','a_b'),writer)

if __name__=='__main__':unittest.main()
