---
title: "ioctl VIDIOC_ENUMAUDOUT"
type: reference
description: "VIDIOC_ENUMAUDOUT - Enumerate audio outputs"
---

<a id="rst-ioctl-vidioc-enumaudout"></a>
<a id="rst-vidioc-enumaudout"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_ENUMAUDOUT - Enumerate audio outputs

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_ENUMAUDOUT"></a>

```c
VIDIOC_ENUMAUDOUT
```

`int ioctl(int fd, VIDIOC_ENUMAUDOUT, struct v4l2_audioout *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_audioout`.

<a id="rst-description"></a>

## Description

To query the attributes of an audio output applications initialize the `index` field and zero out the `reserved` array of a struct `v4l2_audioout` and call the `VIDIOC_G_AUDOUT` ioctl with a pointer to this structure. Drivers fill the rest of the structure or return an `EINVAL` error code when the index is out of bounds. To enumerate all audio outputs applications shall begin at index zero, incrementing by one until the driver returns `EINVAL`.

> [!NOTE]
>
> Connectors on a TV card to loop back the received audio signal to a sound card are not audio outputs in this sense.

See [VIDIOC_G_AUDIOout](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-audioout#rst-vidioc-g-audout>) for a description of struct `v4l2_audioout`.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  The number of the audio output is out of bounds.
