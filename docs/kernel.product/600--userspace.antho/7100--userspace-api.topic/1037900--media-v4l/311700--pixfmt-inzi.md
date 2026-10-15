---
title: "V4L2_PIX_FMT_INZI ('INZI')"
type: reference
description: "Infrared 10-bit linked with Depth 16-bit images"
---

<a id="rst-v4l2-pix-fmt-inzi-inzi"></a>
<a id="rst-v4l2-pix-fmt-inzi"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

Infrared 10-bit linked with Depth 16-bit images

<a id="rst-description"></a>

## Description

Proprietary multi-planar format used by Intel SR300 Depth cameras, comprise of Infrared image followed by Depth data. The pixel definition is 32-bpp, with the Depth and Infrared Data split into separate continuous planes of identical dimensions.

The first plane - Infrared data - is stored according to [V4L2\_PIX\_FMT\_Y10](<~kernel/userspace/userspace-api/media-v4l/pixfmt-yuv-luma#rst-v4l2-pix-fmt-y10>) greyscale format. Each pixel is 16-bit cell, with actual data stored in the 10 LSBs with values in range 0 to 1023. The six remaining MSBs are padded with zeros.

The second plane provides 16-bit per-pixel Depth data arranged in [V4L2-PIX-FMT-Z16](<~kernel/userspace/userspace-api/media-v4l/pixfmt-z16#rst-v4l2-pix-fmt-z16>) format.

<strong>Frame Structure.</strong> Each cell is a 16-bit word with more significant data stored at higher memory address (byte order is little-endian).

<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{2.5cm}|p{2.5cm}|p{2.5cm}|p{2.5cm}|p{2.5cm}|p{2.5cm}| -->


<table>
<tbody>
<tr>
<th scope="row">



Ir<sub>0,0</sub>

</th>
<td>



Ir<sub>0,1</sub>

</td>
<td>



Ir<sub>0,2</sub>

</td>
<td>



...

</td>
<td>



...

</td>
<td>



...

</td>
</tr>
<tr>
<th colspan="6" scope="row">



 ...

</th>
</tr>
<tr>
<th colspan="6" scope="row">



 Infrared Data

</th>
</tr>
<tr>
<th colspan="6" scope="row">



 ...

</th>
</tr>
<tr>
<th scope="row">



...

</th>
<td>



...

</td>
<td>



...

</td>
<td>



Ir<sub>n-1,n-3</sub>

</td>
<td>



Ir<sub>n-1,n-2</sub>

</td>
<td>



Ir<sub>n-1,n-1</sub>

</td>
</tr>
<tr>
<th scope="row">



Depth<sub>0,0</sub>

</th>
<td>



Depth<sub>0,1</sub>

</td>
<td>



Depth<sub>0,2</sub>

</td>
<td>



...

</td>
<td>



...

</td>
<td>



...

</td>
</tr>
<tr>
<th colspan="6" scope="row">



 ...

</th>
</tr>
<tr>
<th colspan="6" scope="row">



 Depth Data

</th>
</tr>
<tr>
<th colspan="6" scope="row">



 ...

</th>
</tr>
<tr>
<th scope="row">



...

</th>
<td>



...

</td>
<td>



...

</td>
<td>



Depth<sub>n-1,n-3</sub>

</td>
<td>



Depth<sub>n-1,n-2</sub>

</td>
<td>



Depth<sub>n-1,n-1</sub>

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->
