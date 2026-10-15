---
title: "ioctl VIDIOC_G_CROP, VIDIOC_S_CROP"
type: reference
description: "VIDIOC_G_CROP - VIDIOC_S_CROP - Get or set the current cropping rectangle"
---

<a id="rst-ioctl-vidioc-g-crop-vidioc-s-crop"></a>
<a id="rst-vidioc-g-crop"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_G_CROP - VIDIOC_S_CROP - Get or set the current cropping rectangle

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_G_CROP"></a>

```c
VIDIOC_G_CROP
```

`int ioctl(int fd, VIDIOC_G_CROP, struct v4l2_crop *argp)`





<a id="c-VIDIOC_S_CROP"></a>

```c
VIDIOC_S_CROP
```

`int ioctl(int fd, VIDIOC_S_CROP, const struct v4l2_crop *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_crop`.

<a id="rst-description"></a>

## Description

To query the cropping rectangle size and position applications set the `type` field of a struct `v4l2_crop` structure to the respective buffer (stream) type and call the [VIDIOC_G_CROP](<#rst-vidioc-g-crop>) ioctl with a pointer to this structure. The driver fills the rest of the structure or returns the `EINVAL` error code if cropping is not supported.

To change the cropping rectangle applications initialize the `type` and struct `v4l2_rect` substructure named `c` of a v4l2_crop structure and call the [VIDIOC_S_CROP](<#rst-vidioc-g-crop>) ioctl with a pointer to this structure.

The driver first adjusts the requested dimensions against hardware limits, i. e. the bounds given by the capture/output window, and it rounds to the closest possible values of horizontal and vertical offset, width and height. In particular the driver must round the vertical offset of the cropping rectangle to frame lines modulo two, such that the field order cannot be confused.

Second the driver adjusts the image size (the opposite rectangle of the scaling process, source or target depending on the data direction) to the closest size possible while maintaining the current horizontal and vertical scaling factor.

Finally the driver programs the hardware with the actual cropping and image parameters. [VIDIOC_S_CROP](<#rst-vidioc-g-crop>) is a write-only ioctl, it does not return the actual parameters. To query them applications must call [VIDIOC_G_CROP](<#rst-vidioc-g-crop>) and [ioctl VIDIOC_G_FMT, VIDIOC_S_FMT, VIDIOC_TRY_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>). When the parameters are unsuitable the application may modify the cropping or image parameters and repeat the cycle until satisfactory parameters have been negotiated.

When cropping is not supported then no parameters are changed and [VIDIOC_S_CROP](<#rst-vidioc-g-crop>) returns the `EINVAL` error code.





<a id="c-v4l2_crop"></a>

```c
v4l2_crop
```

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->


<table>
<caption>struct v4l2_crop</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`type`

</td>
<td>


Type of the data stream, set by the application. Only these types are valid here: `V4L2_BUF_TYPE_VIDEO_CAPTURE`, `V4L2_BUF_TYPE_VIDEO_CAPTURE_MPLANE`, `V4L2_BUF_TYPE_VIDEO_OUTPUT`, `V4L2_BUF_TYPE_VIDEO_OUTPUT_MPLANE` and `V4L2_BUF_TYPE_VIDEO_OVERLAY`. See `v4l2_buf_type` and the note below.

</td>
</tr>
<tr>
<td>


struct `v4l2_rect`

</td>
<td>


`c`

</td>
<td>


Cropping rectangle. The same co-ordinate system as for struct `v4l2_cropcap` `bounds` is used.

</td>
</tr>
</tbody>
</table>

> [!NOTE]
>
> Unfortunately in the case of multiplanar buffer types (`V4L2_BUF_TYPE_VIDEO_CAPTURE_MPLANE` and `V4L2_BUF_TYPE_VIDEO_OUTPUT_MPLANE`) this API was messed up with regards to how the `v4l2_crop` `type` field should be filled in. Some drivers only accepted the `_MPLANE` buffer type while other drivers only accepted a non-multiplanar buffer type (i.e. without the `_MPLANE` at the end).
>
> Starting with kernel 4.13 both variations are allowed.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **ENODATA**

  Cropping is not supported for this input or output.
