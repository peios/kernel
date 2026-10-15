#!/usr/bin/env bash
# Compile all guest test programs without booting a VM or requiring signing keys.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT
mkdir "$work/include"
ln -s "$here/../../include/uapi/pkm" "$work/include/pkm"
for source in "$here"/*.c; do
    gcc -static -O2 -Wall -Wextra -Werror -I"$work/include" \
        "$source" -o "$work/$(basename "${source%.c}")"
done
