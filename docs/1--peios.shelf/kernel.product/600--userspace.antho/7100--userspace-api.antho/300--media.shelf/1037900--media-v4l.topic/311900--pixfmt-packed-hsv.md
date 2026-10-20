---
title: "Packed HSV formats"
type: reference
description: "The hue (h) is measured in degrees, the equivalence between degrees and LSBs depends on the hsv-encoding used, see colorspaces. The saturation (s) and the value (v) are measured in percentage of the cylinder: 0 being the smallest value and…"
---

<a id="rst-packed-hsv-formats"></a>
<a id="rst-packed-hsv"></a>

<a id="rst-description"></a>

## Description

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

The <em>hue</em> (h) is measured in degrees, the equivalence between degrees and LSBs depends on the hsv-encoding used, see [colorspaces](<~kernel/userspace/userspace-api/media-v4l/colorspaces#rst-colorspaces-1>). The <em>saturation</em> (s) and the <em>value</em> (v) are measured in percentage of the cylinder: 0 being the smallest value and 255 the maximum.

The values are packed in 24 or 32 bit formats.

<!-- Source LaTeX layout: \begingroup
\tiny
\setlength{\tabcolsep}{2pt} -->

<!-- tabularcolumns: |p{2.6cm}|p{0.8cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}| -->

<a id="rst-packed-hsv-formats-1"></a>


<table>
<caption>

Packed HSV Image Formats

</caption>
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



 Byte 0 in memory

</th>
<th colspan="8">



 Byte 1

</th>
<th colspan="8">



 Byte 2

</th>
<th colspan="8">



 Byte 3

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



`V4L2_PIX_FMT_HSV32`

</td>
<td>



'HSV4'

</td>
<td>





</td>
<td>





</td>
<td>





</td>
<td>





</td>
<td>





</td>
<td>





</td>
<td>





</td>
<td>





</td>
<td>





</td>
<td>



h<sub>7</sub>

</td>
<td>



h<sub>6</sub>

</td>
<td>



h<sub>5</sub>

</td>
<td>



h<sub>4</sub>

</td>
<td>



h<sub>3</sub>

</td>
<td>



h<sub>2</sub>

</td>
<td>



h<sub>1</sub>

</td>
<td>



h<sub>0</sub>

</td>
<td>



s<sub>7</sub>

</td>
<td>



s<sub>6</sub>

</td>
<td>



s<sub>5</sub>

</td>
<td>



s<sub>4</sub>

</td>
<td>



s<sub>3</sub>

</td>
<td>



s<sub>2</sub>

</td>
<td>



s<sub>1</sub>

</td>
<td>



s<sub>0</sub>

</td>
<td>



v<sub>7</sub>

</td>
<td>



v<sub>6</sub>

</td>
<td>



v<sub>5</sub>

</td>
<td>



v<sub>4</sub>

</td>
<td>



v<sub>3</sub>

</td>
<td>



v<sub>2</sub>

</td>
<td>



v<sub>1</sub>

</td>
<td>



<a id="rst-v4l2-pix-fmt-hsv32"></a>

v<sub>0</sub>

</td>
</tr>
<tr>
<td>



<a id="rst-v4l2-pix-fmt-hsv24"></a>



`V4L2_PIX_FMT_HSV24`

</td>
<td>



'HSV3'

</td>
<td>





</td>
<td>



h<sub>7</sub>

</td>
<td>



h<sub>6</sub>

</td>
<td>



h<sub>5</sub>

</td>
<td>



h<sub>4</sub>

</td>
<td>



h<sub>3</sub>

</td>
<td>



h<sub>2</sub>

</td>
<td>



h<sub>1</sub>

</td>
<td>



h<sub>0</sub>

</td>
<td>



s<sub>7</sub>

</td>
<td>



s<sub>6</sub>

</td>
<td>



s<sub>5</sub>

</td>
<td>



s<sub>4</sub>

</td>
<td>



s<sub>3</sub>

</td>
<td>



s<sub>2</sub>

</td>
<td>



s<sub>1</sub>

</td>
<td>



s<sub>0</sub>

</td>
<td>



v<sub>7</sub>

</td>
<td>



v<sub>6</sub>

</td>
<td>



v<sub>5</sub>

</td>
<td>



v<sub>4</sub>

</td>
<td>



v<sub>3</sub>

</td>
<td>



v<sub>2</sub>

</td>
<td>



v<sub>1</sub>

</td>
<td>



v<sub>0</sub>

</td>
<td colspan="8">





</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \endgroup -->

Bit 7 is the most significant bit.
