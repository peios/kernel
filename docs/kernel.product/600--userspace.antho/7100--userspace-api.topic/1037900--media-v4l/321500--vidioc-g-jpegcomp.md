---
title: "ioctl VIDIOC_G_JPEGCOMP, VIDIOC_S_JPEGCOMP"
type: reference
description: "VIDIOC_G_JPEGCOMP - VIDIOC_S_JPEGCOMP"
---

<a id="rst-ioctl-vidioc-g-jpegcomp-vidioc-s-jpegcomp"></a>
<a id="rst-vidioc-g-jpegcomp"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_G_JPEGCOMP - VIDIOC_S_JPEGCOMP

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_G_JPEGCOMP"></a>

```c
VIDIOC_G_JPEGCOMP
```

`int ioctl(int fd, VIDIOC_G_JPEGCOMP, v4l2_jpegcompression *argp)`





<a id="c-VIDIOC_S_JPEGCOMP"></a>

```c
VIDIOC_S_JPEGCOMP
```

`int ioctl(int fd, VIDIOC_S_JPEGCOMP, const v4l2_jpegcompression *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_jpegcompression`.

<a id="rst-description"></a>

## Description

These ioctls are **deprecated**. New drivers and applications should use [JPEG class controls](<~kernel/userspace/userspace-api/media-v4l/ext-ctrls-jpeg#rst-jpeg-controls>) for image quality and JPEG markers control.

\[to do\]

Ronald Bultje elaborates:

APP is some application-specific information. The application can set it itself, and it'll be stored in the JPEG-encoded fields (eg; interlacing information for in an AVI or so). COM is the same, but it's comments, like 'encoded by me' or so.

jpeg_markers describes whether the huffman tables, quantization tables and the restart interval information (all JPEG-specific stuff) should be stored in the JPEG-encoded fields. These define how the JPEG field is encoded. If you omit them, applications assume you've used standard encoding. You usually do want to add them.

<!-- tabularcolumns: |p{1.2cm}|p{3.0cm}|p{13.1cm}| -->





<a id="c-v4l2_jpegcompression"></a>

```c
v4l2_jpegcompression
```


<table>
<caption>struct v4l2_jpegcompression</caption>
<tbody>
<tr>
<td>


int

</td>
<td>


`quality`

</td>
<td>


Deprecated. If [V4L2_CID_JPEG_COMPRESSION_QUALITY](<~kernel/userspace/userspace-api/media-v4l/ext-ctrls-jpeg#rst-jpeg-quality-control>) control is exposed by a driver applications should use it instead and ignore this field.

</td>
</tr>
<tr>
<td>


int

</td>
<td>


`APPn`

</td>
<td>




</td>
</tr>
<tr>
<td>


int

</td>
<td>


`APP_len`

</td>
<td>




</td>
</tr>
<tr>
<td>


char

</td>
<td>


`APP_data`\[60\]

</td>
<td>




</td>
</tr>
<tr>
<td>


int

</td>
<td>


`COM_len`

</td>
<td>




</td>
</tr>
<tr>
<td>


char

</td>
<td>


`COM_data`\[60\]

</td>
<td>




</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`jpeg_markers`

</td>
<td>


See [jpeg-markers](<#rst-jpeg-markers>). Deprecated. If [V4L2_CID_JPEG_ACTIVE_MARKER](<~kernel/userspace/userspace-api/media-v4l/ext-ctrls-jpeg#rst-jpeg-active-marker-control>) control is exposed by a driver applications should use it instead and ignore this field.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{6.6cm}|p{2.2cm}|p{8.5cm}| -->

<a id="rst-jpeg-markers"></a>


<table>
<caption>JPEG Markers Flags</caption>
<tbody>
<tr>
<td>


`V4L2_JPEG_MARKER_DHT`

</td>
<td>


(1&lt;&lt;3)

</td>
<td>


Define Huffman Tables

</td>
</tr>
<tr>
<td>


`V4L2_JPEG_MARKER_DQT`

</td>
<td>


(1&lt;&lt;4)

</td>
<td>


Define Quantization Tables

</td>
</tr>
<tr>
<td>


`V4L2_JPEG_MARKER_DRI`

</td>
<td>


(1&lt;&lt;5)

</td>
<td>


Define Restart Interval

</td>
</tr>
<tr>
<td>


`V4L2_JPEG_MARKER_COM`

</td>
<td>


(1&lt;&lt;6)

</td>
<td>


Comment segment

</td>
</tr>
<tr>
<td>


`V4L2_JPEG_MARKER_APP`

</td>
<td>


(1&lt;&lt;7)

</td>
<td>


App segment, driver will always use APP0

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
