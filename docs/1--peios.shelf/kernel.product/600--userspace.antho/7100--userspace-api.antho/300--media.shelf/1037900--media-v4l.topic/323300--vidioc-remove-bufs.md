---
title: "ioctl VIDIOC_REMOVE_BUFS"
type: reference
description: "VIDIOC_REMOVE_BUFS - Removes buffers from a queue"
---

<a id="rst-ioctl-vidioc-remove-bufs"></a>
<a id="rst-vidioc-remove-bufs"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_REMOVE_BUFS - Removes buffers from a queue

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_REMOVE_BUFS"></a>

```c
VIDIOC_REMOVE_BUFS
```

`int ioctl(int fd, VIDIOC_REMOVE_BUFS, struct v4l2_remove_buffers *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_remove_buffers`.

<a id="rst-description"></a>

## Description

Applications can optionally call the [ioctl VIDIOC_REMOVE_BUFS](<#rst-vidioc-remove-bufs>) ioctl to remove buffers from a queue. [ioctl VIDIOC_CREATE_BUFS](<~kernel/userspace/userspace-api/media-v4l/vidioc-create-bufs#rst-vidioc-create-bufs>) ioctl support is mandatory to enable [ioctl VIDIOC_REMOVE_BUFS](<#rst-vidioc-remove-bufs>). This ioctl is available if the `V4L2_BUF_CAP_SUPPORTS_REMOVE_BUFS` capability is set on the queue when `VIDIOC_REQBUFS()` or `VIDIOC_CREATE_BUFS()` are invoked.





<a id="c-v4l2_remove_buffers"></a>

```c
v4l2_remove_buffers
```

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->


<table>
<caption>struct v4l2_remove_buffers</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`index`

</td>
<td>


The starting buffer index to remove. This field is ignored if count == 0.

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


The number of buffers to be removed with indices 'index' until 'index + count - 1'. All buffers in this range must be valid and in DEQUEUED state. [ioctl VIDIOC_REMOVE_BUFS](<#rst-vidioc-remove-bufs>) will always check the validity of `type`, if it is invalid it returns `EINVAL` error code. If count is set to 0 [ioctl VIDIOC_REMOVE_BUFS](<#rst-vidioc-remove-bufs>) will do nothing and return 0.

</td>
</tr>
<tr>
<td>


\__u32

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


\__u32

</td>
<td>


`reserved`\[13\]

</td>
<td>


A place holder for future extensions. Drivers and applications must set the array to zero.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter. If an error occurs, no buffers will be freed and one of the error codes below will be returned:

- **EBUSY**

  File I/O is in progress. One or more of the buffers in the range `index` to `index + count - 1` are not in DEQUEUED state.

- **EINVAL**

  One or more of the buffers in the range `index` to `index + count - 1` do not exist in the queue. The buffer type (`type` field) is not valid.
