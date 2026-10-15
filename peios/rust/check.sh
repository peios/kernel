#!/bin/bash
# Host tests exercise the exact semantic core source compiled by Kbuild.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
cargo +1.98.1 test --workspace --locked --offline
cargo +1.98.1 clippy --workspace --all-targets --locked --offline -- -A clippy::all -D clippy::correctness
