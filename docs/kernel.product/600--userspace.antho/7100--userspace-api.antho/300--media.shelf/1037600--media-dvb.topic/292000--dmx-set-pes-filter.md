---
title: "DMX_SET_PES_FILTER"
type: reference
description: "Duplicate implicit target name: \"dmx_set_pes_filter\"."
---

<a id="rst-dmx-set-pes-filter-1"></a>
<a id="rst-dmx-set-pes-filter"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.dmx -->

<a id="rst-name"></a>

## Name

DMX_SET_PES_FILTER

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-DMX_SET_PES_FILTER"></a>

```c
DMX_SET_PES_FILTER
```

`int ioctl(int fd, DMX_SET_PES_FILTER, struct dmx_pes_filter_params *params)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`params`**

  Pointer to structure containing filter parameters.

<a id="rst-description"></a>

## Description

This ioctl call sets up a PES filter according to the parameters provided. By a PES filter is meant a filter that is based just on the packet identifier (PID), i.e. no PES header or payload filtering capability is supported.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned.

On error -1 is returned, and the `errno` variable is set appropriately.

<!-- tabularcolumns: |p{2.5cm}|p{15.0cm}| -->


<table>
<tbody>
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
