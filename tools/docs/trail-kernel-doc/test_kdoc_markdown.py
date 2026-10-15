# SPDX-License-Identifier: GPL-2.0
"""
Tests for kdoc_markdown's reStructuredText-to-Markdown conversion.

kdoc_markdown imports the kernel's kdoc package, so point KERNEL_SRCTREE
at a kernel tree (default: ../kernel beside this directory):

    KERNEL_SRCTREE=/path/to/kernel python3 -m unittest test_kdoc_markdown
"""

import os
import sys
import unittest

HERE = os.path.dirname(os.path.realpath(__file__))
SRCTREE = os.environ.get("KERNEL_SRCTREE", os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(SRCTREE, "tools", "lib", "python"))
sys.path.insert(1, HERE)

import kdoc_markdown as km  # noqa: E402


def resolved(text, symbols=None, page="kernel/here"):
    return km.resolve_refs(km.convert(text), symbols or {}, page)


class Inline(unittest.TestCase):
    def test_kernel_doc_highlights(self):
        self.assertEqual(
            resolved("Call foo() on @dev with %GFP_KERNEL and &struct bar."),
            "Call `foo()` on **dev** with `GFP_KERNEL` and `struct bar`.",
        )

    def test_references_link_to_documented_symbols(self):
        symbols = {
            ("ident", "foo"): ("kernel/here", "c-foo"),
            ("struct", "bar"): ("kernel/there", "c-struct-bar"),
        }
        self.assertEqual(
            resolved("foo() and &struct bar and &bar", symbols),
            "[`foo()`](#c-foo) and [`struct bar`](~kernel/there#c-struct-bar)"
            " and [`bar`](~kernel/there#c-struct-bar)",
        )

    def test_roles(self):
        symbols = {("ident", "foo"): ("kernel/here", "c-foo")}
        self.assertEqual(
            resolved(":c:func:`foo` and :ref:`the guide <guide>` and :file:`a/b`", symbols),
            "[`foo()`](#c-foo) and the guide and `a/b`",
        )

    def test_brackets_and_angles_stay_text(self):
        self.assertEqual(
            resolved("disable_work[_sync]() includes <linux/x.h>"),
            "disable\\_work\\[\\_sync\\]() includes \\<linux/x.h>".replace("\\_", "_"),
        )

    def test_a_bang_before_a_link_does_not_make_an_image(self):
        symbols = {("ident", "f"): ("kernel/here", "c-f")}
        self.assertEqual(resolved("if !f() then", symbols), "if \\![`f()`](#c-f) then")

    def test_relative_hyperlinks_keep_only_their_words(self):
        self.assertEqual(
            resolved("see `KASAN <kasan.html>`_ or `site <https://x.org>`_"),
            "see KASAN or [site](https://x.org)",
        )

    def test_email_addresses_are_not_parameters(self):
        self.assertEqual(resolved("mail me@example.com"), "mail me@example.com")


class Blocks(unittest.TestCase):
    def test_literal_blocks_become_fences(self):
        self.assertEqual(
            resolved("Example::\n\n    int x;\n    x++;\n\nAfter."),
            "Example:\n\n```text\nint x;\nx++;\n```\n\nAfter.",
        )

    def test_code_block_directives_keep_their_language(self):
        self.assertEqual(
            resolved(".. code-block:: c\n\n    int x;\n"),
            "```c\nint x;\n```",
        )

    def test_admonitions(self):
        self.assertEqual(
            resolved(".. note::\n\n   Careful with foo.\n"),
            "> [!NOTE]\n> Careful with foo.",
        )

    def test_admonition_text_can_start_on_the_directive_line(self):
        self.assertEqual(
            resolved(".. note:: When reading this,\n          look first.\n\n.. note:: One.\n\n   Two.\n"),
            "> [!NOTE]\n> When reading this,\n> look first.\n\n> [!NOTE]\n> One.\n>\n> Two.",
        )

    def test_sibling_items_of_a_deeply_indented_list_stay_siblings(self):
        self.assertEqual(
            resolved("- outer:\n\n      - one\n      - two\n        wraps\n\n- next\n\nAfter."),
            "- outer:\n\n  - one\n  - two\n    wraps\n\n- next\n\nAfter.",
        )

    def test_section_underlines_become_bold_titles(self):
        self.assertEqual(
            resolved("Intro.\n\nExample\n~~~~~~~\n\nText."),
            "Intro.\n\n**Example**\n\nText.",
        )

    def test_definition_lists_become_term_lists(self):
        self.assertEqual(
            resolved("**Flags**\n\n%ONE\n    Does one.\n\n%TWO:\n    Does two,\n    over two lines.\n\nAfter."),
            "**Flags**\n\n- `ONE`:\n  Does one.\n\n- `TWO`:\n  Does two,\n  over two lines.\n\nAfter.",
        )

    def test_wrapped_prose_definitions_keep_their_words(self):
        self.assertEqual(
            resolved("Claims the lock to serialize\n    first-time initialization."),
            "- Claims the lock to serialize\n\n  first-time initialization.",
        )

    def test_fence_like_lines_are_escaped(self):
        self.assertEqual(resolved("a\n\n~~~~\n\nb"), "a\n\n\\~~~~\n\nb")

    def test_indentation_survives_only_inside_lists(self):
        self.assertEqual(
            resolved("- one\n  more\n\n      indented para\n\nback"),
            "- one\n  more\n\n  indented para\n\nback",
        )
        self.assertEqual(resolved("para\n\n        quoted"), "para\n\nquoted")


