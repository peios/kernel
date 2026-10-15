---
title: "Kernel driver Ampere(R)'s Altra(R) SMpro hwmon"
type: reference
description: "Supported chips:"
---

<a id="rst-kernel-driver-ampere-r-s-altra-r-smpro-hwmon"></a>

<!-- SPDX-License-Identifier: GPL-2.0-only -->

Supported chips:

> - Ampere(R) Altra(R)
>
>   Prefix: `smpro`
>
>   Reference: `Altra SoC BMC Interface Specification`

Author: Thu Nguyen &lt;[thu@os.amperecomputing.com](<mailto:thu@os.amperecomputing.com>)&gt;

<a id="rst-description"></a>

## Description

The smpro-hwmon driver supports hardware monitoring for Ampere(R) Altra(R) SoCs based on the SMpro co-processor (SMpro).  The following sensor metrics are supported by the driver:

> - temperature
>
> - voltage
>
> - current
>
> - power

The interface provides the registers to query the various sensors and their values which are then exported to userspace by this driver.

<a id="rst-usage-notes"></a>

## Usage Notes

The driver creates at least two sysfs files for each sensor.

- `<sensor_type><idx>_label` reports the sensor label.

- `<sensor_type><idx>_input` returns the sensor value.

The sysfs files are allocated in the SMpro rootfs folder, with one root directory for each instance.

When the SoC is turned off, the driver will fail to read registers and return `-ENXIO`.

<a id="rst-sysfs-entries"></a>

## Sysfs entries

The following sysfs files are supported:

