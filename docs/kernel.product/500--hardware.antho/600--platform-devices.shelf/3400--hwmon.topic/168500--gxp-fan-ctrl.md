---
title: "Kernel driver gxp-fan-ctrl"
type: reference
description: "Supported chips:"
---

<a id="rst-kernel-driver-gxp-fan-ctrl"></a>

<!-- SPDX-License-Identifier: GPL-2.0-only -->

Supported chips:

> - HPE GXP SOC

Author: Nick Hawkins &lt;[nick.hawkins@hpe.com](<mailto:nick.hawkins@hpe.com>)&gt;

<a id="rst-description"></a>

## Description

gxp-fan-ctrl is a driver which provides fan control for the hpe gxp soc. The driver allows the gathering of fan status and the use of fan PWM control.

<a id="rst-sysfs-attributes"></a>

## Sysfs attributes


<table>
<tbody>
<tr>
<td>


pwm\[0-7\]

</td>
<td>


Fan 0 to 7 respective PWM value (0-255)

</td>
</tr>
<tr>
<td>


fan\[0-7\]\_fault

</td>
<td>


Fan 0 to 7 respective fault status: 1 fail, 0 ok

</td>
</tr>
<tr>
<td>


fan\[0-7\]\_enable

</td>
<td>


Fan 0 to 7 respective enabled status: 1 enabled, 0 disabled

</td>
</tr>
</tbody>
</table>
