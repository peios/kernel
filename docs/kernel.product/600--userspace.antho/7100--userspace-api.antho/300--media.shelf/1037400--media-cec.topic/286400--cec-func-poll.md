---
title: "cec poll()"
type: reference
description: "cec-poll - Wait for some event on a file descriptor"
---

<a id="rst-cec-poll"></a>
<a id="rst-cec-func-poll"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: CEC -->

<a id="rst-name"></a>

## Name

cec-poll - Wait for some event on a file descriptor

<a id="rst-synopsis"></a>

## Synopsis



```c
#include <sys/poll.h>
```





<a id="c-poll"></a>

```c
int poll( struct pollfd *ufds, unsigned int nfds, int timeout )
```

<a id="rst-arguments"></a>

## Arguments

- **`ufds`**

  List of FD events to be watched

- **`nfds`**

  Number of FD events at the \*ufds array

- **`timeout`**

  Timeout to wait for events

<a id="rst-description"></a>

## Description

With the `poll()` function applications can wait for CEC events.

On success `poll()` returns the number of file descriptors that have been selected (that is, file descriptors for which the `revents` field of the respective struct `pollfd` is non-zero). CEC devices set the `POLLIN` and `POLLRDNORM` flags in the `revents` field if there are messages in the receive queue. If the transmit queue has room for new messages, the `POLLOUT` and `POLLWRNORM` flags are set. If there are events in the event queue, then the `POLLPRI` flag is set. When the function times out it returns a value of zero, on failure it returns -1 and the `errno` variable is set appropriately.

For more details see the `poll()` manual page.

<a id="rst-return-value"></a>

## Return Value

On success, `poll()` returns the number structures which have non-zero `revents` fields, or zero if the call timed out. On error -1 is returned, and the `errno` variable is set appropriately:

- **`EBADF`**

  One or more of the `ufds` members specify an invalid file descriptor.

- **`EFAULT`**

  `ufds` references an inaccessible memory area.

- **`EINTR`**

  The call was interrupted by a signal.

- **`EINVAL`**

  The `nfds` value exceeds the `RLIMIT_NOFILE` value. Use `getrlimit()` to obtain this value.
