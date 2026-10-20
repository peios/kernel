---
title: "ioctl VIDIOC_G_OUTPUT, VIDIOC_S_OUTPUT"
type: reference
description: "VIDIOC_G_OUTPUT - VIDIOC_S_OUTPUT - Query or select the current video output"
---

<a id="rst-ioctl-vidioc-g-output-vidioc-s-output"></a>
<a id="rst-vidioc-g-output"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_G_OUTPUT - VIDIOC_S_OUTPUT - Query or select the current video output

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_G_OUTPUT"></a>

```c
VIDIOC_G_OUTPUT
```

`int ioctl(int fd, VIDIOC_G_OUTPUT, int *argp)`





<a id="c-VIDIOC_S_OUTPUT"></a>

```c
VIDIOC_S_OUTPUT
```

`int ioctl(int fd, VIDIOC_S_OUTPUT, int *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to an integer with output index.

<a id="rst-description"></a>

## Description

To query the current video output applications call the [VIDIOC_G_OUTPUT](<#rst-vidioc-g-output>) ioctl with a pointer to an integer where the driver stores the number of the output, as in the struct `v4l2_output` `index` field. This ioctl will fail only when there are no video outputs, returning the `EINVAL` error code.

To select a video output applications store the number of the desired output in an integer and call the [VIDIOC_S_OUTPUT](<#rst-vidioc-g-output>) ioctl with a pointer to this integer. Side effects are possible. For example outputs may support different video standards, so the driver may implicitly switch the current standard. Because of these possible side effects applications must select an output before querying or negotiating any other parameters.

Information about video outputs is available using the [ioctl VIDIOC_ENUMOUTPUT](<~kernel/userspace/userspace-api/media-v4l/vidioc-enumoutput#rst-vidioc-enumoutput>) ioctl.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  The number of the video output is out of bounds, or there are no video outputs at all.
