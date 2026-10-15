---
title: "V4L2_SDR_FMT_RU12LE ('RU12')"
type: reference
description: "Real unsigned 12-bit little endian sample"
---

<a id="rst-v4l2-sdr-fmt-ru12le-ru12"></a>
<a id="rst-v4l2-sdr-fmt-ru12le"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

Real unsigned 12-bit little endian sample

<a id="rst-description"></a>

## Description

This format contains sequence of real number samples. Each sample is represented as a 12 bit unsigned little endian number. Sample is stored in 16 bit space with unused high bits padded with 0.

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


I'<sub>0[11:8]</sub>

</td>
</tr>
</tbody>
</table>
