# SPDX-License-Identifier: GPL-2.0
"""
Markdown output for the kernel's kernel-doc parser, written for Trail.

``MarkdownFormat`` is a sibling of ``RestFormat`` in
``tools/lib/python/kdoc/kdoc_output.py``: the same parser feeds it, the
same filters decide what is output, and it renders each declaration as
Markdown instead of reStructuredText.

kernel-doc comments are written in a reStructuredText dialect, so their
text passes through ``convert()``, which handles the subset that appears
in practice: kernel-doc's own highlights (``func()``, ``&struct foo``,
``@param``, ``%CONST``), inline literals and roles, literal and
code-block blocks, admonitions, simple lists, section underlines, and
kernel-figure diagrams that have a Mermaid drawing. Anything else is kept
visible as preformatted text rather than dropped.

Cross-references come out as placeholders (see ``ref()``) because the
symbol they name may be documented by a block rendered later; the plugin
resolves them once every block has rendered.
"""

import re
import sys
import textwrap

from kdoc.kdoc_output import OutputFormat, function_pointer
from kdoc.kdoc_parser import KernelDoc

# --------------------------------------------------------------------------
# Symbols, anchors and cross-reference placeholders
# --------------------------------------------------------------------------

#: Namespaces a symbol can live in. "ident" is C's ordinary identifier
#: namespace (functions, macros, variables, typedefs); tagged types each
#: have their own, as in C, so ``struct stat`` and ``stat()`` can coexist.
KINDS = ("ident", "struct", "union", "enum")

REF_RE = re.compile("\x00([^\x01]*)\x01([^\x01]*)\x01([^\x02]*)\x02")


def anchor(kind, name):
    """The fragment id a documented symbol is given on its page."""
    return f"c-{name}" if kind == "ident" else f"c-{kind}-{name}"


def ref(kind, name, text):
    """
    A cross-reference placeholder: ``text`` (already Markdown) linking to
    symbol ``name``. ``kind`` is one of ``KINDS``, or "type" for a
    reference that may name any type (``&foo``), tried as a typedef, then
    struct, union and enum.
    """
    return f"\x00{kind}\x01{name}\x01{text}\x02"


def resolve_refs(markdown, symbols, reference, fallback=None):
    """
    Replace placeholders with links to wherever each symbol is documented,
    or leave their text unlinked. ``symbols`` maps (kind, name) to
    (page reference, anchor); ``reference`` is the page being rendered,
    whose own symbols get plain fragment links. An empty anchor links to
    the page as a whole. A symbol ``symbols`` lacks is looked up with
    ``fallback(kind, name)``, if given, which returns a target or None.
    """

    def link(match):
        kind, name, text = match.groups()
        kinds = ("ident",) + KINDS[1:] if kind == "type" else (kind,)
        targets = [symbols.get((candidate, name)) for candidate in kinds]
        if fallback:
            targets.append(fallback(kind, name))
        for target in targets:
            if target:
                page, fragment = target
                if not fragment:
                    # The page itself: no link from it to itself.
                    return text if page == reference else f"[{text}](~{page})"
                href = f"#{fragment}" if page == reference else f"~{page}#{fragment}"
                return f"[{text}]({href})"
        return text

    return REF_RE.sub(link, markdown)


def authored_anchors(kind, name):
    """
    The anchors an authored page may give a type that kernel-doc did not
    document. The kernel docs' migration (PEI-1505) writes
    ``.. c:type:: x`` as ``c-x`` and ``.. c:struct:: x`` as ``c-struct-x``,
    the scheme of ``anchor()``; Sphinx's ``c:type`` covers structs, unions
    and enums too.

    Functions, macros and variables are left alone. The anchors drop the
    C namespace a declaration sat in, and the authored ones are mostly the
    media uAPI's per-device read(), open() and poll(), which namespaces
    keep apart from every other read() in Sphinx. Type names are
    distinctive (v4l2_buffer), and a struct is the same struct wherever it
    is mentioned.
    """
    if kind == "ident":
        return []
    if kind == "type":
        # A bare &name may be a malformed parameter reference (e.g. &start).
        # The untyped c-NAME anchor could be a function; only tagged anchors
        # prove a type here. Explicit &struct/union/enum references still use
        # the legacy c-NAME spelling below, as media's c:type declarations do.
        return [f"c-{tag}-{name}" for tag in KINDS[1:]]
    return [f"c-{kind}-{name}", f"c-{name}"]


