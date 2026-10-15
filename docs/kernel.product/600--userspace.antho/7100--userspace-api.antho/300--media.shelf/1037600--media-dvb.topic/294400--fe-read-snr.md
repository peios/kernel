---
title: "FE_READ_SNR"
type: reference
description: "Duplicate implicit target name: \"fe_read_snr\"."
---

<a id="rst-fe-read-snr-1"></a>
<a id="rst-fe-read-snr"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.fe -->

<a id="rst-name"></a>

## Name

FE_READ_SNR

> [!NOTE]
>
> This ioctl is deprecated.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-FE_READ_SNR"></a>

```c
FE_READ_SNR
```

`int ioctl(int fd, FE_READ_SNR, int16_t *snr)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`snr`**

  The signal-to-noise ratio is stored into \*snr.

<a id="rst-description"></a>

## Description

This ioctl call returns the signal-to-noise ratio for the signal currently received by the front-end. For this command, read-only access to the device is sufficient.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned.

On error -1 is returned, and the `errno` variable is set appropriately.

Generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
