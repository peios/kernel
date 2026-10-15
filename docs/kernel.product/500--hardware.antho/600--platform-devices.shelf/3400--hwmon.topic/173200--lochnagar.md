---
title: "Kernel Driver Lochnagar"
type: reference
description: "Cirrus Logic : Lochnagar 2"
---

<a id="rst-kernel-driver-lochnagar"></a>

- **Supported systems:**

  - Cirrus Logic : Lochnagar 2

Author: Lucas A. Tanure Alves

<a id="rst-description"></a>

## Description

Lochnagar 2 features built-in Current Monitor circuitry that allows for the measurement of both voltage and current on up to eight of the supply voltage rails provided to the minicards. The Current Monitor does not require any hardware modifications or external circuitry to operate.

The current and voltage measurements are obtained through the standard register map interface to the Lochnagar board controller, and can therefore be monitored by software.

<a id="rst-sysfs-attributes"></a>

## Sysfs attributes


<table>
<tbody>
<tr>
<td>


temp1_input

</td>
<td>


The Lochnagar board temperature (milliCelsius)

</td>
</tr>
<tr>
<td>


in0_input

</td>
<td>


Measured voltage for DBVDD1 (milliVolts)

</td>
</tr>
<tr>
<td>


in0_label

</td>
<td>


"DBVDD1"

</td>
</tr>
<tr>
<td>


curr1_input

</td>
<td>


Measured current for DBVDD1 (milliAmps)

</td>
</tr>
<tr>
<td>


curr1_label

</td>
<td>


"DBVDD1"

</td>
</tr>
<tr>
<td>


power1_average

</td>
<td>


Measured average power for DBVDD1 (microWatts)

</td>
</tr>
<tr>
<td>


power1_average_interval

</td>
<td>


Power averaging time input valid from 1 to 1708mS

</td>
</tr>
<tr>
<td>


power1_label

</td>
<td>


"DBVDD1"

</td>
</tr>
<tr>
<td>


in1_input

</td>
<td>


Measured voltage for 1V8 DSP (milliVolts)

</td>
</tr>
<tr>
<td>


in1_label

</td>
<td>


"1V8 DSP"

</td>
</tr>
<tr>
<td>


curr2_input

</td>
<td>


Measured current for 1V8 DSP (milliAmps)

</td>
</tr>
<tr>
<td>


curr2_label

</td>
<td>


"1V8 DSP"

</td>
</tr>
<tr>
<td>


power2_average

</td>
<td>


Measured average power for 1V8 DSP (microWatts)

</td>
</tr>
<tr>
<td>


power2_average_interval

</td>
<td>


Power averaging time input valid from 1 to 1708mS

</td>
</tr>
<tr>
<td>


power2_label

</td>
<td>


"1V8 DSP"

</td>
</tr>
<tr>
<td>


in2_input

</td>
<td>


Measured voltage for 1V8 CDC (milliVolts)

</td>
</tr>
<tr>
<td>


in2_label

</td>
<td>


"1V8 CDC"

</td>
</tr>
<tr>
<td>


curr3_input

</td>
<td>


Measured current for 1V8 CDC (milliAmps)

</td>
</tr>
<tr>
<td>


curr3_label

</td>
<td>


"1V8 CDC"

</td>
</tr>
<tr>
<td>


power3_average

</td>
<td>


Measured average power for 1V8 CDC (microWatts)

</td>
</tr>
<tr>
<td>


power3_average_interval

</td>
<td>


Power averaging time input valid from 1 to 1708mS

</td>
</tr>
<tr>
<td>


power3_label

</td>
<td>


"1V8 CDC"

</td>
</tr>
<tr>
<td>


in3_input

</td>
<td>


Measured voltage for VDDCORE DSP (milliVolts)

</td>
</tr>
<tr>
<td>


in3_label

</td>
<td>


"VDDCORE DSP"

