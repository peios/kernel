---
title: "Multi-planar format structures"
type: reference
description: "The struct v4l2_plane_pix_format structures define size and layout for each of the planes in a multi-planar format. The struct v4l2_pix_format_mplane structure contains information common to all planes (such as image width and height) and…"
---

<a id="rst-multi-planar-format-structures"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

The struct `v4l2_plane_pix_format` structures define size and layout for each of the planes in a multi-planar format. The struct `v4l2_pix_format_mplane` structure contains information common to all planes (such as image width and height) and an array of struct `v4l2_plane_pix_format` structures, describing all planes of that format.

<!-- tabularcolumns: |p{1.4cm}|p{4.0cm}|p{11.9cm}| -->

<a id="c-v4l2_plane_pix_format"></a>



```c
v4l2_plane_pix_format
```


<table>
<caption>

struct v4l2\_plane\_pix\_format

</caption>
<tbody>
<tr>
<td>



\_\_u32

</td>
<td>



`sizeimage`

</td>
<td>



Maximum size in bytes required for image data in this plane, set by the driver. When the image consists of variable length compressed data this is the number of bytes required by the codec to support the worst-case compression scenario.

The driver will set the value for uncompressed images.

Clients are allowed to set the sizeimage field for variable length compressed data flagged with `V4L2_FMT_FLAG_COMPRESSED` at [vidioc\_enum\_fmt](<~kernel/userspace/userspace-api/media-v4l/vidioc-enum-fmt#rst-vidioc-enum-fmt>), but the driver may ignore it and set the value itself, or it may modify the provided value based on alignment requirements or minimum/maximum size requirements. If the client wants to leave this to the driver, then it should set sizeimage to 0.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`bytesperline`

</td>
<td>



Distance in bytes between the leftmost pixels in two adjacent lines. See struct `v4l2_pix_format`.

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`reserved[6]`

</td>
<td>



Reserved for future extensions. Should be zeroed by drivers and applications.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{4.4cm}|p{5.6cm}|p{7.3cm}| -->

<a id="c-v4l2_pix_format_mplane"></a>



```c
v4l2_pix_format_mplane
```


<table>
<caption>

struct v4l2\_pix\_format\_mplane

</caption>
<tbody>
<tr>
<td>



\_\_u32

</td>
<td>



`width`

</td>
<td>



Image width in pixels. See struct `v4l2_pix_format`.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`height`

</td>
<td>



Image height in pixels. See struct `v4l2_pix_format`.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`pixelformat`

</td>
<td>



The pixel format. Both single- and multi-planar four character codes can be used.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`field`

</td>
<td>



Field order, from enum `v4l2_field`. See struct `v4l2_pix_format`.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`colorspace`

</td>
<td>



Colorspace encoding, from enum `v4l2_colorspace`. See struct `v4l2_pix_format`.

</td>
</tr>
<tr>
<td>



struct `v4l2_plane_pix_format`

</td>
<td>



`plane_fmt[VIDEO_MAX_PLANES]`

</td>
<td>



An array of structures describing format of each plane this pixel format consists of. The number of valid entries in this array has to be put in the `num_planes` field.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`num_planes`

</td>
<td>



Number of planes (i.e. separate memory buffers) for this format and the number of valid entries in the `plane_fmt` array.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`flags`

</td>
<td>



Flags set by the application or driver, see [format-flags](<~kernel/userspace/userspace-api/media-v4l/pixfmt-v4l2#rst-format-flags>).

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



\_\_u8

</td>
<td>



`ycbcr_enc`

</td>
<td>



Y'CbCr encoding, from enum `v4l2_ycbcr_encoding`. See struct `v4l2_pix_format`.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`hsv_enc`

</td>
<td>



HSV encoding, from enum `v4l2_hsv_encoding`. See struct `v4l2_pix_format`.

</td>
</tr>
<tr>
<td>



\}

</td>
<td colspan="2">





</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`quantization`

</td>
<td>



Quantization range, from enum `v4l2_quantization`. See struct `v4l2_pix_format`.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`xfer_func`

</td>
<td>



Transfer function, from enum `v4l2_xfer_func`. See struct `v4l2_pix_format`.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`reserved[7]`

</td>
<td>



Reserved for future extensions. Should be zeroed by drivers and applications.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->
