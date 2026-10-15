---
title: "V4L2_PIX_FMT_SRGGB14P ('pREE'), V4L2_PIX_FMT_SGRBG14P ('pgEE'), V4L2_PIX_FMT_SGBRG14P ('pGEE'), V4L2_PIX_FMT_SBGGR14P ('pBEE'),"
type: reference
description: "man V4L2_PIX_FMT_SRGGB14P(2)"
---

<a id="rst-v4l2-pix-fmt-srggb14p-pree-v4l2-pix-fmt-sgrbg14p-pgee-v4l2-pix-fmt-sgbrg14p-pgee-v4l2-pix-fmt-sbggr14p-pbee"></a>
<a id="rst-v4l2-pix-fmt-sgrbg14p"></a>
<a id="rst-v4l2-pix-fmt-sgbrg14p"></a>
<a id="rst-v4l2-pix-fmt-sbggr14p"></a>
<a id="rst-v4l2-pix-fmt-srggb14p"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<em>man V4L2\_PIX\_FMT\_SRGGB14P(2)</em>

V4L2\_PIX\_FMT\_SGRBG14P V4L2\_PIX\_FMT\_SGBRG14P V4L2\_PIX\_FMT\_SBGGR14P 14-bit packed Bayer formats

<a id="rst-description"></a>

## Description

These four pixel formats are packed raw sRGB / Bayer formats with 14 bits per colour. Every four consecutive samples are packed into seven bytes. Each of the first four bytes contain the eight high order bits of the pixels, and the three following bytes contains the six least significant bits of each pixel, in the same order.

Each n-pixel row contains n/2 green samples and n/2 blue or red samples, with alternating green-red and green-blue rows. They are conventionally described as GRGR... BGBG..., RGRG... GBGB..., etc. Below is an example of one of these formats:

<strong>Byte Order.</strong> Each cell is one byte.

<!-- Source LaTeX layout: \begingroup
\footnotesize
\setlength{\tabcolsep}{2pt} -->

<!-- tabularcolumns: |p{1.6cm}|p{1.0cm}|p{1.0cm}|p{1.0cm}|p{1.0cm}|p{3.5cm}|p{3.5cm}|p{3.5cm}| -->


<table>
<tbody>
<tr>
<td>



start + 0

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



G<sub>01low bits 1--0</sub>(bits 7--6)

B<sub>00low bits 5--0</sub>(bits 5--0)

</td>
<td>



B<sub>02low bits 3--0</sub>(bits 7--4)

G<sub>01low bits 5--2</sub>(bits 3--0)

</td>
<td>



G<sub>03low bits 5--0</sub>(bits 7--2)

B<sub>02low bits 5--4</sub>(bits 1--0)

</td>
</tr>
<tr>
<td>



start + 7

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



R<sub>11low bits 1--0</sub>(bits 7--6)

G<sub>10low bits 5--0</sub>(bits 5--0)

</td>
<td>



G<sub>12low bits 3--0</sub>(bits 7--4)

R<sub>11low bits 5--2</sub>(bits 3--0)

</td>
<td>



R<sub>13low bits 5--0</sub>(bits 7--2)

G<sub>12low bits 5--4</sub>(bits 1--0)

</td>
</tr>
<tr>
<td>



start + 14

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



G<sub>21low bits 1--0</sub>(bits 7--6)

B<sub>20low bits 5--0</sub>(bits 5--0)

</td>
<td>



B<sub>22low bits 3--0</sub>(bits 7--4)

G<sub>21low bits 5--2</sub>(bits 3--0)

</td>
<td>



G<sub>23low bits 5--0</sub>(bits 7--2)

B<sub>22low bits 5--4</sub>(bits 1--0)

</td>
</tr>
<tr>
<td>



start + 21

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



R<sub>31low bits 1--0</sub>(bits 7--6) G<sub>30low bits 5--0</sub>(bits 5--0)

</td>
<td>



G<sub>32low bits 3--0</sub>(bits 7--4) R<sub>31low bits 5--2</sub>(bits 3--0)

</td>
<td>



R<sub>33low bits 5--0</sub>(bits 7--2) G<sub>32low bits 5--4</sub>(bits 1--0)

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \endgroup -->
