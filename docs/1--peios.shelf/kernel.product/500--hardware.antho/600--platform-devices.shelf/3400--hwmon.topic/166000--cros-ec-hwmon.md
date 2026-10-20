---
title: "Kernel driver cros_ec_hwmon"
type: reference
description: "Supported chips:"
---

<a id="rst-kernel-driver-cros-ec-hwmon"></a>

<!-- SPDX-License-Identifier: GPL-2.0-or-later -->

Supported chips:

> - ChromeOS embedded controllers.
>
>   Prefix: 'cros_ec'
>
>   Addresses scanned: -

Author:

> - Thomas Weißschuh &lt;[linux@weissschuh.net](<mailto:linux@weissschuh.net>)&gt;

<a id="rst-description"></a>

## Description

This driver implements support for hardware monitoring commands exposed by the ChromeOS embedded controller used in Chromebooks and other devices.

The channel labels exposed via hwmon are retrieved from the EC itself.

<a id="rst-supported-features"></a>

## Supported features

- **Fan readings**

  Always supported.

- **Fan target speed**

  If supported by the EC.

- **Temperature readings**

  Always supported.

- **Temperature thresholds**

  If supported by the EC.

- **PWM fan control**

  If the EC also supports setting fan PWM values and fan mode.

  Note that EC will switch fan control mode back to auto when suspended. This driver will restore the fan state to what they were before suspended when resumed.

  If a fan is controllable, this driver will register that fan as a cooling device in the thermal framework as well.
