# SPDX-License-Identifier: GPL-2.0
"""
Markdown for a uAPI header's table of symbols: what Sphinx's
``kernel-include`` gives with ``:generate-cross-refs:`` and ``:toc:``.

The kernel's own ``kdoc.parse_data_structs.ParseDataStructs`` finds the
header's ioctls, macros, enumeration values, enums, structs and typedefs,
and the reference each should link to, as the header's exception file
adjusts them. A reference names an RST label (``:ref:``) or a C-domain
entry (``:c:type:``) on an authored page. Authored pages carry those as
anchors, ``rst-<label id>`` and ``c-<name>``, which the site's anchor
index finds.
"""

import re
import unicodedata

from kdoc_markdown import code
from trail_plugin import text

#: A reference as ParseDataStructs writes it: :ref:`SHOWN <target>`,
#: :c:type:`SHOWN <namespace.target>`, or a bare :ref:`target`.
REFERENCE = re.compile(r"(:ref|:c:\w+):`(?:[^`<]*?\s*<([^>`]+)>|([^`]+))`")


def make_id(name):
    """
    docutils' ``nodes.make_id``, which turns an RST label into the id its
    target gets, and so the migration into the anchor after ``rst-``.
    """
    value = unicodedata.normalize("NFKD", name.lower()).encode("ascii", "ignore").decode("ascii")
    value = re.sub("[^a-z0-9]+", "-", " ".join(value.split()))
    return re.sub(r"^[-0-9]+|-+$", "", value)


def candidates(role, target):
    """The anchors that may stand for a reference, in order of preference."""
    if role == ":ref":
        return ["rst-" + make_id(target)]
    # Anchors drop the C namespace ("V4L.v4l2_format" is c-v4l2_format).
    name = target.rsplit(".", 1)[-1]
    return [f"c-{name}"] + [f"c-{tag}-{name}" for tag in ("struct", "union", "enum")]


def toc(parser, path, find, here):
    """
    The header's symbols by kind, each linked where ``find(candidates)``
    locates its reference. Returns the Markdown and the symbols that
    linked nowhere.
    """
    out = []
    unresolved = []
    kinds = sorted((definition["description"], kind) for kind, definition in parser.DEF_SYMBOL_TYPES.items())
    for description, kind in kinds:
        entries = parser.symbols[kind]
        if not entries:
            continue
        out += [f"## {text(description)}", ""]
        for symbol, (reference, line) in sorted(entries.items()):
            shown = code(symbol)
            match = REFERENCE.search(reference)
            target = find(candidates(match.group(1), match.group(2) or match.group(3))) if match else None
            if target:
                page, anchor = target
                href = f"#{anchor}" if page == here else f"~{page}#{anchor}"
                shown = f"[{shown}]({href})"
            else:
                unresolved.append(symbol)
            # ParseDataStructs counts lines from 0.
            out.append(f"- {shown}: {code(path)}, line {line + 1}")
        out.append("")
    return "\n".join(out), unresolved
