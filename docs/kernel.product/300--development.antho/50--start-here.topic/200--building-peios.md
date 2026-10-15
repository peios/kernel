---
title: "Building Peios"
type: guide
description: "Set up the pinned toolchain, build the kernel and understand outputs and trust inputs."
---

The repository builds the directly maintained kernel source. Bazel declares
inputs, invokes Kbuild and caches complete build outputs. Run commands from
the kernel repository root. The inherited [Kbuild reference](<~kernel/development/kbuild/index>)
explains the underlying machinery.

## Host requirements

The initial host is **x86_64 Linux** with Python 3.11 or newer at `/usr/bin/python3`, Docker
at `/usr/bin/docker`, and access to the local `/var/run/docker.sock` daemon.
Use `./peios/bazel` to download and run Bazel **8.4.2**, pinned in `.bazelversion`.
The launcher requires `curl` and `sha256sum`, verifies the binary, and caches
it under `${XDG_CACHE_HOME:-$HOME/.cache}/peios/bazel/`. Alternatively use an
installed Bazel 8.4.2 or Bazelisk (which honours `.bazelversion`).
The upstream Linux x86_64 binary has SHA-256:

```
4dc8e99dfa802e252dac176d08201fd15c542ae78c448c8a89974b6f387c282c
```

`peios/build-settings.json` pins the existing PKM build image by its content ID,
with LLVM 18, Rust 1.83.0 and bindgen 0.65.1. The image must already exist in
the local daemon. Builds fail if it is missing; they do not pull a mutable tag
or choose host compilers. To transfer the existing image to another machine,
use `docker save` and `docker load`, then verify its ID against the settings.
Registry distribution is not set up yet. `peios/Containerfile` and
`peios/original-toolchain.lock` preserve the inherited image recipe for reference;
rebuilding it does not promise the same content ID. Changing the selected
image is an explicit toolchain update in `peios/build-settings.json`.

## Build and test

```sh
./peios/bazel build //:kernel       # production configuration, development keys
./peios/bazel build //:kernel-kunit # built-in QEMU/KUnit configuration
./peios/bazel test //:kunit         # build and boot the KUnit configuration
./peios/bazel run //:kernel-dev
./peios/bazel run //:kernel-dev -- --profile kunit
```

The controlled build declares all kernel source, configuration, public-key
and recipe files as inputs. It copies them into a fresh private tree and runs
Kbuild with a separate `O=` directory. The container has no network, receives
no private signing keys, and uses fixed build identity, timestamp and debug
paths. No generated header or `.config` is written into your source tree.
The configuration invariant checker is retained from PKM, including the
ML-DSA, lockdown, LSM and firmware policy checks.

Kbuild, staging and payload-assembly actions run locally outside Bazel's
filesystem sandbox. Assembly reads the declared staging trees directly so
Bazel's input-transport symlinks cannot become package contents. Bazel caches
complete outputs; remote execution is not supported. The image is pinned,
but this is not yet a fully hermetic Bazel toolchain: host Python/Docker and
the host kernel remain execution prerequisites. Remote caching is supported
by the action but no shared cache is configured or qualified here.

Bazel's local action cache reuses unchanged outputs. To retain outputs across
input revisions or clean output directories, opt into a disk cache with
`./peios/bazel build --disk_cache=/absolute/path/to/cache //:kernel-kunit`
(or `//:kernel`). Use the same cache path on subsequent builds. No disk-cache
location is enabled by default.

`kernel-dev` deliberately runs outside the Bazel action cache. It keeps private
source copies, object files and artifacts under `.peios-dev/<profile>/`.
Content changes and deleted inputs are synchronised before Kbuild runs; equal
inputs retain their timestamps. Each profile is locked against concurrent
writers. An image change discards that profile's objects. Remove that profile
directory while no build is running to start fresh. These artifacts are marked
`mode: dev`; release automation should consume controlled build outputs.

Both modes read the same settings. `jobs` caps Kbuild parallelism (initially
four), independently of Bazel's action parallelism. `source_date_epoch` and
`localversion` are explicit inputs; no current clock or Git dirty state is
stamped into the kernel. The initial suffix is `-peios-dev`, not a release.

`peios/config/pkm.fragment` defines the Peios configuration. The build runs
`peios/verify-config.sh` against the resolved configuration. A generic Linux
`defconfig` does not establish the same Peios policy.

## Outputs and release limits

Controlled outputs are in `bazel-bin/kernel/` or `bazel-bin/kernel-kunit/`:
`bzImage`, `vmlinux`, `System.map`, resolved `config`, `Module.symvers`,
`kernel.release`, `modules.tar`, `kbuild-support.tar` and `build.json`.
The support archive retains generated headers, public trust inputs and Kbuild
helper programs for package assembly. The module archive contains
raw **unsigned** modules and module lists, preserving their Kbuild paths.
It is not an installable package. `build.json` records the image, settings,
profile, build mode and a digest of the declared input contents and modes.

The checked-in `peios/keys/dev-modsig.pem` certificate and `peios/keys/dev-tcb.hex` public
key preserve the old PKM development keyring for production-configuration
development builds. KUnit uses the public certificate in `peios/keys/kunit-modsig.pem` and an empty built-in TCB table, matching that existing test path.
These are **development trust roots**, not release credentials. Substituting
release public inputs and choosing release versions belong to release setup.
Module signature enforcement remains enabled even though this build stage
does not sign the modules it produces.

## Next steps

- [Package assembly](<~kernel/development/build-tools/packages>) covers userspace
  tools, package stores, provenance and release limits.
- [KUnit execution](<~kernel/development/native-subsystems/kunit>) explains logs,
  filters and completion checks.
- [Guest qualification](<~kernel/development/native-subsystems/guest-qualification>)
  exercises native syscalls, mounted filesystems and signed inputs.
- [Style tooling](<~kernel/development/build-tools/style>) and
  [shared Rust core tests](<~kernel/development/native-subsystems/rust-tests>)
  cover host checks.
- [Data generators](<~kernel/development/build-tools/generators>) covers event
  tables, registry seed data, Unicode tables and test fixtures.
