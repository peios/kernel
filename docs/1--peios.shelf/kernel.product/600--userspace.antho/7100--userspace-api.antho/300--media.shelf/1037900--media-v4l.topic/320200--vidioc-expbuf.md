---
title: "ioctl VIDIOC_EXPBUF"
type: reference
description: "VIDIOC_EXPBUF - Export a buffer as a DMABUF file descriptor."
---

<a id="rst-ioctl-vidioc-expbuf"></a>
<a id="rst-vidioc-expbuf"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_EXPBUF - Export a buffer as a DMABUF file descriptor.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_EXPBUF"></a>

```c
VIDIOC_EXPBUF
```

`int ioctl(int fd, VIDIOC_EXPBUF, struct v4l2_exportbuffer *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_exportbuffer`.

<a id="rst-description"></a>

## Description

This ioctl is an extension to the [memory mapping](<~kernel/userspace/userspace-api/media-v4l/mmap#rst-mmap>) I/O method, therefore it is available only for `V4L2_MEMORY_MMAP` buffers. It can be used to export a buffer as a DMABUF file at any time after buffers have been allocated with the [vidioc_reqbufs](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-reqbufs.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) ioctl.

To export a buffer, applications fill struct `v4l2_exportbuffer`. The `type` field is set to the same buffer type as was previously used with struct `v4l2_requestbuffers` `type`. Applications must also set the `index` field. Valid index numbers range from zero to the number of buffers allocated with [vidioc_reqbufs](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-reqbufs.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) (struct `v4l2_requestbuffers` `count`) minus one. For the multi-planar API, applications set the `plane` field to the index of the plane to be exported. Valid planes range from zero to the maximal number of valid planes for the currently active format. For the single-planar API, applications must set `plane` to zero. Additional flags may be posted in the `flags` field. Refer to a manual for open() for details. Currently only O_CLOEXEC, O_RDONLY, O_WRONLY, and O_RDWR are supported. All other fields must be set to zero. In the case of multi-planar API, every plane is exported separately using multiple [ioctl VIDIOC_EXPBUF](<#rst-vidioc-expbuf>) calls.

After calling [ioctl VIDIOC_EXPBUF](<#rst-vidioc-expbuf>) the `fd` field will be set by a driver. This is a DMABUF file descriptor. The application may pass it to other DMABUF-aware devices. Refer to [DMABUF importing](<~kernel/userspace/userspace-api/media-v4l/dmabuf#rst-dmabuf>) for details about importing DMABUF files into V4L2 nodes. It is recommended to close a DMABUF file when it is no longer used to allow the associated memory to be reclaimed.

<a id="rst-examples"></a>

## Examples



```c
int buffer_export(int v4lfd, enum v4l2_buf_type bt, int index, int *dmafd)
{
    struct v4l2_exportbuffer expbuf;

    memset(&expbuf, 0, sizeof(expbuf));
    expbuf.type = bt;
    expbuf.index = index;
    if (ioctl(v4lfd, VIDIOC_EXPBUF, &expbuf) == -1) {
        perror("VIDIOC_EXPBUF");
        return -1;
    }

    *dmafd = expbuf.fd;

    return 0;
}
```



```c
int buffer_export_mp(int v4lfd, enum v4l2_buf_type bt, int index,
    int dmafd[], int n_planes)
{
    int i;

    for (i = 0; i < n_planes; ++i) {
        struct v4l2_exportbuffer expbuf;

        memset(&expbuf, 0, sizeof(expbuf));
        expbuf.type = bt;
        expbuf.index = index;
        expbuf.plane = i;
        if (ioctl(v4lfd, VIDIOC_EXPBUF, &expbuf) == -1) {
            perror("VIDIOC_EXPBUF");
            while (i)
                close(dmafd[--i]);
            return -1;
        }
        dmafd[i] = expbuf.fd;
    }

    return 0;
}
```





<a id="c-v4l2_exportbuffer"></a>

```c
v4l2_exportbuffer
```

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->


<table>
<caption>struct v4l2_exportbuffer</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`type`

</td>
<td>


Type of the buffer, same as struct `v4l2_format` `type` or struct `v4l2_requestbuffers` `type`, set by the application. See `v4l2_buf_type`

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`index`

</td>
<td>


Number of the buffer, set by the application. This field is only used for [memory mapping](<~kernel/userspace/userspace-api/media-v4l/mmap#rst-mmap>) I/O and can range from zero to the number of buffers allocated with the [vidioc_reqbufs](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-reqbufs.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) and/or [ioctl VIDIOC_CREATE_BUFS](<~kernel/userspace/userspace-api/media-v4l/vidioc-create-bufs#rst-vidioc-create-bufs>) ioctls.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`plane`

</td>
<td>


Index of the plane to be exported when using the multi-planar API. Otherwise this value must be set to zero.

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


Flags for the newly created file, currently only `O_CLOEXEC`, `O_RDONLY`, `O_WRONLY`, and `O_RDWR` are supported, refer to the manual of open() for more details.

</td>
</tr>
<tr>
<td>


\__s32

</td>
<td>


`fd`

</td>
<td>


The DMABUF file descriptor associated with a buffer. Set by the driver.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`reserved[11]`

</td>
<td>


Reserved field for future use. Drivers and applications must set the array to zero.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  A queue is not in MMAP mode or DMABUF exporting is not supported or `flags` or `type` or `index` or `plane` fields are invalid.
