---
title: "Luma-Only Formats"
type: reference
description: "This family of formats only store the luma component of a Y'CbCr image. They are often referred to as greyscale formats."
---

<a id="rst-luma-only-formats"></a>
<a id="rst-yuv-luma-only"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

This family of formats only store the luma component of a Y'CbCr image. They are often referred to as greyscale formats.

> [!NOTE]
>
> - In all the tables that follow, bit 7 is the most significant bit in a byte.
>
> - Formats are described with the minimum number of pixels needed to create a byte-aligned repeating pattern. `...` indicates repetition of the pattern.
>
> - Y'<sub>x</sub>\[9:2\] denotes bits 9 to 2 of the Y' value for pixel at column `x`.
>
> - `0` denotes padding bits set to 0.

<!-- Source LaTeX layout: \tiny -->

<!-- tabularcolumns: |p{3.6cm}|p{2.4cm}|p{1.3cm}|p{1.3cm}|p{1.3cm}|p{1.3cm}|p{1.3cm}|p{1.3cm}|p{1.3cm}| -->


<table>
<caption>

Luma-Only Image Formats

</caption>
<thead>
<tr>
<th>



Identifier

</th>
<th>



Code

</th>
<th>



Byte 0

</th>
<th>



Byte 1

</th>
<th>



Byte 2

</th>
<th>



Byte 3

</th>
<th>



Byte 4

</th>
<th>



Byte 5

</th>
<th>



Byte 6

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



`V4L2_PIX_FMT_GREY`

</td>
<td>



'GREY'

</td>
<td>



Y'<sub>0</sub>\[7:0\]

</td>
<td>



...

</td>
<td>



...

</td>
<td>



...

</td>
<td>



...

</td>
<td>



...

</td>
<td>



<a id="rst-v4l2-pix-fmt-grey"></a>

...

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_IPU3_Y10`

</td>
<td>



'ip3y'

</td>
<td>



Y'<sub>0</sub>\[7:0\]

</td>
<td>



Y'<sub>1</sub>\[5:0\] Y'<sub>0</sub>\[9:8\]

</td>
<td>



Y'<sub>2</sub>\[3:0\] Y'<sub>1</sub>\[9:6\]

</td>
<td>



Y'<sub>3</sub>\[1:0\] Y'<sub>2</sub>\[9:4\]

</td>
<td>



Y'<sub>3</sub>\[9:2\]

</td>
<td>



...

</td>
<td>



<a id="rst-v4l2-pix-fmt-ipu3-y10"></a>

...

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_Y10`

</td>
<td>



'Y10 '

</td>
<td>



Y'<sub>0</sub>\[7:0\]

</td>
<td>



`000000` Y'<sub>0</sub>\[9:8\]

</td>
<td>



...

</td>
<td>



...

</td>
<td>



...

</td>
<td>



...

</td>
<td>



<a id="rst-v4l2-pix-fmt-y10"></a>

...

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_Y10BPACK`

</td>
<td>



'Y10B'

</td>
<td>



Y'<sub>0</sub>\[9:2\]

</td>
<td>



Y'<sub>0</sub>\[1:0\] Y'<sub>1</sub>\[9:4\]

</td>
<td>



Y'<sub>1</sub>\[3:0\] Y'<sub>2</sub>\[9:6\]

</td>
<td>



Y'<sub>2</sub>\[5:0\] Y'<sub>3</sub>\[9:8\]

</td>
<td>



Y'<sub>3</sub>\[7:0\]

</td>
<td>



...

</td>
<td>



<a id="rst-v4l2-pix-fmt-y10bpack"></a>

...

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_Y10P`

</td>
<td>



'Y10P'

</td>
<td>



Y'<sub>0</sub>\[9:2\]

</td>
<td>



Y'<sub>1</sub>\[9:2\]

</td>
<td>



Y'<sub>2</sub>\[9:2\]

</td>
<td>



Y'<sub>3</sub>\[9:2\]

</td>
<td>



Y'<sub>3</sub>\[1:0\] Y'<sub>2</sub>\[1:0\] Y'<sub>1</sub>\[1:0\] Y'<sub>0</sub>\[1:0\]

