---
title: "Selection flags"
type: reference
description: "Reference for Selection flags."
---

<a id="rst-selection-flags"></a>
<a id="rst-v4l2-selection-flags"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-v4l2-selection-flags-table"></a>



<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{5.6cm}|p{2.0cm}|p{6.5cm}|p{1.2cm}|p{1.2cm}| -->


<table>
<caption>

Selection flag definitions

</caption>
<thead>
<tr>
<th>



Flag name

</th>
<th>



id

</th>
<th>



Definition

</th>
<th>



Valid for V4L2

</th>
<th>



Valid for V4L2 subdev

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



`V4L2_SEL_FLAG_GE`

</td>
<td>



(1 &lt;&lt; 0)

</td>
<td>



Suggest the driver it should choose greater or equal rectangle (in size) than was requested. Albeit the driver may choose a lesser size, it will only do so due to hardware limitations. Without this flag (and `V4L2_SEL_FLAG_LE`) the behaviour is to choose the closest possible rectangle.

</td>
<td>



Yes

</td>
<td>



Yes

</td>
</tr>
<tr>
<td>



`V4L2_SEL_FLAG_LE`

</td>
<td>



(1 &lt;&lt; 1)

</td>
<td>



Suggest the driver it should choose lesser or equal rectangle (in size) than was requested. Albeit the driver may choose a greater size, it will only do so due to hardware limitations.

</td>
<td>



Yes

</td>
<td>



Yes

</td>
</tr>
<tr>
<td>



`V4L2_SEL_FLAG_KEEP_CONFIG`

</td>
<td>



(1 &lt;&lt; 2)

</td>
<td>



The configuration must not be propagated to any further processing steps. If this flag is not given, the configuration is propagated inside the subdevice to all further processing steps.

</td>
<td>



No

</td>
<td>



Yes

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->