class Directives(unittest.TestCase):
    def setUp(self):
        self.style = km.MarkdownFormat()
        self.style.begin("kernel/here")

    def test_c_macro_is_an_anchored_symbol(self):
        text = ".. c:macro:: FLAG_WAIT\n\n   Wait for it.\n\n.. c:macro:: FLAG_SIGNAL\n\nUnindented description."
        self.assertEqual(
            km.convert(text, self.style),
            '#### <a id="c-FLAG_WAIT"></a>`FLAG_WAIT`\n\nWait for it.\n\n'
            '#### <a id="c-FLAG_SIGNAL"></a>`FLAG_SIGNAL`\n\nUnindented description.',
        )
        self.assertEqual(self.style.symbols[("ident", "FLAG_WAIT")], ("kernel/here", "c-FLAG_WAIT"))

    def test_c_function_shows_its_signature(self):
        self.assertEqual(
            km.convert(".. c:function:: int foo(int x)\n\n   Does foo.", self.style),
            '#### <a id="c-foo"></a>`foo()`\n\n```c\nint foo(int x)\n```\n\nDoes foo.',
        )

    def test_flat_table_cells_are_markdown_in_html(self):
        text = (
            ".. flat-table:: Caption\n   :widths: 1 5\n   :stub-columns: 1\n\n"
            "   * - %ONE\n     - First line\n       continues.\n\n       Second para.\n\n"
            "   * - TWO\n     -\n"
        )
        self.assertEqual(
            km.convert(text, self.style),
            "<table>\n<caption>Caption</caption>\n<tbody>\n<tr>\n"
            '<th scope="row">\n\n`ONE`\n\n</th>\n<td>\n\nFirst line\ncontinues.\n\nSecond para.\n\n</td>\n'
            '</tr>\n<tr>\n<th scope="row">\n\nTWO\n\n</th>\n<td></td>\n</tr>\n</tbody>\n</table>',
        )

    def test_flat_table_headers_spans_and_short_rows(self):
        text = (
            ".. flat-table::\n   :header-rows: 1\n\n"
            "   * - A\n     - B\n     - C\n"
            "   * - :rspan:`1` tall\n     - :cspan:`1` wide\n"
            "   * - x\n"
            "   * - short\n"
        )
        html = km.convert(text, self.style)
        self.assertIn("<thead>\n<tr>\n<th>\n\nA\n\n</th>", html)
        self.assertIn('<td rowspan="2">\n\ntall', html)
        self.assertIn('<td colspan="2">\n\nwide', html)
        # "x" sits beside the row-spanning cell, so it is short by one
        # column and spans it; "short" spans all three.
        self.assertIn('<td colspan="2">\n\nx\n\n</td>', html)
        self.assertIn('<td colspan="3">\n\nshort', html)

    def test_flat_tables_nest(self):
        text = (
            ".. flat-table::\n\n"
            "   * - outer\n     - Text.\n\n       .. flat-table::\n\n          * - inner\n"
        )
        html = km.convert(text, self.style)
        self.assertEqual(html.count("<table>"), 2)
        self.assertIn("<td>\n\ninner\n\n</td>", html)

    def test_nested_kernel_doc_goes_to_the_expander(self):
        calls = []
        self.style.expand_kernel_doc = lambda argument, options: calls.append((argument, options)) or "EXPANDED"
        out = km.convert("Errors.\n\n.. kernel-doc:: include/x.h\n    :identifiers: a b\n", self.style)
        self.assertEqual(calls, [("include/x.h", {"identifiers": "a b"})])
        self.assertEqual(out, "Errors.\n\nEXPANDED")

    def test_kernel_figures_use_reviewed_renderer(self):
        self.style.expand_kernel_figure = lambda argument, options, body: ("```mermaid\nflowchart TB\n  a --> b\n```", "\n".join(body))
        out = km.convert(".. kernel-figure:: x/f.dot\n\n   Caption.", self.style)
        self.assertIn("```mermaid", out)
        self.assertIn("Caption.", out)

    def test_kernel_figures_without_renderer_fail(self):
        with self.assertRaisesRegex(ValueError, "reviewed Mermaid"):
            km.convert(".. kernel-figure:: x/g.dot\n\n   Caption.", self.style)


if __name__ == "__main__":
    unittest.main()
