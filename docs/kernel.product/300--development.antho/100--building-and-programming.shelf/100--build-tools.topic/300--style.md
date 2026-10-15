---
title: "Style tooling"
type: guide
description: "Install and run the scoped Peios formatters, linters and CI checks."
---

Run commands from the kernel repository root. Follow `peios/CODING_STYLE.md`
and the workspace `_styleguide` for the underlying rules.

The kernel carries the subset of the central Peios style tooling that it needs.
It works from this checkout alone. `peios/style/ORIGIN.json` records central configuration
hashes and adaptations; update the snapshot deliberately when policy changes.

## Setup and use

Use x86_64 Linux. Setup needs Python 3.14.4 with venv/pip, network access, and
rustfmt installed for Rust 1.83.0 and 1.98.1. The existing build wrappers still
support Python 3.11; the newer Python version belongs to the style tools.

```sh
rustup toolchain install 1.83.0 --profile minimal --component rustfmt
rustup toolchain install 1.98.1 --profile minimal --component rustfmt --component clippy
python3 peios/style.py setup

./peios/bazel test //:style //peios/style:tests
./peios/bazel run //:format
./peios/bazel run //:style-review -- HEAD
```

Select Python 3.14.4 for the setup command. It installs exact, hash-locked wheels
and binaries in `~/.cache/peios/kernel-style/<lock-identity>`. Set
`PEIOS_STYLE_CACHE` to relocate that cache. Setup does not install Rust or change
the default toolchain. Checks verify tools and fail if setup is missing; checks
never download dependencies or repair source. A check can be run directly with
`python3 peios/style.py check`; formatting with `python3 peios/style.py format`.

The Bazel test rules inherit only the tool lookup/cache variables they need:
PATH, HOME, RUSTUP_HOME, CARGO_HOME and PEIOS_STYLE_CACHE. They are deliberately
local checks, with remote execution and cached test results disabled. This is
not a hermetic compiler image. The environment allowance is implemented in
`peios/style/rules.bzl`.

## Scope and gates

`peios/style/scope.json` lists owned roots, individual integration headers, and exclusions
with reasons. Run `python3 peios/style.py inventory` to inspect the selected
files. New supported source files under an owned root are discovered automatically.
When adding an independently owned root or a Bazel subpackage, update both this
scope and `//:style-sources` so the Bazel runfiles contain it.

Included: Peios subsystems under `security/pkm`, `fs/stratafs`, and `net/ntfe`;
their owned integration/UAPI headers; Peios build/package wrappers; this tooling;
and the Cargo workspace and tests. Generated constants, event tables, test
vectors, Unicode tables and ABI types stay generated. The pinned `peios/vendor`
snapshot retains its source conventions. The separate, active documentation
migration is temporarily excluded; its style integration is still outstanding.

Blocking checks are formatter stability, Ruff, mypy, ShellCheck and the selected
buildifier checks. C uses clang-format 18.1.8 and the inherited `.clang-format`.
Kernel Rust uses rustfmt 1.83.0 and `.rustfmt.toml`, preserving module/import order
as approved for Peios source. Host Rust uses rustfmt 1.98.1 and each Cargo crate's
edition. Formatters receive one file at a time; Rust formatting does not traverse
into excluded child modules. Python uses the common 3.11 syntax profile and
package-local import roots. Mypy does not reuse incremental results.

`style-review` runs the checked-out kernel's checkpatch against a chosen Git base.
It reports findings without imposing checkpatch's whole policy as a merge gate.
Git/tool failures still fail the command. Untracked additions are not in a Git
diff; the owned-file style check covers their formatting. The command does not
modify code. Review inheritance changes in their surrounding upstream context.

Soft width/function-size/nesting guidance, names, ownership, interfaces and
performance remain review responsibilities. Compiler checks and KUnit retain
their normal build commands. No full-kernel clang-tidy policy is introduced.

## CI

`.github/workflows/style.yml` installs the same pins and runs the same Bazel
style, command regression, Cargo, C ABI and KMES event-table targets on pushes
and pull requests.
PRs also receive advisory checkpatch output against the merge commit's first
parent. Actions are pinned to reviewed release commit IDs, credentials are not
persisted, and the workflow has read-only repository permission.

Making the workflow job a required merge check is a separate repository-settings
action; the workflow file does not establish branch protection. The workflow does not claim a kernel build or VM test.
