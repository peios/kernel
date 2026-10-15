---
title: "ioctl VIDIOC_SUBDEV_ENUM_FRAME_SIZE"
type: reference
description: "VIDIOC_SUBDEV_ENUM_FRAME_SIZE - Enumerate media bus frame sizes"
---

<a id="rst-ioctl-vidioc-subdev-enum-frame-size"></a>
<a id="rst-vidioc-subdev-enum-frame-size"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_SUBDEV_ENUM_FRAME_SIZE - Enumerate media bus frame sizes

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_SUBDEV_ENUM_FRAME_SIZE"></a>

```c
VIDIOC_SUBDEV_ENUM_FRAME_SIZE
```

`int ioctl(int fd, VIDIOC_SUBDEV_ENUM_FRAME_SIZE, struct v4l2_subdev_frame_size_enum * argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_subdev_frame_size_enum`.

<a id="rst-description"></a>

## Description

This ioctl allows applications to access the enumeration of frame sizes supported by a sub-device on the specified pad for the specified media bus format. Supported formats can be retrieved with the [vidioc_subdev_enum_mbus_code](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-subdev-enum-mbus-code.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) ioctl.

The enumerations are defined by the driver, and indexed using the `index` field of the struct `v4l2_subdev_frame_size_enum`. Each pair of `pad` and `code` correspond to a separate enumeration. Each enumeration starts with the `index` of 0, and the lowest invalid index marks the end of the enumeration.

Therefore, to enumerate frame sizes allowed on the specified pad and using the specified mbus format, initialize the `pad`, `which`, and `code` fields to desired values, and set `index` to 0. Then call the [ioctl VIDIOC_SUBDEV_ENUM_FRAME_SIZE](<#rst-vidioc-subdev-enum-frame-size>) ioctl with a pointer to the structure.

A successful call will return with minimum and maximum frame sizes filled in. Repeat with increasing `index` until `EINVAL` is received. `EINVAL` means that either no more entries are available in the enumeration, or that an input parameter was invalid.

Sub-devices that only support discrete frame sizes (such as most sensors) will return one or more frame sizes with identical minimum and maximum values.

Not all possible sizes in given \[minimum, maximum\] ranges need to be supported. For instance, a scaler that uses a fixed-point scaling ratio might not be able to produce every frame size between the minimum and maximum values. Applications must use the [VIDIOC_SUBDEV_S_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-subdev-g-fmt#rst-vidioc-subdev-g-fmt>) ioctl to try the sub-device for an exact supported frame size.

Available frame sizes may depend on the current 'try' formats at other pads of the sub-device, as well as on the current active links and the current values of V4L2 controls. See [ioctl VIDIOC_SUBDEV_G_FMT, VIDIOC_SUBDEV_S_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-subdev-g-fmt#rst-vidioc-subdev-g-fmt>) for more information about try formats.





<a id="c-v4l2_subdev_frame_size_enum"></a>

```c
v4l2_subdev_frame_size_enum
```

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->


<table>
<caption>struct v4l2_subdev_frame_size_enum</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`index`

</td>
<td>


Index of the frame size in the enumeration belonging to the given pad and format. Filled in by the application.

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


Pad number as reported by the media controller API. Filled in by the application.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`code`

</td>
<td>


The media bus format code, as defined in [v4l2-mbus-format](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/subdev-formats.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>). Filled in by the application.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`min_width`

</td>
<td>


Minimum frame width, in pixels. Filled in by the driver.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`max_width`

</td>
<td>


Maximum frame width, in pixels. Filled in by the driver.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`min_height`

</td>
<td>


Minimum frame height, in pixels. Filled in by the driver.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`max_height`

</td>
<td>


Maximum frame height, in pixels. Filled in by the driver.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`which`

</td>
<td>


Frame sizes to be enumerated, from enum [v4l2_subdev_format_whence](<~kernel/userspace/userspace-api/media-v4l/vidioc-subdev-g-fmt#rst-v4l2-subdev-format-whence>).

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

- **EINVAL**

  The struct `v4l2_subdev_frame_size_enum` `pad` references a non-existing pad, the `which` field has an unsupported value, the `code` is invalid for the given pad, or the `index` field is out of bounds.
