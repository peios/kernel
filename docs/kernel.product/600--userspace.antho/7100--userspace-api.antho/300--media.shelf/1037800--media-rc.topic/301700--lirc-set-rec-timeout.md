---
title: "ioctl LIRC_GET_REC_TIMEOUT and LIRC_SET_REC_TIMEOUT"
type: reference
description: "LIRC_GET_REC_TIMEOUT/LIRC_SET_REC_TIMEOUT - Get/set the integer value for IR inactivity timeout."
---

<a id="rst-ioctl-lirc-get-rec-timeout-and-lirc-set-rec-timeout"></a>
<a id="rst-lirc-get-rec-timeout"></a>
<a id="rst-lirc-set-rec-timeout"></a>

<!-- SPDX-License-Identifier: GPL-2.0 OR GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: RC -->

<a id="rst-name"></a>

## Name

LIRC_GET_REC_TIMEOUT/LIRC_SET_REC_TIMEOUT - Get/set the integer value for IR inactivity timeout.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-LIRC_GET_REC_TIMEOUT"></a>

```c
LIRC_GET_REC_TIMEOUT
```

`int ioctl(int fd, LIRC_GET_REC_TIMEOUT, __u32 *timeout)`





<a id="c-LIRC_SET_REC_TIMEOUT"></a>

```c
LIRC_SET_REC_TIMEOUT
```

`int ioctl(int fd, LIRC_SET_REC_TIMEOUT, __u32 *timeout)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by open().

- **`timeout`**

  Timeout, in microseconds.

<a id="rst-description"></a>

## Description

Get and set the integer value for IR inactivity timeout.

If supported by the hardware, setting it to 0  disables all hardware timeouts and data should be reported as soon as possible. If the exact value cannot be set, then the next possible value \_greater\_ than the given value should be set.

> [!NOTE]
>
> The range of supported timeout is given by [ioctls LIRC_GET_MIN_TIMEOUT and LIRC_GET_MAX_TIMEOUT](<~kernel/userspace/userspace-api/media-rc/lirc-get-timeout#rst-lirc-get-min-timeout>).

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
