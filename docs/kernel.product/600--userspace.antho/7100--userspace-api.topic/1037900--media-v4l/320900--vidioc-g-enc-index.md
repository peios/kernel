---
title: "ioctl VIDIOC_G_ENC_INDEX"
type: reference
description: "VIDIOC_G_ENC_INDEX - Get meta data about a compressed video stream"
---

<a id="rst-ioctl-vidioc-g-enc-index"></a>
<a id="rst-vidioc-g-enc-index"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_G_ENC_INDEX - Get meta data about a compressed video stream

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_G_ENC_INDEX"></a>

```c
VIDIOC_G_ENC_INDEX
```

`int ioctl(int fd, VIDIOC_G_ENC_INDEX, struct v4l2_enc_idx *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_enc_idx`.

<a id="rst-description"></a>

## Description

The [VIDIOC_G_ENC_INDEX](<#rst-vidioc-g-enc-index>) ioctl provides meta data about a compressed video stream the same or another application currently reads from the driver, which is useful for random access into the stream without decoding it.

To read the data applications must call [VIDIOC_G_ENC_INDEX](<#rst-vidioc-g-enc-index>) with a pointer to a struct `v4l2_enc_idx`. On success the driver fills the `entry` array, stores the number of elements written in the `entries` field, and initializes the `entries_cap` field.

Each element of the `entry` array contains meta data about one picture. A [VIDIOC_G_ENC_INDEX](<#rst-vidioc-g-enc-index>) call reads up to `V4L2_ENC_IDX_ENTRIES` entries from a driver buffer, which can hold up to `entries_cap` entries. This number can be lower or higher than `V4L2_ENC_IDX_ENTRIES`, but not zero. When the application fails to read the meta data in time the oldest entries will be lost. When the buffer is empty or no capturing/encoding is in progress, `entries` will be zero.

Currently this ioctl is only defined for MPEG-2 program streams and video elementary streams.

<!-- tabularcolumns: |p{4.2cm}|p{6.2cm}|p{6.9cm}| -->





<a id="c-v4l2_enc_idx"></a>

```c
v4l2_enc_idx
```


<table>
<caption>struct v4l2_enc_idx</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`entries`

</td>
<td>


The number of entries the driver stored in the `entry` array.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`entries_cap`

</td>
<td>


The number of entries the driver can buffer. Must be greater than zero.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`reserved`\[4\]

</td>
<td>


Reserved for future extensions. Drivers must set the array to zero.

</td>
</tr>
<tr>
<td>


struct `v4l2_enc_idx_entry`

</td>
<td>


`entry`\[`V4L2_ENC_IDX_ENTRIES`\]

</td>
<td>


Meta data about a compressed video stream. Each element of the array corresponds to one picture, sorted in ascending order by their `offset`.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->





<a id="c-v4l2_enc_idx_entry"></a>

```c
v4l2_enc_idx_entry
```


<table>
<caption>struct v4l2_enc_idx_entry</caption>
<tbody>
<tr>
<td>


\__u64

</td>
<td>


`offset`

</td>
<td>


The offset in bytes from the beginning of the compressed video stream to the beginning of this picture, that is a *PES packet header* as defined in [ISO 13818-1](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-mpeg2part1>) or a *picture header* as defined in [ISO 13818-2](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-mpeg2part2>). When the encoder is stopped, the driver resets the offset to zero.

</td>
</tr>
<tr>
<td>


\__u64

</td>
<td>


`pts`

</td>
<td>


The 33 bit *Presentation Time Stamp* of this picture as defined in [ISO 13818-1](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-mpeg2part1>).

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`length`

</td>
<td>


The length of this picture in bytes.

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


Flags containing the coding type of this picture, see [enc-idx-flags](<#rst-enc-idx-flags>).

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


Reserved for future extensions. Drivers must set the array to zero.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{6.6cm}|p{2.2cm}|p{8.5cm}| -->

<a id="rst-enc-idx-flags"></a>


<table>
<caption>Index Entry Flags</caption>
<tbody>
<tr>
<td>


`V4L2_ENC_IDX_FRAME_I`

</td>
<td>


0x00

</td>
<td>


This is an Intra-coded picture.

</td>
</tr>
<tr>
<td>


`V4L2_ENC_IDX_FRAME_P`

</td>
<td>


0x01

</td>
<td>


This is a Predictive-coded picture.

</td>
</tr>
<tr>
<td>


`V4L2_ENC_IDX_FRAME_B`

</td>
<td>


0x02

</td>
<td>


This is a Bidirectionally predictive-coded picture.

</td>
</tr>
<tr>
<td>


`V4L2_ENC_IDX_FRAME_MASK`

</td>
<td>


0x0F

</td>
<td>


*AND* the flags field with this mask to obtain the picture coding type.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
