---
title: "ioctl VIDIOC_DBG_G_REGISTER, VIDIOC_DBG_S_REGISTER"
type: reference
description: "VIDIOC_DBG_G_REGISTER - VIDIOC_DBG_S_REGISTER - Read or write hardware registers"
---

<a id="rst-ioctl-vidioc-dbg-g-register-vidioc-dbg-s-register"></a>
<a id="rst-vidioc-dbg-g-register"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_DBG_G_REGISTER - VIDIOC_DBG_S_REGISTER - Read or write hardware registers

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_DBG_G_REGISTER"></a>

```c
VIDIOC_DBG_G_REGISTER
```

`int ioctl(int fd, VIDIOC_DBG_G_REGISTER, struct v4l2_dbg_register *argp)`





<a id="c-VIDIOC_DBG_S_REGISTER"></a>

```c
VIDIOC_DBG_S_REGISTER
```

`int ioctl(int fd, VIDIOC_DBG_S_REGISTER, const struct v4l2_dbg_register *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_dbg_register`.

<a id="rst-description"></a>

## Description

> [!NOTE]
>
> This is an [Experimental API Elements](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/hist-v4l2.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) interface and may change in the future.

For driver debugging purposes these ioctls allow test applications to access hardware registers directly. Regular applications must not use them.

Since writing or even reading registers can jeopardize the system security, its stability and damage the hardware, both ioctls require superuser privileges. Additionally the Linux kernel must be compiled with the `CONFIG_VIDEO_ADV_DEBUG` option to enable these ioctls.

To write a register applications must initialize all fields of a struct `v4l2_dbg_register` except for `size` and call `VIDIOC_DBG_S_REGISTER` with a pointer to this structure. The `match.type` and `match.addr` or `match.name` fields select a chip on the TV card, the `reg` field specifies a register number and the `val` field the value to be written into the register.

To read a register applications must initialize the `match.type`, `match.addr` or `match.name` and `reg` fields, and call `VIDIOC_DBG_G_REGISTER` with a pointer to this structure. On success the driver stores the register value in the `val` field and the size (in bytes) of the value in `size`.

When `match.type` is `V4L2_CHIP_MATCH_BRIDGE`, `match.addr` selects the nth non-sub-device chip on the TV card. The number zero always selects the host chip, e. g. the chip connected to the PCI or USB bus. You can find out which chips are present with the [ioctl VIDIOC_DBG_G_CHIP_INFO](<~kernel/userspace/userspace-api/media-v4l/vidioc-dbg-g-chip-info#rst-vidioc-dbg-g-chip-info>) ioctl.

When `match.type` is `V4L2_CHIP_MATCH_SUBDEV`, `match.addr` selects the nth sub-device.

These ioctls are optional, not all drivers may support them. However when a driver supports these ioctls it must also support [ioctl VIDIOC_DBG_G_CHIP_INFO](<~kernel/userspace/userspace-api/media-v4l/vidioc-dbg-g-chip-info#rst-vidioc-dbg-g-chip-info>). Conversely it may support `VIDIOC_DBG_G_CHIP_INFO` but not these ioctls.

`VIDIOC_DBG_G_REGISTER` and `VIDIOC_DBG_S_REGISTER` were introduced in Linux 2.6.21, but their API was changed to the one described here in kernel 2.6.29.

We recommended the v4l2-dbg utility over calling these ioctls directly. It is available from the LinuxTV v4l-dvb repository; see [https://linuxtv.org/repo/](<https://linuxtv.org/repo/>) for access instructions.

<!-- tabularcolumns: |p{3.5cm}|p{3.5cm}|p{3.5cm}|p{6.6cm}| -->





<a id="c-v4l2_dbg_match"></a>

```c
v4l2_dbg_match
```


<table>
<caption>struct v4l2_dbg_match</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`type`

</td>
<td>


See [chip-match-types](<#rst-chip-match-types>) for a list of possible types.

</td>
</tr>
<tr>
<td>


union \{

</td>
<td colspan="2">


(anonymous)

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`addr`

</td>
<td>


Match a chip by this number, interpreted according to the `type` field.

</td>
</tr>
<tr>
<td>


char

</td>
<td>


`name[32]`

</td>
<td>


Match a chip by this name, interpreted according to the `type` field. Currently unused.

</td>
</tr>
<tr>
<td>


\}

</td>
<td colspan="2">




</td>
</tr>
</tbody>
</table>





<a id="c-v4l2_dbg_register"></a>

```c
v4l2_dbg_register
```


<table>
<caption>struct v4l2_dbg_register</caption>
<tbody>
<tr>
<td>


struct v4l2_dbg_match

</td>
<td>


`match`

</td>
<td>


How to match the chip, see `v4l2_dbg_match`.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`size`

</td>
<td>


The register size in bytes.

</td>
</tr>
<tr>
<td>


\__u64

</td>
<td>


`reg`

</td>
<td>


A register number.

</td>
</tr>
<tr>
<td>


\__u64

</td>
<td>


`val`

</td>
<td>


The value read from, or to be written into the register.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{6.6cm}|p{2.2cm}|p{8.5cm}| -->

<a id="rst-chip-match-types"></a>


<table>
<caption>Chip Match Types</caption>
<tbody>
<tr>
<td>


`V4L2_CHIP_MATCH_BRIDGE`

</td>
<td>


0

</td>
<td>


Match the nth chip on the card, zero for the bridge chip. Does not match sub-devices.

</td>
</tr>
<tr>
<td>


`V4L2_CHIP_MATCH_SUBDEV`

</td>
<td>


4

</td>
<td>


Match the nth sub-device.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EPERM**

  Insufficient permissions. Root privileges are required to execute these ioctls.
