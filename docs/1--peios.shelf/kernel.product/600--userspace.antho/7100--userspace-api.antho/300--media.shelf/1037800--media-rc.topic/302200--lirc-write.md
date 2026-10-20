---
title: "LIRC write()"
type: reference
description: "lirc-write - Write to a LIRC device"
---

<a id="rst-lirc-write-1"></a>
<a id="rst-lirc-write"></a>

<!-- SPDX-License-Identifier: GPL-2.0 OR GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: RC -->

<a id="rst-name"></a>

## Name

lirc-write - Write to a LIRC device

<a id="rst-synopsis"></a>

## Synopsis



```c
#include <unistd.h>
```





<a id="c-write"></a>

```c
ssize_t write( int fd, void *buf, size_t count )
```

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`buf`**

  Buffer with data to be written

- **`count`**

  Number of bytes at the buffer

<a id="rst-description"></a>

## Description

`write()` writes up to `count` bytes to the device referenced by the file descriptor `fd` from the buffer starting at `buf`.

The exact format of the data depends on what mode a driver is in, use [ioctl LIRC_GET_FEATURES](<~kernel/userspace/userspace-api/media-rc/lirc-get-features#rst-lirc-get-features>) to get the supported modes and use [ioctls LIRC_GET_SEND_MODE and LIRC_SET_SEND_MODE](<~kernel/userspace/userspace-api/media-rc/lirc-get-send-mode#rst-lirc-set-send-mode>) set the mode.

When in [LIRC_MODE_PULSE](<~kernel/userspace/userspace-api/media-rc/lirc-dev-intro#rst-lirc-mode-pulse>) mode, the data written to the chardev is a pulse/space sequence of integer values. Pulses and spaces are only marked implicitly by their position. The data must start and end with a pulse, therefore, the data must always include an uneven number of samples. The write function blocks until the data has been transmitted by the hardware. If more data is provided than the hardware can send, the driver returns `EINVAL`.

When in [LIRC_MODE_SCANCODE](<~kernel/userspace/userspace-api/media-rc/lirc-dev-intro#rst-lirc-mode-scancode>) mode, one `struct lirc_scancode` must be written to the chardev at a time, else `EINVAL` is returned. Set the desired scancode in the `scancode` member, and the [IR protocol](<~kernel/userspace/userspace-api/media-rc/rc-protos#rst-remote-controllers-protocols>) in the `rc_proto`: member. All other members must be set to 0, else `EINVAL` is returned. If there is no protocol encoder for the protocol or the scancode is not valid for the specified protocol, `EINVAL` is returned. The write function blocks until the scancode is transmitted by the hardware.

<a id="rst-return-value"></a>

## Return Value

On success, the number of bytes written is returned. It is not an error if this number is smaller than the number of bytes requested, or the amount of data required for one frame.  On error, -1 is returned, and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
