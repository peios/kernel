---
title: "ioctls LIRC_GET_MIN_TIMEOUT and LIRC_GET_MAX_TIMEOUT"
type: reference
description: "LIRC_GET_MIN_TIMEOUT / LIRC_GET_MAX_TIMEOUT - Obtain the possible timeout range for IR receive."
---

<a id="rst-ioctls-lirc-get-min-timeout-and-lirc-get-max-timeout"></a>
<a id="rst-lirc-get-max-timeout"></a>
<a id="rst-lirc-get-min-timeout"></a>

<!-- SPDX-License-Identifier: GPL-2.0 OR GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: RC -->

<a id="rst-name"></a>

## Name

LIRC_GET_MIN_TIMEOUT / LIRC_GET_MAX_TIMEOUT - Obtain the possible timeout range for IR receive.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-LIRC_GET_MIN_TIMEOUT"></a>

```c
LIRC_GET_MIN_TIMEOUT
```

`int ioctl(int fd, LIRC_GET_MIN_TIMEOUT, __u32 *timeout)`





<a id="c-LIRC_GET_MAX_TIMEOUT"></a>

```c
LIRC_GET_MAX_TIMEOUT
```

`int ioctl(int fd, LIRC_GET_MAX_TIMEOUT, __u32 *timeout)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by open().

- **`timeout`**

  Timeout, in microseconds.

<a id="rst-description"></a>

## Description

Some devices have internal timers that can be used to detect when there's no IR activity for a long time. This can help lircd in detecting that a IR signal is finished and can speed up the decoding process. Returns an integer value with the minimum/maximum timeout that can be set.

> [!NOTE]
>
> Some devices have a fixed timeout, in that case both ioctls will return the same value even though the timeout cannot be changed via [ioctl LIRC_GET_REC_TIMEOUT and LIRC_SET_REC_TIMEOUT](<~kernel/userspace/userspace-api/media-rc/lirc-set-rec-timeout#rst-lirc-set-rec-timeout>).

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
