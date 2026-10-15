---
title: "Kernel driver gigabyte_waterforce"
type: reference
description: "Supported devices:"
---

<a id="rst-kernel-driver-gigabyte-waterforce"></a>

<!-- SPDX-License-Identifier: GPL-2.0-or-later -->

Supported devices:

- Gigabyte AORUS WATERFORCE X240

- Gigabyte AORUS WATERFORCE X280

- Gigabyte AORUS WATERFORCE X360

Author: Aleksa Savic

<a id="rst-description"></a>

## Description

This driver enables hardware monitoring support for the listed Gigabyte Waterforce all-in-one CPU liquid coolers. Available sensors are pump and fan speed in RPM, as well as coolant temperature. Also available through debugfs is the firmware version.

Attaching a fan is optional and allows it to be controlled from the device. If it's not connected, the fan-related sensors will report zeroes.

The addressable RGB LEDs and LCD screen are not supported in this driver and should be controlled through userspace tools.

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


Fan speed (in rpm)

</td>
</tr>
<tr>
<td>


fan2_input

</td>
<td>


Pump speed (in rpm)

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


Device firmware version

</td>
</tr>
</tbody>
</table>
