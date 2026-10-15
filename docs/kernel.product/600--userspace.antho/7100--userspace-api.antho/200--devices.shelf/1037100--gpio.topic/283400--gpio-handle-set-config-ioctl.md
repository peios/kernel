---
title: "GPIOHANDLE_SET_CONFIG_IOCTL"
type: reference
description: "Duplicate implicit target name: \"gpiohandle_set_config_ioctl\"."
---

<a id="rst-gpiohandle-set-config-ioctl-1"></a>
<a id="rst-gpiohandle-set-config-ioctl"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

> [!WARNING]
>
> This ioctl is part of [chardev_v1.rst](~kernel/userspace/userspace-api/gpio/chardev-v1) and is obsoleted by [gpio-v2-line-set-config-ioctl.rst](~kernel/userspace/userspace-api/gpio/gpio-v2-line-set-config-ioctl).

<a id="rst-name"></a>

## Name

GPIOHANDLE_SET_CONFIG_IOCTL - Update the configuration of previously requested lines.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-GPIOHANDLE_SET_CONFIG_IOCTL"></a>

```c
GPIOHANDLE_SET_CONFIG_IOCTL
```

`int ioctl(int handle_fd, GPIOHANDLE_SET_CONFIG_IOCTL, struct gpiohandle_config *config)`

<a id="rst-arguments"></a>

## Arguments

- **`handle_fd`**

  The file descriptor of the GPIO character device, as returned in the `request.fd<gpiohandle_request>` by [gpio-get-linehandle-ioctl.rst](~kernel/userspace/userspace-api/gpio/gpio-get-linehandle-ioctl).

- **`config`**

  The new `configuration<gpiohandle_config>` to apply to the requested lines.

<a id="rst-description"></a>

## Description

Update the configuration of previously requested lines, without releasing the line or introducing potential glitches.

The configuration applies to all requested lines.

The same [Configuration Rules](<~kernel/userspace/userspace-api/gpio/gpio-get-linehandle-ioctl#rst-gpio-get-linehandle-config-rules>) and [Configuration Support](<~kernel/userspace/userspace-api/gpio/gpio-get-linehandle-ioctl#rst-gpio-get-linehandle-config-support>) that apply when requesting the lines also apply when updating the line configuration, with the additional restriction that a direction flag must be set. Requesting an invalid configuration, including without a direction flag set, is an error (**EINVAL**).

The motivating use case for this command is changing direction of bi-directional lines between input and output, but it may be used more generally to move lines seamlessly from one configuration state to another.

To only change the value of output lines, use [gpio-handle-set-line-values-ioctl.rst](~kernel/userspace/userspace-api/gpio/gpio-handle-set-line-values-ioctl).

First added in 5.5.

<a id="rst-return-value"></a>

## Return Value

On success 0.

On error -1 and the `errno` variable is set appropriately. Common error codes are described in [error-codes.rst](~kernel/userspace/userspace-api/gpio/error-codes).
