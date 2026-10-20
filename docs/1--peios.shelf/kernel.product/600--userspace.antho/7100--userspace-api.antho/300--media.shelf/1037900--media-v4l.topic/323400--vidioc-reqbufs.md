---
title: "ioctl VIDIOC_REQBUFS"
type: reference
description: "VIDIOC_REQBUFS - Initiate Memory Mapping, User Pointer I/O or DMA buffer I/O"
---

<a id="rst-ioctl-vidioc-reqbufs"></a>
<a id="rst-vidioc-reqbufs"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC\_REQBUFS - Initiate Memory Mapping, User Pointer I/O or DMA buffer I/O

<a id="rst-synopsis"></a>

## Synopsis

<a id="c-VIDIOC_REQBUFS"></a>



```c
VIDIOC_REQBUFS
```

`int ioctl(int fd, VIDIOC_REQBUFS, struct v4l2_requestbuffers *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_requestbuffers`.

<a id="rst-description"></a>

## Description

This ioctl is used to initiate [memory mapped](<~kernel/userspace/userspace-api/media-v4l/mmap#rst-mmap>), [user pointer](<~kernel/userspace/userspace-api/media-v4l/userp#rst-userp>) or [DMABUF](<~kernel/userspace/userspace-api/media-v4l/dmabuf#rst-dmabuf>) based I/O. Memory mapped buffers are located in device memory and must be allocated with this ioctl before they can be mapped into the application's address space. User buffers are allocated by applications themselves, and this ioctl is merely used to switch the driver into user pointer I/O mode and to setup some internal structures. Similarly, DMABUF buffers are allocated by applications through a device driver, and this ioctl only configures the driver into DMABUF I/O mode without performing any direct allocation.

To allocate device buffers applications initialize all fields of the struct `v4l2_requestbuffers` structure. They set the `type` field to the respective stream or buffer type, the `count` field to the desired number of buffers, `memory` must be set to the requested I/O method and the `reserved` array must be zeroed. When the ioctl is called with a pointer to this structure the driver will attempt to allocate the requested number of buffers and it stores the actual number allocated in the `count` field. It can be smaller than the number requested, even zero, when the driver runs out of free memory. A larger number is also possible when the driver requires more buffers to function correctly. For example video output requires at least two buffers, one displayed and one filled by the application.

When the I/O method is not supported the ioctl returns an `EINVAL` error code.

Applications can call [ioctl VIDIOC\_REQBUFS](<#rst-vidioc-reqbufs>) again to change the number of buffers. Note that if any buffers are still mapped or exported via DMABUF, then [ioctl VIDIOC\_REQBUFS](<#rst-vidioc-reqbufs>) can only succeed if the `V4L2_BUF_CAP_SUPPORTS_ORPHANED_BUFS` capability is set. Otherwise [ioctl VIDIOC\_REQBUFS](<#rst-vidioc-reqbufs>) will return the `EBUSY` error code. If `V4L2_BUF_CAP_SUPPORTS_ORPHANED_BUFS` is set, then these buffers are orphaned and will be freed when they are unmapped or when the exported DMABUF fds are closed. A `count` value of zero frees or orphans all buffers, after aborting or finishing any DMA in progress, an implicit [VIDIOC\_STREAMOFF](<~kernel/userspace/userspace-api/media-v4l/vidioc-streamon#rst-vidioc-streamon>).

<a id="c-v4l2_requestbuffers"></a>



```c
v4l2_requestbuffers
```

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->


<table>
<caption>

struct v4l2\_requestbuffers

</caption>
<tbody>
<tr>
<td>



\_\_u32

</td>
<td>



`count`

</td>
<td>



The number of buffers requested or granted.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`type`

</td>
<td>



Type of the stream or buffers, this is the same as the struct `v4l2_format` `type` field. See `v4l2_buf_type` for valid values.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`memory`

</td>
<td>



Applications set this field to `V4L2_MEMORY_MMAP`, `V4L2_MEMORY_DMABUF` or `V4L2_MEMORY_USERPTR`. See `v4l2_memory`.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`capabilities`

</td>
<td>



Set by the driver. If 0, then the driver doesn't support capabilities. In that case all you know is that the driver is guaranteed to support `V4L2_MEMORY_MMAP` and <em>might</em> support other `v4l2_memory` types. It will not support any other capabilities.

If you want to query the capabilities with a minimum of side-effects, then this can be called with `count` set to 0, `memory` set to `V4L2_MEMORY_MMAP` and `type` set to the buffer type. This will free any previously allocated buffers, so this is typically something that will be done at the start of the application.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`flags`

</td>
<td>



Specifies additional buffer management attributes. See [memory-flags](<#rst-memory-flags>).

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`reserved`\[3\]

</td>
<td>



Reserved for future extensions.

</td>
</tr>
</tbody>
</table>

<a id="rst-v4l2-buf-cap-supports-remove-bufs"></a>
<a id="rst-v4l2-buf-cap-supports-max-num-buffers"></a>
<a id="rst-v4l2-buf-cap-supports-mmap-cache-hints"></a>
<a id="rst-v4l2-buf-cap-supports-m2m-hold-capture-buf"></a>
<a id="rst-v4l2-buf-cap-supports-orphaned-bufs"></a>
<a id="rst-v4l2-buf-cap-supports-requests"></a>
<a id="rst-v4l2-buf-cap-supports-dmabuf"></a>
<a id="rst-v4l2-buf-cap-supports-userptr"></a>
<a id="rst-v4l2-buf-cap-supports-mmap"></a>
<a id="rst-v4l2-buf-capabilities"></a>


<table>
<caption>

V4L2 Buffer Capabilities Flags

</caption>
<tbody>
<tr>
<td>



`V4L2_BUF_CAP_SUPPORTS_MMAP`

</td>
<td>



0x00000001

</td>
<td>



This buffer type supports the `V4L2_MEMORY_MMAP` streaming mode.

</td>
</tr>
<tr>
<td>



`V4L2_BUF_CAP_SUPPORTS_USERPTR`

</td>
<td>



0x00000002

</td>
<td>



This buffer type supports the `V4L2_MEMORY_USERPTR` streaming mode.

</td>
</tr>
<tr>
<td>



`V4L2_BUF_CAP_SUPPORTS_DMABUF`

</td>
<td>



0x00000004

</td>
<td>



This buffer type supports the `V4L2_MEMORY_DMABUF` streaming mode.

</td>
</tr>
<tr>
<td>



`V4L2_BUF_CAP_SUPPORTS_REQUESTS`

</td>
<td>



0x00000008

</td>
<td>



This buffer type supports [requests](<~kernel/userspace/userspace-api/media-mediactl/request-api#rst-media-request-api>).

</td>
</tr>
<tr>
<td>



`V4L2_BUF_CAP_SUPPORTS_ORPHANED_BUFS`

</td>
<td>



0x00000010

</td>
<td>



The kernel allows calling [ioctl VIDIOC\_REQBUFS](<#rst-vidioc-reqbufs>) while buffers are still mapped or exported via DMABUF. These orphaned buffers will be freed when they are unmapped or when the exported DMABUF fds are closed.

</td>
</tr>
<tr>
<td>



`V4L2_BUF_CAP_SUPPORTS_M2M_HOLD_CAPTURE_BUF`

</td>
<td>



0x00000020

</td>
<td>



Only valid for stateless decoders. If set, then userspace can set the `V4L2_BUF_FLAG_M2M_HOLD_CAPTURE_BUF` flag to hold off on returning the capture buffer until the OUTPUT timestamp changes.

</td>
</tr>
<tr>
<td>



`V4L2_BUF_CAP_SUPPORTS_MMAP_CACHE_HINTS`

</td>
<td>



0x00000040

</td>
<td>



This capability is set by the driver to indicate that the queue supports cache and memory management hints. However, it's only valid when the queue is used for [memory mapping](<~kernel/userspace/userspace-api/media-v4l/mmap#rst-mmap>) streaming I/O. See [V4L2\_BUF\_FLAG\_NO\_CACHE\_INVALIDATE](<~kernel/userspace/userspace-api/media-v4l/buffer#rst-v4l2-buf-flag-no-cache-invalidate>), [V4L2\_BUF\_FLAG\_NO\_CACHE\_CLEAN](<~kernel/userspace/userspace-api/media-v4l/buffer#rst-v4l2-buf-flag-no-cache-clean>) and [V4L2\_MEMORY\_FLAG\_NON\_COHERENT](<#rst-v4l2-memory-flag-non-coherent>).

</td>
</tr>
<tr>
<td>



`V4L2_BUF_CAP_SUPPORTS_MAX_NUM_BUFFERS`

</td>
<td>



0x00000080

</td>
<td>



If set, then the `max_num_buffers` field in `struct v4l2_create_buffers` is valid. If not set, then the maximum is `VIDEO_MAX_FRAME` buffers.

</td>
</tr>
<tr>
<td>



`V4L2_BUF_CAP_SUPPORTS_REMOVE_BUFS`

</td>
<td>



0x00000100

</td>
<td>



If set, then `VIDIOC_REMOVE_BUFS` is supported.

</td>
</tr>
</tbody>
</table>

<a id="rst-v4l2-memory-flag-non-coherent"></a>
<a id="rst-memory-flags"></a>


<table>
<caption>

Memory Consistency Flags

</caption>
<tbody>
<tr>
<td>



`V4L2_MEMORY_FLAG_NON_COHERENT`

</td>
<td>



0x00000001

</td>
<td>



A buffer is allocated either in coherent (it will be automatically coherent between the CPU and the bus) or non-coherent memory. The latter can provide performance gains, for instance the CPU cache sync/flush operations can be avoided if the buffer is accessed by the corresponding device only and the CPU does not read/write to/from that buffer. However, this requires extra care from the driver -- it must guarantee memory consistency by issuing a cache flush/sync when consistency is needed. If this flag is set V4L2 will attempt to allocate the buffer in non-coherent memory. The flag takes effect only if the buffer is used for [memory mapping](<~kernel/userspace/userspace-api/media-v4l/mmap#rst-mmap>) I/O and the queue reports the [V4L2\_BUF\_CAP\_SUPPORTS\_MMAP\_CACHE\_HINTS](<#rst-v4l2-buf-cap-supports-mmap-cache-hints>) capability.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  The buffer type (`type` field) or the requested I/O method (`memory`) is not supported.
