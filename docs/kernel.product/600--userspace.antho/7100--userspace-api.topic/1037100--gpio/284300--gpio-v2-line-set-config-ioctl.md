---
title: "GPIO_V2_LINE_SET_CONFIG_IOCTL"
type: reference
description: "Duplicate implicit target name: \"gpio_v2_line_set_config_ioctl\"."
---

<a id="rst-gpio-v2-line-set-config-ioctl-1"></a>
<a id="rst-gpio-v2-line-set-config-ioctl"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-name"></a>

## Name

GPIO_V2_LINE_SET_CONFIG_IOCTL - Update the configuration of previously requested lines.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-GPIO_V2_LINE_SET_CONFIG_IOCTL"></a>

```c
GPIO_V2_LINE_SET_CONFIG_IOCTL
```

`int ioctl(int req_fd, GPIO_V2_LINE_SET_CONFIG_IOCTL, struct gpio_v2_line_config *config)`

<a id="rst-arguments"></a>

## Arguments

- **`req_fd`**

  The file descriptor of the GPIO character device, as returned in the `request.fd<gpio_v2_line_request>` by [gpio-v2-get-line-ioctl.rst](~kernel/userspace/userspace-api/gpio/gpio-v2-get-line-ioctl).

- **`config`**

  The new `configuration<gpio_v2_line_config>` to apply to the requested lines.

<a id="rst-description"></a>

## Description

Update the configuration of previously requested lines, without releasing the line or introducing potential glitches.

The new configuration must specify a configuration for all requested lines.

The same [Configuration Rules](<~kernel/userspace/userspace-api/gpio/gpio-v2-get-line-ioctl#rst-gpio-v2-get-line-config-rules>) and [Configuration Support](<~kernel/userspace/userspace-api/gpio/gpio-v2-get-line-ioctl#rst-gpio-v2-get-line-config-support>) that apply when requesting the lines also apply when updating the line configuration, with the additional restriction that a direction flag must be set to enable reconfiguration. If no direction flag is set in the configuration for a given line then the configuration for that line is left unchanged.

The motivating use case for this command is changing direction of bi-directional lines between input and output, but it may also be used to dynamically control edge detection, or more generally move lines seamlessly from one configuration state to another.

To only change the value of output lines, use [gpio-v2-line-set-values-ioctl.rst](~kernel/userspace/userspace-api/gpio/gpio-v2-line-set-values-ioctl).

<a id="rst-return-value"></a>

## Return Value

On success 0.

On error -1 and the `errno` variable is set appropriately. Common error codes are described in [error-codes.rst](~kernel/userspace/userspace-api/gpio/error-codes).
