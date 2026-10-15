---
title: "ioctl LIRC_SET_MEASURE_CARRIER_MODE"
type: reference
description: "LIRC_SET_MEASURE_CARRIER_MODE - enable or disable measure mode"
---

<a id="rst-ioctl-lirc-set-measure-carrier-mode"></a>
<a id="rst-lirc-set-measure-carrier-mode"></a>

<!-- SPDX-License-Identifier: GPL-2.0 OR GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: RC -->

<a id="rst-name"></a>

## Name

LIRC_SET_MEASURE_CARRIER_MODE - enable or disable measure mode

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-LIRC_SET_MEASURE_CARRIER_MODE"></a>

```c
LIRC_SET_MEASURE_CARRIER_MODE
```

`int ioctl(int fd, LIRC_SET_MEASURE_CARRIER_MODE, __u32 *enable)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by open().

- **`enable`**

  enable = 1 means enable measure mode, enable = 0 means disable measure mode.

<a id="rst-description"></a>

## Description

<a id="rst-lirc-mode2-frequency"></a>

Enable or disable measure mode. If enabled, from the next key press on, the driver will send `LIRC_MODE2_FREQUENCY` packets. By default this should be turned off.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
