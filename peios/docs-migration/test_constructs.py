import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from docutils import nodes
import bulk
import constructs
import test_bulk


class ConstructTests(unittest.TestCase):
    def render(self,text,**kwargs):
        return test_bulk.BulkTests().render(text,**kwargs)

    def test_raw_accepts_only_reviewed_layout(self):
        body=self.render('Title\n=====\n\n.. raw:: latex\n\n   \\footnotesize\n\nKeep this prose.\n')
        self.assertIn('Keep this prose.',body)
        for fmt,text in [('latex',r'\textbf{important prose}'),('html','<p>important prose</p>')]:
            with self.assertRaisesRegex(ValueError,'raw content requires explicit review'):
                self.render('Title\n=====\n\n.. raw:: '+fmt+'\n\n   '+text+'\n')

    def test_conditions_select_only_known_web_branch(self):
        body=self.render("Title\n=====\n\n.. ifconfig:: builder != 'latex'\n\n   Web text.\n\n.. ifconfig:: builder == 'latex'\n\n   Print fallback.\n")
        self.assertIn('Web text.',body);self.assertNotIn('Print fallback.',body)
        with self.assertRaisesRegex(ValueError,'unreviewed web condition'):
            self.render('Title\n=====\n\n.. only:: unknown\n\n   Something.\n')

    def test_glossary_blank_line_and_term_reference(self):
        body=self.render('Title\n=====\n\n.. glossary::\n\n   Data Unit\n\n     A sample.\n\nSee :term:`Data Unit`.\n',labels={'guide/a.rst':{'data unit':('guide/a.rst','term-data-unit','Data Unit')}})
        self.assertIn('id="rst-term-data-unit"',body)
        self.assertIn('[Data Unit](<#rst-term-data-unit>)',body)

    def test_csv_dependencies_and_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=root/'a.rst';csv=root/'values.csv'
            csv.write_text('name,value\nalpha,12\n')
            p.write_text('Title\n=====\n\n.. csv-table::\n   :file: values.csv\n   :header-rows: 1\n')
            with patch('constructs.ROOT',root), patch('live_includes.ROOT',root):
                tree=bulk.parse(p)
                self.assertEqual(len(list(tree.findall(nodes.table))),1)
                self.assertIn(str(csv),tree.settings.record_dependencies.list)
                p.write_text(p.read_text().replace('values.csv','../outside.csv'))
                with self.assertRaisesRegex(ValueError,'CSV input missing or outside'):
                    bulk.parse(p)

    def test_code_caption_and_deferred_emphasis(self):
        body=self.render('Title\n=====\n\n.. code-block:: c\n   :caption: Example\n   :emphasize-lines: 1\n\n   int x;\n')
        self.assertIn('Example',body);self.assertIn('```c\nint x;\n```',body)
        with self.assertRaises(ValueError):
            self.render('Title\n=====\n\n.. code-block:: c\n')

    def test_nested_lines_and_options_survive(self):
        self.render('Title\n=====\n\n| 1. First\n|    Nested\n| 2. Second\n\n--help  Show help.\n')

    def test_c_anchor_kinds_and_function_pointer_typedef(self):
        cases=[('function','const struct item *lookup(int id)','c-lookup'),
               ('struct','item','c-struct-item'),('union','item','c-union-item'),
               ('enum','state','c-enum-state'),('macro','MAX(x, y)','c-MAX'),
               ('type','typedef void (*callback)(int)','c-callback'),('var','int count','c-count')]
        for kind,signature,anchor in cases:
            self.assertEqual(constructs.declaration_anchor(kind,signature),anchor)
        with self.assertRaises(ValueError):constructs.declaration_anchor('function','not a declaration')

    def test_namespace_and_noindex(self):
        body=self.render('Title\n=====\n\n.. c:namespace:: V4L\n\n.. c:function:: int open(int fd)\n\n.. c:macro:: OPEN\n   :noindex:\n')
        self.assertIn('id="c-open"',body);self.assertNotIn('id="c-OPEN"',body)

    def test_table_caption_reference_is_resolved(self):
        body=self.render('Title\n=====\n\n.. list-table:: See :ref:`other`\n\n   * - Value\n',labels={'guide/a.rst':{'other':('guide/b.rst','other','Other')}})
        self.assertIn('[Other]',body)


if __name__=='__main__':unittest.main()
