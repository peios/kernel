---
title: "FE_GET_FRONTEND"
type: reference
description: "Duplicate implicit target name: \"fe_get_frontend\"."
---

<a id="rst-fe-get-frontend-1"></a>
<a id="rst-fe-get-frontend"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.fe -->

<a id="rst-name"></a>

## Name

FE_GET_FRONTEND

> [!NOTE]
>
> This ioctl is deprecated.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-FE_GET_FRONTEND"></a>

```c
FE_GET_FRONTEND
```

`int ioctl(int fd, FE_GET_FRONTEND, struct dvb_frontend_parameters *p)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`p`**

  Points to parameters for tuning operation.

<a id="rst-description"></a>

## Description

This ioctl call queries the currently effective frontend parameters. For this command, read-only access to the device is sufficient.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned.

On error -1 is returned, and the `errno` variable is set appropriately.


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
