---
title: "Building and administering the Peios kernel"
type: guide
description: "Repository build entry points, configuration, artifacts and diagnostic guidance."
---

<a id="rst-linux-kernel-release-6-x-http-kernel-org"></a>
<a id="rst-readme"></a>

This repository contains the Peios kernel based on Linux 7.0.9. Its supported
build entry points, configuration and security model differ from a generic
Linux installation. Start with [Building Peios](<~kernel/development/start-here/building-peios>)
and [Peios kernel behaviour](<~kernel/introduction/peios-behaviour>).

<a id="rst-what-is-linux"></a>

## Relationship to Linux

Peios retains Linux kernel infrastructure and interfaces while adding native
security and system services. Its source includes upstream drivers and
architectures that are not necessarily enabled or qualified by the Peios
configuration. The repository's `COPYING` and per-file licenses govern the
source; see the licensing documentation for their interpretation.

<a id="rst-on-what-hardware-does-it-run"></a>

## Build target and hardware

The repository's configured build targets x86_64. Source support for another
architecture, or a driver appearing in this documentation, is not evidence
of Peios runtime or hardware qualification.

<a id="rst-documentation"></a>

## Documentation

`docs/` is the authoritative human-readable documentation tree. `Documentation/`
retains tooling inputs such as schemas and ABI data used by generators.
Generated references and inherited subsystem guides supplement the Peios
behavior and build guides; they do not override the configured native policy.

<a id="rst-installing-the-kernel-source"></a>

## Source and upstream updates

Build the Peios repository checkout. An upstream Linux tarball does not contain
the Peios changes. Upstream updates require integrating and reviewing code,
configuration and mapped documentation changes together; blindly applying a
version patch is not a Peios upgrade procedure.

<a id="rst-software-requirements"></a>

## Build prerequisites

Follow the pinned image, Bazel launcher and host requirements in
[Building Peios](<~kernel/development/start-here/building-peios>). The controlled
build uses its declared LLVM/Rust toolchain, not whichever GCC happens to be
installed on the host. Package-tool compilation has separate host requirements.

<a id="rst-build-directory-for-the-kernel"></a>

## Build directories

Controlled builds use a private source copy and an out-of-tree Kbuild output
directory. Incremental development builds keep state under `.peios-dev/`.
Do not run `make mrproper` in the working checkout as a routine preparation
step. The build guide describes output locations and provenance reports.

<a id="rst-configuring-the-kernel"></a>

## Configuration

The base configuration, `peios/config/pkm.fragment` and optional KUnit fragment
are merged by the build. `peios/verify-config.sh` checks required invariants.
A menuconfig session, generic defconfig or arbitrary local module selection
does not establish equivalent security policy. Make intended configuration
changes in the repository inputs and validate the resulting build.

The [Kconfig reference](<~kernel/development/kbuild/kconfig>) describes the
underlying configuration machinery.

<a id="rst-compiling-the-kernel"></a>

## Compilation and artifacts

From the kernel repository root:

```sh
./peios/bazel build //:kernel
./peios/bazel test //:kunit
```

These are separate build and test actions. Successful compilation does not
establish runtime qualification. Development outputs include unsigned modules
even though the kernel enforces module signatures; signing and release
publication remain separate stages. The build does not install a kernel onto
the host. A generic `sudo make install` or `make modules_install` command is
not the repository's Peios deployment workflow.

<a id="rst-legacy-lilo-instructions"></a>

## Deployment boundary

The historical LILO commands attached to this anchor have been retired from
the Peios guide. Deploy a matching, signed and qualified kernel/module set
through the applicable Peios release or qualification workflow. Preserve the
artifact provenance and a recovery path when changing a boot environment.
The repository build alone is not a release or installation action.

<a id="rst-if-something-goes-wrong"></a>

## Diagnostics

Record the kernel commit, resolved configuration, build provenance, boot
arguments and complete failure logs. Distinguish a build failure, signature or
authorization refusal, missing runtime prerequisite and kernel fault before
changing configuration to work around it.

The [bug-hunting guide](<~kernel/administration/admin-guide/diagnostics/bug-hunting>)
and [GDB debugging reference](<~kernel/development/process/debugging/gdb-kernel-debugging>)
describe useful mechanisms. Their availability still depends on the Peios
configuration, lockdown policy and native authorization.
