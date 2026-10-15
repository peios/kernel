---
title: "Renesas R-Car Fine Display Processor (FDP1) Driver"
type: reference
description: "The R-Car FDP1 driver implements driver-specific controls as follows."
---

<a id="rst-renesas-r-car-fine-display-processor-fdp1-driver"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

The R-Car FDP1 driver implements driver-specific controls as follows.

- **`V4L2_CID_DEINTERLACING_MODE (menu)`**

  The video deinterlacing mode (such as Bob, Weave, ...). The R-Car FDP1 driver implements the following modes.


<table>
<tbody>
<tr>
<td>


`"Progressive" (0)`

</td>
<td>


The input image video stream is progressive (not interlaced). No deinterlacing is performed. Apart from (optional) format and encoding conversion output frames are identical to the input frames.

</td>
</tr>
<tr>
<td>


`"Adaptive 2D/3D" (1)`

</td>
<td>


Motion adaptive version of 2D and 3D deinterlacing. Use 3D deinterlacing in the presence of fast motion and 2D deinterlacing with diagonal interpolation otherwise.

</td>
</tr>
<tr>
<td>


`"Fixed 2D" (2)`

</td>
<td>


The current field is scaled vertically by averaging adjacent lines to recover missing lines. This method is also known as blending or Line Averaging (LAV).

</td>
</tr>
<tr>
<td>


`"Fixed 3D" (3)`

</td>
<td>


The previous and next fields are averaged to recover lines missing from the current field. This method is also known as Field Averaging (FAV).

</td>
</tr>
<tr>
<td>


`"Previous field" (4)`

</td>
<td>


The current field is weaved with the previous field, i.e. the previous field is used to fill missing lines from the current field. This method is also known as weave deinterlacing.

</td>
</tr>
<tr>
<td>


`"Next field" (5)`

</td>
<td>


The current field is weaved with the next field, i.e. the next field is used to fill missing lines from the current field. This method is also known as weave deinterlacing.

</td>
</tr>
</tbody>
</table>
