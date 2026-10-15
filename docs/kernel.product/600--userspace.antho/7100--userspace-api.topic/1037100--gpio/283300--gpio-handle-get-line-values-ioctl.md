---
title: "GPIOHANDLE_GET_LINE_VALUES_IOCTL"
type: reference
description: "Duplicate implicit target name: \"gpiohandle_get_line_values_ioctl\"."
---

<a id="rst-gpiohandle-get-line-values-ioctl-1"></a>
<a id="rst-gpiohandle-get-line-values-ioctl"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

> [!WARNING]
>
> This ioctl is part of [chardev_v1.rst](~kernel/userspace/userspace-api/gpio/chardev-v1) and is obsoleted by [gpio-v2-line-get-values-ioctl.rst](~kernel/userspace/userspace-api/gpio/gpio-v2-line-get-values-ioctl).

<a id="rst-name"></a>

## Name

GPIOHANDLE_GET_LINE_VALUES_IOCTL - Get the values of all requested lines.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-GPIOHANDLE_GET_LINE_VALUES_IOCTL"></a>

```c
GPIOHANDLE_GET_LINE_VALUES_IOCTL
```

`int ioctl(int handle_fd, GPIOHANDLE_GET_LINE_VALUES_IOCTL, struct gpiohandle_data *values)`

<a id="rst-arguments"></a>

## Arguments

- **`handle_fd`**

  The file descriptor of the GPIO character device, as returned in the `request.fd<gpiohandle_request>` by [gpio-get-linehandle-ioctl.rst](~kernel/userspace/userspace-api/gpio/gpio-get-linehandle-ioctl).

- **`values`**

  The `line_values<gpiohandle_data>` to be populated.

<a id="rst-description"></a>

## Description

Get the values of all requested lines.

The values returned are logical, indicating if the line is active or inactive. The `GPIOHANDLE_REQUEST_ACTIVE_LOW` flag controls the mapping between physical values (high/low) and logical values (active/inactive). If `GPIOHANDLE_REQUEST_ACTIVE_LOW` is not set then high is active and low is inactive. If `GPIOHANDLE_REQUEST_ACTIVE_LOW` is set then low is active and high is inactive.

The values of both input and output lines may be read.

For output lines, the value returned is driver and configuration dependent and may be either the output buffer (the last requested value set) or the input buffer (the actual level of the line), and depending on the hardware and configuration these may differ.

This ioctl can also be used to read the line value for line events, substituting the `event_fd` for the `handle_fd`.  As there is only one line requested in that case, only the one value is returned in `values`.

<a id="rst-return-value"></a>

## Return Value

On success 0 and `values` populated with the values read.

On error -1 and the `errno` variable is set appropriately. Common error codes are described in [error-codes.rst](~kernel/userspace/userspace-api/gpio/error-codes).
