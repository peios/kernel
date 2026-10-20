---
title: "Guest qualification"
type: guide
description: "Run native syscall, filesystem and signature harnesses with explicit kernel and fixture inputs."
---

The harnesses in `peios/qualification/` build small initramfs guests and boot
a supplied kernel. They do not build that kernel or qualify an entire OS release.
Use an x86_64 Linux host with `gcc`, static libc development files, `cpio`,
`timeout` and `qemu-system-x86_64`; firmware fixture preparation also needs `zstd`.
QEMU uses KVM when available, with TCG fallback. The harnesses run on the host,
outside the pinned kernel build container.

Run the Bazel commands below from the kernel repository root. Their underlying
scripts locate the guest C sources relative to themselves and can also be called
directly from another working directory with absolute input paths.

## Compile the guest programs

```sh
./peios/bazel test //:qualification-build-test
```

This compiles all guest C programs with static linking and warnings as errors.
It does not boot a VM or require signing keys. A passing compilation is separate
from a passing guest run.

## Mount namespaces and StrataFS

```sh
./peios/bazel run //:qualify-mntns -- /path/to/bzImage
./peios/bazel run //:qualify-stratafs -- /path/to/bzImage
./peios/bazel run //:qualify-stratafs-dir-bench -- /path/to/bzImage
```

Each accepts a direct image, including `bazel-bin/kernel/bzImage`, or a Kbuild
output tree containing `arch/x86/boot/bzImage`. Supply a kernel with the relevant
Peios subsystem and the guest's required filesystem support enabled. A script
finding the image does not establish that the configuration meets its needs.

The mount-namespace harness exercises KACS objects through syscalls and checks
both child and parent results. The StrataFS smoke harness exercises a mounted
filesystem. The directory benchmark validates its expected result rows and
completion marker; retain those rows when comparing performance. All three
reject their failure markers, kernel warnings and fatal diagnostics, and require
successful QEMU exit.

## Module signatures

```sh
./peios/bazel run //:qualify-modsig -- /path/to/kbuild-output /path/to/modules-root
```

The first directory must contain `arch/x86/boot/bzImage`. The second must contain
one matching release under `lib/modules/`, with `modules.dep` and signed,
zstd-compressed modules trusted by the kernel. The harness selects a
dependency-free module, boots with a copy of it and a corrupted copy, and
requires the valid module to load and the corrupted one to be rejected.

The flat `bazel-bin/kernel/` directory is not the required Kbuild layout, and its
`modules.tar` contains unsigned modules. Prepare the output layout and separately
signed module tree before invoking this harness. Confirm signature enforcement
in the supplied kernel configuration; a load alone is not evidence of enforcement
when testing a differently configured kernel.

## Firmware signatures

The kernel needs its firmware verification policy and `CONFIG_TEST_FIRMWARE=m`.
The matching module tree must contain a trusted, signed `test_firmware.ko.zst`.
Prepare fixtures in a new, existing output directory:

```sh
mkdir /path/to/fixtures
bash peios/qualification/prepare-fwsig.sh \
    /path/to/kbuild-output /path/to/modules-root /path/to/fixtures
```

Preparation compiles `root/init`, copies the firmware test module, and creates
good, unsigned, tampered and compressed firmware payloads under `root/lib/firmware/`.
It does not sign anything. Have the signing coordinator provide detached Peios
signatures trusted by this kernel at:

- `root/lib/firmware/fwsig-good.bin.peios.sig`
- `root/lib/firmware/fwsig-goodz.bin.zst.peios.sig`

Preserve the prepared directory as a whole, including its signed test module.
The guest reuses the good signature when testing tampered bytes. No private
signing key is passed to the harness. Once the fixtures are signed:

```sh
./peios/bazel run //:qualify-fwsig -- \
    /path/to/kbuild-output /path/to/modules-root /path/to/fixtures
```

The harness boots once with `kacs_fwsig=enforce` and once with `kacs_fwsig=log`.
It requires four guest checks per mode, the appropriate refusal or log verdict,
no listed fatal diagnostics, and successful QEMU exit. The expected policy
warnings are part of the test, so this harness does not reject every warning.

## Logs and timeouts

Set `QEMU_BIN` to choose another QEMU executable. The retained `PKM_*` names are
the current script interfaces. Timeout values are in seconds.

| Harness | Default log | Log override | Timeout override (default) |
| --- | --- | --- | --- |
| Mount namespaces | `mntns-qemu.log` | `PKM_MNTNS_LOG` | `PKM_MNTNS_TIMEOUT` (120) |
| StrataFS smoke | `stratafs-qemu.log` | `PKM_STRATAFS_LOG` | `PKM_STRATAFS_TIMEOUT` (120) |
| Directory benchmark | `stratafs-dir-bench-qemu.log` | `PKM_STRATAFS_DIR_BENCH_LOG` | `PKM_STRATAFS_DIR_BENCH_TIMEOUT` (1200) |
| Module signatures | `modsig-qemu.log` | `PKM_MODSIG_LOG` | `PKM_MODSIG_TIMEOUT` (120) |
| Firmware signatures | `fwsig-enforce-qemu.log`, `fwsig-log-qemu.log` | `PKM_FWSIG_LOGDIR` | `PKM_FWSIG_TIMEOUT` (120 per boot) |

Logs default to the supplied tree, or beside the direct image where that input
form is supported. Ensure the chosen log directory exists and is writable.
Use distinct log paths for concurrent runs. Temporary initramfs trees are removed
on exit; retain serial logs, kernel revision/configuration, module provenance and
fixture identity as the evidence for a qualification run.
