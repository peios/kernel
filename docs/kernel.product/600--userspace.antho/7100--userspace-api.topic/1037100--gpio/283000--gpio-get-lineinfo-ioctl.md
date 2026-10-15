---
title: "GPIO_GET_LINEINFO_IOCTL"
type: reference
description: "Duplicate implicit target name: \"gpio_get_lineinfo_ioctl\"."
---

<a id="rst-gpio-get-lineinfo-ioctl-1"></a>
<a id="rst-gpio-get-lineinfo-ioctl"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

> [!WARNING]
>
> This ioctl is part of [chardev_v1.rst](~kernel/userspace/userspace-api/gpio/chardev-v1) and is obsoleted by [gpio-v2-get-lineinfo-ioctl.rst](~kernel/userspace/userspace-api/gpio/gpio-v2-get-lineinfo-ioctl).

<a id="rst-name"></a>

## Name

GPIO_GET_LINEINFO_IOCTL - Get the publicly available information for a line.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-GPIO_GET_LINEINFO_IOCTL"></a>

```c
GPIO_GET_LINEINFO_IOCTL
```

`int ioctl(int chip_fd, GPIO_GET_LINEINFO_IOCTL, struct gpioline_info *info)`

<a id="rst-arguments"></a>

## Arguments

- **`chip_fd`**

  The file descriptor of the GPIO character device returned by `open()`.

- **`info`**

  The `line_info<gpioline_info>` to be populated, with the `offset` field set to indicate the line to be collected.

<a id="rst-description"></a>

## Description

Get the publicly available information for a line.

This information is available independent of whether the line is in use.

> [!NOTE]
>
> The line info does not include the line value.
>
> The line must be requested using [gpio-get-linehandle-ioctl.rst](~kernel/userspace/userspace-api/gpio/gpio-get-linehandle-ioctl) or [gpio-get-lineevent-ioctl.rst](~kernel/userspace/userspace-api/gpio/gpio-get-lineevent-ioctl) to access its value.

<a id="rst-return-value"></a>

## Return Value

On success 0 and `info` is populated with the chip info.

On error -1 and the `errno` variable is set appropriately. Common error codes are described in [error-codes.rst](~kernel/userspace/userspace-api/gpio/error-codes).
