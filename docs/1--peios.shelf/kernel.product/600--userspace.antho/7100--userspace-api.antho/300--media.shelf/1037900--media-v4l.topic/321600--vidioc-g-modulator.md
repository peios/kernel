---
title: "ioctl VIDIOC_G_MODULATOR, VIDIOC_S_MODULATOR"
type: reference
description: "VIDIOC_G_MODULATOR - VIDIOC_S_MODULATOR - Get or set modulator attributes"
---

<a id="rst-ioctl-vidioc-g-modulator-vidioc-s-modulator"></a>
<a id="rst-vidioc-g-modulator"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_G_MODULATOR - VIDIOC_S_MODULATOR - Get or set modulator attributes

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_G_MODULATOR"></a>

```c
VIDIOC_G_MODULATOR
```

`int ioctl(int fd, VIDIOC_G_MODULATOR, struct v4l2_modulator *argp)`





<a id="c-VIDIOC_S_MODULATOR"></a>

```c
VIDIOC_S_MODULATOR
```

`int ioctl(int fd, VIDIOC_S_MODULATOR, const struct v4l2_modulator *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_modulator`.

<a id="rst-description"></a>

## Description

To query the attributes of a modulator applications initialize the `index` field and zero out the `reserved` array of a struct `v4l2_modulator` and call the [VIDIOC_G_MODULATOR](<#rst-vidioc-g-modulator>) ioctl with a pointer to this structure. Drivers fill the rest of the structure or return an `EINVAL` error code when the index is out of bounds. To enumerate all modulators applications shall begin at index zero, incrementing by one until the driver returns EINVAL.

Modulators have two writable properties, an audio modulation set and the radio frequency. To change the modulated audio subprograms, applications initialize the `index` and `txsubchans` fields and the `reserved` array and call the [VIDIOC_S_MODULATOR](<#rst-vidioc-g-modulator>) ioctl. Drivers may choose a different audio modulation if the request cannot be satisfied. However this is a write-only ioctl, it does not return the actual audio modulation selected.

[SDR](<~kernel/userspace/userspace-api/media-v4l/dev-sdr#rst-sdr>) specific modulator types are `V4L2_TUNER_SDR` and `V4L2_TUNER_RF`. For SDR devices `txsubchans` field must be initialized to zero. The term 'modulator' means SDR transmitter in this context.

To change the radio frequency the [VIDIOC_S_FREQUENCY](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-frequency#rst-vidioc-g-frequency>) ioctl is available.

<!-- tabularcolumns: |p{2.9cm}|p{2.9cm}|p{5.8cm}|p{2.9cm}|p{2.4cm}| -->





<a id="c-v4l2_modulator"></a>

```c
v4l2_modulator
```


<table>
<caption>struct v4l2_modulator</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`index`

</td>
<td colspan="3">


Identifies the modulator, set by the application.

</td>
</tr>
<tr>
<td>


\__u8

</td>
<td>


`name`\[32\]

</td>
<td colspan="3">


Name of the modulator, a NUL-terminated ASCII string.

This information is intended for the user.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`capability`

</td>
<td colspan="3">


Modulator capability flags. No flags are defined for this field, the tuner flags in struct `v4l2_tuner` are used accordingly. The audio flags indicate the ability to encode audio subprograms. They will *not* change for example with the current video standard.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`rangelow`

</td>
<td colspan="3">


The lowest tunable frequency in units of 62.5 KHz, or if the `capability` flag `V4L2_TUNER_CAP_LOW` is set, in units of 62.5 Hz, or if the `capability` flag `V4L2_TUNER_CAP_1HZ` is set, in units of 1 Hz.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`rangehigh`

</td>
<td colspan="3">


The highest tunable frequency in units of 62.5 KHz, or if the `capability` flag `V4L2_TUNER_CAP_LOW` is set, in units of 62.5 Hz, or if the `capability` flag `V4L2_TUNER_CAP_1HZ` is set, in units of 1 Hz.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`txsubchans`

</td>
<td colspan="3">


With this field applications can determine how audio sub-carriers shall be modulated. It contains a set of flags as defined in [modulator-txsubchans](<#rst-modulator-txsubchans>).

> [!NOTE]
>
> The tuner `rxsubchans` flags  are reused, but the semantics are different. Video output devices are assumed to have an analog or PCM audio input with 1-3 channels. The `txsubchans` flags select one or more channels for modulation, together with some audio subprogram indicator, for example, a stereo pilot tone.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`type`

</td>
<td colspan="3">


 Type of the modulator, see `v4l2_tuner_type`.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`reserved`\[3\]

</td>
<td colspan="3">


Reserved for future extensions.

Drivers and applications must set the array to zero.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{6.0cm}|p{2.0cm}|p{9.3cm}| -->

<a id="rst-modulator-txsubchans"></a>


<table>
<caption>Modulator Audio Transmission Flags</caption>
<tbody>
<tr>
<td>


`V4L2_TUNER_SUB_MONO`

</td>
<td>


0x0001

</td>
<td>


Modulate channel 1 as mono audio, when the input has more channels, a down-mix of channel 1 and 2. This flag does not combine with `V4L2_TUNER_SUB_STEREO` or `V4L2_TUNER_SUB_LANG1`.

</td>
</tr>
<tr>
<td>


`V4L2_TUNER_SUB_STEREO`

</td>
<td>


0x0002

</td>
<td>


Modulate channel 1 and 2 as left and right channel of a stereo audio signal. When the input has only one channel or two channels and `V4L2_TUNER_SUB_SAP` is also set, channel 1 is encoded as left and right channel. This flag does not combine with `V4L2_TUNER_SUB_MONO` or `V4L2_TUNER_SUB_LANG1`. When the driver does not support stereo audio it shall fall back to mono.

</td>
</tr>
<tr>
<td>


`V4L2_TUNER_SUB_LANG1`

</td>
<td>


0x0008

</td>
<td>


Modulate channel 1 and 2 as primary and secondary language of a bilingual audio signal. When the input has only one channel it is used for both languages. It is not possible to encode the primary or secondary language only. This flag does not combine with `V4L2_TUNER_SUB_MONO`, `V4L2_TUNER_SUB_STEREO` or `V4L2_TUNER_SUB_SAP`. If the hardware does not support the respective audio matrix, or the current video standard does not permit bilingual audio the [VIDIOC_S_MODULATOR](<#rst-vidioc-g-modulator>) ioctl shall return an `EINVAL` error code and the driver shall fall back to mono or stereo mode.

</td>
</tr>
<tr>
<td>


`V4L2_TUNER_SUB_LANG2`

</td>
<td>


0x0004

</td>
<td>


Same effect as `V4L2_TUNER_SUB_SAP`.

</td>
</tr>
<tr>
<td>


`V4L2_TUNER_SUB_SAP`

</td>
<td>


0x0004

</td>
<td>


When combined with `V4L2_TUNER_SUB_MONO` the first channel is encoded as mono audio, the last channel as Second Audio Program. When the input has only one channel it is used for both audio tracks. When the input has three channels the mono track is a down-mix of channel 1 and 2. When combined with `V4L2_TUNER_SUB_STEREO` channel 1 and 2 are encoded as left and right stereo audio, channel 3 as Second Audio Program. When the input has only two channels, the first is encoded as left and right channel and the second as SAP. When the input has only one channel it is used for all audio tracks. It is not possible to encode a Second Audio Program only. This flag must combine with `V4L2_TUNER_SUB_MONO` or `V4L2_TUNER_SUB_STEREO`. If the hardware does not support the respective audio matrix, or the current video standard does not permit SAP the [VIDIOC_S_MODULATOR](<#rst-vidioc-g-modulator>) ioctl shall return an `EINVAL` error code and driver shall fall back to mono or stereo mode.

</td>
</tr>
<tr>
<td>


`V4L2_TUNER_SUB_RDS`

</td>
<td>


0x0010

</td>
<td>


Enable the RDS encoder for a radio FM transmitter.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  The struct `v4l2_modulator` `index` is out of bounds.
