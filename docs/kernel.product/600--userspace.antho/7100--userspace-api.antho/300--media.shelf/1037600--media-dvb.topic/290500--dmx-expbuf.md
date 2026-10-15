---
title: "ioctl DMX_EXPBUF"
type: reference
description: "DMX_EXPBUF - Export a buffer as a DMABUF file descriptor."
---

<a id="rst-ioctl-dmx-expbuf"></a>
<a id="rst-dmx-expbuf"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.dmx -->

<a id="rst-name"></a>

## Name

DMX_EXPBUF - Export a buffer as a DMABUF file descriptor.

> [!WARNING]
>
> this API is still experimental

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-DMX_EXPBUF"></a>

```c
DMX_EXPBUF
```

`int ioctl(int fd, DMX_EXPBUF, struct dmx_exportbuffer *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `dmx_exportbuffer`.

<a id="rst-description"></a>

## Description

This ioctl is an extension to the memory mapping I/O method. It can be used to export a buffer as a DMABUF file at any time after buffers have been allocated with the [ioctl DMX_REQBUFS](<~kernel/userspace/userspace-api/media-dvb/dmx-reqbufs#rst-dmx-reqbufs>) ioctl.

To export a buffer, applications fill struct `dmx_exportbuffer`. Applications must set the `index` field. Valid index numbers range from zero to the number of buffers allocated with [ioctl DMX_REQBUFS](<~kernel/userspace/userspace-api/media-dvb/dmx-reqbufs#rst-dmx-reqbufs>) (struct `dmx_requestbuffers` `count`) minus one. Additional flags may be posted in the `flags` field. Refer to a manual for open() for details. Currently only O_CLOEXEC, O_RDONLY, O_WRONLY, and O_RDWR are supported. All other fields must be set to zero. In the case of multi-planar API, every plane is exported separately using multiple [ioctl DMX_EXPBUF](<#rst-dmx-expbuf>) calls.

After calling [ioctl DMX_EXPBUF](<#rst-dmx-expbuf>) the `fd` field will be set by a driver, on success. This is a DMABUF file descriptor. The application may pass it to other DMABUF-aware devices. It is recommended to close a DMABUF file when it is no longer used to allow the associated memory to be reclaimed.

<a id="rst-examples"></a>

## Examples



```c
int buffer_export(int v4lfd, enum dmx_buf_type bt, int index, int *dmafd)
{
    struct dmx_exportbuffer expbuf;

    memset(&expbuf, 0, sizeof(expbuf));
    expbuf.type = bt;
    expbuf.index = index;
    if (ioctl(v4lfd, DMX_EXPBUF, &expbuf) == -1) {
        perror("DMX_EXPBUF");
        return -1;
    }

    *dmafd = expbuf.fd;

    return 0;
}
```

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  A queue is not in MMAP mode or DMABUF exporting is not supported or `flags` or `index` fields are invalid.
