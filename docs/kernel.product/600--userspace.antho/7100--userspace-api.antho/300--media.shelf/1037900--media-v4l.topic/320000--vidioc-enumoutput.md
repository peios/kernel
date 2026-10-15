---
title: "ioctl VIDIOC_ENUMOUTPUT"
type: reference
description: "VIDIOC_ENUMOUTPUT - Enumerate video outputs"
---

<a id="rst-ioctl-vidioc-enumoutput"></a>
<a id="rst-vidioc-enumoutput"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_ENUMOUTPUT - Enumerate video outputs

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_ENUMOUTPUT"></a>

```c
VIDIOC_ENUMOUTPUT
```

`int ioctl(int fd, VIDIOC_ENUMOUTPUT, struct v4l2_output *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_output`.

<a id="rst-description"></a>

## Description

To query the attributes of a video outputs applications initialize the `index` field of struct `v4l2_output` and call the [ioctl VIDIOC_ENUMOUTPUT](<#rst-vidioc-enumoutput>) with a pointer to this structure. Drivers fill the rest of the structure or return an `EINVAL` error code when the index is out of bounds. To enumerate all outputs applications shall begin at index zero, incrementing by one until the driver returns `EINVAL`.

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->





<a id="c-v4l2_output"></a>

```c
v4l2_output
```


<table>
<caption>struct v4l2_output</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`index`

</td>
<td>


Identifies the output, set by the application.

</td>
</tr>
<tr>
<td>


\__u8

</td>
<td>


`name`\[32\]

</td>
<td>


Name of the video output, a NUL-terminated ASCII string, for example: "Vout". This information is intended for the user, preferably the connector label on the device itself.

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


Type of the output, see [output-type](<#rst-output-type>).

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`audioset`

</td>
<td>


Drivers can enumerate up to 32 video and audio outputs. This field shows which audio outputs were selectable as the current output if this was the currently selected video output. It is a bit mask. The LSB corresponds to audio output 0, the MSB to output 31. Any number of bits can be set, or none.

When the driver does not enumerate audio outputs no bits must be set. Applications shall not interpret this as lack of audio support. Drivers may automatically select audio outputs without enumerating them.

For details on audio outputs and how to select the current output see [Audio Inputs and Outputs](<~kernel/userspace/userspace-api/media-v4l/audio#rst-audio>).

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`modulator`

</td>
<td>


Output devices can have zero or more RF modulators. When the `type` is `V4L2_OUTPUT_TYPE_MODULATOR` this is an RF connector and this field identifies the modulator. It corresponds to struct `v4l2_modulator` field `index`. For details on modulators see [Tuners and Modulators](<~kernel/userspace/userspace-api/media-v4l/tuner#rst-tuner>).

</td>
</tr>
<tr>
<td>


[v4l2_std_id](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-enumstd.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)

</td>
<td>


`std`

</td>
<td>


Every video output supports one or more different video standards. This field is a set of all supported standards. For details on video standards and how to switch see [Video Standards](<~kernel/userspace/userspace-api/media-v4l/standard#rst-standard>).

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`capabilities`

</td>
<td>


This field provides capabilities for the output. See [output-capabilities](<#rst-output-capabilities>) for flags.

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

<!-- tabularcolumns: |p{7.5cm}|p{0.6cm}|p{9.2cm}| -->

<a id="rst-output-type"></a>


<table>
<caption>Output Type</caption>
<tbody>
<tr>
<td>


`V4L2_OUTPUT_TYPE_MODULATOR`

</td>
<td>


1

</td>
<td>


This output is an analog TV modulator.

</td>
</tr>
<tr>
<td>


`V4L2_OUTPUT_TYPE_ANALOG`

</td>
<td>


2

</td>
<td>


Any non-modulator video output, for example Composite Video, S-Video, HDMI. The naming as `_TYPE_ANALOG` is historical, today we would have called it `_TYPE_VIDEO`.

</td>
</tr>
<tr>
<td>


`V4L2_OUTPUT_TYPE_ANALOGVGAOVERLAY`

</td>
<td>


3

</td>
<td>


The video output will be copied to a [video overlay](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/dev-overlay.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>).

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{6.4cm}|p{2.4cm}|p{8.5cm}| -->

<a id="rst-output-capabilities"></a>


<table>
<caption>Output capabilities</caption>
<tbody>
<tr>
<td>


`V4L2_OUT_CAP_DV_TIMINGS`

</td>
<td>


0x00000002

</td>
<td>


This output supports setting video timings by using `VIDIOC_S_DV_TIMINGS`.

</td>
</tr>
<tr>
<td>


`V4L2_OUT_CAP_STD`

</td>
<td>


0x00000004

</td>
<td>


This output supports setting the TV standard by using `VIDIOC_S_STD`.

</td>
</tr>
<tr>
<td>


`V4L2_OUT_CAP_NATIVE_SIZE`

</td>
<td>


0x00000008

</td>
<td>


This output supports setting the native size using the `V4L2_SEL_TGT_NATIVE_SIZE` selection target, see [Common selection definitions](<~kernel/userspace/userspace-api/media-v4l/selections-common#rst-v4l2-selections-common>).

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  The struct `v4l2_output` `index` is out of bounds.
