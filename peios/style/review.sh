#!/bin/bash
# Kernel checkpatch is advisory: its rules include policies Peios keeps soft.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.."
base=${1:?Usage: review.sh BASE_REF}
git rev-parse --verify "${base}^{commit}" >/dev/null
patch=$(mktemp)
trap 'rm -f -- "$patch"' EXIT
git diff --no-ext-diff --no-color "$base" -- \
    arch block drivers fs include kernel mm net security >"$patch"
if [[ ! -s "$patch" ]]; then
    echo "No kernel changes for checkpatch to review."
    exit 0
fi
if perl scripts/checkpatch.pl --no-tree --no-signoff --show-types "$patch"; then
    exit 0
else
    status=$?
    if [[ "$status" == 1 ]]; then
        echo "Checkpatch findings above require review; this check is advisory."
        exit 0
    fi
    exit "$status"
fi
