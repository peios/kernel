---
title: "Kernel Driver IBMPOWERNV"
type: reference
description: "Supported systems:"
---

<a id="rst-kernel-driver-ibmpowernv"></a>

Supported systems:

> - Any recent IBM P servers based on POWERNV platform

Author: Neelesh Gupta

<a id="rst-description"></a>

## Description

This driver implements reading the platform sensors data like temperature/fan/ voltage/power for 'POWERNV' platform.

The driver uses the platform device infrastructure. It probes the device tree for sensor devices during the \__init phase and registers them with the 'hwmon'. 'hwmon' populates the 'sysfs' tree having attribute files, each for a given sensor type and its attribute data.

All the nodes in the DT appear under "/ibm,opal/sensors" and each valid node in the DT maps to an attribute file in 'sysfs'. The node exports unique 'sensor-id' which the driver uses to make an OPAL call to the firmware.

<a id="rst-usage-notes"></a>

## Usage notes

The driver is built statically with the kernel by enabling the config CONFIG_SENSORS_IBMPOWERNV. It can also be built as module 'ibmpowernv'.

<a id="rst-sysfs-attributes"></a>

## Sysfs attributes


<table>
<tbody>
<tr>
<td>


fanX_input

</td>
<td>


Measured RPM value.

</td>
</tr>
<tr>
<td>


fanX_min

</td>
<td>


Threshold RPM for alert generation.

</td>
</tr>
<tr>
<td>


fanX_fault

</td>
<td>


- 0: No fail condition

- 1: Failing fan

</td>
</tr>
<tr>
<td>


tempX_input

</td>
<td>


Measured ambient temperature.

</td>
</tr>
<tr>
<td>


tempX_max

</td>
<td>


Threshold ambient temperature for alert generation.

</td>
</tr>
<tr>
<td>


tempX_highest

</td>
<td>


Historical maximum temperature

</td>
</tr>
<tr>
<td>


tempX_lowest

</td>
<td>


Historical minimum temperature

</td>
</tr>
<tr>
<td>


tempX_enable

</td>
<td>


Enable/disable all temperature sensors belonging to the sub-group. In POWER9, this attribute corresponds to each OCC. Using this attribute each OCC can be asked to disable/enable all of its temperature sensors.

- 1: Enable

- 0: Disable

</td>
</tr>
<tr>
<td>


inX_input

</td>
<td>


Measured power supply voltage (millivolt)

</td>
</tr>
<tr>
<td>


inX_fault

</td>
<td>


- 0: No fail condition.

- 1: Failing power supply.

</td>
</tr>
<tr>
<td>


inX_highest

</td>
<td>


Historical maximum voltage

</td>
</tr>
<tr>
<td>


inX_lowest

</td>
<td>


Historical minimum voltage

</td>
</tr>
<tr>
<td>


inX_enable

</td>
<td>


Enable/disable all voltage sensors belonging to the sub-group. In POWER9, this attribute corresponds to each OCC. Using this attribute each OCC can be asked to disable/enable all of its voltage sensors.

- 1: Enable

- 0: Disable

</td>
</tr>
<tr>
<td>


powerX_input

</td>
<td>


Power consumption (microWatt)

</td>
</tr>
<tr>
<td>


powerX_input_highest

</td>
<td>


Historical maximum power

</td>
</tr>
<tr>
<td>


powerX_input_lowest

</td>
<td>


Historical minimum power

</td>
</tr>
<tr>
<td>


powerX_enable

</td>
<td>


Enable/disable all power sensors belonging to the sub-group. In POWER9, this attribute corresponds to each OCC. Using this attribute each OCC can be asked to disable/enable all of its power sensors.

- 1: Enable

- 0: Disable

</td>
</tr>
<tr>
<td>


currX_input

</td>
<td>


Measured current (milliampere)

</td>
</tr>
<tr>
<td>


currX_highest

</td>
<td>


Historical maximum current

</td>
</tr>
<tr>
<td>


currX_lowest

</td>
<td>


Historical minimum current

</td>
</tr>
<tr>
<td>


currX_enable

</td>
<td>


Enable/disable all current sensors belonging to the sub-group. In POWER9, this attribute corresponds to each OCC. Using this attribute each OCC can be asked to disable/enable all of its current sensors.

- 1: Enable

- 0: Disable

</td>
</tr>
<tr>
<td>


energyX_input

</td>
<td>


Cumulative energy (microJoule)

</td>
</tr>
</tbody>
</table>
