---
title: "FE_GET_EVENT"
type: reference
description: "Duplicate implicit target name: \"fe_get_event\"."
---

<a id="rst-fe-get-event-1"></a>
<a id="rst-fe-get-event"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.fe -->

<a id="rst-name"></a>

## Name

FE_GET_EVENT

> [!NOTE]
>
> This ioctl is deprecated.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-FE_GET_EVENT"></a>

```c
FE_GET_EVENT
```

`int ioctl(int fd, FE_GET_EVENT, struct dvb_frontend_event *ev)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`ev`**

  Points to the location where the event, if any, is to be stored.

<a id="rst-description"></a>

## Description

This ioctl call returns a frontend event if available. If an event is not available, the behavior depends on whether the device is in blocking or non-blocking mode. In the latter case, the call fails immediately with errno set to `EWOULDBLOCK`. In the former case, the call blocks until an event becomes available.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned.

On error -1 is returned, and the `errno` variable is set appropriately.


<table>
<tbody>
<tr>
<td>


`EWOULDBLOCK`

</td>
<td>


There is no event pending, and the device is in non-blocking mode.

</td>
</tr>
<tr>
<td>


`EOVERFLOW`

</td>
<td>


Overflow in event queue - one or more events were lost.

</td>
</tr>
</tbody>
</table>

Generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
