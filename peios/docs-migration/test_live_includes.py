import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from docutils import nodes
import bulk
import live_includes


class LiveIncludeTests(unittest.TestCase):
    def test_literal_preservation_and_altered_path_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'Documentation').mkdir();p=root/'Documentation/a.rst'
            (root/'Documentation/data.txt').write_text('\nfirst\n\f\n\tlast\n\n')
            p.write_text('Title\n=====\n\n.. include:: data.txt\n   :literal:\n')
            with patch('bulk.KERNEL_ROOT',root),patch('live_includes.ROOT',root):
                tree=bulk.parse(p);writer=bulk.BulkWriter('a.rst',{'a.rst':{}},{},'commit',set(),{})
                body=writer.anchors(tree)+'\n'+writer.block(tree)
                bulk.verify_page(tree,body,writer)
                self.assertIn('{kernel-include} Documentation/data.txt',body)
                with self.assertRaisesRegex(ValueError,'path differs'):
                    bulk.verify_page(tree,body.replace('Documentation/data.txt','Documentation/wrong.txt'),writer)

    def test_kernel_paths_are_root_relative(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'Documentation').mkdir();(root/'sample.txt').write_text('root file\n')
            p=root/'Documentation/a.rst';p.write_text('Title\n=====\n\n.. kernel-include:: sample.txt\n   :literal:\n')
            with patch('bulk.KERNEL_ROOT',root),patch('live_includes.ROOT',root):
                tree=bulk.parse(p)
                self.assertEqual(live_includes.records(tree)[0]['path'],'sample.txt')
                self.assertEqual(next(tree.findall(nodes.literal_block)).astext(),'root file\n')

    def test_code_include_keeps_file_text_and_language(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=root/'a.rst';(root/'sample.c').write_text('int x;\n')
            p.write_text('Title\n=====\n\n.. include:: sample.c\n   :code: c\n')
            with patch('bulk.KERNEL_ROOT',root),patch('live_includes.ROOT',root):
                tree=bulk.parse(p);writer=bulk.BulkWriter('a.rst',{'a.rst':{}},{},'commit',set(),{})
                body=writer.anchors(tree)+'\n'+writer.block(tree)
                bulk.verify_page(tree,body,writer)
                self.assertEqual(live_includes.records(tree)[0]['options']['language'],'c')

    def test_literalinclude_language_and_source_dependency(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=root/'a.rst';data=root/'sample.c';data.write_text('int x;\n')
            p.write_text('Title\n=====\n\n.. literalinclude:: sample.c\n   :language: c\n')
            with patch('bulk.KERNEL_ROOT',root),patch('live_includes.ROOT',root):
                tree=bulk.parse(p);r=live_includes.records(tree)[0]
                self.assertEqual(r['options']['language'],'c')
                self.assertIn(str(data),tree.settings.record_dependencies.list)


if __name__=='__main__':unittest.main()
