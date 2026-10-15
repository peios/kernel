---
title: "Linux HP WMI Sensors Driver"
type: reference
description: "Hewlett-Packard (and some HP Compaq) business-class computers report hardware monitoring information via Windows Management Instrumentation (WMI). This driver exposes that information to the Linux hwmon subsystem, allowing userspace…"
---

<a id="rst-linux-hp-wmi-sensors-driver"></a>

<!-- SPDX-License-Identifier: GPL-2.0-or-later -->

<!-- This data file has been placed in the public domain. -->

<!-- Derived from the Unicode character mappings available from
<http://www.w3.org/2003/entities/xml/>.
Processed by unicode2rstsubs.py, part of Docutils:
<https://docutils.sourceforge.io>. -->

**Copyright:** © 2023 James Seo &lt;[james@equiv.tech](<mailto:james@equiv.tech>)&gt;

<a id="rst-description"></a>

## Description

Hewlett-Packard (and some HP Compaq) business-class computers report hardware monitoring information via Windows Management Instrumentation (WMI). This driver exposes that information to the Linux hwmon subsystem, allowing userspace utilities like `sensors` to gather numeric sensor readings.

<a id="rst-sysfs-interface"></a>

## sysfs interface

When the driver is loaded, it discovers the sensors available on the system and creates the following sysfs attributes as necessary within `/sys/class/hwmon/hwmon[X]`:

(`[X]` is some number that depends on other system components.)


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


`curr[X]_input`

</td>
<td>


RO

</td>
<td>


Current in milliamperes (mA).

</td>
</tr>
<tr>
<td>


`curr[X]_label`

</td>
<td>


RO

</td>
<td>


Current sensor label.

</td>
</tr>
<tr>
<td>


`fan[X]_input`

</td>
<td>


RO

</td>
<td>


Fan speed in RPM.

</td>
</tr>
<tr>
<td>


`fan[X]_label`

</td>
<td>


RO

</td>
<td>


Fan sensor label.

</td>
</tr>
<tr>
<td>


`fan[X]_fault`

</td>
<td>


RO

</td>
<td>


Fan sensor fault indicator.

</td>
</tr>
<tr>
<td>


`fan[X]_alarm`

</td>
<td>


RO

</td>
<td>


Fan sensor alarm indicator.

</td>
</tr>
<tr>
<td>


`in[X]_input`

</td>
<td>


RO

</td>
<td>


Voltage in millivolts (mV).

</td>
</tr>
<tr>
<td>


`in[X]_label`

</td>
<td>


RO

</td>
<td>


Voltage sensor label.

</td>
</tr>
<tr>
<td>


`temp[X]_input`

</td>
<td>


RO

</td>
<td>


Temperature in millidegrees Celsius (m°C).

</td>
</tr>
<tr>
<td>


`temp[X]_label`

</td>
<td>


RO

</td>
<td>


Temperature sensor label.

</td>
</tr>
<tr>
<td>


`temp[X]_fault`

</td>
<td>


RO

</td>
<td>


Temperature sensor fault indicator.

</td>
</tr>
<tr>
<td>


`temp[X]_alarm`

</td>
<td>


RO

</td>
<td>


Temperature sensor alarm indicator.

</td>
</tr>
<tr>
<td>


`intrusion[X]_alarm`

</td>
<td>


RW

</td>
<td>


Chassis intrusion alarm indicator.

</td>
</tr>
</tbody>
</table>

- **`fault` attributes**

  Reading `1` instead of `0` as the `fault` attribute for a sensor indicates that it has encountered some issue during operation such that measurements from it should not be trusted. If a sensor with the fault condition recovers later, reading this attribute will return `0` again.

- **`alarm` attributes**

  Reading `1` instead of `0` as the `alarm` attribute for a sensor indicates that one of the following has occurred, depending on its type:

  - `fan`: The fan has stalled or has been disconnected while running.

  - `temp`: The sensor reading has reached a critical threshold. The exact threshold is system-dependent.

  - `intrusion`: The system's chassis has been opened.

  After `1` is read from an `alarm` attribute, the attribute resets itself and returns `0` on subsequent reads. As an exception, an `intrusion[X]_alarm` can only be manually reset by writing `0` to it.

<a id="rst-debugfs-interface"></a>

