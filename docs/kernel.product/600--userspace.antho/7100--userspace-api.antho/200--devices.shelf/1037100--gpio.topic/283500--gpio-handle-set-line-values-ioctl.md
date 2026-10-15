---
title: "GPIO_HANDLE_SET_LINE_VALUES_IOCTL"
type: reference
description: "Duplicate implicit target name: \"gpio_handle_set_line_values_ioctl\"."
---

<a id="rst-gpio-handle-set-line-values-ioctl-1"></a>
<a id="rst-gpio-handle-set-line-values-ioctl"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

> [!WARNING]
>
> This ioctl is part of [chardev_v1.rst](~kernel/userspace/userspace-api/gpio/chardev-v1) and is obsoleted by [gpio-v2-line-set-values-ioctl.rst](~kernel/userspace/userspace-api/gpio/gpio-v2-line-set-values-ioctl).

<a id="rst-name"></a>

## Name

GPIO_HANDLE_SET_LINE_VALUES_IOCTL - Set the values of all requested output lines.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-GPIO_HANDLE_SET_LINE_VALUES_IOCTL"></a>

```c
GPIO_HANDLE_SET_LINE_VALUES_IOCTL
```

`int ioctl(int handle_fd, GPIO_HANDLE_SET_LINE_VALUES_IOCTL, struct gpiohandle_data *values)`

<a id="rst-arguments"></a>

## Arguments

- **`handle_fd`**

  The file descriptor of the GPIO character device, as returned in the `request.fd<gpiohandle_request>` by [gpio-get-linehandle-ioctl.rst](~kernel/userspace/userspace-api/gpio/gpio-get-linehandle-ioctl).

- **`values`**

  The `line_values<gpiohandle_data>` to set.

<a id="rst-description"></a>

## Description

Set the values of all requested output lines.

The values set are logical, indicating if the line is to be active or inactive. The `GPIOHANDLE_REQUEST_ACTIVE_LOW` flag controls the mapping between logical values (active/inactive) and physical values (high/low). If  `GPIOHANDLE_REQUEST_ACTIVE_LOW` is not set then active is high and inactive is low. If `GPIOHANDLE_REQUEST_ACTIVE_LOW` is set then active is low and inactive is high.

Only the values of output lines may be set. Attempting to set the value of input lines is an error (**EPERM**).

<a id="rst-return-value"></a>

## Return Value

On success 0.

On error -1 and the `errno` variable is set appropriately. Common error codes are described in [error-codes.rst](~kernel/userspace/userspace-api/gpio/error-codes).
