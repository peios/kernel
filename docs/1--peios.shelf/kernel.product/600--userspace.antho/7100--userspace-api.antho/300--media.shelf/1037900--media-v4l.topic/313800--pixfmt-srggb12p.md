---
title: "V4L2_PIX_FMT_SRGGB12P ('pRCC'), V4L2_PIX_FMT_SGRBG12P ('pgCC'), V4L2_PIX_FMT_SGBRG12P ('pGCC'), V4L2_PIX_FMT_SBGGR12P ('pBCC')"
type: reference
description: "These four pixel formats are packed raw sRGB / Bayer formats with 12 bits per colour. Every two consecutive samples are packed into three bytes. Each of the first two bytes contain the 8 high order bits of the pixels, and the third byte…"
---

<a id="rst-v4l2-pix-fmt-srggb12p-prcc-v4l2-pix-fmt-sgrbg12p-pgcc-v4l2-pix-fmt-sgbrg12p-pgcc-v4l2-pix-fmt-sbggr12p-pbcc"></a>
<a id="rst-v4l2-pix-fmt-sgrbg12p"></a>
<a id="rst-v4l2-pix-fmt-sgbrg12p"></a>
<a id="rst-v4l2-pix-fmt-sbggr12p"></a>
<a id="rst-v4l2-pix-fmt-srggb12p"></a>

<a id="rst-bit-packed-bayer-formats"></a>

## 12-bit packed Bayer formats

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-description"></a>

## Description

These four pixel formats are packed raw sRGB / Bayer formats with 12 bits per colour. Every two consecutive samples are packed into three bytes. Each of the first two bytes contain the 8 high order bits of the pixels, and the third byte contains the four least significant bits of each pixel, in the same order.

Each n-pixel row contains n/2 green samples and n/2 blue or red samples, with alternating green-red and green-blue rows. They are conventionally described as GRGR... BGBG..., RGRG... GBGB..., etc. Below is an example of a small V4L2_PIX_FMT_SBGGR12P image:

**Byte Order.** Each cell is one byte.

<!-- tabularcolumns: |p{2.2cm}|p{1.2cm}|p{1.2cm}|p{3.1cm}|p{1.2cm}|p{1.2cm}|p{6.4cm}| -->


<table>
<tbody>
<tr>
<td>


start + 0:

</td>
<td>


B<sub>00high</sub>

</td>
<td>


G<sub>01high</sub>

</td>
<td>


G<sub>01low</sub>(bits 7--4)

B<sub>00low</sub>(bits 3--0)

</td>
<td>


B<sub>02high</sub>

</td>
<td>


G<sub>03high</sub>

</td>
<td>


G<sub>03low</sub>(bits 7--4)

B<sub>02low</sub>(bits 3--0)

</td>
</tr>
<tr>
<td>


start + 6:

</td>
<td>


G<sub>10high</sub>

</td>
<td>


R<sub>11high</sub>

</td>
<td>


R<sub>11low</sub>(bits 7--4)

G<sub>10low</sub>(bits 3--0)

</td>
<td>


G<sub>12high</sub>

</td>
<td>


R<sub>13high</sub>

</td>
<td>


R<sub>13low</sub>(bits 7--4)

G<sub>12low</sub>(bits 3--0)

</td>
</tr>
<tr>
<td>


start + 12:

</td>
<td>


B<sub>20high</sub>

</td>
<td>


G<sub>21high</sub>

</td>
<td>


G<sub>21low</sub>(bits 7--4)

B<sub>20low</sub>(bits 3--0)

</td>
<td>


B<sub>22high</sub>

</td>
<td>


G<sub>23high</sub>

</td>
<td>


G<sub>23low</sub>(bits 7--4)

B<sub>22low</sub>(bits 3--0)

</td>
</tr>
<tr>
<td>


start + 18:

</td>
<td>


G<sub>30high</sub>

</td>
<td>


R<sub>31high</sub>

</td>
<td>


R<sub>31low</sub>(bits 7--4)

G<sub>30low</sub>(bits 3--0)

</td>
<td>


G<sub>32high</sub>

</td>
<td>


R<sub>33high</sub>

</td>
<td>


R<sub>33low</sub>(bits 7--4)

G<sub>32low</sub>(bits 3--0)

</td>
</tr>
</tbody>
</table>
