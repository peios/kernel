---
title: "Sliced VBI Data Interface"
type: reference
description: "VBI stands for Vertical Blanking Interval, a gap in the sequence of lines of an analog video signal. During VBI no picture information is transmitted, allowing some time while the electron beam of a cathode ray tube TV returns to the top…"
---

<a id="rst-sliced-vbi-data-interface"></a>
<a id="rst-sliced"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

VBI stands for Vertical Blanking Interval, a gap in the sequence of lines of an analog video signal. During VBI no picture information is transmitted, allowing some time while the electron beam of a cathode ray tube TV returns to the top of the screen.

Sliced VBI devices use hardware to demodulate data transmitted in the VBI. V4L2 drivers shall <em>not</em> do this by software, see also the [raw VBI interface](<~kernel/userspace/userspace-api/media-v4l/dev-raw-vbi#rst-raw-vbi>). The data is passed as short packets of fixed size, covering one scan line each. The number of packets per video frame is variable.

Sliced VBI capture and output devices are accessed through the same character special files as raw VBI devices. When a driver supports both interfaces, the default function of a `/dev/vbi` device is <em>raw</em> VBI capturing or output, and the sliced VBI function is only available after calling the [VIDIOC\_S\_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) ioctl as defined below. Likewise a `/dev/video` device may support the sliced VBI API, however the default function here is video capturing or output. Different file descriptors must be used to pass raw and sliced VBI data simultaneously, if this is supported by the driver.

<a id="rst-querying-capabilities"></a>

## Querying Capabilities

Devices supporting the sliced VBI capturing or output API set the `V4L2_CAP_SLICED_VBI_CAPTURE` or `V4L2_CAP_SLICED_VBI_OUTPUT` flag respectively, in the `capabilities` field of struct `v4l2_capability` returned by the [vidioc\_querycap](<~kernel/userspace/userspace-api/media-v4l/vidioc-querycap#rst-vidioc-querycap>) ioctl. At least one of the read/write or streaming [I/O methods](<~kernel/userspace/userspace-api/media-v4l/io#rst-io>) must be supported. Sliced VBI devices may have a tuner or modulator.

<a id="rst-supplemental-functions"></a>

## Supplemental Functions

Sliced VBI devices shall support [video input or output](<~kernel/userspace/userspace-api/media-v4l/video#rst-video>) and [tuner or modulator](<~kernel/userspace/userspace-api/media-v4l/tuner#rst-tuner>) ioctls if they have these capabilities, and they may support [control](<~kernel/userspace/userspace-api/media-v4l/control#rst-control>) ioctls. The [video standard](<~kernel/userspace/userspace-api/media-v4l/standard#rst-standard>) ioctls provide information vital to program a sliced VBI device, therefore must be supported.

<a id="rst-sliced-vbi-format-negotiation-1"></a>
<a id="rst-sliced-vbi-format-negotiation"></a>

## Sliced VBI Format Negotiation

To find out which data services are supported by the hardware applications can call the [VIDIOC\_G\_SLICED\_VBI\_CAP](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-sliced-vbi-cap#rst-vidioc-g-sliced-vbi-cap>) ioctl. All drivers implementing the sliced VBI interface must support this ioctl. The results may differ from those of the [VIDIOC\_S\_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) ioctl when the number of VBI lines the hardware can capture or output per frame, or the number of services it can identify on a given line are limited. For example on PAL line 16 the hardware may be able to look for a VPS or Teletext signal, but not both at the same time.

To determine the currently selected services applications set the `type` field of struct `v4l2_format` to `V4L2_BUF_TYPE_SLICED_VBI_CAPTURE` or `V4L2_BUF_TYPE_SLICED_VBI_OUTPUT`, and the [VIDIOC\_G\_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) ioctl fills the `fmt.sliced` member, a struct `v4l2_sliced_vbi_format`.

Applications can request different parameters by initializing or modifying the `fmt.sliced` member and calling the [VIDIOC\_S\_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) ioctl with a pointer to the struct `v4l2_format` structure.

The sliced VBI API is more complicated than the raw VBI API because the hardware must be told which VBI service to expect on each scan line. Not all services may be supported by the hardware on all lines (this is especially true for VBI output where Teletext is often unsupported and other services can only be inserted in one specific line). In many cases, however, it is sufficient to just set the `service_set` field to the required services and let the driver fill the `service_lines` array according to hardware capabilities. Only if more precise control is needed should the programmer set the `service_lines` array explicitly.

The [VIDIOC\_S\_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) ioctl modifies the parameters according to hardware capabilities. When the driver allocates resources at this point, it may return an `EBUSY` error code if the required resources are temporarily unavailable. Other resource allocation points which may return `EBUSY` can be the [vidioc\_streamon](<~kernel/userspace/userspace-api/media-v4l/vidioc-streamon#rst-vidioc-streamon>) ioctl and the first `read()`, `write()` and `select()` call.

<a id="c-v4l2_sliced_vbi_format"></a>



```c
v4l2_sliced_vbi_format
```

<a id="rst-struct-v4l2-sliced-vbi-format"></a>

### struct v4l2\_sliced\_vbi\_format

<!-- Source LaTeX layout: \begingroup
\scriptsize
\setlength{\tabcolsep}{2pt} -->

<!-- tabularcolumns: |p{.85cm}|p{3.3cm}|p{4.45cm}|p{4.45cm}|p{4.45cm}| -->


<table>
<tbody>
<tr>
<td>



\_\_u16

</td>
<td>



`service_set`

</td>
<td colspan="3">



If `service_set` is non-zero when passed with [VIDIOC\_S\_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) or [VIDIOC\_TRY\_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>), the `service_lines` array will be filled by the driver according to the services specified in this field. For example, if `service_set` is initialized with `V4L2_SLICED_TELETEXT_B | V4L2_SLICED_WSS_625`, a driver for the cx25840 video decoder sets lines 7-22 of both fields <a id="rst-footnote-reference-1"></a>[1](#rst-f1) to `V4L2_SLICED_TELETEXT_B` and line 23 of the first field to `V4L2_SLICED_WSS_625`. If `service_set` is set to zero, then the values of `service_lines` will be used instead.

On return the driver sets this field to the union of all elements of the returned `service_lines` array. It may contain less services than requested, perhaps just one, if the hardware cannot handle more services simultaneously. It may be empty (zero) if none of the requested services are supported by the hardware.

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



Applications initialize this array with sets of data services the driver shall look for or insert on the respective scan line. Subject to hardware capabilities drivers return the requested set, a subset, which may be just a single service, or an empty set. When the hardware cannot handle multiple services on the same line the driver shall choose one. No assumptions can be made on which service the driver chooses.

Data services are defined in [Sliced VBI services](<#rst-vbi-services2>). Array indices map to ITU-R line numbers<a id="rst-footnote-reference-2"></a>[2](#rst-f2) as follows:

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
<td>





</td>
<td>





</td>
<td colspan="3">



 Drivers must set `service_lines` \[0\]\[0\] and `service_lines`\[1\]\[0\] to zero. The `V4L2_VBI_ITU_525_F1_START`, `V4L2_VBI_ITU_525_F2_START`, `V4L2_VBI_ITU_625_F1_START` and `V4L2_VBI_ITU_625_F2_START` defines give the start line numbers for each field for each 525 or 625 line format as a convenience. Don't forget that ITU line numbering starts at 1, not 0.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`io_size`

</td>
<td colspan="3">



 Maximum number of bytes passed by one `read()` or `write()` call, and the buffer size in bytes for the [vidioc\_qbuf](<~kernel/userspace/userspace-api/media-v4l/vidioc-qbuf#rst-vidioc-qbuf>) and [VIDIOC\_DQBUF](<~kernel/userspace/userspace-api/media-v4l/vidioc-qbuf#rst-vidioc-qbuf>) ioctl. Drivers set this field to the size of struct `v4l2_sliced_vbi_data` times the number of non-zero elements in the returned `service_lines` array (that is the number of lines potentially carrying data).

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`reserved`\[2\]

</td>
<td colspan="3">



 This array is reserved for future extensions.

Applications and drivers must set it to zero.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \endgroup -->

<a id="rst-sliced-vbi-services"></a>
<a id="rst-vbi-services2"></a>

### Sliced VBI services

<!-- Source LaTeX layout: \footnotesize -->

<!-- tabularcolumns: |p{4.2cm}|p{1.1cm}|p{2.1cm}|p{2.0cm}|p{6.5cm}| -->


<table>
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



[itu1119](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-itu1119>),

[en300294](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-en300294>)

</td>
<td>



PAL/SECAM line 23

</td>
<td>



See [V4L2\_SLICED\_WSS\_625 payload](<#rst-v4l2-sliced-wss-625-payload>) below.

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

Drivers may return an `EINVAL` error code when applications attempt to read or write data without prior format negotiation, after switching the video standard (which may invalidate the negotiated VBI parameters) and after switching the video input (which may change the video standard as a side effect). The [VIDIOC\_S\_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) ioctl may return an `EBUSY` error code when applications attempt to change the format while i/o is in progress (between a [vidioc\_streamon](<~kernel/userspace/userspace-api/media-v4l/vidioc-streamon#rst-vidioc-streamon>) and [VIDIOC\_STREAMOFF](<~kernel/userspace/userspace-api/media-v4l/vidioc-streamon#rst-vidioc-streamon>) call, and after the first `read()` or `write()` call).

<a id="rst-v4l2-sliced-wss-625-payload-1"></a>
<a id="rst-v4l2-sliced-wss-625-payload"></a>

#### V4L2\_SLICED\_WSS\_625 payload

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

<a id="rst-reading-and-writing-sliced-vbi-data"></a>

## Reading and writing sliced VBI data

A single `read()` or `write()` call must pass all data belonging to one video frame. That is an array of struct `v4l2_sliced_vbi_data` structures with one or more elements and a total size not exceeding `io_size` bytes. Likewise in streaming I/O mode one buffer of `io_size` bytes must contain data of one video frame. The `id` of unused struct `v4l2_sliced_vbi_data` elements must be zero.

<a id="c-v4l2_sliced_vbi_data"></a>



```c
v4l2_sliced_vbi_data
```

<a id="rst-struct-v4l2-sliced-vbi-data"></a>

### struct v4l2\_sliced\_vbi\_data

<!-- tabularcolumns: |p{1.2cm}|p{2.2cm}|p{13.9cm}| -->


<table>
<tbody>
<tr>
<td>



\_\_u32

</td>
<td>



`id`

</td>
<td>



A flag from [vbi-services](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-sliced-vbi-cap#rst-vbi-services>) identifying the type of data in this packet. Only a single bit must be set. When the `id` of a captured packet is zero, the packet is empty and the contents of other fields are undefined. Applications shall ignore empty packets. When the `id` of a packet for output is zero the contents of the `data` field are undefined and the driver must no longer insert data on the requested `field` and `line`.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`field`

</td>
<td>



The video field number this data has been captured from, or shall be inserted at. `0` for the first field, `1` for the second field.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`line`

</td>
<td>



The field (as opposed to frame) line number this data has been captured from, or shall be inserted at. See [vbi-525](<~kernel/userspace/userspace-api/media-v4l/dev-raw-vbi#rst-vbi-525>) and [vbi-625](<~kernel/userspace/userspace-api/media-v4l/dev-raw-vbi#rst-vbi-625>) for valid values. Sliced VBI capture devices can set the line number of all packets to `0` if the hardware cannot reliably identify scan lines. The field number must always be valid.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`reserved`

</td>
<td>



This field is reserved for future extensions. Applications and drivers must set it to zero.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`data`\[48\]

</td>
<td>



The packet payload. See [vbi-services](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-sliced-vbi-cap#rst-vbi-services>) for the contents and number of bytes passed for each data type. The contents of padding bytes at the end of this array are undefined, drivers and applications shall ignore them.

</td>
</tr>
</tbody>
</table>

Packets are always passed in ascending line number order, without duplicate line numbers. The `write()` function and the [vidioc\_qbuf](<~kernel/userspace/userspace-api/media-v4l/vidioc-qbuf#rst-vidioc-qbuf>) ioctl must return an `EINVAL` error code when applications violate this rule. They must also return an EINVAL error code when applications pass an incorrect field or line number, or a combination of `field`, `line` and `id` which has not been negotiated with the [VIDIOC\_G\_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) or [VIDIOC\_S\_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) ioctl. When the line numbers are unknown the driver must pass the packets in transmitted order. The driver can insert empty packets with `id` set to zero anywhere in the packet array.

To assure synchronization and to distinguish from frame dropping, when a captured frame does not carry any of the requested data services drivers must pass one or more empty packets. When an application fails to pass VBI data in time for output, the driver must output the last VPS and WSS packet again, and disable the output of Closed Caption and Teletext data, or output data which is ignored by Closed Caption and Teletext decoders.

A sliced VBI device may support [read/write](<~kernel/userspace/userspace-api/media-v4l/rw#rst-rw>) and/or streaming ([memory mapping](<~kernel/userspace/userspace-api/media-v4l/mmap#rst-mmap>) and/or [user pointer](<~kernel/userspace/userspace-api/media-v4l/userp#rst-userp>)) I/O. The latter bears the possibility of synchronizing video and VBI data by using buffer timestamps.

<a id="rst-sliced-vbi-data-in-mpeg-streams"></a>

## Sliced VBI Data in MPEG Streams

If a device can produce an MPEG output stream, it may be capable of providing [negotiated sliced VBI services](<#rst-sliced-vbi-format-negotiation>) as data embedded in the MPEG stream. Users or applications control this sliced VBI data insertion with the [V4L2\_CID\_MPEG\_STREAM\_VBI\_FMT](<~kernel/userspace/userspace-api/media-v4l/ext-ctrls-codec#rst-v4l2-mpeg-stream-vbi-fmt>) control.

If the driver does not provide the [V4L2\_CID\_MPEG\_STREAM\_VBI\_FMT](<~kernel/userspace/userspace-api/media-v4l/ext-ctrls-codec#rst-v4l2-mpeg-stream-vbi-fmt>) control, or only allows that control to be set to [V4L2\_MPEG\_STREAM\_VBI\_FMT\_NONE](<~kernel/userspace/userspace-api/media-v4l/ext-ctrls-codec#rst-v4l2-mpeg-stream-vbi-fmt>), then the device cannot embed sliced VBI data in the MPEG stream.

The [V4L2\_CID\_MPEG\_STREAM\_VBI\_FMT](<~kernel/userspace/userspace-api/media-v4l/ext-ctrls-codec#rst-v4l2-mpeg-stream-vbi-fmt>) control does not implicitly set the device driver to capture nor cease capturing sliced VBI data. The control only indicates to embed sliced VBI data in the MPEG stream, if an application has negotiated sliced VBI service be captured.

It may also be the case that a device can embed sliced VBI data in only certain types of MPEG streams: for example in an MPEG-2 PS but not an MPEG-2 TS. In this situation, if sliced VBI data insertion is requested, the sliced VBI data will be embedded in MPEG stream types when supported, and silently omitted from MPEG stream types where sliced VBI data insertion is not supported by the device.

The following subsections specify the format of the embedded sliced VBI data.

<a id="rst-mpeg-stream-embedded-sliced-vbi-data-format-none"></a>

### MPEG Stream Embedded, Sliced VBI Data Format: NONE

The [V4L2\_MPEG\_STREAM\_VBI\_FMT\_NONE](<~kernel/userspace/userspace-api/media-v4l/ext-ctrls-codec#rst-v4l2-mpeg-stream-vbi-fmt>) embedded sliced VBI format shall be interpreted by drivers as a control to cease embedding sliced VBI data in MPEG streams. Neither the device nor driver shall insert "empty" embedded sliced VBI data packets in the MPEG stream when this format is set. No MPEG stream data structures are specified for this format.

<a id="rst-mpeg-stream-embedded-sliced-vbi-data-format-ivtv"></a>

### MPEG Stream Embedded, Sliced VBI Data Format: IVTV

The [V4L2\_MPEG\_STREAM\_VBI\_FMT\_IVTV](<~kernel/userspace/userspace-api/media-v4l/ext-ctrls-codec#rst-v4l2-mpeg-stream-vbi-fmt>) embedded sliced VBI format, when supported, indicates to the driver to embed up to 36 lines of sliced VBI data per frame in an MPEG-2 <em>Private Stream 1 PES</em> packet encapsulated in an MPEG-2 <em>Program Pack</em> in the MPEG stream.

<em>Historical context</em>: This format specification originates from a custom, embedded, sliced VBI data format used by the `ivtv` driver. This format has already been informally specified in the kernel sources in the file `Documentation/userspace-api/media/drivers/cx2341x-uapi.rst` . The maximum size of the payload and other aspects of this format are driven by the CX23415 MPEG decoder's capabilities and limitations with respect to extracting, decoding, and displaying sliced VBI data embedded within an MPEG stream.

This format's use is <em>not</em> exclusive to the `ivtv` driver <em>nor</em> exclusive to CX2341x devices, as the sliced VBI data packet insertion into the MPEG stream is implemented in driver software. At least the `cx18` driver provides sliced VBI data insertion into an MPEG-2 PS in this format as well.

The following definitions specify the payload of the MPEG-2 <em>Private Stream 1 PES</em> packets that contain sliced VBI data when [V4L2\_MPEG\_STREAM\_VBI\_FMT\_IVTV](<~kernel/userspace/userspace-api/media-v4l/ext-ctrls-codec#rst-v4l2-mpeg-stream-vbi-fmt>) is set. (The MPEG-2 <em>Private Stream 1 PES</em> packet header and encapsulating MPEG-2 <em>Program Pack</em> header are not detailed here. Please refer to the MPEG-2 specifications for details on those packet headers.)

The payload of the MPEG-2 <em>Private Stream 1 PES</em> packets that contain sliced VBI data is specified by struct `v4l2_mpeg_vbi_fmt_ivtv`. The payload is variable length, depending on the actual number of lines of sliced VBI data present in a video frame. The payload may be padded at the end with unspecified fill bytes to align the end of the payload to a 4-byte boundary. The payload shall never exceed 1552 bytes (2 fields with 18 lines/field with 43 bytes of data/line and a 4 byte magic number).

<a id="c-v4l2_mpeg_vbi_fmt_ivtv"></a>



```c
v4l2_mpeg_vbi_fmt_ivtv
```

<a id="rst-struct-v4l2-mpeg-vbi-fmt-ivtv"></a>

### struct v4l2\_mpeg\_vbi\_fmt\_ivtv

<!-- tabularcolumns: |p{4.2cm}|p{2.0cm}|p{11.1cm}| -->


<table>
<tbody>
<tr>
<td>



\_\_u8

</td>
<td>



`magic`\[4\]

</td>
<td>



A "magic" constant from [Magic Constants for struct v4l2\_mpeg\_vbi\_fmt\_ivtv magic field](<#rst-v4l2-mpeg-vbi-fmt-ivtv-magic>) that indicates this is a valid sliced VBI data payload and also indicates which member of the anonymous union, `itv0` or `ITV0`, to use for the payload data.

</td>
</tr>
<tr>
<td>



union \{

</td>
<td colspan="2">



(anonymous)

</td>
</tr>
<tr>
<td>



struct `v4l2_mpeg_vbi_itv0`

</td>
<td>



`itv0`

</td>
<td>



The primary form of the sliced VBI data payload that contains anywhere from 1 to 35 lines of sliced VBI data. Line masks are provided in this form of the payload indicating which VBI lines are provided.

</td>
</tr>
<tr>
<td>



struct [v4l2\_mpeg\_vbi\_ITV0](<#rst-v4l2-mpeg-vbi-itv0-1>)

</td>
<td>



`ITV0`

</td>
<td>



An alternate form of the sliced VBI data payload used when 36 lines of sliced VBI data are present. No line masks are provided in this form of the payload; all valid line mask bits are implicitly set.

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

<a id="rst-magic-constants-for-struct-v4l2-mpeg-vbi-fmt-ivtv-magic-field"></a>
<a id="rst-v4l2-mpeg-vbi-fmt-ivtv-magic"></a>

### Magic Constants for struct v4l2\_mpeg\_vbi\_fmt\_ivtv magic field

<!-- tabularcolumns: |p{6.6cm}|p{2.2cm}|p{8.5cm}| -->


<table>
<thead>
<tr>
<th>



Defined Symbol

</th>
<th>



Value

</th>
<th>



Description

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



`V4L2_MPEG_VBI_IVTV_MAGIC0`

</td>
<td>



"itv0"

</td>
<td>



Indicates the `itv0` member of the union in struct `v4l2_mpeg_vbi_fmt_ivtv` is valid.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VBI_IVTV_MAGIC1`

</td>
<td>



"ITV0"

</td>
<td>



Indicates the `ITV0` member of the union in struct `v4l2_mpeg_vbi_fmt_ivtv` is valid and that 36 lines of sliced VBI data are present.

</td>
</tr>
</tbody>
</table>

<a id="c-v4l2_mpeg_vbi_itv0"></a>



```c
v4l2_mpeg_vbi_itv0
```

<a id="c-v4l2_mpeg_vbi_ITV0"></a>



```c
v4l2_mpeg_vbi_ITV0
```

<a id="rst-structs-v4l2-mpeg-vbi-itv0-and-v4l2-mpeg-vbi-itv0"></a>

### structs v4l2\_mpeg\_vbi\_itv0 and v4l2\_mpeg\_vbi\_ITV0

<!-- Source LaTeX layout: \footnotesize -->

<!-- tabularcolumns: |p{4.6cm}|p{2.0cm}|p{10.7cm}| -->


<table>
<tbody>
<tr>
<td>



\_\_le32

</td>
<td>



`linemask`\[2\]

</td>
<td>



Bitmasks indicating the VBI service lines present. These `linemask` values are stored in little endian byte order in the MPEG stream. Some reference `linemask` bit positions with their corresponding VBI line number and video field are given below. b<sub>0</sub> indicates the least significant bit of a `linemask` value:



```text
linemask[0] b0:     line  6  first field
linemask[0] b17:    line 23  first field
linemask[0] b18:    line  6  second field
linemask[0] b31:    line 19  second field
linemask[1] b0:     line 20  second field
linemask[1] b3:     line 23  second field
linemask[1] b4-b31: unused and set to 0
```

</td>
</tr>
<tr>
<td>



struct `v4l2_mpeg_vbi_itv0_line`

</td>
<td>



`line`\[35\]

</td>
<td>



This is a variable length array that holds from 1 to 35 lines of sliced VBI data. The sliced VBI data lines present correspond to the bits set in the `linemask` array, starting from b<sub>0</sub> of `linemask`\[0\] up through b<sub>31</sub> of `linemask`\[0\], and from b<sub>0</sub> of `linemask`\[1\] up through b<sub>3</sub> of `linemask`\[1\]. `line`\[0\] corresponds to the first bit found set in the `linemask` array, `line`\[1\] corresponds to the second bit found set in the `linemask` array, etc. If no `linemask` array bits are set, then `line`\[0\] may contain one line of unspecified data that should be ignored by applications.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

<a id="rst-struct-v4l2-mpeg-vbi-itv0"></a>
<a id="rst-v4l2-mpeg-vbi-itv0-1"></a>

### struct v4l2\_mpeg\_vbi\_ITV0

<!-- tabularcolumns: |p{5.2cm}|p{2.4cm}|p{9.7cm}| -->


<table>
<tbody>
<tr>
<td>



struct `v4l2_mpeg_vbi_itv0_line`

</td>
<td>



`line`\[36\]

</td>
<td>



A fixed length array of 36 lines of sliced VBI data. `line`\[0\] through `line`\[17\] correspond to lines 6 through 23 of the first field. `line`\[18\] through `line`\[35\] corresponds to lines 6 through 23 of the second field.

</td>
</tr>
</tbody>
</table>

<a id="c-v4l2_mpeg_vbi_itv0_line"></a>



```c
v4l2_mpeg_vbi_itv0_line
```

<a id="rst-struct-v4l2-mpeg-vbi-itv0-line"></a>

### struct v4l2\_mpeg\_vbi\_itv0\_line

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->


<table>
<tbody>
<tr>
<td>



\_\_u8

</td>
<td>



`id`

</td>
<td>



A line identifier value from [Line Identifiers for struct v4l2\_mpeg\_vbi\_itv0\_line id field](<#rst-itv0-line-identifier-constants>) that indicates the type of sliced VBI data stored on this line.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`data`\[42\]

</td>
<td>



The sliced VBI data for the line.

</td>
</tr>
</tbody>
</table>

<a id="rst-line-identifiers-for-struct-v4l2-mpeg-vbi-itv0-line-id-field"></a>
<a id="rst-itv0-line-identifier-constants"></a>

### Line Identifiers for struct v4l2\_mpeg\_vbi\_itv0\_line id field

<!-- tabularcolumns: |p{7.0cm}|p{1.8cm}|p{8.5cm}| -->


<table>
<thead>
<tr>
<th>



Defined Symbol

</th>
<th>



Value

</th>
<th>



Description

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



`V4L2_MPEG_VBI_IVTV_TELETEXT_B`

</td>
<td>



1

</td>
<td>



Refer to [Sliced VBI services](<#rst-vbi-services2>) for a description of the line payload.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VBI_IVTV_CAPTION_525`

</td>
<td>



4

</td>
<td>



Refer to [Sliced VBI services](<#rst-vbi-services2>) for a description of the line payload.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VBI_IVTV_WSS_625`

</td>
<td>



5

</td>
<td>



Refer to [Sliced VBI services](<#rst-vbi-services2>) for a description of the line payload.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VBI_IVTV_VPS`

</td>
<td>



7

</td>
<td>



Refer to [Sliced VBI services](<#rst-vbi-services2>) for a description of the line payload.

</td>
</tr>
</tbody>
</table>

<a id="rst-f1"></a>



**[1]** According to [ETS 300 706](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-ets300706>) lines 6-22 of the first field and lines 5-22 of the second field may carry Teletext data.

<a id="rst-f2"></a>



**[2]** See also [vbi-525](<~kernel/userspace/userspace-api/media-v4l/dev-raw-vbi#rst-vbi-525>) and [vbi-625](<~kernel/userspace/userspace-api/media-v4l/dev-raw-vbi#rst-vbi-625>).
