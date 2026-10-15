# Building the Peios kernel

This repository builds the directly edited Linux source with Kbuild. Bazel
provides the entry points, declared inputs and whole-kernel build caching.
Package assembly consumes those build outputs. Module signing and release
publication remain separate stages.

The Peios kernel fork is maintained by
[Jack Palfrey](mailto:jackgpalfrey@outlook.com). The `PEIOS KERNEL EXTENSIONS`
entry in [MAINTAINERS](../MAINTAINERS) lists the Peios-specific code and build
machinery covered by this maintainership.

## Host and toolchain

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
Registry distribution is not set up yet. `Containerfile` and
`original-toolchain.lock` preserve the inherited image recipe for reference;
rebuilding it does not promise the same content ID. Changing the selected
image is an explicit toolchain update in `build-settings.json`.

Packaging uses an unchanged snapshot of the current `ppknew` writer under
`peios/vendor/ppk/`, with its Cargo lockfile. Bazel downloads the pinned Rust
1.96.0 toolchain and locked crates for this host tool, independently of the
kernel's Rust compiler. Its native zstd dependency uses Bazel's detected host
C toolchain, so packaging also requires a host C compiler and linker. Initial
dependency fetching needs network access; package actions themselves do not.

## Commands

```sh
./peios/bazel build //:kernel                 # production configuration, development keys
./peios/bazel build //:kernel-kunit           # built-in QEMU/KUnit configuration
./peios/bazel test //:kunit                   # build then boot KUnit; retain serial log
./peios/bazel run //:kernel-dev               # persistent production Kbuild state
./peios/bazel run //:kernel-dev -- --profile kunit
./peios/bazel build //:kernel-tools           # Debian-development userspace tools
./peios/bazel build //:kernel-package-content # intermediate kernel package file trees
./peios/bazel build //:packages               # all 42 packages, one deduplicated store
./peios/bazel build //peios/packages:perf      # one userspace package
./peios/bazel build //peios/packages:kernel-source # source only; no kernel compilation
./peios/bazel test //peios/packages:assembly-test //peios/packages:store-test //peios/vendor/ppk:commit-test
./peios/bazel test //peios/packages/tests:tree-input-test
./peios/bazel test //peios/packages:stage-test
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

## Outputs and trust material

Controlled outputs are in `bazel-bin/kernel/` or `bazel-bin/kernel-kunit/`:
`bzImage`, `vmlinux`, `System.map`, resolved `config`, `Module.symvers`,
`kernel.release`, `modules.tar`, `kbuild-support.tar` and `build.json`.
The support archive retains generated headers, public trust inputs and Kbuild
helper programs for package assembly. The module archive contains
raw **unsigned** modules and module lists, preserving their Kbuild paths.
It is not an installable package. `build.json` records the image, settings,
profile, build mode and a digest of the declared input contents and modes.

The checked-in `keys/dev-modsig.pem` certificate and `keys/dev-tcb.hex` public
key preserve the old PKM development keyring for production-configuration
development builds. KUnit uses the old `kunit.keyring.pekit.toml` public
certificate and an empty built-in TCB table, matching that existing test path.
These are **development trust roots**, not release credentials. Substituting
release public inputs and choosing release versions belong to release setup.
Module signature enforcement remains enabled even though this build stage
does not sign the modules it produces.

## Packages

The package family contains PKM's 41 binary packages plus
`dev.peios.kernel-source`. `peios/packages/legacy/` preserves the
original recipes and their metadata, and `data/` preserves the registration
files and PKM license text they install.

`kernel-tools` produces a `root/` staging tree and provenance under
`bazel-bin/kernel-tools/`. These tools use the pinned **Debian** image's
userspace ABI, including its Python ABI; they are development outputs, not
Peios-native release binaries.

`kernel-package-content` consumes the controlled kernel output and prepares
the kernel, module, initramfs-module, UAPI-header, development-kit and debug
trees. It preserves PKM's initramfs membership and dependency-closure checks.
Module payloads remain unsigned. `assembly.py` checks the inherited mappings,
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

## Tests

`bazel test //:kunit` uses QEMU from the pinned image and the existing PKM runner.
It uses KVM when `/dev/kvm` is available, otherwise TCG. The test requires
complete KTAP accounting, passing PKM suites, clean power-down and no kernel
warning/oops/lockdep failure signatures. Its result is rerun on every test
invocation. Serial output is retained under
`bazel-testlogs/kunit/test.outputs/`. Native integration and hardware
qualification remain additional checks.

The migrated configs, verifier, key generator and KUnit runner come from PKM
commit `ac4c6eb57ff94821f1eaea2b3bde460777d48f5b`. No dependency on the old PKM
checkout is needed to run these commands.

## Style and Rust core tests

Run `./peios/bazel test //:style //peios/style:tests` to check the scoped style
profile, and `./peios/bazel run //:format` to apply it. First install the pinned
local tooling as described in [the style command guide](style/README.md).

The [Cargo workspace](rust/README.md) tests the same semantic core source used
by Kbuild: `./peios/bazel test //:rust-core-tests //:uapi-tests`. It also retains
the NTFE userspace crate and generated ABI layout tests. No PKM checkout is
required. Cargo tests complement kernel compilation and KUnit.
