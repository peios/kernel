---
title: "V4L2 munmap()"
type: reference
description: "v4l2-munmap - Unmap device memory"
---

<a id="rst-v4l2-munmap"></a>
<a id="rst-func-munmap"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

v4l2-munmap - Unmap device memory

<a id="rst-synopsis"></a>

## Synopsis



```c
#include <unistd.h>
#include <sys/mman.h>
```





<a id="c-munmap"></a>

```c
int munmap( void *start, size_t length )
```

<a id="rst-arguments"></a>

## Arguments

- **`start`**

  Address of the mapped buffer as returned by the `mmap()` function.

- **`length`**

  Length of the mapped buffer. This must be the same value as given to `mmap()` and returned by the driver in the struct `v4l2_buffer` `length` field for the single-planar API and in the struct `v4l2_plane` `length` field for the multi-planar API.

<a id="rst-description"></a>

## Description

Unmaps a previously with the `mmap()` function mapped buffer and frees it, if possible.

<a id="rst-return-value"></a>

## Return Value

On success `munmap()` returns 0, on failure -1 and the `errno` variable is set appropriately:

- **EINVAL**

  The `start` or `length` is incorrect, or no buffers have been mapped yet.
