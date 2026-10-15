---
title: "Kernel driver peci-cputemp"
type: reference
description: "Intel Xeon E5-14xx v3 family Intel Xeon E5-24xx v3 family Intel Xeon E5-16xx v3 family Intel Xeon E5-26xx v3 family Intel Xeon E5-46xx v3 family Intel Xeon E7-48xx v3 family Intel Xeon E7-88xx v3 family"
---

<a id="rst-kernel-driver-peci-cputemp"></a>

<!-- SPDX-License-Identifier: GPL-2.0-only -->

- **Supported chips:**

  - **One of Intel server CPUs listed below which is connected to a PECI bus.**

    - - **Intel Xeon E5/E7 v3 server processors**

        Intel Xeon E5-14xx v3 family Intel Xeon E5-24xx v3 family Intel Xeon E5-16xx v3 family Intel Xeon E5-26xx v3 family Intel Xeon E5-46xx v3 family Intel Xeon E7-48xx v3 family Intel Xeon E7-88xx v3 family

    - - **Intel Xeon E5/E7 v4 server processors**

        Intel Xeon E5-16xx v4 family Intel Xeon E5-26xx v4 family Intel Xeon E5-46xx v4 family Intel Xeon E7-48xx v4 family Intel Xeon E7-88xx v4 family

    - - **Intel Xeon Scalable server processors**

        Intel Xeon D family Intel Xeon Bronze family Intel Xeon Silver family Intel Xeon Gold family Intel Xeon Platinum family

  Datasheet: Available from [http://www.intel.com/design/literature.htm](<http://www.intel.com/design/literature.htm>)

Author: Jae Hyun Yoo &lt;[jae.hyun.yoo@linux.intel.com](<mailto:jae.hyun.yoo@linux.intel.com>)&gt;

<a id="rst-description"></a>

## Description

This driver implements a generic PECI hwmon feature which provides Digital Thermal Sensor (DTS) thermal readings of the CPU package and CPU cores that are accessible via the processor PECI interface.

All temperature values are given in millidegree Celsius and will be measurable only when the target CPU is powered on.

<a id="rst-sysfs-interface"></a>

## Sysfs interface


<table>
<tbody>
<tr>
<td>


temp1_label

</td>
<td>


"Die"

</td>
</tr>
<tr>
<td>


temp1_input

</td>
<td>


Provides current die temperature of the CPU package.

</td>
</tr>
<tr>
<td>


temp1_max

</td>
<td>


Provides thermal control temperature of the CPU package which is also known as Tcontrol.

</td>
</tr>
<tr>
<td>


temp1_crit

</td>
<td>


Provides shutdown temperature of the CPU package which is also known as the maximum processor junction temperature, Tjmax or Tprochot.

</td>
</tr>
<tr>
<td>


temp1_crit_hyst

</td>
<td>


Provides the hysteresis temperature of the CPU package. Returns Tcontrol, the temperature at which the critical condition clears.

</td>
</tr>
<tr>
<td>


temp2_label

</td>
<td>


"DTS"

</td>
</tr>
<tr>
<td>


temp2_input

</td>
<td>


Provides current temperature of the CPU package scaled to match DTS thermal profile.

</td>
</tr>
<tr>
<td>


temp2_max

</td>
<td>


Provides thermal control temperature of the CPU package which is also known as Tcontrol.

</td>
</tr>
<tr>
<td>


temp2_crit

</td>
<td>


Provides shutdown temperature of the CPU package which is also known as the maximum processor junction temperature, Tjmax or Tprochot.

</td>
</tr>
<tr>
<td>


temp2_crit_hyst

</td>
<td>


Provides the hysteresis temperature of the CPU package. Returns Tcontrol, the temperature at which the critical condition clears.

</td>
</tr>
<tr>
<td>


temp3_label

</td>
<td>


"Tcontrol"

</td>
</tr>
<tr>
<td>


temp3_input

</td>
<td>


Provides current Tcontrol temperature of the CPU package which is also known as Fan Temperature target. Indicates the relative value from thermal monitor trip temperature at which fans should be engaged.

</td>
</tr>
<tr>
<td>


temp3_crit

</td>
<td>


Provides Tcontrol critical value of the CPU package which is same to Tjmax.

</td>
</tr>
<tr>
<td>


temp4_label

</td>
<td>


"Tthrottle"

</td>
</tr>
<tr>
<td>


temp4_input

</td>
<td>


Provides current Tthrottle temperature of the CPU package. Used for throttling temperature. If this value is allowed and lower than Tjmax - the throttle will occur and reported at lower than Tjmax.

</td>
</tr>
<tr>
<td>


temp5_label

</td>
<td>


"Tjmax"

</td>
</tr>
<tr>
<td>


temp5_input

</td>
<td>


Provides the maximum junction temperature, Tjmax of the CPU package.

</td>
</tr>
<tr>
<td>


temp\[6-N\]\_label

</td>
<td>


Provides string "Core X", where X is resolved core number.

</td>
</tr>
<tr>
<td>


temp\[6-N\]\_input

</td>
<td>


Provides current temperature of each core.

</td>
</tr>
</tbody>
</table>
