---
title: "V4L2_META_FMT_VIVID ('VIVD')"
type: reference
description: "VIVID Metadata Format"
---

<a id="rst-v4l2-meta-fmt-vivid-vivd"></a>
<a id="rst-v4l2-meta-fmt-vivid"></a>

<!-- SPDX-License-Identifier: GPL-2.0 OR GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

VIVID Metadata Format

<a id="rst-description"></a>

## Description

This describes metadata format used by the vivid driver.

It sets Brightness, Saturation, Contrast and Hue, each of which maps to corresponding controls of the vivid driver with respect to the range and default values.

It contains the following fields:


<table>
<caption>VIVID Metadata</caption>
<thead>
<tr>
<th>


Field

</th>
<th>


Description

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


u16 brightness;

</td>
<td>


Image brightness, the value is in the range 0 to 255, with the default value as 128.

</td>
</tr>
<tr>
<td>


u16 contrast;

</td>
<td>


Image contrast, the value is in the range 0 to 255, with the default value as 128.

</td>
</tr>
<tr>
<td>


u16 saturation;

</td>
<td>


Image color saturation, the value is in the range 0 to 255, with the default value as 128.

</td>
</tr>
<tr>
<td>


s16 hue;

</td>
<td>


Image color balance, the value is in the range -128 to 128, with the default value as 0.

</td>
</tr>
</tbody>
</table>
