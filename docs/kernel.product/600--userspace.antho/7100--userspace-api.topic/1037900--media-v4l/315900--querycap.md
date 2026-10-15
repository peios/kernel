---
title: "Querying Capabilities"
type: reference
description: "Because V4L2 covers a wide variety of devices not all aspects of the API are equally applicable to all types of devices. Furthermore devices of the same type have different capabilities and this specification permits the omission of a few…"
---

<a id="rst-querying-capabilities"></a>
<a id="rst-querycap"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

Because V4L2 covers a wide variety of devices not all aspects of the API are equally applicable to all types of devices. Furthermore devices of the same type have different capabilities and this specification permits the omission of a few complicated and less important parts of the API.

The [ioctl VIDIOC_QUERYCAP](<~kernel/userspace/userspace-api/media-v4l/vidioc-querycap#rst-vidioc-querycap>) ioctl is available to check if the kernel device is compatible with this specification, and to query the [functions](<~kernel/userspace/userspace-api/media-v4l/devices#rst-devices>) and [I/O methods](<~kernel/userspace/userspace-api/media-v4l/io#rst-io>) supported by the device.

Starting with kernel version 3.1, [ioctl VIDIOC_QUERYCAP](<~kernel/userspace/userspace-api/media-v4l/vidioc-querycap#rst-vidioc-querycap>) will return the V4L2 API version used by the driver, with generally matches the Kernel version. There's no need of using [ioctl VIDIOC_QUERYCAP](<~kernel/userspace/userspace-api/media-v4l/vidioc-querycap#rst-vidioc-querycap>) to check if a specific ioctl is supported, the V4L2 core now returns `ENOTTY` if a driver doesn't provide support for an ioctl.

Other features can be queried by calling the respective ioctl, for example [ioctl VIDIOC_ENUMINPUT](<~kernel/userspace/userspace-api/media-v4l/vidioc-enuminput#rst-vidioc-enuminput>) to learn about the number, types and names of video connectors on the device. Although abstraction is a major objective of this API, the [ioctl VIDIOC_QUERYCAP](<~kernel/userspace/userspace-api/media-v4l/vidioc-querycap#rst-vidioc-querycap>) ioctl also allows driver specific applications to reliably identify the driver.

All V4L2 drivers must support [ioctl VIDIOC_QUERYCAP](<~kernel/userspace/userspace-api/media-v4l/vidioc-querycap#rst-vidioc-querycap>). Applications should always call this ioctl after opening the device.
