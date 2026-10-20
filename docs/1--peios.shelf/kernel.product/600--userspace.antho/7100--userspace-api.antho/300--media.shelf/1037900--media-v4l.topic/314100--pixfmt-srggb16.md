---
title: "V4L2_PIX_FMT_SRGGB16 ('RG16'), V4L2_PIX_FMT_SGRBG16 ('GR16'), V4L2_PIX_FMT_SGBRG16 ('GB16'), V4L2_PIX_FMT_SBGGR16 ('BYR2'),"
type: reference
description: "These four pixel formats are raw sRGB / Bayer formats with 16 bits per sample. Each sample is stored in a 16-bit word. Each n-pixel row contains n/2 green samples and n/2 blue or red samples, with alternating red and blue rows. Bytes are…"
---

<a id="rst-v4l2-pix-fmt-srggb16-rg16-v4l2-pix-fmt-sgrbg16-gr16-v4l2-pix-fmt-sgbrg16-gb16-v4l2-pix-fmt-sbggr16-byr2"></a>
<a id="rst-v4l2-pix-fmt-sgrbg16"></a>
<a id="rst-v4l2-pix-fmt-sgbrg16"></a>
<a id="rst-v4l2-pix-fmt-sbggr16"></a>
<a id="rst-v4l2-pix-fmt-srggb16"></a>

<a id="rst-bit-bayer-formats"></a>

## 16-bit Bayer formats

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-description"></a>

## Description

These four pixel formats are raw sRGB / Bayer formats with 16 bits per sample. Each sample is stored in a 16-bit word. Each n-pixel row contains n/2 green samples and n/2 blue or red samples, with alternating red and blue rows. Bytes are stored in memory in little endian order. They are conventionally described as GRGR... BGBG..., RGRG... GBGB..., etc. Below is an example of a small V4L2_PIX_FMT_SBGGR16 image:

**Byte Order.** Each cell is one byte.


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
