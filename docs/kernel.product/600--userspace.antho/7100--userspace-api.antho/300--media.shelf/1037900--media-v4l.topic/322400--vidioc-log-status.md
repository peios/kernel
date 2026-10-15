---
title: "ioctl VIDIOC_LOG_STATUS"
type: reference
description: "VIDIOC_LOG_STATUS - Log driver status information"
---

<a id="rst-ioctl-vidioc-log-status"></a>
<a id="rst-vidioc-log-status"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_LOG_STATUS - Log driver status information

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_LOG_STATUS"></a>

```c
VIDIOC_LOG_STATUS
```

`int ioctl(int fd, VIDIOC_LOG_STATUS)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

<a id="rst-description"></a>

## Description

As the video/audio devices become more complicated it becomes harder to debug problems. When this ioctl is called the driver will output the current device status to the kernel log. This is particular useful when dealing with problems like no sound, no video and incorrectly tuned channels. Also many modern devices autodetect video and audio standards and this ioctl will report what the device thinks what the standard is. Mismatches may give an indication where the problem is.

This ioctl is optional and not all drivers support it. It was introduced in Linux 2.6.15.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
