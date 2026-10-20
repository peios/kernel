---
title: "ioctl VIDIOC_QBUF, VIDIOC_DQBUF"
type: reference
description: "VIDIOC_QBUF - VIDIOC_DQBUF - Exchange a buffer with the driver"
---

<a id="rst-ioctl-vidioc-qbuf-vidioc-dqbuf"></a>
<a id="rst-vidioc-qbuf"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_QBUF - VIDIOC_DQBUF - Exchange a buffer with the driver

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_QBUF"></a>

```c
VIDIOC_QBUF
```

`int ioctl(int fd, VIDIOC_QBUF, struct v4l2_buffer *argp)`





<a id="c-VIDIOC_DQBUF"></a>

```c
VIDIOC_DQBUF
```

`int ioctl(int fd, VIDIOC_DQBUF, struct v4l2_buffer *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_buffer`.

<a id="rst-description"></a>

## Description

Applications call the `VIDIOC_QBUF` ioctl to enqueue an empty (capturing) or filled (output) buffer in the driver's incoming queue. The semantics depend on the selected I/O method.

To enqueue a buffer applications set the `type` field of a struct `v4l2_buffer` to the same buffer type as was previously used with struct `v4l2_format` `type` and struct `v4l2_requestbuffers` `type`. Applications must also set the `index` field. Valid index numbers range from zero to the number of buffers allocated with [vidioc_reqbufs](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-reqbufs.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) (struct `v4l2_requestbuffers` `count`) minus one. The contents of the struct `v4l2_buffer` returned by a [ioctl VIDIOC_QUERYBUF](<~kernel/userspace/userspace-api/media-v4l/vidioc-querybuf#rst-vidioc-querybuf>) ioctl will do as well. When the buffer is intended for output (`type` is `V4L2_BUF_TYPE_VIDEO_OUTPUT`, `V4L2_BUF_TYPE_VIDEO_OUTPUT_MPLANE`, or `V4L2_BUF_TYPE_VBI_OUTPUT`) applications must also initialize the `bytesused`, `field` and `timestamp` fields, see [buffer](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/buffer.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) for details. Applications must also set `flags` to 0. The `reserved2` and `reserved` fields must be set to 0. When using the [multi-planar API](<~kernel/userspace/userspace-api/media-v4l/planar-apis#rst-planar-apis>), the `m.planes` field must contain a userspace pointer to a filled-in array of struct `v4l2_plane` and the `length` field must be set to the number of elements in that array.

To enqueue a [memory mapped](<~kernel/userspace/userspace-api/media-v4l/mmap#rst-mmap>) buffer applications set the `memory` field to `V4L2_MEMORY_MMAP`. When `VIDIOC_QBUF` is called with a pointer to this structure the driver sets the `V4L2_BUF_FLAG_MAPPED` and `V4L2_BUF_FLAG_QUEUED` flags and clears the `V4L2_BUF_FLAG_DONE` flag in the `flags` field, or it returns an `EINVAL` error code.

To enqueue a [user pointer](<~kernel/userspace/userspace-api/media-v4l/userp#rst-userp>) buffer applications set the `memory` field to `V4L2_MEMORY_USERPTR`, the `m.userptr` field to the address of the buffer and `length` to its size. When the multi-planar API is used, `m.userptr` and `length` members of the passed array of struct `v4l2_plane` have to be used instead. When `VIDIOC_QBUF` is called with a pointer to this structure the driver sets the `V4L2_BUF_FLAG_QUEUED` flag and clears the `V4L2_BUF_FLAG_MAPPED` and `V4L2_BUF_FLAG_DONE` flags in the `flags` field, or it returns an error code. This ioctl locks the memory pages of the buffer in physical memory, they cannot be swapped out to disk. Buffers remain locked until dequeued, until the [VIDIOC_STREAMOFF](<~kernel/userspace/userspace-api/media-v4l/vidioc-streamon#rst-vidioc-streamon>) or [vidioc_reqbufs](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-reqbufs.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) ioctl is called, or until the device is closed.

To enqueue a [DMABUF](<~kernel/userspace/userspace-api/media-v4l/dmabuf#rst-dmabuf>) buffer applications set the `memory` field to `V4L2_MEMORY_DMABUF` and the `m.fd` field to a file descriptor associated with a DMABUF buffer. When the multi-planar API is used the `m.fd` fields of the passed array of struct `v4l2_plane` have to be used instead. When `VIDIOC_QBUF` is called with a pointer to this structure the driver sets the `V4L2_BUF_FLAG_QUEUED` flag and clears the `V4L2_BUF_FLAG_MAPPED` and `V4L2_BUF_FLAG_DONE` flags in the `flags` field, or it returns an error code. This ioctl locks the buffer. Locking a buffer means passing it to a driver for a hardware access (usually DMA). If an application accesses (reads/writes) a locked buffer then the result is undefined. Buffers remain locked until dequeued, until the [VIDIOC_STREAMOFF](<~kernel/userspace/userspace-api/media-v4l/vidioc-streamon#rst-vidioc-streamon>) or [vidioc_reqbufs](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-reqbufs.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) ioctl is called, or until the device is closed.

The `request_fd` field can be used with the `VIDIOC_QBUF` ioctl to specify the file descriptor of a [request](<~kernel/userspace/userspace-api/media-mediactl/request-api#rst-media-request-api>), if requests are in use. Setting it means that the buffer will not be passed to the driver until the request itself is queued. Also, the driver will apply any settings associated with the request for this buffer. This field will be ignored unless the `V4L2_BUF_FLAG_REQUEST_FD` flag is set. If the device does not support requests, then `EBADR` will be returned. If requests are supported but an invalid request file descriptor is given, then `EINVAL` will be returned.

> [!CAUTION]
>
> It is not allowed to mix queuing requests with queuing buffers directly. `EBUSY` will be returned if the first buffer was queued directly and then the application tries to queue a request, or vice versa. After closing the file descriptor, calling [VIDIOC_STREAMOFF](<~kernel/userspace/userspace-api/media-v4l/vidioc-streamon#rst-vidioc-streamon>) or calling [vidioc_reqbufs](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-reqbufs.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) the check for this will be reset.
>
> For [memory-to-memory devices](<~kernel/userspace/userspace-api/media-v4l/dev-mem2mem#rst-mem2mem>) you can specify the `request_fd` only for output buffers, not for capture buffers. Attempting to specify this for a capture buffer will result in an `EBADR` error.

Applications call the `VIDIOC_DQBUF` ioctl to dequeue a filled (capturing) or displayed (output) buffer from the driver's outgoing queue. They just set the `type`, `memory` and `reserved` fields of a struct `v4l2_buffer` as above, when `VIDIOC_DQBUF` is called with a pointer to this structure the driver fills all remaining fields or returns an error code. The driver may also set `V4L2_BUF_FLAG_ERROR` in the `flags` field. It indicates a non-critical (recoverable) streaming error. In such case the application may continue as normal, but should be aware that data in the dequeued buffer might be corrupted. When using the multi-planar API, the planes array must be passed in as well.

If the application sets the `memory` field to `V4L2_MEMORY_DMABUF` to dequeue a [DMABUF](<~kernel/userspace/userspace-api/media-v4l/dmabuf#rst-dmabuf>) buffer, the driver fills the `m.fd` field with a file descriptor numerically the same as the one given to `VIDIOC_QBUF` when the buffer was enqueued. No new file descriptor is created at dequeue time and the value is only for the application convenience. When the multi-planar API is used the `m.fd` fields of the passed array of struct `v4l2_plane` are filled instead.

By default `VIDIOC_DQBUF` blocks when no buffer is in the outgoing queue. When the `O_NONBLOCK` flag was given to the `open()` function, `VIDIOC_DQBUF` returns immediately with an `EAGAIN` error code when no buffer is available.

The struct `v4l2_buffer` structure is specified in [buffer](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/buffer.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>).

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EAGAIN**

  Non-blocking I/O has been selected using `O_NONBLOCK` and no buffer was in the outgoing queue.

- **EINVAL**

  The buffer `type` is not supported, or the `index` is out of bounds, or no buffers have been allocated yet, or the `userptr` or `length` are invalid, or the `V4L2_BUF_FLAG_REQUEST_FD` flag was set but the given `request_fd` was invalid, or `m.fd` was an invalid DMABUF file descriptor.

- **EIO**

  `VIDIOC_DQBUF` failed due to an internal error. Can also indicate temporary problems like signal loss.

  > [!NOTE]
  >
  > The driver might dequeue an (empty) buffer despite returning an error, or even stop capturing. Reusing such buffer may be unsafe though and its details (e.g. `index`) may not be returned either. It is recommended that drivers indicate recoverable errors by setting the `V4L2_BUF_FLAG_ERROR` and returning 0 instead. In that case the application should be able to safely reuse the buffer and continue streaming.

- **EPIPE**

  `VIDIOC_DQBUF` returns this on an empty capture queue for mem2mem codecs if a buffer with the `V4L2_BUF_FLAG_LAST` was already dequeued and no new buffers are expected to become available.

- **EBADR**

  The `V4L2_BUF_FLAG_REQUEST_FD` flag was set but the device does not support requests for the given buffer type, or the `V4L2_BUF_FLAG_REQUEST_FD` flag was not set but the device requires that the buffer is part of a request.

- **EBUSY**

  The first buffer was queued via a request, but the application now tries to queue it directly, or vice versa (it is not permitted to mix the two APIs).
