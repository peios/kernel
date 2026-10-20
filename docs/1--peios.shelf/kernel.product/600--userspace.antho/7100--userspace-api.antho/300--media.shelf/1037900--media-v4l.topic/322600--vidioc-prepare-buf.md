---
title: "ioctl VIDIOC_PREPARE_BUF"
type: reference
description: "VIDIOC_PREPARE_BUF - Prepare a buffer for I/O"
---

<a id="rst-ioctl-vidioc-prepare-buf"></a>
<a id="rst-vidioc-prepare-buf"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_PREPARE_BUF - Prepare a buffer for I/O

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_PREPARE_BUF"></a>

```c
VIDIOC_PREPARE_BUF
```

`int ioctl(int fd, VIDIOC_PREPARE_BUF, struct v4l2_buffer *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_buffer`.

<a id="rst-description"></a>

## Description

Applications can optionally call the [ioctl VIDIOC_PREPARE_BUF](<#rst-vidioc-prepare-buf>) ioctl to pass ownership of the buffer to the driver before actually enqueuing it, using the [VIDIOC_QBUF](<~kernel/userspace/userspace-api/media-v4l/vidioc-qbuf#rst-vidioc-qbuf>) ioctl, and to prepare it for future I/O. Such preparations may include cache invalidation or cleaning. Performing them in advance saves time during the actual I/O.

The struct `v4l2_buffer` structure is specified in [buffer](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/buffer.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>).

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EBUSY**

  File I/O is in progress.

- **EINVAL**

  The buffer `type` is not supported, or the `index` is out of bounds, or no buffers have been allocated yet, or the `userptr` or `length` are invalid.
