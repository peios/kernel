# SPDX-License-Identifier: GPL-2.0
"""
Tests for the feature, ABI and MAINTAINERS renderers, on made-up data.
They import kdoc_markdown, which needs the kernel tree (see
test_kdoc_markdown.py):

    KERNEL_SRCTREE=/path/to/kernel python3 -m unittest test_generators
"""

import os
import sys
import unittest
from types import SimpleNamespace

HERE = os.path.dirname(os.path.realpath(__file__))
SRCTREE = os.environ.get("KERNEL_SRCTREE", os.path.join(HERE, "..", "kernel"))
sys.path.insert(0, os.path.join(SRCTREE, "tools", "lib", "python"))
sys.path.insert(1, HERE)

import abi_markdown  # noqa: E402
import feat_markdown  # noqa: E402
import kdoc_markdown  # noqa: E402
import maintainers_markdown  # noqa: E402
import uapi_markdown  # noqa: E402
from trail_plugin import AnchorIndex  # noqa: E402

FEATURES = {
    "eBPF-JIT": {
        "subsys": "core", "kconfig": "HAVE_EBPF_JIT", "description": "arch supports eBPF JIT",
        "table": {"x86": "ok", "arm": "TODO", "alpha": "---"},
    },
    "THP": {
        "subsys": "vm", "kconfig": "A || B", "description": "transparent huge pages",
        "table": {"x86": "ok"},
    },
}


class Features(unittest.TestCase):
    def test_arch_tables_link_features_to_the_matrix(self):
        symbols = {("feat", "feat-core-eBPF-JIT"): ("k/all", "feat-core-eBPF-JIT")}
        markdown = kdoc_markdown.resolve_refs(feat_markdown.arch_table(FEATURES, "x86"), symbols, "k/x86")
        self.assertEqual(
            markdown,
            "| Subsystem | Feature | Kconfig | Status | Description |\n|---|---|---|---|---|\n"
            "| core | [eBPF-JIT](~k/all#feat-core-eBPF-JIT) | `HAVE_EBPF_JIT` | ok | arch supports eBPF JIT |\n"
            "| vm | THP | `A \\|\\| B` | ok | transparent huge pages |",
        )

    def test_the_matrix_groups_statuses_and_links_architectures(self):
        symbols = {("feat-arch", "x86"): ("k/x86", ""), ("feat-arch", "arm"): ("k/all", "")}
        markdown = kdoc_markdown.resolve_refs(feat_markdown.matrix(FEATURES), symbols, "k/all")
        self.assertIn("## Subsystem: core\n", markdown)
        self.assertIn(
            '| <a id="feat-core-eBPF-JIT"></a>eBPF-JIT | `HAVE_EBPF_JIT` | arch supports eBPF JIT | '
            "**ok**: [x86](~k/x86)<br>**TODO**: arm<br>**Not compatible**: alpha |",
            markdown,
        )


def abi_tree():
    return SimpleNamespace(
        data={
            "abi_sys_a": {
                "what": ["/sys/a", "/sys/a2"], "file": [("Documentation/ABI/stable/sysfs-a", "f_a")],
                "path": "stable", "line_no": 1, "date": "May 2007", "contact": "x <x@y.org>",
                "description": "See /sys/b and Documentation/ABI/stable/sysfs-a.\nHeading\n=======\n100% @here",
            },
            "abi_sys_b": {
                "what": ["/sys/b"], "file": [("Documentation/ABI/stable/sysfs-a", "f_a")],
                "path": "stable", "line_no": 9, "description": "",
            },
            "f_a": {
                "what": ["ABI file stable/sysfs-a"], "type": "File", "path": "stable",
                "file": [("Documentation/ABI/stable/sysfs-a", "f_a")], "description": "",
                "symbols": [("/sys/a", "abi_sys_a"), ("/sys/b", "abi_sys_b")],
            },
        },
        what_refs={"/sys/a": "abi_sys_a", "/sys/a2": "abi_sys_a", "/sys/b": "abi_sys_b"},
    )


