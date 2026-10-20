---
title: "GPIO_GET_LINEINFO_WATCH_IOCTL"
type: reference
description: "Duplicate implicit target name: \"gpio_get_lineinfo_watch_ioctl\"."
---

<a id="rst-gpio-get-lineinfo-watch-ioctl-1"></a>
<a id="rst-gpio-get-lineinfo-watch-ioctl"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

> [!WARNING]
>
> This ioctl is part of [chardev_v1.rst](~kernel/userspace/userspace-api/gpio/chardev-v1) and is obsoleted by [gpio-v2-get-lineinfo-watch-ioctl.rst](~kernel/userspace/userspace-api/gpio/gpio-v2-get-lineinfo-watch-ioctl).

<a id="rst-name"></a>

## Name

GPIO_GET_LINEINFO_WATCH_IOCTL - Enable watching a line for changes to its request state and configuration information.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-GPIO_GET_LINEINFO_WATCH_IOCTL"></a>

```c
GPIO_GET_LINEINFO_WATCH_IOCTL
```

`int ioctl(int chip_fd, GPIO_GET_LINEINFO_WATCH_IOCTL, struct gpioline_info *info)`

<a id="rst-arguments"></a>

## Arguments

- **`chip_fd`**

  The file descriptor of the GPIO character device returned by `open()`.

- **`info`**

  The `line_info<gpioline_info>` struct to be populated, with the `offset` set to indicate the line to watch

<a id="rst-description"></a>

## Description

Enable watching a line for changes to its request state and configuration information. Changes to line info include a line being requested, released or reconfigured.

> [!NOTE]
>
> Watching line info is not generally required, and would typically only be used by a system monitoring component.
>
> The line info does NOT include the line value.
>
> The line must be requested using [gpio-get-linehandle-ioctl.rst](~kernel/userspace/userspace-api/gpio/gpio-get-linehandle-ioctl) or [gpio-get-lineevent-ioctl.rst](~kernel/userspace/userspace-api/gpio/gpio-get-lineevent-ioctl) to access its value, and the line event can monitor a line for events using [gpio-lineevent-data-read.rst](~kernel/userspace/userspace-api/gpio/gpio-lineevent-data-read).

By default all lines are unwatched when the GPIO chip is opened.

Multiple lines may be watched simultaneously by adding a watch for each.

Once a watch is set, any changes to line info will generate events which can be read from the `chip_fd` as described in [gpio-lineinfo-changed-read.rst](~kernel/userspace/userspace-api/gpio/gpio-lineinfo-changed-read).

Adding a watch to a line that is already watched is an error (**EBUSY**).

Watches are specific to the `chip_fd` and are independent of watches on the same GPIO chip opened with a separate call to `open()`.

First added in 5.7.

<a id="rst-return-value"></a>

## Return Value

On success 0 and `info` is populated with the current line info.

On error -1 and the `errno` variable is set appropriately. Common error codes are described in [error-codes.rst](~kernel/userspace/userspace-api/gpio/error-codes).
