---
title: "Colorimetry Control Reference"
type: reference
description: "The Colorimetry class includes controls for High Dynamic Range imaging for representing colors in digital images and video. The controls should be used for video and image encoding and decoding as well as in HDMI receivers and transmitters."
---

<a id="rst-colorimetry-control-reference"></a>
<a id="rst-colorimetry-controls"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

The Colorimetry class includes controls for High Dynamic Range imaging for representing colors in digital images and video. The controls should be used for video and image encoding and decoding as well as in HDMI receivers and transmitters.

<a id="rst-colorimetry-control-ids"></a>

## Colorimetry Control IDs

<a id="rst-colorimetry-control-id"></a>

- **`V4L2_CID_COLORIMETRY_CLASS (class)`**

  The Colorimetry class descriptor. Calling [vidioc_queryctrl](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-queryctrl.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) for this control will return a description of this control class.

- **`V4L2_CID_COLORIMETRY_HDR10_CLL_INFO (struct)`**

  The Content Light Level defines upper bounds for the nominal target brightness light level of the pictures.





<a id="c-v4l2_ctrl_hdr10_cll_info"></a>

```c
v4l2_ctrl_hdr10_cll_info
```


<table>
<caption>struct v4l2_ctrl_hdr10_cll_info</caption>
<tbody>
<tr>
<td>


\__u16

</td>
<td>


`max_content_light_level`

</td>
<td>


The upper bound for the maximum light level among all individual samples for the pictures of a video sequence, cd/m<sup>2</sup>. When equal to 0 no such upper bound is present.

</td>
</tr>
<tr>
<td>


\__u16

</td>
<td>


`max_pic_average_light_level`

</td>
<td>


The upper bound for the maximum average light level among the samples for any individual picture of a video sequence, cd/m<sup>2</sup>. When equal to 0 no such upper bound is present.

</td>
</tr>
</tbody>
</table>

- **`V4L2_CID_COLORIMETRY_HDR10_MASTERING_DISPLAY (struct)`**

  The mastering display defines the color volume (the color primaries, white point and luminance range) of a display considered to be the mastering display for the current video content.





<a id="c-v4l2_ctrl_hdr10_mastering_display"></a>

```c
v4l2_ctrl_hdr10_mastering_display
```


<table>
<caption>struct v4l2_ctrl_hdr10_mastering_display</caption>
<tbody>
<tr>
<td>


\__u16

</td>
<td>


`display_primaries_x[3]`

</td>
<td>


Specifies the normalized x chromaticity coordinate of the color primary component c of the mastering display in increments of 0.00002. For describing the mastering display that uses Red, Green and Blue color primaries, index value c equal to 0 corresponds to the Green primary, c equal to 1 corresponds to Blue primary and c equal to 2 corresponds to the Red color primary.

</td>
</tr>
<tr>
<td>


\__u16

</td>
<td>


`display_primaries_y[3]`

</td>
<td>


Specifies the normalized y chromaticity coordinate of the color primary component c of the mastering display in increments of 0.00002. For describing the mastering display that uses Red, Green and Blue color primaries, index value c equal to 0 corresponds to the Green primary, c equal to 1 corresponds to Blue primary and c equal to 2 corresponds to Red color primary.

</td>
</tr>
<tr>
<td>


\__u16

</td>
<td>


`white_point_x`

</td>
<td>


Specifies the normalized x chromaticity coordinate of the white point of the mastering display in increments of 0.00002.

</td>
</tr>
<tr>
<td>


\__u16

</td>
<td>


`white_point_y`

</td>
<td>


Specifies the normalized y chromaticity coordinate of the white point of the mastering display in increments of 0.00002.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`max_luminance`

</td>
<td>


Specifies the nominal maximum display luminance of the mastering display in units of 0.0001 cd/m<sup>2</sup>.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`min_luminance`

</td>
<td>


specifies the nominal minimum display luminance of the mastering display in units of 0.0001 cd/m<sup>2</sup>.

</td>
</tr>
</tbody>
</table>
