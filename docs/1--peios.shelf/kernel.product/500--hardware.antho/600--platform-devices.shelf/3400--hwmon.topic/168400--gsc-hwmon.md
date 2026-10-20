---
title: "Kernel driver gsc-hwmon"
type: reference
description: "Supported chips: Gateworks GSC Datasheet: http://trac.gateworks.com/wiki/gsc Author: Tim Harvey <tharvey@gateworks.com>"
---

<a id="rst-kernel-driver-gsc-hwmon"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

Supported chips: Gateworks GSC Datasheet: [http://trac.gateworks.com/wiki/gsc](<http://trac.gateworks.com/wiki/gsc>) Author: Tim Harvey &lt;[tharvey@gateworks.com](<mailto:tharvey@gateworks.com>)&gt;

<a id="rst-description"></a>

## Description:

This driver supports hardware monitoring for the temperature sensor, various ADC's connected to the GSC, and optional FAN controller available on some boards.

<a id="rst-voltage-monitoring"></a>

## Voltage Monitoring

The voltage inputs are scaled either internally or by the driver depending on the GSC version and firmware. The values returned by the driver do not need further scaling. The voltage input labels provide the voltage rail name:

inX_input                  Measured voltage (mV). inX_label                  Name of voltage rail.

<a id="rst-temperature-monitoring"></a>

## Temperature Monitoring

Temperatures are measured with 12-bit or 10-bit resolution and are scaled either internally or by the driver depending on the GSC version and firmware. The values returned by the driver reflect millidegree Celsius:

tempX_input                Measured temperature. tempX_label                Name of temperature input.

<a id="rst-pwm-output-control"></a>

## PWM Output Control

The GSC features 1 PWM output that operates in automatic mode where the PWM value will be scaled depending on 6 temperature boundaries. The tempeature boundaries are read-write and in millidegree Celsius and the read-only PWM values range from 0 (off) to 255 (full speed). Fan speed will be set to minimum (off) when the temperature sensor reads less than pwm1_auto_point1_temp and maximum when the temperature sensor equals or exceeds pwm1_auto_point6_temp.

pwm1_auto_point\[1-6\]\_pwm       PWM value. pwm1_auto_point\[1-6\]\_temp      Temperature boundary.
