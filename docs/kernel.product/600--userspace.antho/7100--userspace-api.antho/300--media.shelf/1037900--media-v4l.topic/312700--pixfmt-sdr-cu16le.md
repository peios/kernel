---
title: "V4L2_SDR_FMT_CU16LE ('CU16')"
type: reference
description: "Complex unsigned 16-bit little endian IQ sample"
---

<a id="rst-v4l2-sdr-fmt-cu16le-cu16"></a>
<a id="rst-v4l2-sdr-fmt-cu16le"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

Complex unsigned 16-bit little endian IQ sample

<a id="rst-description"></a>

## Description

This format contains sequence of complex number samples. Each complex number consist two parts, called In-phase and Quadrature (IQ). Both I and Q are represented as a 16 bit unsigned little endian number. I value comes first and Q value after that.

**Byte Order.** Each cell is one byte.


<table>
<tbody>
<tr>
<td>


start + 0:

</td>
<td>


I'<sub>0[7:0]</sub>

</td>
<td>


I'<sub>0[15:8]</sub>

</td>
</tr>
<tr>
<td>


start + 2:

</td>
<td>


Q'<sub>0[7:0]</sub>

</td>
<td>


Q'<sub>0[15:8]</sub>

</td>
</tr>
</tbody>
</table>
