---
title: "ioctl VIDIOC_G_CTRL, VIDIOC_S_CTRL"
type: reference
description: "VIDIOC_G_CTRL - VIDIOC_S_CTRL - Get or set the value of a control"
---

<a id="rst-ioctl-vidioc-g-ctrl-vidioc-s-ctrl"></a>
<a id="rst-vidioc-g-ctrl"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_G_CTRL - VIDIOC_S_CTRL - Get or set the value of a control

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_G_CTRL"></a>

```c
VIDIOC_G_CTRL
```

`int ioctl(int fd, VIDIOC_G_CTRL, struct v4l2_control *argp)`





<a id="c-VIDIOC_S_CTRL"></a>

```c
VIDIOC_S_CTRL
```

`int ioctl(int fd, VIDIOC_S_CTRL, struct v4l2_control *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_control`.

<a id="rst-description"></a>

## Description

To get the current value of a control applications initialize the `id` field of a struct `v4l2_control` and call the [VIDIOC_G_CTRL](<#rst-vidioc-g-ctrl>) ioctl with a pointer to this structure. To change the value of a control applications initialize the `id` and `value` fields of a struct `v4l2_control` and call the [VIDIOC_S_CTRL](<#rst-vidioc-g-ctrl>) ioctl.

When the `id` is invalid drivers return an `EINVAL` error code. When the `value` is out of bounds drivers can choose to take the closest valid value or return an `ERANGE` error code, whatever seems more appropriate. However, [VIDIOC_S_CTRL](<#rst-vidioc-g-ctrl>) is a write-only ioctl, it does not return the actual new value. If the `value` is inappropriate for the control (e.g. if it refers to an unsupported menu index of a menu control), then EINVAL error code is returned as well.

These ioctls work only with user controls. For other control classes the [VIDIOC_G_EXT_CTRLS](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-g-ext-ctrls.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>), [VIDIOC_S_EXT_CTRLS](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-g-ext-ctrls.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) or [VIDIOC_TRY_EXT_CTRLS](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-g-ext-ctrls.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) must be used.





<a id="c-v4l2_control"></a>

```c
v4l2_control
```

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->


<table>
<caption>struct v4l2_control</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`id`

</td>
<td>


Identifies the control, set by the application.

</td>
</tr>
<tr>
<td>


\__s32

</td>
<td>


`value`

</td>
<td>


New value or current value.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  The struct `v4l2_control` `id` is invalid or the `value` is inappropriate for the given control (i.e. if a menu item is selected that is not supported by the driver according to [VIDIOC_QUERYMENU](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-queryctrl.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)).

- **ERANGE**

  The struct `v4l2_control` `value` is out of bounds.

- **EBUSY**

  The control is temporarily not changeable, possibly because another applications took over control of the device function this control belongs to.

- **EACCES**

  Attempt to set a read-only control or to get a write-only control.

  Or if there is an attempt to set an inactive control and the driver is not capable of caching the new value until the control is active again.
