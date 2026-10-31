#!/usr/bin/env python3
"""Make one tree the same as another, rewriting only what differs.

`stage-tree.py SOURCE DEST [--owned PATH]...` makes DEST hold what SOURCE
holds: each file with its content and whether it is executable, each
symbolic link with its target, each directory. A file whose content and
mode are already the same is left alone, its modification time with it,
so that Kbuild, which judges what to rebuild by modification times, rebuilds
only what changed. A file written is given the time it was written. What
DEST holds that SOURCE doesn't is removed, but an `--owned` path, which the
build writes itself, is neither written nor removed.
"""

import argparse
import os
import shutil
import stat
import sys
from pathlib import Path


def same_file(source: Path, dest: Path) -> bool:
    """Whether `dest` is a regular file of `source`'s content and mode."""
    try:
        info = dest.lstat()
    except FileNotFoundError:
        return False
    if not stat.S_ISREG(info.st_mode):
        return False
    wanted = source.stat()
    if (info.st_mode & 0o111 != 0) != (wanted.st_mode & 0o111 != 0):
        return False
    if info.st_size != wanted.st_size:
        return False
    with source.open("rb") as one, dest.open("rb") as other:
        while True:
            a = one.read(1 << 20)
            if a != other.read(1 << 20):
                return False
            if not a:
                return True


def remove(path: Path) -> None:
    """Removes `path`, whatever it is, a directory with what it holds."""
    if path.is_dir() and not path.is_symlink():
        for parent, directories, names in os.walk(path):
            for name in directories:
                os.chmod(os.path.join(parent, name), 0o755)
        shutil.rmtree(path)
    elif path.exists() or path.is_symlink():
        path.unlink()


def stage(source: Path, dest: Path, owned: set[str]) -> int:
    """Makes `dest` hold what `source` does: how many entries it wrote."""
    written = 0
    dest.mkdir(parents=True, exist_ok=True)
    for parent, directories, names in os.walk(source):
        directories.sort()
        relative = Path(parent).relative_to(source)
        into = dest / relative
        wanted = set(directories) | set(names)
        # What the tree here no longer holds goes, but what the build owns.
        for present in os.listdir(into):
            if present not in wanted and str(relative / present) not in owned:
                remove(into / present)
        for name in [*directories]:
            at = Path(parent) / name
            target = into / name
            if at.is_symlink():
                directories.remove(name)
                names.append(name)
                continue
            if target.is_symlink() or (target.exists() and not target.is_dir()):
                remove(target)
            target.mkdir(exist_ok=True)
            os.chmod(target, 0o755)
        for name in sorted(names):
            path = relative / name
            if str(path) in owned:
                continue
            at = Path(parent) / name
            target = into / name
            if at.is_symlink():
                link = os.readlink(at)
                if target.is_symlink() and os.readlink(target) == link:
                    continue
                remove(target)
                os.symlink(link, target)
                written += 1
            elif not same_file(at, target):
                remove(target)
                shutil.copyfile(at, target)
                os.chmod(target, 0o755 if at.stat().st_mode & 0o111 else 0o644)
                written += 1
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("source", type=Path)
    parser.add_argument("dest", type=Path)
    parser.add_argument("--owned", action="append", default=[])
    args = parser.parse_args()
    written = stage(args.source, args.dest, set(args.owned))
    print(f"stage-tree: {written} entries written", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
