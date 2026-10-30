---
title: "Running KUnit"
type: guide
description: "Build and boot KUnit, preserve serial logs and distinguish complete runs from partial output."
---

From the kernel repository root:

```sh
pekit run kunit
```

`pekit run kunit` builds the KUnit configuration's kernel with the pinned
toolchain, then boots it with the existing PKM runner and the host's QEMU,
`qemu-system-x86_64`. It's a script you run by hand, not a test, because it
needs QEMU and wants KVM. It uses KVM when `/dev/kvm` is available, otherwise
TCG. The run requires complete KTAP accounting, passing PKM suites, clean
power-down and no kernel warning/oops/lockdep failure signatures. The serial
log is `kunit-qemu.log` beside the image, as the direct runner writes it, or
where `PKM_KUNIT_LOG` says. Native integration and hardware qualification
remain additional checks.

The migrated configs, verifier, key generator and KUnit runner come from PKM
commit `ac4c6eb57ff94821f1eaea2b3bde460777d48f5b`. No dependency on the old PKM
checkout is needed to run these commands.

## Run an existing kernel directly

The direct runner accepts either a `bzImage` or a Kbuild output tree containing
`arch/x86/boot/bzImage`. It uses host QEMU and `timeout`, as `pekit run kunit` does.

```sh
bash peios/test-kunit.sh /path/to/bzImage
```

The direct runner supports these environment variables:

| Variable | Meaning | Default |
| --- | --- | --- |
| `QEMU_BIN` | QEMU executable | `qemu-system-x86_64` |
| `PKM_KUNIT_TIMEOUT` | Boot timeout in seconds | `420` |
| `PKM_KUNIT_LOG` | Serial log path | `kunit-qemu.log` beside the image, or in the supplied tree |
| `PKM_KUNIT_INITRD` | Optional initramfs | None |
| `PKM_KUNIT_FILTER` | KUnit filter glob | Full configured run |

Set overrides in the environment of either command.

## What a pass means

The runner requires successful QEMU exit, the clean power-down marker, a
top-level KTAP plan, exactly the planned number of results and the final
successful result. It rejects failure, warning, oops and lockdep signatures.
An unfiltered run additionally requires the PKM smoke marker and a passing
PKM suite summary. A filtered run instead requires actual selected case results.

A selected passing suite is evidence for that selection, not a full suite run.
Retain the serial log with the kernel revision and configuration used.

The host-side parser and runner regression tests can be run without booting:

```sh
pekit test kunit_runner
```
