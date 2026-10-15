# SPDX-License-Identifier: GPL-2.0
"""
Tests for include_markdown, which needs nothing from the kernel tree:

    python3 -m unittest test_include_markdown
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

import include_markdown as im  # noqa: E402

TEXT = "zero\none\ntwo: start here\nthree\nfour\n"


class Ranges(unittest.TestCase):
    def test_line_slices_are_zero_based_and_end_exclusive(self):
        self.assertEqual(im.select(TEXT, 1, 3), "one\ntwo: start here")
        self.assertEqual(im.select(TEXT, end_line=-2), "zero\none\ntwo: start here")

    def test_text_markers_cut_inside_lines(self):
        self.assertEqual(im.select(TEXT, start_after="start here", end_before="four"), "\nthree\n")
        self.assertEqual(im.select(TEXT, start_after="two:"), " start here\nthree\nfour\n")

    def test_lines_are_sliced_before_markers_are_found(self):
        with self.assertRaises(im.RangeError):
            im.select(TEXT, 3, None, start_after="start here")

    def test_missing_markers_are_errors(self):
        with self.assertRaises(im.RangeError):
            im.select(TEXT, end_before="nowhere")


class Fences(unittest.TestCase):
    def test_text_is_kept_verbatim(self):
        self.assertEqual(im.fence("c", "\tint x;\n\n  y\f\n"), "```c\n\tint x;\n\n  y\f\n\n```")

    def test_boundary_newlines_are_preserved(self):
        self.assertEqual(im.fence("text", "\nthree\n\n"), "```text\n\nthree\n\n\n```")

    def test_fences_outgrow_backtick_runs(self):
        self.assertEqual(im.fence("text", "a\n````\nb"), "`````text\na\n````\nb\n`````")


class Tables(unittest.TestCase):
    def test_one_header_row_makes_a_markdown_table(self):
        text = 'Name, Mask\nINFO, 0x1\n"a, b",\n\nRadeon R* | V1*/R1* <x>\n'
        self.assertEqual(
            im.csv_table(text, 1),
            "| Name | Mask |\n|---|---|\n| INFO | 0x1 |\n| a, b |  |\n"
            "| Radeon R\\* \\| V1\\*/R1\\* \\<x\\> |  |",
        )

    def test_other_header_counts_make_html_tables(self):
        self.assertEqual(
            im.csv_table("a,b\n1,<2>\n", 0),
            "<table>\n<tbody>\n<tr><td>a</td><td>b</td></tr>\n<tr><td>1</td><td>&lt;2&gt;</td></tr>\n</tbody>\n</table>",
        )
        self.assertIn("<thead>\n<tr><th>a</th>", im.csv_table("a\nb\nc\n", 2))

    def test_impossible_header_counts_are_errors(self):
        with self.assertRaises(ValueError):
            im.csv_table("a\n", 2)


if __name__ == "__main__":
    unittest.main()
