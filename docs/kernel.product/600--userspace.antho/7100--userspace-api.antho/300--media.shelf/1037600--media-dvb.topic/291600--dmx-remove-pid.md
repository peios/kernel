---
title: "DMX_REMOVE_PID"
type: reference
description: "Duplicate implicit target name: \"dmx_remove_pid\"."
---

<a id="rst-dmx-remove-pid-1"></a>
<a id="rst-dmx-remove-pid"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.dmx -->

<a id="rst-name"></a>

## Name

DMX_REMOVE_PID

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-DMX_REMOVE_PID"></a>

```c
DMX_REMOVE_PID
```

`int ioctl(fd, DMX_REMOVE_PID, __u16 *pid)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`pid`**

  PID of the PES filter to be removed.

<a id="rst-description"></a>

## Description

This ioctl call allows to remove a PID when multiple PIDs are set on a transport stream filter, e. g. a filter previously set up with output equal to `DMX_OUT_TSDEMUX_TAP <dmx_output>`, created via either [DMX_SET_PES_FILTER](<~kernel/userspace/userspace-api/media-dvb/dmx-set-pes-filter#rst-dmx-set-pes-filter-1>) or [DMX_ADD_PID](<~kernel/userspace/userspace-api/media-dvb/dmx-add-pid#rst-dmx-add-pid-1>).

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned.

On error -1 is returned, and the `errno` variable is set appropriately.

The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