def code(text):
    """An inline code span holding ``text`` verbatim."""
    text = " ".join(text.split("\n"))
    run = max((len(r) for r in re.findall(r"`+", text)), default=0)
    fence = "`" * (run + 1)
    pad = " " if text.startswith("`") or text.endswith("`") or run else ""
    return f"{fence}{pad}{text}{pad}{fence}"


def fence(language, lines):
    """A fenced code block, long enough to hold any backtick run inside."""
    run = max((len(r) for line in lines for r in re.findall(r"`{3,}", line)), default=2)
    marker = "`" * (run + 1)
    return [f"{marker}{language}", *lines, marker, ""]


# --------------------------------------------------------------------------
# reStructuredText (kernel-doc dialect) to Markdown
# --------------------------------------------------------------------------

#: Admonition directives, mapped to Trail's five admonition kinds.
ADMONITIONS = {
    "admonition": "NOTE",
    "note": "NOTE",
    "seealso": "NOTE",
    "hint": "TIP",
    "tip": "TIP",
    "important": "IMPORTANT",
    "attention": "IMPORTANT",
    "warning": "WARNING",
    "caution": "CAUTION",
    "danger": "CAUTION",
    "error": "CAUTION",
}

CODE_DIRECTIVES = ("code-block", "code", "sourcecode")

DIRECTIVE = re.compile(r"^\.\.\s+([\w:-]+)::(?:\s+(.*))?$")
EXPLICIT_MARKUP = re.compile(r"^\.\.(\s|$)")
LITERAL_INTRO = re.compile(r"^[^.].*::$")
TABLE_BORDER = re.compile(r"^(\+[-=+]+\+|=+(\s+=+)+)$")
UNDERLINE = re.compile(r"^([=\-~^\"'`#*+])\1{2,}$")
LIST_MARKER = re.compile(r"^([-*+]|\d+[.)]|#\.)(\s+|$)")
#: A definition-list term that names something: one word, or one bold or
#: literal span.
SIMPLE_TERM = re.compile(r"^(\S+|\*\*[^*]+\*\*|``[^`]+``)$")
BLOCK_START = re.compile(r"^(```|~~~|>|<div|\*\*|([-*+]|\d+[.)])(\s|$))")

INLINE = re.compile(
    r"""
      (?P<literal>``(?P<lit>(?s:.+?))``)
    | (?P<role>:(?P<rname>[\w:+.-]+):`(?P<rtext>[^`]+)`)
    | (?P<hyperlink>`(?P<htext>[^`<]*?)\s*<(?P<hurl>[^>`]+)>`__?)
    | (?P<interpreted>`(?P<itext>[^`]+)`(?:__?)?)
    | (?P<memberfunc>&(?P<mft>\w+)(?P<mfop>\.|->)(?P<mfm>\w+)\(\))
    | (?P<member>&(?P<mt>\w+)(?P<mop>\.|->)(?P<mm>\w+))
    | (?P<tagged>&(?P<tag>enum|struct|union|typedef)\s*(?P<tname>\w+))
    | (?P<amp>&(?P<aname>\w+))
    | (?P<fpparam>@(?P<fp>\w+(?:->\S+?)?)\(\))
    | (?P<func>\b(?P<fname>\w+)\(\))
    | (?P<const>%(?P<cname>[-_*\w]+))
    | (?P<param>(?<!\w)(?P<pp>[!~*]?)@(?P<pname>\w+(?:(?:\.\w+)|(?:->\w+))*(?:\.\.\.)?))
    """,
    re.X,
)

ROLE_KINDS = {
    "c:func": "ident",
    "c:macro": "ident",
    "c:data": "ident",
    "c:var": "ident",
    "c:type": "type",
    "c:struct": "struct",
    "c:union": "union",
    "c:enum": "enum",
}

CODE_ROLES = {"file", "envvar", "kbd", "command", "program", "manpage", "samp", "c:expr", "c:texpr", "c:member", "c:enumerator"}


