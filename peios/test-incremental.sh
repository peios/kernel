#!/bin/bash
# An incremental kernel build gives what a clean one does (PEI-1639),
# after a build that failed too (PEI-1643): the kernel built in a temporary
# worktree of this checkout, one source file broken and the build required
# to fail on it, the file changed instead, built again incrementally from
# the object tree pekit keeps in the step's scratch directory, and the same
# tree built strictly, from an empty one. Every output is compared byte for
# byte. The incremental build's time is printed. Opt-in, since it builds
# the kernel three times at most, and run by hand,
# `bash peios/test-incremental.sh [TARGET]`, not by `pekit run`: its builds
# run pekit, whose sandboxes a script's can't hold.
set -euo pipefail

profile=${1:-kernel}
repo=$(git rev-parse --show-toplevel)
work=$(mktemp -d "${TMPDIR:-/var/tmp}/kernel-incremental.XXXXXX")
cleanup() {
    git -C "$repo" worktree remove --force "$work/tree" 2>/dev/null || true
    rm -r --one-file-system "$work"
}
trap cleanup EXIT
git -C "$repo" worktree add --quiet --detach "$work/tree" HEAD
cd "$work/tree"

# Where pekit says a build of the target put its outputs.
outputs() {
    awk -v target="built /$profile" \
        'found { sub(/^  /, ""); print; exit } $0 == target || index($0, target ":") == 1 { found = 1 }'
}

# The object tree, made or brought up to date for this tree.
pekit build "$profile" >/dev/null

# A source file that doesn't compile, whose build must fail on that file.
printf '\nstatic int incremental_check __used = ;\n' >>kernel/sys.c
if pekit build "$profile" >"$work/failed" 2>&1; then
    echo "a build of a broken source file passed" >&2
    exit 1
fi
if ! grep -q 'kernel/sys\.c' "$work/failed"; then
    cat "$work/failed" >&2
    echo "the build failed, but not on the broken source file" >&2
    exit 1
fi
git checkout -- kernel/sys.c

# One change to a source file, which an incremental build rebuilds alone.
printf '\nstatic int incremental_check __used = 1;\n' >>kernel/sys.c

began=$(date +%s)
incremental=$(pekit build "$profile" | outputs)
echo "incremental build after one change: $(($(date +%s) - began)) s"
clean=$(pekit build --strict "$profile" | outputs)

# Each output of the two builds, by its digest.
digests() {
    (cd "$1" && find . -type f -print0 | sort -z | xargs -0 sha256sum)
}
if diff <(digests "$incremental") <(digests "$clean"); then
    echo "the incremental build gives what a clean build does"
else
    echo "the incremental build differs from a clean build" >&2
    exit 1
fi
