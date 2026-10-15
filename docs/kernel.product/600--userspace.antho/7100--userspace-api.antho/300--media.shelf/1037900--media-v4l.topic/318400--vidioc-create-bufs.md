---
title: "ioctl VIDIOC_CREATE_BUFS"
type: reference
description: "VIDIOC_CREATE_BUFS - Create buffers for Memory Mapped or User Pointer or DMA Buffer I/O"
---

<a id="rst-ioctl-vidioc-create-bufs"></a>
<a id="rst-vidioc-create-bufs"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_CREATE_BUFS - Create buffers for Memory Mapped or User Pointer or DMA Buffer I/O

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_CREATE_BUFS"></a>

```c
VIDIOC_CREATE_BUFS
```

`int ioctl(int fd, VIDIOC_CREATE_BUFS, struct v4l2_create_buffers *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_create_buffers`.

<a id="rst-description"></a>

## Description

This ioctl is used to create buffers for [memory mapped](<~kernel/userspace/userspace-api/media-v4l/mmap#rst-mmap>) or [user pointer](<~kernel/userspace/userspace-api/media-v4l/userp#rst-userp>) or [DMA buffer](<~kernel/userspace/userspace-api/media-v4l/dmabuf#rst-dmabuf>) I/O. It can be used as an alternative or in addition to the [vidioc_reqbufs](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-reqbufs.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) ioctl, when a tighter control over buffers is required. This ioctl can be called multiple times to create buffers of different sizes.

To allocate the device buffers applications must initialize the relevant fields of the struct `v4l2_create_buffers` structure. The `count` field must be set to the number of requested buffers, the `memory` field specifies the requested I/O method and the `reserved` array must be zeroed.

The `format` field specifies the image format that the buffers must be able to handle. The application has to fill in this struct `v4l2_format`. Usually this will be done using the [VIDIOC_TRY_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) or [VIDIOC_G_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) ioctls to ensure that the requested format is supported by the driver. Based on the format's `type` field the requested buffer size (for single-planar) or plane sizes (for multi-planar formats) will be used for the allocated buffers. The driver may return an error if the size(s) are not supported by the hardware (usually because they are too small).

The buffers created by this ioctl will have as minimum size the size defined by the `format.pix.sizeimage` field (or the corresponding fields for other format types). Usually if the `format.pix.sizeimage` field is less than the minimum required for the given format, then an error will be returned since drivers will typically not allow this. If it is larger, then the value will be used as-is. In other words, the driver may reject the requested size, but if it is accepted the driver will use it unchanged.

When the ioctl is called with a pointer to this structure the driver will attempt to allocate up to the requested number of buffers and store the actual number allocated and the starting index in the `count` and the `index` fields respectively. On return `count` can be smaller than the number requested.





<a id="c-v4l2_create_buffers"></a>

```c
v4l2_create_buffers
```

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->


<table>
<caption>struct v4l2_create_buffers</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`index`

</td>
<td>


The starting buffer index, returned by the driver.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`count`

</td>
<td>


The number of buffers requested or granted. If count == 0, then [ioctl VIDIOC_CREATE_BUFS](<#rst-vidioc-create-bufs>) will set `index` to the current number of created buffers, and it will check the validity of `memory` and `format.type`. If those are invalid -1 is returned and errno is set to `EINVAL` error code, otherwise [ioctl VIDIOC_CREATE_BUFS](<#rst-vidioc-create-bufs>) returns 0. It will never set errno to `EBUSY` error code in this particular case.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`memory`

</td>
<td>


Applications set this field to `V4L2_MEMORY_MMAP`, `V4L2_MEMORY_DMABUF` or `V4L2_MEMORY_USERPTR`. See `v4l2_memory`

</td>
</tr>
<tr>
<td>


struct `v4l2_format`

</td>
<td>


`format`

</td>
<td>


Filled in by the application, preserved by the driver.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`capabilities`

</td>
<td>


Set by the driver. If 0, then the driver doesn't support capabilities. In that case all you know is that the driver is guaranteed to support `V4L2_MEMORY_MMAP` and *might* support other `v4l2_memory` types. It will not support any other capabilities. See [here](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-reqbufs.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) for a list of the capabilities.

If you want to just query the capabilities without making any other changes, then set `count` to 0, `memory` to `V4L2_MEMORY_MMAP` and `format.type` to the buffer type.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`flags`

</td>
<td>


Specifies additional buffer management attributes. See [memory-flags](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-reqbufs.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>).

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`max_num_buffers`

</td>
<td>


If the V4L2_BUF_CAP_SUPPORTS_MAX_NUM_BUFFERS capability flag is set this field indicates the maximum possible number of buffers for this queue.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`reserved`\[5\]

</td>
<td>


A place holder for future extensions. Drivers and applications must set the array to zero.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **ENOMEM**

  No memory to allocate buffers for [memory mapped](<~kernel/userspace/userspace-api/media-v4l/mmap#rst-mmap>) I/O.

- **EINVAL**

  The buffer type (`format.type` field), requested I/O method (`memory`) or format (`format` field) is not valid.
