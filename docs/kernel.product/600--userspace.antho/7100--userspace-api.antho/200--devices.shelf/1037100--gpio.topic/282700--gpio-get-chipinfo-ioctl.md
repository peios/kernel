---
title: "GPIO_GET_CHIPINFO_IOCTL"
type: reference
description: "Duplicate implicit target name: \"gpio_get_chipinfo_ioctl\"."
---

<a id="rst-gpio-get-chipinfo-ioctl-1"></a>
<a id="rst-gpio-get-chipinfo-ioctl"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-name"></a>

## Name

GPIO_GET_CHIPINFO_IOCTL - Get the publicly available information for a chip.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-GPIO_GET_CHIPINFO_IOCTL"></a>

```c
GPIO_GET_CHIPINFO_IOCTL
```

`int ioctl(int chip_fd, GPIO_GET_CHIPINFO_IOCTL, struct gpiochip_info *info)`

<a id="rst-arguments"></a>

## Arguments

- **`chip_fd`**

  The file descriptor of the GPIO character device returned by `open()`.

- **`info`**

  The `chip_info<gpiochip_info>` to be populated.

<a id="rst-description"></a>

## Description

Gets the publicly available information for a particular GPIO chip.

<a id="rst-return-value"></a>

## Return Value

On success 0 and `info` is populated with the chip info.

On error -1 and the `errno` variable is set appropriately. Common error codes are described in [error-codes.rst](~kernel/userspace/userspace-api/gpio/error-codes).
