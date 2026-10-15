---
title: "Developing native kernel subsystems"
description: "Find canonical source, host tests and kernel integration checks for Peios subsystems."
type: guide
---

The kernel repository owns the native subsystem code. Make implementation
changes in `security/pkm/`, `fs/stratafs/` and `net/ntfe/`, with public declarations
in `include/uapi/pkm/`.

## Shared Rust cores

The Cargo workspace in `peios/rust/` compiles the semantic sources used by
Kbuild through small wrapper crates. It does not maintain a second copy of
the implementation. From the kernel root:

```sh
./peios/bazel test //:rust-core-tests //:uapi-tests
```

For a direct host run:

```sh
cd peios/rust
cargo test --workspace --locked --offline
bash check.sh
```

The host workspace's toolchain is pinned in `peios/rust/rust-toolchain.toml`;
the kernel build has its own toolchain requirements. Host tests exercise the
userspace allocation/runtime path. Do not use Cargo `--all-features` as a
substitute for Kbuild, KUnit or VM integration tests.

## Kernel integration

Use [Building Peios](<~kernel/development/start-here/building-peios>) for the
supported build entry points. Select the subsystem's KUnit configuration and
inspect the resulting KTAP and kernel log when exercising kernel glue.
Runtime qualification and a passing host suite are separate evidence.

[StrataFS test hooks](<~kernel/development/native-subsystems/stratafs-test-hooks>)
documents its gated securityfs fault-injection interface.

## Maintaining the reference

The kernel owns both the native interface reference and its generators.
Regenerate the ABI and constants pages from the kernel root:

```sh
python3 tools/docs/peios-reference/generate.py
python3 tools/docs/peios-reference/generate.py --check
```

Edit handwritten explanations directly in `docs/`; do not put them in generated
pages. See [Maintaining native subsystem documentation](<~kernel/development/native-subsystems/documentation>)
for provenance, claim anchors and the retained TRM.
