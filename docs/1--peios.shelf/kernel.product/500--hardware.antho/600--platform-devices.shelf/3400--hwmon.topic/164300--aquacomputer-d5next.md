---
title: "Kernel driver aquacomputer-d5next"
type: reference
description: "Supported devices:"
---

<a id="rst-kernel-driver-aquacomputer-d5next"></a>

<!-- SPDX-License-Identifier: GPL-2.0-or-later -->

Supported devices:

- Aquacomputer Aquaero 5/6 fan controllers

- Aquacomputer D5 Next watercooling pump

- Aquacomputer Farbwerk RGB controller

- Aquacomputer Farbwerk 360 RGB controller

- Aquacomputer Octo fan controller

- Aquacomputer Quadro fan controller

- Aquacomputer High Flow Next sensor

- Aquacomputer Leakshield leak prevention system

- Aquacomputer Aquastream XT watercooling pump

- Aquacomputer Aquastream Ultimate watercooling pump

- Aquacomputer Poweradjust 3 fan controller

- Aquacomputer High Flow USB flow meter

- Aquacomputer MPS Flow devices

Author: Aleksa Savic

<a id="rst-description"></a>

## Description

This driver exposes hardware sensors of listed Aquacomputer devices, which communicate through proprietary USB HID protocols.

The Aquaero devices expose eight physical, eight virtual and four calculated virtual temperature sensors, as well as two flow sensors. The fans expose their speed (in RPM), power, voltage and current. Temperature offsets and fan speeds can be controlled.

For the D5 Next pump, available sensors are pump and fan speed, power, voltage and current, as well as coolant temperature and eight virtual temp sensors. Also available through debugfs are the serial number, firmware version and power-on count. Attaching a fan to it is optional and allows it to be controlled using temperature curves directly from the pump. If it's not connected, the fan-related sensors will report zeroes.

The pump can be configured either through software or via its physical interface. Configuring the pump through this driver is not implemented, as it seems to require sending it a complete configuration. That includes addressable RGB LEDs, for which there is no standard sysfs interface. Thus, that task is better suited for userspace tools.

The Octo exposes four physical and sixteen virtual temperature sensors, a flow sensor as well as eight PWM controllable fans, along with their speed (in RPM), power, voltage and current. Flow sensor pulses are also available.

The Quadro exposes four physical and sixteen virtual temperature sensors, a flow sensor and four PWM controllable fans, along with their speed (in RPM), power, voltage and current. Flow sensor pulses are also available.

The Farbwerk and Farbwerk 360 expose four temperature sensors. Additionally, sixteen virtual temperature sensors of the Farbwerk 360 are exposed.

The High Flow Next exposes +5V voltages, water quality, conductivity and flow readings. A temperature sensor can be connected to it, in which case it provides its reading and an estimation of the dissipated/absorbed power in the liquid cooling loop.

The Leakshield exposes two temperature sensors and coolant pressure (current, min, max and target readings). It also exposes the estimated reservoir volume and how much of it is filled with coolant. Pump RPM and flow can be set to enhance on-device calculations, but this is not yet implemented here.

The Aquastream XT pump exposes temperature readings for the coolant, external sensor and fan IC. It also exposes pump and fan speeds (in RPM), voltages, as well as pump current.

The Aquastream Ultimate pump exposes coolant temp and an external temp sensor, along with speed, power, voltage and current of both the pump and optionally connected fan. It also exposes pressure and flow speed readings.

The Poweradjust 3 controller exposes a single external temperature sensor.

The High Flow USB exposes an internal and external temperature sensor, and a flow meter.

The MPS Flow devices expose the same entries as the High Flow USB because they have the same USB product ID and report sensors equivalently.

Depending on the device, not all sysfs and debugfs entries will be available. Writing to virtual temperature sensors is not currently supported.

<a id="rst-usage-notes"></a>

## Usage notes

The devices communicate via HID reports. The driver is loaded automatically by the kernel and supports hotswapping.

<a id="rst-sysfs-entries"></a>

## Sysfs entries


<table>
<tbody>
<tr>
<td>


temp\[1-20\]\_input

</td>
<td>


Physical/virtual temperature sensors (in millidegrees Celsius)

</td>
</tr>
<tr>
<td>


temp\[1-8\]\_offset

</td>
<td>


Temperature sensor correction offset (in millidegrees Celsius)

</td>
</tr>
<tr>
<td>


fan\[1-9\]\_input

</td>
<td>


Pump/fan speed (in RPM) / Flow speed (in dL/h)

</td>
</tr>
<tr>
<td>


fan1_min

</td>
<td>


Minimal fan speed (in RPM)

</td>
</tr>
<tr>
<td>


fan1_max

</td>
<td>


Maximal fan speed (in RPM)

</td>
</tr>
<tr>
<td>


fan1_target

</td>
<td>


Target fan speed (in RPM)

</td>
</tr>
<tr>
<td>


fan5_pulses

</td>
<td>


Quadro flow sensor pulses

</td>
</tr>
<tr>
<td>


fan9_pulses

</td>
<td>


Octo flow sensor pulses

</td>
</tr>
<tr>
<td>


power\[1-8\]\_input

</td>
<td>


Pump/fan power (in micro Watts)

</td>
</tr>
<tr>
<td>


in\[0-7\]\_input

</td>
<td>


Pump/fan voltage (in milli Volts)

</td>
</tr>
<tr>
<td>


curr\[1-8\]\_input

</td>
<td>


Pump/fan current (in milli Amperes)

</td>
</tr>
<tr>
<td>


pwm\[1-8\]

</td>
<td>


Fan PWM (0 - 255)

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


serial_number

</td>
<td>


Serial number of the device

</td>
</tr>
<tr>
<td>


firmware_version

</td>
<td>


Version of installed firmware

</td>
</tr>
<tr>
<td>


power_cycles

</td>
<td>


Count of how many times the device was powered on

</td>
</tr>
</tbody>
</table>
