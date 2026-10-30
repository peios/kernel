---
title: "Package assembly"
type: guide
description: "Build the kernel's packages, inspect their stores and understand development limits."
---

Package assembly consumes controlled outputs from [Building Peios](<~kernel/development/start-here/building-peios>).
Run these commands from the kernel repository root.

## The writer

Packaging uses an unchanged snapshot of the current `ppknew` writer under
`peios/vendor/ppk/`, with its Cargo lockfile. pekit builds it, and the store
checker in `peios/packages/check-blobs/`, with the rust library's pinned
Rust and the crates their locks pin, independently of the kernel's Rust
compiler.

## Build commands

```sh
pekit build kernel_content         # the kernel's package file trees
pekit build packages               # the package family's merged store
pekit build kernel_source_package  # dev.peios.kernel-source alone
```

## Outputs and package identity

The family pekit builds holds the kernel's seven binary packages, `kernel`,
`kernel-modules`, `kernel-modules-irf`, `kernel-devel`, `kernel-headers`,
`kernel-debuginfo`, and `kernel-debugsource`, plus `dev.peios.kernel-source`.
`peios/packages/legacy/` preserves PKM's recipes for all 41 binary packages
and their metadata, and `peios/packages/data/` preserves the registration
files and PKM license text they install. The userspace tools' packages, such
as `perf` and `bpftool`, and `kernel-tools-debuginfo` aren't built yet: their
tools need a pinned build of their own.

`kernel_content` consumes the kernel's outputs and prepares
the kernel, module, initramfs-module, UAPI-header, development-kit and debug
trees. It preserves PKM's initramfs membership and dependency-closure checks.
Module payloads remain unsigned. `peios/packages/assembly.py` checks the inherited mappings,
exclusions and destination collisions before a payload is passed to a packer.

`packages.gcsl` lists the packages. Building the family shares a single
kernel build, and each package is committed in a step of its own.

Every package's version is `0.0.0-dev`, `PACKAGE_VERSION` in `packages.gcsl`.
A version changes the package identity without recompiling the kernel. The actual compiled kernel release, initially
`7.0.9-peios-dev`, determines module installation paths independently of the
package version. Existing `noarch` distinctions are preserved.

`packages` combines the packages' stores into one:

```
blobs/sha256/<uncompressed-content-sha256>.zst
manifests/<name>/<version>/<arch>/manifest.toml
index.json
```

The manifest is exactly the current `ppknew` format: name, version, arch and
sorted file entries recording blobs, executable flags, symlinks and empty
directories. Each file blob uses zstd; its identity hashes the uncompressed
bytes. The package identity hashes the canonical manifest bytes. The aggregate
deduplicates shared blobs, checks manifest identities and references, and
decompresses every distinct blob to verify its SHA-256 before succeeding.

`index.json` records package identities and development provenance outside
the canonical format. Individual stores carry equivalent `provenance.json`
files. These are build reports, not signed repository metadata. Legacy
dependencies, virtual provides, licenses and install actions remain in the
recipes; the current canonical format cannot express those relationships,
and these targets do not resolve dependencies or apply installation actions.

The source package contains the declared Linux/Peios sources, public trust
inputs, build and package recipes, writer snapshot and dependency lockfiles
under `usr/src/peios-kernel/`. It excludes Git history, private keys, object
trees and build outputs. It holds pekit's build files too. It materialises source links in the same way as the
controlled build's source staging. It doesn't bundle the toolchain or
the downloaded crates. `kernel-debugsource` retains the
inherited vmlinux debug-source selection; the complete source package also
provides the rest of the source tree.

These remain **development packages**. Their provenance says
`release_ready: false`; modules are unsigned and module-signature enforcement
is unchanged. Packaging is not native runtime qualification, signing or release
publication. No package is installed by a build command.

The writer produces deterministic blobs and manifests for a given payload,
and `pekit build --check-reproducible packages` checks that every step
gives the same outputs again.

## Assembly checks

```sh
pekit test package_assembly package_store ppk_commit package_tree_input package_stage
```

These checks cover assembly and store handling. Use
[guest qualification](<~kernel/development/native-subsystems/guest-qualification>)
for runtime behaviour; package construction alone does not qualify a release.
