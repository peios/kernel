---
title: "V4L2_PIX_FMT_SRGGB10 ('RG10'), V4L2_PIX_FMT_SGRBG10 ('BA10'), V4L2_PIX_FMT_SGBRG10 ('GB10'), V4L2_PIX_FMT_SBGGR10 ('BG10'),"
type: reference
description: "V4L2_PIX_FMT_SGRBG10 V4L2_PIX_FMT_SGBRG10 V4L2_PIX_FMT_SBGGR10 10-bit Bayer formats expanded to 16 bits"
---

<a id="rst-v4l2-pix-fmt-srggb10-rg10-v4l2-pix-fmt-sgrbg10-ba10-v4l2-pix-fmt-sgbrg10-gb10-v4l2-pix-fmt-sbggr10-bg10"></a>
<a id="rst-v4l2-pix-fmt-sgrbg10"></a>
<a id="rst-v4l2-pix-fmt-sgbrg10"></a>
<a id="rst-v4l2-pix-fmt-sbggr10"></a>
<a id="rst-v4l2-pix-fmt-srggb10"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

V4L2_PIX_FMT_SGRBG10 V4L2_PIX_FMT_SGBRG10 V4L2_PIX_FMT_SBGGR10 10-bit Bayer formats expanded to 16 bits

<a id="rst-description"></a>

## Description

These four pixel formats are raw sRGB / Bayer formats with 10 bits per sample. Each sample is stored in a 16-bit word, with 6 unused high bits filled with zeros. Each n-pixel row contains n/2 green samples and n/2 blue or red samples, with alternating red and blue rows. Bytes are stored in memory in little endian order. They are conventionally described as GRGR... BGBG..., RGRG... GBGB..., etc. Below is an example of one of these formats:

**Byte Order.** Each cell is one byte, the 6 most significant bits in the high bytes are 0.


<table>
<tbody>
<tr>
<td>


start + 0:

</td>
<td>


B<sub>00low</sub>

</td>
<td>


B<sub>00high</sub>

</td>
<td>


G<sub>01low</sub>

</td>
<td>


G<sub>01high</sub>

</td>
<td>


B<sub>02low</sub>

</td>
<td>


B<sub>02high</sub>

</td>
<td>


G<sub>03low</sub>

</td>
<td>


G<sub>03high</sub>

</td>
</tr>
<tr>
<td>


start + 8:

</td>
<td>


G<sub>10low</sub>

</td>
<td>


G<sub>10high</sub>

</td>
<td>


R<sub>11low</sub>

</td>
<td>


R<sub>11high</sub>

</td>
<td>


G<sub>12low</sub>

</td>
<td>


G<sub>12high</sub>

</td>
<td>


R<sub>13low</sub>

</td>
<td>


R<sub>13high</sub>

</td>
</tr>
<tr>
<td>


start + 16:

</td>
<td>


B<sub>20low</sub>

</td>
<td>


B<sub>20high</sub>

</td>
<td>


G<sub>21low</sub>

</td>
<td>


G<sub>21high</sub>

</td>
<td>


B<sub>22low</sub>

</td>
<td>


B<sub>22high</sub>

</td>
<td>


G<sub>23low</sub>

</td>
<td>


G<sub>23high</sub>

</td>
</tr>
<tr>
<td>


start + 24:

</td>
<td>


G<sub>30low</sub>

</td>
<td>


G<sub>30high</sub>

</td>
<td>


R<sub>31low</sub>

</td>
<td>


R<sub>31high</sub>

</td>
<td>


G<sub>32low</sub>

</td>
<td>


G<sub>32high</sub>

</td>
<td>


R<sub>33low</sub>

</td>
<td>


R<sub>33high</sub>

</td>
</tr>
</tbody>
</table>