## debugfs interface

> [!WARNING]
>
> The debugfs interface is subject to change without notice and is only available when the kernel is compiled with `CONFIG_DEBUG_FS` defined.

The standard hwmon interface in sysfs exposes sensors of several common types that are connected as of driver initialization. However, there are usually other sensors in WMI that do not meet these criteria. In addition, a number of system-dependent "platform events objects" used for `alarm` attributes may be present. A debugfs interface is therefore provided for read-only access to all available HP WMI sensors and platform events objects.

`/sys/kernel/debug/hp-wmi-sensors-[X]/sensor` contains one numbered entry per sensor with the following attributes:


<table>
<thead>
<tr>
<th>


Name

</th>
<th>


Example

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


`name`

</td>
<td>


`CPU0 Fan`

</td>
</tr>
<tr>
<td>


`description`

</td>
<td>


`Reports CPU0 fan speed`

</td>
</tr>
<tr>
<td>


`sensor_type`

</td>
<td>


`12`

</td>
</tr>
<tr>
<td>


`other_sensor_type`

</td>
<td>


(an empty string)

</td>
</tr>
<tr>
<td>


`operational_status`

</td>
<td>


`2`

</td>
</tr>
<tr>
<td>


`possible_states`

</td>
<td>


`Normal,Caution,Critical,Not Present`

</td>
</tr>
<tr>
<td>


`current_state`

</td>
<td>


`Normal`

</td>
</tr>
<tr>
<td>


`base_units`

</td>
<td>


`19`

</td>
</tr>
<tr>
<td>


`unit_modifier`

</td>
<td>


`0`

</td>
</tr>
<tr>
<td>


`current_reading`

</td>
<td>


`1008`

</td>
</tr>
<tr>
<td>


`rate_units`

</td>
<td>


`0` (only exists on some systems)

</td>
</tr>
</tbody>
</table>

If platform events objects are available, `/sys/kernel/debug/hp-wmi-sensors-[X]/platform_events` contains one numbered entry per object with the following attributes:


<table>
<thead>
<tr>
<th>


Name

</th>
<th>


Example

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


`name`

</td>
<td>


`CPU0 Fan Stall`

</td>
</tr>
<tr>
<td>


`description`

</td>
<td>


`CPU0 Fan Speed`

</td>
</tr>
<tr>
<td>


`source_namespace`

</td>
<td>


`root\wmi`

</td>
</tr>
<tr>
<td>


`source_class`

</td>
<td>


`HPBIOS_BIOSEvent`

</td>
</tr>
<tr>
<td>


`category`

</td>
<td>


`3`

</td>
</tr>
<tr>
<td>


`possible_severity`

</td>
<td>


`25`

</td>
</tr>
<tr>
<td>


`possible_status`

</td>
<td>


`5`

</td>
</tr>
</tbody>
</table>

These represent the properties of the underlying `HPBIOS_BIOSNumericSensor` and `HPBIOS_PlatformEvents` WMI objects, which vary between systems. See <a id="rst-footnote-reference-1"></a>[1](#rst-footnote-1) for more details and Managed Object Format (MOF) definitions.

<a id="rst-known-issues-and-limitations"></a>

## Known issues and limitations

- If the existing hp-wmi driver for non-business-class HP systems is already loaded, `alarm` attributes will be unavailable even on systems that support them. This is because the same WMI event GUID used by this driver for `alarm` attributes is used on those systems for e.g. laptop hotkeys.

- Dubious sensor hardware and inconsistent BIOS WMI implementations have been observed to cause inaccurate readings and peculiar behavior, such as alarms failing to occur or occurring only once per boot.

- Only temperature, fan speed, and intrusion sensor types have been seen in the wild so far. Support for voltage and current sensors is therefore provisional.

- Although HP WMI sensors may claim to be of any type, any oddball sensor types unknown to hwmon will not be supported.

<a id="rst-references"></a>

## References

<a id="rst-footnote-1"></a>



**[1]** Hewlett-Packard Development Company, L.P., "HP Client Management Interface Technical White Paper", 2005. \[Online\]. Available: [https://h20331.www2.hp.com/hpsub/downloads/cmi_whitepaper.pdf](<https://h20331.www2.hp.com/hpsub/downloads/cmi_whitepaper.pdf>)
