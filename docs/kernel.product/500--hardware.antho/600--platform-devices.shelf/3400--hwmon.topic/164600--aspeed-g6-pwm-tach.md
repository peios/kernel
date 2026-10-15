---
title: "Kernel driver aspeed-g6-pwm-tach"
type: reference
description: "ASPEED AST2600"
---

<a id="rst-kernel-driver-aspeed-g6-pwm-tach"></a>

<!-- SPDX-License-Identifier: GPL-2.0-or-later -->

- **Supported chips:**

  ASPEED AST2600

- **Authors:**

  &lt;[billy_tsai@aspeedtech.com](<mailto:billy_tsai@aspeedtech.com>)&gt;

<a id="rst-description"></a>

## Description:

This driver implements support for ASPEED AST2600 Fan Tacho controller. The controller supports up to 16 tachometer inputs.

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


fanX_div

</td>
<td>


rw

</td>
<td>


Fan divisor: Supported value are power of 4 (1, 4, 16 64, ... 4194304) The larger divisor, the less rpm accuracy and the less affected by fan signal glitch.

</td>
</tr>
</tbody>
</table>
