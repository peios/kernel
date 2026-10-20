---
title: "Microchip SparX-5 SoC"
type: reference
description: "Supported chips:"
---

<a id="rst-microchip-sparx-5-soc"></a>

<!-- SPDX-License-Identifier: GPL-2.0-only -->

Supported chips:

> - VSC7546, VSC7549, VSC755, VSC7556, and VSC7558 (Sparx5 series)
>
>   Prefix: 'sparx5-temp'
>
>   Addresses scanned: -
>
>   Datasheet: Provided by Microchip upon request and under NDA

Author: Lars Povlsen &lt;[lars.povlsen@microchip.com](<mailto:lars.povlsen@microchip.com>)&gt;

<a id="rst-description"></a>

## Description

The Sparx5 SoC contains a temperature sensor based on the MR74060 Moortec IP.

The sensor has a range of -40°C to +125°C and an accuracy of +/-5°C.

<a id="rst-sysfs-entries"></a>

## Sysfs entries

The following attributes are supported.


<table>
<tbody>
<tr>
<td>


temp1_input

</td>
<td>


Die temperature (in millidegree Celsius.)

</td>
</tr>
</tbody>
</table>
