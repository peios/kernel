---
title: "Kernel driver nzxt-kraken3"
type: reference
description: "Supported devices:"
---

<a id="rst-kernel-driver-nzxt-kraken3"></a>

<!-- SPDX-License-Identifier: GPL-2.0-or-later -->

Supported devices:

- NZXT Kraken X53

- NZXT Kraken X63

- NZXT Kraken X73

- NZXT Kraken Z53

- NZXT Kraken Z63

- NZXT Kraken Z73

- NZXT Kraken 2023

- NZXT Kraken 2023 Elite

Author: Jonas Malaco, Aleksa Savic

<a id="rst-description"></a>

## Description

This driver enables hardware monitoring support for NZXT Kraken X53/X63/X73, Z53/Z63/Z73 and Kraken 2023 (standard and Elite) all-in-one CPU liquid coolers. All models expose liquid temperature and pump speed (in RPM), as well as PWM control (either as a fixed value or through a temp-PWM curve). The Z-series and Kraken 2023 models additionally expose the speed and duty of an optionally connected fan, with the same PWM control capabilities.

Pump and fan duty control mode can be set through pwm\[1-2\]\_enable, where 1 is for the manual control mode and 2 is for the liquid temp to PWM curve mode. Writing a 0 disables control of the channel through the driver after setting its duty to 100%.

The temperature of the curves relates to the fixed \[20-59\] range, correlating to the detected liquid temperature. Only PWM values (ranging from 0-255) can be set. If in curve mode, setting point values should be done in moderation - the devices require complete curves to be sent for each change; they can lock up or discard the changes if they are too numerous at once. Suggestion is to set them while in an another mode, and then apply them by switching to curve.

The devices can report if they are faulty. The driver supports that situation and will issue a warning. This can also happen when the USB cable is connected, but SATA power is not.

The addressable RGB LEDs and LCD screen (only on Z-series and Kraken 2023 models) are not supported in this driver, but can be controlled through existing userspace tools, such as [liquidctl](<https://github.com/liquidctl/liquidctl>).

<a id="rst-liquidctl"></a>



<a id="rst-usage-notes"></a>

## Usage Notes

As these are USB HIDs, the driver can be loaded automatically by the kernel and supports hot swapping.

Possible pwm_enable values are:


<table>
<tbody>
<tr>
<td>


0

</td>
<td>


Set fan to 100%

</td>
</tr>
<tr>
<td>


1

</td>
<td>


Direct PWM mode (applies value in corresponding PWM entry)

</td>
</tr>
<tr>
<td>


2

</td>
<td>


Curve control mode (applies the temp-PWM duty curve based on coolant temp)

</td>
</tr>
</tbody>
</table>

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


Fan speed (in rpm)

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


Pump duty (value between 0-255)

</td>
</tr>
<tr>
<td>


pwm1_enable

</td>
<td>


Pump duty control mode (0: disabled, 1: manual, 2: curve)

</td>
</tr>
<tr>
<td>


pwm2

</td>
<td>


Fan duty (value between 0-255)

</td>
</tr>
<tr>
<td>


pwm2_enable

</td>
<td>


Fan duty control mode (0: disabled, 1: manual, 2: curve)

</td>
</tr>
<tr>
<td>


temp\[1-2\]\_auto_point\[1-40\]\_pwm

</td>
<td>


Temp-PWM duty curves (for pump and fan), related to coolant temp

</td>
</tr>
</tbody>
</table>
