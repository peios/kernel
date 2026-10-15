---
title: "ioctl VIDIOC_OVERLAY"
type: reference
description: "VIDIOC_OVERLAY - Start or stop video overlay"
---

<a id="rst-ioctl-vidioc-overlay"></a>
<a id="rst-vidioc-overlay"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_OVERLAY - Start or stop video overlay

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_OVERLAY"></a>

```c
VIDIOC_OVERLAY
```

`int ioctl(int fd, VIDIOC_OVERLAY, const int *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to an integer.

<a id="rst-description"></a>

## Description

This ioctl is part of the [video overlay](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/dev-overlay.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) I/O method. Applications call [ioctl VIDIOC_OVERLAY](<#rst-vidioc-overlay>) to start or stop the overlay. It takes a pointer to an integer which must be set to zero by the application to stop overlay, to one to start.

Drivers do not support [ioctl VIDIOC_STREAMON, VIDIOC_STREAMOFF](<~kernel/userspace/userspace-api/media-v4l/vidioc-streamon#rst-vidioc-streamon>) or [VIDIOC_STREAMOFF](<~kernel/userspace/userspace-api/media-v4l/vidioc-streamon#rst-vidioc-streamon>) with `V4L2_BUF_TYPE_VIDEO_OVERLAY`.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  The overlay parameters have not been set up. See [Video Overlay Interface](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/dev-overlay.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) for the necessary steps.
