---
title: "ioctl LIRC_SET_REC_CARRIER_RANGE"
type: reference
description: "LIRC_SET_REC_CARRIER_RANGE - Set lower bound of the carrier used to modulate IR receive."
---

<a id="rst-ioctl-lirc-set-rec-carrier-range"></a>
<a id="rst-lirc-set-rec-carrier-range"></a>

<!-- SPDX-License-Identifier: GPL-2.0 OR GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: RC -->

<a id="rst-name"></a>

## Name

LIRC_SET_REC_CARRIER_RANGE - Set lower bound of the carrier used to modulate IR receive.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-LIRC_SET_REC_CARRIER_RANGE"></a>

```c
LIRC_SET_REC_CARRIER_RANGE
```

`int ioctl(int fd, LIRC_SET_REC_CARRIER_RANGE, __u32 *frequency)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by open().

- **`frequency`**

  Frequency of the carrier that modulates PWM data, in Hz.

<a id="rst-description"></a>

## Description

This ioctl sets the upper range of carrier frequency that will be recognized by the IR receiver.

> [!NOTE]
>
> To set a range use [LIRC_SET_REC_CARRIER_RANGE](<#rst-lirc-set-rec-carrier-range>) with the lower bound first and later call [LIRC_SET_REC_CARRIER](<~kernel/userspace/userspace-api/media-rc/lirc-set-rec-carrier#rst-lirc-set-rec-carrier>) with the upper bound.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
