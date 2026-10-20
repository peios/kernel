---
title: "ioctl VIDIOC_G_INPUT, VIDIOC_S_INPUT"
type: reference
description: "VIDIOC_G_INPUT - VIDIOC_S_INPUT - Query or select the current video input"
---

<a id="rst-ioctl-vidioc-g-input-vidioc-s-input"></a>
<a id="rst-vidioc-g-input"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_G_INPUT - VIDIOC_S_INPUT - Query or select the current video input

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_G_INPUT"></a>

```c
VIDIOC_G_INPUT
```

`int ioctl(int fd, VIDIOC_G_INPUT, int *argp)`





<a id="c-VIDIOC_S_INPUT"></a>

```c
VIDIOC_S_INPUT
```

`int ioctl(int fd, VIDIOC_S_INPUT, int *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer an integer with input index.

<a id="rst-description"></a>

## Description

To query the current video input applications call the [VIDIOC_G_INPUT](<#rst-vidioc-g-input>) ioctl with a pointer to an integer where the driver stores the number of the input, as in the struct `v4l2_input` `index` field. This ioctl will fail only when there are no video inputs, returning `EINVAL`.

To select a video input applications store the number of the desired input in an integer and call the [VIDIOC_S_INPUT](<#rst-vidioc-g-input>) ioctl with a pointer to this integer. Side effects are possible. For example inputs may support different video standards, so the driver may implicitly switch the current standard. Because of these possible side effects applications must select an input before querying or negotiating any other parameters.

Information about video inputs is available using the [ioctl VIDIOC_ENUMINPUT](<~kernel/userspace/userspace-api/media-v4l/vidioc-enuminput#rst-vidioc-enuminput>) ioctl.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  The number of the video input is out of bounds.
