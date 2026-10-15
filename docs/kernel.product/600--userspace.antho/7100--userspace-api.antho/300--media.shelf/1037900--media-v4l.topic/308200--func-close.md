---
title: "V4L2 close()"
type: reference
description: "v4l2-close - Close a V4L2 device"
---

<a id="rst-v4l2-close"></a>
<a id="rst-func-close"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

v4l2-close - Close a V4L2 device

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

  File descriptor returned by `open()`.

<a id="rst-description"></a>

## Description

Closes the device. Any I/O in progress is terminated and resources associated with the file descriptor are freed. However data format parameters, current input or output, control values or other properties remain unchanged.

<a id="rst-return-value"></a>

## Return Value

The function returns 0 on success, -1 on failure and the `errno` is set appropriately. Possible error codes:

- **EBADF**

  `fd` is not a valid open file descriptor.
