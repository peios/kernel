---
title: "ioctl VIDIOC_ENUM_DV_TIMINGS, VIDIOC_SUBDEV_ENUM_DV_TIMINGS"
type: reference
description: "VIDIOC_ENUM_DV_TIMINGS - VIDIOC_SUBDEV_ENUM_DV_TIMINGS - Enumerate supported Digital Video timings"
---

<a id="rst-ioctl-vidioc-enum-dv-timings-vidioc-subdev-enum-dv-timings"></a>
<a id="rst-vidioc-enum-dv-timings"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_ENUM_DV_TIMINGS - VIDIOC_SUBDEV_ENUM_DV_TIMINGS - Enumerate supported Digital Video timings

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_ENUM_DV_TIMINGS"></a>

```c
VIDIOC_ENUM_DV_TIMINGS
```

`int ioctl(int fd, VIDIOC_ENUM_DV_TIMINGS, struct v4l2_enum_dv_timings *argp)`





<a id="c-VIDIOC_SUBDEV_ENUM_DV_TIMINGS"></a>

```c
VIDIOC_SUBDEV_ENUM_DV_TIMINGS
```

`int ioctl(int fd, VIDIOC_SUBDEV_ENUM_DV_TIMINGS, struct v4l2_enum_dv_timings *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_enum_dv_timings`.

<a id="rst-description"></a>

## Description

While some DV receivers or transmitters support a wide range of timings, others support only a limited number of timings. With this ioctl applications can enumerate a list of known supported timings. Call [ioctl VIDIOC_DV_TIMINGS_CAP, VIDIOC_SUBDEV_DV_TIMINGS_CAP](<~kernel/userspace/userspace-api/media-v4l/vidioc-dv-timings-cap#rst-vidioc-dv-timings-cap>) to check if it also supports other standards or even custom timings that are not in this list.

To query the available timings, applications initialize the `index` field, set the `pad` field to 0, zero the reserved array of struct `v4l2_enum_dv_timings` and call the `VIDIOC_ENUM_DV_TIMINGS` ioctl on a video node with a pointer to this structure. Drivers fill the rest of the structure or return an `EINVAL` error code when the index is out of bounds. To enumerate all supported DV timings, applications shall begin at index zero, incrementing by one until the driver returns `EINVAL`.

> [!NOTE]
>
> Drivers may enumerate a different set of DV timings after switching the video input or output.

When implemented by the driver DV timings of subdevices can be queried by calling the `VIDIOC_SUBDEV_ENUM_DV_TIMINGS` ioctl directly on a subdevice node. The DV timings are specific to inputs (for DV receivers) or outputs (for DV transmitters), applications must specify the desired pad number in the struct `v4l2_enum_dv_timings` `pad` field. Attempts to enumerate timings on a pad that doesn't support them will return an `EINVAL` error code.





<a id="c-v4l2_enum_dv_timings"></a>

```c
v4l2_enum_dv_timings
```

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->


<table>
<caption>struct v4l2_enum_dv_timings</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`index`

</td>
<td>


Number of the DV timings, set by the application.

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


Pad number as reported by the media controller API. This field is only used when operating on a subdevice node. When operating on a video node applications must set this field to zero.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`reserved`\[2\]

</td>
<td>


Reserved for future extensions. Drivers and applications must set the array to zero.

</td>
</tr>
<tr>
<td>


struct `v4l2_dv_timings`

</td>
<td>


`timings`

</td>
<td>


The timings.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  The struct `v4l2_enum_dv_timings` `index` is out of bounds or the `pad` number is invalid.

- **ENODATA**

  Digital video presets are not supported for this input or output.
