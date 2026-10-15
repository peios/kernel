---
title: "Kernel driver dell-smm-hwmon"
type: reference
description: "On many Dell laptops the System Management Mode (SMM) BIOS can be queried for the status of fans and temperature sensors. Userspace utilities like sensors can be used to return the readings. The userspace suite i8kutils can also be used to…"
---

<a id="rst-kernel-driver-dell-smm-hwmon"></a>

<!-- SPDX-License-Identifier: GPL-2.0-or-later -->

<!-- This data file has been placed in the public domain. -->

<!-- Derived from the Unicode character mappings available from
<http://www.w3.org/2003/entities/xml/>.
Processed by unicode2rstsubs.py, part of Docutils:
<https://docutils.sourceforge.io>. -->

**Copyright:** © 2002-2005 Massimo Dal Zotto &lt;[dz@debian.org](<mailto:dz@debian.org>)&gt;

**Copyright:** © 2019 Giovanni Mascellani &lt;[gio@debian.org](<mailto:gio@debian.org>)&gt;

<a id="rst-description"></a>

## Description

On many Dell laptops the System Management Mode (SMM) BIOS can be queried for the status of fans and temperature sensors.  Userspace utilities like `sensors` can be used to return the readings. The userspace suite [i8kutils](<https://github.com/vitorafsr/i8kutils>) can also be used to read the sensors and automatically adjust fan speed (please notice that it currently uses the deprecated `/proc/i8k` interface).

> <a id="rst-target-1"></a>
>

<a id="rst-sysfs-interface"></a>

## `sysfs` interface

Temperature sensors and fans can be queried and set via the standard `hwmon` interface on `sysfs`, under the directory `/sys/class/hwmon/hwmonX` for some value of `X` (search for the `X` such that `/sys/class/hwmon/hwmonX/name` has content `dell_smm`). A number of other attributes can be read or written:


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


fan\[1-4\]\_input

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


fan\[1-4\]\_label

</td>
<td>


RO

</td>
<td>


Fan label.

</td>
</tr>
<tr>
<td>


fan\[1-4\]\_min

</td>
<td>


RO

</td>
<td>


Minimal Fan speed in RPM

</td>
</tr>
<tr>
<td>


fan\[1-4\]\_max

</td>
<td>


RO

</td>
<td>


Maximal Fan speed in RPM

</td>
</tr>
<tr>
<td>


fan\[1-4\]\_target

</td>
<td>


RO

</td>
<td>


Expected Fan speed in RPM

</td>
</tr>
<tr>
<td>


pwm\[1-4\]

</td>
<td>


RW

</td>
<td>


Control the fan PWM duty-cycle.

</td>
</tr>
<tr>
<td>


pwm\[1-4\]\_enable

</td>
<td>


RW/WO

</td>
<td>


Enable or disable automatic BIOS fan control (not supported on all laptops, see below for details).

</td>
</tr>
<tr>
<td>


temp\[1-10\]\_input

</td>
<td>


RO

</td>
<td>


Temperature reading in milli-degrees Celsius.

</td>
</tr>
<tr>
<td>


temp\[1-10\]\_label

</td>
<td>


RO

</td>
<td>


Temperature sensor label.

</td>
</tr>
</tbody>
</table>

Due to the nature of the SMM interface, each pwmX attribute controls fan number X.

<a id="rst-enabling-disabling-automatic-bios-fan-control"></a>

## Enabling/Disabling automatic BIOS fan control

There exist two methods for enabling/disabling automatic BIOS fan control:

1. Separate SMM commands to enable/disable automatic BIOS fan control for all fans.

2. A special fan state that enables automatic BIOS fan control for a individual fan.

The driver cannot reliably detect what method should be used on a given device, so instead the following heuristic is used:

- use fan state 3 for enabling BIOS fan control if the maximum fan state setable by the user is smaller than 3 (default setting).

- use separate SMM commands if device is whitelisted to support them.

When using the first method, each fan will have a standard `pwmX_enable` sysfs attribute. Writing `1` into this attribute will disable automatic BIOS fan control for the associated fan and set it to maximum speed. Enabling BIOS fan control again can be achieved by writing `2` into this attribute. Reading this sysfs attributes returns the current setting as reported by the underlying hardware.

When using the second method however, only the `pwm1_enable` sysfs attribute will be available to enable/disable automatic BIOS fan control globaly for all fans available on a given device. Additionally, this sysfs attribute is write-only as there exists no SMM command for reading the current fan control setting.

If no `pwmX_enable` attributes are available, then it means that the driver cannot use the first method and the SMM codes for enabling and disabling automatic BIOS fan control are not whitelisted for your device. It is possible that codes that work for other laptops actually work for yours as well, or that you have to discover new codes.

Check the list `i8k_whitelist_fan_control` in file `drivers/hwmon/dell-smm-hwmon.c` in the kernel tree: as a first attempt you can try to add your machine and use an already-known code pair. If, after recompiling the kernel, you see that `pwm1_enable` is present and works (i.e., you can manually control the fan speed), then please submit your finding as a kernel patch, so that other users can benefit from it. Please see [Documentation/process/submitting-patches.rst](<~kernel/development/process/submitting-patches#rst-submittingpatches>) for information on submitting patches.

If no known code works on your machine, you need to resort to do some probing, because unfortunately Dell does not publish datasheets for its SMM. You can experiment with the code in [this repository](<https://github.com/clopez/dellfan/>) to probe the BIOS on your machine and discover the appropriate codes.

> <a id="rst-target-2"></a>
>

Again, when you find new codes, we'd be happy to have your patches\!

<a id="rst-thermal-interface"></a>

## `thermal` interface

The driver also exports the fans as thermal cooling devices with `type` set to `dell-smm-fan[1-4]`. This allows for easy fan control using one of the thermal governors.

<a id="rst-module-parameters"></a>

## Module parameters

- - **force:bool**

    Force loading without checking for supported models. (default: 0)

- - **ignore_dmi:bool**

    Continue probing hardware even if DMI data does not match. (default: 0)

- - **restricted:bool**

    Allow fan control only to processes with the `CAP_SYS_ADMIN` capability set or processes run as root when using the legacy `/proc/i8k` interface. In this case normal users will be able to read temperature and fan status but not to control the fan.  If your notebook is shared with other users and you don't trust them you may want to use this option. (default: 1, only available with `CONFIG_I8K`)

- - **power_status:bool**

    Report AC status in `/proc/i8k`. (default: 0, only available with `CONFIG_I8K`)

- - **fan_mult:uint**

    Factor to multiply fan speed with. (default: autodetect)

- - **fan_max:uint**

    Maximum configurable fan speed. (default: autodetect)

<a id="rst-legacy-proc-interface"></a>

## Legacy `/proc` interface

> [!WARNING]
>
> This interface is obsolete and deprecated and should not used in new applications. This interface is only available when kernel is compiled with option `CONFIG_I8K`.

The information provided by the kernel driver can be accessed by simply reading the `/proc/i8k` file. For example:



```text
$ cat /proc/i8k
1.0 A17 2J59L02 52 2 1 8040 6420 1 2
```

The fields read from `/proc/i8k` are:



```text
1.0 A17 2J59L02 52 2 1 8040 6420 1 2
|   |   |       |  | | |    |    | |
|   |   |       |  | | |    |    | +------- 10. buttons status
|   |   |       |  | | |    |    +--------- 9.  AC status
|   |   |       |  | | |    +-------------- 8.  fan0 RPM
|   |   |       |  | | +------------------- 7.  fan1 RPM
|   |   |       |  | +--------------------- 6.  fan0 status
|   |   |       |  +----------------------- 5.  fan1 status
|   |   |       +-------------------------- 4.  temp0 reading (Celsius)
|   |   +---------------------------------- 3.  Dell service tag (later known as 'serial number')
|   +-------------------------------------- 2.  BIOS version
+------------------------------------------ 1.  /proc/i8k format version
```

A negative value, for example -22, indicates that the BIOS doesn't return the corresponding information. This is normal on some models/BIOSes.

For performance reasons the `/proc/i8k` doesn't report by default the AC status since this SMM call takes a long time to execute and is not really needed.  If you want to see the ac status in `/proc/i8k` you must explictitly enable this option by passing the `power_status=1` parameter to insmod. If AC status is not available -1 is printed instead.

The driver provides also an ioctl interface which can be used to obtain the same information and to control the fan status. The ioctl interface can be accessed from C programs or from shell using the i8kctl utility. See the source file of `i8kutils` for more information on how to use the ioctl interface.

<a id="rst-smm-interface"></a>

## SMM Interface

> [!WARNING]
>
> The SMM interface was reverse-engineered by trial-and-error since Dell did not provide any Documentation, please keep that in mind.

The driver uses the SMM interface to send commands to the system BIOS. This interface is normally used by Dell's 32-bit diagnostic program or on newer notebook models by the buildin BIOS diagnostics. The SMM may cause short hangs when the BIOS code is taking too long to execute.

The SMM handler inside the system BIOS looks at the contents of the `eax`, `ebx`, `ecx`, `edx`, `esi` and `edi` registers. Each register has a special purpose:


<table>
<thead>
<tr>
<th>


Register

</th>
<th>


Purpose

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


eax

</td>
<td>


Holds the command code before SMM, holds the first result after SMM.

</td>
</tr>
<tr>
<td>


ebx

</td>
<td>


Holds the arguments.

</td>
</tr>
<tr>
<td>


ecx

</td>
<td>


Unknown, set to 0.

</td>
</tr>
<tr>
<td>


edx

</td>
<td>


Holds the second result after SMM.

</td>
</tr>
<tr>
<td>


esi

</td>
<td>


Unknown, set to 0.

</td>
</tr>
<tr>
<td>


edi

</td>
<td>


Unknown, set to 0.

</td>
</tr>
</tbody>
</table>

The SMM handler can signal a failure by either:

- setting the lower sixteen bits of `eax` to `0xffff`

- not modifying `eax` at all

- setting the carry flag (legacy SMM interface only)

<a id="rst-legacy-smm-interface"></a>

## Legacy SMM Interface

When using the legacy SMM interface, a SMM is triggered by writing the least significant byte of the command code to the special ioports `0xb2` and `0x84`. This interface is not described inside the ACPI tables and can thus only be detected by issuing a test SMM call.

<a id="rst-wmi-smm-interface"></a>

## WMI SMM Interface

On modern Dell machines, the SMM calls are done over ACPI WMI:



```text
#pragma namespace("\\\\.\\root\\dcim\\sysman\\diagnostics")
[WMI, Provider("Provider_DiagnosticsServices"), Dynamic, Locale("MS\\0x409"),
 Description("RunDellDiag"), guid("{F1DDEE52-063C-4784-A11E-8A06684B9B01}")]
class LegacyDiags {
 [key, read] string InstanceName;
 [read] boolean Active;

 [WmiMethodId(1), Implemented, read, write, Description("Legacy Method ")]
 void Execute([in, out] uint32 EaxLen, [in, out, WmiSizeIs("EaxLen") : ToInstance] uint8 EaxVal[],
              [in, out] uint32 EbxLen, [in, out, WmiSizeIs("EbxLen") : ToInstance] uint8 EbxVal[],
              [in, out] uint32 EcxLen, [in, out, WmiSizeIs("EcxLen") : ToInstance] uint8 EcxVal[],
              [in, out] uint32 EdxLen, [in, out, WmiSizeIs("EdxLen") : ToInstance] uint8 EdxVal[]);
};
```

Some machines support only the WMI SMM interface, while some machines support both interfaces. The driver automatically detects which interfaces are present and will use the WMI SMM interface if the legacy SMM interface is not present. The WMI SMM interface is usually slower than the legacy SMM interface since ACPI methods need to be called in order to trigger a SMM.

<a id="rst-smm-command-codes"></a>

## SMM command codes


<table>
<thead>
<tr>
<th>


Command Code

</th>
<th>


Command Name

</th>
<th>


Description

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


`0x0025`

</td>
<td>


Get Fn key status

</td>
<td>


Returns the Fn key pressed after SMM:

- 9th bit in `eax` indicates Volume up

- 10th bit in `eax` indicates Volume down

- both bits indicate Volume mute

</td>
</tr>
<tr>
<td>


`0xa069`

</td>
<td>


Get power status

</td>
<td>


Returns current power status after SMM:

- 1st bit in `eax` indicates Battery connected

- 3th bit in `eax` indicates AC connected

</td>
</tr>
<tr>
<td>


`0x00a3`

</td>
<td>


Get fan state

</td>
<td>


Returns current fan state after SMM:

- 1st byte in `eax` holds the current fan state (0 - 2 or 3)

</td>
</tr>
<tr>
<td>


`0x01a3`

</td>
<td>


Set fan state

</td>
<td>


Sets the fan speed:

- 1st byte in `ebx` holds the fan number

- 2nd byte in `ebx` holds the desired fan state (0 - 2 or 3)

</td>
</tr>
<tr>
<td>


`0x02a3`

</td>
<td>


Get fan speed

</td>
<td>


Returns the current fan speed in RPM:

- 1st byte in `ebx` holds the fan number

- 1st word in `eax` holds the current fan speed in RPM (after SMM)

</td>
</tr>
<tr>
<td>


`0x03a3`

</td>
<td>


Get fan type

</td>
<td>


Returns the fan type:

- 1st byte in `ebx` holds the fan number

- 1st byte in `eax` holds the fan type (after SMM):

  - 5th bit indicates docking fan

  - 1 indicates Processor fan

  - 2 indicates Motherboard fan

  - 3 indicates Video fan

  - 4 indicates Power supply fan

  - 5 indicates Chipset fan

  - 6 indicates other fan type

</td>
</tr>
<tr>
<td>


`0x04a3`

</td>
<td>


Get nominal fan speed

</td>
<td>


Returns the nominal RPM in each fan state:

- 1st byte in `ebx` holds the fan number

- 2nd byte in `ebx` holds the fan state in question (0 - 2 or 3)

- 1st word in `eax` holds the nominal fan speed in RPM (after SMM)

</td>
</tr>
<tr>
<td>


`0x05a3`

</td>
<td>


Get fan speed tolerance

</td>
<td>


Returns the speed tolerance for each fan state:

- 1st byte in `ebx` holds the fan number

- 2nd byte in `ebx` holds the fan state in question (0 - 2 or 3)

- 1st byte in `eax` returns the speed tolerance

</td>
</tr>
<tr>
<td>


`0x10a3`

</td>
<td>


Get sensor temperature

</td>
<td>


Returns the measured temperature:

- 1st byte in `ebx` holds the sensor number

- 1st byte in `eax` holds the measured temperature (after SMM)

</td>
</tr>
<tr>
<td>


`0x11a3`

</td>
<td>


Get sensor type

</td>
<td>


Returns the sensor type:

- 1st byte in `ebx` holds the sensor number

- 1st byte in `eax` holds the temperature type (after SMM):

  - 1 indicates CPU sensor

  - 2 indicates GPU sensor

  - 3 indicates SODIMM sensor

  - 4 indicates other sensor type

  - 5 indicates Ambient sensor

  - 6 indicates other sensor type

</td>
</tr>
<tr>
<td>


`0xfea3`

</td>
<td>


Get SMM signature

</td>
<td>


Returns Dell signature if interface is supported (after SMM):

- `eax` holds 1145651527 (0x44494147 or "DIAG")

- `edx` holds 1145392204 (0x44454c4c or "DELL")

</td>
</tr>
<tr>
<td>


`0xffa3`

</td>
<td>


Get SMM signature

</td>
<td>


Same as `0xfea3`, check both.

</td>
</tr>
</tbody>
</table>

There are additional commands for enabling (`0x31a3` or `0x35a3`) and disabling (`0x30a3` or `0x34a3`) automatic fan speed control. The commands are however causing severe sideeffects on many machines, so they are not used by default.

On several machines (Inspiron 3505, Precision 490, Vostro 1720, ...), the fans supports a 4th "magic" state, which signals the BIOS that automatic fan control should be enabled for a specific fan. However there are also some machines who do support a 4th regular fan state too, but in case of the "magic" state, the nominal RPM reported for this state is a placeholder value, which however is not always detectable.

<a id="rst-firmware-bugs"></a>

## Firmware Bugs

The SMM calls can behave erratic on some machines:


<table>
<thead>
<tr>
<th>


Firmware Bug

</th>
<th>


Affected Machines

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


Reading of fan states return spurious errors.

</td>
<td>


Precision 490

OptiPlex 7060

</td>
</tr>
<tr>
<td>


Reading of fan types causes erratic fan behaviour.

</td>
<td>


Studio XPS 8000

Studio XPS 8100

Inspiron 580

Inspiron 3505

</td>
</tr>
<tr>
<td>


Fan-related SMM calls take too long (about 500ms).

</td>
<td>


Inspiron 7720

Vostro 3360

XPS 13 9333

XPS 15 L502X

</td>
</tr>
</tbody>
</table>

In case you experience similar issues on your Dell machine, please submit a bugreport on bugzilla to we can apply workarounds.

<a id="rst-limitations"></a>

## Limitations

The SMM calls can take too long to execute on some machines, causing short hangs and/or audio glitches. Also the fan state needs to be restored after suspend, as well as the automatic mode settings. When reading a temperature sensor, values above 127 degrees indicate a BIOS read error or a deactivated sensor.