</td>
<td>



...

</td>
<td>



<a id="rst-v4l2-pix-fmt-y10p"></a>

...

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_Y12`

</td>
<td>



'Y12 '

</td>
<td>



Y'<sub>0</sub>\[7:0\]

</td>
<td>



`0000` Y'<sub>0</sub>\[11:8\]

</td>
<td>



...

</td>
<td>



...

</td>
<td>



...

</td>
<td>



...

</td>
<td>



<a id="rst-v4l2-pix-fmt-y12"></a>

...

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_Y012`

</td>
<td>



'Y012'

</td>
<td>



Y'<sub>0</sub>\[3:0\] `0000`

</td>
<td>



Y'<sub>0</sub>\[11:4\]

</td>
<td>



...

</td>
<td>



...

</td>
<td>



...

</td>
<td>



...

</td>
<td>



<a id="rst-v4l2-pix-fmt-y012"></a>

...

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_Y12P`

</td>
<td>



'Y12P'

</td>
<td>



Y'<sub>0</sub>\[11:4\]

</td>
<td>



Y'<sub>1</sub>\[11:4\]

</td>
<td>



Y'<sub>1</sub>\[3:0\] Y'<sub>0</sub>\[3:0\]

</td>
<td>



...

</td>
<td>



...

</td>
<td>



...

</td>
<td>



<a id="rst-v4l2-pix-fmt-y12p"></a>

...

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_Y14`

</td>
<td>



'Y14 '

</td>
<td>



Y'<sub>0</sub>\[7:0\]

</td>
<td>



`00` Y'<sub>0</sub>\[13:8\]

</td>
<td>



...

</td>
<td>



...

</td>
<td>



...

</td>
<td>



...

</td>
<td>



<a id="rst-v4l2-pix-fmt-y14"></a>

...

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_Y14P`

</td>
<td>



'Y14P'

</td>
<td>



Y'<sub>0</sub>\[13:6\]

</td>
<td>



Y'<sub>1</sub>\[13:6\]

</td>
<td>



Y'<sub>2</sub>\[13:6\]

</td>
<td>



Y'<sub>3</sub>\[13:6\]

</td>
<td>



Y'<sub>1</sub>\[1:0\] Y'<sub>0</sub>\[5:0\]

</td>
<td>



Y'<sub>2</sub>\[3:0\] Y'<sub>1</sub>\[5:2\]

</td>
<td>



<a id="rst-v4l2-pix-fmt-y14p"></a>

Y'<sub>3</sub>\[5:0\] Y'<sub>2</sub>\[5:4\]

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_Y16`

</td>
<td>



'Y16 '

</td>
<td>



Y'<sub>0</sub>\[7:0\]

</td>
<td>



Y'<sub>0</sub>\[15:8\]

</td>
<td>



...

</td>
<td>



...

</td>
<td>



...

</td>
<td>



...

</td>
<td>



<a id="rst-v4l2-pix-fmt-y16"></a>

...

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_Y16_BE`

</td>
<td>



'Y16 ' \| (1U &lt;&lt; 31)

</td>
<td>



Y'<sub>0</sub>\[15:8\]

</td>
<td>



Y'<sub>0</sub>\[7:0\]

</td>
<td>



...

</td>
<td>



...

</td>
<td>



...

</td>
<td>



...

</td>
<td>



<a id="rst-v4l2-pix-fmt-y16-be"></a>

...

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

> [!NOTE]
>
> For the Y16 and Y16\_BE formats, the actual sampling precision may be lower than 16 bits. For example, 10 bits per pixel uses values in the range 0 to 1023. For the IPU3\_Y10 format 25 pixels are packed into 32 bytes, which leaves the 6 most significant bits of the last byte padded with 0.
>
> For Y012 and Y12 formats, Y012 places its data in the 12 high bits, with padding zeros in the 4 low bits, in contrast to the Y12 format, which has its padding located in the most significant bits of the 16 bit word.
>
> The 'P' variations of the Y10, Y12 and Y14 formats are packed according to the RAW10, RAW12 and RAW14 packing scheme as defined by the MIPI CSI-2 specification.
