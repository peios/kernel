---
title: "Dell AWCC WMI interface driver (alienware-wmi)"
type: reference
description: "The WMI device WMAX has been implemented for many Alienware and Dell's G-Series models. Throughout these models, two implementations have been identified. The first one, used by older systems, deals with HDMI, brightness, RGB, amplifier…"
---

<a id="rst-dell-awcc-wmi-interface-driver-alienware-wmi"></a>

<!-- SPDX-License-Identifier: GPL-2.0-or-later -->

<a id="rst-introduction"></a>

## Introduction

The WMI device WMAX has been implemented for many Alienware and Dell's G-Series models. Throughout these models, two implementations have been identified. The first one, used by older systems, deals with HDMI, brightness, RGB, amplifier and deep sleep control. The second one used by newer systems deals primarily with thermal control and overclocking.

It is suspected that the latter is used by Alienware Command Center (AWCC) to manage manufacturer predefined thermal profiles. The alienware-wmi driver exposes Thermal_Information and Thermal_Control methods through the Platform Profile API to mimic AWCC's behavior.

This newer interface, named AWCCMethodFunction has been reverse engineered, as Dell has not provided any official documentation. We will try to describe to the best of our ability its discovered inner workings.

> [!NOTE]
>
> The following method description may be incomplete and some operations have different implementations between devices.

<a id="rst-wmi-interface-description"></a>

### WMI interface description

