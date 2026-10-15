---
title: "ioctl VIDIOC_G_FREQUENCY, VIDIOC_S_FREQUENCY"
type: reference
description: "VIDIOC_G_FREQUENCY - VIDIOC_S_FREQUENCY - Get or set tuner or modulator radio frequency"
---

<a id="rst-ioctl-vidioc-g-frequency-vidioc-s-frequency"></a>
<a id="rst-vidioc-g-frequency"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_G_FREQUENCY - VIDIOC_S_FREQUENCY - Get or set tuner or modulator radio frequency

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_G_FREQUENCY"></a>

```c
VIDIOC_G_FREQUENCY
```

`int ioctl(int fd, VIDIOC_G_FREQUENCY, struct v4l2_frequency *argp)`





<a id="c-VIDIOC_S_FREQUENCY"></a>

```c
VIDIOC_S_FREQUENCY
```

`int ioctl(int fd, VIDIOC_S_FREQUENCY, const struct v4l2_frequency *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_frequency`.

<a id="rst-description"></a>

## Description

To get the current tuner or modulator radio frequency applications set the `tuner` field of a struct `v4l2_frequency` to the respective tuner or modulator number (only input devices have tuners, only output devices have modulators), zero out the `reserved` array and call the [VIDIOC_G_FREQUENCY](<#rst-vidioc-g-frequency>) ioctl with a pointer to this structure. The driver stores the current frequency in the `frequency` field.

To change the current tuner or modulator radio frequency applications initialize the `tuner`, `type` and `frequency` fields, and the `reserved` array of a struct `v4l2_frequency` and call the [VIDIOC_S_FREQUENCY](<#rst-vidioc-g-frequency>) ioctl with a pointer to this structure. When the requested frequency is not possible the driver assumes the closest possible value. However [VIDIOC_S_FREQUENCY](<#rst-vidioc-g-frequency>) is a write-only ioctl, it does not return the actual new frequency.

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->





<a id="c-v4l2_frequency"></a>

```c
v4l2_frequency
```


<table>
<caption>struct v4l2_frequency</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`tuner`

</td>
<td>


The tuner or modulator index number. This is the same value as in the struct `v4l2_input` `tuner` field and the struct `v4l2_tuner` `index` field, or the struct `v4l2_output` `modulator` field and the struct `v4l2_modulator` `index` field.

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


The tuner type. This is the same value as in the struct `v4l2_tuner` `type` field. The type must be set to `V4L2_TUNER_RADIO` for `/dev/radioX` device nodes, and to `V4L2_TUNER_ANALOG_TV` for all others. Set this field to `V4L2_TUNER_RADIO` for modulators (currently only radio modulators are supported). See `v4l2_tuner_type`

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`frequency`

</td>
<td>


Tuning frequency in units of 62.5 kHz, or if the struct `v4l2_tuner` or struct `v4l2_modulator` `capability` flag `V4L2_TUNER_CAP_LOW` is set, in units of 62.5 Hz. A 1 Hz unit is used when the `capability` flag `V4L2_TUNER_CAP_1HZ` is set.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`reserved`\[8\]

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

  The `tuner` index is out of bounds or the value in the `type` field is wrong.

- **EBUSY**

  A hardware seek is in progress.
