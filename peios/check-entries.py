#!/usr/bin/env python3
"""Fail if a tracked top-level entry is neither kernel source nor left out.

`kernel.gcsl` names the kernel's source by its top-level entries, so that
editing pekit's own files rebuilds no kernel. A new entry, from a rebase on
a new Linux release say, has to be placed in those lists or in
`NOT_KERNEL` on purpose: otherwise Kbuild would silently go without it.
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).absolute().parents[1]
LISTS = ("KERNEL_DIRS", "KERNEL_FILES", "NOT_KERNEL")


def listed() -> set[str]:
    """The top-level entries `kernel.gcsl`'s lists name."""
    text = (ROOT / "kernel.gcsl").read_text()
    names: set[str] = set()
    for name in LISTS:
        found = re.search(rf"^let {name} = \[(.*?)\]$", text, re.MULTILINE | re.DOTALL)
        if found is None:
            raise ValueError(f"kernel.gcsl has no list {name}")
        names.update(re.findall(r'"([^"]+)"', found[1]))
    return names


def tracked() -> set[str]:
    """The top-level entries git tracks."""
    files = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, check=True, capture_output=True
    ).stdout
    return {name.split("/")[0] for name in files.decode().split("\0") if name}


def main() -> int:
    missing = sorted(tracked() - listed())
    for name in missing:
        print(f"check-entries: {name} is neither kernel source nor in NOT_KERNEL", file=sys.stderr)
    return int(bool(missing))


if __name__ == "__main__":
    sys.exit(main())
