---
title: "V4L2_SDR_FMT_CS8 ('CS08')"
type: reference
description: "Complex signed 8-bit IQ sample"
---

<a id="rst-v4l2-sdr-fmt-cs8-cs08"></a>
<a id="rst-v4l2-sdr-fmt-cs8"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

Complex signed 8-bit IQ sample

<a id="rst-description"></a>

## Description

This format contains sequence of complex number samples. Each complex number consist two parts, called In-phase and Quadrature (IQ). Both I and Q are represented as a 8 bit signed number. I value comes first and Q value after that.

**Byte Order.** Each cell is one byte.


<table>
<tbody>
<tr>
<td>


start + 0:

</td>
<td>


I'<sub>0</sub>

</td>
</tr>
<tr>
<td>


start + 1:

</td>
<td>


Q'<sub>0</sub>

</td>
</tr>
</tbody>
</table>
