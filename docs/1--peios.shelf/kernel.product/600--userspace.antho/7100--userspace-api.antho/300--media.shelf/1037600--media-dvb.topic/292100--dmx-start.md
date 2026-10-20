---
title: "DMX_START"
type: reference
description: "Duplicate implicit target name: \"dmx_start\"."
---

<a id="rst-dmx-start-1"></a>
<a id="rst-dmx-start"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.dmx -->

<a id="rst-name"></a>

## Name

DMX_START

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-DMX_START"></a>

```c
DMX_START
```

`int ioctl(int fd, DMX_START)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

<a id="rst-description"></a>

## Description

This ioctl call is used to start the actual filtering operation defined via the ioctl calls [DMX_SET_FILTER](<~kernel/userspace/userspace-api/media-dvb/dmx-set-filter#rst-dmx-set-filter-1>) or [DMX_SET_PES_FILTER](<~kernel/userspace/userspace-api/media-dvb/dmx-set-pes-filter#rst-dmx-set-pes-filter-1>).

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned.

On error -1 is returned, and the `errno` variable is set appropriately.

<!-- tabularcolumns: |p{2.5cm}|p{15.0cm}| -->


<table>
<tbody>
<tr>
<td>


`EINVAL`

</td>
<td>


Invalid argument, i.e. no filtering parameters provided via the [DMX_SET_FILTER](<~kernel/userspace/userspace-api/media-dvb/dmx-set-filter#rst-dmx-set-filter-1>) or [DMX_SET_PES_FILTER](<~kernel/userspace/userspace-api/media-dvb/dmx-set-pes-filter#rst-dmx-set-pes-filter-1>) ioctls.

</td>
</tr>
<tr>
<td>


`EBUSY`

</td>
<td>


This error code indicates that there are conflicting requests. There are active filters filtering data from another input source. Make sure that these filters are stopped before starting this filter.

</td>
</tr>
</tbody>
</table>

The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