class Abi(unittest.TestCase):
    def setUp(self):
        self.views = abi_markdown.AbiMarkdown(abi_tree())
        self.symbols = self.views.context.symbols
        self.views.register(self.symbols, "k/abi-stable", "stable", True, False)
        self.views.register(self.symbols, "k/abi-stable-files", "stable", False, True)

    def render(self, page, **view):
        return kdoc_markdown.resolve_refs(self.views.render(page, "stable", **view), self.symbols, page)

    def test_symbols_link_to_their_file_and_what_they_mention(self):
        markdown = self.render("k/abi-stable", show_files=False)
        self.assertTrue(markdown.startswith(
            '## Symbols under /sys/a\n\n#### <a id="abi-sys-a"></a>`/sys/a`\n\n- `/sys/a2`\n\n'
            "Defined in [`sysfs-a`](~k/abi-stable-files#abi-file-stable-sysfs-a).\n\n"
            "- **Date:** May 2007\n- **Contact:** x \\<x@y.org\\>\n\n"
            "See [/sys/b](#abi-sys-b) and "
            "[Documentation/ABI/stable/sysfs-a](~k/abi-stable-files#abi-file-stable-sysfs-a).\n"
            # Underlines go, as AbiParser drops them, and plain
            # reStructuredText has no %CONST or @param.
            "Heading\n\n100% @here\n"
        ), markdown)
        self.assertIn('#### <a id="abi-sys-b"></a>`/sys/b`', markdown)
        self.assertIn("*No description.*", markdown)

    def test_files_list_their_symbols(self):
        markdown = self.render("k/abi-stable-files", show_symbols=False)
        self.assertEqual(
            markdown,
            '## <a id="abi-file-stable-sysfs-a"></a>File stable/sysfs-a\n\nHas the following ABI:\n\n'
            "- [`/sys/a`](~k/abi-stable#abi-sys-a)\n- [`/sys/b`](~k/abi-stable#abi-sys-b)\n",
        )


MAINTAINERS = """List of maintainers
===================

Descriptions of section entries and preferred order
---------------------------------------------------

	M: *Mail* patches to: FullName <address@domain>
	F: *Files* and directories wildcard patterns.

Maintainers List
----------------

.. note:: Look for the most precise areas
          first.

3C59X NETWORK DRIVER
M:	Steffen Klassert <klassert@kernel.org>
M:	A_N Other <other@kernel.org>
L:	netdev@vger.kernel.org (moderated)
W:	https://example.org/x_y
F:	drivers/net/*_3c59x.c

3C59X NETWORK DRIVER
S:	Odd Fixes
"""


class Maintainers(unittest.TestCase):
    def test_entries_become_anchored_field_lists(self):
        markdown = maintainers_markdown.render(MAINTAINERS)
        self.assertTrue(markdown.startswith("## Descriptions of section entries and preferred order\n\n```text\n"))
        self.assertIn("> [!NOTE]\n> Look for the most precise areas\n> first.\n", markdown)
        self.assertIn(
            '#### <a id="maintainers-3c59x-network-driver"></a>3C59X NETWORK DRIVER\n\n'
            "- **Mail:** Steffen Klassert \\<<klassert@kernel.org>\\>, A\\_N Other \\<<other@kernel.org>\\>\n"
            "- **L:** <netdev@vger.kernel.org> (moderated)\n"
            "- **W:** <https://example.org/x_y>\n"
            "- **Files:** `drivers/net/*_3c59x.c`\n",
            markdown,
        )
        self.assertIn('<a id="maintainers-3c59x-network-driver-2"></a>', markdown)


ANCHORS = AnchorIndex({
    "k/uapi/v4l/vidioc-querycap": ["rst-vidioc-querycap", "c-v4l2_capability"],
    "k/uapi/v4l/buffer": ["c-enum-v4l2_buf_type"],
    "k/uapi/cec/caps": ["c-v4l2_capability"],
    "k/core/api": ["c-ktime_get"],
})


