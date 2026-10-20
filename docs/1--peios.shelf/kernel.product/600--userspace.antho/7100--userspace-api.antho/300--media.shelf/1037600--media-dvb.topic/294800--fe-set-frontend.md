---
title: "FE_SET_FRONTEND"
type: reference
description: "Duplicate implicit target name: \"fe_set_frontend\"."
---

<a id="rst-fe-set-frontend-1"></a>
<a id="rst-fe-set-frontend"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.fe -->

> [!NOTE]
>
> This ioctl is deprecated.

<a id="rst-name"></a>

## Name

FE_SET_FRONTEND

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-FE_SET_FRONTEND"></a>

```c
FE_SET_FRONTEND
```

`int ioctl(int fd, FE_SET_FRONTEND, struct dvb_frontend_parameters *p)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`p`**

  Points to parameters for tuning operation.

<a id="rst-description"></a>

## Description

This ioctl call starts a tuning operation using specified parameters. The result of this call will be successful if the parameters were valid and the tuning could be initiated. The result of the tuning operation in itself, however, will arrive asynchronously as an event (see documentation for [FE_GET_EVENT](<~kernel/userspace/userspace-api/media-dvb/fe-get-event#rst-fe-get-event-1>) and FrontendEvent.) If a new [FE_SET_FRONTEND](<#rst-fe-set-frontend-1>) operation is initiated before the previous one was completed, the previous operation will be aborted in favor of the new one. This command requires read/write access to the device.

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


Maximum supported symbol rate reached.

</td>
</tr>
</tbody>
</table>

Generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