- Ampere(R) Altra(R):


  <table>
  <thead>
  <tr>
  <th>


  Name

  </th>
  <th>


  Unit

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


  temp1_input

  </td>
  <td>


  millicelsius

  </td>
  <td>


  RO

  </td>
  <td>


  SoC temperature

  </td>
  </tr>
  <tr>
  <td>


  temp2_input

  </td>
  <td>


  millicelsius

  </td>
  <td>


  RO

  </td>
  <td>


  Max temperature reported among SoC VRDs

  </td>
  </tr>
  <tr>
  <td>


  temp2_crit

  </td>
  <td>


  millicelsius

  </td>
  <td>


  RO

  </td>
  <td>


  SoC VRD HOT Threshold temperature

  </td>
  </tr>
  <tr>
  <td>


  temp3_input

  </td>
  <td>


  millicelsius

  </td>
  <td>


  RO

  </td>
  <td>


  Max temperature reported among DIMM VRDs

  </td>
  </tr>
  <tr>
  <td>


  temp4_input

  </td>
  <td>


  millicelsius

  </td>
  <td>


  RO

  </td>
  <td>


  Max temperature reported among Core VRDs

  </td>
  </tr>
  <tr>
  <td>


  temp5_input

  </td>
  <td>


  millicelsius

  </td>
  <td>


  RO

  </td>
  <td>


  Temperature of DIMM0 on CH0

  </td>
  </tr>
  <tr>
  <td>


  temp5_crit

  </td>
  <td>


  millicelsius

  </td>
  <td>


  RO

  </td>
  <td>


  MEM HOT Threshold for all DIMMs

  </td>
  </tr>
  <tr>
  <td>


  temp6_input

  </td>
  <td>


  millicelsius

  </td>
  <td>


  RO

  </td>
  <td>


  Temperature of DIMM0 on CH1

  </td>
  </tr>
  <tr>
  <td>


  temp6_crit

  </td>
  <td>


  millicelsius

  </td>
  <td>


  RO

  </td>
  <td>


  MEM HOT Threshold for all DIMMs

  </td>
  </tr>
  <tr>
  <td>


  temp7_input

  </td>
  <td>


  millicelsius

  </td>
  <td>


  RO

  </td>
  <td>


  Temperature of DIMM0 on CH2

  </td>
  </tr>
  <tr>
  <td>


  temp7_crit

  </td>
  <td>


  millicelsius

  </td>
  <td>


  RO

  </td>
  <td>


  MEM HOT Threshold for all DIMMs

  </td>
  </tr>
  <tr>
  <td>


  temp8_input

  </td>
  <td>


  millicelsius

  </td>
  <td>


  RO

  </td>
  <td>


  Temperature of DIMM0 on CH3

  </td>
  </tr>
  <tr>
  <td>


  temp8_crit

  </td>
  <td>


  millicelsius

  </td>
  <td>


  RO

  </td>
  <td>


  MEM HOT Threshold for all DIMMs

  </td>
  </tr>
  <tr>
  <td>


  temp9_input

  </td>
  <td>


  millicelsius

  </td>
  <td>


  RO

  </td>
  <td>


  Temperature of DIMM0 on CH4

  </td>
  </tr>
  <tr>
  <td>


  temp9_crit

  </td>
  <td>


  millicelsius

  </td>
  <td>


  RO

  </td>
  <td>


  MEM HOT Threshold for all DIMMs

  </td>
  </tr>
  <tr>
  <td>


  temp10_input

  </td>
  <td>


  millicelsius

  </td>
  <td>


  RO

  </td>
  <td>


  Temperature of DIMM0 on CH5

  </td>
  </tr>
  <tr>
  <td>


  temp10_crit

  </td>
  <td>


  millicelsius

  </td>
  <td>


  RO

  </td>
  <td>


  MEM HOT Threshold for all DIMMs

  </td>
  </tr>
  <tr>
  <td>


  temp11_input

  </td>
  <td>


  millicelsius

  </td>
  <td>


  RO

  </td>
  <td>


  Temperature of DIMM0 on CH6

  </td>
  </tr>
  <tr>
  <td>


  temp11_crit

  </td>
  <td>


  millicelsius

  </td>
  <td>


  RO

  </td>
  <td>


  MEM HOT Threshold for all DIMMs

  </td>
  </tr>
  <tr>
  <td>


  temp12_input

  </td>
  <td>


  millicelsius

  </td>
  <td>


  RO

  </td>
  <td>


  Temperature of DIMM0 on CH7

  </td>
  </tr>
  <tr>
  <td>


  temp12_crit

  </td>
  <td>


  millicelsius

  </td>
  <td>


  RO

  </td>
  <td>


  MEM HOT Threshold for all DIMMs

  </td>
  </tr>
  <tr>
  <td>


  temp13_input

  </td>
  <td>


  millicelsius

  </td>
  <td>


  RO

  </td>
  <td>


  Max temperature reported among RCA VRDs

  </td>
  </tr>
  <tr>
  <td>


  in0_input

  </td>
  <td>


  millivolts

  </td>
  <td>


  RO

  </td>
  <td>


  Core voltage

  </td>
  </tr>
  <tr>
  <td>


  in1_input

  </td>
  <td>


  millivolts

  </td>
  <td>


  RO

  </td>
  <td>


  SoC voltage

  </td>
  </tr>
  <tr>
  <td>


  in2_input

  </td>
  <td>


  millivolts

  </td>
  <td>


  RO

  </td>
  <td>


  DIMM VRD1 voltage

  </td>
  </tr>
  <tr>
  <td>


  in3_input

  </td>
  <td>


  millivolts

  </td>
  <td>


  RO

  </td>
  <td>


  DIMM VRD2 voltage

  </td>
  </tr>
  <tr>
  <td>


  in4_input

  </td>
  <td>


  millivolts

  </td>
  <td>


  RO

  </td>
  <td>


  RCA VRD voltage

  </td>
  </tr>
  <tr>
  <td>


  cur1_input

  </td>
  <td>


  milliamperes

  </td>
  <td>


  RO

  </td>
  <td>


  Core VRD current

  </td>
  </tr>
  <tr>
  <td>


  cur2_input

  </td>
  <td>


  milliamperes

  </td>
  <td>


  RO

  </td>
  <td>


  SoC VRD current

  </td>
  </tr>
  <tr>
  <td>


  cur3_input

  </td>
  <td>


  milliamperes

  </td>
  <td>


  RO

  </td>
  <td>


  DIMM VRD1 current

  </td>
  </tr>
  <tr>
  <td>


  cur4_input

  </td>
  <td>


  milliamperes

  </td>
  <td>


  RO

  </td>
  <td>


  DIMM VRD2 current

  </td>
  </tr>
  <tr>
  <td>


  cur5_input

  </td>
  <td>


  milliamperes

  </td>
  <td>


  RO

  </td>
  <td>


  RCA VRD current

  </td>
  </tr>
  <tr>
  <td>


  power1_input

  </td>
  <td>


  microwatts

  </td>
  <td>


  RO

  </td>
  <td>


  Core VRD power

  </td>
  </tr>
  <tr>
  <td>


  power2_input

  </td>
  <td>


  microwatts

  </td>
  <td>


  RO

  </td>
  <td>


  SoC VRD power

  </td>
  </tr>
  <tr>
  <td>


  power3_input

  </td>
  <td>


  microwatts

  </td>
  <td>


  RO

  </td>
  <td>


  DIMM VRD1 power

  </td>
  </tr>
  <tr>
  <td>


  power4_input

  </td>
  <td>


  microwatts

  </td>
  <td>


  RO

  </td>
  <td>


  DIMM VRD2 power

  </td>
  </tr>
  <tr>
  <td>


  power5_input

  </td>
  <td>


  microwatts

  </td>
  <td>


  RO

  </td>
  <td>


  RCA VRD power

  </td>
  </tr>
  </tbody>
  </table>

  Example:



  ```text
  # cat in0_input
  830
  # cat temp1_input
  37000
  # cat curr1_input
  9000
  # cat power5_input
  19500000
  ```
