---
title: "ioctl DMX_QBUF, DMX_DQBUF"
type: reference
description: "DMX_QBUF - DMX_DQBUF - Exchange a buffer with the driver"
---

<a id="rst-ioctl-dmx-qbuf-dmx-dqbuf"></a>
<a id="rst-dmx-qbuf"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.dmx -->

<a id="rst-name"></a>

## Name

DMX_QBUF - DMX_DQBUF - Exchange a buffer with the driver

> [!WARNING]
>
> this API is still experimental

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-DMX_QBUF"></a>

```c
DMX_QBUF
```

`int ioctl(int fd, DMX_QBUF, struct dmx_buffer *argp)`





<a id="c-DMX_DQBUF"></a>

```c
DMX_DQBUF
```

`int ioctl(int fd, DMX_DQBUF, struct dmx_buffer *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `dmx_buffer`.

<a id="rst-description"></a>

## Description

Applications call the `DMX_QBUF` ioctl to enqueue an empty (capturing) or filled (output) buffer in the driver's incoming queue. The semantics depend on the selected I/O method.

To enqueue a buffer applications set the `index` field. Valid index numbers range from zero to the number of buffers allocated with [ioctl DMX_REQBUFS](<~kernel/userspace/userspace-api/media-dvb/dmx-reqbufs#rst-dmx-reqbufs>) (struct `dmx_requestbuffers` `count`) minus one. The contents of the struct `dmx_buffer` returned by a [ioctl DMX_QUERYBUF](<~kernel/userspace/userspace-api/media-dvb/dmx-querybuf#rst-dmx-querybuf>) ioctl will do as well.

When `DMX_QBUF` is called with a pointer to this structure, it locks the memory pages of the buffer in physical memory, so they cannot be swapped out to disk. Buffers remain locked until dequeued, until the device is closed.

Applications call the `DMX_DQBUF` ioctl to dequeue a filled (capturing) buffer from the driver's outgoing queue. They just set the `index` field with the buffer ID to be queued. When `DMX_DQBUF` is called with a pointer to struct `dmx_buffer`, the driver fills the remaining fields or returns an error code.

By default `DMX_DQBUF` blocks when no buffer is in the outgoing queue. When the `O_NONBLOCK` flag was given to the `open()` function, `DMX_DQBUF` returns immediately with an `EAGAIN` error code when no buffer is available.

The struct `dmx_buffer` structure is specified in [buffer](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/buffer.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>).

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EAGAIN**

  Non-blocking I/O has been selected using `O_NONBLOCK` and no buffer was in the outgoing queue.

- **EINVAL**

  The `index` is out of bounds, or no buffers have been allocated yet.

- **EIO**

  `DMX_DQBUF` failed due to an internal error. Can also indicate temporary problems like signal loss or CRC errors.
