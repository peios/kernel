---
title: "Kernel driver: x86_pkg_temp_thermal"
type: reference
description: "Supported chips:"
---

<a id="rst-kernel-driver-x86-pkg-temp-thermal"></a>

Supported chips:

- x86: with package level thermal management

(Verify using: CPUID.06H:EAX\[bit 6\] =1)

Authors: Srinivas Pandruvada &lt;[srinivas.pandruvada@linux.intel.com](<mailto:srinivas.pandruvada@linux.intel.com>)&gt;

<a id="rst-reference"></a>

## Reference

Intel® 64 and IA-32 Architectures Software Developer’s Manual (Jan, 2013): Chapter 14.6: PACKAGE LEVEL THERMAL MANAGEMENT

<a id="rst-description"></a>

## Description

This driver register CPU digital temperature package level sensor as a thermal zone with maximum two user mode configurable trip points. Number of trip points depends on the capability of the package. Once the trip point is violated, user mode can receive notification via thermal notification mechanism and can take any action to control temperature.

<a id="rst-threshold-management"></a>

## Threshold management

Each package will register as a thermal zone under /sys/class/thermal.

Example:



```text
/sys/class/thermal/thermal_zone1
```

This contains two trip points:

- trip_point_0_temp

- trip_point_1_temp

User can set any temperature between 0 to TJ-Max temperature. Temperature units are in milli-degree Celsius. Refer to "[Documentation/driver-api/thermal/sysfs-api.rst](~kernel/hardware/driver-api/thermal/sysfs-api)" for thermal sys-fs details.

Any value other than 0 in these trip points, can trigger thermal notifications. Setting 0, stops sending thermal notifications.

Thermal notifications: To get kobject-uevent notifications, set the thermal zone policy to "user_space".

For example:



```text
echo -n "user_space" > policy
```
