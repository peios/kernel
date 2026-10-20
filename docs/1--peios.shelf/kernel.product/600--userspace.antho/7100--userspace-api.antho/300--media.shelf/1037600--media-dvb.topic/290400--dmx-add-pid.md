---
title: "DMX_ADD_PID"
type: reference
description: "Duplicate implicit target name: \"dmx_add_pid\"."
---

<a id="rst-dmx-add-pid-1"></a>
<a id="rst-dmx-add-pid"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.dmx -->

<a id="rst-name"></a>

## Name

DMX_ADD_PID

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-DMX_ADD_PID"></a>

```c
DMX_ADD_PID
```

`int ioctl(fd, DMX_ADD_PID, __u16 *pid)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`pid`**

  PID number to be filtered.

<a id="rst-description"></a>

## Description

This ioctl call allows to add multiple PIDs to a transport stream filter previously set up with [DMX_SET_PES_FILTER](<~kernel/userspace/userspace-api/media-dvb/dmx-set-pes-filter#rst-dmx-set-pes-filter-1>) and output equal to `DMX_OUT_TSDEMUX_TAP <dmx_output>`.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned.

On error -1 is returned, and the `errno` variable is set appropriately.

Generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
