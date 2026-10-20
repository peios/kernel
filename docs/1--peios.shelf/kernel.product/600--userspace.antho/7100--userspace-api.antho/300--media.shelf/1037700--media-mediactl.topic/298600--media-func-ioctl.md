---
title: "media ioctl()"
type: reference
description: "media-ioctl - Control a media device"
---

<a id="rst-media-ioctl"></a>
<a id="rst-media-func-ioctl"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: MC -->

<a id="rst-name"></a>

## Name

media-ioctl - Control a media device

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

  Media ioctl request code as defined in the media.h header file, for example MEDIA_IOC_SETUP_LINK.

- **`argp`**

  Pointer to a request-specific structure.

<a id="rst-description"></a>

## Description

The [ioctl()](<#rst-media-func-ioctl>) function manipulates media device parameters. The argument `fd` must be an open file descriptor.

The ioctl `request` code specifies the media function to be called. It has encoded in it whether the argument is an input, output or read/write parameter, and the size of the argument `argp` in bytes.

Macros and structures definitions specifying media ioctl requests and their parameters are located in the media.h header file. All media ioctl requests, their respective function and parameters are specified in [Function Reference](<~kernel/userspace/userspace-api/media-mediactl/media-funcs#rst-media-user-func>).

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

Request-specific error codes are listed in the individual requests descriptions.

When an ioctl that takes an output or read/write parameter fails, the parameter remains unmodified.
