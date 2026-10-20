---
title: "ioctl VIDIOC_SUBDEV_G_SELECTION, VIDIOC_SUBDEV_S_SELECTION"
type: reference
description: "VIDIOC_SUBDEV_G_SELECTION - VIDIOC_SUBDEV_S_SELECTION - Get or set selection rectangles on a subdev pad"
---

<a id="rst-ioctl-vidioc-subdev-g-selection-vidioc-subdev-s-selection"></a>
<a id="rst-vidioc-subdev-g-selection"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_SUBDEV_G_SELECTION - VIDIOC_SUBDEV_S_SELECTION - Get or set selection rectangles on a subdev pad

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_SUBDEV_G_SELECTION"></a>

```c
VIDIOC_SUBDEV_G_SELECTION
```

`int ioctl(int fd, VIDIOC_SUBDEV_G_SELECTION, struct v4l2_subdev_selection *argp)`





<a id="c-VIDIOC_SUBDEV_S_SELECTION"></a>

```c
VIDIOC_SUBDEV_S_SELECTION
```

`int ioctl(int fd, VIDIOC_SUBDEV_S_SELECTION, struct v4l2_subdev_selection *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_subdev_selection`.

<a id="rst-description"></a>

## Description

The selections are used to configure various image processing functionality performed by the subdevs which affect the image size. This currently includes cropping, scaling and composition.

The selection API replaces [the old subdev crop API](<~kernel/userspace/userspace-api/media-v4l/vidioc-subdev-g-crop#rst-vidioc-subdev-g-crop>). All the function of the crop API, and more, are supported by the selections API.

See [subdev](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/dev-subdev.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) for more information on how each selection target affects the image processing pipeline inside the subdevice.

If the subdev device node has been registered in read-only mode, calls to `VIDIOC_SUBDEV_S_SELECTION` are only valid if the `which` field is set to `V4L2_SUBDEV_FORMAT_TRY`, otherwise an error is returned and the errno variable is set to `-EPERM`.

<a id="rst-types-of-selection-targets"></a>

### Types of selection targets

There are two types of selection targets: actual and bounds. The actual targets are the targets which configure the hardware. The BOUNDS target will return a rectangle that contain all possible actual rectangles.

<a id="rst-discovering-supported-features"></a>

### Discovering supported features

To discover which targets are supported, the user can perform `VIDIOC_SUBDEV_G_SELECTION` on them. Any unsupported target will return `EINVAL`.

Selection targets and flags are documented in [Common selection definitions](<~kernel/userspace/userspace-api/media-v4l/selections-common#rst-v4l2-selections-common>).





<a id="c-v4l2_subdev_selection"></a>

```c
v4l2_subdev_selection
```

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->


<table>
<caption>struct v4l2_subdev_selection</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`which`

</td>
<td>


Active or try selection, from enum [v4l2_subdev_format_whence](<~kernel/userspace/userspace-api/media-v4l/vidioc-subdev-g-fmt#rst-v4l2-subdev-format-whence>).

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`pad`

</td>
<td>


Pad number as reported by the media framework.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`target`

</td>
<td>


Target selection rectangle. See [Common selection definitions](<~kernel/userspace/userspace-api/media-v4l/selections-common#rst-v4l2-selections-common>).

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`flags`

</td>
<td>


Flags. See [v4l2-selection-flags](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/v4l2-selection-flags.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>).

</td>
</tr>
<tr>
<td>


struct `v4l2_rect`

</td>
<td>


`r`

</td>
<td>


Selection rectangle, in pixels.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`stream`

</td>
<td>


Stream identifier.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`reserved`\[7\]

</td>
<td>


Reserved for future extensions. Applications and drivers must set the array to zero.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EBUSY**

  The selection rectangle can't be changed because the pad is currently busy. This can be caused, for instance, by an active video stream on the pad. The ioctl must not be retried without performing another action to fix the problem first. Only returned by `VIDIOC_SUBDEV_S_SELECTION`

- **EINVAL**

  The struct `v4l2_subdev_selection` `pad` references a non-existing pad, the `which` field has an unsupported value, or the selection target is not supported on the given subdev pad.

- **EPERM**

  The `VIDIOC_SUBDEV_S_SELECTION` ioctl has been called on a read-only subdevice and the `which` field is set to `V4L2_SUBDEV_FORMAT_ACTIVE`.
