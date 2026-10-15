---
title: "DMX_STOP"
type: reference
description: "Duplicate implicit target name: \"dmx_stop\"."
---

<a id="rst-dmx-stop-1"></a>
<a id="rst-dmx-stop"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.dmx -->

<a id="rst-name"></a>

## Name

DMX_STOP

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-DMX_STOP"></a>

```c
DMX_STOP
```

`int ioctl(int fd, DMX_STOP)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

<a id="rst-description"></a>

## Description

This ioctl call is used to stop the actual filtering operation defined via the ioctl calls [DMX_SET_FILTER](<~kernel/userspace/userspace-api/media-dvb/dmx-set-filter#rst-dmx-set-filter-1>) or [DMX_SET_PES_FILTER](<~kernel/userspace/userspace-api/media-dvb/dmx-set-pes-filter#rst-dmx-set-pes-filter-1>) and started via the [DMX_START](<~kernel/userspace/userspace-api/media-dvb/dmx-start#rst-dmx-start-1>) command.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned.

On error -1 is returned, and the `errno` variable is set appropriately.

The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
