---
title: "Package assembly"
type: guide
description: "Build kernel packages and userspace tools, inspect their stores and understand development limits."
---

Package assembly consumes controlled outputs from [Building Peios](<~kernel/development/start-here/building-peios>).
Run these commands from the kernel repository root.

## Additional host requirements

Packaging uses an unchanged snapshot of the current `ppknew` writer under
`peios/vendor/ppk/`, with its Cargo lockfile. Bazel downloads the pinned Rust
1.96.0 toolchain and locked crates for this host tool, independently of the
kernel's Rust compiler. Its native zstd dependency uses Bazel's detected host
C toolchain, so packaging also requires a host C compiler and linker. Initial
dependency fetching needs network access; package actions themselves do not.

## Build commands

```sh
./peios/bazel build //:kernel-tools
./peios/bazel build //:kernel-package-content
./peios/bazel build //:packages
./peios/bazel build //peios/packages:perf
./peios/bazel build //peios/packages:kernel-source
```

## Outputs and package identity

The package family contains PKM's 41 binary packages plus
`dev.peios.kernel-source`. `peios/packages/legacy/` preserves the
original recipes and their metadata, and `peios/packages/data/` preserves the registration
files and PKM license text they install.

`kernel-tools` produces a `root/` staging tree and provenance under
`bazel-bin/kernel-tools/`. These tools use the pinned **Debian** image's
userspace ABI, including its Python ABI; they are development outputs, not
Peios-native release binaries.

`kernel-package-content` consumes the controlled kernel output and prepares
the kernel, module, initramfs-module, UAPI-header, development-kit and debug
trees. It preserves PKM's initramfs membership and dependency-closure checks.
Module payloads remain unsigned. `peios/packages/assembly.py` checks the inherited mappings,
exclusions and destination collisions before a payload is passed to a packer.

Each binary package has a target `//peios/packages:<short-name>`; for example,
`kernel`, `kernel-modules`, `kernel-devel`, `kernel-headers`, `perf`, `bpftool`
and `python3-perf`. Use `./peios/bazel query 'kind(kernel_package, //peios/packages:*)'`
to list all 42. Individual targets build only their required stages. Building
the family shares a single kernel build and a single userspace-tools build.

The default package version is `0.0.0-dev`. Set independent package versions
in `peios/packages/versions.bzl`; an override changes the package identity
without recompiling the kernel. The actual compiled kernel release, initially
`7.0.9-peios-dev`, determines module installation paths independently of the
package version. Existing `noarch` distinctions are preserved.

Individual stores are under `bazel-bin/peios/packages/<short-name>.ppk/`.
`//:packages` combines them into `bazel-bin/packages/`:

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
trees and Bazel outputs. It materialises source links in the same way as the
controlled build's source staging. It does not bundle the Docker image or
downloaded compiler/crate dependencies. `kernel-debugsource` retains the
inherited vmlinux debug-source selection; the complete source package also
provides the rest of the source tree.

These remain **Debian-based development packages**. Their provenance says
`release_ready: false`; modules are unsigned and module-signature enforcement
is unchanged. Packaging is not native runtime qualification, signing or release
publication. No package is installed by a build command.

The writer produces deterministic blobs/manifests for a given payload. Full
userspace compilation reproducibility is not yet qualified: clean perf builds
have produced differing read-only data and build IDs; the cause is unresolved.
Pinning the image and caching outputs does not establish that every rebuild
is byte-identical.

## Assembly checks

```sh
./peios/bazel test //peios/packages:assembly-test //peios/packages:store-test //peios/vendor/ppk:commit-test
./peios/bazel test //peios/packages/tests:tree-input-test
./peios/bazel test //peios/packages:stage-test
```

These checks cover assembly and store handling. Use
[guest qualification](<~kernel/development/native-subsystems/guest-qualification>)
for runtime behaviour; package construction alone does not qualify a release.
