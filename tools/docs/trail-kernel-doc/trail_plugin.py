# SPDX-License-Identifier: GPL-2.0
"""
The Trail plugin protocol, shared by the plugins in this directory.

Trail runs a plugin once per build. It writes a JSON request to the
plugin's stdin holding every block on the site that names the plugin,
and reads a JSON response from its stdout: the Markdown (or an error)
for each block, and the files that output was made from.
"""

import json
import re
import sys

PROTOCOL = 1

#: ASCII punctuation that could start Markdown (or Trail) syntax in a line
#: of text. CommonMark lets any ASCII punctuation be backslash-escaped.
SPECIALS = re.compile(r"([\\`*_\[\]<>|~!&#$])")


def text(value):
    """Plain text as Markdown inline content, nothing in it interpreted."""
    return SPECIALS.sub(r"\\\1", " ".join(value.split()))


def markdown_table(header, rows, escape=True):
    """
    A Markdown table. Cells are plain text unless ``escape`` is false, in
    which case they are Markdown already (and must not contain a "|").
    """
    cell = text if escape else (lambda value: value)
    lines = ["| " + " | ".join(cell(c) for c in header) + " |", "|" + "---|" * len(header)]
    lines.extend("| " + " | ".join(cell(c) for c in row) + " |" for row in rows)
    return "\n".join(lines)


def slug(value):
    """An anchor-safe form of ``value``: runs of other characters become "-"."""
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-")


class BlockError(Exception):
    """A problem with one block, reported against it by Trail."""


def fail(plugin, message):
    """Give up on the whole request."""
    print(f"{plugin}: {message}", file=sys.stderr)
    sys.exit(1)


def read_request(plugin):
    try:
        request = json.load(sys.stdin)
    except json.JSONDecodeError as error:
        fail(plugin, f"the request is not JSON: {error}")
    if request.get("protocol") != PROTOCOL:
        fail(plugin, f"speaks Trail plugin protocol {PROTOCOL}, not {request.get('protocol')}")
    return request


class AnchorIndex:
    """
    The anchors authored pages define, which Trail sends to plugins
    configured with ``anchors = true``: each page's ids written in raw HTML
    (``<a id="c-v4l2_format">``), before any plugin's output is added.
    """

    def __init__(self, anchors):
        #: Anchor -> the pages defining it.
        self.pages = {}
        for page, ids in (anchors or {}).items():
            for anchor in ids:
                self.pages.setdefault(anchor, []).append(page)

    def find(self, candidates, near):
        """
        The (page, anchor) of the first of ``candidates`` that some page
        defines. Where several pages define it, the one nearest ``near``
        in the site wins: C namespaces don't survive into anchors, and
        the namespace a reference means is usually its own neighbourhood's.
        """
        here = near.split("/")
        for anchor in candidates:
            pages = self.pages.get(anchor)
            if pages:

                def shared(page):
                    count = 0
                    for a, b in zip(page.split("/"), here):
                        if a != b:
                            break
                        count += 1
                    return count

                return min(pages, key=lambda page: (-shared(page), page)), anchor
        return None


def block_options(block, known, hints=None):
    """
    A block's options, with names lower-cased as docutils matches them.
    An option outside ``known`` fails the block, with its ``hints``
    entry, if any, saying what to write instead.
    """
    options = {name.lower(): value for name, value in block["options"].items()}
    hints = hints or {}
    for name in sorted(options):
        if name in hints:
            raise BlockError(f":{name}: {hints[name]}")
    unknown = sorted(set(options) - set(known))
    if unknown:
        raise BlockError(
            "unknown option(s) " + ", ".join(f":{o}:" for o in unknown)
            + " (expected " + ", ".join(f":{o}:" for o in known) + ")"
        )
    return options


def respond(blocks, depends_on):
    """
    Write the response: ``blocks`` maps each block to its Markdown or
    its BlockError.
    """
    out = []
    for block, result in blocks:
        if isinstance(result, Exception):
            out.append({"id": block["id"], "error": str(result)})
        else:
            out.append({"id": block["id"], "markdown": result.strip("\n") + "\n"})
    json.dump({"blocks": out, "depends_on": sorted(set(depends_on))}, sys.stdout)
