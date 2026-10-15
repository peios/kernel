---
title: "ioctl VIDIOC_SUBDEV_ENUM_FRAME_INTERVAL"
type: reference
description: "VIDIOC_SUBDEV_ENUM_FRAME_INTERVAL - Enumerate frame intervals"
---

<a id="rst-ioctl-vidioc-subdev-enum-frame-interval"></a>
<a id="rst-vidioc-subdev-enum-frame-interval"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_SUBDEV_ENUM_FRAME_INTERVAL - Enumerate frame intervals

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_SUBDEV_ENUM_FRAME_INTERVAL"></a>

```c
VIDIOC_SUBDEV_ENUM_FRAME_INTERVAL
```

`int ioctl(int fd, VIDIOC_SUBDEV_ENUM_FRAME_INTERVAL, struct v4l2_subdev_frame_interval_enum * argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_subdev_frame_interval_enum`.

<a id="rst-description"></a>

## Description

This ioctl lets applications enumerate available frame intervals on a given sub-device pad. Frame intervals only makes sense for sub-devices that can control the frame period on their own. This includes, for instance, image sensors and TV tuners.

For the common use case of image sensors, the frame intervals available on the sub-device output pad depend on the frame format and size on the same pad. Applications must thus specify the desired format and size when enumerating frame intervals.

To enumerate frame intervals applications initialize the `index`, `pad`, `which`, `code`, `width` and `height` fields of struct `v4l2_subdev_frame_interval_enum` and call the [ioctl VIDIOC_SUBDEV_ENUM_FRAME_INTERVAL](<#rst-vidioc-subdev-enum-frame-interval>) ioctl with a pointer to this structure. Drivers fill the rest of the structure or return an EINVAL error code if one of the input fields is invalid. All frame intervals are enumerable by beginning at index zero and incrementing by one until `EINVAL` is returned.

Available frame intervals may depend on the current 'try' formats at other pads of the sub-device, as well as on the current active links. See [ioctl VIDIOC_SUBDEV_G_FMT, VIDIOC_SUBDEV_S_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-subdev-g-fmt#rst-vidioc-subdev-g-fmt>) for more information about the try formats.

Sub-devices that support the frame interval enumeration ioctl should implemented it on a single pad only. Its behaviour when supported on multiple pads of the same sub-device is not defined.





<a id="c-v4l2_subdev_frame_interval_enum"></a>

```c
v4l2_subdev_frame_interval_enum
```

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->


<table>
<caption>struct v4l2_subdev_frame_interval_enum</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`index`

</td>
<td>


Number of the format in the enumeration, set by the application.

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


Pad number as reported by the media controller API.

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


The media bus format code, as defined in [v4l2-mbus-format](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/subdev-formats.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>).

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`width`

</td>
<td>


Frame width, in pixels.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`height`

</td>
<td>


Frame height, in pixels.

</td>
</tr>
<tr>
<td>


struct `v4l2_fract`

</td>
<td>


`interval`

</td>
<td>


Period, in seconds, between consecutive video frames.

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


Frame intervals to be enumerated, from enum [v4l2_subdev_format_whence](<~kernel/userspace/userspace-api/media-v4l/vidioc-subdev-g-fmt#rst-v4l2-subdev-format-whence>).

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

  The struct `v4l2_subdev_frame_interval_enum` `pad` references a non-existing pad, the `which` field has an unsupported value, one of the `code`, `width` or `height` fields are invalid for the given pad, or the `index` field is out of bounds.
