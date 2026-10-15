---
title: "ioctl VIDIOC_G_FMT, VIDIOC_S_FMT, VIDIOC_TRY_FMT"
type: reference
description: "VIDIOC_G_FMT - VIDIOC_S_FMT - VIDIOC_TRY_FMT - Get or set the data format, try a format"
---

<a id="rst-ioctl-vidioc-g-fmt-vidioc-s-fmt-vidioc-try-fmt"></a>
<a id="rst-vidioc-g-fmt"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_G_FMT - VIDIOC_S_FMT - VIDIOC_TRY_FMT - Get or set the data format, try a format

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_G_FMT"></a>

```c
VIDIOC_G_FMT
```

`int ioctl(int fd, VIDIOC_G_FMT, struct v4l2_format *argp)`





<a id="c-VIDIOC_S_FMT"></a>

```c
VIDIOC_S_FMT
```

`int ioctl(int fd, VIDIOC_S_FMT, struct v4l2_format *argp)`





<a id="c-VIDIOC_TRY_FMT"></a>

```c
VIDIOC_TRY_FMT
```

`int ioctl(int fd, VIDIOC_TRY_FMT, struct v4l2_format *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_format`.

<a id="rst-description"></a>

## Description

These ioctls are used to negotiate the format of data (typically image format) exchanged between driver and application.

To query the current parameters applications set the `type` field of a struct `v4l2_format` to the respective buffer (stream) type. For example video capture devices use `V4L2_BUF_TYPE_VIDEO_CAPTURE` or `V4L2_BUF_TYPE_VIDEO_CAPTURE_MPLANE`. When the application calls the [VIDIOC_G_FMT](<#rst-vidioc-g-fmt>) ioctl with a pointer to this structure the driver fills the respective member of the `fmt` union. In case of video capture devices that is either the struct `v4l2_pix_format` `pix` or the struct `v4l2_pix_format_mplane` `pix_mp` member. When the requested buffer type is not supported drivers return an `EINVAL` error code.

To change the current format parameters applications initialize the `type` field and all fields of the respective `fmt` union member. For details see the documentation of the various devices types in [Interfaces](<~kernel/userspace/userspace-api/media-v4l/devices#rst-devices>). Good practice is to query the current parameters first, and to modify only those parameters not suitable for the application. When the application calls the [VIDIOC_S_FMT](<#rst-vidioc-g-fmt>) ioctl with a pointer to a struct `v4l2_format` structure the driver checks and adjusts the parameters against hardware abilities. Drivers should not return an error code unless the `type` field is invalid, this is a mechanism to fathom device capabilities and to approach parameters acceptable for both the application and driver. On success the driver may program the hardware, allocate resources and generally prepare for data exchange. Finally the [VIDIOC_S_FMT](<#rst-vidioc-g-fmt>) ioctl returns the current format parameters as [VIDIOC_G_FMT](<#rst-vidioc-g-fmt>) does. Very simple, inflexible devices may even ignore all input and always return the default parameters. However all V4L2 devices exchanging data with the application must implement the [VIDIOC_G_FMT](<#rst-vidioc-g-fmt>) and [VIDIOC_S_FMT](<#rst-vidioc-g-fmt>) ioctl. When the requested buffer type is not supported drivers return an EINVAL error code on a [VIDIOC_S_FMT](<#rst-vidioc-g-fmt>) attempt. When I/O is already in progress or the resource is not available for other reasons drivers return the `EBUSY` error code.

The [VIDIOC_TRY_FMT](<#rst-vidioc-g-fmt>) ioctl is equivalent to [VIDIOC_S_FMT](<#rst-vidioc-g-fmt>) with one exception: it does not change driver state. It can also be called at any time, never returning `EBUSY`. This function is provided to negotiate parameters, to learn about hardware limitations, without disabling I/O or possibly time consuming hardware preparations. Although strongly recommended drivers are not required to implement this ioctl.

The format as returned by [VIDIOC_TRY_FMT](<#rst-vidioc-g-fmt>) must be identical to what [VIDIOC_S_FMT](<#rst-vidioc-g-fmt>) returns for the same input or output.





<a id="c-v4l2_format"></a>

```c
v4l2_format
```

<!-- tabularcolumns: |p{7.4cm}|p{4.4cm}|p{5.5cm}| -->


<table>
<caption>struct v4l2_format</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`type`

</td>
<td>


Type of the data stream, see `v4l2_buf_type`.

</td>
</tr>
<tr>
<td>


union \{

</td>
<td colspan="2">


`fmt`

</td>
</tr>
<tr>
<td>


struct `v4l2_pix_format`

</td>
<td>


`pix`

</td>
<td>


Definition of an image format, see [Image Formats](<~kernel/userspace/userspace-api/media-v4l/pixfmt#rst-pixfmt>), used by video capture and output devices.

</td>
</tr>
<tr>
<td>


struct `v4l2_pix_format_mplane`

</td>
<td>


`pix_mp`

</td>
<td>


Definition of an image format, see [Image Formats](<~kernel/userspace/userspace-api/media-v4l/pixfmt#rst-pixfmt>), used by video capture and output devices that support the [multi-planar version of the API](<~kernel/userspace/userspace-api/media-v4l/planar-apis#rst-planar-apis>).

</td>
</tr>
<tr>
<td>


struct `v4l2_window`

</td>
<td>


`win`

</td>
<td>


Definition of an overlaid image, see [Video Overlay Interface](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/dev-overlay.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>), used by video overlay devices.

</td>
</tr>
<tr>
<td>


struct `v4l2_vbi_format`

</td>
<td>


`vbi`

</td>
<td>


Raw VBI capture or output parameters. This is discussed in more detail in [Raw VBI Data Interface](<~kernel/userspace/userspace-api/media-v4l/dev-raw-vbi#rst-raw-vbi>). Used by raw VBI capture and output devices.

</td>
</tr>
<tr>
<td>


struct `v4l2_sliced_vbi_format`

</td>
<td>


`sliced`

</td>
<td>


Sliced VBI capture or output parameters. See [sliced](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/dev-sliced-vbi.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) for details. Used by sliced VBI capture and output devices.

</td>
</tr>
<tr>
<td>


struct `v4l2_sdr_format`

</td>
<td>


`sdr`

</td>
<td>


Definition of a data format, see [Image Formats](<~kernel/userspace/userspace-api/media-v4l/pixfmt#rst-pixfmt>), used by SDR capture and output devices.

</td>
</tr>
<tr>
<td>


struct `v4l2_meta_format`

</td>
<td>


`meta`

</td>
<td>


Definition of a metadata format, see [Metadata Formats](<~kernel/userspace/userspace-api/media-v4l/meta-formats#rst-meta-formats>), used by metadata capture devices.

</td>
</tr>
<tr>
<td>


\__u8

</td>
<td>


`raw_data`\[200\]

</td>
<td>


Place holder for future extensions.

</td>
</tr>
<tr>
<td>


\}

</td>
<td colspan="2">




</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  The struct `v4l2_format` `type` field is invalid or the requested buffer type not supported.

- **EBUSY**

  The device is busy and cannot change the format. This could be because or the device is streaming or buffers are allocated or queued to the driver. Relevant for [VIDIOC_S_FMT](<#rst-vidioc-g-fmt>) only.
