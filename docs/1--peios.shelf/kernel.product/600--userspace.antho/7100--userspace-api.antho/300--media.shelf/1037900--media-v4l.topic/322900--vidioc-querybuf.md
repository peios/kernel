---
title: "ioctl VIDIOC_QUERYBUF"
type: reference
description: "VIDIOC_QUERYBUF - Query the status of a buffer"
---

<a id="rst-ioctl-vidioc-querybuf"></a>
<a id="rst-vidioc-querybuf"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_QUERYBUF - Query the status of a buffer

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_QUERYBUF"></a>

```c
VIDIOC_QUERYBUF
```

`int ioctl(int fd, VIDIOC_QUERYBUF, struct v4l2_buffer *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_buffer`.

<a id="rst-description"></a>

## Description

This ioctl is part of the [streaming](<~kernel/userspace/userspace-api/media-v4l/mmap#rst-mmap>) I/O method. It can be used to query the status of a buffer at any time after buffers have been allocated with the [vidioc_reqbufs](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-reqbufs.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) ioctl.

Applications set the `type` field of a struct `v4l2_buffer` to the same buffer type as was previously used with struct `v4l2_format` `type` and struct `v4l2_requestbuffers` `type`, and the `index` field. Valid index numbers range from zero to the number of buffers allocated with [vidioc_reqbufs](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-reqbufs.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) (struct `v4l2_requestbuffers` `count`) minus one. The `reserved` and `reserved2` fields must be set to 0. When using the [multi-planar API](<~kernel/userspace/userspace-api/media-v4l/planar-apis#rst-planar-apis>), the `m.planes` field must contain a userspace pointer to an array of struct `v4l2_plane` and the `length` field has to be set to the number of elements in that array. After calling [ioctl VIDIOC_QUERYBUF](<#rst-vidioc-querybuf>) with a pointer to this structure drivers return an error code or fill the rest of the structure.

In the `flags` field the `V4L2_BUF_FLAG_MAPPED`, `V4L2_BUF_FLAG_PREPARED`, `V4L2_BUF_FLAG_QUEUED` and `V4L2_BUF_FLAG_DONE` flags will be valid. The `memory` field will be set to the current I/O method. For the single-planar API, the `m.offset` contains the offset of the buffer from the start of the device memory, the `length` field its size. For the multi-planar API, fields `m.mem_offset` and `length` in the `m.planes` array elements will be used instead and the `length` field of struct `v4l2_buffer` is set to the number of filled-in array elements. The driver may or may not set the remaining fields and flags, they are meaningless in this context.

The struct `v4l2_buffer` structure is specified in [buffer](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/buffer.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>).

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  The buffer `type` is not supported, or the `index` is out of bounds.
