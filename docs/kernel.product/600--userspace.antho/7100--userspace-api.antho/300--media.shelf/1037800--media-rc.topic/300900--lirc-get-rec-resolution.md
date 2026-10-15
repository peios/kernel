---
title: "ioctl LIRC_GET_REC_RESOLUTION"
type: reference
description: "LIRC_GET_REC_RESOLUTION - Obtain the value of receive resolution, in microseconds."
---

<a id="rst-ioctl-lirc-get-rec-resolution"></a>
<a id="rst-lirc-get-rec-resolution"></a>

<!-- SPDX-License-Identifier: GPL-2.0 OR GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: RC -->

<a id="rst-name"></a>

## Name

LIRC_GET_REC_RESOLUTION - Obtain the value of receive resolution, in microseconds.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-LIRC_GET_REC_RESOLUTION"></a>

```c
LIRC_GET_REC_RESOLUTION
```

`int ioctl(int fd, LIRC_GET_REC_RESOLUTION, __u32 *microseconds)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by open().

- **`microseconds`**

  Resolution, in microseconds.

<a id="rst-description"></a>

## Description

Some receivers have maximum resolution which is defined by internal sample rate or data format limitations. E.g. it's common that signals can only be reported in 50 microsecond steps.

This ioctl returns the integer value with such resolution, with can be used by userspace applications like lircd to automatically adjust the tolerance value.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
