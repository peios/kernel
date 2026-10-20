---
title: "Kernel driver corsair-psu"
type: reference
description: "Supported devices:"
---

<a id="rst-kernel-driver-corsair-psu"></a>

<!-- SPDX-License-Identifier: GPL-2.0-or-later -->

Supported devices:

- Corsair Power Supplies

  Corsair HX550i

  Corsair HX650i

  Corsair HX750i

  Corsair HX850i

  Corsair HX1000i (Legacy and Series 2023)

  Corsair HX1200i (Legacy, Series 2023 and Series 2025)

  Corsair HX1500i (Legacy and Series 2023)

  Corsair RM550i

  Corsair RM650i

  Corsair RM750i

  Corsair RM850i

  Corsair RM1000i

Author: Wilken Gottwalt

<a id="rst-description"></a>

## Description

This driver implements the sysfs interface for the Corsair PSUs with a HID protocol interface of the HXi and RMi series. These power supplies provide access to a micro-controller with 2 attached temperature sensors, 1 fan rpm sensor, 4 sensors for volt levels, 4 sensors for power usage and 4 sensors for current levels and additional non-sensor information like uptimes.

<a id="rst-sysfs-entries"></a>

## Sysfs entries


<table>
<tbody>
<tr>
<td>


curr1_input

</td>
<td>


Total current usage

</td>
</tr>
<tr>
<td>


curr2_input

</td>
<td>


Current on the 12v psu rail

</td>
</tr>
<tr>
<td>


curr2_crit

</td>
<td>


Current max critical value on the 12v psu rail

</td>
</tr>
<tr>
<td>


curr3_input

</td>
<td>


Current on the 5v psu rail

</td>
</tr>
<tr>
<td>


curr3_crit

</td>
<td>


Current max critical value on the 5v psu rail

</td>
</tr>
<tr>
<td>


curr4_input

</td>
<td>


Current on the 3.3v psu rail

</td>
</tr>
<tr>
<td>


curr4_crit

</td>
<td>


Current max critical value on the 3.3v psu rail

</td>
</tr>
<tr>
<td>


fan1_input

</td>
<td>


RPM of psu fan

</td>
</tr>
<tr>
<td>


in0_input

</td>
<td>


Voltage of the psu ac input

</td>
</tr>
<tr>
<td>


in1_input

</td>
<td>


Voltage of the 12v psu rail

</td>
</tr>
<tr>
<td>


in1_crit

</td>
<td>


Voltage max critical value on the 12v psu rail

</td>
</tr>
<tr>
<td>


in1_lcrit

</td>
<td>


Voltage min critical value on the 12v psu rail

</td>
</tr>
<tr>
<td>


in2_input

</td>
<td>


Voltage of the 5v psu rail

</td>
</tr>
<tr>
<td>


in2_crit

</td>
<td>


Voltage max critical value on the 5v psu rail

</td>
</tr>
<tr>
<td>


in2_lcrit

</td>
<td>


Voltage min critical value on the 5v psu rail

</td>
</tr>
<tr>
<td>


in3_input

</td>
<td>


Voltage of the 3.3v psu rail

</td>
</tr>
<tr>
<td>


in3_crit

</td>
<td>


Voltage max critical value on the 3.3v psu rail

</td>
</tr>
<tr>
<td>


in3_lcrit

</td>
<td>


Voltage min critical value on the 3.3v psu rail

</td>
</tr>
<tr>
<td>


power1_input

</td>
<td>


Total power usage

</td>
</tr>
<tr>
<td>


power2_input

</td>
<td>


Power usage of the 12v psu rail

</td>
</tr>
<tr>
<td>


power3_input

</td>
<td>


Power usage of the 5v psu rail

</td>
</tr>
<tr>
<td>


power4_input

</td>
<td>


Power usage of the 3.3v psu rail

</td>
</tr>
<tr>
<td>


pwm1

</td>
<td>


PWM value, read only

</td>
</tr>
<tr>
<td>


pwm1_enable

</td>
<td>


PWM mode, read only

</td>
</tr>
<tr>
<td>


temp1_input

</td>
<td>


Temperature of the psu vrm component

</td>
</tr>
<tr>
<td>


temp1_crit

</td>
<td>


Temperature max cirtical value of the psu vrm component

</td>
</tr>
<tr>
<td>


temp2_input

</td>
<td>


Temperature of the psu case

</td>
</tr>
<tr>
<td>


temp2_crit

</td>
<td>


Temperature max critical value of psu case

</td>
</tr>
</tbody>
</table>

<a id="rst-usage-notes"></a>

## Usage Notes

It is an USB HID device, so it is auto-detected, supports hot-swapping and several devices at once.

Flickering values in the rail voltage levels can be an indicator for a failing PSU. Accordingly to the default automatic fan speed plan the fan starts at about 30% of the wattage rating. If this does not happen, a fan failure is likely. The driver also provides some additional useful values via debugfs, which do not fit into the hwmon class.

<a id="rst-debugfs-entries"></a>

## Debugfs entries


<table>
<tbody>
<tr>
<td>


ocpmode

</td>
<td>


Single or multi rail mode of the PCIe power connectors

</td>
</tr>
<tr>
<td>


product

</td>
<td>


Product name of the psu

</td>
</tr>
<tr>
<td>


uptime

</td>
<td>


Session uptime of the psu

</td>
</tr>
<tr>
<td>


uptime_total

</td>
<td>


Total uptime of the psu

</td>
</tr>
<tr>
<td>


vendor

</td>
<td>


Vendor name of the psu

</td>
</tr>
</tbody>
</table>
