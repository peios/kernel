---
title: "Kernel driver twl4030-madc"
type: reference
description: "Supported chips:"
---

<a id="rst-kernel-driver-twl4030-madc"></a>

Supported chips:

> - Texas Instruments TWL4030
>
> Prefix: 'twl4030-madc'

- **Authors:**

  J Keerthy &lt;[j-keerthy@ti.com](<mailto:j-keerthy@ti.com>)&gt;

<a id="rst-description"></a>

## Description

The Texas Instruments TWL4030 is a Power Management and Audio Circuit. Among other things it contains a 10-bit A/D converter MADC. The converter has 16 channels which can be used in different modes.

See this table for the meaning of the different channels


<table>
<thead>
<tr>
<th>


Channel

</th>
<th>


Signal

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


0

</td>
<td>


Battery type(BTYPE)

</td>
</tr>
<tr>
<td>


1

</td>
<td>


BCI: Battery temperature (BTEMP)

</td>
</tr>
<tr>
<td>


2

</td>
<td>


GP analog input

</td>
</tr>
<tr>
<td>


3

</td>
<td>


GP analog input

</td>
</tr>
<tr>
<td>


4

</td>
<td>


GP analog input

</td>
</tr>
<tr>
<td>


5

</td>
<td>


GP analog input

</td>
</tr>
<tr>
<td>


6

</td>
<td>


GP analog input

</td>
</tr>
<tr>
<td>


7

</td>
<td>


GP analog input

</td>
</tr>
<tr>
<td>


8

</td>
<td>


BCI: VBUS voltage(VBUS)

</td>
</tr>
<tr>
<td>


9

</td>
<td>


Backup Battery voltage (VBKP)

</td>
</tr>
<tr>
<td>


10

</td>
<td>


BCI: Battery charger current (ICHG)

</td>
</tr>
<tr>
<td>


11

</td>
<td>


BCI: Battery charger voltage (VCHG)

</td>
</tr>
<tr>
<td>


12

</td>
<td>


BCI: Main battery voltage (VBAT)

</td>
</tr>
<tr>
<td>


13

</td>
<td>


Reserved

</td>
</tr>
<tr>
<td>


14

</td>
<td>


Reserved

</td>
</tr>
<tr>
<td>


15

</td>
<td>


VRUSB Supply/Speaker left/Speaker right polarization level

</td>
</tr>
</tbody>
</table>

The Sysfs nodes will represent the voltage in the units of mV, the temperature channel shows the converted temperature in degree Celsius. The Battery charging current channel represents battery charging current in mA.
