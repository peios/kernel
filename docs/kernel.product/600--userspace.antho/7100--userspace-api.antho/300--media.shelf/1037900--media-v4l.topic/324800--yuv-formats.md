---
title: "YUV Formats"
type: reference
description: "YUV is the format native to TV broadcast and composite video signals. It separates the brightness information (Y) from the color information (U and V or Cb and Cr). The color information consists of red and blue color difference signals,…"
---

<a id="rst-yuv-formats-1"></a>
<a id="rst-yuv-formats"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

YUV is the format native to TV broadcast and composite video signals. It separates the brightness information (Y) from the color information (U and V or Cb and Cr). The color information consists of red and blue *color difference* signals, this way the green component can be reconstructed by subtracting from the brightness component. See [Colorspaces](<~kernel/userspace/userspace-api/media-v4l/colorspaces#rst-colorspaces-1>) for conversion examples. YUV was chosen because early television would only transmit brightness information. To add color in a way compatible with existing receivers a new signal carrier was added to transmit the color difference signals.

<a id="rst-subsampling"></a>

## Subsampling

YUV formats commonly encode images with a lower resolution for the chroma components than for the luma component. This compression technique, taking advantage of the human eye being more sensitive to luminance than color differences, is called chroma subsampling.

While many combinations of subsampling factors in the horizontal and vertical direction are possible, common factors are 1 (no subsampling), 2 and 4, with horizontal subsampling always larger than or equal to vertical subsampling. Common combinations are named as follows.

- `4:4:4`: No subsampling

- `4:2:2`: Horizontal subsampling by 2, no vertical subsampling

- `4:2:0`: Horizontal subsampling by 2, vertical subsampling by 2

- `4:1:1`: Horizontal subsampling by 4, no vertical subsampling

- `4:1:0`: Horizontal subsampling by 4, vertical subsampling by 4

Subsampling the chroma component effectively creates chroma values that can be located in different spatial locations:

- <a id="rst-yuv-chroma-centered"></a>

  The subsampled chroma value may be calculated by simply averaging the chroma value of two consecutive pixels. It effectively models the chroma of a pixel sited between the two original pixels. This is referred to as centered or interstitially sited chroma.

- <a id="rst-yuv-chroma-cosited"></a>

  The other option is to subsample chroma values in a way that place them in the same spatial sites as the pixels. This may be performed by skipping every other chroma sample (creating aliasing artifacts), or with filters using an odd number of taps. This is referred to as co-sited chroma.

The following examples show different combination of chroma siting in a 4x4 image.


<table>
<caption>4:2:2 subsampling, interstitially sited</caption>
<thead>
<tr>
<th>




</th>
<th>


0

</th>
<th>




</th>
<th>


1

</th>
<th>




</th>
<th>


2

</th>
<th>




</th>
<th>


3

</th>
</tr>
</thead>
<tbody>
<tr>
<th scope="row">


0

</th>
<td>


Y

</td>
<td>


C

</td>
<td>


Y

</td>
<td>




</td>
<td>


Y

</td>
<td>


C

</td>
<td>


Y

</td>
</tr>
<tr>
<th scope="row">


1

</th>
<td>


Y

</td>
<td>


C

</td>
<td>


Y

</td>
<td>




</td>
<td>


Y

</td>
<td>


C

</td>
<td>


Y

</td>
</tr>
<tr>
<th scope="row">


2

</th>
<td>


Y

</td>
<td>


C

</td>
<td>


Y

</td>
<td>




</td>
<td>


Y

</td>
<td>


C

</td>
<td>


Y

</td>
</tr>
<tr>
<th scope="row">


3

</th>
<td>


Y

</td>
<td>


C

</td>
<td>


Y

</td>
<td>




</td>
<td>


Y

</td>
<td>


C

</td>
<td>


Y

</td>
</tr>
</tbody>
</table>


<table>
<caption>4:2:2 subsampling, co-sited</caption>
<thead>
<tr>
<th>




</th>
<th>


0

</th>
<th>




</th>
<th>


1

</th>
<th>




</th>
<th>


2

</th>
<th>




</th>
<th>


3

</th>
</tr>
</thead>
<tbody>
<tr>
<th scope="row">


0

</th>
<td>


Y/C

</td>
<td>




</td>
<td>


Y

</td>
<td>




</td>
<td>


Y/C

</td>
<td>




</td>
<td>


Y

</td>
</tr>
<tr>
<th scope="row">


1

</th>
<td>


Y/C

</td>
<td>




</td>
<td>


Y

</td>
<td>




</td>
<td>


Y/C

</td>
<td>




</td>
<td>


Y

</td>
</tr>
<tr>
<th scope="row">


2

</th>
<td>


Y/C

</td>
<td>




</td>
<td>


Y

</td>
<td>




</td>
<td>


Y/C

</td>
<td>




</td>
<td>


Y

</td>
</tr>
<tr>
<th scope="row">


3

</th>
<td>


Y/C

</td>
<td>




</td>
<td>


Y

</td>
<td>




</td>
<td>


Y/C

</td>
<td>




</td>
<td>


Y

</td>
</tr>
</tbody>
</table>


<table>
<caption>4:2:0 subsampling, horizontally interstitially sited, vertically co-sited</caption>
<thead>
<tr>
<th>




</th>
<th>


0

</th>
<th>




</th>
<th>


1

</th>
<th>




</th>
<th>


2

</th>
<th>




</th>
<th>


3

</th>
</tr>
</thead>
<tbody>
<tr>
<th scope="row">


0

</th>
<td>


Y

</td>
<td>


C

</td>
<td>


Y

</td>
<td>




</td>
<td>


Y

</td>
<td>


C

</td>
<td>


Y

</td>
</tr>
<tr>
<th scope="row">


1

</th>
<td>


Y

</td>
<td>




</td>
<td>


Y

</td>
<td>




</td>
<td>


Y

</td>
<td>




</td>
<td>


Y

</td>
</tr>
<tr>
<th scope="row">


2

</th>
<td>


Y

</td>
<td>


C

</td>
<td>


Y

</td>
<td>




</td>
<td>


Y

</td>
<td>


C

</td>
<td>


Y

</td>
</tr>
<tr>
<th scope="row">


3

</th>
<td>


Y

</td>
<td>




</td>
<td>


Y

</td>
<td>




</td>
<td>


Y

</td>
<td>




</td>
<td>


Y

</td>
</tr>
</tbody>
</table>


<table>
<caption>4:1:0 subsampling, horizontally and vertically interstitially sited</caption>
<thead>
<tr>
<th>




</th>
<th>


0

</th>
<th>




</th>
<th>


1

</th>
<th>




</th>
<th>


2

</th>
<th>




</th>
<th>


3

</th>
</tr>
</thead>
<tbody>
<tr>
<th scope="row">


0

</th>
<td>


Y

</td>
<td>




</td>
<td>


Y

</td>
<td>




</td>
<td>


Y

</td>
<td>




</td>
<td>


Y

</td>
</tr>
<tr>
<th scope="row">




</th>
<td>




</td>
<td>




</td>
<td>




</td>
<td>




</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<th scope="row">


1

</th>
<td>


Y

</td>
<td>




</td>
<td>


Y

</td>
<td>




</td>
<td>


Y

</td>
<td>




</td>
<td>


Y

</td>
</tr>
<tr>
<th scope="row">




</th>
<td>




</td>
<td>




</td>
<td>




</td>
<td>


C

</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<th scope="row">


2

</th>
<td>


Y

</td>
<td>




</td>
<td>


Y

</td>
<td>




</td>
<td>


Y

</td>
<td>




</td>
<td>


Y

</td>
</tr>
<tr>
<th scope="row">




</th>
<td>




</td>
<td>




</td>
<td>




</td>
<td>




</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<th scope="row">


3

</th>
<td>


Y

</td>
<td>




</td>
<td>


Y

</td>
<td>




</td>
<td>


Y

</td>
<td>




</td>
<td>


Y

</td>
</tr>
</tbody>
</table>

- [pixfmt-packed-yuv](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/pixfmt-packed-yuv.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)
- [pixfmt-yuv-planar](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/pixfmt-yuv-planar.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)
- [pixfmt-yuv-luma](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/pixfmt-yuv-luma.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)
- [V4L2_PIX_FMT_Y8I ('Y8I ')](<~kernel/userspace/userspace-api/media-v4l/pixfmt-y8i>)
- [V4L2_PIX_FMT_Y12I ('Y12I')](<~kernel/userspace/userspace-api/media-v4l/pixfmt-y12i>)
- [V4L2_PIX_FMT_Y16I ('Y16I')](<~kernel/userspace/userspace-api/media-v4l/pixfmt-y16i>)
- [V4L2_PIX_FMT_UV8 ('UV8')](<~kernel/userspace/userspace-api/media-v4l/pixfmt-uv8>)
- [V4L2_PIX_FMT_M420 ('M420')](<~kernel/userspace/userspace-api/media-v4l/pixfmt-m420>)
