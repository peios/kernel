---
title: "Digital TV frontend close()"
type: reference
description: "fe-close - Close a frontend device"
---

<a id="rst-digital-tv-frontend-close"></a>
<a id="rst-frontend-f-close"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.fe -->

<a id="rst-name"></a>

## Name

fe-close - Close a frontend device

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

This system call closes a previously opened front-end device. After closing a front-end device, its corresponding hardware might be powered down automatically.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned.

On error -1 is returned, and the `errno` variable is set appropriately.

Generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