</td>
</tr>
<tr>
<td>


curr4_input

</td>
<td>


Measured current for VDDCORE DSP (milliAmps)

</td>
</tr>
<tr>
<td>


curr4_label

</td>
<td>


"VDDCORE DSP"

</td>
</tr>
<tr>
<td>


power4_average

</td>
<td>


Measured average power for VDDCORE DSP (microWatts)

</td>
</tr>
<tr>
<td>


power4_average_interval

</td>
<td>


Power averaging time input valid from 1 to 1708mS

</td>
</tr>
<tr>
<td>


power4_label

</td>
<td>


"VDDCORE DSP"

</td>
</tr>
<tr>
<td>


in4_input

</td>
<td>


Measured voltage for AVDD 1V8 (milliVolts)

</td>
</tr>
<tr>
<td>


in4_label

</td>
<td>


"AVDD 1V8"

</td>
</tr>
<tr>
<td>


curr5_input

</td>
<td>


Measured current for AVDD 1V8 (milliAmps)

</td>
</tr>
<tr>
<td>


curr5_label

</td>
<td>


"AVDD 1V8"

</td>
</tr>
<tr>
<td>


power5_average

</td>
<td>


Measured average power for AVDD 1V8 (microWatts)

</td>
</tr>
<tr>
<td>


power5_average_interval

</td>
<td>


Power averaging time input valid from 1 to 1708mS

</td>
</tr>
<tr>
<td>


power5_label

</td>
<td>


"AVDD 1V8"

</td>
</tr>
<tr>
<td>


curr6_input

</td>
<td>


Measured current for SYSVDD (milliAmps)

</td>
</tr>
<tr>
<td>


curr6_label

</td>
<td>


"SYSVDD"

</td>
</tr>
<tr>
<td>


power6_average

</td>
<td>


Measured average power for SYSVDD (microWatts)

</td>
</tr>
<tr>
<td>


power6_average_interval

</td>
<td>


Power averaging time input valid from 1 to 1708mS

</td>
</tr>
<tr>
<td>


power6_label

</td>
<td>


"SYSVDD"

</td>
</tr>
<tr>
<td>


in6_input

</td>
<td>


Measured voltage for VDDCORE CDC (milliVolts)

</td>
</tr>
<tr>
<td>


in6_label

</td>
<td>


"VDDCORE CDC"

</td>
</tr>
<tr>
<td>


curr7_input

</td>
<td>


Measured current for VDDCORE CDC (milliAmps)

</td>
</tr>
<tr>
<td>


curr7_label

</td>
<td>


"VDDCORE CDC"

</td>
</tr>
<tr>
<td>


power7_average

</td>
<td>


Measured average power for VDDCORE CDC (microWatts)

</td>
</tr>
<tr>
<td>


power7_average_interval

</td>
<td>


Power averaging time input valid from 1 to 1708mS

</td>
</tr>
<tr>
<td>


power7_label

</td>
<td>


"VDDCORE CDC"

</td>
</tr>
<tr>
<td>


in7_input

</td>
<td>


Measured voltage for MICVDD (milliVolts)

</td>
</tr>
<tr>
<td>


in7_label

</td>
<td>


"MICVDD"

</td>
</tr>
<tr>
<td>


curr8_input

</td>
<td>


Measured current for MICVDD (milliAmps)

</td>
</tr>
<tr>
<td>


curr8_label

</td>
<td>


"MICVDD"

</td>
</tr>
<tr>
<td>


power8_average

</td>
<td>


Measured average power for MICVDD (microWatts)

</td>
</tr>
<tr>
<td>


power8_average_interval

</td>
<td>


Power averaging time input valid from 1 to 1708mS

</td>
</tr>
<tr>
<td>


power8_label

</td>
<td>


"MICVDD"

</td>
</tr>
</tbody>
</table>

- **Note:**

  It is not possible to measure voltage on the SYSVDD rail.
