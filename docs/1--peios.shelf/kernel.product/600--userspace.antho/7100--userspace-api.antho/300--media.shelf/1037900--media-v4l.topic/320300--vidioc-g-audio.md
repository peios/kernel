---
title: "ioctl VIDIOC_G_AUDIO, VIDIOC_S_AUDIO"
type: reference
description: "VIDIOC_G_AUDIO - VIDIOC_S_AUDIO - Query or select the current audio input and its attributes"
---

<a id="rst-ioctl-vidioc-g-audio-vidioc-s-audio"></a>
<a id="rst-vidioc-g-audio"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_G_AUDIO - VIDIOC_S_AUDIO - Query or select the current audio input and its attributes

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_G_AUDIO"></a>

```c
VIDIOC_G_AUDIO
```

`int ioctl(int fd, VIDIOC_G_AUDIO, struct v4l2_audio *argp)`





<a id="c-VIDIOC_S_AUDIO"></a>

```c
VIDIOC_S_AUDIO
```

`int ioctl(int fd, VIDIOC_S_AUDIO, const struct v4l2_audio *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_audio`.

<a id="rst-description"></a>

## Description

To query the current audio input applications zero out the `reserved` array of a struct `v4l2_audio` and call the [VIDIOC_G_AUDIO](<#rst-vidioc-g-audio>) ioctl with a pointer to this structure. Drivers fill the rest of the structure or return an `EINVAL` error code when the device has no audio inputs, or none which combine with the current video input.

Audio inputs have one writable property, the audio mode. To select the current audio input *and* change the audio mode, applications initialize the `index` and `mode` fields, and the `reserved` array of a struct `v4l2_audio` structure and call the [VIDIOC_S_AUDIO](<#rst-vidioc-g-audio>) ioctl. Drivers may switch to a different audio mode if the request cannot be satisfied. However, this is a write-only ioctl, it does not return the actual new audio mode.

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->





<a id="c-v4l2_audio"></a>

```c
v4l2_audio
```


<table>
<caption>struct v4l2_audio</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`index`

</td>
<td>


Identifies the audio input, set by the driver or application.

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


Name of the audio input, a NUL-terminated ASCII string, for example: "Line In". This information is intended for the user, preferably the connector label on the device itself.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`capability`

</td>
<td>


Audio capability flags, see [audio-capability](<#rst-audio-capability>).

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`mode`

</td>
<td>


Audio mode flags set by drivers and applications (on [VIDIOC_S_AUDIO](<#rst-vidioc-g-audio>) ioctl), see [audio-mode](<#rst-audio-mode>).

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`reserved`\[2\]

</td>
<td>


Reserved for future extensions. Drivers and applications must set the array to zero.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{6.6cm}|p{2.2cm}|p{8.5cm}| -->

<a id="rst-audio-capability"></a>


<table>
<caption>Audio Capability Flags</caption>
<tbody>
<tr>
<td>


`V4L2_AUDCAP_STEREO`

</td>
<td>


0x00001

</td>
<td>


This is a stereo input. The flag is intended to automatically disable stereo recording etc. when the signal is always monaural. The API provides no means to detect if stereo is *received*, unless the audio input belongs to a tuner.

</td>
</tr>
<tr>
<td>


`V4L2_AUDCAP_AVL`

</td>
<td>


0x00002

</td>
<td>


Automatic Volume Level mode is supported.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{6.6cm}|p{2.2cm}|p{8.5cm}| -->

<a id="rst-audio-mode"></a>


<table>
<caption>Audio Mode Flags</caption>
<tbody>
<tr>
<td>


`V4L2_AUDMODE_AVL`

</td>
<td>


0x00001

</td>
<td>


AVL mode is on.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  No audio inputs combine with the current video input, or the number of the selected audio input is out of bounds or it does not combine.
