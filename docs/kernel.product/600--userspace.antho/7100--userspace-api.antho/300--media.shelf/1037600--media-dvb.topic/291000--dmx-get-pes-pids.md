---
title: "DMX_GET_PES_PIDS"
type: reference
description: "Duplicate implicit target name: \"dmx_get_pes_pids\"."
---

<a id="rst-dmx-get-pes-pids-1"></a>
<a id="rst-dmx-get-pes-pids"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.dmx -->

<a id="rst-name"></a>

## Name

DMX_GET_PES_PIDS

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-DMX_GET_PES_PIDS"></a>

```c
DMX_GET_PES_PIDS
```

`int ioctl(fd, DMX_GET_PES_PIDS, __u16 pids[5])`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`pids`**

  Array used to store 5 Program IDs.

<a id="rst-description"></a>

## Description

This ioctl allows to query a DVB device to return the first PID used by audio, video, textext, subtitle and PCR programs on a given service. They're stored as:


<table>
<thead>
<tr>
<th>


PID  element

</th>
<th>


position

</th>
<th>


content

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


pids\[DMX_PES_AUDIO\]

</td>
<td>


0

</td>
<td>


first audio PID

</td>
</tr>
<tr>
<td>


pids\[DMX_PES_VIDEO\]

</td>
<td>


1

</td>
<td>


first video PID

</td>
</tr>
<tr>
<td>


pids\[DMX_PES_TELETEXT\]

</td>
<td>


2

</td>
<td>


first teletext PID

</td>
</tr>
<tr>
<td>


pids\[DMX_PES_SUBTITLE\]

</td>
<td>


3

</td>
<td>


first subtitle PID

</td>
</tr>
<tr>
<td>


pids\[DMX_PES_PCR\]

</td>
<td>


4

</td>
<td>


first Program Clock Reference PID

</td>
</tr>
</tbody>
</table>

> [!NOTE]
>
> A value equal to 0xffff means that the PID was not filled by the Kernel.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned.

On error -1 is returned, and the `errno` variable is set appropriately.

The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
