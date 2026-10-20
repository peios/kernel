---
title: "V4L2 select()"
type: reference
description: "v4l2-select - Synchronous I/O multiplexing"
---

<a id="rst-v4l2-select"></a>
<a id="rst-func-select"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

v4l2-select - Synchronous I/O multiplexing

<a id="rst-synopsis"></a>

## Synopsis



```c
#include <sys/time.h>
#include <sys/types.h>
#include <unistd.h>
```





<a id="c-select"></a>

```c
int select( int nfds, fd_set *readfds, fd_set *writefds, fd_set *exceptfds, struct timeval *timeout )
```

<a id="rst-arguments"></a>

## Arguments

- **`nfds`**

  The highest-numbered file descriptor in any of the three sets, plus 1.

- **`readfds`**

  File descriptions to be watched if a read() call won't block.

- **`writefds`**

  File descriptions to be watched if a write() won't block.

- **`exceptfds`**

  File descriptions to be watched for V4L2 events.

- **`timeout`**

  Maximum time to wait.

<a id="rst-description"></a>

## Description

With the `select()` function applications can suspend execution until the driver has captured data or is ready to accept data for output.

When streaming I/O has been negotiated this function waits until a buffer has been filled or displayed and can be dequeued with the [VIDIOC_DQBUF](<~kernel/userspace/userspace-api/media-v4l/vidioc-qbuf#rst-vidioc-qbuf>) ioctl. When buffers are already in the outgoing queue of the driver the function returns immediately.

On success `select()` returns the total number of bits set in `fd_set`. When the function timed out it returns a value of zero. On failure it returns -1 and the `errno` variable is set appropriately. When the application did not call [ioctl VIDIOC_QBUF, VIDIOC_DQBUF](<~kernel/userspace/userspace-api/media-v4l/vidioc-qbuf#rst-vidioc-qbuf>) or [ioctl VIDIOC_STREAMON, VIDIOC_STREAMOFF](<~kernel/userspace/userspace-api/media-v4l/vidioc-streamon#rst-vidioc-streamon>) yet the `select()` function succeeds, setting the bit of the file descriptor in `readfds` or `writefds`, but subsequent [VIDIOC_DQBUF](<~kernel/userspace/userspace-api/media-v4l/vidioc-qbuf#rst-vidioc-qbuf>) calls will fail. <a id="rst-footnote-reference-1"></a>[1](#rst-f1)

When use of the `read()` function has been negotiated and the driver does not capture yet, the `select()` function starts capturing. When that fails, `select()` returns successful and a subsequent `read()` call, which also attempts to start capturing, will return an appropriate error code. When the driver captures continuously (as opposed to, for example, still images) and data is already available the `select()` function returns immediately.

When use of the `write()` function has been negotiated the `select()` function just waits until the driver is ready for a non-blocking `write()` call.

All drivers implementing the `read()` or `write()` function or streaming I/O must also support the `select()` function.

For more details see the `select()` manual page.

<a id="rst-return-value"></a>

## Return Value

On success, `select()` returns the number of descriptors contained in the three returned descriptor sets, which will be zero if the timeout expired. On error -1 is returned, and the `errno` variable is set appropriately; the sets and `timeout` are undefined. Possible error codes are:

- **EBADF**

  One or more of the file descriptor sets specified a file descriptor that is not open.

- **EBUSY**

  The driver does not support multiple read or write streams and the device is already in use.

- **EFAULT**

  The `readfds`, `writefds`, `exceptfds` or `timeout` pointer references an inaccessible memory area.

- **EINTR**

  The call was interrupted by a signal.

- **EINVAL**

  The `nfds` argument is less than zero or greater than `FD_SETSIZE`.

<a id="rst-f1"></a>



**[1]** The Linux kernel implements `select()` like the `poll()` function, but `select()` cannot return a `POLLERR`.
