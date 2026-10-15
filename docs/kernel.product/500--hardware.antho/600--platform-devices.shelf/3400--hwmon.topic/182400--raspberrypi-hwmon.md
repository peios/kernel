---
title: "Kernel driver raspberrypi-hwmon"
type: reference
description: "Supported boards:"
---

<a id="rst-kernel-driver-raspberrypi-hwmon"></a>

Supported boards:

> - Raspberry Pi A+ (via GPIO on SoC)
>
> - Raspberry Pi B+ (via GPIO on SoC)
>
> - Raspberry Pi 2 B (via GPIO on SoC)
>
> - Raspberry Pi 3 B (via GPIO on port expander)
>
> - Raspberry Pi 3 B+ (via PMIC)

Author: Stefan Wahren &lt;[stefan.wahren@i2se.com](<mailto:stefan.wahren@i2se.com>)&gt;

<a id="rst-description"></a>

## Description

This driver periodically polls a mailbox property of the VC4 firmware to detect undervoltage conditions.

<a id="rst-sysfs-entries"></a>

## Sysfs entries


<table>
<tbody>
<tr>
<td>


in0_lcrit_alarm

</td>
<td>


Undervoltage alarm

</td>
</tr>
</tbody>
</table>
