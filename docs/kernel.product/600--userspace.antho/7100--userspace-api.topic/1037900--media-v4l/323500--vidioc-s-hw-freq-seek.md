---
title: "ioctl VIDIOC_S_HW_FREQ_SEEK"
type: reference
description: "VIDIOC_S_HW_FREQ_SEEK - Perform a hardware frequency seek"
---

<a id="rst-ioctl-vidioc-s-hw-freq-seek"></a>
<a id="rst-vidioc-s-hw-freq-seek"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_S_HW_FREQ_SEEK - Perform a hardware frequency seek

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_S_HW_FREQ_SEEK"></a>

```c
VIDIOC_S_HW_FREQ_SEEK
```

`int ioctl(int fd, VIDIOC_S_HW_FREQ_SEEK, struct v4l2_hw_freq_seek *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_hw_freq_seek`.

<a id="rst-description"></a>

## Description

Start a hardware frequency seek from the current frequency. To do this applications initialize the `tuner`, `type`, `seek_upward`, `wrap_around`, `spacing`, `rangelow` and `rangehigh` fields, and zero out the `reserved` array of a struct `v4l2_hw_freq_seek` and call the `VIDIOC_S_HW_FREQ_SEEK` ioctl with a pointer to this structure.

The `rangelow` and `rangehigh` fields can be set to a non-zero value to tell the driver to search a specific band. If the struct `v4l2_tuner` `capability` field has the `V4L2_TUNER_CAP_HWSEEK_PROG_LIM` flag set, these values must fall within one of the bands returned by [ioctl VIDIOC_ENUM_FREQ_BANDS](<~kernel/userspace/userspace-api/media-v4l/vidioc-enum-freq-bands#rst-vidioc-enum-freq-bands>). If the `V4L2_TUNER_CAP_HWSEEK_PROG_LIM` flag is not set, then these values must exactly match those of one of the bands returned by [ioctl VIDIOC_ENUM_FREQ_BANDS](<~kernel/userspace/userspace-api/media-v4l/vidioc-enum-freq-bands#rst-vidioc-enum-freq-bands>). If the current frequency of the tuner does not fall within the selected band it will be clamped to fit in the band before the seek is started.

If an error is returned, then the original frequency will be restored.

This ioctl is supported if the `V4L2_CAP_HW_FREQ_SEEK` capability is set.

If this ioctl is called from a non-blocking filehandle, then `EAGAIN` error code is returned and no seek takes place.

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->





<a id="c-v4l2_hw_freq_seek"></a>

```c
v4l2_hw_freq_seek
```


<table>
<caption>struct v4l2_hw_freq_seek</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`tuner`

</td>
<td>


The tuner index number. This is the same value as in the struct `v4l2_input` `tuner` field and the struct `v4l2_tuner` `index` field.

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


The tuner type. This is the same value as in the struct `v4l2_tuner` `type` field. See `v4l2_tuner_type`

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`seek_upward`

</td>
<td>


If non-zero, seek upward from the current frequency, else seek downward.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`wrap_around`

</td>
<td>


If non-zero, wrap around when at the end of the frequency range, else stop seeking. The struct `v4l2_tuner` `capability` field will tell you what the hardware supports.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`spacing`

</td>
<td>


If non-zero, defines the hardware seek resolution in Hz. The driver selects the nearest value that is supported by the device. If spacing is zero a reasonable default value is used.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`rangelow`

</td>
<td>


If non-zero, the lowest tunable frequency of the band to search in units of 62.5 kHz, or if the struct `v4l2_tuner` `capability` field has the `V4L2_TUNER_CAP_LOW` flag set, in units of 62.5 Hz or if the struct `v4l2_tuner` `capability` field has the `V4L2_TUNER_CAP_1HZ` flag set, in units of 1 Hz. If `rangelow` is zero a reasonable default value is used.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`rangehigh`

</td>
<td>


If non-zero, the highest tunable frequency of the band to search in units of 62.5 kHz, or if the struct `v4l2_tuner` `capability` field has the `V4L2_TUNER_CAP_LOW` flag set, in units of 62.5 Hz or if the struct `v4l2_tuner` `capability` field has the `V4L2_TUNER_CAP_1HZ` flag set, in units of 1 Hz. If `rangehigh` is zero a reasonable default value is used.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`reserved`\[5\]

</td>
<td>


Reserved for future extensions. Applications must set the array to zero.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  The `tuner` index is out of bounds, the `wrap_around` value is not supported or one of the values in the `type`, `rangelow` or `rangehigh` fields is wrong.

- **EAGAIN**

  Attempted to call `VIDIOC_S_HW_FREQ_SEEK` with the filehandle in non-blocking mode.

- **ENODATA**

  The hardware seek found no channels.

- **EBUSY**

  Another hardware seek is already in progress.
