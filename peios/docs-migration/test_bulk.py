import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
from docutils import nodes
from bulk import BulkWriter, parse, verify_page, layout


class BulkTests(unittest.TestCase):
    def render(self, text, other=None, labels=None):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'a.rst';p.write_text(text)
            tree=parse(p)
        targets={'guide/a.rst':{'reference':'kernel/guide/a'}}
        targets.update(other or {})
        writer=BulkWriter('guide/a.rst',targets,labels or {},'commit',{'guide/a.rst','guide/b.rst','other.rst'},{'guide/b.rst':'Other guide'})
        body=writer.anchors(tree)+'\n\n'+writer.block(tree)
        verify_page(tree,body,writer)
        return body

    def test_toctree_preserves_caption_and_external_destination(self):
        body=self.render('Title\n=====\n\n.. toctree::\n   :caption: Read next\n   :hidden:\n\n   b\n   Custom <../other>\n')
        self.assertIn('**Read next**',body)
        self.assertIn('[Other guide](<https://git.kernel.org/',body)
        self.assertIn('Documentation/other.rst?id=commit',body)

    def test_doc_link_normalizes_parent_and_absolute_source_paths(self):
        body=self.render('Title\n=====\n\n:doc:`../other` and :doc:`/other`\n',{'other.rst':{'reference':'kernel/other'}})
        self.assertEqual(body.count('<~kernel/other>'),2)

    def test_reference_uses_source_title_and_explicit_caption(self):
        labels={'guide/b.rst':{'example':('guide/b.rst','example','Other heading')}}
        body=self.render('Title\n=====\n\n:ref:`example` and :ref:`custom <example>`\n',{'guide/b.rst':{'reference':'kernel/guide/b'}},labels)
        self.assertIn('[Other heading](<~kernel/guide/b#rst-example>)',body)
        self.assertIn('[custom](<~kernel/guide/b#rst-example>)',body)

    def test_table_preserves_links_and_nested_literal_blocks(self):
        body=self.render('Title\n=====\n\n.. list-table:: Caption\n\n   * - `A <https://example.org/>`_\n     - Example::\n\n           x < y\n')
        self.assertIn('<caption>\n\nCaption\n\n</caption>',body)
        self.assertIn('[A](<https://example.org/>)',body)
        self.assertIn('x < y',body)

    def test_named_admonition_keeps_title(self):
        self.assertIn('**Watch out**',self.render('Title\n=====\n\n.. admonition:: Watch out\n\n   Important text.\n'))

    def test_unsupported_construct_cannot_be_silently_dropped(self):
        with self.assertRaises(ValueError):
            self.render('Title\n=====\n\n.. image:: a.svg\n')

    def test_c_declaration_keeps_signature_and_body(self):
        body=self.render('Title\n=====\n\n.. c:function:: int foo(int x)\n\n   Does something.\n')
        self.assertIn('```c\nint foo(int x)\n```',body)
        self.assertIn('Does something.',body)

    def test_lettered_and_empty_list_items_survive(self):
        body=self.render('Title\n=====\n\na) First\n\nb) Second\n\n*\n*\n')
        self.assertIn('**a)** First',body)
        self.assertEqual(body.count('empty source list item'),2)

    def test_escaped_source_text_is_checked_without_docutils_escape_markers(self):
        self.render('Title\n=====\n\nThe path is /dev/foo\\*.\n')

    def test_multiline_reference_and_case_normalization(self):
        labels={'guide/b.rst':{'example':('guide/b.rst','example','Other heading')}}
        body=self.render('Title\n=====\n\n:ref:`some\nwords<EXAMPLE>`\n',{'guide/b.rst':{'reference':'kernel/guide/b'}},labels)
        self.assertIn('[some words](<~kernel/guide/b#rst-example>)',body)

    def test_label_on_paragraph_keeps_its_anchor(self):
        body=self.render('Title\n=====\n\n.. _label:\n\nParagraph.\n')
        self.assertIn('id="rst-label"',body)

    def test_wrapped_prose_does_not_become_a_markdown_list(self):
        self.render('Title\n=====\n\nFirst line\n- wrapped prose.\n')

    def test_unknown_bare_filename_stays_plain_text(self):
        body=self.render('Title\n=====\n\nSee irq-affinity.rst.\n')
        self.assertIn('See irq-affinity.rst.',body)
        self.assertNotIn('git.kernel.org',body)

    def test_footnote_reference_and_target_aliases_survive(self):
        body=self.render('Title\n=====\n\nText [1]_.\n\n.. [1] Footnote.\n')
        self.assertIn('id="rst-footnote-reference-1"',body)
        self.assertIn('id="rst-footnote-1"',body)

    def test_verifier_rejects_missing_prose(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'a.rst';p.write_text('Title\n=====\n\nKeep this.\n')
            tree=parse(p)
        writer=BulkWriter('guide/a.rst',{'guide/a.rst':{}},{},'commit',set(),{})
        with self.assertRaisesRegex(ValueError,'prose preservation'):
            verify_page(tree,'<a id="rst-title"></a>\n',writer)

    def test_c_identifiers_do_not_turn_into_emphasis(self):
        self.render('Title\n=====\n\n__attribute__((packed)) and __CHECKER__ remain identifiers.\n')

    def test_literal_paragraphs_do_not_become_lists_or_rules(self):
        for text in ['1) Metadata zones: details.','1. Numbered prose.','5595. A device identifier.','---','-']:
            writer=BulkWriter('guide/a.rst',{'guide/a.rst':{}}, {},'commit',set(),{})
            tree=nodes.document('',None);tree+=nodes.paragraph('',text)
            body=writer.block(tree)
            verify_page(tree,body,writer)

    def test_adjacent_literals_keep_their_text(self):
        self.render('Title\n=====\n\n:c:type:`v4l2_fh`\\ ``.subscribed`` stays adjacent.\n')

    def test_inline_target_keeps_its_words_and_destination(self):
        body=self.render('Title\n=====\n\n_`Preferred licenses`: see `Preferred licenses`_.\n')
        self.assertIn('id="rst-preferred-licenses"',body)

    def test_emphasis_at_word_boundary_keeps_the_suffix(self):
        self.render('Title\n=====\n\nThese *ioctl()*\\s remain plural.\n')

    def test_title_footnote_remains_linked(self):
        body=self.render('Title [1]_\n==========\n\nBody.\n\n.. [1] Name history.\n')
        self.assertIn('id="rst-footnote-reference-1"',body)
        self.assertIn('](#rst-footnote-1)',body)

    def test_double_digit_list_can_start_with_code(self):
        self.render('Title\n=====\n\n10. ::\n\n       hello()\n\n11. ::\n\n       next()\n')

    def test_indenting_a_literal_preserves_form_feeds(self):
        writer=BulkWriter('guide/a.rst',{'guide/a.rst':{}}, {},'commit',set(),{})
        tree=nodes.document('',None);block=nodes.block_quote()
        block+=nodes.literal_block('','page one\n\f\npage two\n')
        tree+=block
        verify_page(tree,writer.block(tree),writer)

    def test_file_reference_links_to_existing_pinned_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'samples').mkdir();(root/'samples/example.c').write_text('int x;\n')
            with patch('bulk.KERNEL_ROOT',root):
                body=self.render('Title\n=====\n\nSee <file:samples/example.c>.\n')
                self.assertIn('/tree/samples/example.c?id=commit',body)
                with self.assertRaisesRegex(ValueError,'missing file reference'):
                    self.render('Title\n=====\n\nSee <file:samples/missing.c>.\n')


if __name__=='__main__':unittest.main()
