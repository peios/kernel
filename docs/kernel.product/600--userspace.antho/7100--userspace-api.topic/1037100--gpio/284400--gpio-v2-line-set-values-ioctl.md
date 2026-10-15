---
title: "GPIO_V2_LINE_SET_VALUES_IOCTL"
type: reference
description: "Duplicate implicit target name: \"gpio_v2_line_set_values_ioctl\"."
---

<a id="rst-gpio-v2-line-set-values-ioctl-1"></a>
<a id="rst-gpio-v2-line-set-values-ioctl"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-name"></a>

## Name

GPIO_V2_LINE_SET_VALUES_IOCTL - Set the values of requested output lines.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-GPIO_V2_LINE_SET_VALUES_IOCTL"></a>

```c
GPIO_V2_LINE_SET_VALUES_IOCTL
```

`int ioctl(int req_fd, GPIO_V2_LINE_SET_VALUES_IOCTL, struct gpio_v2_line_values *values)`

<a id="rst-arguments"></a>

## Arguments

- **`req_fd`**

  The file descriptor of the GPIO character device, as returned in the `request.fd<gpio_v2_line_request>` by [gpio-v2-get-line-ioctl.rst](~kernel/userspace/userspace-api/gpio/gpio-v2-get-line-ioctl).

- **`values`**

  The `line_values<gpio_v2_line_values>` to set with the `mask` set to indicate the subset of requested lines to set and `bits` set to indicate the new value.

<a id="rst-description"></a>

## Description

Set the values of requested output lines.

The values set are logical, indicating if the line is to be active or inactive. The `GPIO_V2_LINE_FLAG_ACTIVE_LOW` flag controls the mapping between logical values (active/inactive) and physical values (high/low). If `GPIO_V2_LINE_FLAG_ACTIVE_LOW` is not set then active is high and inactive is low.  If `GPIO_V2_LINE_FLAG_ACTIVE_LOW` is set then active is low and inactive is high.

Only the values of output lines may be set. Attempting to set the value of an input line is an error (**EPERM**).

<a id="rst-return-value"></a>

## Return Value

On success 0.

On error -1 and the `errno` variable is set appropriately. Common error codes are described in [error-codes.rst](~kernel/userspace/userspace-api/gpio/error-codes).
