---
title: "Indexed Format"
type: reference
description: "In this format each pixel is represented by an 8 bit index into a 256 entry ARGB palette. It is intended for Video Output Overlays <osd> only. There are no ioctls to access the palette, this must be done with ioctls of the Linux…"
---

<a id="rst-indexed-format"></a>
<a id="rst-pixfmt-indexed"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

In this format each pixel is represented by an 8 bit index into a 256 entry ARGB palette. It is intended for [Video Output Overlays](<~kernel/userspace/userspace-api/media-v4l/dev-osd#rst-osd>) only. There are no ioctls to access the palette, this must be done with ioctls of the Linux framebuffer API.


<table>
<caption>Indexed Image Format</caption>
<thead>
<tr>
<th>


Identifier

</th>
<th>


Code

</th>
<th>




</th>
<th colspan="8">


 Byte 0

</th>
</tr>
<tr>
<th>




</th>
<th>




</th>
<th>


Bit

</th>
<th>


7

</th>
<th>


6

</th>
<th>


5

</th>
<th>


4

</th>
<th>


3

</th>
<th>


2

</th>
<th>


1

</th>
<th>


0

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


`V4L2_PIX_FMT_PAL8`

</td>
<td>


'PAL8'

</td>
<td>




</td>
<td>


i<sub>7</sub>

</td>
<td>


i<sub>6</sub>

</td>
<td>


i<sub>5</sub>

</td>
<td>


i<sub>4</sub>

</td>
<td>


i<sub>3</sub>

</td>
<td>


i<sub>2</sub>

</td>
<td>


i<sub>1</sub>

</td>
<td>


<a id="rst-v4l2-pix-fmt-pal8"></a>

i<sub>0</sub>

</td>
</tr>
</tbody>
</table>
