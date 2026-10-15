---
title: "ioctl VIDIOC_SUBDEV_ENUM_MBUS_CODE"
type: reference
description: "VIDIOC_SUBDEV_ENUM_MBUS_CODE - Enumerate media bus formats"
---

<a id="rst-ioctl-vidioc-subdev-enum-mbus-code"></a>
<a id="rst-vidioc-subdev-enum-mbus-code"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC\_SUBDEV\_ENUM\_MBUS\_CODE - Enumerate media bus formats

<a id="rst-synopsis"></a>

## Synopsis

<a id="c-VIDIOC_SUBDEV_ENUM_MBUS_CODE"></a>



```c
VIDIOC_SUBDEV_ENUM_MBUS_CODE
```

`int ioctl(int fd, VIDIOC_SUBDEV_ENUM_MBUS_CODE, struct v4l2_subdev_mbus_code_enum * argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_subdev_mbus_code_enum`.

<a id="rst-description"></a>

## Description

This call is used by the application to access the enumeration of media bus formats for the selected pad.

The enumerations are defined by the driver, and indexed using the `index` field of struct `v4l2_subdev_mbus_code_enum`. Each enumeration starts with the `index` of 0, and the lowest invalid index marks the end of enumeration.

Therefore, to enumerate media bus formats available at a given sub-device pad, initialize the `pad`, and `which` fields to desired values, and set `index` to 0. Then call the [ioctl VIDIOC\_SUBDEV\_ENUM\_MBUS\_CODE](<#rst-vidioc-subdev-enum-mbus-code>) ioctl with a pointer to this structure.

A successful call will return with the `code` field filled in with a mbus code value. Repeat with increasing `index` until `EINVAL` is received. `EINVAL` means that either `pad` is invalid, or that there are no more codes available at this pad.

The driver must not return the same value of `code` for different indices at the same pad.

Available media bus formats may depend on the current 'try' formats at other pads of the sub-device, as well as on the current active links. See [vidioc\_subdev\_g\_fmt](<~kernel/userspace/userspace-api/media-v4l/vidioc-subdev-g-fmt#rst-vidioc-subdev-g-fmt>) for more information about the try formats.

<a id="c-v4l2_subdev_mbus_code_enum"></a>



```c
v4l2_subdev_mbus_code_enum
```

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->


<table>
<caption>

struct v4l2\_subdev\_mbus\_code\_enum

</caption>
<tbody>
<tr>
<td>



\_\_u32

</td>
<td>



`pad`

</td>
<td>



Pad number as reported by the media controller API. Filled in by the application.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`index`

</td>
<td>



Index of the mbus code in the enumeration belonging to the given pad. Filled in by the application.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`code`

</td>
<td>



The media bus format code, as defined in [Media Bus Formats](<~kernel/userspace/userspace-api/media-v4l/subdev-formats#rst-v4l2-mbus-format>). Filled in by the driver.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`which`

</td>
<td>



Media bus format codes to be enumerated, from enum [v4l2\_subdev\_format\_whence](<~kernel/userspace/userspace-api/media-v4l/vidioc-subdev-g-fmt#rst-v4l2-subdev-format-whence>).

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`flags`

</td>
<td>



See [v4l2-subdev-mbus-code-flags](<#rst-v4l2-subdev-mbus-code-flags>)

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`stream`

</td>
<td>



Stream identifier.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`reserved`\[6\]

</td>
<td>



Reserved for future extensions. Applications and drivers must set the array to zero.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \footnotesize -->

<!-- tabularcolumns: |p{8.8cm}|p{2.2cm}|p{6.3cm}| -->

<a id="rst-v4l2-subdev-mbus-code-flags"></a>


<table>
<caption>

Subdev Media Bus Code Enumerate Flags

</caption>
<tbody>
<tr>
<td>



V4L2\_SUBDEV\_MBUS\_CODE\_CSC\_COLORSPACE

</td>
<td>



0x00000001

</td>
<td>



The driver allows the application to try to change the default colorspace encoding. The application can ask to configure the colorspace of the subdevice when calling the [VIDIOC\_SUBDEV\_S\_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-subdev-g-fmt#rst-vidioc-subdev-g-fmt>) ioctl with [V4L2\_MBUS\_FRAMEFMT\_SET\_CSC](<~kernel/userspace/userspace-api/media-v4l/subdev-formats#rst-mbus-framefmt-set-csc>) set. See [Media Bus Formats](<~kernel/userspace/userspace-api/media-v4l/subdev-formats#rst-v4l2-mbus-format>) on how to do this.

</td>
</tr>
<tr>
<td>



V4L2\_SUBDEV\_MBUS\_CODE\_CSC\_XFER\_FUNC

</td>
<td>



0x00000002

</td>
<td>



The driver allows the application to try to change the default transform function. The application can ask to configure the transform function of the subdevice when calling the [VIDIOC\_SUBDEV\_S\_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-subdev-g-fmt#rst-vidioc-subdev-g-fmt>) ioctl with [V4L2\_MBUS\_FRAMEFMT\_SET\_CSC](<~kernel/userspace/userspace-api/media-v4l/subdev-formats#rst-mbus-framefmt-set-csc>) set. See [Media Bus Formats](<~kernel/userspace/userspace-api/media-v4l/subdev-formats#rst-v4l2-mbus-format>) on how to do this.

</td>
</tr>
<tr>
<td>



V4L2\_SUBDEV\_MBUS\_CODE\_CSC\_YCBCR\_ENC

</td>
<td>



0x00000004

</td>
<td>



The driver allows the application to try to change the default Y'CbCr encoding. The application can ask to configure the Y'CbCr encoding of the subdevice when calling the [VIDIOC\_SUBDEV\_S\_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-subdev-g-fmt#rst-vidioc-subdev-g-fmt>) ioctl with [V4L2\_MBUS\_FRAMEFMT\_SET\_CSC](<~kernel/userspace/userspace-api/media-v4l/subdev-formats#rst-mbus-framefmt-set-csc>) set. See [Media Bus Formats](<~kernel/userspace/userspace-api/media-v4l/subdev-formats#rst-v4l2-mbus-format>) on how to do this.

</td>
</tr>
<tr>
<td>



V4L2\_SUBDEV\_MBUS\_CODE\_CSC\_HSV\_ENC

</td>
<td>



0x00000004

</td>
<td>



The driver allows the application to try to change the default HSV encoding. The application can ask to configure the HSV encoding of the subdevice when calling the [VIDIOC\_SUBDEV\_S\_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-subdev-g-fmt#rst-vidioc-subdev-g-fmt>) ioctl with [V4L2\_MBUS\_FRAMEFMT\_SET\_CSC](<~kernel/userspace/userspace-api/media-v4l/subdev-formats#rst-mbus-framefmt-set-csc>) set. See [Media Bus Formats](<~kernel/userspace/userspace-api/media-v4l/subdev-formats#rst-v4l2-mbus-format>) on how to do this.

</td>
</tr>
<tr>
<td>



V4L2\_SUBDEV\_MBUS\_CODE\_CSC\_QUANTIZATION

</td>
<td>



0x00000008

</td>
<td>



The driver allows the application to try to change the default quantization. The application can ask to configure the quantization of the subdevice when calling the [VIDIOC\_SUBDEV\_S\_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-subdev-g-fmt#rst-vidioc-subdev-g-fmt>) ioctl with [V4L2\_MBUS\_FRAMEFMT\_SET\_CSC](<~kernel/userspace/userspace-api/media-v4l/subdev-formats#rst-mbus-framefmt-set-csc>) set. See [Media Bus Formats](<~kernel/userspace/userspace-api/media-v4l/subdev-formats#rst-v4l2-mbus-format>) on how to do this.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  The struct `v4l2_subdev_mbus_code_enum` `pad` references a non-existing pad, the `which` field has an unsupported value, or the `index` field is out of bounds.
