---
title: "ioctl VIDIOC_ENUM_FMT"
type: reference
description: "VIDIOC_ENUM_FMT - Enumerate image formats"
---

<a id="rst-ioctl-vidioc-enum-fmt"></a>
<a id="rst-vidioc-enum-fmt"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_ENUM_FMT - Enumerate image formats

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_ENUM_FMT"></a>

```c
VIDIOC_ENUM_FMT
```

`int ioctl(int fd, VIDIOC_ENUM_FMT, struct v4l2_fmtdesc *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_fmtdesc`.

<a id="rst-description"></a>

## Description

To enumerate image formats applications initialize the `type`, `mbus_code` and `index` fields of struct `v4l2_fmtdesc` and call the [ioctl VIDIOC_ENUM_FMT](<#rst-vidioc-enum-fmt>) ioctl with a pointer to this structure. Drivers fill the rest of the structure or return an `EINVAL` error code. All formats are enumerable by beginning at index zero and incrementing by one until `EINVAL` is returned. If applicable, drivers shall return formats in preference order, where preferred formats are returned before (that is, with lower `index` value) less-preferred formats.

Depending on the `V4L2_CAP_IO_MC` [capability](<~kernel/userspace/userspace-api/media-v4l/vidioc-querycap#rst-device-capabilities>), the `mbus_code` field is handled differently:

1. `V4L2_CAP_IO_MC` is not set (also known as a 'video-node-centric' driver)

   Applications shall initialize the `mbus_code` field to zero and drivers shall ignore the value of the field.

   Drivers shall enumerate all image formats.

   > [!NOTE]
   >
   > After switching the input or output the list of enumerated image formats may be different.

2. `V4L2_CAP_IO_MC` is set (also known as an 'MC-centric' driver)

   If the `mbus_code` field is zero, then all image formats shall be enumerated.

   If the `mbus_code` field is initialized to a valid (non-zero) [media bus format code](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/subdev-formats.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>), then drivers shall restrict enumeration to only the image formats that can produce (for video output devices) or be produced from (for video capture devices) that media bus code. If the `mbus_code` is unsupported by the driver, then `EINVAL` shall be returned.

   Regardless of the value of the `mbus_code` field, the enumerated image formats shall not depend on the active configuration of the video device or device pipeline.





<a id="c-v4l2_fmtdesc"></a>

```c
v4l2_fmtdesc
```

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->


<table>
<caption>struct v4l2_fmtdesc</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`index`

</td>
<td>


Number of the format in the enumeration, set by the application. This is in no way related to the `pixelformat` field. When the index is ORed with `V4L2_FMTDESC_FLAG_ENUM_ALL` the driver clears the flag and enumerates all the possible formats, ignoring any limitations from the current configuration. Drivers which do not support this flag always return an `EINVAL` error code without clearing this flag. Formats enumerated when using `V4L2_FMTDESC_FLAG_ENUM_ALL` flag shouldn't be used when calling `VIDIOC_ENUM_FRAMESIZES()` or `VIDIOC_ENUM_FRAMEINTERVALS()`. `V4L2_FMTDESC_FLAG_ENUM_ALL` should only be used by drivers that can return different format list depending on this flag.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`type`

</td>
<td>


Type of the data stream, set by the application. Only these types are valid here: `V4L2_BUF_TYPE_VIDEO_CAPTURE`, `V4L2_BUF_TYPE_VIDEO_CAPTURE_MPLANE`, `V4L2_BUF_TYPE_VIDEO_OUTPUT`, `V4L2_BUF_TYPE_VIDEO_OUTPUT_MPLANE`, `V4L2_BUF_TYPE_VIDEO_OVERLAY`, `V4L2_BUF_TYPE_SDR_CAPTURE`, `V4L2_BUF_TYPE_SDR_OUTPUT`, `V4L2_BUF_TYPE_META_CAPTURE` and `V4L2_BUF_TYPE_META_OUTPUT`. See `v4l2_buf_type`.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`flags`

</td>
<td>


See [fmtdesc-flags](<#rst-fmtdesc-flags>)

</td>
</tr>
<tr>
<td>


\__u8

</td>
<td>


`description`\[32\]

</td>
<td>


Description of the format, a NUL-terminated ASCII string. This information is intended for the user, for example: "YUV 4:2:2".

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`pixelformat`

</td>
<td>


The image format identifier. This is a four character code as computed by the v4l2_fourcc() macro:

</td>
</tr>
<tr>
<td colspan="3">


<a id="rst-v4l2-fourcc"></a>

`#define v4l2_fourcc(a,b,c,d)`

`(((__u32)(a)<<0)|((__u32)(b)<<8)|((__u32)(c)<<16)|((__u32)(d)<<24))`

Several image formats are already defined by this specification in [Image Formats](<~kernel/userspace/userspace-api/media-v4l/pixfmt#rst-pixfmt>).

> [!NOTE]
>
> These codes are not the same as those used in the Windows world.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`mbus_code`

</td>
<td>


Media bus code restricting the enumerated formats, set by the application. Only applicable to drivers that advertise the `V4L2_CAP_IO_MC` [capability](<~kernel/userspace/userspace-api/media-v4l/vidioc-querycap#rst-device-capabilities>), shall be 0 otherwise.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`reserved`\[3\]

</td>
<td>


Reserved for future extensions. Drivers must set the array to zero.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{8.4cm}|p{1.8cm}|p{7.1cm}| -->

<a id="rst-fmtdesc-flags"></a>


<table>
<caption>Image Format Description Flags</caption>
<tbody>
<tr>
<td>


`V4L2_FMT_FLAG_COMPRESSED`

</td>
<td>


0x0001

</td>
<td>


This is a compressed format.

</td>
</tr>
<tr>
<td>


`V4L2_FMT_FLAG_EMULATED`

</td>
<td>


0x0002

</td>
<td>


This format is not native to the device but emulated through software (usually libv4l2), where possible try to use a native format instead for better performance.

</td>
</tr>
<tr>
<td>


`V4L2_FMT_FLAG_CONTINUOUS_BYTESTREAM`

</td>
<td>


0x0004

</td>
<td>


The hardware decoder for this compressed bytestream format (aka coded format) is capable of parsing a continuous bytestream. Applications do not need to parse the bytestream themselves to find the boundaries between frames/fields.

This flag can only be used in combination with the `V4L2_FMT_FLAG_COMPRESSED` flag, since this applies to compressed formats only. This flag is valid for stateful decoders only.

</td>
</tr>
<tr>
<td>


`V4L2_FMT_FLAG_DYN_RESOLUTION`

</td>
<td>


0x0008

</td>
<td>


Dynamic resolution switching is supported by the device for this compressed bytestream format (aka coded format). It will notify the user via the event `V4L2_EVENT_SOURCE_CHANGE` when changes in the video parameters are detected.

This flag can only be used in combination with the `V4L2_FMT_FLAG_COMPRESSED` flag, since this applies to compressed formats only. This flag is valid for stateful codecs only.

</td>
</tr>
<tr>
<td>


`V4L2_FMT_FLAG_ENC_CAP_FRAME_INTERVAL`

</td>
<td>


0x0010

</td>
<td>


The hardware encoder supports setting the `CAPTURE` coded frame interval separately from the `OUTPUT` raw frame interval. Setting the `OUTPUT` raw frame interval with [VIDIOC_S_PARM](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-parm#rst-vidioc-g-parm>) also sets the `CAPTURE` coded frame interval to the same value. If this flag is set, then the `CAPTURE` coded frame interval can be set to a different value afterwards. This is typically used for offline encoding where the `OUTPUT` raw frame interval is used as a hint for reserving hardware encoder resources and the `CAPTURE` coded frame interval is the actual frame rate embedded in the encoded video stream.

This flag can only be used in combination with the `V4L2_FMT_FLAG_COMPRESSED` flag, since this applies to compressed formats only. This flag is valid for stateful encoders only.

</td>
</tr>
<tr>
<td>


`V4L2_FMT_FLAG_CSC_COLORSPACE`

</td>
<td>


0x0020

</td>
<td>


The driver allows the application to try to change the default colorspace. This flag is relevant only for capture devices. The application can ask to configure the colorspace of the capture device when calling the [VIDIOC_S_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) ioctl with [V4L2_PIX_FMT_FLAG_SET_CSC](<~kernel/userspace/userspace-api/media-v4l/pixfmt-v4l2#rst-v4l2-pix-fmt-flag-set-csc>) set.

</td>
</tr>
<tr>
<td>


`V4L2_FMT_FLAG_CSC_XFER_FUNC`

</td>
<td>


0x0040

</td>
<td>


The driver allows the application to try to change the default transfer function. This flag is relevant only for capture devices. The application can ask to configure the transfer function of the capture device when calling the [VIDIOC_S_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) ioctl with [V4L2_PIX_FMT_FLAG_SET_CSC](<~kernel/userspace/userspace-api/media-v4l/pixfmt-v4l2#rst-v4l2-pix-fmt-flag-set-csc>) set.

</td>
</tr>
<tr>
<td>


`V4L2_FMT_FLAG_CSC_YCBCR_ENC`

</td>
<td>


0x0080

</td>
<td>


The driver allows the application to try to change the default Y'CbCr encoding. This flag is relevant only for capture devices. The application can ask to configure the Y'CbCr encoding of the capture device when calling the [VIDIOC_S_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) ioctl with [V4L2_PIX_FMT_FLAG_SET_CSC](<~kernel/userspace/userspace-api/media-v4l/pixfmt-v4l2#rst-v4l2-pix-fmt-flag-set-csc>) set.

</td>
</tr>
<tr>
<td>


`V4L2_FMT_FLAG_CSC_HSV_ENC`

</td>
<td>


0x0080

</td>
<td>


The driver allows the application to try to change the default HSV encoding. This flag is relevant only for capture devices. The application can ask to configure the HSV encoding of the capture device when calling the [VIDIOC_S_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) ioctl with [V4L2_PIX_FMT_FLAG_SET_CSC](<~kernel/userspace/userspace-api/media-v4l/pixfmt-v4l2#rst-v4l2-pix-fmt-flag-set-csc>) set.

</td>
</tr>
<tr>
<td>


`V4L2_FMT_FLAG_CSC_QUANTIZATION`

</td>
<td>


0x0100

</td>
<td>


The driver allows the application to try to change the default quantization. This flag is relevant only for capture devices. The application can ask to configure the quantization of the capture device when calling the [VIDIOC_S_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) ioctl with [V4L2_PIX_FMT_FLAG_SET_CSC](<~kernel/userspace/userspace-api/media-v4l/pixfmt-v4l2#rst-v4l2-pix-fmt-flag-set-csc>) set.

</td>
</tr>
<tr>
<td>


`V4L2_FMT_FLAG_META_LINE_BASED`

</td>
<td>


0x0200

</td>
<td>


The metadata format is line-based. In this case the `width`, `height` and `bytesperline` fields of `v4l2_meta_format` are valid. The buffer consists of `height` lines, each having `width` Data Units of data and the offset (in bytes) between the beginning of each two consecutive lines is `bytesperline`.

</td>
</tr>
<tr>
<td>


`V4L2_FMTDESC_FLAG_ENUM_ALL`

</td>
<td>


0x80000000

</td>
<td>


When the applications ORs `index` with `V4L2_FMTDESC_FLAG_ENUM_ALL` flag the driver enumerates all the possible pixel formats without taking care of any already set configuration. Drivers which do not support this flag, always return `EINVAL` without clearing this flag.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  The struct `v4l2_fmtdesc` `type` is not supported or the `index` is out of bounds.

  If `V4L2_CAP_IO_MC` is set and the specified `mbus_code` is unsupported, then also return this error code.
