---
title: "Kernel driver qnap-mcu-hwmon"
type: reference
description: "This driver enables the use of the hardware monitoring and fan control of the MCU used on some QNAP network attached storage devices."
---

<a id="rst-kernel-driver-qnap-mcu-hwmon"></a>

<!-- SPDX-License-Identifier: GPL-2.0-or-later -->

This driver enables the use of the hardware monitoring and fan control of the MCU used on some QNAP network attached storage devices.

Author: Heiko Stuebner &lt;[heiko@sntech.de](<mailto:heiko@sntech.de>)&gt;

<a id="rst-description"></a>

## Description

The driver implements a simple interface for driving the fan controlled by setting its PWM output value and exposes the fan rpm and case-temperature to user space through hwmon's sysfs interface.

The fan rotation speed returned via the optional 'fan1_input' is calculated inside the MCU device.

The driver provides the following sensor accesses in sysfs:


<table>
<tbody>
<tr>
<td>


fan1_input

</td>
<td>


ro

</td>
<td>


fan tachometer speed in RPM

</td>
</tr>
<tr>
<td>


pwm1

</td>
<td>


rw

</td>
<td>


relative speed (0-255), 255=max. speed.

</td>
</tr>
<tr>
<td>


temp1_input

</td>
<td>


ro

</td>
<td>


Measured temperature in millicelsius

</td>
</tr>
</tbody>
</table>
