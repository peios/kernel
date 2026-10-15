---
title: "V4L2 ioctl()"
type: reference
description: "v4l2-ioctl - Program a V4L2 device"
---

<a id="rst-v4l2-ioctl"></a>
<a id="rst-func-ioctl"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

v4l2-ioctl - Program a V4L2 device

<a id="rst-synopsis"></a>

## Synopsis



```c
#include <sys/ioctl.h>
```

`int ioctl(int fd, int request, void *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`request`**

  V4L2 ioctl request code as defined in the `videodev2.h` header file, for example VIDIOC_QUERYCAP.

- **`argp`**

  Pointer to a function parameter, usually a structure.

<a id="rst-description"></a>

## Description

The [ioctl()](<#rst-func-ioctl>) function is used to program V4L2 devices. The argument `fd` must be an open file descriptor. An ioctl `request` has encoded in it whether the argument is an input, output or read/write parameter, and the size of the argument `argp` in bytes. Macros and defines specifying V4L2 ioctl requests are located in the `videodev2.h` header file. Applications should use their own copy, not include the version in the kernel sources on the system they compile on. All V4L2 ioctl requests, their respective function and parameters are specified in [Function Reference](<~kernel/userspace/userspace-api/media-v4l/user-func#rst-user-func>).

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

When an ioctl that takes an output or read/write parameter fails, the parameter remains unmodified.
