---
title: "ioctl VIDIOC_ENUMAUDIO"
type: reference
description: "VIDIOC_ENUMAUDIO - Enumerate audio inputs"
---

<a id="rst-ioctl-vidioc-enumaudio"></a>
<a id="rst-vidioc-enumaudio"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_ENUMAUDIO - Enumerate audio inputs

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_ENUMAUDIO"></a>

```c
VIDIOC_ENUMAUDIO
```

`int ioctl(int fd, VIDIOC_ENUMAUDIO, struct v4l2_audio *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_audio`.

<a id="rst-description"></a>

## Description

To query the attributes of an audio input applications initialize the `index` field and zero out the `reserved` array of a struct `v4l2_audio` and call the [ioctl VIDIOC_ENUMAUDIO](<#rst-vidioc-enumaudio>) ioctl with a pointer to this structure. Drivers fill the rest of the structure or return an `EINVAL` error code when the index is out of bounds. To enumerate all audio inputs applications shall begin at index zero, incrementing by one until the driver returns `EINVAL`.

See [VIDIOC_G_AUDIO](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-audio#rst-vidioc-g-audio>) for a description of struct `v4l2_audio`.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  The number of the audio input is out of bounds.
