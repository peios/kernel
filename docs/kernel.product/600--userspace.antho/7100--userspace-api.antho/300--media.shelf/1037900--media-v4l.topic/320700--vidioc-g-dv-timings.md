---
title: "ioctl VIDIOC_G_DV_TIMINGS, VIDIOC_S_DV_TIMINGS"
type: reference
description: "VIDIOC_G_DV_TIMINGS - VIDIOC_S_DV_TIMINGS - VIDIOC_SUBDEV_G_DV_TIMINGS - VIDIOC_SUBDEV_S_DV_TIMINGS - Get or set DV timings for input or output"
---

<a id="rst-ioctl-vidioc-g-dv-timings-vidioc-s-dv-timings"></a>
<a id="rst-vidioc-g-dv-timings"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_G_DV_TIMINGS - VIDIOC_S_DV_TIMINGS - VIDIOC_SUBDEV_G_DV_TIMINGS - VIDIOC_SUBDEV_S_DV_TIMINGS - Get or set DV timings for input or output

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_G_DV_TIMINGS"></a>

```c
VIDIOC_G_DV_TIMINGS
```

`int ioctl(int fd, VIDIOC_G_DV_TIMINGS, struct v4l2_dv_timings *argp)`





<a id="c-VIDIOC_S_DV_TIMINGS"></a>

```c
VIDIOC_S_DV_TIMINGS
```

`int ioctl(int fd, VIDIOC_S_DV_TIMINGS, struct v4l2_dv_timings *argp)`





<a id="c-VIDIOC_SUBDEV_G_DV_TIMINGS"></a>

```c
VIDIOC_SUBDEV_G_DV_TIMINGS
```

`int ioctl(int fd, VIDIOC_SUBDEV_G_DV_TIMINGS, struct v4l2_dv_timings *argp)`





<a id="c-VIDIOC_SUBDEV_S_DV_TIMINGS"></a>

```c
VIDIOC_SUBDEV_S_DV_TIMINGS
```

`int ioctl(int fd, VIDIOC_SUBDEV_S_DV_TIMINGS, struct v4l2_dv_timings *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_dv_timings`.

<a id="rst-description"></a>

## Description

