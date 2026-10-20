---
title: "ioctl MEDIA_REQUEST_IOC_REINIT"
type: reference
description: "MEDIA_REQUEST_IOC_REINIT - Re-initialize a request"
---

<a id="rst-ioctl-media-request-ioc-reinit"></a>
<a id="rst-media-request-ioc-reinit"></a>

<!-- SPDX-License-Identifier: GPL-2.0 OR GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: MC -->

<a id="rst-name"></a>

## Name

MEDIA_REQUEST_IOC_REINIT - Re-initialize a request

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-MEDIA_REQUEST_IOC_REINIT"></a>

```c
MEDIA_REQUEST_IOC_REINIT
```

`int ioctl(int request_fd, MEDIA_REQUEST_IOC_REINIT)`

<a id="rst-arguments"></a>

## Arguments

- **`request_fd`**

  File descriptor returned by [ioctl MEDIA_IOC_REQUEST_ALLOC](<~kernel/userspace/userspace-api/media-mediactl/media-ioc-request-alloc#rst-media-ioc-request-alloc>).

<a id="rst-description"></a>

## Description

If the media device supports [requests](<~kernel/userspace/userspace-api/media-mediactl/request-api#rst-media-request-api>), then this request ioctl can be used to re-initialize a previously allocated request.

Re-initializing a request will clear any existing data from the request. This avoids having to `close()` a completed request and allocate a new request. Instead the completed request can just be re-initialized and it is ready to be used again.

A request can only be re-initialized if it either has not been queued yet, or if it was queued and completed. Otherwise it will set `errno` to `EBUSY`. No other error codes can be returned.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately.

- **EBUSY**

  The request is queued but not yet completed.
