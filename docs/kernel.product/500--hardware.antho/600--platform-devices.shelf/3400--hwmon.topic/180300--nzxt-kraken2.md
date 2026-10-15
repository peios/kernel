---
title: "Kernel driver nzxt-kraken2"
type: reference
description: "Supported devices:"
---

<a id="rst-kernel-driver-nzxt-kraken2"></a>

<!-- SPDX-License-Identifier: GPL-2.0-or-later -->

Supported devices:

- NZXT Kraken X42

- NZXT Kraken X52

- NZXT Kraken X62

- NZXT Kraken X72

Author: Jonas Malaco

<a id="rst-description"></a>

## Description

This driver enables hardware monitoring support for NZXT Kraken X42/X52/X62/X72 all-in-one CPU liquid coolers.  Three sensors are available: fan speed, pump speed and coolant temperature.

Fan and pump control, while supported by the firmware, are not currently exposed.  The addressable RGB LEDs, present in the integrated CPU water block and pump head, are not supported either.  But both features can be found in existing user-space tools (e.g. [liquidctl](<https://github.com/liquidctl/liquidctl>)).

<a id="rst-liquidctl"></a>



<a id="rst-usage-notes"></a>

## Usage Notes

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
