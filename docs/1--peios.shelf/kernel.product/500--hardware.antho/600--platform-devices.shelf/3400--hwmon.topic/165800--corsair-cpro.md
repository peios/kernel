---
title: "Kernel driver corsair-cpro"
type: reference
description: "Supported devices:"
---

<a id="rst-kernel-driver-corsair-cpro"></a>

<!-- SPDX-License-Identifier: GPL-2.0-or-later -->

Supported devices:

> - Corsair Commander Pro
>
> - Corsair Commander Pro (1000D)

Author: Marius Zachmann

<a id="rst-description"></a>

## Description

This driver implements the sysfs interface for the Corsair Commander Pro. The Corsair Commander Pro is a USB device with 6 fan connectors, 4 temperature sensor connectors and 2 Corsair LED connectors. It can read the voltage levels on the SATA power connector.

<a id="rst-usage-notes"></a>

## Usage Notes

Since it is a USB device, hotswapping is possible. The device is autodetected.

<a id="rst-sysfs-entries"></a>

## Sysfs entries


<table>
<tbody>
<tr>
<td>


in0_input

</td>
<td>


Voltage on SATA 12v

</td>
</tr>
<tr>
<td>


in1_input

</td>
<td>


Voltage on SATA 5v

</td>
</tr>
<tr>
<td>


in2_input

</td>
<td>


Voltage on SATA 3.3v

</td>
</tr>
<tr>
<td>


temp\[1-4\]\_input

</td>
<td>


Temperature on connected temperature sensors

</td>
</tr>
<tr>
<td>


fan\[1-6\]\_input

</td>
<td>


Connected fan rpm.

</td>
</tr>
<tr>
<td>


fan\[1-6\]\_label

</td>
<td>


Shows fan type as detected by the device.

</td>
</tr>
<tr>
<td>


fan\[1-6\]\_target

</td>
<td>


Sets fan speed target rpm. When reading, it reports the last value if it was set by the driver. Otherwise returns an error.

</td>
</tr>
<tr>
<td>


pwm\[1-6\]

</td>
<td>


Sets the fan speed. Values from 0-255. Can only be read if pwm was set directly.

</td>
</tr>
</tbody>
</table>

<a id="rst-debugfs-entries"></a>

## Debugfs entries


<table>
<tbody>
<tr>
<td>


firmware_version

</td>
<td>


Firmware version

</td>
</tr>
<tr>
<td>


bootloader_version

</td>
<td>


Bootloader version

</td>
</tr>
</tbody>
</table>
