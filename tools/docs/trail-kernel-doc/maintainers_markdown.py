# SPDX-License-Identifier: GPL-2.0
"""
Markdown for the kernel's MAINTAINERS file, following the reading that
Sphinx's ``maintainers-include`` directive gives it:

- the file's title is dropped (the page has its own);
- its "Descriptions" block, which explains the field letters and is laid
  out with tabs, stays preformatted, and names the fields: ``*Mail*``
  makes "M:" lines "Mail";
- every subsystem entry becomes an anchored heading with its fields
  listed beneath, consecutive lines of one field joined.
"""

import re

from kdoc_markdown import code, convert
from trail_plugin import SPECIALS, slug, text

#: Fields whose values are paths or patterns, shown as code.
PATTERN_FIELDS = ("F", "N", "X", "K")

#: Addresses and URLs in field values, made links.
LINKABLE = re.compile(
    r"(?P<url>(?:https?|ftp|git|irc|ircs)://[^\s<>]+|mailto:[^\s<>]+)"
    r"|(?P<email>[\w.+-]+@[\w-]+(?:\.[\w-]+)+)"
)


def anchor(name):
    return "maintainers-" + slug(name).lower()


def value(field, details):
    """One field line's value as Markdown."""
    if field in PATTERN_FIELDS:
        return code(details)

    def plain(piece):
        return SPECIALS.sub(r"\\\1", re.sub(r"\s+", " ", piece))

    out = []
    last = 0
    for match in LINKABLE.finditer(details):
        out.append(plain(details[last : match.start()]))
        # Autolinked; angle brackets around an address stay visible.
        out.append(f"<{match.group(0)}>")
        last = match.end()
    out.append(plain(details[last:]))
    return "".join(out)


def render(source):
    lines = source.split("\n")
    out = []
    fields = {}
    i = 0

    # The file's own title.
    if len(lines) > 1 and re.fullmatch(r"=+", lines[1].strip()):
        i = 2

    # Up to the first subsystem: headings, the Descriptions block, prose.
    prose = []

    def flush():
        if any(line.strip() for line in prose):
            out.extend([convert("\n".join(prose)), ""])
        prose.clear()

    maintainers = False
    while i < len(lines):
        line = lines[i].rstrip()
        underline = lines[i + 1].strip() if i + 1 < len(lines) else ""
        if line and re.fullmatch(r"-{3,}", underline):
            flush()
            out.extend([f"## {text(line)}", ""])
            i += 2
            if line.startswith("Descriptions"):
                block = []
                while i < len(lines) and not lines[i].startswith("Maintainers"):
                    block.append(lines[i].rstrip())
                    i += 1
                while block and not block[-1]:
                    block.pop()
                while block and not block[0]:
                    block.pop(0)
                for entry in block:
                    match = re.search(r"\s(\S):\s", entry)
                    named = re.search(r"\*([^*]+)\*", entry)
                    if match and named and match.group(1) not in fields:
                        fields[match.group(1)] = named.group(1)
                run = max((len(r) for r in re.findall(r"`{3,}", "\n".join(block))), default=2)
                out.extend(["`" * (run + 1) + "text", *block, "`" * (run + 1), ""])
            elif line.startswith("Maintainers"):
                maintainers = True
            continue
        if maintainers and re.match(r"[A-Z0-9]", line):
            break
        prose.append(lines[i])
        i += 1
    flush()

    # The subsystem entries.
    used = {}
    entry = None
    for line in lines[i:]:
        line = line.rstrip()
        if not line:
            continue
        if len(line) < 2 or line[1] != ":":
            if entry:
                out.extend(entry_markdown(*entry, fields))
            name = re.sub(r"\s+", " ", line)
            base = anchor(name)
            count = used[base] = used.get(base, 0) + 1
            entry = (name, base if count == 1 else f"{base}-{count}", [])
            continue
        if entry is None:
            continue
        field, details = line.split(":", 1)
        details = details.strip()
        rows = entry[2]
        if rows and rows[-1][0] == field:
            rows[-1][1].append(details)
        else:
            rows.append((field, [details]))
    if entry:
        out.extend(entry_markdown(*entry, fields))
    return "\n".join(out)


def entry_markdown(name, fragment, rows, fields):
    out = [f'#### <a id="{fragment}"></a>{text(name)}', ""]
    for field, values in rows:
        label = fields.get(field, field)
        out.append(f"- **{text(label)}:** " + ", ".join(value(field, v) for v in values))
    return out + [""]
