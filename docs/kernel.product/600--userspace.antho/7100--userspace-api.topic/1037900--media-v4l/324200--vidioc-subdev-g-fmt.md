---
title: "ioctl VIDIOC_SUBDEV_G_FMT, VIDIOC_SUBDEV_S_FMT"
type: reference
description: "VIDIOC_SUBDEV_G_FMT - VIDIOC_SUBDEV_S_FMT - Get or set the data format on a subdev pad"
---

<a id="rst-ioctl-vidioc-subdev-g-fmt-vidioc-subdev-s-fmt"></a>
<a id="rst-vidioc-subdev-g-fmt"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_SUBDEV_G_FMT - VIDIOC_SUBDEV_S_FMT - Get or set the data format on a subdev pad

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_SUBDEV_G_FMT"></a>

```c
VIDIOC_SUBDEV_G_FMT
```

`int ioctl(int fd, VIDIOC_SUBDEV_G_FMT, struct v4l2_subdev_format *argp)`





<a id="c-VIDIOC_SUBDEV_S_FMT"></a>

```c
VIDIOC_SUBDEV_S_FMT
```

`int ioctl(int fd, VIDIOC_SUBDEV_S_FMT, struct v4l2_subdev_format *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_subdev_format`.

<a id="rst-description"></a>

## Description

These ioctls are used to negotiate the frame format at specific subdev pads in the image pipeline.

To retrieve the current format applications set the `pad` field of a struct `v4l2_subdev_format` to the desired pad number as reported by the media API and the `which` field to `V4L2_SUBDEV_FORMAT_ACTIVE`. When they call the `VIDIOC_SUBDEV_G_FMT` ioctl with a pointer to this structure the driver fills the members of the `format` field.

To change the current format applications set both the `pad` and `which` fields and all members of the `format` field. When they call the `VIDIOC_SUBDEV_S_FMT` ioctl with a pointer to this structure the driver verifies the requested format, adjusts it based on the hardware capabilities and configures the device. Upon return the struct `v4l2_subdev_format` contains the current format as would be returned by a `VIDIOC_SUBDEV_G_FMT` call.

Applications can query the device capabilities by setting the `which` to `V4L2_SUBDEV_FORMAT_TRY`. When set, 'try' formats are not applied to the device by the driver, but are changed exactly as active formats and stored in the sub-device file handle. Two applications querying the same sub-device would thus not interact with each other.

For instance, to try a format at the output pad of a sub-device, applications would first set the try format at the sub-device input with the `VIDIOC_SUBDEV_S_FMT` ioctl. They would then either retrieve the default format at the output pad with the `VIDIOC_SUBDEV_G_FMT` ioctl, or set the desired output pad format with the `VIDIOC_SUBDEV_S_FMT` ioctl and check the returned value.

Try formats do not depend on active formats, but can depend on the current links configuration or sub-device controls value. For instance, a low-pass noise filter might crop pixels at the frame boundaries, modifying its output frame size.

If the subdev device node has been registered in read-only mode, calls to `VIDIOC_SUBDEV_S_FMT` are only valid if the `which` field is set to `V4L2_SUBDEV_FORMAT_TRY`, otherwise an error is returned and the errno variable is set to `-EPERM`.

Drivers must not return an error solely because the requested format doesn't match the device capabilities. They must instead modify the format to match what the hardware can provide. The modified format should be as close as possible to the original request.

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->





<a id="c-v4l2_subdev_format"></a>

```c
v4l2_subdev_format
```


<table>
<caption>struct v4l2_subdev_format</caption>
<tbody>
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


`which`

</td>
<td>


Format to modified, from enum [v4l2_subdev_format_whence](<#rst-v4l2-subdev-format-whence>).

</td>
</tr>
<tr>
<td>


struct `v4l2_mbus_framefmt`

</td>
<td>


`format`

</td>
<td>


Definition of an image format, see `v4l2_mbus_framefmt` for details.

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

<!-- tabularcolumns: |p{6.6cm}|p{2.2cm}|p{8.5cm}| -->

<a id="rst-v4l2-subdev-format-whence"></a>


<table>
<caption>enum v4l2_subdev_format_whence</caption>
<tbody>
<tr>
<td>


V4L2_SUBDEV_FORMAT_TRY

</td>
<td>


0

</td>
<td>


Try formats, used for querying device capabilities.

</td>
</tr>
<tr>
<td>


V4L2_SUBDEV_FORMAT_ACTIVE

</td>
<td>


1

</td>
<td>


Active formats, applied to the hardware.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EBUSY**

  The format can't be changed because the pad is currently busy. This can be caused, for instance, by an active video stream on the pad. The ioctl must not be retried without performing another action to fix the problem first. Only returned by `VIDIOC_SUBDEV_S_FMT`

- **EINVAL**

  The struct `v4l2_subdev_format` `pad` references a non-existing pad, or the `which` field has an unsupported value.

- **EPERM**

  The `VIDIOC_SUBDEV_S_FMT` ioctl has been called on a read-only subdevice and the `which` field is set to `V4L2_SUBDEV_FORMAT_ACTIVE`.

---

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
