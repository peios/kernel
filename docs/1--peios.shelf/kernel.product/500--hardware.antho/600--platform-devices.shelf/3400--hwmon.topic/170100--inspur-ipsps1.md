---
title: "Kernel driver inspur-ipsps1"
type: reference
description: "Supported chips:"
---

<a id="rst-kernel-driver-inspur-ipsps1"></a>

Supported chips:

> - Inspur Power System power supply unit

Author: John Wang &lt;[wangzqbj@inspur.com](<mailto:wangzqbj@inspur.com>)&gt;

<a id="rst-description"></a>

## Description

This driver supports Inspur Power System power supplies. This driver is a client to the core PMBus driver.

<a id="rst-usage-notes"></a>

## Usage Notes

This driver does not auto-detect devices. You will have to instantiate the devices explicitly. Please see [Documentation/i2c/instantiating-devices.rst](~kernel/hardware/i2c/instantiating-devices) for details.

<a id="rst-sysfs-entries"></a>

## Sysfs entries

The following attributes are supported:


<table>
<tbody>
<tr>
<td>


curr1_input

</td>
<td>


Measured input current

</td>
</tr>
<tr>
<td>


curr1_label

</td>
<td>


"iin"

</td>
</tr>
<tr>
<td>


curr1_max

</td>
<td>


Maximum current

</td>
</tr>
<tr>
<td>


curr1_max_alarm

</td>
<td>


Current high alarm

</td>
</tr>
<tr>
<td>


curr2_input

</td>
<td>


Measured output current in mA.

</td>
</tr>
<tr>
<td>


curr2_label

</td>
<td>


"iout1"

</td>
</tr>
<tr>
<td>


curr2_crit

</td>
<td>


Critical maximum current

</td>
</tr>
<tr>
<td>


curr2_crit_alarm

</td>
<td>


Current critical high alarm

</td>
</tr>
<tr>
<td>


curr2_max

</td>
<td>


Maximum current

</td>
</tr>
<tr>
<td>


curr2_max_alarm

</td>
<td>


Current high alarm

</td>
</tr>
<tr>
<td>


fan1_alarm

</td>
<td>


Fan 1 warning.

</td>
</tr>
<tr>
<td>


fan1_fault

</td>
<td>


Fan 1 fault.

</td>
</tr>
<tr>
<td>


fan1_input

</td>
<td>


Fan 1 speed in RPM.

</td>
</tr>
<tr>
<td>


in1_alarm

</td>
<td>


Input voltage under-voltage alarm.

</td>
</tr>
<tr>
<td>


in1_input

</td>
<td>


Measured input voltage in mV.

</td>
</tr>
<tr>
<td>


in1_label

</td>
<td>


"vin"

</td>
</tr>
<tr>
<td>


in2_input

</td>
<td>


Measured output voltage in mV.

</td>
</tr>
<tr>
<td>


in2_label

</td>
<td>


"vout1"

</td>
</tr>
<tr>
<td>


in2_lcrit

</td>
<td>


Critical minimum output voltage

</td>
</tr>
<tr>
<td>


in2_lcrit_alarm

</td>
<td>


Output voltage critical low alarm

</td>
</tr>
<tr>
<td>


in2_max

</td>
<td>


Maximum output voltage

</td>
</tr>
<tr>
<td>


in2_max_alarm

</td>
<td>


Output voltage high alarm

</td>
</tr>
<tr>
<td>


in2_min

</td>
<td>


Minimum output voltage

</td>
</tr>
<tr>
<td>


in2_min_alarm

</td>
<td>


Output voltage low alarm

</td>
</tr>
<tr>
<td>


power1_alarm

</td>
<td>


Input fault or alarm.

</td>
</tr>
<tr>
<td>


power1_input

</td>
<td>


Measured input power in uW.

</td>
</tr>
<tr>
<td>


power1_label

</td>
<td>


"pin"

</td>
</tr>
<tr>
<td>


power1_max

</td>
<td>


Input power limit

</td>
</tr>
<tr>
<td>


power2_max_alarm

</td>
<td>


Output power high alarm

</td>
</tr>
<tr>
<td>


power2_max

</td>
<td>


Output power limit

</td>
</tr>
<tr>
<td>


power2_input

</td>
<td>


Measured output power in uW.

</td>
</tr>
<tr>
<td>


power2_label

</td>
<td>


"pout"

</td>
</tr>
<tr>
<td>


temp\[1-3\]\_input

</td>
<td>


Measured temperature

</td>
</tr>
<tr>
<td>


temp\[1-2\]\_max

</td>
<td>


Maximum temperature

</td>
</tr>
<tr>
<td>


temp\[1-3\]\_max_alarm

</td>
<td>


Temperature high alarm

</td>
</tr>
<tr>
<td>


vendor

</td>
<td>


Manufacturer name

</td>
</tr>
<tr>
<td>


model

</td>
<td>


Product model

</td>
</tr>
<tr>
<td>


part_number

</td>
<td>


Product part number

</td>
</tr>
<tr>
<td>


serial_number

</td>
<td>


Product serial number

</td>
</tr>
<tr>
<td>


fw_version

</td>
<td>


Firmware version

</td>
</tr>
<tr>
<td>


hw_version

</td>
<td>


Hardware version

</td>
</tr>
<tr>
<td>


mode

</td>
<td>


Work mode. Can be set to active or standby, when set to standby, PSU will automatically switch between standby and redundancy mode.

</td>
</tr>
</tbody>
</table>
