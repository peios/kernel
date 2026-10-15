---
title: "request close()"
type: reference
description: "request-close - Close a request file descriptor"
---

<a id="rst-request-close"></a>
<a id="rst-request-func-close"></a>

<!-- SPDX-License-Identifier: GPL-2.0 OR GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: MC.request -->

<a id="rst-name"></a>

## Name

request-close - Close a request file descriptor

<a id="rst-synopsis"></a>

## Synopsis



```c
#include <unistd.h>
```





<a id="c-close"></a>

```c
int close( int fd )
```

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by [ioctl MEDIA_IOC_REQUEST_ALLOC](<~kernel/userspace/userspace-api/media-mediactl/media-ioc-request-alloc#rst-media-ioc-request-alloc>).

<a id="rst-description"></a>

## Description

Closes the request file descriptor. Resources associated with the request are freed once all file descriptors associated with the request are closed and the driver has completed the request. See [here](<~kernel/userspace/userspace-api/media-mediactl/request-api#rst-media-request-life-time>) for more information.

<a id="rst-return-value"></a>

## Return Value

`close()` returns 0 on success. On error, -1 is returned, and `errno` is set appropriately. Possible error codes are:

- **EBADF**

  `fd` is not a valid open file descriptor.