class Anchors(unittest.TestCase):
    def test_bare_ampersand_does_not_link_to_an_authored_function(self):
        self.assertIsNone(ANCHORS.find(kdoc_markdown.authored_anchors('type', 'ktime_get'), 'k/core/time'))

    def test_the_nearest_page_wins_when_several_define_an_anchor(self):
        self.assertEqual(
            ANCHORS.find(["c-v4l2_capability"], "k/uapi/v4l/videodev"),
            ("k/uapi/v4l/vidioc-querycap", "c-v4l2_capability"),
        )
        self.assertEqual(ANCHORS.find(["c-v4l2_capability"], "k/uapi/cec/header")[0], "k/uapi/cec/caps")
        self.assertIsNone(ANCHORS.find(["c-nothing"], "k/x"))

    def test_kernel_doc_falls_back_to_authored_types_only(self):
        def authored(kind, name):
            return ANCHORS.find(kdoc_markdown.authored_anchors(kind, name), "k/core/time")

        markdown = kdoc_markdown.convert("See &struct v4l2_capability, &v4l2_buf_type and ktime_get().")
        # Function names stay unlinked: authored ones drop their namespace.
        self.assertEqual(
            kdoc_markdown.resolve_refs(markdown, {}, "k/core/time", authored),
            "See [`struct v4l2_capability`](~k/uapi/cec/caps#c-v4l2_capability), "
            "[`v4l2_buf_type`](~k/uapi/v4l/buffer#c-enum-v4l2_buf_type) and `ktime_get()`.",
        )


class Uapi(unittest.TestCase):
    def test_labels_become_their_docutils_ids(self):
        self.assertEqual(uapi_markdown.make_id("VIDIOC_QUERYCAP"), "vidioc-querycap")
        self.assertEqual(uapi_markdown.make_id("2-Bandwidth  1.712_MHz-"), "bandwidth-1-712-mhz")

    def test_symbols_link_to_their_labels_and_types(self):
        parser = SimpleNamespace(
            DEF_SYMBOL_TYPES={
                "ioctl": {"description": "IOCTL Commands"},
                "struct": {"description": "Structures"},
                "symbol": {"description": "Enumeration values"},
                "typedef": {"description": "Type Definitions"},
            },
            symbols={
                "ioctl": {"VIDIOC_QUERYCAP": ("\\ :ref:`VIDIOC_QUERYCAP <vidioc_querycap>`\\ ", 2659)},
                "struct": {
                    "v4l2_capability": ("\\ :c:type:`v4l2_capability <V4L.v4l2_capability>`\\ ", 470),
                    "v4l2_secret": ("\\ :c:type:`v4l2_secret <V4L.v4l2_secret>`\\ ", 9),
                },
                "symbol": {"V4L2_BUF_TYPE_X": (":c:type:`V4L2_BUF_TYPE_X <V4L.v4l2_buf_type>`", 153)},
                "typedef": {},
            },
        )
        here = "k/uapi/v4l/videodev"
        markdown, unresolved = uapi_markdown.toc(
            parser, "include/uapi/linux/videodev2.h", lambda c: ANCHORS.find(c, here), here
        )
        self.assertEqual(
            markdown,
            "## Enumeration values\n\n"
            "- [`V4L2_BUF_TYPE_X`](~k/uapi/v4l/buffer#c-enum-v4l2_buf_type): "
            "`include/uapi/linux/videodev2.h`, line 154\n\n"
            "## IOCTL Commands\n\n"
            "- [`VIDIOC_QUERYCAP`](~k/uapi/v4l/vidioc-querycap#rst-vidioc-querycap): "
            "`include/uapi/linux/videodev2.h`, line 2660\n\n"
            "## Structures\n\n"
            "- [`v4l2_capability`](~k/uapi/v4l/vidioc-querycap#c-v4l2_capability): "
            "`include/uapi/linux/videodev2.h`, line 471\n"
            "- `v4l2_secret`: `include/uapi/linux/videodev2.h`, line 10\n",
        )
        self.assertEqual(unresolved, ["v4l2_secret"])


if __name__ == "__main__":
    unittest.main()
