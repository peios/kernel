---
title: "Streaming Parameters"
type: reference
description: "Streaming parameters are intended to optimize the video capture process as well as I/O. Presently applications can request a high quality capture mode with the VIDIOC_S_PARM <VIDIOC_G_PARM> ioctl."
---

<a id="rst-streaming-parameters"></a>
<a id="rst-streaming-par"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

Streaming parameters are intended to optimize the video capture process as well as I/O. Presently applications can request a high quality capture mode with the [VIDIOC_S_PARM](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-parm#rst-vidioc-g-parm>) ioctl.

The current video standard determines a nominal number of frames per second. If less than this number of frames is to be captured or output, applications can request frame skipping or duplicating on the driver side. This is especially useful when using the `read()` or `write()`, which are not augmented by timestamps or sequence counters, and to avoid unnecessary data copying.

Finally these ioctls can be used to determine the number of buffers used internally by a driver in read/write mode. For implications see the section discussing the `read()` function.

To get and set the streaming parameters applications call the [VIDIOC_G_PARM](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-parm#rst-vidioc-g-parm>) and [VIDIOC_S_PARM](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-parm#rst-vidioc-g-parm>) ioctl, respectively. They take a pointer to a struct `v4l2_streamparm`, which contains a union holding separate parameters for input and output devices.

These ioctls are optional, drivers need not implement them. If so, they return the `EINVAL` error code.
