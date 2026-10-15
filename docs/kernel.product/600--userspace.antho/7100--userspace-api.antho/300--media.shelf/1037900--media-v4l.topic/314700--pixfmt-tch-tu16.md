---
title: "V4L2_TCH_FMT_TU16 ('TU16')"
type: reference
description: "man V4L2_TCH_FMT_TU16(2)"
---

<a id="rst-v4l2-tch-fmt-tu16-tu16"></a>
<a id="rst-v4l2-tch-fmt-tu16"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

*man V4L2_TCH_FMT_TU16(2)*

16-bit unsigned little endian raw touch data

<a id="rst-description"></a>

## Description

This format represents unsigned 16-bit data from a touch controller.

This may be used for output for raw and reference data. Values may range from 0 to 65535.

**Byte Order.** Each cell is one byte.


<table>
<tbody>
<tr>
<td>


start + 0:

</td>
<td>


R'<sub>00low</sub>

</td>
<td>


R'<sub>00high</sub>

</td>
<td>


R'<sub>01low</sub>

</td>
<td>


R'<sub>01high</sub>

</td>
<td>


R'<sub>02low</sub>

</td>
<td>


R'<sub>02high</sub>

</td>
<td>


R'<sub>03low</sub>

</td>
<td>


R'<sub>03high</sub>

</td>
</tr>
<tr>
<td>


start + 8:

</td>
<td>


R'<sub>10low</sub>

</td>
<td>


R'<sub>10high</sub>

</td>
<td>


R'<sub>11low</sub>

</td>
<td>


R'<sub>11high</sub>

</td>
<td>


R'<sub>12low</sub>

</td>
<td>


R'<sub>12high</sub>

</td>
<td>


R'<sub>13low</sub>

</td>
<td>


R'<sub>13high</sub>

</td>
</tr>
<tr>
<td>


start + 16:

</td>
<td>


R'<sub>20low</sub>

</td>
<td>


R'<sub>20high</sub>

</td>
<td>


R'<sub>21low</sub>

</td>
<td>


R'<sub>21high</sub>

</td>
<td>


R'<sub>22low</sub>

</td>
<td>


R'<sub>22high</sub>

</td>
<td>


R'<sub>23low</sub>

</td>
<td>


R'<sub>23high</sub>

</td>
</tr>
<tr>
<td>


start + 24:

</td>
<td>


R'<sub>30low</sub>

</td>
<td>


R'<sub>30high</sub>

</td>
<td>


R'<sub>31low</sub>

</td>
<td>


R'<sub>31high</sub>

</td>
<td>


R'<sub>32low</sub>

</td>
<td>


R'<sub>32high</sub>

</td>
<td>


R'<sub>33low</sub>

</td>
<td>


R'<sub>33high</sub>

</td>
</tr>
</tbody>
</table>