def warn(message):
    print(f"trail-kernel-doc: {message}", file=sys.stderr)


def escape(text):
    """
    Escape what Markdown would read as markup but reStructuredText as
    text: raw HTML, and brackets ("disable_work[_sync]()" is a link).
    """
    return text.replace("<", "\\<").replace("[", "\\[").replace("]", "\\]")


def is_url(target):
    return re.match(r"^([a-z][a-z0-9+.-]*://|mailto:)", target, re.I) is not None


#: Inline forms that only kernel-doc comments give meaning to. In plain
#: reStructuredText (``context.highlights`` false) they are text.
KERNEL_DOC_ONLY = ("memberfunc", "member", "tagged", "amp", "fpparam", "const", "param")


def inline(text, context=None):
    """
    Convert one paragraph's inline markup. A ``context`` may turn off
    kernel-doc's highlights (``highlights``), and may link words in plain
    text (``autolink``, which takes text and returns Markdown).
    """
    highlights = getattr(context, "highlights", True)
    plain = getattr(context, "autolink", None) or escape

    def convert_match(m):
        if not highlights and any(m.group(g) for g in KERNEL_DOC_ONLY):
            return plain(m.group(0))
        if m.group("literal"):
            return code(m.group("lit"))
        if m.group("role"):
            return role(m.group("rname"), m.group("rtext"))
        if m.group("hyperlink"):
            label = m.group("htext") or m.group("hurl")
            # A relative target ("kasan.html") names a Sphinx output page,
            # which has no counterpart here: keep the words, drop the link.
            if not is_url(m.group("hurl")):
                return escape(label)
            return f"[{escape(label)}]({m.group('hurl')})"
        if m.group("interpreted"):
            return code(m.group("itext"))
        if m.group("memberfunc"):
            t, op, member = m.group("mft"), m.group("mfop"), m.group("mfm")
            return ref("type", t, code(f"{t}{op}{member}()"))
        if m.group("member"):
            t, op, member = m.group("mt"), m.group("mop"), m.group("mm")
            return ref("type", t, code(f"{t}{op}{member}"))
        if m.group("tagged"):
            tag, name = m.group("tag"), m.group("tname")
            kind = "ident" if tag == "typedef" else tag
            return ref(kind, name, code(f"{tag} {name}"))
        if m.group("amp"):
            return ref("type", m.group("aname"), code(m.group("aname")))
        if m.group("fpparam"):
            return f"**{m.group('fp')}()**"
        if m.group("func"):
            return ref("ident", m.group("fname"), code(m.group("fname") + "()"))
        if m.group("const"):
            return code(m.group("cname"))
        if m.group("param"):
            prefix = m.group("pp")
            prefix = "\\" + prefix if prefix in ("*", "~") else prefix
            return f"**{prefix}{m.group('pname')}**"
        return m.group(0)

    out = []
    last = 0
    for m in INLINE.finditer(text):
        out.append(plain(text[last : m.start()]))
        out.append(convert_match(m))
        last = m.end()
    out.append(plain(text[last:]))
    # "!" before what may become a link would make it an image.
    return re.sub(r"!(?=\x00)", r"\\!", "".join(out))


def role(name, text):
    """An interpreted-text role such as :c:func:`foo` or :ref:`label`."""
    target_match = re.match(r"(?s)(.*?)\s*<([^>]+)>$", text)
    label, target = (target_match.group(1), target_match.group(2)) if target_match else (text, text)
    label = label or target
    if name in ROLE_KINDS:
        symbol = re.sub(r"\(\)$", "", target.strip()).split()[-1]
        display = label.strip()
        if name == "c:func" and not display.endswith(")") and not target_match:
            display += "()"
        return ref(ROLE_KINDS[name], symbol, code(display))
    if name in CODE_ROLES:
        return code(label)
    # :ref:, :doc: and anything else: the text the reader would see.
    return escape(label)


