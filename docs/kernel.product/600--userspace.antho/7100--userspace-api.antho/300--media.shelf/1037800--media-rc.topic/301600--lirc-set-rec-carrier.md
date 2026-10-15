---
title: "ioctl LIRC_SET_REC_CARRIER"
type: reference
description: "LIRC_SET_REC_CARRIER - Set carrier used to modulate IR receive."
---

<a id="rst-ioctl-lirc-set-rec-carrier"></a>
<a id="rst-lirc-set-rec-carrier"></a>

<!-- SPDX-License-Identifier: GPL-2.0 OR GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: RC -->

<a id="rst-name"></a>

## Name

LIRC_SET_REC_CARRIER - Set carrier used to modulate IR receive.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-LIRC_SET_REC_CARRIER"></a>

```c
LIRC_SET_REC_CARRIER
```

`int ioctl(int fd, LIRC_SET_REC_CARRIER, __u32 *frequency)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by open().

- **`frequency`**

  Frequency of the carrier that modulates PWM data, in Hz.

<a id="rst-description"></a>

## Description

Set receive carrier used to modulate IR PWM pulses and spaces.

> [!NOTE]
>
> If called together with [ioctl LIRC_SET_REC_CARRIER_RANGE](<~kernel/userspace/userspace-api/media-rc/lirc-set-rec-carrier-range#rst-lirc-set-rec-carrier-range>), this ioctl sets the upper bound frequency that will be recognized by the device.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
