---
title: "ioctl LIRC_SET_SEND_CARRIER"
type: reference
description: "LIRC_SET_SEND_CARRIER - Set send carrier used to modulate IR TX."
---

<a id="rst-ioctl-lirc-set-send-carrier"></a>
<a id="rst-lirc-set-send-carrier"></a>

<!-- SPDX-License-Identifier: GPL-2.0 OR GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: RC -->

<a id="rst-name"></a>

## Name

LIRC_SET_SEND_CARRIER - Set send carrier used to modulate IR TX.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-LIRC_SET_SEND_CARRIER"></a>

```c
LIRC_SET_SEND_CARRIER
```

`int ioctl(int fd, LIRC_SET_SEND_CARRIER, __u32 *frequency)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by open().

- **`frequency`**

  Frequency of the carrier to be modulated, in Hz.

<a id="rst-description"></a>

## Description

Set send carrier used to modulate IR PWM pulses and spaces.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
