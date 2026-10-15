---
title: "ioctl VIDIOC_G_SLICED_VBI_CAP"
type: reference
description: "VIDIOC_G_SLICED_VBI_CAP - Query sliced VBI capabilities"
---

<a id="rst-ioctl-vidioc-g-sliced-vbi-cap"></a>
<a id="rst-vidioc-g-sliced-vbi-cap"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC\_G\_SLICED\_VBI\_CAP - Query sliced VBI capabilities

<a id="rst-synopsis"></a>

## Synopsis

<a id="c-VIDIOC_G_SLICED_VBI_CAP"></a>



```c
VIDIOC_G_SLICED_VBI_CAP
```

`int ioctl(int fd, VIDIOC_G_SLICED_VBI_CAP, struct v4l2_sliced_vbi_cap *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_sliced_vbi_cap`.

<a id="rst-description"></a>

## Description

To find out which data services are supported by a sliced VBI capture or output device, applications initialize the `type` field of a struct `v4l2_sliced_vbi_cap`, clear the `reserved` array and call the [VIDIOC\_G\_SLICED\_VBI\_CAP](<#rst-vidioc-g-sliced-vbi-cap>) ioctl. The driver fills in the remaining fields or returns an `EINVAL` error code if the sliced VBI API is unsupported or `type` is invalid.

> [!NOTE]
>
> The `type` field was added, and the ioctl changed from read-only to write-read, in Linux 2.6.19.

<a id="c-v4l2_sliced_vbi_cap"></a>



```c
v4l2_sliced_vbi_cap
```

<!-- tabularcolumns: |p{1.4cm}|p{4.4cm}|p{4.5cm}|p{3.6cm}|p{3.6cm}| -->


<table>
<caption>

struct v4l2\_sliced\_vbi\_cap

</caption>
<tbody>
<tr>
<td>



\_\_u16

</td>
<td>



`service_set`

</td>
<td colspan="3">



 A set of all data services supported by the driver.

Equal to the union of all elements of the `service_lines` array.

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`service_lines`\[2\]\[24\]

</td>
<td colspan="3">



 Each element of this array contains a set of data services the hardware can look for or insert into a particular scan line. Data services are defined in [vbi-services](<#rst-vbi-services>). Array indices map to ITU-R line numbers<a id="rst-footnote-reference-1"></a>[1](#rst-f1) as follows:

</td>
</tr>
<tr>
<td>





</td>
<td>





</td>
<td>



Element

</td>
<td>



525 line systems

</td>
<td>



625 line systems

</td>
</tr>
<tr>
<td>





</td>
<td>





</td>
<td>



`service_lines`\[0\]\[1\]

</td>
<td>



1

</td>
<td>



1

</td>
</tr>
<tr>
<td>





</td>
<td>





</td>
<td>



`service_lines`\[0\]\[23\]

</td>
<td>



23

</td>
<td>



23

</td>
</tr>
<tr>
<td>





</td>
<td>





</td>
<td>



`service_lines`\[1\]\[1\]

</td>
<td>



264

</td>
<td>



314

</td>
</tr>
<tr>
<td>





</td>
<td>





</td>
<td>



`service_lines`\[1\]\[23\]

</td>
<td>



286

</td>
<td>



336

</td>
</tr>
<tr>
<td colspan="5">





</td>
</tr>
<tr>
<td>





</td>
<td>





</td>
<td colspan="3">



 The number of VBI lines the hardware can capture or output per frame, or the number of services it can identify on a given line may be limited. For example on PAL line 16 the hardware may be able to look for a VPS or Teletext signal, but not both at the same time. Applications can learn about these limits using the [VIDIOC\_S\_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) ioctl as described in [Sliced VBI Data Interface](<~kernel/userspace/userspace-api/media-v4l/dev-sliced-vbi#rst-sliced>).

</td>
</tr>
<tr>
<td colspan="5">





</td>
</tr>
<tr>
<td>





</td>
<td>





</td>
<td colspan="3">



 Drivers must set `service_lines` \[0\]\[0\] and `service_lines`\[1\]\[0\] to zero.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`type`

</td>
<td colspan="3">



Type of the data stream, see `v4l2_buf_type`. Should be `V4L2_BUF_TYPE_SLICED_VBI_CAPTURE` or `V4L2_BUF_TYPE_SLICED_VBI_OUTPUT`.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`reserved`\[3\]

</td>
<td colspan="3">



 This array is reserved for future extensions.

Applications and drivers must set it to zero.

</td>
</tr>
</tbody>
</table>

<a id="rst-f1"></a>



**[1]** See also [vbi-525](<~kernel/userspace/userspace-api/media-v4l/dev-raw-vbi#rst-vbi-525>) and [vbi-625](<~kernel/userspace/userspace-api/media-v4l/dev-raw-vbi#rst-vbi-625>).

<!-- Source LaTeX layout: \scriptsize -->

<!-- tabularcolumns: |p{3.9cm}|p{1.0cm}|p{2.0cm}|p{3.0cm}|p{7.0cm}| -->

<a id="rst-vbi-services"></a>


<table>
<caption>

Sliced VBI services

</caption>
<thead>
<tr>
<th>



Symbol

</th>
<th>



Value

</th>
<th>



Reference

</th>
<th>



Lines, usually

</th>
<th>



Payload

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



`V4L2_SLICED_TELETEXT_B` (Teletext System B)

</td>
<td>



0x0001

</td>
<td>



[ets300706](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-ets300706>),

[itu653](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-itu653>)

</td>
<td>



PAL/SECAM line 7-22, 320-335 (second field 7-22)

</td>
<td>



Last 42 of the 45 byte Teletext packet, that is without clock run-in and framing code, lsb first transmitted.

</td>
</tr>
<tr>
<td>



`V4L2_SLICED_VPS`

</td>
<td>



0x0400

</td>
<td>



[ets300231](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-ets300231>)

</td>
<td>



PAL line 16

</td>
<td>



Byte number 3 to 15 according to Figure 9 of ETS 300 231, lsb first transmitted.

</td>
</tr>
<tr>
<td>



`V4L2_SLICED_CAPTION_525`

</td>
<td>



0x1000

</td>
<td>



[cea608](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-cea608>)

</td>
<td>



NTSC line 21, 284 (second field 21)

</td>
<td>



Two bytes in transmission order, including parity bit, lsb first transmitted.

</td>
</tr>
<tr>
<td>



`V4L2_SLICED_WSS_625`

</td>
<td>



0x4000

</td>
<td>



[en300294](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-en300294>),

[itu1119](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-itu1119>)

</td>
<td>



PAL/SECAM line 23

</td>
<td>



See [V4L2\_SLICED\_VBI\_CAP WSS\_625 payload](<#rst-v4l2-sliced-vbi-cap-wss-625-payload>) below.

</td>
</tr>
<tr>
<td>



`V4L2_SLICED_VBI_525`

</td>
<td>



0x1000

</td>
<td colspan="3">



 Set of services applicable to 525 line systems.

</td>
</tr>
<tr>
<td>



`V4L2_SLICED_VBI_625`

</td>
<td>



0x4401

</td>
<td colspan="3">



 Set of services applicable to 625 line systems.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

<a id="rst-v4l2-sliced-vbi-cap-wss-625-payload-1"></a>
<a id="rst-v4l2-sliced-vbi-cap-wss-625-payload"></a>

### V4L2\_SLICED\_VBI\_CAP WSS\_625 payload

The payload for `V4L2_SLICED_WSS_625` is:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
>
> Byte
>
> </td>
> <td colspan="8">
>
>
>
> 0
>
> </td>
> <td colspan="8">
>
>
>
> 1
>
> </td>
> </tr>
> <tr>
> <td rowspan="2">
>
>
>
> Bit
>
> </td>
> <td colspan="4">
>
>
>
> msb
>
> </td>
> <td colspan="4">
>
>
>
> lsb
>
> </td>
> <td colspan="4">
>
>
>
> msb
>
> </td>
> <td colspan="4">
>
>
>
> lsb
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
> 7
>
> </td>
> <td>
>
>
>
> 6
>
> </td>
> <td>
>
>
>
> 5
>
> </td>
> <td>
>
>
>
> 4
>
> </td>
> <td>
>
>
>
> 3
>
> </td>
> <td>
>
>
>
> 2
>
> </td>
> <td>
>
>
>
> 1
>
> </td>
> <td>
>
>
>
> 0
>
> </td>
> <td>
>
>
>
> x
>
> </td>
> <td>
>
>
>
> x
>
> </td>
> <td>
>
>
>
> 13
>
> </td>
> <td>
>
>
>
> 12
>
> </td>
> <td>
>
>
>
> 11
>
> </td>
> <td>
>
>
>
> 10
>
> </td>
> <td>
>
>
>
> 9
>
> </td>
> <td>
>
>
>
> 8
>
> </td>
> </tr>
> </tbody>
> </table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  The value in the `type` field is wrong.
