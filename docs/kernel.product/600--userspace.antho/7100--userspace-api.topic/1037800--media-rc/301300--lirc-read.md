---
title: "LIRC read()"
type: reference
description: "lirc-read - Read from a LIRC device"
---

<a id="rst-lirc-read-1"></a>
<a id="rst-lirc-read"></a>

<!-- SPDX-License-Identifier: GPL-2.0 OR GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: RC -->

<a id="rst-name"></a>

## Name

lirc-read - Read from a LIRC device

<a id="rst-synopsis"></a>

## Synopsis



```c
#include <unistd.h>
```





<a id="c-read"></a>

```c
ssize_t read( int fd, void *buf, size_t count )
```

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`buf`**

  Buffer to be filled

- **`count`**

  Max number of bytes to read

<a id="rst-description"></a>

## Description

`read()` attempts to read up to `count` bytes from file descriptor `fd` into the buffer starting at `buf`.  If `count` is zero, `read()` returns zero and has no other results. If `count` is greater than `SSIZE_MAX`, the result is unspecified.

The exact format of the data depends on what [LIRC modes](<~kernel/userspace/userspace-api/media-rc/lirc-dev-intro#rst-lirc-modes>) a driver uses. Use [ioctl LIRC_GET_FEATURES](<~kernel/userspace/userspace-api/media-rc/lirc-get-features#rst-lirc-get-features>) to get the supported mode, and use [ioctls LIRC_GET_REC_MODE and LIRC_SET_REC_MODE](<~kernel/userspace/userspace-api/media-rc/lirc-get-rec-mode#rst-lirc-set-rec-mode>) set the current active mode.

The mode [LIRC_MODE_MODE2](<~kernel/userspace/userspace-api/media-rc/lirc-dev-intro#rst-lirc-mode-mode2>) is for raw IR, in which packets containing an unsigned int value describing an IR signal are read from the chardev.

Alternatively, [LIRC_MODE_SCANCODE](<~kernel/userspace/userspace-api/media-rc/lirc-dev-intro#rst-lirc-mode-scancode>) can be available, in this mode scancodes which are either decoded by software decoders, or by hardware decoders. The `rc_proto` member is set to the [IR protocol](<~kernel/userspace/userspace-api/media-rc/rc-protos#rst-remote-controllers-protocols>) used for transmission, and `scancode` to the decoded scancode, and the `keycode` set to the keycode or `KEY_RESERVED`.

<a id="rst-return-value"></a>

## Return Value

On success, the number of bytes read is returned. It is not an error if this number is smaller than the number of bytes requested, or the amount of data required for one frame.  On error, -1 is returned, and the `errno` variable is set appropriately.
