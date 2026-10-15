---
title: "ioctl LIRC_GET_FEATURES"
type: reference
description: "LIRC_GET_FEATURES - Get the underlying hardware device's features"
---

<a id="rst-ioctl-lirc-get-features"></a>
<a id="rst-lirc-get-features"></a>

<!-- SPDX-License-Identifier: GPL-2.0 OR GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: RC -->

<a id="rst-name"></a>

## Name

LIRC_GET_FEATURES - Get the underlying hardware device's features

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-LIRC_GET_FEATURES"></a>

```c
LIRC_GET_FEATURES
```

`int ioctl(int fd, LIRC_GET_FEATURES, __u32 *features)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by open().

- **`features`**

  Bitmask with the LIRC features.

<a id="rst-description"></a>

## Description

Get the underlying hardware device's features. If a driver does not announce support of certain features, calling of the corresponding ioctls is undefined.

<a id="rst-lirc-features"></a>

## LIRC features

<a id="rst-lirc-can-rec-raw"></a>

`LIRC_CAN_REC_RAW`

> Unused. Kept just to avoid breaking uAPI.

<a id="rst-lirc-can-rec-pulse"></a>

`LIRC_CAN_REC_PULSE`

> Unused. Kept just to avoid breaking uAPI. [LIRC_MODE_PULSE](<~kernel/userspace/userspace-api/media-rc/lirc-dev-intro#rst-lirc-mode-pulse>) can only be used for transmitting.

<a id="rst-lirc-can-rec-mode2"></a>

`LIRC_CAN_REC_MODE2`

> This is raw IR driver for receiving. This means that [LIRC_MODE_MODE2](<~kernel/userspace/userspace-api/media-rc/lirc-dev-intro#rst-lirc-mode-mode2>) is used. This also implies that [LIRC_MODE_SCANCODE](<~kernel/userspace/userspace-api/media-rc/lirc-dev-intro#rst-lirc-mode-scancode>) is also supported, as long as the kernel is recent enough. Use the [ioctls LIRC_GET_REC_MODE and LIRC_SET_REC_MODE](<~kernel/userspace/userspace-api/media-rc/lirc-get-rec-mode#rst-lirc-set-rec-mode>) to switch modes.

<a id="rst-lirc-can-rec-lirccode"></a>

`LIRC_CAN_REC_LIRCCODE`

> Unused. Kept just to avoid breaking uAPI.

<a id="rst-lirc-can-rec-scancode"></a>

`LIRC_CAN_REC_SCANCODE`

> This is a scancode driver for receiving. This means that [LIRC_MODE_SCANCODE](<~kernel/userspace/userspace-api/media-rc/lirc-dev-intro#rst-lirc-mode-scancode>) is used.

<a id="rst-lirc-can-set-send-carrier"></a>

`LIRC_CAN_SET_SEND_CARRIER`

> The driver supports changing the modulation frequency via [ioctl LIRC_SET_SEND_CARRIER](<~kernel/userspace/userspace-api/media-rc/lirc-set-send-carrier#rst-lirc-set-send-carrier>).

<a id="rst-lirc-can-set-send-duty-cycle"></a>

`LIRC_CAN_SET_SEND_DUTY_CYCLE`

> The driver supports changing the duty cycle using [ioctl LIRC_SET_SEND_DUTY_CYCLE](<~kernel/userspace/userspace-api/media-rc/lirc-set-send-duty-cycle#rst-lirc-set-send-duty-cycle>).

<a id="rst-lirc-can-set-transmitter-mask"></a>

`LIRC_CAN_SET_TRANSMITTER_MASK`

> The driver supports changing the active transmitter(s) using [ioctl LIRC_SET_TRANSMITTER_MASK](<~kernel/userspace/userspace-api/media-rc/lirc-set-transmitter-mask#rst-lirc-set-transmitter-mask>).

<a id="rst-lirc-can-set-rec-carrier"></a>

`LIRC_CAN_SET_REC_CARRIER`

> The driver supports setting the receive carrier frequency using [ioctl LIRC_SET_REC_CARRIER](<~kernel/userspace/userspace-api/media-rc/lirc-set-rec-carrier#rst-lirc-set-rec-carrier>).

<a id="rst-lirc-can-set-rec-carrier-range"></a>

`LIRC_CAN_SET_REC_CARRIER_RANGE`

> The driver supports [ioctl LIRC_SET_REC_CARRIER_RANGE](<~kernel/userspace/userspace-api/media-rc/lirc-set-rec-carrier-range#rst-lirc-set-rec-carrier-range>).

<a id="rst-lirc-can-get-rec-resolution"></a>

`LIRC_CAN_GET_REC_RESOLUTION`

> The driver supports [ioctl LIRC_GET_REC_RESOLUTION](<~kernel/userspace/userspace-api/media-rc/lirc-get-rec-resolution#rst-lirc-get-rec-resolution>).

<a id="rst-lirc-can-set-rec-timeout"></a>

`LIRC_CAN_SET_REC_TIMEOUT`

> The driver supports [ioctl LIRC_SET_REC_TIMEOUT](<~kernel/userspace/userspace-api/media-rc/lirc-set-rec-timeout#rst-lirc-set-rec-timeout>).

<a id="rst-lirc-can-measure-carrier"></a>

`LIRC_CAN_MEASURE_CARRIER`

> The driver supports measuring of the modulation frequency using [ioctl LIRC_SET_MEASURE_CARRIER_MODE](<~kernel/userspace/userspace-api/media-rc/lirc-set-measure-carrier-mode#rst-lirc-set-measure-carrier-mode>).

<a id="rst-lirc-can-use-wideband-receiver"></a>

`LIRC_CAN_USE_WIDEBAND_RECEIVER`

> The driver supports learning mode using [ioctl LIRC_SET_WIDEBAND_RECEIVER](<~kernel/userspace/userspace-api/media-rc/lirc-set-wideband-receiver#rst-lirc-set-wideband-receiver>).

<a id="rst-lirc-can-send-raw"></a>

`LIRC_CAN_SEND_RAW`

> Unused. Kept just to avoid breaking uAPI.

<a id="rst-lirc-can-send-pulse"></a>

`LIRC_CAN_SEND_PULSE`

> The driver supports sending (also called as IR blasting or IR TX) using [LIRC_MODE_PULSE](<~kernel/userspace/userspace-api/media-rc/lirc-dev-intro#rst-lirc-mode-pulse>). This implies that [LIRC_MODE_SCANCODE](<~kernel/userspace/userspace-api/media-rc/lirc-dev-intro#rst-lirc-mode-scancode>) is also supported for transmit, as long as the kernel is recent enough. Use the [ioctls LIRC_GET_SEND_MODE and LIRC_SET_SEND_MODE](<~kernel/userspace/userspace-api/media-rc/lirc-get-send-mode#rst-lirc-set-send-mode>) to switch modes.

<a id="rst-lirc-can-send-mode2"></a>

`LIRC_CAN_SEND_MODE2`

> Unused. Kept just to avoid breaking uAPI. [LIRC_MODE_MODE2](<~kernel/userspace/userspace-api/media-rc/lirc-dev-intro#rst-lirc-mode-mode2>) can only be used for receiving.

<a id="rst-lirc-can-send-lirccode"></a>

`LIRC_CAN_SEND_LIRCCODE`

> Unused. Kept just to avoid breaking uAPI.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
