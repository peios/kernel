---
title: "Kernel driver aspeed-pwm-tacho"
type: reference
description: "ASPEED AST2400/2500"
---

<a id="rst-kernel-driver-aspeed-pwm-tacho"></a>

- **Supported chips:**

  ASPEED AST2400/2500

- **Authors:**

  &lt;[jaghu@google.com](<mailto:jaghu@google.com>)&gt;

<a id="rst-description"></a>

## Description:

This driver implements support for ASPEED AST2400/2500 PWM and Fan Tacho controller. The PWM controller supports up to 8 PWM outputs. The Fan tacho controller supports up to 16 tachometer inputs.

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
