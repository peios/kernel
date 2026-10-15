---
title: "request ioctl()"
type: reference
description: "request-ioctl - Control a request file descriptor"
---

<a id="rst-request-ioctl"></a>
<a id="rst-request-func-ioctl"></a>

<!-- SPDX-License-Identifier: GPL-2.0 OR GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: MC -->

<a id="rst-name"></a>

## Name

request-ioctl - Control a request file descriptor

<a id="rst-synopsis"></a>

## Synopsis



```c
#include <sys/ioctl.h>
```

`int ioctl(int fd, int cmd, void *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by [ioctl MEDIA_IOC_REQUEST_ALLOC](<~kernel/userspace/userspace-api/media-mediactl/media-ioc-request-alloc#rst-media-ioc-request-alloc>).

- **`cmd`**

  The request ioctl command code as defined in the media.h header file, for example [ioctl MEDIA_REQUEST_IOC_QUEUE](<~kernel/userspace/userspace-api/media-mediactl/media-request-ioc-queue#rst-media-request-ioc-queue>).

- **`argp`**

  Pointer to a request-specific structure.

<a id="rst-description"></a>

## Description

The [ioctl()](<#rst-request-func-ioctl>) function manipulates request parameters. The argument `fd` must be an open file descriptor.

The ioctl `cmd` code specifies the request function to be called. It has encoded in it whether the argument is an input, output or read/write parameter, and the size of the argument `argp` in bytes.

Macros and structures definitions specifying request ioctl commands and their parameters are located in the media.h header file. All request ioctl commands, their respective function and parameters are specified in [Function Reference](<~kernel/userspace/userspace-api/media-mediactl/media-funcs#rst-media-user-func>).

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

Command-specific error codes are listed in the individual command descriptions.

When an ioctl that takes an output or read/write parameter fails, the parameter remains unmodified.
