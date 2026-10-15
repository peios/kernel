---
title: "ioctl VIDIOC_G_STD, VIDIOC_S_STD, VIDIOC_SUBDEV_G_STD, VIDIOC_SUBDEV_S_STD"
type: reference
description: "VIDIOC_G_STD - VIDIOC_S_STD - VIDIOC_SUBDEV_G_STD - VIDIOC_SUBDEV_S_STD - Query or select the video standard of the current input"
---

<a id="rst-ioctl-vidioc-g-std-vidioc-s-std-vidioc-subdev-g-std-vidioc-subdev-s-std"></a>
<a id="rst-vidioc-g-std"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_G_STD - VIDIOC_S_STD - VIDIOC_SUBDEV_G_STD - VIDIOC_SUBDEV_S_STD - Query or select the video standard of the current input

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_G_STD"></a>

```c
VIDIOC_G_STD
```

`int ioctl(int fd, VIDIOC_G_STD, v4l2_std_id *argp)`





<a id="c-VIDIOC_S_STD"></a>

```c
VIDIOC_S_STD
```

`int ioctl(int fd, VIDIOC_S_STD, const v4l2_std_id *argp)`





<a id="c-VIDIOC_SUBDEV_G_STD"></a>

```c
VIDIOC_SUBDEV_G_STD
```

`int ioctl(int fd, VIDIOC_SUBDEV_G_STD, v4l2_std_id *argp)`





<a id="c-VIDIOC_SUBDEV_S_STD"></a>

```c
VIDIOC_SUBDEV_S_STD
```

`int ioctl(int fd, VIDIOC_SUBDEV_S_STD, const v4l2_std_id *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to `v4l2_std_id`.

<a id="rst-description"></a>

## Description

To query and select the current video standard applications use the [VIDIOC_G_STD](<#rst-vidioc-g-std>) and [VIDIOC_S_STD](<#rst-vidioc-g-std>) ioctls which take a pointer to a [v4l2_std_id](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-enumstd.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) type as argument. [VIDIOC_G_STD](<#rst-vidioc-g-std>) can return a single flag or a set of flags as in struct `v4l2_standard` field `id`. The flags must be unambiguous such that they appear in only one enumerated struct `v4l2_standard` structure.

[VIDIOC_S_STD](<#rst-vidioc-g-std>) accepts one or more flags, being a write-only ioctl it does not return the actual new standard as [VIDIOC_G_STD](<#rst-vidioc-g-std>) does. When no flags are given or the current input does not support the requested standard the driver returns an `EINVAL` error code. When the standard set is ambiguous drivers may return `EINVAL` or choose any of the requested standards. If the current input or output does not support standard video timings (e.g. if [ioctl VIDIOC_ENUMINPUT](<~kernel/userspace/userspace-api/media-v4l/vidioc-enuminput#rst-vidioc-enuminput>) does not set the `V4L2_IN_CAP_STD` flag), then `ENODATA` error code is returned.

Calling `VIDIOC_SUBDEV_S_STD` on a subdev device node that has been registered in read-only mode is not allowed. An error is returned and the errno variable is set to `-EPERM`.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  The [VIDIOC_S_STD](<#rst-vidioc-g-std>) parameter was unsuitable.

- **ENODATA**

  Standard video timings are not supported for this input or output.

- **EPERM**

  `VIDIOC_SUBDEV_S_STD` has been called on a read-only subdevice.
