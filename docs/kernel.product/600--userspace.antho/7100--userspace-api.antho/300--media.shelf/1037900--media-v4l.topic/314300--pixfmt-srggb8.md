---
title: "V4L2_PIX_FMT_SRGGB8 ('RGGB'), V4L2_PIX_FMT_SGRBG8 ('GRBG'), V4L2_PIX_FMT_SGBRG8 ('GBRG'), V4L2_PIX_FMT_SBGGR8 ('BA81'),"
type: reference
description: "These four pixel formats are raw sRGB / Bayer formats with 8 bits per sample. Each sample is stored in a byte. Each n-pixel row contains n/2 green samples and n/2 blue or red samples, with alternating red and blue rows. They are…"
---

<a id="rst-v4l2-pix-fmt-srggb8-rggb-v4l2-pix-fmt-sgrbg8-grbg-v4l2-pix-fmt-sgbrg8-gbrg-v4l2-pix-fmt-sbggr8-ba81"></a>
<a id="rst-v4l2-pix-fmt-sgrbg8"></a>
<a id="rst-v4l2-pix-fmt-sgbrg8"></a>
<a id="rst-v4l2-pix-fmt-sbggr8"></a>
<a id="rst-v4l2-pix-fmt-srggb8"></a>

<a id="rst-bit-bayer-formats"></a>

## 8-bit Bayer formats

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-description"></a>

## Description

These four pixel formats are raw sRGB / Bayer formats with 8 bits per sample. Each sample is stored in a byte. Each n-pixel row contains n/2 green samples and n/2 blue or red samples, with alternating red and blue rows. They are conventionally described as GRGR... BGBG..., RGRG... GBGB..., etc. Below is an example of a small V4L2_PIX_FMT_SBGGR8 image:

**Byte Order.** Each cell is one byte.


<table>
<tbody>
<tr>
<td>


start + 0:

</td>
<td>


B<sub>00</sub>

</td>
<td>


G<sub>01</sub>

</td>
<td>


B<sub>02</sub>

</td>
<td>


G<sub>03</sub>

</td>
</tr>
<tr>
<td>


start + 4:

</td>
<td>


G<sub>10</sub>

</td>
<td>


R<sub>11</sub>

</td>
<td>


G<sub>12</sub>

</td>
<td>


R<sub>13</sub>

</td>
</tr>
<tr>
<td>


start + 8:

</td>
<td>


B<sub>20</sub>

</td>
<td>


G<sub>21</sub>

</td>
<td>


B<sub>22</sub>

</td>
<td>


G<sub>23</sub>

</td>
</tr>
<tr>
<td>


start + 12:

</td>
<td>


G<sub>30</sub>

</td>
<td>


R<sub>31</sub>

</td>
<td>


G<sub>32</sub>

</td>
<td>


R<sub>33</sub>

</td>
</tr>
</tbody>
</table>