def indented_block(lines, start, indent):
    """
    The block of lines after ``start`` indented deeper than ``indent``
    (blank lines included), dedented, with the index just past it.
    """
    end = start
    while end < len(lines) and (not lines[end].strip() or leading(lines[end]) > indent):
        end += 1
    while end > start and not lines[end - 1].strip():
        end -= 1
    block = textwrap.dedent("\n".join(lines[start:end])).split("\n") if end > start else []
    while block and not block[0].strip():
        block.pop(0)
    return block, end


def leading(line):
    return len(line) - len(line.lstrip())


def parse_options(lines):
    """
    A directive's ``:name: value`` option lines, as a dict. An indented
    line continues the previous option's value.
    """
    options = {}
    last = None
    for line in lines:
        match = re.match(r"^:([\w-]+):(?:\s+(.*))?$", line)
        if match:
            last = match.group(1)
            options[last] = (match.group(2) or "").strip()
        elif last and line.strip():
            options[last] = f"{options[last]} {line.strip()}".strip()
    return options


def convert(text, context=None):
    """
    Convert a kernel-doc text section to Markdown. ``context`` is the
    ``MarkdownFormat`` rendering it, which C-domain directives need to
    register symbols and nested kernel-doc directives need to expand;
    without one (tests), those degrade to unanchored headings and errors.
    """
    lines = textwrap.dedent(text.expandtabs(8)).strip("\n").split("\n")
    out = []
    prose = []

    def flush():
        out.extend(convert_prose(prose, context))
        prose.clear()

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        indent = leading(line)

        directive = DIRECTIVE.match(stripped)
        if directive:
            flush()
            name = directive.group(1).lower()
            argument = (directive.group(2) or "").strip()
            # Whether a blank line separates the directive from its block.
            separated = i + 1 >= len(lines) or not lines[i + 1].strip()
            block, i = indented_block(lines, i + 1, indent)
            options = []
            while block and (
                re.match(r"^:[\w-]+:", block[0])
                or (options and block[0].strip() and block[0][0].isspace())
            ):
                options.append(block.pop(0))
            while block and not block[0].strip():
                block.pop(0)
            if name in CODE_DIRECTIVES:
                out.extend(fence(argument or "text", block))
            elif name in ADMONITIONS:
                if name == "admonition" and argument:
                    # A generic admonition's argument is its title.
                    lead = [f"**{argument}**", ""]
                elif argument:
                    # Any other's is the start of its text, which lines
                    # beneath it may continue.
                    lead = [argument] + ([""] if separated else [])
                else:
                    lead = []
                inner = convert("\n".join(lead + block), context)
                out.append(f"> [!{ADMONITIONS[name]}]")
                out.extend(f"> {l}" if l else ">" for l in inner.split("\n"))
                out.append("")
            elif name in C_DIRECTIVES:
                out.extend(c_directive(name, argument, block, context))
            elif name == "flat-table":
                try:
                    out.extend(flat_table(argument, parse_options(options), block, context))
                except ValueError as error:
                    warn(f"flat-table not converted ({error}); kept as preformatted text")
                    out.extend(fence("text", [stripped] + options + [""] + block))
            elif name == "kernel-doc":
                if context is None:
                    raise ValueError("a nested kernel-doc directive needs a rendering context")
                out.extend([context.expand_kernel_doc(argument, parse_options(options)), ""])
            elif name == "kernel-figure":
                if context is None or not hasattr(context, "expand_kernel_figure"):
                    raise ValueError("a kernel-figure needs a reviewed Mermaid rendering context")
                diagram, caption = context.expand_kernel_figure(argument, parse_options(options), block)
                out.extend([diagram, "", convert(caption, context), ""])
            else:
                warn(f"no Markdown form for '.. {name}::'; kept as preformatted text")
                out.extend(fence("text", [stripped] + options + ([""] if options else []) + block))
            continue

        if EXPLICIT_MARKUP.match(stripped):
            # A comment or a hyperlink target: nothing a reader sees.
            flush()
            _, i = indented_block(lines, i + 1, indent)
            continue

        if TABLE_BORDER.match(stripped):
            flush()
            end = i
            while end < len(lines) and lines[end].strip():
                end += 1
            out.extend(fence("text", textwrap.dedent("\n".join(lines[i:end])).split("\n")))
            i = end
            continue

        if (
            stripped
            and not UNDERLINE.match(stripped)
            and i + 1 < len(lines)
            and UNDERLINE.match(lines[i + 1].strip())
            and len(lines[i + 1].strip()) >= len(stripped)
            and (i == 0 or not lines[i - 1].strip())
        ):
            # A section title. Markdown would read a "~~~" underline as a
            # code fence, and the page owns the real headings anyway.
            flush()
            out.extend([f"**{inline(stripped, context)}**", ""])
            i += 2
            continue

        if stripped == "::" or LITERAL_INTRO.match(stripped):
            # "Text::" ends a paragraph and introduces a literal block:
            # "Text:" stays, a bare "::" or a spaced " ::" vanishes.
            intro = stripped[:-2]
            if intro.strip():
                prose.append(line.rstrip()[:-2] + ("" if intro.endswith(" ") else ":"))
            flush()
            block, i = indented_block(lines, i + 1, indent)
            if block:
                out.extend(fence("text", block))
            continue

        prose.append(line)
        i += 1
    flush()
    return "\n".join(collapse_blank_lines(out)).strip("\n")


