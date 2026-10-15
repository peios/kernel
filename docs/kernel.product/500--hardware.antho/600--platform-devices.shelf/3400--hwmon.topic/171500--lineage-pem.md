---
title: "Kernel driver lineage-pem"
type: reference
description: "Supported devices:"
---

<a id="rst-kernel-driver-lineage-pem"></a>

Supported devices:

> - Lineage Compact Power Line Power Entry Modules
>
>   Prefix: 'lineage-pem'
>
>   Addresses scanned: -
>
>   Documentation:
>
>   > [http://www.lineagepower.com/oem/pdf/CPLI2C.pdf](<http://www.lineagepower.com/oem/pdf/CPLI2C.pdf>)

Author: Guenter Roeck &lt;[linux@roeck-us.net](<mailto:linux@roeck-us.net>)&gt;

<a id="rst-description"></a>

## Description

This driver supports various Lineage Compact Power Line DC/DC and AC/DC converters such as CP1800, CP2000AC, CP2000DC, CP2100DC, and others.

Lineage CPL power entry modules are nominally PMBus compliant. However, most standard PMBus commands are not supported. Specifically, all hardware monitoring and status reporting commands are non-standard. For this reason, a standard PMBus driver can not be used.

<a id="rst-usage-notes"></a>

## Usage Notes

This driver does not probe for Lineage CPL devices, since there is no register which can be safely used to identify the chip. You will have to instantiate the devices explicitly.

Example: the following will load the driver for a Lineage PEM at address 0x40 on I2C bus \#1:



```text
$ modprobe lineage-pem
$ echo lineage-pem 0x40 > /sys/bus/i2c/devices/i2c-1/new_device
```

All Lineage CPL power entry modules have a built-in I2C bus master selector (PCA9541). To ensure device access, this driver should only be used as client driver to the pca9541 I2C master selector driver.

<a id="rst-sysfs-entries"></a>

## Sysfs entries

All Lineage CPL devices report output voltage and device temperature as well as alarms for output voltage, temperature, input voltage, input current, input power, and fan status.

Input voltage, input current, input power, and fan speed measurement is only supported on newer devices. The driver detects if those attributes are supported, and only creates respective sysfs entries if they are.


<table>
<tbody>
<tr>
<td>


in1_input

</td>
<td>


Output voltage (mV)

</td>
</tr>
<tr>
<td>


in1_min_alarm

</td>
<td>


Output undervoltage alarm

</td>
</tr>
<tr>
<td>


in1_max_alarm

</td>
<td>


Output overvoltage alarm

</td>
</tr>
<tr>
<td>


in1_crit

</td>
<td>


Output voltage critical alarm

</td>
</tr>
<tr>
<td>


in2_input

</td>
<td>


Input voltage (mV, optional)

</td>
</tr>
<tr>
<td>


in2_alarm

</td>
<td>


Input voltage alarm

</td>
</tr>
<tr>
<td>


curr1_input

</td>
<td>


Input current (mA, optional)

</td>
</tr>
<tr>
<td>


curr1_alarm

</td>
<td>


Input overcurrent alarm

</td>
</tr>
<tr>
<td>


power1_input

</td>
<td>


Input power (uW, optional)

</td>
</tr>
<tr>
<td>


power1_alarm

</td>
<td>


Input power alarm

</td>
</tr>
<tr>
<td>


fan1_input

</td>
<td>


Fan 1 speed (rpm, optional)

</td>
</tr>
<tr>
<td>


fan2_input

</td>
<td>


Fan 2 speed (rpm, optional)

</td>
</tr>
<tr>
<td>


fan3_input

</td>
<td>


Fan 3 speed (rpm, optional)

</td>
</tr>
<tr>
<td>


temp1_input

</td>
<td>




</td>
</tr>
<tr>
<td>


temp1_max

</td>
<td>




</td>
</tr>
<tr>
<td>


temp1_crit

</td>
<td>




</td>
</tr>
<tr>
<td>


temp1_alarm

</td>
<td>




</td>
</tr>
<tr>
<td>


temp1_crit_alarm

</td>
<td>




</td>
</tr>
<tr>
<td>


temp1_fault

</td>
<td>




</td>
</tr>
</tbody>
</table>
