---
title: "ioctl MEDIA_IOC_REQUEST_ALLOC"
type: reference
description: "MEDIA_IOC_REQUEST_ALLOC - Allocate a request"
---

<a id="rst-ioctl-media-ioc-request-alloc"></a>
<a id="rst-media-ioc-request-alloc"></a>

<!-- SPDX-License-Identifier: GPL-2.0 OR GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: MC -->

<a id="rst-name"></a>

## Name

MEDIA_IOC_REQUEST_ALLOC - Allocate a request

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-MEDIA_IOC_REQUEST_ALLOC"></a>

```c
MEDIA_IOC_REQUEST_ALLOC
```

`int ioctl(int fd, MEDIA_IOC_REQUEST_ALLOC, int *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to an integer.

<a id="rst-description"></a>

## Description

If the media device supports [requests](<~kernel/userspace/userspace-api/media-mediactl/request-api#rst-media-request-api>), then this ioctl can be used to allocate a request. If it is not supported, then `errno` is set to `ENOTTY`. A request is accessed through a file descriptor that is returned in `*argp`.

If the request was successfully allocated, then the request file descriptor can be passed to the [VIDIOC_QBUF](<~kernel/userspace/userspace-api/media-v4l/vidioc-qbuf#rst-vidioc-qbuf>), [VIDIOC_G_EXT_CTRLS](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-g-ext-ctrls.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>), [VIDIOC_S_EXT_CTRLS](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-g-ext-ctrls.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) and [VIDIOC_TRY_EXT_CTRLS](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-g-ext-ctrls.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) ioctls.

In addition, the request can be queued by calling [ioctl MEDIA_REQUEST_IOC_QUEUE](<~kernel/userspace/userspace-api/media-mediactl/media-request-ioc-queue#rst-media-request-ioc-queue>) and re-initialized by calling [ioctl MEDIA_REQUEST_IOC_REINIT](<~kernel/userspace/userspace-api/media-mediactl/media-request-ioc-reinit#rst-media-request-ioc-reinit>).

Finally, the file descriptor can be [polled](<~kernel/userspace/userspace-api/media-mediactl/request-func-poll#rst-request-func-poll>) to wait for the request to complete.

The request will remain allocated until all the file descriptors associated with it are closed by `close()` and the driver no longer uses the request internally. See also [here](<~kernel/userspace/userspace-api/media-mediactl/request-api#rst-media-request-life-time>) for more information.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **ENOTTY**

  The driver has no support for requests.
