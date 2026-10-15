---
title: "ioctl VIDIOC_SUBDEV_G_CLIENT_CAP, VIDIOC_SUBDEV_S_CLIENT_CAP"
type: reference
description: "VIDIOC_SUBDEV_G_CLIENT_CAP - VIDIOC_SUBDEV_S_CLIENT_CAP - Get or set client capabilities."
---

<a id="rst-ioctl-vidioc-subdev-g-client-cap-vidioc-subdev-s-client-cap"></a>
<a id="rst-vidioc-subdev-g-client-cap"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_SUBDEV_G_CLIENT_CAP - VIDIOC_SUBDEV_S_CLIENT_CAP - Get or set client capabilities.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_SUBDEV_G_CLIENT_CAP"></a>

```c
VIDIOC_SUBDEV_G_CLIENT_CAP
```

`int ioctl(int fd, VIDIOC_SUBDEV_G_CLIENT_CAP, struct v4l2_subdev_client_capability *argp)`





<a id="c-VIDIOC_SUBDEV_S_CLIENT_CAP"></a>

```c
VIDIOC_SUBDEV_S_CLIENT_CAP
```

`int ioctl(int fd, VIDIOC_SUBDEV_S_CLIENT_CAP, struct v4l2_subdev_client_capability *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by [open()](<~kernel/userspace/userspace-api/media-v4l/func-open#rst-func-open>).

- **`argp`**

  Pointer to struct `v4l2_subdev_client_capability`.

<a id="rst-description"></a>

## Description

These ioctls are used to get and set the client (the application using the subdevice ioctls) capabilities. The client capabilities are stored in the file handle of the opened subdev device node, and the client must set the capabilities for each opened subdev separately.

By default no client capabilities are set when a subdev device node is opened.

The purpose of the client capabilities are to inform the kernel of the behavior of the client, mainly related to maintaining compatibility with different kernel and userspace versions.

The `VIDIOC_SUBDEV_G_CLIENT_CAP` ioctl returns the current client capabilities associated with the file handle `fd`.

The `VIDIOC_SUBDEV_S_CLIENT_CAP` ioctl sets client capabilities for the file handle `fd`. The new capabilities fully replace the current capabilities, the ioctl can therefore also be used to remove capabilities that have previously been set.

`VIDIOC_SUBDEV_S_CLIENT_CAP` modifies the struct `v4l2_subdev_client_capability` to reflect the capabilities that have been accepted. A common case for the kernel not accepting a capability is that the kernel is older than the headers the userspace uses, and thus the capability is unknown to the kernel.

<!-- tabularcolumns: |p{1.5cm}|p{2.9cm}|p{12.9cm}| -->





<a id="c-v4l2_subdev_client_capability"></a>

```c
v4l2_subdev_client_capability
```


<table>
<caption>struct v4l2_subdev_client_capability</caption>
<tbody>
<tr>
<td>


\__u64

</td>
<td>


`capabilities`

</td>
<td>


Sub-device client capabilities of the opened device.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{6.8cm}|p{2.4cm}|p{8.1cm}| -->


<table>
<caption>Client Capabilities</caption>
<thead>
<tr>
<th>


Capability

</th>
<th>


Description

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


`V4L2_SUBDEV_CLIENT_CAP_STREAMS`

</td>
<td>


The client is aware of streams. Setting this flag enables the use of 'stream' fields (referring to the stream number) with various ioctls. If this is not set (which is the default), the 'stream' fields will be forced to 0 by the kernel.

</td>
</tr>
<tr>
<td>


`V4L2_SUBDEV_CLIENT_CAP_INTERVAL_USES_WHICH`

</td>
<td>


The client is aware of the `v4l2_subdev_frame_interval` `which` field. If this is not set (which is the default), the `which` field is forced to `V4L2_SUBDEV_FORMAT_ACTIVE` by the kernel.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **ENOIOCTLCMD**

  The kernel does not support this ioctl.
