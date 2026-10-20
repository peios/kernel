---
title: "ioctl VIDIOC_G_AUDOUT, VIDIOC_S_AUDOUT"
type: reference
description: "VIDIOC_G_AUDOUT - VIDIOC_S_AUDOUT - Query or select the current audio output"
---

<a id="rst-ioctl-vidioc-g-audout-vidioc-s-audout"></a>
<a id="rst-vidioc-g-audout"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_G_AUDOUT - VIDIOC_S_AUDOUT - Query or select the current audio output

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_G_AUDOUT"></a>

```c
VIDIOC_G_AUDOUT
```

`int ioctl(int fd, VIDIOC_G_AUDOUT, struct v4l2_audioout *argp)`





<a id="c-VIDIOC_S_AUDOUT"></a>

```c
VIDIOC_S_AUDOUT
```

`int ioctl(int fd, VIDIOC_S_AUDOUT, const struct v4l2_audioout *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_audioout`.

<a id="rst-description"></a>

## Description

To query the current audio output applications zero out the `reserved` array of a struct `v4l2_audioout` and call the `VIDIOC_G_AUDOUT` ioctl with a pointer to this structure. Drivers fill the rest of the structure or return an `EINVAL` error code when the device has no audio inputs, or none which combine with the current video output.

Audio outputs have no writable properties. Nevertheless, to select the current audio output applications can initialize the `index` field and `reserved` array (which in the future may contain writable properties) of a struct `v4l2_audioout` structure and call the `VIDIOC_S_AUDOUT` ioctl. Drivers switch to the requested output or return the `EINVAL` error code when the index is out of bounds. This is a write-only ioctl, it does not return the current audio output attributes as `VIDIOC_G_AUDOUT` does.

> [!NOTE]
>
> Connectors on a TV card to loop back the received audio signal to a sound card are not audio outputs in this sense.





<a id="c-v4l2_audioout"></a>

```c
v4l2_audioout
```

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->


<table>
<caption>struct v4l2_audioout</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`index`

</td>
<td>


Identifies the audio output, set by the driver or application.

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


Name of the audio output, a NUL-terminated ASCII string, for example: "Line Out". This information is intended for the user, preferably the connector label on the device itself.

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


Audio capability flags, none defined yet. Drivers must set this field to zero.

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


Audio mode, none defined yet. Drivers and applications (on `VIDIOC_S_AUDOUT`) must set this field to zero.

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

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  No audio outputs combine with the current video output, or the number of the selected audio output is out of bounds or it does not combine.
