---
title: "ioctl VIDIOC_SUBDEV_QUERYCAP"
type: reference
description: "VIDIOC_SUBDEV_QUERYCAP - Query sub-device capabilities"
---

<a id="rst-ioctl-vidioc-subdev-querycap"></a>
<a id="rst-vidioc-subdev-querycap"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_SUBDEV_QUERYCAP - Query sub-device capabilities

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_SUBDEV_QUERYCAP"></a>

```c
VIDIOC_SUBDEV_QUERYCAP
```

`int ioctl(int fd, VIDIOC_SUBDEV_QUERYCAP, struct v4l2_subdev_capability *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_subdev_capability`.

<a id="rst-description"></a>

## Description

All V4L2 sub-devices support the `VIDIOC_SUBDEV_QUERYCAP` ioctl. It is used to identify kernel devices compatible with this specification and to obtain information about driver and hardware capabilities. The ioctl takes a pointer to a struct `v4l2_subdev_capability` which is filled by the driver. When the driver is not compatible with this specification the ioctl returns `ENOTTY` error code.

<!-- tabularcolumns: |p{1.5cm}|p{2.9cm}|p{12.9cm}| -->





<a id="c-v4l2_subdev_capability"></a>

```c
v4l2_subdev_capability
```


<table>
<caption>struct v4l2_subdev_capability</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`version`

</td>
<td>


Version number of the driver.

The version reported is provided by the V4L2 subsystem following the kernel numbering scheme. However, it may not always return the same version as the kernel if, for example, a stable or distribution-modified kernel uses the V4L2 stack from a newer kernel.

The version number is formatted using the `KERNEL_VERSION()` macro:

</td>
</tr>
<tr>
<td colspan="3">


`#define KERNEL_VERSION(a,b,c) (((a) << 16) + ((b) << 8) + (c))`

`__u32 version = KERNEL_VERSION(0, 8, 1);`

`printf ("Version: %u.%u.%u\\n",`

`(version >> 16) & 0xFF, (version >> 8) & 0xFF, version & 0xFF);`

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


Sub-device capabilities of the opened device, see [subdevice-capabilities](<#rst-subdevice-capabilities>).

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`reserved`\[14\]

</td>
<td>


Reserved for future extensions. Set to 0 by the V4L2 core.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{6.8cm}|p{2.4cm}|p{8.1cm}| -->

<a id="rst-subdevice-capabilities"></a>


<table>
<caption>Sub-Device Capabilities Flags</caption>
<tbody>
<tr>
<td>


V4L2_SUBDEV_CAP_RO_SUBDEV

</td>
<td>


0x00000001

</td>
<td>


The sub-device device node is registered in read-only mode. Access to the sub-device ioctls that modify the device state is restricted. Refer to each individual subdevice ioctl documentation for a description of which restrictions apply to a read-only sub-device.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **ENOTTY**

  The device node is not a V4L2 sub-device.
