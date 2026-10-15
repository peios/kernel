---
title: "GPIO_GET_LINEINFO_UNWATCH_IOCTL"
type: reference
description: "Duplicate implicit target name: \"gpio_get_lineinfo_unwatch_ioctl\"."
---

<a id="rst-gpio-get-lineinfo-unwatch-ioctl-1"></a>
<a id="rst-gpio-get-lineinfo-unwatch-ioctl"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-name"></a>

## Name

GPIO_GET_LINEINFO_UNWATCH_IOCTL - Disable watching a line for changes to its requested state and configuration information.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-GPIO_GET_LINEINFO_UNWATCH_IOCTL"></a>

```c
GPIO_GET_LINEINFO_UNWATCH_IOCTL
```

`int ioctl(int chip_fd, GPIO_GET_LINEINFO_UNWATCH_IOCTL, u32 *offset)`

<a id="rst-arguments"></a>

## Arguments

- **`chip_fd`**

  The file descriptor of the GPIO character device returned by `open()`.

- **`offset`**

  The offset of the line to no longer watch.

<a id="rst-description"></a>

## Description

Remove the line from the list of lines being watched on this `chip_fd`.

This is the reverse of [gpio-v2-get-lineinfo-watch-ioctl.rst](~kernel/userspace/userspace-api/gpio/gpio-v2-get-lineinfo-watch-ioctl) (v2) and [gpio-get-lineinfo-watch-ioctl.rst](~kernel/userspace/userspace-api/gpio/gpio-get-lineinfo-watch-ioctl) (v1).

Unwatching a line that is not watched is an error (**EBUSY**).

First added in 5.7.

<a id="rst-return-value"></a>

## Return Value

On success 0.

On error -1 and the `errno` variable is set appropriately. Common error codes are described in [error-codes.rst](~kernel/userspace/userspace-api/gpio/error-codes).
