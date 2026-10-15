---
title: "Digital TV mmap()"
type: reference
description: "dmx-mmap - Map device memory into application address space"
---

<a id="rst-digital-tv-mmap"></a>
<a id="rst-dmx-mmap"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.dmx -->

<a id="rst-name"></a>

## Name

dmx-mmap - Map device memory into application address space

> [!WARNING]
>
> this API is still experimental

<a id="rst-synopsis"></a>

## Synopsis



```c
#include <unistd.h>
#include <sys/mman.h>
```





<a id="c-mmap"></a>

```c
void *mmap( void *start, size_t length, int prot, int flags, int fd, off_t offset )
```

<a id="rst-arguments"></a>

## Arguments

- **`start`**

  Map the buffer to this address in the application's address space. When the `MAP_FIXED` flag is specified, `start` must be a multiple of the pagesize and mmap will fail when the specified address cannot be used. Use of this option is discouraged; applications should just specify a `NULL` pointer here.

- **`length`**

  Length of the memory area to map. This must be a multiple of the DVB packet length (188, on most drivers).

- **`prot`**

  The `prot` argument describes the desired memory protection. Regardless of the device type and the direction of data exchange it should be set to `PROT_READ` \| `PROT_WRITE`, permitting read and write access to image buffers. Drivers should support at least this combination of flags.

- **`flags`**

  The `flags` parameter specifies the type of the mapped object, mapping options and whether modifications made to the mapped copy of the page are private to the process or are to be shared with other references.

  `MAP_FIXED` requests that the driver selects no other address than the one specified. If the specified address cannot be used, `mmap()` will fail. If `MAP_FIXED` is specified, `start` must be a multiple of the pagesize. Use of this option is discouraged.

  One of the `MAP_SHARED` or `MAP_PRIVATE` flags must be set. `MAP_SHARED` allows applications to share the mapped memory with other (e. g. child-) processes.

  > [!NOTE]
  >
  > The Linux Digital TV applications should not set the `MAP_PRIVATE`, `MAP_DENYWRITE`, `MAP_EXECUTABLE` or `MAP_ANON` flags.

- **`fd`**

  File descriptor returned by `open()`.

- **`offset`**

  Offset of the buffer in device memory, as returned by [ioctl DMX_QUERYBUF](<~kernel/userspace/userspace-api/media-dvb/dmx-querybuf#rst-dmx-querybuf>) ioctl.

<a id="rst-description"></a>

## Description

The `mmap()` function asks to map `length` bytes starting at `offset` in the memory of the device specified by `fd` into the application address space, preferably at address `start`. This latter address is a hint only, and is usually specified as 0.

Suitable length and offset parameters are queried with the [ioctl DMX_QUERYBUF](<~kernel/userspace/userspace-api/media-dvb/dmx-querybuf#rst-dmx-querybuf>) ioctl. Buffers must be allocated with the [ioctl DMX_REQBUFS](<~kernel/userspace/userspace-api/media-dvb/dmx-reqbufs#rst-dmx-reqbufs>) ioctl before they can be queried.

To unmap buffers the `munmap()` function is used.

<a id="rst-return-value"></a>

## Return Value

On success `mmap()` returns a pointer to the mapped buffer. On error `MAP_FAILED` (-1) is returned, and the `errno` variable is set appropriately. Possible error codes are:

- **EBADF**

  `fd` is not a valid file descriptor.

- **EACCES**

  `fd` is not open for reading and writing.

- **EINVAL**

  The `start` or `length` or `offset` are not suitable. (E. g. they are too large, or not aligned on a `PAGESIZE` boundary.)

  The `flags` or `prot` value is not supported.

  No buffers have been allocated with the [ioctl DMX_REQBUFS](<~kernel/userspace/userspace-api/media-dvb/dmx-reqbufs#rst-dmx-reqbufs>) ioctl.

- **ENOMEM**

  Not enough physical or virtual memory was available to complete the request.
