---
title: "Kernel driver asus_rog_ryujin"
type: reference
description: "Supported devices:"
---

<a id="rst-kernel-driver-asus-rog-ryujin"></a>

<!-- SPDX-License-Identifier: GPL-2.0-or-later -->

Supported devices:

- ASUS ROG RYUJIN II 360

Author: Aleksa Savic

<a id="rst-description"></a>

## Description

This driver enables hardware monitoring support for the listed ASUS ROG RYUJIN all-in-one CPU liquid coolers. Available sensors are pump, internal and external (controller) fan speed in RPM, their duties in PWM, as well as coolant temperature.

Attaching external fans to the controller is optional and allows them to be controlled from the device. If not connected, the fan-related sensors will report zeroes. The controller is a separate hardware unit that comes bundled with the AIO and connects to it to allow fan control.

The addressable LCD screen is not supported in this driver and should be controlled through userspace tools.

<a id="rst-usage-notes"></a>

## Usage notes

As these are USB HIDs, the driver can be loaded automatically by the kernel and supports hot swapping.

<a id="rst-sysfs-entries"></a>

## Sysfs entries


<table>
<tbody>
<tr>
<td>


fan1_input

</td>
<td>


Pump speed (in rpm)

</td>
</tr>
<tr>
<td>


fan2_input

</td>
<td>


Internal fan speed (in rpm)

</td>
</tr>
<tr>
<td>


fan3_input

</td>
<td>


External (controller) fan 1 speed (in rpm)

</td>
</tr>
<tr>
<td>


fan4_input

</td>
<td>


External (controller) fan 2 speed (in rpm)

</td>
</tr>
<tr>
<td>


fan5_input

</td>
<td>


External (controller) fan 3 speed (in rpm)

</td>
</tr>
<tr>
<td>


fan6_input

</td>
<td>


External (controller) fan 4 speed (in rpm)

</td>
</tr>
<tr>
<td>


temp1_input

</td>
<td>


Coolant temperature (in millidegrees Celsius)

</td>
</tr>
<tr>
<td>


pwm1

</td>
<td>


Pump duty

</td>
</tr>
<tr>
<td>


pwm2

</td>
<td>


Internal fan duty

</td>
</tr>
<tr>
<td>


pwm3

</td>
<td>


External (controller) fan duty

</td>
</tr>
</tbody>
</table>
