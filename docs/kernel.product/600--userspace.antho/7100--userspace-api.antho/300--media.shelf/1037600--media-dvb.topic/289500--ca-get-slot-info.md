---
title: "CA_GET_SLOT_INFO"
type: reference
description: "Duplicate implicit target name: \"ca_get_slot_info\"."
---

<a id="rst-ca-get-slot-info-1"></a>
<a id="rst-ca-get-slot-info"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.ca -->

<a id="rst-name"></a>

## Name

CA_GET_SLOT_INFO

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-CA_GET_SLOT_INFO"></a>

```c
CA_GET_SLOT_INFO
```

`int ioctl(fd, CA_GET_SLOT_INFO, struct ca_slot_info *info)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by a previous call to `open()`.

- **`info`**

  Pointer to struct `ca_slot_info`.

<a id="rst-description"></a>

## Description

Returns information about a CA slot identified by `ca_slot_info`.slot_num.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, and `ca_slot_info` is filled.

On error -1 is returned, and the `errno` variable is set appropriately.

<!-- tabularcolumns: |p{2.5cm}|p{15.0cm}| -->


<table>
<tbody>
<tr>
<td>


`ENODEV`

</td>
<td>


the slot is not available.

</td>
</tr>
</tbody>
</table>

The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
