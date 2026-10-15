---
title: "ioctl VIDIOC_DBG_G_CHIP_INFO"
type: reference
description: "VIDIOC_DBG_G_CHIP_INFO - Identify the chips on a TV card"
---

<a id="rst-ioctl-vidioc-dbg-g-chip-info"></a>
<a id="rst-vidioc-dbg-g-chip-info"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_DBG_G_CHIP_INFO - Identify the chips on a TV card

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_DBG_G_CHIP_INFO"></a>

```c
VIDIOC_DBG_G_CHIP_INFO
```

`int ioctl(int fd, VIDIOC_DBG_G_CHIP_INFO, struct v4l2_dbg_chip_info *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_dbg_chip_info`.

<a id="rst-description"></a>

## Description

> [!NOTE]
>
> This is an [Experimental API Elements](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/hist-v4l2.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) interface and may change in the future.

For driver debugging purposes this ioctl allows test applications to query the driver about the chips present on the TV card. Regular applications must not use it. When you found a chip specific bug, please contact the linux-media mailing list ([https://linuxtv.org/lists.php](<https://linuxtv.org/lists.php>)) so it can be fixed.

Additionally the Linux kernel must be compiled with the `CONFIG_VIDEO_ADV_DEBUG` option to enable this ioctl.

To query the driver applications must initialize the `match.type` and `match.addr` or `match.name` fields of a struct `v4l2_dbg_chip_info` and call [ioctl VIDIOC_DBG_G_CHIP_INFO](<#rst-vidioc-dbg-g-chip-info>) with a pointer to this structure. On success the driver stores information about the selected chip in the `name` and `flags` fields.

When `match.type` is `V4L2_CHIP_MATCH_BRIDGE`, `match.addr` selects the nth bridge 'chip' on the TV card. You can enumerate all chips by starting at zero and incrementing `match.addr` by one until [ioctl VIDIOC_DBG_G_CHIP_INFO](<#rst-vidioc-dbg-g-chip-info>) fails with an `EINVAL` error code. The number zero always selects the bridge chip itself, e. g. the chip connected to the PCI or USB bus. Non-zero numbers identify specific parts of the bridge chip such as an AC97 register block.

When `match.type` is `V4L2_CHIP_MATCH_SUBDEV`, `match.addr` selects the nth sub-device. This allows you to enumerate over all sub-devices.

On success, the `name` field will contain a chip name and the `flags` field will contain `V4L2_CHIP_FL_READABLE` if the driver supports reading registers from the device or `V4L2_CHIP_FL_WRITABLE` if the driver supports writing registers to the device.

We recommended the v4l2-dbg utility over calling this ioctl directly. It is available from the LinuxTV v4l-dvb repository; see [https://linuxtv.org/repo/](<https://linuxtv.org/repo/>) for access instructions.

<!-- tabularcolumns: |p{3.5cm}|p{3.5cm}|p{3.5cm}|p{6.6cm}| -->

<a id="rst-name-v4l2-dbg-match"></a>


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


See [name-chip-match-types](<#rst-name-chip-match-types>) for a list of possible types.

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

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->





<a id="c-v4l2_dbg_chip_info"></a>

```c
v4l2_dbg_chip_info
```


<table>
<caption>struct v4l2_dbg_chip_info</caption>
<tbody>
<tr>
<td>


struct v4l2_dbg_match

</td>
<td>


`match`

</td>
<td>


How to match the chip, see [name-v4l2-dbg-match](<#rst-name-v4l2-dbg-match>).

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


The name of the chip.

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


Set by the driver. If `V4L2_CHIP_FL_READABLE` is set, then the driver supports reading registers from the device. If `V4L2_CHIP_FL_WRITABLE` is set, then it supports writing registers.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`reserved[8]`

</td>
<td>


Reserved fields, both application and driver must set these to 0.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{6.6cm}|p{2.2cm}|p{8.5cm}| -->

<a id="rst-name-chip-match-types"></a>


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

- **EINVAL**

  The `match_type` is invalid or no device could be matched.
