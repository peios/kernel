---
title: "V4L2 open()"
type: reference
description: "v4l2-open - Open a V4L2 device"
---

<a id="rst-v4l2-open"></a>
<a id="rst-func-open"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

v4l2-open - Open a V4L2 device

<a id="rst-synopsis"></a>

## Synopsis



```c
#include <fcntl.h>
```





<a id="c-open"></a>

```c
int open( const char *device_name, int flags )
```

<a id="rst-arguments"></a>

## Arguments

- **`device_name`**

  Device to be opened.

- **`flags`**

  Open flags. Access mode must be `O_RDWR`. This is just a technicality, input devices still support only reading and output devices only writing.

  When the `O_NONBLOCK` flag is given, the `read()` function and the [VIDIOC_DQBUF](<~kernel/userspace/userspace-api/media-v4l/vidioc-qbuf#rst-vidioc-qbuf>) ioctl will return the `EAGAIN` error code when no data is available or no buffer is in the driver outgoing queue, otherwise these functions block until data becomes available. All V4L2 drivers exchanging data with applications must support the `O_NONBLOCK` flag.

  Other flags have no effect.

<a id="rst-description"></a>

## Description

To open a V4L2 device applications call `open()` with the desired device name. This function has no side effects; all data format parameters, current input or output, control values or other properties remain unchanged. At the first `open()` call after loading the driver they will be reset to default values, drivers are never in an undefined state.

<a id="rst-return-value"></a>

## Return Value

On success `open()` returns the new file descriptor. On error -1 is returned, and the `errno` variable is set appropriately. Possible error codes are:

- **EACCES**

  The caller has no permission to access the device.

- **EBUSY**

  The driver does not support multiple opens and the device is already in use.

- **ENODEV**

  Device not found or was removed.

- **ENOMEM**

  Not enough kernel memory was available to complete the request.

- **EMFILE**

  The process already has the maximum number of files open.

- **ENFILE**

  The limit on the total number of files open on the system has been reached.
