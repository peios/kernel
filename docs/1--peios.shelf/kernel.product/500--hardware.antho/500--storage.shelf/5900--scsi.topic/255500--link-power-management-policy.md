---
title: "Link Power Managent Policy"
type: reference
description: "This parameter allows the user to set the link (interface) power management. There are 6 possible options:"
---

<a id="rst-link-power-managent-policy"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

This parameter allows the user to set the link (interface) power management. There are 6 possible options:


<table>
<thead>
<tr>
<th>


Value

</th>
<th>


Effect

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


min_power

</td>
<td>


Enable slumber mode(no partial mode) for the link to use the least possible power when possible.  This may sacrifice some performance due to increased latency when coming out of lower power states.

</td>
</tr>
<tr>
<td>


max_performance

</td>
<td>


Generally, this means no power management.  Tell the controller to have performance be a priority over power management.

</td>
</tr>
<tr>
<td>


medium_power

</td>
<td>


Tell the controller to enter a lower power state when possible, but do not enter the lowest power state, thus improving latency over min_power setting.

</td>
</tr>
<tr>
<td>


keep_firmware_settings

</td>
<td>


Do not change the current firmware settings for Power management. This is the default setting.

</td>
</tr>
<tr>
<td>


med_power_with_dipm

</td>
<td>


Same as medium_power, but additionally with Device-initiated power management(DIPM) enabled, as Intel Rapid Storage Technology(IRST) does.

</td>
</tr>
<tr>
<td>


min_power_with_partial

</td>
<td>


Same as min_power, but additionally with partial power state enabled, which may improve performance over min_power setting.

</td>
</tr>
</tbody>
</table>
