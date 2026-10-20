---
title: "ioctl LIRC_SET_TRANSMITTER_MASK"
type: reference
description: "LIRC_SET_TRANSMITTER_MASK - Enables send codes on a given set of transmitters"
---

<a id="rst-ioctl-lirc-set-transmitter-mask"></a>
<a id="rst-lirc-set-transmitter-mask"></a>

<!-- SPDX-License-Identifier: GPL-2.0 OR GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: RC -->

<a id="rst-name"></a>

## Name

LIRC_SET_TRANSMITTER_MASK - Enables send codes on a given set of transmitters

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-LIRC_SET_TRANSMITTER_MASK"></a>

```c
LIRC_SET_TRANSMITTER_MASK
```

`int ioctl(int fd, LIRC_SET_TRANSMITTER_MASK, __u32 *mask)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by open().

- **`mask`**

  Mask with channels to enable tx. Channel 0 is the least significant bit.

<a id="rst-description"></a>

## Description

Some IR TX devices have multiple output channels, in such case, [LIRC_CAN_SET_TRANSMITTER_MASK](<~kernel/userspace/userspace-api/media-rc/lirc-get-features#rst-lirc-can-set-transmitter-mask>) is returned via [ioctl LIRC_GET_FEATURES](<~kernel/userspace/userspace-api/media-rc/lirc-get-features#rst-lirc-get-features>) and this ioctl sets what channels will send IR codes.

This ioctl enables the given set of transmitters. The first transmitter is encoded by the least significant bit and so on.

When an invalid bit mask is given, i.e. a bit is set, even though the device does not have so many transitters, then this ioctl returns the number of available transitters and does nothing otherwise.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
