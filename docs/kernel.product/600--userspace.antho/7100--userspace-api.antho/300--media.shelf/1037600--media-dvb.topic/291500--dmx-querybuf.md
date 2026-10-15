---
title: "ioctl DMX_QUERYBUF"
type: reference
description: "DMX_QUERYBUF - Query the status of a buffer"
---

<a id="rst-ioctl-dmx-querybuf"></a>
<a id="rst-dmx-querybuf"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.dmx -->

<a id="rst-name"></a>

## Name

DMX_QUERYBUF - Query the status of a buffer

> [!WARNING]
>
> this API is still experimental

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-DMX_QUERYBUF"></a>

```c
DMX_QUERYBUF
```

`int ioctl(int fd, DMX_QUERYBUF, struct dvb_buffer *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `dvb_buffer`.

<a id="rst-description"></a>

## Description

This ioctl is part of the mmap streaming I/O method. It can be used to query the status of a buffer at any time after buffers have been allocated with the [ioctl DMX_REQBUFS](<~kernel/userspace/userspace-api/media-dvb/dmx-reqbufs#rst-dmx-reqbufs>) ioctl.

Applications set the `index` field. Valid index numbers range from zero to the number of buffers allocated with [ioctl DMX_REQBUFS](<~kernel/userspace/userspace-api/media-dvb/dmx-reqbufs#rst-dmx-reqbufs>) (struct `dvb_requestbuffers` `count`) minus one.

After calling [ioctl DMX_QUERYBUF](<#rst-dmx-querybuf>) with a pointer to this structure, drivers return an error code or fill the rest of the structure.

On success, the `offset` will contain the offset of the buffer from the start of the device memory, the `length` field its size, and the `bytesused` the number of bytes occupied by data in the buffer (payload).

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, the `offset` will contain the offset of the buffer from the start of the device memory, the `length` field its size, and the `bytesused` the number of bytes occupied by data in the buffer (payload).

On error it returns -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  The `index` is out of bounds.
