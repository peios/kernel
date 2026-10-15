---
title: "V4L2_PIX_FMT_SRGGB10P ('pRAA'), V4L2_PIX_FMT_SGRBG10P ('pgAA'), V4L2_PIX_FMT_SGBRG10P ('pGAA'), V4L2_PIX_FMT_SBGGR10P ('pBAA'),"
type: reference
description: "V4L2_PIX_FMT_SGRBG10P V4L2_PIX_FMT_SGBRG10P V4L2_PIX_FMT_SBGGR10P 10-bit packed Bayer formats"
---

<a id="rst-v4l2-pix-fmt-srggb10p-praa-v4l2-pix-fmt-sgrbg10p-pgaa-v4l2-pix-fmt-sgbrg10p-pgaa-v4l2-pix-fmt-sbggr10p-pbaa"></a>
<a id="rst-v4l2-pix-fmt-sgrbg10p"></a>
<a id="rst-v4l2-pix-fmt-sgbrg10p"></a>
<a id="rst-v4l2-pix-fmt-sbggr10p"></a>
<a id="rst-v4l2-pix-fmt-srggb10p"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

V4L2_PIX_FMT_SGRBG10P V4L2_PIX_FMT_SGBRG10P V4L2_PIX_FMT_SBGGR10P 10-bit packed Bayer formats

<a id="rst-description"></a>

## Description

These four pixel formats are packed raw sRGB / Bayer formats with 10 bits per sample. Every four consecutive samples are packed into 5 bytes. Each of the first 4 bytes contain the 8 high order bits of the pixels, and the 5th byte contains the 2 least significants bits of each pixel, in the same order.

Each n-pixel row contains n/2 green samples and n/2 blue or red samples, with alternating green-red and green-blue rows. They are conventionally described as GRGR... BGBG..., RGRG... GBGB..., etc. Below is an example of a small V4L2_PIX_FMT_SBGGR10P image:

**Byte Order.** Each cell is one byte.

<!-- tabularcolumns: |p{2.4cm}|p{1.4cm}|p{1.2cm}|p{1.2cm}|p{1.2cm}|p{9.3cm}| -->


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


B<sub>02high</sub>

</td>
<td>


G<sub>03high</sub>

</td>
<td>


G<sub>03low</sub>(bits 7--6) B<sub>02low</sub>(bits 5--4)

G<sub>01low</sub>(bits 3--2) B<sub>00low</sub>(bits 1--0)

</td>
</tr>
<tr>
<td>


start + 5:

</td>
<td>


G<sub>10high</sub>

</td>
<td>


R<sub>11high</sub>

</td>
<td>


G<sub>12high</sub>

</td>
<td>


R<sub>13high</sub>

</td>
<td>


R<sub>13low</sub>(bits 7--6) G<sub>12low</sub>(bits 5--4)

R<sub>11low</sub>(bits 3--2) G<sub>10low</sub>(bits 1--0)

</td>
</tr>
<tr>
<td>


start + 10:

</td>
<td>


B<sub>20high</sub>

</td>
<td>


G<sub>21high</sub>

</td>
<td>


B<sub>22high</sub>

</td>
<td>


G<sub>23high</sub>

</td>
<td>


G<sub>23low</sub>(bits 7--6) B<sub>22low</sub>(bits 5--4)

G<sub>21low</sub>(bits 3--2) B<sub>20low</sub>(bits 1--0)

</td>
</tr>
<tr>
<td>


start + 15:

</td>
<td>


G<sub>30high</sub>

</td>
<td>


R<sub>31high</sub>

</td>
<td>


G<sub>32high</sub>

</td>
<td>


R<sub>33high</sub>

</td>
<td>


R<sub>33low</sub>(bits 7--6) G<sub>32low</sub>(bits 5--4)

R<sub>31low</sub>(bits 3--2) G<sub>30low</sub>(bits 1--0)

</td>
</tr>
</tbody>
</table>
