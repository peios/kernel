---
title: "GPIO_V2_LINE_GET_VALUES_IOCTL"
type: reference
description: "Duplicate implicit target name: \"gpio_v2_line_get_values_ioctl\"."
---

<a id="rst-gpio-v2-line-get-values-ioctl-1"></a>
<a id="rst-gpio-v2-line-get-values-ioctl"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-name"></a>

## Name

GPIO_V2_LINE_GET_VALUES_IOCTL - Get the values of requested lines.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-GPIO_V2_LINE_GET_VALUES_IOCTL"></a>

```c
GPIO_V2_LINE_GET_VALUES_IOCTL
```

`int ioctl(int req_fd, GPIO_V2_LINE_GET_VALUES_IOCTL, struct gpio_v2_line_values *values)`

<a id="rst-arguments"></a>

## Arguments

- **`req_fd`**

  The file descriptor of the GPIO character device, as returned in the `request.fd<gpio_v2_line_request>` by [gpio-v2-get-line-ioctl.rst](~kernel/userspace/userspace-api/gpio/gpio-v2-get-line-ioctl).

- **`values`**

  The `line_values<gpio_v2_line_values>` to get with the `mask` set to indicate the subset of requested lines to get.

<a id="rst-description"></a>

## Description

Get the values of requested lines.

The values returned are logical, indicating if the line is active or inactive. The `GPIO_V2_LINE_FLAG_ACTIVE_LOW` flag controls the mapping between physical values (high/low) and logical values (active/inactive). If `GPIO_V2_LINE_FLAG_ACTIVE_LOW` is not set then high is active and low is inactive.  If `GPIO_V2_LINE_FLAG_ACTIVE_LOW` is set then low is active and high is inactive.

The values of both input and output lines may be read.

For output lines, the value returned is driver and configuration dependent and may be either the output buffer (the last requested value set) or the input buffer (the actual level of the line), and depending on the hardware and configuration these may differ.

<a id="rst-return-value"></a>

## Return Value

On success 0 and the corresponding `values.bits<gpio_v2_line_values>` contain the value read.

On error -1 and the `errno` variable is set appropriately. Common error codes are described in [error-codes.rst](~kernel/userspace/userspace-api/gpio/error-codes).
