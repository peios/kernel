---
title: "cec close()"
type: reference
description: "cec-close - Close a cec device"
---

<a id="rst-cec-close"></a>
<a id="rst-cec-func-close"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: CEC -->

<a id="rst-name"></a>

## Name

cec-close - Close a cec device

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

Closes the cec device. Resources associated with the file descriptor are freed. The device configuration remain unchanged.

<a id="rst-return-value"></a>

## Return Value

`close()` returns 0 on success. On error, -1 is returned, and `errno` is set appropriately. Possible error codes are:

- **`EBADF`**

  `fd` is not a valid open file descriptor.
