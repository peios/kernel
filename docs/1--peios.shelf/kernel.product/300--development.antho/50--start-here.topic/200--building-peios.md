---
title: "Building Peios"
type: guide
description: "Build the kernel with pekit's pinned toolchain, and understand its outputs and trust inputs."
---

The repository builds the directly maintained kernel source. pekit builds it
with Kbuild in a sandbox, from a toolchain it builds from pinned sources, and
keeps every result. Run commands from the kernel repository root. The
inherited [Kbuild reference](<~kernel/development/kbuild/index>) explains the
underlying machinery.

## Host requirements

The host is **x86_64 Linux** with [pekit](<~pekit/pekit>)
installed. pekit fetches and builds everything else, pinned by digest:

- LLVM 18.1.8's release, which compiles the kernel.
- Rust 1.83.0 with its source and rustfmt, and bindgen 0.65.1.
- The host tools Kbuild runs, each built from its signed release: bison,
  flex, bc, perl, OpenSSL, elfutils, pahole, GNU's core utilities, and
  others. `tools.gcsl` lists them.
- The Bootlin GCC toolchain, which builds those tools and Kbuild's own host
  programs.

The build reads nothing from the host but the kernel it runs on. A kernel
build needs about 25 GB of RAM and 70 GB of free disk at its peak, because
the object tree holds full debug information.

## Build and test

```sh
pekit build kernel        # production configuration, development keys
pekit build kernel_kunit  # built-in QEMU/KUnit configuration
pekit run kunit           # build and boot the KUnit configuration
pekit test                # every host check
peios/check               # the contributor check
```

`peios/check` first checks that each tracked top-level entry is in the
kernel's source or left out of it on purpose, then runs `pekit test --strict`.
`pekit run kunit` and the qualification scripts boot QEMU, so they aren't
tests: run them by hand.

The kernel step is given the kernel's top-level directories and files, and
of `peios/` only the build recipe: `build.sh`, `build-settings.json`,
`generate-keys.py`, `runner.py`, `verify-config.sh`, `config/`, and `keys/`.
A change to another Peios script builds no kernel. `kernel.gcsl` lists the
entries.

The step copies the source into its sandbox and runs `peios/build.sh` with
a separate `O=` directory. It has no network, receives no private signing
keys, and uses a fixed build identity, timestamp, and debug paths. No
generated header or `.config` is written into your source tree. The
configuration invariant checker is retained from PKM, including the ML-DSA,
lockdown, LSM, and firmware policy checks.

The kernel is one step: Kbuild's own dependency graph makes a kernel build
incremental, and a change to the source builds the kernel again from
nothing. pekit finds an unchanged kernel in its store. `pekit build
--strict` builds with nothing of the host's, and `--check-reproducible`
builds each step twice and compares the outputs.

`peios/build-settings.json` gives the build its settings. `source_date_epoch`
and `localversion` are explicit inputs; no current clock or Git state is
stamped into the kernel. The initial suffix is `-peios-dev`, not a release.

`peios/config/pkm.fragment` defines the Peios configuration. The build runs
`peios/verify-config.sh` against the resolved configuration. A generic Linux
`defconfig` doesn't establish the same Peios policy.

## Outputs and release limits

pekit prints where each build's outputs are, under `pekit-out/`. The kernel's
are `bzImage`, `vmlinux`, `System.map`, resolved `config`, `Module.symvers`,
`kernel.release`, `modules.tar`, `kbuild-support.tar`, and `build.json`. The
support archive retains generated headers, public trust inputs, and Kbuild
helper programs, for building modules against the kernel. The module archive contains raw
**unsigned** modules and module lists, preserving their Kbuild paths. It
isn't an installable package. `build.json` records the settings, the profile,
and a digest of the source's contents and modes.

The checked-in `peios/keys/dev-modsig.pem` certificate and
`peios/keys/dev-tcb.hex` public key preserve the old PKM development keyring
for production-configuration development builds. KUnit uses the public
certificate in `peios/keys/kunit-modsig.pem` and an empty built-in TCB table,
matching that existing test path. These are **development trust roots**, not
release credentials. Substituting release public inputs and choosing release
versions belong to release setup. Module signature enforcement remains
enabled even though this build stage doesn't sign the modules it produces.

## Next steps

- [KUnit execution](<~kernel/development/native-subsystems/kunit>) explains
  logs, filters, and completion checks.
- [Guest qualification](<~kernel/development/native-subsystems/guest-qualification>)
  exercises native syscalls, mounted filesystems, and signed inputs.
- [Style tooling](<~kernel/development/build-tools/style>) and
  [shared Rust core tests](<~kernel/development/native-subsystems/rust-tests>)
  cover host checks.
- [Data generators](<~kernel/development/build-tools/generators>) covers
  event tables, registry seed data, Unicode tables, and test fixtures.
