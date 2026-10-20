---
title: "Alienware WMI Driver"
type: reference
description: "Kurt Borja <kuurtb@gmail.com>"
---

<a id="rst-alienware-wmi-driver"></a>

<!-- SPDX-License-Identifier: GPL-2.0-or-later -->

Kurt Borja &lt;[kuurtb@gmail.com](<mailto:kuurtb@gmail.com>)&gt;

This is a driver for the "WMAX" WMI device, which is found in most Dell gaming laptops and controls various special features.

Before the launch of M-Series laptops (\~2018), the "WMAX" device controlled basic RGB lighting, deep sleep mode, HDMI mode and amplifier status.

Later, this device was completely repurpused. Now it mostly deals with thermal profiles, sensor monitoring and overclocking. This interface is named "AWCC" and is known to be used by the AWCC OEM application to control these features.

The alienware-wmi driver controls both interfaces.

<a id="rst-awcc-interface"></a>

## AWCC Interface

WMI device documentation: [Documentation/wmi/devices/alienware-wmi.rst](~kernel/hardware/wmi/devices/alienware-wmi)

<a id="rst-supported-devices"></a>

### Supported devices

- Alienware M-Series laptops

- Alienware X-Series laptops

- Alienware Aurora Desktops

- Dell G-Series laptops

If you believe your device supports the AWCC interface and you don't have any of the features described in this document, try the following alienware-wmi module parameters:

- `force_platform_profile=1`: Forces probing for platform profile support

- `force_hwmon=1`: Forces probing for HWMON support

If the module loads successfully with these parameters, consider submitting a patch adding your model to the `awcc_dmi_table` located in `drivers/platform/x86/dell/alienware-wmi-wmax.c` or contacting the maintainer for further guidance.

<a id="rst-status"></a>

### Status

The following features are currently supported:

- [Platform Profile](<#rst-platform-profile>):

  - Thermal profile control

  - G-Mode toggling

- [HWMON](<#rst-hwmon-1>):

  - Sensor monitoring

  - Manual fan control

<a id="rst-platform-profile-1"></a>
<a id="rst-platform-profile"></a>

### Platform Profile

The AWCC interface exposes various firmware defined thermal profiles. These are exposed to user-space through the Platform Profile class interface. Refer to [sysfs-class-platform-profile](<~kernel/administration/admin-guide/abi/abi-testing-files#abi-file-testing-sysfs-class-platform-profile>) for more information.

The name of the platform-profile class device exported by this driver is "alienware-wmi" and it's path can be found with:



```text
grep -l "alienware-wmi" /sys/class/platform-profile/platform-profile-*/name | sed 's|/[^/]*$||'
```

If the device supports G-Mode, it is also toggled when selecting the `performance` profile.

> [!NOTE]
>
> You may set the `force_gmode` module parameter to always try to toggle this feature, without checking if your model supports it.

<a id="rst-hwmon-1"></a>
<a id="rst-hwmon"></a>

### HWMON

The AWCC interface also supports sensor monitoring and manual fan control. Both of these features are exposed to user-space through the HWMON interface.

The name of the hwmon class device exported by this driver is "alienware\_wmi" and it's path can be found with:



```text
grep -l "alienware_wmi" /sys/class/hwmon/hwmon*/name | sed 's|/[^/]*$||'
```

Sensor monitoring is done through the standard HWMON interface. Refer to [sysfs-class-hwmon](<~kernel/administration/admin-guide/abi/abi-testing-files#abi-file-testing-sysfs-class-hwmon>) for more information.

Manual fan control on the other hand, is not exposed directly by the AWCC interface. Instead it let's us control a fan `boost` value. This `boost` value has the following approximate behavior over the fan pwm:



```text
pwm = pwm_base + (fan_boost / 255) * (pwm_max - pwm_base)
```

Due to the above behavior, the fan `boost` control is exposed to user-space through the following, custom hwmon sysfs attribute:


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



fan\[1-4\]\_boost

</td>
<td>



RW

</td>
<td>



Fan boost value.

Integer value between 0 and 255

</td>
</tr>
</tbody>
</table>

> [!NOTE]
>
> In some devices, manual fan control only works reliably if the `custom` platform profile is selected.
