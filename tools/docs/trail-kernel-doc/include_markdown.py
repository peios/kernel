# SPDX-License-Identifier: GPL-2.0
"""
Markdown for files included whole: a code block of the file's text, or a
table of a CSV file's rows. ``trail-kernel-include`` reads the files and
calls these.
"""

import csv
import html
import io
import re


class RangeError(ValueError):
    """A range option that selects nothing."""


def select(text, start_line=None, end_line=None, start_after=None, end_before=None):
    """
    The part of ``text`` that docutils' include options select. The line
    slice comes first (0-based, end exclusive, as Python slices are),
    then the text after the first ``start_after``, then the text before
    the first ``end_before`` in what remains.
    """
    if start_line or end_line is not None:
        text = "\n".join(text.splitlines()[start_line:end_line])
    if start_after is not None:
        at = text.find(start_after)
        if at < 0:
            raise RangeError(f":start-after: text {start_after!r} is not in the file")
        text = text[at + len(start_after):]
    if end_before is not None:
        at = text.find(end_before)
        if at < 0:
            raise RangeError(f":end-before: text {end_before!r} is not in the file")
        text = text[:at]
    return text


def fence(language, text):
    """
    A fenced code block holding ``text`` verbatim, including blank lines.
    The final delimiter newline is distinct from any newline in the file.
    """
    lines = text.split("\n")
    run = max((len(r) for line in lines for r in re.findall(r"`{3,}", line)), default=2)
    marker = "`" * (run + 1)
    return "\n".join([f"{marker}{language}", *lines, marker])


#: ASCII punctuation that could start Markdown (or Trail) syntax inside a
#: table cell. CommonMark lets any ASCII punctuation be backslash-escaped.
CELL_SPECIALS = re.compile(r"([\\`*_\[\]<>|~!&#$])")


def cell(text):
    """A CSV cell as Markdown inline text: plain text, nothing interpreted."""
    return CELL_SPECIALS.sub(r"\\\1", " ".join(text.split()))


def rows(text):
    """
    A CSV file's rows, read as docutils' csv-table reads them: spaces after
    a delimiter are skipped, and blank lines are not rows. Short rows are
    padded to the widest.
    """
    table = [[c.strip() for c in row] for row in csv.reader(io.StringIO(text), skipinitialspace=True) if row]
    width = max((len(row) for row in table), default=0)
    return [row + [""] * (width - len(row)) for row in table]


def csv_table(text, header_rows=0):
    """
    A CSV file as a table. One header row makes a Markdown table, which
    reads well in the page's Markdown mirror; any other number makes an
    HTML table, since a Markdown table has exactly one header row.
    """
    table = rows(text)
    if not table:
        raise ValueError("the CSV file has no rows")
    if header_rows > len(table):
        raise ValueError(f":header-rows: is {header_rows}, but the file has {len(table)} rows")
    if header_rows == 1:
        lines = ["| " + " | ".join(cell(c) for c in table[0]) + " |"]
        lines.append("|" + "---|" * len(table[0]))
        lines.extend("| " + " | ".join(cell(c) for c in row) + " |" for row in table[1:])
        return "\n".join(lines)

    def html_rows(section, tag):
        return [
            "<tr>" + "".join(f"<{tag}>{html.escape(c, quote=False)}</{tag}>" for c in row) + "</tr>"
            for row in section
        ]

    out = ["<table>"]
    if header_rows:
        out += ["<thead>", *html_rows(table[:header_rows], "th"), "</thead>"]
    out += ["<tbody>", *html_rows(table[header_rows:], "td"), "</tbody>", "</table>"]
    return "\n".join(out)
