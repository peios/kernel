---
title: "DMX_GET_STC"
type: reference
description: "Duplicate implicit target name: \"dmx_get_stc\"."
---

<a id="rst-dmx-get-stc-1"></a>
<a id="rst-dmx-get-stc"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.dmx -->

<a id="rst-name"></a>

## Name

DMX_GET_STC

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-DMX_GET_STC"></a>

```c
DMX_GET_STC
```

`int ioctl(int fd, DMX_GET_STC, struct dmx_stc *stc)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`stc`**

  Pointer to `dmx_stc` where the stc data is to be stored.

<a id="rst-description"></a>

## Description

This ioctl call returns the current value of the system time counter (which is driven by a PES filter of type `DMX_PES_PCR <dmx_ts_pes>`). Some hardware supports more than one STC, so you must specify which one by setting the `num <dmx_stc>` field of stc before the ioctl (range 0...n). The result is returned in form of a ratio with a 64 bit numerator and a 32 bit denominator, so the real 90kHz STC value is `stc->stc / stc->base`.

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


Invalid stc number.

</td>
</tr>
</tbody>
</table>

The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
