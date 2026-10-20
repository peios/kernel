---
title: "V4L2_SDR_FMT_PCU20BE ('PC20')"
type: reference
description: "Planar complex unsigned 20-bit big endian IQ sample"
---

<a id="rst-v4l2-sdr-fmt-pcu20be-pc20"></a>
<a id="rst-v4l2-sdr-fmt-pcu20be"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

Planar complex unsigned 20-bit big endian IQ sample

<a id="rst-description"></a>

## Description

This format contains a sequence of complex number samples. Each complex number consist of two parts called In-phase and Quadrature (IQ). Both I and Q are represented as a 20 bit unsigned big endian number stored in 32 bit space. The remaining unused bits within the 32 bit space will be padded with 0. I value starts first and Q value starts at an offset equalling half of the buffer size (i.e.) offset = buffersize/2. Out of the 20 bits, bit 19:2 (18 bit) is data and bit 1:0 (2 bit) can be any value.

**Byte Order.** Each cell is one byte.


<table>
<thead>
<tr>
<th>


Offset:

</th>
<th>


Byte B0

</th>
<th>


Byte B1

</th>
<th>


Byte B2

</th>
<th>


Byte B3

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


start + 0:

</td>
<td>


I'<sub>0[19:12]</sub>

</td>
<td>


I'<sub>0[11:4]</sub>

</td>
<td>


I'<sub>0[3:0]; B2[3:0]=pad</sub>

</td>
<td>


pad

</td>
</tr>
<tr>
<td>


start + 4:

</td>
<td>


I'<sub>1[19:12]</sub>

</td>
<td>


I'<sub>1[11:4]</sub>

</td>
<td>


I'<sub>1[3:0]; B2[3:0]=pad</sub>

</td>
<td>


pad

</td>
</tr>
<tr>
<td colspan="5">


...

</td>
</tr>
<tr>
<td>


start + offset:

</td>
<td>


Q'<sub>0[19:12]</sub>

</td>
<td>


Q'<sub>0[11:4]</sub>

</td>
<td>


Q'<sub>0[3:0]; B2[3:0]=pad</sub>

</td>
<td>


pad

</td>
</tr>
<tr>
<td>


start + offset + 4:

</td>
<td>


Q'<sub>1[19:12]</sub>

</td>
<td>


Q'<sub>1[11:4]</sub>

</td>
<td>


Q'<sub>1[3:0]; B2[3:0]=pad</sub>

</td>
<td>


pad

</td>
</tr>
</tbody>
</table>
