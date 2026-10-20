---
title: "V4L2_PIX_FMT_UV8 ('UV8')"
type: reference
description: "UV plane interleaved"
---

<a id="rst-v4l2-pix-fmt-uv8-uv8"></a>
<a id="rst-v4l2-pix-fmt-uv8"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

UV plane interleaved

<a id="rst-description"></a>

## Description

In this format there is no Y plane, Only CbCr plane. ie (UV interleaved)

**Byte Order.** Each cell is one byte.


<table>
<tbody>
<tr>
<td>


start + 0:

</td>
<td>


Cb<sub>00</sub>

</td>
<td>


Cr<sub>00</sub>

</td>
<td>


Cb<sub>01</sub>

</td>
<td>


Cr<sub>01</sub>

</td>
</tr>
<tr>
<td>


start + 4:

</td>
<td>


Cb<sub>10</sub>

</td>
<td>


Cr<sub>10</sub>

</td>
<td>


Cb<sub>11</sub>

</td>
<td>


Cr<sub>11</sub>

</td>
</tr>
<tr>
<td>


start + 8:

</td>
<td>


Cb<sub>20</sub>

</td>
<td>


Cr<sub>20</sub>

</td>
<td>


Cb<sub>21</sub>

</td>
<td>


Cr<sub>21</sub>

</td>
</tr>
<tr>
<td>


start + 12:

</td>
<td>


Cb<sub>30</sub>

</td>
<td>


Cr<sub>30</sub>

</td>
<td>


Cb<sub>31</sub>

</td>
<td>


Cr<sub>31</sub>

</td>
</tr>
</tbody>
</table>
