---
title: "Shared Rust core tests"
type: guide
description: "Test the semantic source shared by Cargo and Kbuild without duplicating implementations."
---

The kernel repository owns these crates. Kbuild and Cargo compile the same
semantic files under `security/pkm`; nothing is copied or rewritten at build
time. Small `lib.rs` entry points adapt their module layout to the existing
Cargo crate APIs. Change core behaviour in `security/pkm`, and its tests in `peios/rust/`.

The workspace contains `kacs-core`, `lcs-core`, `pnp-core`, `stratafs-core`,
the `ntfe` userspace library and raw `peios-uapi` bindings. `peios/rust/ORIGIN.json` records
the PKM revision used for the migration. No PKM checkout is needed.

```sh
# From the kernel root: all tests, then selected Clippy correctness checks.
pekit test rust_cores rust_clippy uapi

# Or work on one crate directly.
cd peios/rust
cargo test -p kacs-core --locked --offline
cargo test --workspace --locked --offline
bash check.sh
```

The host test toolchain is pinned to Rust 1.98.1 in `peios/rust/rust-toolchain.toml`.
Install it with rustfmt and Clippy first. This does not change the kernel's
Rust 1.83.0 build toolchain. The workspace has only local path dependencies;
Cargo tests are offline after toolchain installation. pekit builds the crates
in its sandbox, with its own pinned Rust 1.98.1, each crate given
`security/pkm` where its `#[path]` reaches. Direct Cargo uses the ignored
`peios/rust/target/` directory.

The Cargo workspace tests the userspace allocation implementation. The `kernel`
configuration is supplied by Kbuild, which has the kernel allocation/runtime
dependencies. Do not use Cargo `--all-features` to simulate a kernel build.
Run the normal kernel build and KUnit commands to exercise that integration.

For header changes, follow [ABI regeneration](<~kernel/development/native-subsystems/abi-generation>).
For kernel execution, use [KUnit](<~kernel/development/native-subsystems/kunit>)
and [guest qualification](<~kernel/development/native-subsystems/guest-qualification>).
