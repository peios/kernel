---
title: "ioctl VIDIOC_SUBDEV_G_CROP, VIDIOC_SUBDEV_S_CROP"
type: reference
description: "VIDIOC_SUBDEV_G_CROP - VIDIOC_SUBDEV_S_CROP - Get or set the crop rectangle on a subdev pad"
---

<a id="rst-ioctl-vidioc-subdev-g-crop-vidioc-subdev-s-crop"></a>
<a id="rst-vidioc-subdev-g-crop"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_SUBDEV_G_CROP - VIDIOC_SUBDEV_S_CROP - Get or set the crop rectangle on a subdev pad

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_SUBDEV_G_CROP"></a>

```c
VIDIOC_SUBDEV_G_CROP
```

`int ioctl(int fd, VIDIOC_SUBDEV_G_CROP, struct v4l2_subdev_crop *argp)`





<a id="c-VIDIOC_SUBDEV_S_CROP"></a>

```c
VIDIOC_SUBDEV_S_CROP
```

`int ioctl(int fd, VIDIOC_SUBDEV_S_CROP, const struct v4l2_subdev_crop *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_subdev_crop`.

<a id="rst-description"></a>

## Description

> [!NOTE]
>
> This is an [Obsolete API Elements](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/hist-v4l2.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) interface and may be removed in the future. It is superseded by [the selection API](<~kernel/userspace/userspace-api/media-v4l/vidioc-subdev-g-selection#rst-vidioc-subdev-g-selection>). No new extensions to the `v4l2_subdev_crop` structure will be accepted.

To retrieve the current crop rectangle applications set the `pad` field of a struct `v4l2_subdev_crop` to the desired pad number as reported by the media API and the `which` field to `V4L2_SUBDEV_FORMAT_ACTIVE`. They then call the `VIDIOC_SUBDEV_G_CROP` ioctl with a pointer to this structure. The driver fills the members of the `rect` field or returns `EINVAL` error code if the input arguments are invalid, or if cropping is not supported on the given pad.

To change the current crop rectangle applications set both the `pad` and `which` fields and all members of the `rect` field. They then call the `VIDIOC_SUBDEV_S_CROP` ioctl with a pointer to this structure. The driver verifies the requested crop rectangle, adjusts it based on the hardware capabilities and configures the device. Upon return the struct `v4l2_subdev_crop` contains the current format as would be returned by a `VIDIOC_SUBDEV_G_CROP` call.

Applications can query the device capabilities by setting the `which` to `V4L2_SUBDEV_FORMAT_TRY`. When set, 'try' crop rectangles are not applied to the device by the driver, but are mangled exactly as active crop rectangles and stored in the sub-device file handle. Two applications querying the same sub-device would thus not interact with each other.

If the subdev device node has been registered in read-only mode, calls to `VIDIOC_SUBDEV_S_CROP` are only valid if the `which` field is set to `V4L2_SUBDEV_FORMAT_TRY`, otherwise an error is returned and the errno variable is set to `-EPERM`.

Drivers must not return an error solely because the requested crop rectangle doesn't match the device capabilities. They must instead modify the rectangle to match what the hardware can provide. The modified format should be as close as possible to the original request.





<a id="c-v4l2_subdev_crop"></a>

```c
v4l2_subdev_crop
```

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->


<table>
<caption>struct v4l2_subdev_crop</caption>
<tbody>
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


`which`

</td>
<td>


Crop rectangle to get or set, from enum [v4l2_subdev_format_whence](<~kernel/userspace/userspace-api/media-v4l/vidioc-subdev-g-fmt#rst-v4l2-subdev-format-whence>).

</td>
</tr>
<tr>
<td>


struct `v4l2_rect`

</td>
<td>


`rect`

</td>
<td>


Crop rectangle boundaries, in pixels.

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

  The crop rectangle can't be changed because the pad is currently busy. This can be caused, for instance, by an active video stream on the pad. The ioctl must not be retried without performing another action to fix the problem first. Only returned by `VIDIOC_SUBDEV_S_CROP`

- **EINVAL**

  The struct `v4l2_subdev_crop` `pad` references a non-existing pad, the `which` field has an unsupported value, or cropping is not supported on the given subdev pad.

- **EPERM**

  The `VIDIOC_SUBDEV_S_CROP` ioctl has been called on a read-only subdevice and the `which` field is set to `V4L2_SUBDEV_FORMAT_ACTIVE`.