The WMI interface description can be decoded from the embedded binary MOF (bmof) data using the [bmfdec](<https://github.com/pali/bmfdec>)<a id="rst-bmfdec"></a> utility:



```text
[WMI, Dynamic, Provider("WmiProv"), Locale("MS\\0x409"), Description("WMI Function"), guid("{A70591CE-A997-11DA-B012-B622A1EF5492}")]
class AWCCWmiMethodFunction {
  [key, read] string InstanceName;
  [read] boolean Active;

  [WmiMethodId(13), Implemented, read, write, Description("Return Overclocking Report.")] void Return_OverclockingReport([out] uint32 argr);
  [WmiMethodId(14), Implemented, read, write, Description("Set OCUIBIOS Control.")] void Set_OCUIBIOSControl([in] uint32 arg2, [out] uint32 argr);
  [WmiMethodId(15), Implemented, read, write, Description("Clear OC FailSafe Flag.")] void Clear_OCFailSafeFlag([out] uint32 argr);
  [WmiMethodId(19), Implemented, read, write, Description("Get Fan Sensors.")] void GetFanSensors([in] uint32 arg2, [out] uint32 argr);
  [WmiMethodId(20), Implemented, read, write, Description("Thermal Information.")] void Thermal_Information([in] uint32 arg2, [out] uint32 argr);
  [WmiMethodId(21), Implemented, read, write, Description("Thermal Control.")] void Thermal_Control([in] uint32 arg2, [out] uint32 argr);
  [WmiMethodId(23), Implemented, read, write, Description("MemoryOCControl.")] void MemoryOCControl([in] uint32 arg2, [out] uint32 argr);
  [WmiMethodId(26), Implemented, read, write, Description("System Information.")] void SystemInformation([in] uint32 arg2, [out] uint32 argr);
  [WmiMethodId(28), Implemented, read, write, Description("Power Information.")] void PowerInformation([in] uint32 arg2, [out] uint32 argr);
  [WmiMethodId(32), Implemented, read, write, Description("FW Update GPIO toggle.")] void FWUpdateGPIOtoggle([in] uint32 arg2, [out] uint32 argr);
  [WmiMethodId(33), Implemented, read, write, Description("Read Total of GPIOs.")] void ReadTotalofGPIOs([out] uint32 argr);
  [WmiMethodId(34), Implemented, read, write, Description("Read GPIO pin Status.")] void ReadGPIOpPinStatus([in] uint32 arg2, [out] uint32 argr);
  [WmiMethodId(35), Implemented, read, write, Description("Read Chassis Color.")] void ReadChassisColor([out] uint32 argr);
  [WmiMethodId(36), Implemented, read, write, Description("Read Platform Properties.")] void ReadPlatformProperties([out] uint32 argr);
  [WmiMethodId(37), Implemented, read, write, Description("Game Shift Status.")] void GameShiftStatus([in] uint32 arg2, [out] uint32 argr);
  [WmiMethodId(128), Implemented, read, write, Description("Caldera SW installation.")] void CalderaSWInstallation([out] uint32 argr);
  [WmiMethodId(129), Implemented, read, write, Description("Caldera SW is released.")] void CalderaSWReleased([out] uint32 argr);
  [WmiMethodId(130), Implemented, read, write, Description("Caldera Connection Status.")] void CalderaConnectionStatus([in] uint32 arg2, [out] uint32 argr);
  [WmiMethodId(131), Implemented, read, write, Description("Surprise Unplugged Flag Status.")] void SurpriseUnpluggedFlagStatus([out] uint32 argr);
  [WmiMethodId(132), Implemented, read, write, Description("Clear Surprise Unplugged Flag.")] void ClearSurpriseUnpluggedFlag([out] uint32 argr);
  [WmiMethodId(133), Implemented, read, write, Description("Cancel Undock Request.")] void CancelUndockRequest([out] uint32 argr);
  [WmiMethodId(135), Implemented, read, write, Description("Devices in Caldera.")] void DevicesInCaldera([in] uint32 arg2, [out] uint32 argr);
  [WmiMethodId(136), Implemented, read, write, Description("Notify BIOS for SW ready to disconnect Caldera.")] void NotifyBIOSForSWReadyToDisconnectCaldera([out] uint32 argr);
  [WmiMethodId(160), Implemented, read, write, Description("Tobii SW installation.")] void TobiiSWinstallation([out] uint32 argr);
  [WmiMethodId(161), Implemented, read, write, Description("Tobii SW Released.")] void TobiiSWReleased([out] uint32 argr);
  [WmiMethodId(162), Implemented, read, write, Description("Tobii Camera Power Reset.")] void TobiiCameraPowerReset([out] uint32 argr);
  [WmiMethodId(163), Implemented, read, write, Description("Tobii Camera Power On.")] void TobiiCameraPowerOn([out] uint32 argr);
  [WmiMethodId(164), Implemented, read, write, Description("Tobii Camera Power Off.")] void TobiiCameraPowerOff([out] uint32 argr);
};
```

Methods not described in the following document have unknown behavior.

<a id="rst-argument-structure"></a>

### Argument Structure

All input arguments have type **uint32** and their structure is very similar between methods. Usually, the first byte corresponds to a specific *operation* the method performs, and the subsequent bytes correspond to *arguments* passed to this *operation*. For example, if an operation has code 0x01 and requires an ID 0xA0, the argument you would pass to the method is 0xA001.

<a id="rst-thermal-methods"></a>

## Thermal Methods

<a id="rst-wmi-method-getfansensors-in-uint32-arg2-out-uint32-argr"></a>

### WMI method GetFanSensors(\[in\] uint32 arg2, \[out\] uint32 argr)


<table>
<thead>
<tr>
<th>


Operation (Byte 0)

</th>
<th>


Description

</th>
<th>


Arguments

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


0x01

</td>
<td>


Get the number of temperature sensors related with a fan ID

</td>
<td>


- Byte 1: Fan ID

</td>
</tr>
<tr>
<td>


0x02

</td>
<td>


Get the temperature sensor IDs related to a fan sensor ID

</td>
<td>


- Byte 1: Fan ID

- Byte 2: Index

</td>
</tr>
</tbody>
</table>

<a id="rst-wmi-method-thermal-information-in-uint32-arg2-out-uint32-argr"></a>

### WMI method Thermal_Information(\[in\] uint32 arg2, \[out\] uint32 argr)


<table>
<thead>
<tr>
<th>


Operation (Byte 0)

</th>
<th>


Description

</th>
<th>


Arguments

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


0x01

</td>
<td>


Unknown.

</td>
<td>


- None

</td>
</tr>
<tr>
<td>


0x02

</td>
<td>


Get system description number with the following structure:

- Byte 0: Number of fans

- Byte 1: Number of temperature sensors

- Byte 2: Unknown

- Byte 3: Number of thermal profiles

</td>
<td>


- None

</td>
</tr>
<tr>
<td>


0x03

</td>
<td>


List an ID or resource at a given index. Fan IDs, temperature IDs, unknown IDs and thermal profile IDs are listed in that exact order.

Operation 0x02 is used to know which indexes map to which resources.

**Returns:** ID at a given index

</td>
<td>


- Byte 1: Index

</td>
</tr>
<tr>
<td>


0x04

</td>
<td>


Get the current temperature for a given temperature sensor.

</td>
<td>


- Byte 1: Sensor ID

</td>
</tr>
<tr>
<td>


0x05

</td>
<td>


Get the current RPM for a given fan.

</td>
<td>


- Byte 1: Fan ID

</td>
</tr>
<tr>
<td>


0x06

</td>
<td>


Get fan speed percentage. (not implemented in every model)

</td>
<td>


- Byte 1: Fan ID

</td>
</tr>
<tr>
<td>


0x07

</td>
<td>


Unknown.

</td>
<td>


- Unknown

</td>
</tr>
<tr>
<td>


0x08

</td>
<td>


Get minimum RPM for a given FAN ID.

</td>
<td>


- Byte 1: Fan ID

</td>
</tr>
<tr>
<td>


0x09

</td>
<td>


Get maximum RPM for a given FAN ID.

</td>
<td>


- Byte 1: Fan ID

</td>
</tr>
<tr>
<td>


0x0A

</td>
<td>


Get balanced thermal profile ID.

</td>
<td>


- None

</td>
</tr>
<tr>
<td>


0x0B

</td>
<td>


Get current thermal profile ID.

</td>
<td>


- None

</td>
</tr>
<tr>
<td>


0x0C

</td>
<td>


Get current `boost` value for a given fan ID.

</td>
<td>


- Byte 1: Fan ID

</td>
</tr>
</tbody>
</table>

<a id="rst-wmi-method-thermal-control-in-uint32-arg2-out-uint32-argr"></a>

### WMI method Thermal_Control(\[in\] uint32 arg2, \[out\] uint32 argr)


<table>
<thead>
<tr>
<th>


Operation (Byte 0)

</th>
<th>


Description

</th>
<th>


Arguments

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


0x01

</td>
<td>


Activate a given thermal profile.

</td>
<td>


- Byte 1: Thermal profile ID

</td>
</tr>
<tr>
<td>


0x02

</td>
<td>


Set a `boost` value for a given fan ID.

</td>
<td>


- Byte 1: Fan ID

- Byte 2: Boost

</td>
</tr>
</tbody>
</table>

These are the known thermal profile codes:


<table>
<thead>
<tr>
<th>


Thermal Profile

</th>
<th>


Type

</th>
<th>


ID

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


Custom

</td>
<td>


Special

</td>
<td>


0x00

</td>
</tr>
<tr>
<td>


G-Mode

</td>
<td>


Special

</td>
<td>


0xAB

</td>
</tr>
<tr>
<td>


Quiet

</td>
<td>


Legacy

</td>
<td>


0x96

</td>
</tr>
<tr>
<td>


Balanced

</td>
<td>


Legacy

</td>
<td>


0x97

</td>
</tr>
<tr>
<td>


Balanced Performance

</td>
<td>


Legacy

</td>
<td>


0x98

</td>
</tr>
<tr>
<td>


Performance

</td>
<td>


Legacy

</td>
<td>


0x99

</td>
</tr>
<tr>
<td>


Balanced

</td>
<td>


USTT

</td>
<td>


0xA0

</td>
</tr>
<tr>
<td>


Balanced Performance

</td>
<td>


USTT

</td>
<td>


0xA1

</td>
</tr>
<tr>
<td>


Cool

</td>
<td>


USTT

</td>
<td>


0xA2

</td>
</tr>
<tr>
<td>


Quiet

</td>
<td>


USTT

</td>
<td>


0xA3

</td>
</tr>
<tr>
<td>


Performance

</td>
<td>


USTT

</td>
<td>


0xA4

</td>
</tr>
<tr>
<td>


Low Power

</td>
<td>


USTT

</td>
<td>


0xA5

</td>
</tr>
</tbody>
</table>

If a model supports the User Selectable Thermal Tables (USTT) profiles, it will not support the Legacy profiles and vice-versa.

Every model supports the CUSTOM (0x00) thermal profile. GMODE replaces PERFORMANCE in G-Series laptops.

<a id="rst-wmi-method-gameshiftstatus-in-uint32-arg2-out-uint32-argr"></a>

### WMI method GameShiftStatus(\[in\] uint32 arg2, \[out\] uint32 argr)


<table>
<thead>
<tr>
<th>


Operation (Byte 0)

</th>
<th>


Description

</th>
<th>


Arguments

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


0x01

</td>
<td>


Toggle *Game Shift*.

</td>
<td>


- None

</td>
</tr>
<tr>
<td>


0x02

</td>
<td>


Get *Game Shift* status.

</td>
<td>


- None

</td>
</tr>
</tbody>
</table>

Game Shift Status does not change the fan speed profile but it could be some sort of CPU/GPU power profile. Benchmarks have not been done.

This method is only present on Dell's G-Series laptops and it's implementation implies GMODE thermal profile is available, even if operation 0x03 of Thermal_Information does not list it.

G-key on Dell's G-Series laptops also changes Game Shift status, so both are directly related.

<a id="rst-overclocking-methods"></a>

## Overclocking Methods

<a id="rst-wmi-method-memoryoccontrol-in-uint32-arg2-out-uint32-argr"></a>

### WMI method MemoryOCControl(\[in\] uint32 arg2, \[out\] uint32 argr)

AWCC supports memory overclocking, but this method is very intricate and has not been deciphered yet.

<a id="rst-gpio-control-methods"></a>

## GPIO control Methods

Alienware and Dell G Series devices with the AWCC interface usually have an embedded STM32 RGB lighting controller with USB/HID capabilities. It's vendor ID is `187c` while it's product ID may vary from model to model.

The control of two GPIO pins of this MCU is exposed as WMI methods for debugging purposes.


<table>
<thead>
<tr>
<th>


Pin

</th>
<th colspan="2">


Description

</th>
</tr>
</thead>
<tbody>
<tr>
<td rowspan="2">


0

</td>
<td rowspan="2">


Device Firmware Update (DFU) mode pin.

</td>
<td>


**HIGH**: Enables DFU mode on next MCU boot.

</td>
</tr>
<tr>
<td>


**LOW**: Disables DFU mode on next MCU boot.

</td>
</tr>
<tr>
<td rowspan="2">


1

</td>
<td rowspan="2">


Negative Reset (NRST) pin.

</td>
<td>


**HIGH**: MCU is ON.

</td>
</tr>
<tr>
<td>


**LOW**: MCU is OFF.

</td>
</tr>
</tbody>
</table>

See [Acknowledgements](<#rst-acknowledgements-1>) for more information on this MCU.

> [!NOTE]
>
> Some GPIO control methods break the usual argument structure and take a **Pin number** instead of an operation on the first byte.

<a id="rst-wmi-method-fwupdategpiotoggle-in-uint32-arg2-out-uint32-argr"></a>

### WMI method FWUpdateGPIOtoggle(\[in\] uint32 arg2, \[out\] uint32 argr)


<table>
<thead>
<tr>
<th>


Operation (Byte 0)

</th>
<th>


Description

</th>
<th>


Arguments

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


Pin number

</td>
<td>


Set the pin status

</td>
<td>


- Byte 1: Pin status

</td>
</tr>
</tbody>
</table>

<a id="rst-wmi-method-readtotalofgpios-out-uint32-argr"></a>

### WMI method ReadTotalofGPIOs(\[out\] uint32 argr)


<table>
<thead>
<tr>
<th>


Operation (Byte 0)

</th>
<th>


Description

</th>
<th>


Arguments

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


N/A

</td>
<td>


Get the total number of GPIOs

</td>
<td>


- None

</td>
</tr>
</tbody>
</table>

> [!NOTE]
>
> Due to how WMI methods are implemented on the firmware level, this method requires a dummy uint32 input argument when invoked.

<a id="rst-wmi-method-readgpioppinstatus-in-uint32-arg2-out-uint32-argr"></a>

### WMI method ReadGPIOpPinStatus(\[in\] uint32 arg2, \[out\] uint32 argr)


<table>
<thead>
<tr>
<th>


Operation (Byte 0)

</th>
<th>


Description

</th>
<th>


Arguments

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


Pin number

</td>
<td>


Get the pin status

</td>
<td>


- None

</td>
</tr>
</tbody>
</table>

> [!NOTE]
>
> There known firmware bug in some laptops where reading the status of a pin also flips it.

<a id="rst-other-information-methods"></a>

## Other information Methods

<a id="rst-wmi-method-readchassiscolor-out-uint32-argr"></a>

### WMI method ReadChassisColor(\[out\] uint32 argr)

Returns the chassis color internal ID.

<a id="rst-acknowledgements-1"></a>
<a id="rst-acknowledgements"></a>

## Acknowledgements

Kudos to

- [AlexIII](<https://github.com/AlexIII/tcc-g15>)<a id="rst-alexiii"></a>

- [T-Troll](<https://github.com/T-Troll/alienfx-tools/>)<a id="rst-t-troll"></a>

- [Gabriel Marcano](<https://gabriel.marcanobrady.family/blog/2024/12/16/dell-g5-5505-se-acpi-or-figuring-out-how-to-reset-the-rgb-controller/>)<a id="rst-gabriel-marcano"></a>

for documenting and testing some of this device's functionality, making it possible to generalize this driver.
