---
title: "ioctls LIRC_GET_REC_MODE and LIRC_SET_REC_MODE"
type: reference
description: "LIRC_GET_REC_MODE/LIRC_SET_REC_MODE - Get/set current receive mode."
---

<a id="rst-ioctls-lirc-get-rec-mode-and-lirc-set-rec-mode"></a>
<a id="rst-lirc-set-rec-mode"></a>
<a id="rst-lirc-get-rec-mode"></a>

<!-- SPDX-License-Identifier: GPL-2.0 OR GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: RC -->

<a id="rst-name"></a>

## Name

LIRC_GET_REC_MODE/LIRC_SET_REC_MODE - Get/set current receive mode.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-LIRC_GET_REC_MODE"></a>

```c
LIRC_GET_REC_MODE
```

`int ioctl(int fd, LIRC_GET_REC_MODE, __u32 *mode)`





<a id="c-LIRC_SET_REC_MODE"></a>

```c
LIRC_SET_REC_MODE
```

`int ioctl(int fd, LIRC_SET_REC_MODE, __u32 *mode)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by open().

- **`mode`**

  Mode used for receive.

<a id="rst-description"></a>

## Description

Get and set the current receive mode. Only [LIRC_MODE_MODE2](<~kernel/userspace/userspace-api/media-rc/lirc-dev-intro#rst-lirc-mode-mode2>) and [LIRC_MODE_SCANCODE](<~kernel/userspace/userspace-api/media-rc/lirc-dev-intro#rst-lirc-mode-scancode>) are supported. Use [ioctl LIRC_GET_FEATURES](<~kernel/userspace/userspace-api/media-rc/lirc-get-features#rst-lirc-get-features>) to find out which modes the driver supports.

<a id="rst-return-value"></a>

## Return Value

<!-- tabularcolumns: |p{2.5cm}|p{15.0cm}| -->


<table>
<tbody>
<tr>
<td>


`ENODEV`

</td>
<td>


Device not available.

</td>
</tr>
<tr>
<td>


`ENOTTY`

</td>
<td>


Device does not support receiving.

</td>
</tr>
<tr>
<td>


`EINVAL`

</td>
<td>


Invalid mode or invalid mode for this device.

</td>
</tr>
</tbody>
</table>
