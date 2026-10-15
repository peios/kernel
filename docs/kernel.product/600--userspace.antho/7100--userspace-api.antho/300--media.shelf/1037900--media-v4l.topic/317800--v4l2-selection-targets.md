---
title: "Selection targets"
type: reference
description: "The precise meaning of the selection targets may be dependent on which of the two interfaces they are used."
---

<a id="rst-selection-targets"></a>
<a id="rst-v4l2-selection-targets"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

The precise meaning of the selection targets may be dependent on which of the two interfaces they are used.

<a id="rst-v4l2-selection-targets-table"></a>



<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{6.2cm}|p{1.4cm}|p{7.3cm}|p{1.2cm}|p{0.8cm}| -->


<table>
<caption>

Selection target definitions

</caption>
<thead>
<tr>
<th>



Target name

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



`V4L2_SEL_TGT_CROP`

</td>
<td>



0x0000

</td>
<td>



Crop rectangle. Defines the cropped area.

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



`V4L2_SEL_TGT_CROP_DEFAULT`

</td>
<td>



0x0001

</td>
<td>



Suggested cropping rectangle that covers the "whole picture". This includes only active pixels and excludes other non-active pixels such as black pixels.

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



`V4L2_SEL_TGT_CROP_BOUNDS`

</td>
<td>



0x0002

</td>
<td>



Bounds of the crop rectangle. All valid crop rectangles fit inside the crop bounds rectangle.

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



`V4L2_SEL_TGT_NATIVE_SIZE`

</td>
<td>



0x0003

</td>
<td>



The native size of the device, e.g. a sensor's pixel array. `left` and `top` fields are zero for this target.

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



`V4L2_SEL_TGT_COMPOSE`

</td>
<td>



0x0100

</td>
<td>



Compose rectangle. Used to configure scaling and composition.

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



`V4L2_SEL_TGT_COMPOSE_DEFAULT`

</td>
<td>



0x0101

</td>
<td>



Suggested composition rectangle that covers the "whole picture".

</td>
<td>



Yes

</td>
<td>



No

</td>
</tr>
<tr>
<td>



`V4L2_SEL_TGT_COMPOSE_BOUNDS`

</td>
<td>



0x0102

</td>
<td>



Bounds of the compose rectangle. All valid compose rectangles fit inside the compose bounds rectangle.

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



`V4L2_SEL_TGT_COMPOSE_PADDED`

</td>
<td>



0x0103

</td>
<td>



The active area and all padding pixels that are inserted or modified by hardware.

</td>
<td>



Yes

</td>
<td>



No

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->
