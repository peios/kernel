---
title: "ioctl VIDIOC_SUBDEV_G_FRAME_INTERVAL, VIDIOC_SUBDEV_S_FRAME_INTERVAL"
type: reference
description: "VIDIOC_SUBDEV_G_FRAME_INTERVAL - VIDIOC_SUBDEV_S_FRAME_INTERVAL - Get or set the frame interval on a subdev pad"
---

<a id="rst-ioctl-vidioc-subdev-g-frame-interval-vidioc-subdev-s-frame-interval"></a>
<a id="rst-vidioc-subdev-g-frame-interval"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_SUBDEV_G_FRAME_INTERVAL - VIDIOC_SUBDEV_S_FRAME_INTERVAL - Get or set the frame interval on a subdev pad

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_SUBDEV_G_FRAME_INTERVAL"></a>

```c
VIDIOC_SUBDEV_G_FRAME_INTERVAL
```

`int ioctl(int fd, VIDIOC_SUBDEV_G_FRAME_INTERVAL, struct v4l2_subdev_frame_interval *argp)`





<a id="c-VIDIOC_SUBDEV_S_FRAME_INTERVAL"></a>

```c
VIDIOC_SUBDEV_S_FRAME_INTERVAL
```

`int ioctl(int fd, VIDIOC_SUBDEV_S_FRAME_INTERVAL, struct v4l2_subdev_frame_interval *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_subdev_frame_interval`.

<a id="rst-description"></a>

## Description

These ioctls are used to get and set the frame interval at specific subdev pads in the image pipeline. The frame interval only makes sense for sub-devices that can control the frame period on their own. This includes, for instance, image sensors and TV tuners. Sub-devices that don't support frame intervals must not implement these ioctls.

To retrieve the current frame interval applications set the `pad` field of a struct `v4l2_subdev_frame_interval` to the desired pad number as reported by the media controller API. When they call the `VIDIOC_SUBDEV_G_FRAME_INTERVAL` ioctl with a pointer to this structure the driver fills the members of the `interval` field.

To change the current frame interval applications set both the `pad` field and all members of the `interval` field. When they call the `VIDIOC_SUBDEV_S_FRAME_INTERVAL` ioctl with a pointer to this structure the driver verifies the requested interval, adjusts it based on the hardware capabilities and configures the device. Upon return the struct `v4l2_subdev_frame_interval` contains the current frame interval as would be returned by a `VIDIOC_SUBDEV_G_FRAME_INTERVAL` call.

If the subdev device node has been registered in read-only mode, calls to `VIDIOC_SUBDEV_S_FRAME_INTERVAL` are only valid if the `which` field is set to `V4L2_SUBDEV_FORMAT_TRY`, otherwise an error is returned and the errno variable is set to `-EPERM`.

Drivers must not return an error solely because the requested interval doesn't match the device capabilities. They must instead modify the interval to match what the hardware can provide. The modified interval should be as close as possible to the original request.

Changing the frame interval shall never change the format. Changing the format, on the other hand, may change the frame interval.

Sub-devices that support the frame interval ioctls should implement them on a single pad only. Their behaviour when supported on multiple pads of the same sub-device is not defined.





<a id="c-v4l2_subdev_frame_interval"></a>

```c
v4l2_subdev_frame_interval
```

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->


<table>
<caption>struct v4l2_subdev_frame_interval</caption>
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


`which`

</td>
<td>


Active or try frame interval, from enum [v4l2_subdev_format_whence](<~kernel/userspace/userspace-api/media-v4l/vidioc-subdev-g-fmt#rst-v4l2-subdev-format-whence>).

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

  The frame interval can't be changed because the pad is currently busy. This can be caused, for instance, by an active video stream on the pad. The ioctl must not be retried without performing another action to fix the problem first. Only returned by `VIDIOC_SUBDEV_S_FRAME_INTERVAL`

- **EINVAL**

  The struct `v4l2_subdev_frame_interval` `pad` references a non-existing pad, the `which` field has an unsupported value, or the pad doesn't support frame intervals.

- **EPERM**

  The `VIDIOC_SUBDEV_S_FRAME_INTERVAL` ioctl has been called on a read-only subdevice and the `which` field is set to `V4L2_SUBDEV_FORMAT_ACTIVE`.
