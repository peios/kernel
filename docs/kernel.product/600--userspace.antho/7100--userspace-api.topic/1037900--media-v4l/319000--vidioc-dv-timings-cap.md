---
title: "ioctl VIDIOC_DV_TIMINGS_CAP, VIDIOC_SUBDEV_DV_TIMINGS_CAP"
type: reference
description: "VIDIOC_DV_TIMINGS_CAP - VIDIOC_SUBDEV_DV_TIMINGS_CAP - The capabilities of the Digital Video receiver/transmitter"
---

<a id="rst-ioctl-vidioc-dv-timings-cap-vidioc-subdev-dv-timings-cap"></a>
<a id="rst-vidioc-dv-timings-cap"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_DV_TIMINGS_CAP - VIDIOC_SUBDEV_DV_TIMINGS_CAP - The capabilities of the Digital Video receiver/transmitter

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_DV_TIMINGS_CAP"></a>

```c
VIDIOC_DV_TIMINGS_CAP
```

`int ioctl(int fd, VIDIOC_DV_TIMINGS_CAP, struct v4l2_dv_timings_cap *argp)`





<a id="c-VIDIOC_SUBDEV_DV_TIMINGS_CAP"></a>

```c
VIDIOC_SUBDEV_DV_TIMINGS_CAP
```

`int ioctl(int fd, VIDIOC_SUBDEV_DV_TIMINGS_CAP, struct v4l2_dv_timings_cap *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_dv_timings_cap`.

<a id="rst-description"></a>

## Description

To query the capabilities of the DV receiver/transmitter applications initialize the `pad` field to 0, zero the reserved array of struct `v4l2_dv_timings_cap` and call the `VIDIOC_DV_TIMINGS_CAP` ioctl on a video node and the driver will fill in the structure.

> [!NOTE]
>
> Drivers may return different values after switching the video input or output.

When implemented by the driver DV capabilities of subdevices can be queried by calling the `VIDIOC_SUBDEV_DV_TIMINGS_CAP` ioctl directly on a subdevice node. The capabilities are specific to inputs (for DV receivers) or outputs (for DV transmitters), applications must specify the desired pad number in the struct `v4l2_dv_timings_cap` `pad` field and zero the `reserved` array. Attempts to query capabilities on a pad that doesn't support them will return an `EINVAL` error code.

<!-- tabularcolumns: |p{1.2cm}|p{3.2cm}|p{12.9cm}| -->





<a id="c-v4l2_bt_timings_cap"></a>

```c
v4l2_bt_timings_cap
```


<table>
<caption>struct v4l2_bt_timings_cap</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`min_width`

</td>
<td>


Minimum width of the active video in pixels.

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


Maximum width of the active video in pixels.

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


Minimum height of the active video in lines.

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


Maximum height of the active video in lines.

</td>
</tr>
<tr>
<td>


\__u64

</td>
<td>


`min_pixelclock`

</td>
<td>


Minimum pixelclock frequency in Hz.

</td>
</tr>
<tr>
<td>


\__u64

</td>
<td>


`max_pixelclock`

</td>
<td>


Maximum pixelclock frequency in Hz.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`standards`

</td>
<td>


The video standard(s) supported by the hardware. See [dv-bt-standards](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-dv-timings#rst-dv-bt-standards>) for a list of standards.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`capabilities`

</td>
<td>


Several flags giving more information about the capabilities. See [dv-bt-cap-capabilities](<#rst-dv-bt-cap-capabilities>) for a description of the flags.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`reserved`\[16\]

</td>
<td>


Reserved for future extensions. Drivers must set the array to zero.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{4.4cm}|p{3.6cm}|p{9.3cm}| -->





<a id="c-v4l2_dv_timings_cap"></a>

```c
v4l2_dv_timings_cap
```


<table>
<caption>struct v4l2_dv_timings_cap</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`type`

</td>
<td>


Type of DV timings as listed in [dv-timing-types](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-dv-timings#rst-dv-timing-types>).

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


Reserved for future extensions.

Drivers and applications must set the array to zero.

</td>
</tr>
<tr>
<td>


union \{

</td>
<td colspan="2">


(anonymous)

</td>
</tr>
<tr>
<td>


struct `v4l2_bt_timings_cap`

</td>
<td>


`bt`

</td>
<td>


BT.656/1120 timings capabilities of the hardware.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td colspan="2">


`raw_data`\[32\]

</td>
</tr>
<tr>
<td>


\}

</td>
<td colspan="2">




</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{7.2cm}|p{10.3cm}| -->

<a id="rst-dv-bt-cap-capabilities"></a>


<table>
<caption>DV BT Timing capabilities</caption>
<tbody>
<tr>
<td>


Flag

</td>
<td>


Description

</td>
</tr>
<tr>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


`V4L2_DV_BT_CAP_INTERLACED`

</td>
<td>


Interlaced formats are supported.

</td>
</tr>
<tr>
<td>


`V4L2_DV_BT_CAP_PROGRESSIVE`

</td>
<td>


Progressive formats are supported.

</td>
</tr>
<tr>
<td>


`V4L2_DV_BT_CAP_REDUCED_BLANKING`

</td>
<td>


CVT/GTF specific: the timings can make use of reduced blanking (CVT) or the 'Secondary GTF' curve (GTF).

</td>
</tr>
<tr>
<td>


`V4L2_DV_BT_CAP_CUSTOM`

</td>
<td>


Can support non-standard timings, i.e. timings not belonging to the standards set in the `standards` field.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
