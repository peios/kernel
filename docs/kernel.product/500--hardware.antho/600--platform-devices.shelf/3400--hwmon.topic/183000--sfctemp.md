---
title: "Kernel driver sfctemp"
type: reference
description: "StarFive JH7100"
---

<a id="rst-kernel-driver-sfctemp"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

- **Supported chips:**

  - StarFive JH7100

  - StarFive JH7110

- **Authors:**

  - Emil Renner Berthing &lt;[kernel@esmil.dk](<mailto:kernel@esmil.dk>)&gt;

<a id="rst-description"></a>

## Description

This driver adds support for reading the built-in temperature sensor on the JH7100 and JH7110 RISC-V SoCs by StarFive Technology Co. Ltd.

<a id="rst-sysfs-interface"></a>

## `sysfs` interface

The temperature sensor can be enabled, disabled and queried via the standard hwmon interface in sysfs under `/sys/class/hwmon/hwmonX` for some value of `X`:


<table>
<thead>
<tr>
<th>


Name

</th>
<th>


Perm

</th>
<th>


Description

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


temp1_enable

</td>
<td>


RW

</td>
<td>


Enable or disable temperature sensor. Automatically enabled by the driver, but may be disabled to save power.

</td>
</tr>
<tr>
<td>


temp1_input

</td>
<td>


RO

</td>
<td>


Temperature reading in milli-degrees Celsius.

</td>
</tr>
</tbody>
</table>
