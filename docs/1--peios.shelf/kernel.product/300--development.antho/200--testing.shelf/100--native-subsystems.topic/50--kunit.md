---
title: "Running KUnit"
type: guide
description: "Build and boot KUnit, preserve serial logs and distinguish complete runs from partial output."
---

From the kernel repository root:

```sh
./peios/bazel test //:kunit
```

`./peios/bazel test //:kunit` uses QEMU from the pinned image and the existing PKM runner.
It uses KVM when `/dev/kvm` is available, otherwise TCG. The test requires
complete KTAP accounting, passing PKM suites, clean power-down and no kernel
warning/oops/lockdep failure signatures. Its result is rerun on every test
invocation. Serial output is retained under
`bazel-testlogs/kunit/test.outputs/`. Native integration and hardware
qualification remain additional checks.

The migrated configs, verifier, key generator and KUnit runner come from PKM
commit `ac4c6eb57ff94821f1eaea2b3bde460777d48f5b`. No dependency on the old PKM
checkout is needed to run these commands.

## Run an existing kernel directly

The direct runner accepts either a `bzImage` or a Kbuild output tree containing
`arch/x86/boot/bzImage`. It uses host QEMU and `timeout`; this is separate from
the Bazel test, which supplies its image and output mounts through `peios/runner.py`.

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

Set overrides when calling the direct script. The Bazel wrapper does not
forward arbitrary host `PKM_KUNIT_*` variables into its container.

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
./peios/bazel test //:kunit-runner-tests
```
