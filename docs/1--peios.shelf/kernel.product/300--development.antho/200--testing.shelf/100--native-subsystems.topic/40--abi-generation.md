---
title: "ABI regeneration"
type: guide
description: "Regenerate native Rust bindings and check C and Rust layouts against kernel UAPI headers."
---

The source ABI headers live in `include/uapi/pkm`. The generated constants at
`security/pkm/kacs/peios_uapi.rs` are shared directly by Cargo and Kbuild.
Generated types and their layout tests live at `peios/rust/peios-uapi/ztypes.rs`.

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

The ABI generator updates compiled bindings and tests. It is separate from
`tools/docs/peios-reference/generate.py`, which updates the documentation's
ABI tables. When changing an interface, review the caller contract and both
generated representations; see [Maintaining native subsystem documentation](<~kernel/development/native-subsystems/documentation>).
