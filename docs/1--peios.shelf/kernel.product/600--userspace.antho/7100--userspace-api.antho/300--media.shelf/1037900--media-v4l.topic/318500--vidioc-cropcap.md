---
title: "ioctl VIDIOC_CROPCAP"
type: reference
description: "VIDIOC_CROPCAP - Information about the video cropping and scaling abilities"
---

<a id="rst-ioctl-vidioc-cropcap"></a>
<a id="rst-vidioc-cropcap"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_CROPCAP - Information about the video cropping and scaling abilities

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_CROPCAP"></a>

```c
VIDIOC_CROPCAP
```

`int ioctl(int fd, VIDIOC_CROPCAP, struct v4l2_cropcap *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_cropcap`.

<a id="rst-description"></a>

## Description

Applications use this function to query the cropping limits, the pixel aspect of images and to calculate scale factors. They set the `type` field of a v4l2_cropcap structure to the respective buffer (stream) type and call the [ioctl VIDIOC_CROPCAP](<#rst-vidioc-cropcap>) ioctl with a pointer to this structure. Drivers fill the rest of the structure. The results are constant except when switching the video standard. Remember this switch can occur implicit when switching the video input or output.

This ioctl must be implemented for video capture or output devices that support cropping and/or scaling and/or have non-square pixels, and for overlay devices.





<a id="c-v4l2_cropcap"></a>

```c
v4l2_cropcap
```

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->


<table>
<caption>struct v4l2_cropcap</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`type`

</td>
<td>


Type of the data stream, set by the application. Only these types are valid here: `V4L2_BUF_TYPE_VIDEO_CAPTURE`, `V4L2_BUF_TYPE_VIDEO_CAPTURE_MPLANE`, `V4L2_BUF_TYPE_VIDEO_OUTPUT`, `V4L2_BUF_TYPE_VIDEO_OUTPUT_MPLANE` and `V4L2_BUF_TYPE_VIDEO_OVERLAY`. See `v4l2_buf_type` and the note below.

</td>
</tr>
<tr>
<td>


struct [v4l2_rect](<#rst-v4l2-rect-crop>)

</td>
<td>


`bounds`

</td>
<td>


Defines the window within capturing or output is possible, this may exclude for example the horizontal and vertical blanking areas. The cropping rectangle cannot exceed these limits. Width and height are defined in pixels, the driver writer is free to choose origin and units of the coordinate system in the analog domain.

</td>
</tr>
<tr>
<td>


struct [v4l2_rect](<#rst-v4l2-rect-crop>)

</td>
<td>


`defrect`

</td>
<td>


Default cropping rectangle, it shall cover the "whole picture". Assuming pixel aspect 1/1 this could be for example a 640 × 480 rectangle for NTSC, a 768 × 576 rectangle for PAL and SECAM centered over the active picture area. The same coordinate system as for `bounds` is used.

</td>
</tr>
<tr>
<td>


struct `v4l2_fract`

</td>
<td>


`pixelaspect`

</td>
<td>


This is the pixel aspect (y / x) when no scaling is applied, the ratio of the actual sampling frequency and the frequency required to get square pixels.

When cropping coordinates refer to square pixels, the driver sets `pixelaspect` to 1/1. Other common values are 54/59 for PAL and SECAM, 11/10 for NTSC sampled according to \[[ITU BT.601](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-itu601>)\].

</td>
</tr>
</tbody>
</table>

> [!NOTE]
>
> Unfortunately in the case of multiplanar buffer types (`V4L2_BUF_TYPE_VIDEO_CAPTURE_MPLANE` and `V4L2_BUF_TYPE_VIDEO_OUTPUT_MPLANE`) this API was messed up with regards to how the `v4l2_cropcap` `type` field should be filled in. Some drivers only accepted the `_MPLANE` buffer type while other drivers only accepted a non-multiplanar buffer type (i.e. without the `_MPLANE` at the end).
>
> Starting with kernel 4.13 both variations are allowed.

<a id="rst-v4l2-rect-crop"></a>



<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->


<table>
<caption>struct v4l2_rect</caption>
<tbody>
<tr>
<td>


\__s32

</td>
<td>


`left`

</td>
<td>


Horizontal offset of the top, left corner of the rectangle, in pixels.

</td>
</tr>
<tr>
<td>


\__s32

</td>
<td>


`top`

</td>
<td>


Vertical offset of the top, left corner of the rectangle, in pixels.

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


Width of the rectangle, in pixels.

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


Height of the rectangle, in pixels.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  The struct `v4l2_cropcap` `type` is invalid.

- **ENODATA**

  Cropping is not supported for this input or output.