To set DV timings for the input or output, applications use the [VIDIOC_S_DV_TIMINGS](<#rst-vidioc-g-dv-timings>) ioctl and to get the current timings, applications use the [VIDIOC_G_DV_TIMINGS](<#rst-vidioc-g-dv-timings>) ioctl. The detailed timing information is filled in using the structure struct `v4l2_dv_timings`. These ioctls take a pointer to the struct `v4l2_dv_timings` structure as argument. If the ioctl is not supported or the timing values are not correct, the driver returns `EINVAL` error code.

Calling `VIDIOC_SUBDEV_S_DV_TIMINGS` on a subdev device node that has been registered in read-only mode is not allowed. An error is returned and the errno variable is set to `-EPERM`.

The `linux/v4l2-dv-timings.h` header can be used to get the timings of the formats in the [CEA-861-E](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-cea861>) and [VESA DMT](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-vesadmt>) standards. If the current input or output does not support DV timings (e.g. if [ioctl VIDIOC_ENUMINPUT](<~kernel/userspace/userspace-api/media-v4l/vidioc-enuminput#rst-vidioc-enuminput>) does not set the `V4L2_IN_CAP_DV_TIMINGS` flag), then `ENODATA` error code is returned.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  This ioctl is not supported, or the [VIDIOC_S_DV_TIMINGS](<#rst-vidioc-g-dv-timings>) parameter was unsuitable.

- **ENODATA**

  Digital video timings are not supported for this input or output.

- **EBUSY**

  The device is busy and therefore can not change the timings.

- **EPERM**

  `VIDIOC_SUBDEV_S_DV_TIMINGS` has been called on a read-only subdevice.





<a id="c-v4l2_bt_timings"></a>

```c
v4l2_bt_timings
```

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->


<table>
<caption>struct v4l2_bt_timings</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`width`

</td>
<td>


Width of the active video in pixels.

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


Height of the active video frame in lines. So for interlaced formats the height of the active video in each field is `height`/2.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`interlaced`

</td>
<td>


Progressive (`V4L2_DV_PROGRESSIVE`) or interlaced (`V4L2_DV_INTERLACED`).

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`polarities`

</td>
<td>


This is a bit mask that defines polarities of sync signals. bit 0 (`V4L2_DV_VSYNC_POS_POL`) is for vertical sync polarity and bit 1 (`V4L2_DV_HSYNC_POS_POL`) is for horizontal sync polarity. If the bit is set (1) it is positive polarity and if is cleared (0), it is negative polarity.

</td>
</tr>
<tr>
<td>


\__u64

</td>
<td>


`pixelclock`

</td>
<td>


Pixel clock in Hz. Ex. 74.25MHz-&gt;74250000

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`hfrontporch`

</td>
<td>


Horizontal front porch in pixels

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`hsync`

</td>
<td>


Horizontal sync length in pixels

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`hbackporch`

</td>
<td>


Horizontal back porch in pixels

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`vfrontporch`

</td>
<td>


Vertical front porch in lines. For interlaced formats this refers to the odd field (aka field 1).

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`vsync`

</td>
<td>


Vertical sync length in lines. For interlaced formats this refers to the odd field (aka field 1).

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`vbackporch`

</td>
<td>


Vertical back porch in lines. For interlaced formats this refers to the odd field (aka field 1).

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`il_vfrontporch`

</td>
<td>


Vertical front porch in lines for the even field (aka field 2) of interlaced field formats. Must be 0 for progressive formats.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`il_vsync`

</td>
<td>


Vertical sync length in lines for the even field (aka field 2) of interlaced field formats. Must be 0 for progressive formats.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`il_vbackporch`

</td>
<td>


Vertical back porch in lines for the even field (aka field 2) of interlaced field formats. Must be 0 for progressive formats.

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


The video standard(s) this format belongs to. This will be filled in by the driver. Applications must set this to 0. See [dv-bt-standards](<#rst-dv-bt-standards>) for a list of standards.

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


Several flags giving more information about the format. See [dv-bt-flags](<#rst-dv-bt-flags>) for a description of the flags.

</td>
</tr>
<tr>
<td>


struct `v4l2_fract`

</td>
<td>


`picture_aspect`

</td>
<td>


The picture aspect if the pixels are not square. Only valid if the `V4L2_DV_FL_HAS_PICTURE_ASPECT` flag is set.

</td>
</tr>
<tr>
<td>


\__u8

</td>
<td>


`cea861_vic`

</td>
<td>


The Video Identification Code according to the CEA-861 standard. Only valid if the `V4L2_DV_FL_HAS_CEA861_VIC` flag is set.

</td>
</tr>
<tr>
<td>


\__u8

</td>
<td>


`hdmi_vic`

</td>
<td>


The Video Identification Code according to the HDMI standard. Only valid if the `V4L2_DV_FL_HAS_HDMI_VIC` flag is set.

</td>
</tr>
<tr>
<td>


\__u8

</td>
<td>


`reserved[46]`

</td>
<td>


Reserved for future extensions. Drivers and applications must set the array to zero.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{3.5cm}|p{3.5cm}|p{7.0cm}|p{3.1cm}| -->





<a id="c-v4l2_dv_timings"></a>

```c
v4l2_dv_timings
```


<table>
<caption>struct v4l2_dv_timings</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`type`

</td>
<td>


Type of DV timings as listed in [dv-timing-types](<#rst-dv-timing-types>).

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


struct `v4l2_bt_timings`

</td>
<td>


`bt`

</td>
<td>


Timings defined by BT.656/1120 specifications

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`reserved`\[32\]

</td>
<td>




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

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->

<a id="rst-dv-timing-types"></a>


<table>
<caption>DV Timing types</caption>
<tbody>
<tr>
<td>


Timing type

</td>
<td>


value

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
<td>




</td>
</tr>
<tr>
<td>


`V4L2_DV_BT_656_1120`

</td>
<td>


0

</td>
<td>


BT.656/1120 timings

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{6.5cm}|p{11.0cm}| -->

<a id="rst-dv-bt-standards"></a>


<table>
<caption>DV BT Timing standards</caption>
<tbody>
<tr>
<td>


Timing standard

</td>
<td>


Description

</td>
</tr>
<tr>
<td>


`V4L2_DV_BT_STD_CEA861`

</td>
<td>


The timings follow the CEA-861 Digital TV Profile standard

</td>
</tr>
<tr>
<td>


`V4L2_DV_BT_STD_DMT`

</td>
<td>


The timings follow the VESA Discrete Monitor Timings standard

</td>
</tr>
<tr>
<td>


`V4L2_DV_BT_STD_CVT`

</td>
<td>


The timings follow the VESA Coordinated Video Timings standard

</td>
</tr>
<tr>
<td>


`V4L2_DV_BT_STD_GTF`

</td>
<td>


The timings follow the VESA Generalized Timings Formula standard

</td>
</tr>
<tr>
<td>


`V4L2_DV_BT_STD_SDI`

</td>
<td>


The timings follow the SDI Timings standard. There are no horizontal syncs/porches at all in this format. Total blanking timings must be set in hsync or vsync fields only.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{7.7cm}|p{9.8cm}| -->

<a id="rst-dv-bt-flags"></a>


<table>
<caption>DV BT Timing flags</caption>
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


`V4L2_DV_FL_REDUCED_BLANKING`

</td>
<td>


CVT/GTF specific: the timings use reduced blanking (CVT) or the 'Secondary GTF' curve (GTF). In both cases the horizontal and/or vertical blanking intervals are reduced, allowing a higher resolution over the same bandwidth. This is a read-only flag, applications must not set this.

</td>
</tr>
<tr>
<td>


`V4L2_DV_FL_CAN_REDUCE_FPS`

</td>
<td>


CEA-861 specific: set for CEA-861 formats with a framerate that is a multiple of six. These formats can be optionally played at 1 / 1.001 speed to be compatible with 60 Hz based standards such as NTSC and PAL-M that use a framerate of 29.97 frames per second. If the transmitter can't generate such frequencies, then the flag will also be cleared. This is a read-only flag, applications must not set this.

</td>
</tr>
<tr>
<td>


`V4L2_DV_FL_REDUCED_FPS`

</td>
<td>


CEA-861 specific: only valid for video transmitters or video receivers that have the `V4L2_DV_FL_CAN_DETECT_REDUCED_FPS` set. This flag is cleared otherwise. It is also only valid for formats with the `V4L2_DV_FL_CAN_REDUCE_FPS` flag set, for other formats the flag will be cleared by the driver.

If the application sets this flag for a transmitter, then the pixelclock used to set up the transmitter is divided by 1.001 to make it compatible with NTSC framerates. If the transmitter can't generate such frequencies, then the flag will be cleared.

If a video receiver detects that the format uses a reduced framerate, then it will set this flag to signal this to the application.

</td>
</tr>
<tr>
<td>


`V4L2_DV_FL_HALF_LINE`

</td>
<td>


Specific to interlaced formats: if set, then the vertical frontporch of field 1 (aka the odd field) is really one half-line longer and the vertical backporch of field 2 (aka the even field) is really one half-line shorter, so each field has exactly the same number of half-lines. Whether half-lines can be detected or used depends on the hardware.

</td>
</tr>
<tr>
<td>


`V4L2_DV_FL_IS_CE_VIDEO`

</td>
<td>


If set, then this is a Consumer Electronics (CE) video format. Such formats differ from other formats (commonly called IT formats) in that if R'G'B' encoding is used then by default the R'G'B' values use limited range (i.e. 16-235) as opposed to full range (i.e. 0-255). All formats defined in CEA-861 except for the 640x480p59.94 format are CE formats.

</td>
</tr>
<tr>
<td>


`V4L2_DV_FL_FIRST_FIELD_EXTRA_LINE`

</td>
<td>


Some formats like SMPTE-125M have an interlaced signal with a odd total height. For these formats, if this flag is set, the first field has the extra line. Else, it is the second field.

</td>
</tr>
<tr>
<td>


`V4L2_DV_FL_HAS_PICTURE_ASPECT`

</td>
<td>


If set, then the picture_aspect field is valid. Otherwise assume that the pixels are square, so the picture aspect ratio is the same as the width to height ratio.

</td>
</tr>
<tr>
<td>


`V4L2_DV_FL_HAS_CEA861_VIC`

</td>
<td>


If set, then the cea861_vic field is valid and contains the Video Identification Code as per the CEA-861 standard.

</td>
</tr>
<tr>
<td>


`V4L2_DV_FL_HAS_HDMI_VIC`

</td>
<td>


If set, then the hdmi_vic field is valid and contains the Video Identification Code as per the HDMI standard (HDMI Vendor Specific InfoFrame).

</td>
</tr>
<tr>
<td>


`V4L2_DV_FL_CAN_DETECT_REDUCED_FPS`

</td>
<td>


CEA-861 specific: only valid for video receivers, the flag is cleared by transmitters. If set, then the hardware can detect the difference between regular framerates and framerates reduced by 1000/1001. E.g.: 60 vs 59.94 Hz, 30 vs 29.97 Hz or 24 vs 23.976 Hz.

</td>
</tr>
</tbody>
</table>
