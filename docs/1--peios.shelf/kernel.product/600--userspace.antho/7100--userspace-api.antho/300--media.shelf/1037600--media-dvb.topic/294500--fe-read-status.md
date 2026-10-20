---
title: "ioctl FE_READ_STATUS"
type: reference
description: "FE_READ_STATUS - Returns status information about the front-end. This call only requires - read-only access to the device"
---

<a id="rst-ioctl-fe-read-status"></a>
<a id="rst-fe-read-status"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.fe -->

<a id="rst-name"></a>

## Name

FE_READ_STATUS - Returns status information about the front-end. This call only requires - read-only access to the device

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-FE_READ_STATUS"></a>

```c
FE_READ_STATUS
```

`int ioctl(int fd, FE_READ_STATUS, unsigned int *status)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`status`**

  pointer to a bitmask integer filled with the values defined by enum `fe_status`.

<a id="rst-description"></a>

## Description

All Digital TV frontend devices support the `FE_READ_STATUS` ioctl. It is used to check about the locking status of the frontend after being tuned. The ioctl takes a pointer to an integer where the status will be written.

> [!NOTE]
>
> The size of status is actually sizeof(enum fe_status), with varies according with the architecture. This needs to be fixed in the future.

<a id="rst-int-fe-status"></a>

## int fe_status

The fe_status parameter is used to indicate the current state and/or state changes of the frontend hardware. It is produced using the enum `fe_status` values on a bitmask

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned.

On error -1 is returned, and the `errno` variable is set appropriately.

Generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
