---
title: "ioctl VIDIOC_ENUM_FREQ_BANDS"
type: reference
description: "VIDIOC_ENUM_FREQ_BANDS - Enumerate supported frequency bands"
---

<a id="rst-ioctl-vidioc-enum-freq-bands"></a>
<a id="rst-vidioc-enum-freq-bands"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_ENUM_FREQ_BANDS - Enumerate supported frequency bands

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_ENUM_FREQ_BANDS"></a>

```c
VIDIOC_ENUM_FREQ_BANDS
```

`int ioctl(int fd, VIDIOC_ENUM_FREQ_BANDS, struct v4l2_frequency_band *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_frequency_band`.

<a id="rst-description"></a>

## Description

Enumerates the frequency bands that a tuner or modulator supports. To do this applications initialize the `tuner`, `type` and `index` fields, and zero out the `reserved` array of a struct `v4l2_frequency_band` and call the [ioctl VIDIOC_ENUM_FREQ_BANDS](<#rst-vidioc-enum-freq-bands>) ioctl with a pointer to this structure.

This ioctl is supported if the `V4L2_TUNER_CAP_FREQ_BANDS` capability of the corresponding tuner/modulator is set.

<!-- tabularcolumns: |p{2.9cm}|p{2.9cm}|p{5.8cm}|p{2.9cm}|p{2.4cm}| -->





<a id="c-v4l2_frequency_band"></a>

```c
v4l2_frequency_band
```


<table>
<caption>struct v4l2_frequency_band</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`tuner`

</td>
<td colspan="3">


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
<td colspan="3">


The tuner type. This is the same value as in the struct `v4l2_tuner` `type` field. The type must be set to `V4L2_TUNER_RADIO` for `/dev/radioX` device nodes, and to `V4L2_TUNER_ANALOG_TV` for all others. Set this field to `V4L2_TUNER_RADIO` for modulators (currently only radio modulators are supported). See `v4l2_tuner_type`

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`index`

</td>
<td colspan="3">


Identifies the frequency band, set by the application.

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


 The tuner/modulator capability flags for this frequency band, see [tuner-capability](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-g-tuner.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>). The `V4L2_TUNER_CAP_LOW` or `V4L2_TUNER_CAP_1HZ` capability must be the same for all frequency bands of the selected tuner/modulator. So either all bands have that capability set, or none of them have that capability.

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


 The lowest tunable frequency in units of 62.5 kHz, or if the `capability` flag `V4L2_TUNER_CAP_LOW` is set, in units of 62.5 Hz, for this frequency band. A 1 Hz unit is used when the `capability` flag `V4L2_TUNER_CAP_1HZ` is set.

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


 The highest tunable frequency in units of 62.5 kHz, or if the `capability` flag `V4L2_TUNER_CAP_LOW` is set, in units of 62.5 Hz, for this frequency band. A 1 Hz unit is used when the `capability` flag `V4L2_TUNER_CAP_1HZ` is set.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`modulation`

</td>
<td colspan="3">


 The supported modulation systems of this frequency band. See [band-modulation](<#rst-band-modulation>).

> [!NOTE]
>
> Currently only one modulation system per frequency band is supported. More work will need to be done if multiple modulation systems are possible. Contact the linux-media mailing list ([https://linuxtv.org/lists.php](<https://linuxtv.org/lists.php>)) if you need such functionality.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`reserved`\[9\]

</td>
<td colspan="3">


Reserved for future extensions.

Applications and drivers must set the array to zero.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{6.6cm}|p{2.2cm}|p{8.5cm}| -->

<a id="rst-band-modulation"></a>


<table>
<caption>Band Modulation Systems</caption>
<tbody>
<tr>
<td>


`V4L2_BAND_MODULATION_VSB`

</td>
<td>


0x02

</td>
<td>


Vestigial Sideband modulation, used for analog TV.

</td>
</tr>
<tr>
<td>


`V4L2_BAND_MODULATION_FM`

</td>
<td>


0x04

</td>
<td>


Frequency Modulation, commonly used for analog radio.

</td>
</tr>
<tr>
<td>


`V4L2_BAND_MODULATION_AM`

</td>
<td>


0x08

</td>
<td>


Amplitude Modulation, commonly used for analog radio.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  The `tuner` or `index` is out of bounds or the `type` field is wrong.
