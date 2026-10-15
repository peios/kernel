---
title: "V4L2_TCH_FMT_DELTA_TD16 ('TD16')"
type: reference
description: "man V4L2_TCH_FMT_DELTA_TD16(2)"
---

<a id="rst-v4l2-tch-fmt-delta-td16-td16"></a>
<a id="rst-v4l2-tch-fmt-delta-td16"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

*man V4L2_TCH_FMT_DELTA_TD16(2)*

16-bit signed little endian Touch Delta

<a id="rst-description"></a>

## Description

This format represents delta data from a touch controller.

Delta values may range from -32768 to 32767. Typically the values will vary through a small range depending on whether the sensor is touched or not. The full value may be seen if one of the touchscreen nodes has a fault or the line is not connected.

**Byte Order.** Each cell is one byte.


<table>
<tbody>
<tr>
<td>


start + 0:

</td>
<td>


D'<sub>00low</sub>

</td>
<td>


D'<sub>00high</sub>

</td>
<td>


D'<sub>01low</sub>

</td>
<td>


D'<sub>01high</sub>

</td>
<td>


D'<sub>02low</sub>

</td>
<td>


D'<sub>02high</sub>

</td>
<td>


D'<sub>03low</sub>

</td>
<td>


D'<sub>03high</sub>

</td>
</tr>
<tr>
<td>


start + 8:

</td>
<td>


D'<sub>10low</sub>

</td>
<td>


D'<sub>10high</sub>

</td>
<td>


D'<sub>11low</sub>

</td>
<td>


D'<sub>11high</sub>

</td>
<td>


D'<sub>12low</sub>

</td>
<td>


D'<sub>12high</sub>

</td>
<td>


D'<sub>13low</sub>

</td>
<td>


D'<sub>13high</sub>

</td>
</tr>
<tr>
<td>


start + 16:

</td>
<td>


D'<sub>20low</sub>

</td>
<td>


D'<sub>20high</sub>

</td>
<td>


D'<sub>21low</sub>

</td>
<td>


D'<sub>21high</sub>

</td>
<td>


D'<sub>22low</sub>

</td>
<td>


D'<sub>22high</sub>

</td>
<td>


D'<sub>23low</sub>

</td>
<td>


D'<sub>23high</sub>

</td>
</tr>
<tr>
<td>


start + 24:

</td>
<td>


D'<sub>30low</sub>

</td>
<td>


D'<sub>30high</sub>

</td>
<td>


D'<sub>31low</sub>

</td>
<td>


D'<sub>31high</sub>

</td>
<td>


D'<sub>32low</sub>

</td>
<td>


D'<sub>32high</sub>

</td>
<td>


D'<sub>33low</sub>

</td>
<td>


D'<sub>33high</sub>

</td>
</tr>
</tbody>
</table>
