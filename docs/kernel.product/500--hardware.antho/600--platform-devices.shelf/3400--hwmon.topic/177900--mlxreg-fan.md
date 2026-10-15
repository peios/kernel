---
title: "Kernel driver mlxreg-fan"
type: reference
description: "Provides FAN control for the next Mellanox systems:"
---

<a id="rst-kernel-driver-mlxreg-fan"></a>

Provides FAN control for the next Mellanox systems:

- QMB700, equipped with 40x200GbE InfiniBand ports;

- MSN3700, equipped with 32x200GbE or 16x400GbE Ethernet ports;

- MSN3410, equipped with 6x400GbE plus 48x50GbE Ethernet ports;

- MSN3800, equipped with 64x1000GbE Ethernet ports;

Author: Vadim Pasternak &lt;[vadimp@mellanox.com](<mailto:vadimp@mellanox.com>)&gt;

These are the Top of the Rack systems, equipped with Mellanox switch board with Mellanox Quantum or Spectrume-2 devices. FAN controller is implemented by the programmable device logic.

The default registers offsets set within the programmable device is as following:


<table>
<tbody>
<tr>
<td>


pwm1

</td>
<td>


0xe3

</td>
</tr>
<tr>
<td>


fan1 (tacho1)

</td>
<td>


0xe4

</td>
</tr>
<tr>
<td>


fan2 (tacho2)

</td>
<td>


0xe5

</td>
</tr>
<tr>
<td>


fan3 (tacho3)

</td>
<td>


0xe6

</td>
</tr>
<tr>
<td>


fan4 (tacho4)

</td>
<td>


0xe7

</td>
</tr>
<tr>
<td>


fan5 (tacho5)

</td>
<td>


0xe8

</td>
</tr>
<tr>
<td>


fan6 (tacho6)

</td>
<td>


0xe9

</td>
</tr>
<tr>
<td>


fan7 (tacho7)

</td>
<td>


0xea

</td>
</tr>
<tr>
<td>


fan8 (tacho8)

</td>
<td>


0xeb

</td>
</tr>
<tr>
<td>


fan9 (tacho9)

</td>
<td>


0xec

</td>
</tr>
<tr>
<td>


fan10 (tacho10)

</td>
<td>


0xed

</td>
</tr>
<tr>
<td>


fan11 (tacho11)

</td>
<td>


0xee

</td>
</tr>
<tr>
<td>


fan12 (tacho12)

</td>
<td>


0xef

</td>
</tr>
</tbody>
</table>

This setup can be re-programmed with other registers.

<a id="rst-description"></a>

## Description

The driver implements a simple interface for driving a fan connected to a PWM output and tachometer inputs. This driver obtains PWM and tachometers registers location according to the system configuration and creates FAN/PWM hwmon objects and a cooling device. PWM and tachometers are sensed through the on-board programmable device, which exports its register map. This device could be attached to any bus type, for which register mapping is supported. Single instance is created with one PWM control, up to 12 tachometers and one cooling device. It could be as many instances as programmable device supports. The driver exposes the fan to the user space through the hwmon's and thermal's sysfs interfaces.

<a id="rst-sys-files-in-hwmon-subsystem"></a>

## /sys files in hwmon subsystem


<table>
<tbody>
<tr>
<td>


fan\[1-12\]\_fault

</td>
<td>


RO

</td>
<td>


files for tachometers TACH1-TACH12 fault indication

</td>
</tr>
<tr>
<td>


fan\[1-12\]\_input

</td>
<td>


RO

</td>
<td>


files for tachometers TACH1-TACH12 input (in RPM)

</td>
</tr>
<tr>
<td>


pwm1

</td>
<td>


RW

</td>
<td>


file for fan\[1-12\] target duty cycle (0..255)

</td>
</tr>
</tbody>
</table>

<a id="rst-sys-files-in-thermal-subsystem"></a>

## /sys files in thermal subsystem


<table>
<tbody>
<tr>
<td>


cur_state

</td>
<td>


RW

</td>
<td>


file for current cooling state of the cooling device (0..max_state)

</td>
</tr>
<tr>
<td>


max_state

</td>
<td>


RO

</td>
<td>


file for maximum cooling state of the cooling device

</td>
</tr>
</tbody>
</table>
