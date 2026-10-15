# Shared-source kernel core tests

The kernel repository owns these crates. Kbuild and Cargo compile the same
semantic files under `security/pkm`; nothing is copied or rewritten at build
time. Small `lib.rs` entry points adapt their module layout to the existing
Cargo crate APIs. Change core behaviour in `security/pkm`, and its tests here.

The workspace contains `kacs-core`, `lcs-core`, `pnp-core`, `stratafs-core`,
the `ntfe` userspace library and raw `peios-uapi` bindings. `ORIGIN.json` records
the PKM revision used for the migration. No PKM checkout is needed.

```sh
# From the kernel root: all tests, then selected Clippy correctness checks.
./peios/bazel test //:rust-core-tests //:uapi-tests

# Or work on one crate directly.
cd peios/rust
cargo test -p kacs-core --locked --offline
cargo test --workspace --locked --offline
bash check.sh
```

The host test toolchain is pinned to Rust 1.98.1 in `rust-toolchain.toml`.
Install it with rustfmt and Clippy first. This does not change the kernel's
Rust 1.83.0 build toolchain. The workspace has only local path dependencies;
Cargo tests are offline after toolchain installation. Bazel places Cargo output
in its test scratch directory; direct Cargo uses the ignored `target/` directory.

The Cargo workspace tests the userspace allocation implementation. The `kernel`
configuration is supplied by Kbuild, which has the kernel allocation/runtime
dependencies. Do not use Cargo `--all-features` to simulate a kernel build.
Run the normal kernel build and KUnit commands to exercise that integration.

## ABI regeneration

The source ABI headers live in `include/uapi/pkm`. The generated constants at
`security/pkm/kacs/peios_uapi.rs` are shared directly by Cargo and Kbuild.
Generated types and their layout tests live at `peios-uapi/ztypes.rs`.

```sh
bash peios/rust/peios-uapi/check-codegen-safe.sh
bash peios/rust/peios-uapi/check-userspace-clean.sh
LIBCLANG_PATH=/path/to/libclang BINDGEN=/path/to/bindgen-0.65.1 \
    bash peios/rust/peios-uapi/gen.sh --check
```

Run these from the kernel root. Omit `--check` to regenerate. The generator
requires bindgen 0.65.1 (also supplied by the kernel build image), libclang, a C
compiler with userspace Linux headers, and rustfmt 1.98.1. It targets Rust 1.64
syntax for generated layouts, preserving the existing runtime layout tests.
The initial migration's drift check was verified with libclang 21 on x86_64.
Generator/sysroot provisioning is not part of the hosted style workflow yet;
CI does run the committed Rust layout tests and C header/ABI checks.

Core logic, public names, ABI layout and package manifests must remain stable
during style-only work. The migrated Cargo suite retained all 1,864 tests with
no ignored or failed tests at integration. Kernel and VM qualification are
separate from this host test result.
