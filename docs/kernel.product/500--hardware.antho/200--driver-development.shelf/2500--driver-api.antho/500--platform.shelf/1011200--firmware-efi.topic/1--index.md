---
title: "Unified Extensible Firmware Interface (UEFI) Support"
type: reference
description: "Reference for Unified Extensible Firmware Interface (UEFI) Support."
---

> **Peios:** File-based firmware loading has an additional Peios signature check. The development profile defaults to logging (`kacs_fwsig=log`); `kacs_fwsig=enforce` requires PeiosTcb trust for that path. This does not cover the separate `FW_UPLOAD` interface. See [Peios kernel behaviour](<~kernel/introduction/peios-behaviour>).


<a id="rst-unified-extensible-firmware-interface-uefi-support"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-uefi-stub-library-functions"></a>

## UEFI stub library functions

```{kernel-doc} drivers/firmware/efi/libstub/mem.c
:internal:
```

<a id="rst-uefi-common-platform-error-record-cper-functions"></a>

## UEFI Common Platform Error Record (CPER) functions

```{kernel-doc} drivers/firmware/efi/cper.c

```
