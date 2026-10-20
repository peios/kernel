---
title: "Firmware verification"
description: "Firmware verification: behaviour and implementation of the Peios kernel."
type: reference
---

<a id="trm-3-6-7"></a>

## Firmware verification

A firmware load is not an exec, so none of the above would see it —
and firmware is code that runs on a device with DMA into host memory,
which makes a tampered blob a complete compromise. KACS therefore
implements the `kernel_read_file` and `kernel_post_read_file` LSM
hooks for `READING_FIRMWARE` (`security/pkm/kacs/firmware.c`).

The signature is the ordinary PIP blob, found by the lookup above.
Firmware is never ELF, so in practice it is the `security.peios.sig`
xattr, which `peipkg` stamps at install from the `<file>.peios.sig`
sidecar the package carries ([PSPU payload entries](https://learn.peios.org/specifications/pspu/package-format-and-repository-protocol/payload-entries)). The bar is the **PeiosTcb**
tier — the same floor a usermodehelper exec must clear, since both are
the kernel choosing to run code it did not ship. A verified signature
at any other tier counts as no signature. <a id="cite-sig.firmware.peiostcb-floor"></a>

For a whole-file read, which is the common case, the post-read hook is
handed the exact bytes the loader will decompress and give to the
device, and those are what is hashed — no second read, no TOCTOU. <a id="cite-sig.firmware.post-read-hashes-loaded-bytes"></a> A
partial read (a driver pulling a window out of a large blob) only
passes through the pre-read hook, where nothing has been read yet, so
that path verifies the file through the reader probe instead. <a id="cite-sig.firmware.partial-read-uses-probe"></a> The
hash covers the compressed bytes as they sit on disk, so verification
precedes decompression. <a id="cite-sig.firmware.hashes-compressed-bytes"></a>

Policy is `CONFIG_SECURITY_PKM_FIRMWARE_SIG_ENFORCE`, overridable for
one boot with `kacs_fwsig=enforce` or `kacs_fwsig=log` on the kernel
command line; there is no runtime switch. <a id="cite-sig.firmware.cmdline-override"></a> Under `enforce` an unsigned,
tampered or under-tier file is refused with `-EPERM`; the loader logs
that against the path it was refused at, moves on to its remaining
search paths, and reports the driver an ordinary load failure. <a id="cite-sig.firmware.enforce-eperm"></a> Under `log` the
verdict goes to a rate-limited warning and the `kacs:kacs_firmware_load`
tracepoint and the load proceeds. <a id="cite-sig.firmware.log-mode"></a> **2026.8 ships in log mode**: the
firmware set is being signed for the first time, and a blob the
packaging missed has to show up as a warning rather than as a device
that silently stops probing. <a id="cite-sig.firmware.default-is-log"></a> Enforcement becomes the default once a
release has run clean.

`CONFIG_FW_UPLOAD` — a device's own sysfs update interface — is not
covered; it is `select`ed by several drivers and cannot be turned off,
and the drivers that expose it are the place to gate it if that ever
matters. The `test.fwsig` build stage exercises both modes through
`CONFIG_TEST_FIRMWARE`'s `trigger_request`, which pulls a named file
through the real loader path with no hardware.
