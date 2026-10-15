---
title: "Building Peios"
type: guide
description: "Build and test the Peios kernel with the repository's Bazel entry points."
---

The repository builds the directly edited kernel source. Bazel declares inputs,
invokes Kbuild and caches complete build outputs. Start from the kernel
repository root. The inherited [Kbuild reference](<~kernel/development/kbuild/index>)
explains the underlying machinery; it is not the Peios release procedure.

## Host requirements

Use an x86_64 Linux host with Python 3.11 or newer at `/usr/bin/python3`, Docker
at `/usr/bin/docker`, and access to the local Docker daemon. `./peios/bazel`
downloads and verifies Bazel 8.4.2 using `curl` and `sha256sum`.

The image selected by content ID in `peios/build-settings.json` must already be
installed in the local daemon. It contains LLVM 18, Rust 1.83.0 and bindgen
0.65.1. The build does not pull a mutable image tag or substitute host compilers.
Transfer the existing image with `docker save` and `docker load` if necessary,
then verify its ID against the settings. Rebuilding the preserved container
recipe does not promise the same content ID.

Package assembly separately downloads pinned Rust 1.96.0 and locked crates for
the host package writer. It also needs a host C compiler and linker for zstd.
Initial dependency fetching needs network access; package actions do not.

## Build and test

```sh
./peios/bazel build //:kernel
./peios/bazel build //:kernel-kunit
./peios/bazel test //:kunit
./peios/bazel run //:kernel-dev
./peios/bazel run //:kernel-dev -- --profile kunit
./peios/bazel build //:kernel-tools
./peios/bazel build //:kernel-package-content
./peios/bazel build //:packages
./peios/bazel build //peios/packages:perf
./peios/bazel build //peios/packages:kernel-source
```

The controlled build uses a private source copy and a separate Kbuild `O=`
directory. It does not write `.config` or generated headers into the checkout.
Build identity, timestamp, local version and parallelism come from committed
settings. `peios/config/pkm.fragment` defines the Peios configuration;
`peios/verify-config.sh` checks its security invariants. Do not substitute a
generic `defconfig` and assume it has equivalent Peios policy.

`kernel-dev` keeps incremental state under `.peios-dev/<profile>/`. Those
artifacts are marked as development outputs and are outside Bazel's action
cache. Release automation should consume controlled outputs. Both modes use
the pinned image and settings. Actions run locally; remote execution is not
supported. Host Python, Docker and the host kernel remain prerequisites, so
pinning the container is not a claim of complete build hermeticity.

`//:kunit` boots the test build in QEMU, using KVM when available and TCG
otherwise. It requires complete KTAP accounting, passing PKM suites, a clean
power-down and no warning, oops or lockdep failure signatures. Logs are retained
under `bazel-testlogs/kunit/test.outputs/`. This does not replace native
integration or hardware qualification.

For style and native semantic-core checks:

```sh
./peios/bazel test //:style //peios/style:tests
./peios/bazel test //:rust-core-tests //:uapi-tests
```

Install the pinned style tools described in `peios/style/README.md` first.
`./peios/bazel run //:format` applies the scoped Peios formatter. Follow the
workspace `_styleguide` for Git and contribution conventions. Linux upstream
submission instructions remain useful when sending a change upstream.

KMES event catalogues live in `peios/packages/data/evman/`. Regenerate and check
their compiled tables with:

```sh
./peios/bazel run //:generate-kmes-events
./peios/bazel test //:kmes-event-table-test
```

## Outputs and release limits

Controlled kernel outputs are in `bazel-bin/kernel/` or
`bazel-bin/kernel-kunit/`: `bzImage`, `vmlinux`, `System.map`, resolved `config`,
`Module.symvers`, `kernel.release`, `modules.tar`, `kbuild-support.tar` and
`build.json`. The provenance report records the image, settings, profile,
mode and declared-input digest.

The production-configuration development build uses checked-in development
public trust roots. Its initial kernel suffix is `-peios-dev`. Modules in the
raw archive are **unsigned**, while the kernel still enforces module signatures.
Signing and release publication are separate stages.

The package family contains 41 binary packages and a source package. Individual
targets are under `//peios/packages:`, and `//:packages` combines their content
stores under `bazel-bin/packages/`. The source package contains declared source
and build inputs, not Git history, private keys, the Docker image or downloaded
compiler dependencies.

Userspace tools currently use the pinned Debian image's ABI. Package provenance
reports `release_ready: false`; these are development outputs, not qualified
Peios-native release binaries. Package assembly does not install packages or
resolve and apply their legacy dependencies and installation actions. Full
userspace build reproducibility is not yet qualified. See `peios/README.md`
and `peios/packages/` for the build recipes and package-format details.