def collapse_blank_lines(lines):
    """One blank line between blocks; fence contents left as they are."""
    out = []
    fence_marker = None
    for line in lines:
        stripped = line.lstrip("> ")
        if fence_marker is None and stripped.startswith("```"):
            fence_marker = stripped[: len(stripped) - len(stripped.lstrip("`"))]
        elif fence_marker is not None and stripped.rstrip() == fence_marker:
            fence_marker = None
        elif fence_marker is None and not line.strip() and out and not out[-1].strip():
            continue
        out.append(line)
    return out


#: Sphinx C-domain directives written by hand in comments, mostly for
#: macros kernel-doc cannot parse (include/uapi/drm/pvr_drm.h).
C_DIRECTIVES = {
    "c:macro": "ident",
    "c:function": "ident",
    "c:var": "ident",
    "c:type": "ident",
    "c:struct": "struct",
    "c:union": "union",
    "c:enum": "enum",
}


def c_directive(name, argument, block, context):
    """
    A hand-written C declaration: the same heading and anchor kernel-doc
    gives a parsed one, so it is a cross-reference target too.
    """
    kind = C_DIRECTIVES[name]
    before_paren = argument.split("(", 1)[0]
    identifiers = re.findall(r"\w+", before_paren)
    if not identifiers:
        warn(f"'.. {name}::' names nothing; kept as text")
        return [escape(argument), ""]
    symbol = identifiers[-1]
    if kind != "ident":
        title = f"{kind} {symbol}"
    elif name == "c:function":
        title = f"{symbol}()"
    else:
        title = argument if name == "c:macro" else symbol
    out = [symbol_heading(context, kind, symbol, title), ""]
    if name in ("c:function", "c:var"):
        out.extend(fence("c", [argument]))
    if block:
        out.extend([convert("\n".join(block), context), ""])
    return out


def symbol_heading(context, kind, name, title):
    if context is None:
        return f"#### {code(title)}"
    return context.heading_markdown(kind, name, title)


CELL_SPAN = re.compile(r"^:([cr])span:`(\d+)`\s*")


def bullet_items(lines):
    """
    The items of a bullet list whose markers sit at column 0, each as its
    lines: the text after the marker, then the rest dedented.
    """
    items = []
    for line in lines:
        marker = re.match(r"^[-*+](\s+|$)", line)
        if marker:
            items.append([line[marker.end() :]])
        elif items:
            items[-1].append(line)
        elif line.strip():
            raise ValueError(f"expected a list item, found '{line.strip()}'")
    out = []
    for first, *rest in items:
        while rest and not rest[-1].strip():
            rest.pop()
        rest = textwrap.dedent("\n".join(rest)).split("\n") if rest else []
        out.append([first, *rest] if first.strip() else rest)
    return out


