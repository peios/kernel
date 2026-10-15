---
title: "ioctl VIDIOC_ENUMINPUT"
type: reference
description: "VIDIOC_ENUMINPUT - Enumerate video inputs"
---

<a id="rst-ioctl-vidioc-enuminput"></a>
<a id="rst-vidioc-enuminput"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_ENUMINPUT - Enumerate video inputs

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_ENUMINPUT"></a>

```c
VIDIOC_ENUMINPUT
```

`int ioctl(int fd, VIDIOC_ENUMINPUT, struct v4l2_input *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_input`.

<a id="rst-description"></a>

## Description

To query the attributes of a video input applications initialize the `index` field of struct `v4l2_input` and call the [ioctl VIDIOC_ENUMINPUT](<#rst-vidioc-enuminput>) with a pointer to this structure. Drivers fill the rest of the structure or return an `EINVAL` error code when the index is out of bounds. To enumerate all inputs applications shall begin at index zero, incrementing by one until the driver returns `EINVAL`.

<!-- tabularcolumns: |p{3.0cm}|p{3.5cm}|p{10.8cm}| -->





<a id="c-v4l2_input"></a>

```c
v4l2_input
```


<table>
<caption>struct v4l2_input</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`index`

</td>
<td>


Identifies the input, set by the application.

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


Name of the video input, a NUL-terminated ASCII string, for example: "Vin (Composite 2)". This information is intended for the user, preferably the connector label on the device itself.

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


Type of the input, see [input-type](<#rst-input-type>).

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


Drivers can enumerate up to 32 video and audio inputs. This field shows which audio inputs were selectable as audio source if this was the currently selected video input. It is a bit mask. The LSB corresponds to audio input 0, the MSB to input 31. Any number of bits can be set, or none.

When the driver does not enumerate audio inputs no bits must be set. Applications shall not interpret this as lack of audio support. Some drivers automatically select audio sources and do not enumerate them since there is no choice anyway.

For details on audio inputs and how to select the current input see [Audio Inputs and Outputs](<~kernel/userspace/userspace-api/media-v4l/audio#rst-audio>).

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`tuner`

</td>
<td>


Capture devices can have zero or more tuners (RF demodulators). When the `type` is set to `V4L2_INPUT_TYPE_TUNER` this is an RF connector and this field identifies the tuner. It corresponds to struct `v4l2_tuner` field `index`. For details on tuners see [Tuners and Modulators](<~kernel/userspace/userspace-api/media-v4l/tuner#rst-tuner>).

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


Every video input supports one or more different video standards. This field is a set of all supported standards. For details on video standards and how to switch see [Video Standards](<~kernel/userspace/userspace-api/media-v4l/standard#rst-standard>).

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`status`

</td>
<td>


This field provides status information about the input. See [input-status](<#rst-input-status>) for flags. With the exception of the sensor orientation bits `status` is only valid when this is the current input.

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


This field provides capabilities for the input. See [input-capabilities](<#rst-input-capabilities>) for flags.

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

<!-- tabularcolumns: |p{6.6cm}|p{1.0cm}|p{9.7cm}| -->

<a id="rst-input-type"></a>


<table>
<caption>Input Types</caption>
<tbody>
<tr>
<td>


`V4L2_INPUT_TYPE_TUNER`

</td>
<td>


1

</td>
<td>


This input uses a tuner (RF demodulator).

</td>
</tr>
<tr>
<td>


`V4L2_INPUT_TYPE_CAMERA`

</td>
<td>


2

</td>
<td>


Any non-tuner video input, for example Composite Video, S-Video, HDMI, camera sensor. The naming as `_TYPE_CAMERA` is historical, today we would have called it `_TYPE_VIDEO`.

</td>
</tr>
<tr>
<td>


`V4L2_INPUT_TYPE_TOUCH`

</td>
<td>


3

</td>
<td>


This input is a touch device for capturing raw touch data.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{5.6cm}|p{2.6cm}|p{9.1cm}| -->

<a id="rst-input-status"></a>


<table>
<caption>Input Status Flags</caption>
<tbody>
<tr>
<td colspan="3">


 General

</td>
</tr>
<tr>
<td>


`V4L2_IN_ST_NO_POWER`

</td>
<td>


0x00000001

</td>
<td>


Attached device is off.

</td>
</tr>
<tr>
<td>


`V4L2_IN_ST_NO_SIGNAL`

</td>
<td>


0x00000002

</td>
<td>




</td>
</tr>
<tr>
<td>


`V4L2_IN_ST_NO_COLOR`

</td>
<td>


0x00000004

</td>
<td>


The hardware supports color decoding, but does not detect color modulation in the signal.

</td>
</tr>
<tr>
<td colspan="3">


 Sensor Orientation

</td>
</tr>
<tr>
<td>


`V4L2_IN_ST_HFLIP`

</td>
<td>


0x00000010

</td>
<td>


The input is connected to a device that produces a signal that is flipped horizontally and does not correct this before passing the signal to userspace.

</td>
</tr>
<tr>
<td>


`V4L2_IN_ST_VFLIP`

</td>
<td>


0x00000020

</td>
<td>


The input is connected to a device that produces a signal that is flipped vertically and does not correct this before passing the signal to userspace. .. note:: A 180 degree rotation is the same as HFLIP \| VFLIP

</td>
</tr>
<tr>
<td colspan="3">


 Analog Video

</td>
</tr>
<tr>
<td>


`V4L2_IN_ST_NO_H_LOCK`

</td>
<td>


0x00000100

</td>
<td>


No horizontal sync lock.

</td>
</tr>
<tr>
<td>


`V4L2_IN_ST_COLOR_KILL`

</td>
<td>


0x00000200

</td>
<td>


A color killer circuit automatically disables color decoding when it detects no color modulation. When this flag is set the color killer is enabled *and* has shut off color decoding.

</td>
</tr>
<tr>
<td>


`V4L2_IN_ST_NO_V_LOCK`

</td>
<td>


0x00000400

</td>
<td>


No vertical sync lock.

</td>
</tr>
<tr>
<td>


`V4L2_IN_ST_NO_STD_LOCK`

</td>
<td>


0x00000800

</td>
<td>


No standard format lock in case of auto-detection format by the component.

</td>
</tr>
<tr>
<td colspan="3">


 Digital Video

</td>
</tr>
<tr>
<td>


`V4L2_IN_ST_NO_SYNC`

</td>
<td>


0x00010000

</td>
<td>


No synchronization lock.

</td>
</tr>
<tr>
<td>


`V4L2_IN_ST_NO_EQU`

</td>
<td>


0x00020000

</td>
<td>


No equalizer lock.

</td>
</tr>
<tr>
<td>


`V4L2_IN_ST_NO_CARRIER`

</td>
<td>


0x00040000

</td>
<td>


Carrier recovery failed.

</td>
</tr>
<tr>
<td colspan="3">


 VCR and Set-Top Box

</td>
</tr>
<tr>
<td>


`V4L2_IN_ST_MACROVISION`

</td>
<td>


0x01000000

</td>
<td>


Macrovision is an analog copy prevention system mangling the video signal to confuse video recorders. When this flag is set Macrovision has been detected.

</td>
</tr>
<tr>
<td>


`V4L2_IN_ST_NO_ACCESS`

</td>
<td>


0x02000000

</td>
<td>


Conditional access denied.

</td>
</tr>
<tr>
<td>


`V4L2_IN_ST_VTR`

</td>
<td>


0x04000000

</td>
<td>


VTR time constant. \[?\]

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{6.6cm}|p{2.4cm}|p{8.3cm}| -->

<a id="rst-input-capabilities"></a>


<table>
<caption>Input capabilities</caption>
<tbody>
<tr>
<td>


`V4L2_IN_CAP_DV_TIMINGS`

</td>
<td>


0x00000002

</td>
<td>


This input supports setting video timings by using `VIDIOC_S_DV_TIMINGS`.

</td>
</tr>
<tr>
<td>


`V4L2_IN_CAP_STD`

</td>
<td>


0x00000004

</td>
<td>


This input supports setting the TV standard by using `VIDIOC_S_STD`.

</td>
</tr>
<tr>
<td>


`V4L2_IN_CAP_NATIVE_SIZE`

</td>
<td>


0x00000008

</td>
<td>


This input supports setting the native size using the `V4L2_SEL_TGT_NATIVE_SIZE` selection target, see [Common selection definitions](<~kernel/userspace/userspace-api/media-v4l/selections-common#rst-v4l2-selections-common>).

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  The struct `v4l2_input` `index` is out of bounds.
