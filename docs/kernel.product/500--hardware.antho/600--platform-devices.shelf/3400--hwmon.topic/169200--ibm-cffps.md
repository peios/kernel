---
title: "Kernel driver ibm-cffps"
type: reference
description: "Supported chips:"
---

<a id="rst-kernel-driver-ibm-cffps"></a>

Supported chips:

> - IBM Common Form Factor power supply

Author: Eddie James &lt;[eajames@us.ibm.com](<mailto:eajames@us.ibm.com>)&gt;

<a id="rst-description"></a>

## Description

This driver supports IBM Common Form Factor (CFF) power supplies. This driver is a client to the core PMBus driver.

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


curr1_alarm

</td>
<td>


Output current over-current alarm.

</td>
</tr>
<tr>
<td>


curr1_input

</td>
<td>


Measured output current in mA.

</td>
</tr>
<tr>
<td>


curr1_label

</td>
<td>


"iout1"

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


fan2_alarm

</td>
<td>


Fan 2 warning.

</td>
</tr>
<tr>
<td>


fan2_fault

</td>
<td>


Fan 2 fault.

</td>
</tr>
<tr>
<td>


fan2_input

</td>
<td>


Fan 2 speed in RPM.

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


in2_alarm

</td>
<td>


Output voltage over-voltage alarm.

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


temp1_alarm

</td>
<td>


PSU inlet ambient temperature over-temperature alarm.

</td>
</tr>
<tr>
<td>


temp1_input

</td>
<td>


Measured PSU inlet ambient temp in millidegrees C.

</td>
</tr>
<tr>
<td>


temp2_alarm

</td>
<td>


Secondary rectifier temp over-temperature alarm.

</td>
</tr>
<tr>
<td>


temp2_input

</td>
<td>


Measured secondary rectifier temp in millidegrees C.

</td>
</tr>
<tr>
<td>


temp3_alarm

</td>
<td>


ORing FET temperature over-temperature alarm.

</td>
</tr>
<tr>
<td>


temp3_input

</td>
<td>


Measured ORing FET temperature in millidegrees C.

</td>
</tr>
</tbody>
</table>
