---
title: "Kernel driver cgbc-hwmon"
type: reference
description: "Supported chips:"
---

<a id="rst-kernel-driver-cgbc-hwmon"></a>

<!-- SPDX-License-Identifier: GPL-2.0-or-later -->

Supported chips:

> - Congatec Board Controller.
>
>   Prefix: 'cgbc-hwmon'

Author: Thomas Richard &lt;[thomas.richard@bootlin.com](<mailto:thomas.richard@bootlin.com>)&gt;

<a id="rst-description"></a>

## Description

This driver enables monitoring support for the Congatec Board Controller. This controller is embedded on the x86 SoMs of Congatec.

<a id="rst-sysfs-entries"></a>

## Sysfs entries

The following sysfs entries list contains all sensors defined in the Board Controller. The available sensors in sysfs depend on the SoM and the system.


<table>
<thead>
<tr>
<th>


Name

</th>
<th>


Description

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


temp1_input

</td>
<td>


CPU temperature

</td>
</tr>
<tr>
<td>


temp2_input

</td>
<td>


Box temperature

</td>
</tr>
<tr>
<td>


temp3_input

</td>
<td>


Ambient temperature

</td>
</tr>
<tr>
<td>


temp4_input

</td>
<td>


Board temperature

</td>
</tr>
<tr>
<td>


temp5_input

</td>
<td>


Carrier temperature

</td>
</tr>
<tr>
<td>


temp6_input

</td>
<td>


Chipset temperature

</td>
</tr>
<tr>
<td>


temp7_input

</td>
<td>


Video temperature

</td>
</tr>
<tr>
<td>


temp8_input

</td>
<td>


Other temperature

</td>
</tr>
<tr>
<td>


temp9_input

</td>
<td>


TOPDIM temperature

</td>
</tr>
<tr>
<td>


temp10_input

</td>
<td>


BOTTOMDIM temperature

</td>
</tr>
<tr>
<td>


in0_input

</td>
<td>


CPU voltage

</td>
</tr>
<tr>
<td>


in1_input

</td>
<td>


DC Runtime voltage

</td>
</tr>
<tr>
<td>


in2_input

</td>
<td>


DC Standby voltage

</td>
</tr>
<tr>
<td>


in3_input

</td>
<td>


CMOS Battery voltage

</td>
</tr>
<tr>
<td>


in4_input

</td>
<td>


Battery voltage

</td>
</tr>
<tr>
<td>


in5_input

</td>
<td>


AC voltage

</td>
</tr>
<tr>
<td>


in6_input

</td>
<td>


Other voltage

</td>
</tr>
<tr>
<td>


in7_input

</td>
<td>


5V voltage

</td>
</tr>
<tr>
<td>


in8_input

</td>
<td>


5V Standby voltage

</td>
</tr>
<tr>
<td>


in9_input

</td>
<td>


3V3 voltage

</td>
</tr>
<tr>
<td>


in10_input

</td>
<td>


3V3 Standby voltage

</td>
</tr>
<tr>
<td>


in11_input

</td>
<td>


VCore A voltage

</td>
</tr>
<tr>
<td>


in12_input

</td>
<td>


VCore B voltage

</td>
</tr>
<tr>
<td>


in13_input

</td>
<td>


12V voltage

</td>
</tr>
<tr>
<td>


curr1_input

</td>
<td>


DC current

</td>
</tr>
<tr>
<td>


curr2_input

</td>
<td>


5V current

</td>
</tr>
<tr>
<td>


curr3_input

</td>
<td>


12V current

</td>
</tr>
<tr>
<td>


fan1_input

</td>
<td>


CPU fan

</td>
</tr>
<tr>
<td>


fan2_input

</td>
<td>


Box fan

</td>
</tr>
<tr>
<td>


fan3_input

</td>
<td>


Ambient fan

</td>
</tr>
<tr>
<td>


fan4_input

</td>
<td>


Chiptset fan

</td>
</tr>
<tr>
<td>


fan5_input

</td>
<td>


Video fan

</td>
</tr>
<tr>
<td>


fan6_input

</td>
<td>


Other fan

</td>
</tr>
</tbody>
</table>
