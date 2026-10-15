---
title: "V4L2_TCH_FMT_DELTA_TD08 ('TD08')"
type: reference
description: "man V4L2_TCH_FMT_DELTA_TD08(2)"
---

<a id="rst-v4l2-tch-fmt-delta-td08-td08"></a>
<a id="rst-v4l2-tch-fmt-delta-td08"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

*man V4L2_TCH_FMT_DELTA_TD08(2)*

8-bit signed Touch Delta

<a id="rst-description"></a>

## Description

This format represents delta data from a touch controller.

Delta values may range from -128 to 127. Typically the values will vary through a small range depending on whether the sensor is touched or not. The full value may be seen if one of the touchscreen nodes has a fault or the line is not connected.

**Byte Order.** Each cell is one byte.


<table>
<tbody>
<tr>
<td>


start + 0:

</td>
<td>


D'<sub>00</sub>

</td>
<td>


D'<sub>01</sub>

</td>
<td>


D'<sub>02</sub>

</td>
<td>


D'<sub>03</sub>

</td>
</tr>
<tr>
<td>


start + 4:

</td>
<td>


D'<sub>10</sub>

</td>
<td>


D'<sub>11</sub>

</td>
<td>


D'<sub>12</sub>

</td>
<td>


D'<sub>13</sub>

</td>
</tr>
<tr>
<td>


start + 8:

</td>
<td>


D'<sub>20</sub>

</td>
<td>


D'<sub>21</sub>

</td>
<td>


D'<sub>22</sub>

</td>
<td>


D'<sub>23</sub>

</td>
</tr>
<tr>
<td>


start + 12:

</td>
<td>


D'<sub>30</sub>

</td>
<td>


D'<sub>31</sub>

</td>
<td>


D'<sub>32</sub>

</td>
<td>


D'<sub>33</sub>

</td>
</tr>
</tbody>
</table>
