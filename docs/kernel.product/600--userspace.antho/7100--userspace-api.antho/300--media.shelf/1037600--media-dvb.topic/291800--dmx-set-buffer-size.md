---
title: "DMX_SET_BUFFER_SIZE"
type: reference
description: "Duplicate implicit target name: \"dmx_set_buffer_size\"."
---

<a id="rst-dmx-set-buffer-size-1"></a>
<a id="rst-dmx-set-buffer-size"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.dmx -->

<a id="rst-name"></a>

## Name

DMX_SET_BUFFER_SIZE

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-DMX_SET_BUFFER_SIZE"></a>

```c
DMX_SET_BUFFER_SIZE
```

`int ioctl(int fd, DMX_SET_BUFFER_SIZE, unsigned long size)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`size`**

  Unsigned long size

<a id="rst-description"></a>

## Description

This ioctl call is used to set the size of the circular buffer used for filtered data. The default size is two maximum sized sections, i.e. if this function is not called a buffer size of `2 * 4096` bytes will be used.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned.

On error -1 is returned, and the `errno` variable is set appropriately.

The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
