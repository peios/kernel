---
title: "ioctl VIDIOC_STREAMON, VIDIOC_STREAMOFF"
type: reference
description: "VIDIOC_STREAMON - VIDIOC_STREAMOFF - Start or stop streaming I/O"
---

<a id="rst-ioctl-vidioc-streamon-vidioc-streamoff"></a>
<a id="rst-vidioc-streamon"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_STREAMON - VIDIOC_STREAMOFF - Start or stop streaming I/O

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_STREAMON"></a>

```c
VIDIOC_STREAMON
```

`int ioctl(int fd, VIDIOC_STREAMON, const int *argp)`





<a id="c-VIDIOC_STREAMOFF"></a>

```c
VIDIOC_STREAMOFF
```

`int ioctl(int fd, VIDIOC_STREAMOFF, const int *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to an integer.

<a id="rst-description"></a>

## Description

The `VIDIOC_STREAMON` and `VIDIOC_STREAMOFF` ioctl start and stop the capture or output process during streaming ([memory mapping](<~kernel/userspace/userspace-api/media-v4l/mmap#rst-mmap>), [user pointer](<~kernel/userspace/userspace-api/media-v4l/userp#rst-userp>) or [DMABUF](<~kernel/userspace/userspace-api/media-v4l/dmabuf#rst-dmabuf>)) I/O.

Capture hardware is disabled and no input buffers are filled (if there are any empty buffers in the incoming queue) until `VIDIOC_STREAMON` has been called. Output hardware is disabled and no video signal is produced until `VIDIOC_STREAMON` has been called.

Memory-to-memory devices will not start until `VIDIOC_STREAMON` has been called for both the capture and output stream types.

If `VIDIOC_STREAMON` fails then any already queued buffers will remain queued.

The `VIDIOC_STREAMOFF` ioctl, apart of aborting or finishing any DMA in progress, unlocks any user pointer buffers locked in physical memory, and it removes all buffers from the incoming and outgoing queues. That means all images captured but not dequeued yet will be lost, likewise all images enqueued for output but not transmitted yet. I/O returns to the same state as after calling [vidioc_reqbufs](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-reqbufs.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) and can be restarted accordingly.

If buffers have been queued with [ioctl VIDIOC_QBUF, VIDIOC_DQBUF](<~kernel/userspace/userspace-api/media-v4l/vidioc-qbuf#rst-vidioc-qbuf>) and `VIDIOC_STREAMOFF` is called without ever having called `VIDIOC_STREAMON`, then those queued buffers will also be removed from the incoming queue and all are returned to the same state as after calling [vidioc_reqbufs](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-reqbufs.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) and can be restarted accordingly.

Both ioctls take a pointer to an integer, the desired buffer or stream type. This is the same as struct `v4l2_requestbuffers` `type`.

If `VIDIOC_STREAMON` is called when streaming is already in progress, or if `VIDIOC_STREAMOFF` is called when streaming is already stopped, then 0 is returned. Nothing happens in the case of `VIDIOC_STREAMON`, but `VIDIOC_STREAMOFF` will return queued buffers to their starting state as mentioned above.

> [!NOTE]
>
> Applications can be preempted for unknown periods right before or after the `VIDIOC_STREAMON` or `VIDIOC_STREAMOFF` calls, there is no notion of starting or stopping "now". Buffer timestamps can be used to synchronize with other events.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  The buffer `type` is not supported, or no buffers have been allocated (memory mapping) or enqueued (output) yet.

- **EPIPE**

  The driver implements [pad-level format configuration](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/dev-subdev.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) and the pipeline configuration is invalid.

- **ENOLINK**

  The driver implements Media Controller interface and the pipeline link configuration is invalid.
