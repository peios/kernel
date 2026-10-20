---
title: "ioctl FE_GET_INFO"
type: reference
description: "FE_GET_INFO - Query Digital TV frontend capabilities and returns information about the - front-end. This call only requires read-only access to the device."
---

<a id="rst-ioctl-fe-get-info"></a>
<a id="rst-fe-get-info"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.fe -->

<a id="rst-name"></a>

## Name

FE_GET_INFO - Query Digital TV frontend capabilities and returns information about the - front-end. This call only requires read-only access to the device.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-FE_GET_INFO"></a>

```c
FE_GET_INFO
```

`int ioctl(int fd, FE_GET_INFO, struct dvb_frontend_info *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  pointer to struct `dvb_frontend_info`

<a id="rst-description"></a>

## Description

All Digital TV frontend devices support the [ioctl FE_GET_INFO](<#rst-fe-get-info>) ioctl. It is used to identify kernel devices compatible with this specification and to obtain information about driver and hardware capabilities. The ioctl takes a pointer to dvb_frontend_info which is filled by the driver. When the driver is not compatible with this specification the ioctl returns an error.

<a id="rst-frontend-capabilities"></a>

## frontend capabilities

Capabilities describe what a frontend can do. Some capabilities are supported only on some specific frontend types.

The frontend capabilities are described at `fe_caps`.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned.

On error -1 is returned, and the `errno` variable is set appropriately.

Generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
