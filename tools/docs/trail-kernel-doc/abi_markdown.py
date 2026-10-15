# SPDX-License-Identifier: GPL-2.0
"""
Markdown for the kernel's ABI documentation (``Documentation/ABI``), from
the data ``abi.abi_parser.AbiParser`` parses.

Two views, as Sphinx's ``kernel-abi`` directive gives: the symbols of one
ABI level (stable, testing, obsolete, removed), grouped by where they
live, and the files they are documented in. Links between the views,
and from descriptions to the symbols and files they mention, are
cross-reference placeholders (``kdoc_markdown.ref``), resolved once every
block has rendered.
"""

import re

import kdoc_markdown
from kdoc_markdown import code, convert, escape, ref
from trail_plugin import slug, text

#: A path an ABI description may mention that names a documented symbol
#: (AbiParser.XREF, with lookarounds so the delimiters stay put).
SYMBOL_PATH = re.compile(r"(?<![^\s(])(/(?:sys|config|proc|dev|kvd)/[^,.:;)\s]+)(?=[,.:;)\s]|$)")

#: A mention of an ABI file.
ABI_FILE = re.compile(r"Documentation/ABI/[\w/-]+")

#: Section underlines inside descriptions, which AbiParser drops.
TITLE_MARK = re.compile(r"\n[-*=^~]+\n")

#: Metadata shown for each symbol, in this order.
FIELDS = (("date", "Date"), ("kernelversion", "KernelVersion"), ("contact", "Contact"))


def is_file(entry):
    return entry.get("type") == "File"


def ordered(data):
    """Entries as Sphinx orders them: symbols, then files, by name."""
    return sorted(
        data.items(),
        key=lambda item: (item[1].get("type", ""), item[1].get("what"), item[1]["file"][0][0], item[1].get("line_no", 0)),
    )


def part(name):
    """The group a symbol is listed under: its first one or two path components."""
    if "/" in name:
        match = re.match(r"(\/?(?:[\w\-]+\/?){1,2})", name)
        if match:
            return "Symbols under " + match.group(1).rstrip("/")
    return name


class AbiMarkdown:
    """Renders views of one parsed ABI tree."""

    def __init__(self, parser):
        self.data = parser.data
        #: What -> the key of the entry documenting it.
        self.what_refs = parser.what_refs
        #: Symbol key -> anchor, unique across the tree and stable while
        #: the symbols' names are.
        self.anchors = {}
        used = {}
        for key, entry in ordered(self.data):
            if is_file(entry):
                base = "abi-file-" + slug(entry["file"][0][0].removeprefix("Documentation/ABI/"))
            else:
                base = "abi-" + slug(entry["what"][0])
            count = used[base] = used.get(base, 0) + 1
            self.anchors[key] = base if count == 1 else f"{base}-{count}"
        self.context = kdoc_markdown.MarkdownFormat()
        self.context.highlights = False
        self.context.autolink = self.autolink

    def autolink(self, value):
        """Link the symbols and ABI files a description mentions."""
        out = []
        last = 0
        for match in re.finditer(f"{SYMBOL_PATH.pattern}|{ABI_FILE.pattern}", value):
            found = match.group(0)
            if found.startswith("Documentation/"):
                link = ref("abi-file", found, escape(found))
            elif found in self.what_refs:
                link = ref("abi", self.what_refs[found], escape(found))
            else:
                continue
            out.append(escape(value[last : match.start()]))
            out.append(link)
            last = match.end()
        out.append(escape(value[last:]))
        return "".join(out)

    def description(self, value):
        value = TITLE_MARK.sub("\n\n", "\n" + value).strip("\n")
        return convert(value, self.context) if value.strip() else ""

    def register(self, symbols, reference, abi_type, show_symbols, show_files):
        """Record the entries a view on page ``reference`` will define."""
        if abi_type == "README":
            return
        for key, entry in self.data.items():
            if entry.get("path") != abi_type:
                continue
            if is_file(entry) and show_files:
                symbols.setdefault(("abi-file", entry["file"][0][0]), (reference, self.anchors[key]))
            elif not is_file(entry) and show_symbols:
                symbols.setdefault(("abi", key), (reference, self.anchors[key]))

    def render(self, reference, abi_type, show_symbols=True, show_files=True):
        self.context.begin(reference)
        out = []
        current = None
        for key, entry in ordered(self.data):
            if entry.get("path") != abi_type:
                continue
            if is_file(entry):
                if show_files:
                    out += self.file_entry(key, entry, readme=abi_type == "README")
            elif show_symbols:
                group = part(entry["what"][0])
                if group != current:
                    current = group
                    out += [f"## {text(group)}", ""]
                out += self.symbol_entry(key, entry)
        return "\n".join(out)

    def symbol_entry(self, key, entry):
        names = entry["what"]
        out = [f'#### <a id="{self.anchors[key]}"></a>{code(names[0])}', ""]
        if len(names) > 1:
            out += [f"- {code(name)}" for name in names[1:]] + [""]
        for path, _ in entry["file"]:
            out += ["Defined in " + ref("abi-file", path, code(path.rsplit("/", 1)[-1])) + ".", ""]
        fields = [f"- **{label}:** {text(entry[tag])}" for tag, label in FIELDS if entry.get(tag, "").strip()]
        if fields:
            out += fields + [""]
        description = self.description(entry.get("description", ""))
        out += [description or "*No description.*", ""]
        users = entry.get("users", "").strip()
        if users:
            out += ["**Users:**", "", self.description(users), ""]
        return out

    def file_entry(self, key, entry, readme=False):
        description = self.description(entry.get("description", ""))
        if readme:
            # The README is the introduction to the ABI documentation.
            return [description, ""]
        # Keep the stable ABI target distinct from Trail's automatic heading
        # slug; "ABI file ..." otherwise produces the same id twice.
        title = "File " + entry["what"][0].removeprefix("ABI file ")
        out = [f'## <a id="{self.anchors[key]}"></a>{text(title)}', ""]
        if description:
            out += [description, ""]
        if entry.get("symbols"):
            out += ["Has the following ABI:", ""]
            out += [f"- {ref('abi', symbol_key, code(what))}" for what, symbol_key in entry["symbols"]]
            out += [""]
        return out