def flat_table(caption, options, block, context):
    """
    The kernel's flat-table (Documentation/sphinx/rstFlatTable.py): a list
    of rows, each a list of cells, with :cspan:/:rspan: roles opening a
    cell, :header-rows:, :stub-columns: and :fill-cells:. Cells hold
    paragraphs, lists and even nested tables, which Markdown's pipe tables
    cannot, so this is an HTML table whose cells are Markdown: CommonMark
    ends an HTML block at a blank line, so blank lines around each cell's
    content make it Markdown again.
    """
    header_rows = int(options.get("header-rows") or 0)
    stub_columns = int(options.get("stub-columns") or 0)
    fill = "fill-cells" in options

    rows = []
    for row in bullet_items(block):
        cells = []
        for cell in bullet_items(row):
            text = "\n".join(cell)
            cspan = rspan = 0
            while True:
                span = CELL_SPAN.match(text)
                if not span:
                    break
                if span.group(1) == "c":
                    cspan = int(span.group(2))
                else:
                    rspan = int(span.group(2))
                text = text[span.end() :]
            cells.append([cspan, rspan, text])
        rows.append(cells)

    # Lay the cells out on a grid to find the table's width, then let each
    # short row's last cell span the rest, or pad it with empty cells.
    occupied = {}
    widths = []
    for r, cells in enumerate(rows):
        column = 0
        for cell in cells:
            while occupied.get((r, column)):
                column += 1
            for dr in range(cell[1] + 1):
                for dc in range(cell[0] + 1):
                    occupied[(r + dr, column + dc)] = True
            column += cell[0] + 1
        widths.append(max([c + 1 for (rr, c) in occupied if rr == r], default=0))
    width = max(widths, default=0)
    for r, cells in enumerate(rows):
        missing = width - widths[r]
        if missing > 0 and cells:
            if fill:
                cells.extend([0, 0, ""] for _ in range(missing))
            else:
                cells[-1][0] += missing

    out = ["<table>"]
    if caption:
        out.append(f"<caption>{html_escape(caption)}</caption>")
    for r, cells in enumerate(rows):
        if r == 0 and header_rows:
            out.append("<thead>")
        if r == header_rows:
            out.append("<tbody>")
        out.append("<tr>")
        for c, (cspan, rspan, text) in enumerate(cells):
            header = r < header_rows
            stub = not header and c < stub_columns
            tag = "th" if header or stub else "td"
            attributes = ' scope="row"' if stub else ""
            if cspan:
                attributes += f' colspan="{cspan + 1}"'
            if rspan:
                attributes += f' rowspan="{rspan + 1}"'
            content = convert(text, context) if text.strip() else ""
            if content:
                out.extend([f"<{tag}{attributes}>", "", content, "", f"</{tag}>"])
            else:
                out.append(f"<{tag}{attributes}></{tag}>")
        out.append("</tr>")
        if header_rows and r == header_rows - 1:
            out.append("</thead>")
    if rows and len(rows) > header_rows:
        out.append("</tbody>")
    out.extend(["</table>", ""])
    return out


