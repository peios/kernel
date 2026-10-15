---
title: "GPIO_V2_GET_LINEINFO_IOCTL"
type: reference
description: "Duplicate implicit target name: \"gpio_v2_get_lineinfo_ioctl\"."
---

<a id="rst-gpio-v2-get-lineinfo-ioctl-1"></a>
<a id="rst-gpio-v2-get-lineinfo-ioctl"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-name"></a>

## Name

GPIO_V2_GET_LINEINFO_IOCTL - Get the publicly available information for a line.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-GPIO_V2_GET_LINEINFO_IOCTL"></a>

```c
GPIO_V2_GET_LINEINFO_IOCTL
```

`int ioctl(int chip_fd, GPIO_V2_GET_LINEINFO_IOCTL, struct gpio_v2_line_info *info)`

<a id="rst-arguments"></a>

## Arguments

- **`chip_fd`**

  The file descriptor of the GPIO character device returned by `open()`.

- **`info`**

  The `line_info<gpio_v2_line_info>` to be populated, with the `offset` field set to indicate the line to be collected.

<a id="rst-description"></a>

## Description

Get the publicly available information for a line.

This information is available independent of whether the line is in use.

> [!NOTE]
>
> The line info does not include the line value.
>
> The line must be requested using [gpio-v2-get-line-ioctl.rst](~kernel/userspace/userspace-api/gpio/gpio-v2-get-line-ioctl) to access its value.

<a id="rst-return-value"></a>

## Return Value

On success 0 and `info` is populated with the chip info.

On error -1 and the `errno` variable is set appropriately. Common error codes are described in [error-codes.rst](~kernel/userspace/userspace-api/gpio/error-codes).
