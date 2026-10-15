---
title: "FE_READ_UNCORRECTED_BLOCKS"
type: reference
description: "Duplicate implicit target name: \"fe_read_uncorrected_blocks\"."
---

<a id="rst-fe-read-uncorrected-blocks-1"></a>
<a id="rst-fe-read-uncorrected-blocks"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.fe -->

<a id="rst-name"></a>

## Name

FE_READ_UNCORRECTED_BLOCKS

> [!NOTE]
>
> This ioctl is deprecated.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-FE_READ_UNCORRECTED_BLOCKS"></a>

```c
FE_READ_UNCORRECTED_BLOCKS
```

`int ioctl(int fd, FE_READ_UNCORRECTED_BLOCKS, uint32_t *ublocks)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`ublocks`**

  The total number of uncorrected blocks seen by the driver so far.

<a id="rst-description"></a>

## Description

This ioctl call returns the number of uncorrected blocks detected by the device driver during its lifetime. For meaningful measurements, the increment in block count during a specific time interval should be calculated. For this command, read-only access to the device is sufficient.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned.

On error -1 is returned, and the `errno` variable is set appropriately.

Generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