def html_escape(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def convert_prose(lines, context=None):
    """
    Paragraphs and lists. reStructuredText indentation means a block
    quote or a definition body, but four spaces after a blank line is a
    code block in Markdown, so indentation is kept only where it continues
    a list item.

    A definition list (a term line, then its definition indented beneath
    it) becomes a "- term: definition" list, the form parameters take.
    """
    if not lines:
        return []
    normalised = []
    content = None  # the column a list item's text starts at
    term_indent = None  # the indent of terms, inside a definition list
    #: Open list items, innermost last, as (source indent of the marker,
    #: source column of the text, output column of the marker, output
    #: column of the text). Siblings share a source indent; an item more
    #: indented than the open one nests inside it, whatever the depth.
    items = []
    for k, line in enumerate(lines):
        if not line.strip():
            normalised.append("")
            continue
        indent = leading(line)
        text = line.strip()
        marker = LIST_MARKER.match(text)
        following = lines[k + 1] if k + 1 < len(lines) else ""
        if (
            not marker
            and following.strip()
            and leading(following) > indent
            and (content is None or term_indent == indent)
            and (k == 0 or not lines[k - 1].strip() or term_indent == indent)
        ):
            column = 0 if term_indent is None else min(indent, term_indent)
            if text.endswith(":"):
                normalised.append(" " * column + f"- {text}")
            elif SIMPLE_TERM.match(text):
                normalised.append(" " * column + f"- {text}:")
            else:
                # Prose that merely wraps with an indent is a definition
                # list to reStructuredText too, but a colon would change
                # its words: keep the definition a paragraph of its own.
                normalised.extend([" " * column + f"- {text}", ""])
            content = column + 2
            term_indent = indent
            items = [(indent, indent + 1, column, content)]
        elif marker:
            bullet = "1." if marker.group(1) == "#." else marker.group(1)
            while items and items[-1][0] > indent:
                items.pop()
            if items and items[-1][0] == indent:
                column = items.pop()[2]
            else:
                column = items[-1][3] if items else 0
            rest = text[marker.end() :]
            normalised.append(" " * column + f"{bullet} {rest}".rstrip())
            content = column + len(bullet) + 1
            items.append((indent, indent + marker.end(), column, content))
        elif content is not None and indent > 0:
            # Text continues the innermost item it is indented into.
            while len(items) > 1 and indent < items[-1][1]:
                items.pop()
            content = items[-1][3] if items else content
            normalised.append(" " * content + text)
        else:
            content = None
            term_indent = None
            items = []
            normalised.append(text)

    converted = inline("\n".join(normalised), context).split("\n")
    out = []
    for line in converted:
        body = line.lstrip()
        pad = line[: len(line) - len(body)]
        # Headings, quotes, and lines of one repeated punctuation mark,
        # which Markdown reads as rules, setext underlines or code fences.
        if body.startswith(("#", ">")) or (
            len(body) >= 3 and len(set(body.replace(" ", ""))) == 1 and not body[0].isalnum()
        ):
            body = "\\" + body
        out.append(pad + body)
    out.append("")
    return out


# --------------------------------------------------------------------------
# The output format
# --------------------------------------------------------------------------


class MarkdownFormat(OutputFormat):
    """kernel-doc output as Markdown for a Trail page."""

    #: Whether text uses kernel-doc's highlights (@param, %CONST, &struct x).
    #: Other plugins converting plain reStructuredText turn this off.
    highlights = True
    #: A function linking words in plain text, or None (see ``inline()``).
    autolink = None

    def __init__(self, parent=None):
        """
        A ``parent`` is the format rendering the block a nested kernel-doc
        directive sits in: the child renders into its own buffer (kdoc's
        output state is per format) but shares the symbol registry and
        the page being rendered.
        """
        super().__init__()
        if parent is None:
            #: (kind, name) -> (page reference, anchor), first definition wins.
            self.symbols = {}
            self.page_anchors = {}
            self.reference = ""
        else:
            self.symbols = parent.symbols
            self.page_anchors = parent.page_anchors
            self.reference = parent.reference
            self.kernel_figure = parent.kernel_figure

    def begin(self, reference):
        """Start rendering a block that will appear on page ``reference``."""
        self.reference = reference
        self.page_anchors.setdefault(reference, set())

    def expand_kernel_doc(self, argument, options):
        """
        Expand a kernel-doc directive found inside a comment. The plugin
        replaces this, since resolving and parsing files is its job.
        """
        raise ValueError("nested kernel-doc directives are not supported here")

    def kernel_figure(self, argument):
        """
        The Mermaid drawing of a ``.. kernel-figure::``, or None to keep
        the directive as text. The plugin replaces this, since the
        drawings live beside it.
        """
        return None

    def heading_markdown(self, kind, name, title):
        """
        A symbol's heading: h4, so it stays out of the page's table of
        contents, carrying the anchor cross-references land on (once per
        page, if a symbol is output twice).
        """
        fragment = anchor(kind, name)
        self.symbols.setdefault((kind, name), (self.reference, fragment))
        anchors = self.page_anchors[self.reference]
        tag = ""
        if fragment not in anchors:
            anchors.add(fragment)
            # Explicit, because the heading's own id is Trail's slug of
            # its text, deduplicated per page: not predictable from here.
            tag = f'<a id="{fragment}"></a>'
        return f"#### {tag}{code(title)}"

    def heading(self, kind, name, title):
        self.data += self.heading_markdown(kind, name, title) + "\n\n"

    def text(self, text):
        converted = convert(text, self)
        if converted:
            self.data += converted + "\n\n"

    def sections(self, args):
        for section, text in args.sections.items():
            if section in self.nosymbol:
                continue
            self.data += f"**{escape(section)}**\n\n"
            self.text(text)

    def items(self, title, entries):
        """A bold title over a list of (code term, description) items."""
        if not entries:
            return
        self.data += f"**{title}**\n\n"
        for term, description in entries:
            converted = convert(description, self) if description else "*undescribed*"
            lines = converted.split("\n")
            if BLOCK_START.match(lines[0]):
                # A fence, list or quote cannot share the term's line.
                self.data += f"- {code(term)}:\n\n"
            else:
                self.data += f"- {code(term)}: {lines.pop(0)}\n"
            for line in lines:
                self.data += f"  {line}\n" if line else "\n"
        self.data += "\n"

    def purpose(self, args):
        purpose = args.get("purpose", "")
        if purpose:
            self.data += inline(purpose, self) + "\n\n"

    def out_doc(self, fname, name, args):
        if not self.check_doc(name, args):
            return
        for section, text in args.sections.items():
            if section in self.nosymbol:
                continue
            # A :doc: block is placed under the page's own heading.
            if self.out_mode != self.OUTPUT_INCLUDE:
                self.data += f"**{escape(section)}**\n\n"
            self.text(text)

    def out_function(self, fname, name, args):
        func_macro = args.get("func_macro", False)
        signature = "" if func_macro else (args.get("functiontype") or "")
        if signature:
            signature += " "
        signature += name
        if not func_macro:
            params = []
            for parameter in args.parameterlist:
                dtype = args.parametertypes.get(parameter, "")
                if function_pointer.search(dtype):
                    params.append(function_pointer.group(1) + parameter + function_pointer.group(3))
                else:
                    params.append(dtype or parameter)
            signature += "(" + ", ".join(params) + ")"
        if args.get("typedef"):
            signature = "typedef " + signature

        self.heading("ident", name, name if func_macro else f"{name}()")
        self.data += "\n".join(fence("c", [signature])) + "\n"
        self.purpose(args)

        entries = []
        for parameter in args.parameterlist:
            parameter_name = re.sub(r"\[.*", "", parameter)
            description = args.parameterdescs.get(parameter_name)
            if description == KernelDoc.undescribed:
                description = None
            entries.append((args.parametertypes.get(parameter) or parameter, description))
        self.items("Parameters", entries)
        self.sections(args)

    def out_enum(self, fname, name, args):
        self.heading("enum", name, f"enum {name}")
        self.purpose(args)
        entries = []
        for parameter in args.parameterlist:
            description = args.parameterdescs.get(parameter)
            if description == KernelDoc.undescribed:
                description = None
            entries.append((parameter, description))
        self.items("Constants", entries)
        self.sections(args)

    def out_var(self, fname, name, args):
        self.heading("ident", name, name)
        self.data += "\n".join(fence("c", [args.other_stuff["full_proto"]])) + "\n"
        self.purpose(args)
        default = args.other_stuff.get("default_val")
        if default:
            self.data += f"**Initialization**\n\ndefault: {code(default)}\n\n"
        self.sections(args)

    def out_typedef(self, fname, name, args):
        self.heading("ident", name, f"typedef {name}")
        self.purpose(args)
        self.sections(args)

    def out_struct(self, fname, name, args):
        dtype = args.type
        self.heading(dtype, name, f"{dtype} {name}")
        self.purpose(args)

        definition = args.get("definition", "") or ""
        body = textwrap.dedent(definition.replace("\t", "    ")).rstrip("\n")
        lines = [f"{dtype} {name} {{"]
        lines += [f"    {line}" if line else "" for line in body.split("\n")] if body else []
        lines.append("};")
        self.data += "**Definition**\n\n" + "\n".join(fence("c", lines)) + "\n"

        entries = []
        for parameter in args.parameterlist:
            if not parameter or parameter.startswith("#"):
                continue
            parameter_name = parameter.split("[", maxsplit=1)[0]
            description = args.parameterdescs.get(parameter_name)
            if description == KernelDoc.undescribed:
                continue
            entries.append((parameter, description))
        self.items("Members", entries)
        self.sections(args)
