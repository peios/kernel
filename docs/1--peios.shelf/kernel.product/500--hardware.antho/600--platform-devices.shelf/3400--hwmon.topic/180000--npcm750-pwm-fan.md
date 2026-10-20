---
title: "Kernel driver npcm750-pwm-fan"
type: reference
description: "Supported chips:"
---

<a id="rst-kernel-driver-npcm750-pwm-fan"></a>

Supported chips:

> NUVOTON NPCM750/730/715/705

Authors:

> &lt;[tomer.maimon@nuvoton.com](<mailto:tomer.maimon@nuvoton.com>)&gt;

<a id="rst-description"></a>

## Description:

This driver implements support for NUVOTON NPCM7XX PWM and Fan Tacho controller. The PWM controller supports up to 8 PWM outputs. The Fan tacho controller supports up to 16 tachometer inputs.

The driver provides the following sensor accesses in sysfs:


<table>
<tbody>
<tr>
<td>


fanX_input

</td>
<td>


ro

</td>
<td>


provide current fan rotation value in RPM as reported by the fan to the device.

</td>
</tr>
<tr>
<td>


pwmX

</td>
<td>


rw

</td>
<td>


get or set PWM fan control value. This is an integer value between 0(off) and 255(full speed).

</td>
</tr>
</tbody>
</table>
