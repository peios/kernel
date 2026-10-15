# SPDX-License-Identifier: GPL-2.0
"""
Markdown for the kernel's feature-support tables (``Documentation/features``),
from the data ``feat.parse_features.ParseFeature`` parses: for each feature,
its subsystem, Kconfig symbol, description and per-architecture status.

Two views, as Sphinx's ``kernel-feat`` directive gives: every feature's
status on one architecture, and the matrix of every feature on every
architecture. Links between them are cross-reference placeholders
(``kdoc_markdown.ref``), resolved once every block has rendered.
"""

from kdoc_markdown import code, ref
from trail_plugin import markdown_table, slug, text

#: Status order within a matrix cell, as ParseFeature sorts them.
STATUS_ORDER = {"ok": 0, "TODO": 1, "N/A": 2}


def status_name(status):
    """
    A status as readers see it. The files write ".." for a feature that
    can't apply to an architecture, which ParseFeature reads as "---".
    """
    return "Not compatible" if status == "---" else status


def anchor(name, feature):
    """A feature's anchor in the matrix."""
    return f"feat-{slug(feature['subsys'])}-{slug(name)}"


def ordered(data):
    """Feature names by subsystem, then name, as Sphinx orders them."""
    return sorted(data, key=lambda name: (data[name]["subsys"], name.lower()))


def kconfig(value):
    # A "|" ends a table cell even inside a code span unless escaped.
    return code(value).replace("|", "\\|")


def arch_table(data, arch):
    """Every feature's status on ``arch``, linking each to the matrix."""
    rows = []
    for name in ordered(data):
        feature = data[name]
        status = feature["table"].get(arch)
        if status is None:
            continue
        rows.append([
            text(feature["subsys"]),
            ref("feat", anchor(name, feature), text(name)),
            kconfig(feature["kconfig"]),
            text(status_name(status)),
            text(feature["description"]),
        ])
    return markdown_table(["Subsystem", "Feature", "Kconfig", "Status", "Description"], rows, escape=False)


def statuses(table):
    """A matrix cell: architectures grouped by status, each linking to its own table."""
    groups = {}
    for arch, status in sorted(table.items(), key=lambda item: (STATUS_ORDER.get(item[1], 99), item[0].lower())):
        groups.setdefault(status_name(status), []).append(ref("feat-arch", arch, text(arch)))
    return "<br>".join(f"**{text(status)}**: " + ", ".join(archs) for status, archs in groups.items())


def matrix(data):
    """Every feature on every architecture, a table per subsystem."""
    out = []
    by_subsystem = {}
    for name in ordered(data):
        by_subsystem.setdefault(data[name]["subsys"], []).append(name)
    for subsystem, names in by_subsystem.items():
        rows = [
            [
                f'<a id="{anchor(name, data[name])}"></a>{text(name)}',
                kconfig(data[name]["kconfig"]),
                text(data[name]["description"]),
                statuses(data[name]["table"]),
            ]
            for name in names
        ]
        out += [
            f"## Subsystem: {text(subsystem)}",
            "",
            markdown_table(["Feature", "Kconfig", "Description", "Status per architecture"], rows, escape=False),
            "",
        ]
    return "\n".join(out)
