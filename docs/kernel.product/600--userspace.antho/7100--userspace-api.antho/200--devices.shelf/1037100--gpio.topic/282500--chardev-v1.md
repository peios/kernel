---
title: "GPIO Character Device Userspace API (v1)"
type: reference
description: "First added in 4.8."
---

<a id="rst-gpio-character-device-userspace-api-v1"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

> [!WARNING]
>
> This API is obsoleted by [chardev.rst](~kernel/userspace/userspace-api/gpio/chardev) (v2).
>
> New developments should use the v2 API, and existing developments are encouraged to migrate as soon as possible, as this API will be removed in the future. The v2 API is a functional superset of the v1 API so any v1 call can be directly translated to a v2 equivalent.
>
> This interface will continue to be maintained for the migration period, but new features will only be added to the new API.

First added in 4.8.

The API is based around three major objects, the [Chip](<#rst-gpio-v1-chip>), the [Line Handle](<#rst-gpio-v1-line-handle>), and the [Line Event](<#rst-gpio-v1-line-event>).

Where "line event" is used in this document it refers to the request that can monitor a line for edge events, not the edge events themselves.

<a id="rst-chip"></a>
<a id="rst-gpio-v1-chip"></a>

## Chip

The Chip represents a single GPIO chip and is exposed to userspace using device files of the form `/dev/gpiochipX`.

Each chip supports a number of GPIO lines, `chip.lines<gpiochip_info>`. Lines on the chip are identified by an `offset` in the range from 0 to `chip.lines - 1`, i.e. `[0,chip.lines)`.

Lines are requested from the chip using either [gpio-get-linehandle-ioctl.rst](~kernel/userspace/userspace-api/gpio/gpio-get-linehandle-ioctl) and the resulting line handle is used to access the GPIO chip's lines, or [gpio-get-lineevent-ioctl.rst](~kernel/userspace/userspace-api/gpio/gpio-get-lineevent-ioctl) and the resulting line event is used to monitor a GPIO line for edge events.

Within this documentation, the file descriptor returned by calling `open()` on the GPIO device file is referred to as `chip_fd`.

<a id="rst-operations"></a>

### Operations

The following operations may be performed on the chip:

- [Get Line Handle](<~kernel/userspace/userspace-api/gpio/gpio-get-linehandle-ioctl>)
- [Get Line Event](<~kernel/userspace/userspace-api/gpio/gpio-get-lineevent-ioctl>)
- [Get Chip Info](<~kernel/userspace/userspace-api/gpio/gpio-get-chipinfo-ioctl>)
- [Get Line Info](<~kernel/userspace/userspace-api/gpio/gpio-get-lineinfo-ioctl>)
- [Watch Line Info](<~kernel/userspace/userspace-api/gpio/gpio-get-lineinfo-watch-ioctl>)
- [Unwatch Line Info](<~kernel/userspace/userspace-api/gpio/gpio-get-lineinfo-unwatch-ioctl>)
- [Read Line Info Changed Events](<~kernel/userspace/userspace-api/gpio/gpio-lineinfo-changed-read>)

<a id="rst-line-handle"></a>
<a id="rst-gpio-v1-line-handle"></a>

## Line Handle

Line handles are created by [gpio-get-linehandle-ioctl.rst](~kernel/userspace/userspace-api/gpio/gpio-get-linehandle-ioctl) and provide access to a set of requested lines.  The line handle is exposed to userspace via the anonymous file descriptor returned  in `request.fd<gpiohandle_request>` by [gpio-get-linehandle-ioctl.rst](~kernel/userspace/userspace-api/gpio/gpio-get-linehandle-ioctl).

Within this documentation, the line handle file descriptor is referred to as `handle_fd`.

<a id="rst-operations-1"></a>

### Operations

The following operations may be performed on the line handle:

- [Get Line Values](<~kernel/userspace/userspace-api/gpio/gpio-handle-get-line-values-ioctl>)
- [Set Line Values](<~kernel/userspace/userspace-api/gpio/gpio-handle-set-line-values-ioctl>)
- [Reconfigure Lines](<~kernel/userspace/userspace-api/gpio/gpio-handle-set-config-ioctl>)

<a id="rst-line-event"></a>
<a id="rst-gpio-v1-line-event"></a>

## Line Event

Line events are created by [gpio-get-lineevent-ioctl.rst](~kernel/userspace/userspace-api/gpio/gpio-get-lineevent-ioctl) and provide access to a requested line.  The line event is exposed to userspace via the anonymous file descriptor returned  in `request.fd<gpioevent_request>` by [gpio-get-lineevent-ioctl.rst](~kernel/userspace/userspace-api/gpio/gpio-get-lineevent-ioctl).

Within this documentation, the line event file descriptor is referred to as `event_fd`.

<a id="rst-operations-2"></a>

### Operations

The following operations may be performed on the line event:

- [Get Line Value](<~kernel/userspace/userspace-api/gpio/gpio-handle-get-line-values-ioctl>)
- [Read Line Edge Events](<~kernel/userspace/userspace-api/gpio/gpio-lineevent-data-read>)

<a id="rst-types"></a>

## Types

This section contains the structs that are referenced by the ABI v1.

The `struct gpiochip_info<gpiochip_info>` is common to ABI v1 and v2.

```{kernel-doc} include/uapi/linux/gpio.h
:identifiers: gpioevent_data gpioevent_request gpiohandle_config gpiohandle_data gpiohandle_request gpioline_info gpioline_info_changed
```

- [GPIO Error Codes](<~kernel/userspace/userspace-api/gpio/error-codes>)
