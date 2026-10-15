import json
from pathlib import Path
import tempfile
import unittest

from docutils import nodes
from markdown_it import MarkdownIt

from convert import KernelDoc, Writer, convert, parse
from verify import Visible


class ConversionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name)/'sample.rst'

    def render(self, text, labels=None):
        self.path.write_text(text)
        tree = parse(self.path)
        writer = Writer('sample.rst', {'sample.rst': {'reference':'kernel/sample'}}, labels or {}, 'baseline')
        return writer.block(tree)

    def test_nested_literal_keeps_code_and_diagram(self):
        text = 'Example\n=======\n\n* Keep this example::\n\n      if (a < b && p->ready) {\n          call("```", x_y);\n      }\n      |---+\n      |   |\n\n* Next item.\n'
        out = self.render(text)
        expected = next(parse(self.path).findall(nodes.literal_block)).astext()
        blocks = [t.content.removesuffix('\n') for t in MarkdownIt().parse(out) if t.type=='fence']
        self.assertEqual(blocks, [expected])
        self.assertIn('Next item.', out)

    def test_plugin_options_and_continuations(self):
        out = self.render('.. kernel-doc:: drivers/base/core.c\n   :export:\n   :functions: alpha \\\n               beta gamma\n')
        self.assertEqual(out, '```{kernel-doc} drivers/base/core.c\n:export:\n:functions: alpha beta gamma\n```')

    def test_empty_identifiers_preserved(self):
        self.assertIn(':identifiers:\n', self.render('.. kernel-doc:: x.h\n   :identifiers:\n'))

    def test_unknown_directive_and_option_fail(self):
        for source in ('.. mystery:: x\n', '.. kernel-doc:: x.h\n   :unknown: x\n', '.. kernel-doc:: x.h\n\n   unexpected body\n'):
            with self.subTest(source=source), self.assertRaises(ValueError):
                self.render(source)

    def test_unsupported_node_fails(self):
        with self.assertRaisesRegex(ValueError, 'unsupported'):
            self.render('.. image:: missing.svg\n')

    def test_c_roles_are_literals(self):
        self.assertEqual(self.render(':c:func:`foo` and :c:type:`thing`\n'), '`foo()` and `thing`')

    def test_reference_prefers_local_label(self):
        labels = {'sample.rst': {'shared': ('kernel/sample','here','Here')},
                  'other.rst': {'shared': ('kernel/other','there','There')}}
        self.assertEqual(self.render(':ref:`shared`\n',labels), '[Here](~kernel/sample#rst-here)')
        with self.assertRaises(ValueError):
            self.render(':ref:`missing`\n',labels)

    def test_markdown_escaping_preserves_visible_text(self):
        source = 'a_b foo\\_bar 0 < 1, *literal stars* and <not-html>.\n'
        out = self.render(source)
        visible = Visible(); visible.feed(MarkdownIt('commonmark',{'html':True}).render(out))
        self.assertEqual(''.join(visible.text).strip(), 'a_b foo_bar 0 < 1, literal stars and <not-html>.')

    def test_tables_keep_empty_cells_and_headerless_shape(self):
        out = self.render('===== =====\nA     B\nC\n===== =====\n')
        visible = Visible(); visible.feed(MarkdownIt('commonmark',{'html':True}).render(out))
        self.assertEqual(visible.counts['td'],4)
        self.assertEqual(visible.counts['th'],0)

    def test_existing_output_refused(self):
        plan = Path(self.tmp.name)/'plan.json'; plan.write_text('{}')
        with self.assertRaisesRegex(ValueError,'refusing to overwrite'):
            convert(Path(self.tmp.name), plan, Path(self.tmp.name))


if __name__ == '__main__':
    unittest.main()
