---
title: "Radio Interface"
type: reference
description: "This interface is intended for AM and FM (analog) radio receivers and transmitters."
---

<a id="rst-radio-interface"></a>
<a id="rst-radio"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

This interface is intended for AM and FM (analog) radio receivers and transmitters.

Conventionally V4L2 radio devices are accessed through character device special files named `/dev/radio` and `/dev/radio0` to `/dev/radio63` with major number 81 and minor numbers 64 to 127.

<a id="rst-querying-capabilities"></a>

## Querying Capabilities

Devices supporting the radio interface set the `V4L2_CAP_RADIO` and `V4L2_CAP_TUNER` or `V4L2_CAP_MODULATOR` flag in the `capabilities` field of struct `v4l2_capability` returned by the [ioctl VIDIOC_QUERYCAP](<~kernel/userspace/userspace-api/media-v4l/vidioc-querycap#rst-vidioc-querycap>) ioctl. Other combinations of capability flags are reserved for future extensions.

<a id="rst-supplemental-functions"></a>

## Supplemental Functions

Radio devices can support [controls](<~kernel/userspace/userspace-api/media-v4l/control#rst-control>), and must support the [tuner or modulator](<~kernel/userspace/userspace-api/media-v4l/tuner#rst-tuner>) ioctls.

They do not support the video input or output, audio input or output, video standard, cropping and scaling, compression and streaming parameter, or overlay ioctls. All other ioctls and I/O methods are reserved for future extensions.

<a id="rst-programming"></a>

## Programming

Radio devices may have a couple audio controls (as discussed in [User Controls](<~kernel/userspace/userspace-api/media-v4l/control#rst-control>)) such as a volume control, possibly custom controls. Further all radio devices have one tuner or modulator (these are discussed in [Tuners and Modulators](<~kernel/userspace/userspace-api/media-v4l/tuner#rst-tuner>)) with index number zero to select the radio frequency and to determine if a monaural or FM stereo program is received/emitted. Drivers switch automatically between AM and FM depending on the selected frequency. The [VIDIOC_G_TUNER](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-g-tuner.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) or [VIDIOC_G_MODULATOR](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-modulator#rst-vidioc-g-modulator>) ioctl reports the supported frequency range.
