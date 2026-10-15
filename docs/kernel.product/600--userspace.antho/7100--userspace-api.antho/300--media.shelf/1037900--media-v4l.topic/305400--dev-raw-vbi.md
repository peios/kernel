---
title: "Raw VBI Data Interface"
type: reference
description: "VBI is an abbreviation of Vertical Blanking Interval, a gap in the sequence of lines of an analog video signal. During VBI no picture information is transmitted, allowing some time while the electron beam of a cathode ray tube TV returns…"
---

<a id="rst-raw-vbi-data-interface"></a>
<a id="rst-raw-vbi"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

VBI is an abbreviation of Vertical Blanking Interval, a gap in the sequence of lines of an analog video signal. During VBI no picture information is transmitted, allowing some time while the electron beam of a cathode ray tube TV returns to the top of the screen. Using an oscilloscope you will find here the vertical synchronization pulses and short data packages ASK modulated <a id="rst-footnote-reference-1"></a>[1](#rst-f1) onto the video signal. These are transmissions of services such as Teletext or Closed Caption.

Subject of this interface type is raw VBI data, as sampled off a video signal, or to be added to a signal for output. The data format is similar to uncompressed video images, a number of lines times a number of samples per line, we call this a VBI image.

Conventionally V4L2 VBI devices are accessed through character device special files named `/dev/vbi` and `/dev/vbi0` to `/dev/vbi31` with major number 81 and minor numbers 224 to 255. `/dev/vbi` is typically a symbolic link to the preferred VBI device. This convention applies to both input and output devices.

To address the problems of finding related video and VBI devices VBI capturing and output is also available as device function under `/dev/video`. To capture or output raw VBI data with these devices applications must call the [VIDIOC_S_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) ioctl. Accessed as `/dev/vbi`, raw VBI capturing or output is the default device function.

<a id="rst-querying-capabilities"></a>

## Querying Capabilities

Devices supporting the raw VBI capturing or output API set the `V4L2_CAP_VBI_CAPTURE` or `V4L2_CAP_VBI_OUTPUT` flags, respectively, in the `capabilities` field of struct `v4l2_capability` returned by the [ioctl VIDIOC_QUERYCAP](<~kernel/userspace/userspace-api/media-v4l/vidioc-querycap#rst-vidioc-querycap>) ioctl. At least one of the read/write or streaming I/O methods must be supported. VBI devices may or may not have a tuner or modulator.

<a id="rst-supplemental-functions"></a>

## Supplemental Functions

VBI devices shall support [video input or output](<~kernel/userspace/userspace-api/media-v4l/video#rst-video>), [tuner or modulator](<~kernel/userspace/userspace-api/media-v4l/tuner#rst-tuner>), and [controls](<~kernel/userspace/userspace-api/media-v4l/control#rst-control>) ioctls as needed. The [video standard](<~kernel/userspace/userspace-api/media-v4l/standard#rst-standard>) ioctls provide information vital to program a VBI device, therefore must be supported.

<a id="rst-raw-vbi-format-negotiation"></a>

## Raw VBI Format Negotiation

Raw VBI sampling abilities can vary, in particular the sampling frequency. To properly interpret the data V4L2 specifies an ioctl to query the sampling parameters. Moreover, to allow for some flexibility applications can also suggest different parameters.

As usual these parameters are *not* reset at `open()` time to permit Unix tool chains, programming a device and then reading from it as if it was a plain file. Well written V4L2 applications should always ensure they really get what they want, requesting reasonable parameters and then checking if the actual parameters are suitable.

To query the current raw VBI capture parameters applications set the `type` field of a struct `v4l2_format` to `V4L2_BUF_TYPE_VBI_CAPTURE` or `V4L2_BUF_TYPE_VBI_OUTPUT`, and call the [VIDIOC_G_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) ioctl with a pointer to this structure. Drivers fill the struct `v4l2_vbi_format` `vbi` member of the `fmt` union.

To request different parameters applications set the `type` field of a struct `v4l2_format` as above and initialize all fields of the struct `v4l2_vbi_format` `vbi` member of the `fmt` union, or better just modify the results of [VIDIOC_G_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>), and call the [VIDIOC_S_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) ioctl with a pointer to this structure. Drivers return an `EINVAL` error code only when the given parameters are ambiguous, otherwise they modify the parameters according to the hardware capabilities and return the actual parameters. When the driver allocates resources at this point, it may return an `EBUSY` error code to indicate the returned parameters are valid but the required resources are currently not available. That may happen for instance when the video and VBI areas to capture would overlap, or when the driver supports multiple opens and another process already requested VBI capturing or output. Anyway, applications must expect other resource allocation points which may return `EBUSY`, at the [ioctl VIDIOC_STREAMON, VIDIOC_STREAMOFF](<~kernel/userspace/userspace-api/media-v4l/vidioc-streamon#rst-vidioc-streamon>) ioctl and the first `read()` , `write()` and `select()` calls.

VBI devices must implement both the [VIDIOC_G_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) and [VIDIOC_S_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) ioctl, even if [VIDIOC_S_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) ignores all requests and always returns default parameters as [VIDIOC_G_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) does. [VIDIOC_TRY_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) is optional.

<!-- tabularcolumns: |p{1.6cm}|p{4.2cm}|p{11.5cm}| -->





<a id="c-v4l2_vbi_format"></a>

```c
v4l2_vbi_format
```


<table>
<caption>struct v4l2_vbi_format</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`sampling_rate`

</td>
<td>


Samples per second, i. e. unit 1 Hz.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`offset`

</td>
<td>


Horizontal offset of the VBI image, relative to the leading edge of the line synchronization pulse and counted in samples: The first sample in the VBI image will be located `offset` / `sampling_rate` seconds following the leading edge. See also [vbi-hsync](<#rst-vbi-hsync>).

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`samples_per_line`

</td>
<td>




</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`sample_format`

</td>
<td>


Defines the sample format as in [Image Formats](<~kernel/userspace/userspace-api/media-v4l/pixfmt#rst-pixfmt>), a four-character-code. <a id="rst-footnote-reference-2"></a>[2](#rst-f2) Usually this is `V4L2_PIX_FMT_GREY`, i. e. each sample consists of 8 bits with lower values oriented towards the black level. Do not assume any other correlation of values with the signal level. For example, the MSB does not necessarily indicate if the signal is 'high' or 'low' because 128 may not be the mean value of the signal. Drivers shall not convert the sample format by software.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`start`<a id="rst-footnote-reference-3"></a>[2](#rst-f2)

</td>
<td>


This is the scanning system line number associated with the first line of the VBI image, of the first and the second field respectively. See [vbi-525](<#rst-vbi-525>) and [vbi-625](<#rst-vbi-625>) for valid values. The `V4L2_VBI_ITU_525_F1_START`, `V4L2_VBI_ITU_525_F2_START`, `V4L2_VBI_ITU_625_F1_START` and `V4L2_VBI_ITU_625_F2_START` defines give the start line numbers for each field for each 525 or 625 line format as a convenience. Don't forget that ITU line numbering starts at 1, not 0. VBI input drivers can return start values 0 if the hardware cannot reliable identify scanning lines, VBI acquisition may not require this information.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`count`<a id="rst-footnote-reference-4"></a>[2](#rst-f2)

</td>
<td>


The number of lines in the first and second field image, respectively.

</td>
</tr>
<tr>
<td colspan="3">


Drivers should be as flexibility as possible. For example, it may be possible to extend or move the VBI capture window down to the picture area, implementing a 'full field mode' to capture data service transmissions embedded in the picture.

An application can set the first or second `count` value to zero if no data is required from the respective field; `count`\[1\] if the scanning system is progressive, i. e. not interlaced. The corresponding start value shall be ignored by the application and driver. Anyway, drivers may not support single field capturing and return both count values non-zero.

Both `count` values set to zero, or line numbers are outside the bounds depicted<a id="rst-footnote-reference-5"></a>[4](#rst-f4), or a field image covering lines of two fields, are invalid and shall not be returned by the driver.

To initialize the `start` and `count` fields, applications must first determine the current video standard selection. The [v4l2_std_id](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-enumstd.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) or the `framelines` field of struct `v4l2_standard` can be evaluated for this purpose.

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


See [vbifmt-flags](<#rst-vbifmt-flags>) below. Currently only drivers set flags, applications must set this field to zero.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`reserved`<a id="rst-footnote-reference-6"></a>[2](#rst-f2)

</td>
<td>


This array is reserved for future extensions. Drivers and applications must set it to zero.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{4.4cm}|p{1.5cm}|p{11.4cm}| -->

<a id="rst-vbifmt-flags"></a>


<table>
<caption>Raw VBI Format Flags</caption>
<tbody>
<tr>
<td>


`V4L2_VBI_UNSYNC`

</td>
<td>


0x0001

</td>
<td>


This flag indicates hardware which does not properly distinguish between fields. Normally the VBI image stores the first field (lower scanning line numbers) first in memory. This may be a top or bottom field depending on the video standard. When this flag is set the first or second field may be stored first, however the fields are still in correct temporal order with the older field first in memory. <a id="rst-footnote-reference-7"></a>[3](#rst-f3)

</td>
</tr>
<tr>
<td>


`V4L2_VBI_INTERLACED`

</td>
<td>


0x0002

</td>
<td>


By default the two field images will be passed sequentially; all lines of the first field followed by all lines of the second field (compare [Field Order](<~kernel/userspace/userspace-api/media-v4l/field-order#rst-field-order>) `V4L2_FIELD_SEQ_TB` and `V4L2_FIELD_SEQ_BT`, whether the top or bottom field is first in memory depends on the video standard). When this flag is set, the two fields are interlaced (cf. `V4L2_FIELD_INTERLACED`). The first line of the first field followed by the first line of the second field, then the two second lines, and so on. Such a layout may be necessary when the hardware has been programmed to capture or output interlaced video images and is unable to separate the fields for VBI capturing at the same time. For simplicity setting this flag implies that both `count` values are equal and non-zero.

</td>
</tr>
</tbody>
</table>

<a id="rst-vbi-hsync"></a>

![vbi_hsync.svg](asset-dc390d3e02a4-vbi-hsync.svg)

Line synchronization

<a id="rst-vbi-525"></a>

![vbi_525.svg](asset-91e44684f98a-vbi-525.svg)

ITU-R 525 line numbering (M/NTSC and M/PAL)

<a id="rst-vbi-625"></a>

![vbi_625.svg](asset-38b141cc6b75-vbi-625.svg)

ITU-R 625 line numbering

Remember the VBI image format depends on the selected video standard, therefore the application must choose a new standard or query the current standard first. Attempts to read or write data ahead of format negotiation, or after switching the video standard which may invalidate the negotiated VBI parameters, should be refused by the driver. A format change during active I/O is not permitted.

<a id="rst-reading-and-writing-vbi-images"></a>

## Reading and writing VBI images

To assure synchronization with the field number and easier implementation, the smallest unit of data passed at a time is one frame, consisting of two fields of VBI images immediately following in memory.

The total size of a frame computes as follows:



```c
(count[0] + count[1]) * samples_per_line * sample size in bytes
```

The sample size is most likely always one byte, applications must check the `sample_format` field though, to function properly with other drivers.

A VBI device may support [read/write](<~kernel/userspace/userspace-api/media-v4l/rw#rst-rw>) and/or streaming ([memory mapping](<~kernel/userspace/userspace-api/media-v4l/mmap#rst-mmap>) or [user pointer](<~kernel/userspace/userspace-api/media-v4l/userp#rst-userp>)) I/O. The latter bears the possibility of synchronizing video and VBI data by using buffer timestamps.

Remember the [VIDIOC_STREAMON](<~kernel/userspace/userspace-api/media-v4l/vidioc-streamon#rst-vidioc-streamon>) ioctl and the first `read()`, `write()` and `select()` call can be resource allocation points returning an `EBUSY` error code if the required hardware resources are temporarily unavailable, for example the device is already in use by another process.

<a id="rst-f1"></a>



**[1]** ASK: Amplitude-Shift Keying. A high signal level represents a '1' bit, a low level a '0' bit.

<a id="rst-f2"></a>



**[2]** A few devices may be unable to sample VBI data at all but can extend the video capture window to the VBI region.

<a id="rst-f3"></a>



**[3]** Most VBI services transmit on both fields, but some have different semantics depending on the field number. These cannot be reliable decoded or encoded when `V4L2_VBI_UNSYNC` is set.

<a id="rst-f4"></a>



**[4]** The valid values ar shown at [vbi-525](<#rst-vbi-525>) and [vbi-625](<#rst-vbi-625>).
