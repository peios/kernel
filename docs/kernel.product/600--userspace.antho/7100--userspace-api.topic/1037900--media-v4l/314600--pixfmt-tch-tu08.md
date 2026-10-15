---
title: "V4L2_TCH_FMT_TU08 ('TU08')"
type: reference
description: "man V4L2_TCH_FMT_TU08(2)"
---

<a id="rst-v4l2-tch-fmt-tu08-tu08"></a>
<a id="rst-v4l2-tch-fmt-tu08"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

*man V4L2_TCH_FMT_TU08(2)*

8-bit unsigned raw touch data

<a id="rst-description"></a>

## Description

This format represents unsigned 8-bit data from a touch controller.

This may be used for output for raw and reference data. Values may range from 0 to 255.

**Byte Order.** Each cell is one byte.


<table>
<tbody>
<tr>
<td>


start + 0:

</td>
<td>


R'<sub>00</sub>

</td>
<td>


R'<sub>01</sub>

</td>
<td>


R'<sub>02</sub>

</td>
<td>


R'<sub>03</sub>

</td>
</tr>
<tr>
<td>


start + 4:

</td>
<td>


R'<sub>10</sub>

</td>
<td>


R'<sub>11</sub>

</td>
<td>


R'<sub>12</sub>

</td>
<td>


R'<sub>13</sub>

</td>
</tr>
<tr>
<td>


start + 8:

</td>
<td>


R'<sub>20</sub>

</td>
<td>


R'<sub>21</sub>

</td>
<td>


R'<sub>22</sub>

</td>
<td>


R'<sub>23</sub>

</td>
</tr>
<tr>
<td>


start + 12:

</td>
<td>


R'<sub>30</sub>

</td>
<td>


R'<sub>31</sub>

</td>
<td>


R'<sub>32</sub>

</td>
<td>


R'<sub>33</sub>

</td>
</tr>
</tbody>
</table>
