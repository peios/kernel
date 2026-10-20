---
title: "ioctls LIRC_GET_SEND_MODE and LIRC_SET_SEND_MODE"
type: reference
description: "LIRC_GET_SEND_MODE/LIRC_SET_SEND_MODE - Get/set current transmit mode."
---

<a id="rst-ioctls-lirc-get-send-mode-and-lirc-set-send-mode"></a>
<a id="rst-lirc-set-send-mode"></a>
<a id="rst-lirc-get-send-mode"></a>

<!-- SPDX-License-Identifier: GPL-2.0 OR GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: RC -->

<a id="rst-name"></a>

## Name

LIRC_GET_SEND_MODE/LIRC_SET_SEND_MODE - Get/set current transmit mode.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-LIRC_GET_SEND_MODE"></a>

```c
LIRC_GET_SEND_MODE
```

`int ioctl(int fd, LIRC_GET_SEND_MODE, __u32 *mode)`





<a id="c-LIRC_SET_SEND_MODE"></a>

```c
LIRC_SET_SEND_MODE
```

`int ioctl(int fd, LIRC_SET_SEND_MODE, __u32 *mode)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by open().

- **`mode`**

  The mode used for transmitting.

<a id="rst-description"></a>

## Description

Get/set current transmit mode.

Only [LIRC_MODE_PULSE](<~kernel/userspace/userspace-api/media-rc/lirc-dev-intro#rst-lirc-mode-pulse>) and [LIRC_MODE_SCANCODE](<~kernel/userspace/userspace-api/media-rc/lirc-dev-intro#rst-lirc-mode-scancode>) are supported by for IR send, depending on the driver. Use [ioctl LIRC_GET_FEATURES](<~kernel/userspace/userspace-api/media-rc/lirc-get-features#rst-lirc-get-features>) to find out which modes the driver supports.

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


Device does not support transmitting.

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
