---
title: "V4L2_PIX_FMT_Y8I ('Y8I ')"
type: reference
description: "Interleaved grey-scale image, e.g. from a stereo-pair"
---

<a id="rst-v4l2-pix-fmt-y8i-y8i"></a>
<a id="rst-v4l2-pix-fmt-y8i"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

Interleaved grey-scale image, e.g. from a stereo-pair

<a id="rst-description"></a>

## Description

This is a grey-scale image with a depth of 8 bits per pixel, but with pixels from 2 sources interleaved. Each pixel is stored in a 16-bit word. E.g. the R200 RealSense camera stores pixel from the left sensor in lower and from the right sensor in the higher 8 bits.

**Byte Order.** Each cell is one byte.


<table>
<tbody>
<tr>
<td>


start + 0:

</td>
<td>


Y'<sub>00left</sub>

</td>
<td>


Y'<sub>00right</sub>

</td>
<td>


Y'<sub>01left</sub>

</td>
<td>


Y'<sub>01right</sub>

</td>
<td>


Y'<sub>02left</sub>

</td>
<td>


Y'<sub>02right</sub>

</td>
<td>


Y'<sub>03left</sub>

</td>
<td>


Y'<sub>03right</sub>

</td>
</tr>
<tr>
<td>


start + 8:

</td>
<td>


Y'<sub>10left</sub>

</td>
<td>


Y'<sub>10right</sub>

</td>
<td>


Y'<sub>11left</sub>

</td>
<td>


Y'<sub>11right</sub>

</td>
<td>


Y'<sub>12left</sub>

</td>
<td>


Y'<sub>12right</sub>

</td>
<td>


Y'<sub>13left</sub>

</td>
<td>


Y'<sub>13right</sub>

</td>
</tr>
<tr>
<td>


start + 16:

</td>
<td>


Y'<sub>20left</sub>

</td>
<td>


Y'<sub>20right</sub>

</td>
<td>


Y'<sub>21left</sub>

</td>
<td>


Y'<sub>21right</sub>

</td>
<td>


Y'<sub>22left</sub>

</td>
<td>


Y'<sub>22right</sub>

</td>
<td>


Y'<sub>23left</sub>

</td>
<td>


Y'<sub>23right</sub>

</td>
</tr>
<tr>
<td>


start + 24:

</td>
<td>


Y'<sub>30left</sub>

</td>
<td>


Y'<sub>30right</sub>

</td>
<td>


Y'<sub>31left</sub>

</td>
<td>


Y'<sub>31right</sub>

</td>
<td>


Y'<sub>32left</sub>

</td>
<td>


Y'<sub>32right</sub>

</td>
<td>


Y'<sub>33left</sub>

</td>
<td>


Y'<sub>33right</sub>

</td>
</tr>
</tbody>
</table>
