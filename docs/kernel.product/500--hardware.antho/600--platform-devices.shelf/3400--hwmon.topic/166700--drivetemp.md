---
title: "Kernel driver drivetemp"
type: reference
description: "ANS T13/1699-D Information technology - AT Attachment 8 - ATA/ATAPI Command Set (ATA8-ACS)"
---

<a id="rst-kernel-driver-drivetemp"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-references"></a>

## References

ANS T13/1699-D Information technology - AT Attachment 8 - ATA/ATAPI Command Set (ATA8-ACS)

ANS Project T10/BSR INCITS 513 Information technology - SCSI Primary Commands - 4 (SPC-4)

ANS Project INCITS 557 Information technology - SCSI / ATA Translation - 5 (SAT-5)

<a id="rst-description"></a>

## Description

This driver supports reporting the temperature of disk and solid state drives with temperature sensors.

If supported, it uses the ATA SCT Command Transport feature to read the current drive temperature and, if available, temperature limits as well as historic minimum and maximum temperatures. If SCT Command Transport is not supported, the driver uses SMART attributes to read the drive temperature.

<a id="rst-usage-note"></a>

## Usage Note

Reading the drive temperature may reset the spin down timer on some drives. This has been observed with WD120EFAX drives, but may be seen with other drives as well. The same behavior is observed if the 'hdtemp' or 'smartd' tools are used to access the drive. With the WD120EFAX drive, reading the drive temperature using the drivetemp driver is still possible \_after\_ it transitioned to standby mode, and reading the drive temperature in this mode will not cause the drive to change its mode (meaning the drive will not spin up). It is unknown if other drives experience similar behavior.

A known workaround for WD120EFAX drives is to read the drive temperature at intervals larger than twice the spin-down time. Otherwise affected drives will never spin down.

<a id="rst-sysfs-entries"></a>

## Sysfs entries

Only the temp1_input attribute is always available. Other attributes are available only if reported by the drive. All temperatures are reported in milli-degrees Celsius.


<table>
<tbody>
<tr>
<td>


temp1_input

</td>
<td>


Current drive temperature

</td>
</tr>
<tr>
<td>


temp1_lcrit

</td>
<td>


Minimum temperature limit. Operating the device below this temperature may cause physical damage to the device.

</td>
</tr>
<tr>
<td>


temp1_min

</td>
<td>


Minimum recommended continuous operating limit

</td>
</tr>
<tr>
<td>


temp1_max

</td>
<td>


Maximum recommended continuous operating temperature

</td>
</tr>
<tr>
<td>


temp1_crit

</td>
<td>


Maximum temperature limit. Operating the device above this temperature may cause physical damage to the device.

</td>
</tr>
<tr>
<td>


temp1_lowest

</td>
<td>


Minimum temperature seen this power cycle

</td>
</tr>
<tr>
<td>


temp1_highest

</td>
<td>


Maximum temperature seen this power cycle

</td>
</tr>
</tbody>
</table>
