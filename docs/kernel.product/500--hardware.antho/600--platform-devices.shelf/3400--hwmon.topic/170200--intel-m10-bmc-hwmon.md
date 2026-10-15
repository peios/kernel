---
title: "Kernel driver intel-m10-bmc-hwmon"
type: reference
description: "Supported chips:"
---

<a id="rst-kernel-driver-intel-m10-bmc-hwmon"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

Supported chips:

> - Intel MAX 10 BMC for Intel PAC N3000
>
>   Prefix: 'n3000bmc-hwmon'

Author: Xu Yilun &lt;[yilun.xu@intel.com](<mailto:yilun.xu@intel.com>)&gt;

<a id="rst-description"></a>

## Description

This driver adds the temperature, voltage, current and power reading support for the Intel MAX 10 Board Management Controller (BMC) chip. The BMC chip is integrated in some Intel Programmable Acceleration Cards (PAC). It connects to a set of sensor chips to monitor the sensor data of different components on the board. The BMC firmware is responsible for sensor data sampling and recording in shared registers. The host driver reads the sensor data from these shared registers and exposes them to users as hwmon interfaces.

The BMC chip is implemented using the Intel MAX 10 CPLD. It could be reprogramed to some variants in order to support different Intel PACs. The driver is designed to be able to distinguish between the variants, but now it only supports the BMC for Intel PAC N3000.

<a id="rst-sysfs-attributes"></a>

## Sysfs attributes

The following attributes are supported:

- Intel MAX 10 BMC for Intel PAC N3000:


<table>
<tbody>
<tr>
<td>


tempX_input

</td>
<td>


Temperature of the component (specified by tempX_label)

</td>
</tr>
<tr>
<td>


tempX_max

</td>
<td>


Temperature maximum setpoint of the component

</td>
</tr>
<tr>
<td>


tempX_crit

</td>
<td>


Temperature critical setpoint of the component

</td>
</tr>
<tr>
<td>


tempX_max_hyst

</td>
<td>


Hysteresis for temperature maximum of the component

</td>
</tr>
<tr>
<td>


tempX_crit_hyst

</td>
<td>


Hysteresis for temperature critical of the component

</td>
</tr>
<tr>
<td>


temp1_label

</td>
<td>


"Board Temperature"

</td>
</tr>
<tr>
<td>


temp2_label

</td>
<td>


"FPGA Die Temperature"

</td>
</tr>
<tr>
<td>


temp3_label

</td>
<td>


"QSFP0 Temperature"

</td>
</tr>
<tr>
<td>


temp4_label

</td>
<td>


"QSFP1 Temperature"

</td>
</tr>
<tr>
<td>


temp5_label

</td>
<td>


"Retimer A Temperature"

</td>
</tr>
<tr>
<td>


temp6_label

</td>
<td>


"Retimer A SerDes Temperature"

</td>
</tr>
<tr>
<td>


temp7_label

</td>
<td>


"Retimer B Temperature"

</td>
</tr>
<tr>
<td>


temp8_label

</td>
<td>


"Retimer B SerDes Temperature"

</td>
</tr>
<tr>
<td>


inX_input

</td>
<td>


Measured voltage of the component (specified by inX_label)

</td>
</tr>
<tr>
<td>


in0_label

</td>
<td>


"QSFP0 Supply Voltage"

</td>
</tr>
<tr>
<td>


in1_label

</td>
<td>


"QSFP1 Supply Voltage"

</td>
</tr>
<tr>
<td>


in2_label

</td>
<td>


"FPGA Core Voltage"

</td>
</tr>
<tr>
<td>


in3_label

</td>
<td>


"12V Backplane Voltage"

</td>
</tr>
<tr>
<td>


in4_label

</td>
<td>


"1.2V Voltage"

</td>
</tr>
<tr>
<td>


in5_label

</td>
<td>


"12V AUX Voltage"

</td>
</tr>
<tr>
<td>


in6_label

</td>
<td>


"1.8V Voltage"

</td>
</tr>
<tr>
<td>


in7_label

</td>
<td>


"3.3V Voltage"

</td>
</tr>
<tr>
<td>


currX_input

</td>
<td>


Measured current of the component (specified by currX_label)

</td>
</tr>
<tr>
<td>


curr1_label

</td>
<td>


"FPGA Core Current"

</td>
</tr>
<tr>
<td>


curr2_label

</td>
<td>


"12V Backplane Current"

</td>
</tr>
<tr>
<td>


curr3_label

</td>
<td>


"12V AUX Current"

</td>
</tr>
<tr>
<td>


powerX_input

</td>
<td>


Measured power of the component (specified by powerX_label)

</td>
</tr>
<tr>
<td>


power1_label

</td>
<td>


"Board Power"

</td>
</tr>
</tbody>
</table>

All the attributes are read-only.
