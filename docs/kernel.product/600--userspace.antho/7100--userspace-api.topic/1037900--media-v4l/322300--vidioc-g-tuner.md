---
title: "ioctl VIDIOC_G_TUNER, VIDIOC_S_TUNER"
type: reference
description: "VIDIOC_G_TUNER - VIDIOC_S_TUNER - Get or set tuner attributes"
---

<a id="rst-ioctl-vidioc-g-tuner-vidioc-s-tuner"></a>
<a id="rst-vidioc-g-tuner"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC\_G\_TUNER - VIDIOC\_S\_TUNER - Get or set tuner attributes

<a id="rst-synopsis"></a>

## Synopsis

<a id="c-VIDIOC_G_TUNER"></a>



```c
VIDIOC_G_TUNER
```

`int ioctl(int fd, VIDIOC_G_TUNER, struct v4l2_tuner *argp)`

<a id="c-VIDIOC_S_TUNER"></a>



```c
VIDIOC_S_TUNER
```

`int ioctl(int fd, VIDIOC_S_TUNER, const struct v4l2_tuner *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_tuner`.

<a id="rst-description"></a>

## Description

To query the attributes of a tuner applications initialize the `index` field and zero out the `reserved` array of a struct `v4l2_tuner` and call the `VIDIOC_G_TUNER` ioctl with a pointer to this structure. Drivers fill the rest of the structure or return an `EINVAL` error code when the index is out of bounds. To enumerate all tuners applications shall begin at index zero, incrementing by one until the driver returns `EINVAL`.

Tuners have two writable properties, the audio mode and the radio frequency. To change the audio mode, applications initialize the `index`, `audmode` and `reserved` fields and call the `VIDIOC_S_TUNER` ioctl. This will <em>not</em> change the current tuner, which is determined by the current video input. Drivers may choose a different audio mode if the requested mode is invalid or unsupported. Since this is a write-only ioctl, it does not return the actually selected audio mode.

[SDR](<~kernel/userspace/userspace-api/media-v4l/dev-sdr#rst-sdr>) specific tuner types are `V4L2_TUNER_SDR` and `V4L2_TUNER_RF`. For SDR devices `audmode` field must be initialized to zero. The term 'tuner' means SDR receiver in this context.

To change the radio frequency the [VIDIOC\_S\_FREQUENCY](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-frequency#rst-vidioc-g-frequency>) ioctl is available.

> <!-- tabularcolumns: |p{1.3cm}|p{3.0cm}|p{7.0cm}|p{5.8cm}| -->

<a id="c-v4l2_tuner"></a>



```c
v4l2_tuner
```


<table>
<caption>

struct v4l2\_tuner

</caption>
<tbody>
<tr>
<td>



\_\_u32

</td>
<td>



`index`

</td>
<td colspan="2">



 Identifies the tuner, set by the application.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`name`\[32\]

</td>
<td colspan="2">



Name of the tuner, a NUL-terminated ASCII string.

This information is intended for the user.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`type`

</td>
<td colspan="2">



 Type of the tuner, see `v4l2_tuner_type`.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`capability`

</td>
<td colspan="2">



Tuner capability flags, see [tuner-capability](<#rst-tuner-capability>). Audio flags indicate the ability to decode audio subprograms. They will <em>not</em> change, for example with the current video standard.

When the structure refers to a radio tuner the `V4L2_TUNER_CAP_LANG1`, `V4L2_TUNER_CAP_LANG2` and `V4L2_TUNER_CAP_NORM` flags can't be used.

If multiple frequency bands are supported, then `capability` is the union of all `capability` fields of each struct `v4l2_frequency_band`.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`rangelow`

</td>
<td colspan="2">



 The lowest tunable frequency in units of 62.5 kHz, or if the `capability` flag `V4L2_TUNER_CAP_LOW` is set, in units of 62.5 Hz, or if the `capability` flag `V4L2_TUNER_CAP_1HZ` is set, in units of 1 Hz. If multiple frequency bands are supported, then `rangelow` is the lowest frequency of all the frequency bands.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`rangehigh`

</td>
<td colspan="2">



 The highest tunable frequency in units of 62.5 kHz, or if the `capability` flag `V4L2_TUNER_CAP_LOW` is set, in units of 62.5 Hz, or if the `capability` flag `V4L2_TUNER_CAP_1HZ` is set, in units of 1 Hz. If multiple frequency bands are supported, then `rangehigh` is the highest frequency of all the frequency bands.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`rxsubchans`

</td>
<td colspan="2">



Some tuners or audio decoders can determine the received audio subprograms by analyzing audio carriers, pilot tones or other indicators. To pass this information drivers set flags defined in [tuner-rxsubchans](<#rst-tuner-rxsubchans>) in this field. For example:

</td>
</tr>
<tr>
<td>





</td>
<td>





</td>
<td>



`V4L2_TUNER_SUB_MONO`

</td>
<td>



receiving mono audio

</td>
</tr>
<tr>
<td>





</td>
<td>





</td>
<td>



`STEREO | SAP`

</td>
<td>



receiving stereo audio and a secondary audio program

</td>
</tr>
<tr>
<td>





</td>
<td>





</td>
<td>



`MONO | STEREO`

</td>
<td>



receiving mono or stereo audio, the hardware cannot distinguish

</td>
</tr>
<tr>
<td>





</td>
<td>





</td>
<td>



`LANG1 | LANG2`

</td>
<td>



receiving bilingual audio

</td>
</tr>
<tr>
<td>





</td>
<td>





</td>
<td>



`MONO | STEREO | LANG1 | LANG2`

</td>
<td>



receiving mono, stereo or bilingual audio

</td>
</tr>
<tr>
<td>





</td>
<td>





</td>
<td colspan="2">



When the `V4L2_TUNER_CAP_STEREO`, `_LANG1`, `_LANG2` or `_SAP` flag is cleared in the `capability` field, the corresponding `V4L2_TUNER_SUB_` flag must not be set here.

This field is valid only if this is the tuner of the current video input, or when the structure refers to a radio tuner.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`audmode`

</td>
<td colspan="2">



The selected audio mode, see [tuner-audmode](<#rst-tuner-audmode>) for valid values. The audio mode does not affect audio subprogram detection, and like a [control](<~kernel/userspace/userspace-api/media-v4l/control#rst-control>) it does not automatically change unless the requested mode is invalid or unsupported. See [tuner-matrix](<#rst-tuner-matrix>) for possible results when the selected and received audio programs do not match.

Currently this is the only field of struct struct `v4l2_tuner` applications can change.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`signal`

</td>
<td colspan="2">



 The signal strength if known.

Ranging from 0 to 65535. Higher values indicate a better signal.

</td>
</tr>
<tr>
<td>



\_\_s32

</td>
<td>



`afc`

</td>
<td colspan="2">



 Automatic frequency control.

When the `afc` value is negative, the frequency is too low, when positive too high.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`reserved`\[4\]

</td>
<td colspan="2">



 Reserved for future extensions.

Drivers and applications must set the array to zero.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{6.6cm}|p{2.2cm}|p{8.5cm}| -->

<a id="c-v4l2_tuner_type"></a>



```c
v4l2_tuner_type
```


<table>
<caption>

enum v4l2\_tuner\_type

</caption>
<tbody>
<tr>
<td>



`V4L2_TUNER_RADIO`

</td>
<td>



1

</td>
<td>



Tuner supports radio

</td>
</tr>
<tr>
<td>



`V4L2_TUNER_ANALOG_TV`

</td>
<td>



2

</td>
<td>



Tuner supports analog TV

</td>
</tr>
<tr>
<td>



`V4L2_TUNER_SDR`

</td>
<td>



4

</td>
<td>



Tuner controls the A/D and/or D/A block of a Software Digital Radio (SDR)

</td>
</tr>
<tr>
<td>



`V4L2_TUNER_RF`

</td>
<td>



5

</td>
<td>



Tuner controls the RF part of a Software Digital Radio (SDR)

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{7.0cm}|p{2.2cm}|p{8.1cm}| -->

<a id="rst-tuner-capability"></a>


<table>
<caption>

Tuner and Modulator Capability Flags

</caption>
<tbody>
<tr>
<td>



`V4L2_TUNER_CAP_LOW`

</td>
<td>



0x0001

</td>
<td>



When set, tuning frequencies are expressed in units of 62.5 Hz instead of 62.5 kHz.

</td>
</tr>
<tr>
<td>



`V4L2_TUNER_CAP_NORM`

</td>
<td>



0x0002

</td>
<td>



This is a multi-standard tuner; the video standard can or must be switched. (B/G PAL tuners for example are typically not considered multi-standard because the video standard is automatically determined from the frequency band.) The set of supported video standards is available from the struct `v4l2_input` pointing to this tuner, see the description of ioctl [vidioc\_enuminput](<~kernel/userspace/userspace-api/media-v4l/vidioc-enuminput#rst-vidioc-enuminput>) for details. Only `V4L2_TUNER_ANALOG_TV` tuners can have this capability.

</td>
</tr>
<tr>
<td>



`V4L2_TUNER_CAP_HWSEEK_BOUNDED`

</td>
<td>



0x0004

</td>
<td>



If set, then this tuner supports the hardware seek functionality where the seek stops when it reaches the end of the frequency range.

</td>
</tr>
<tr>
<td>



`V4L2_TUNER_CAP_HWSEEK_WRAP`

</td>
<td>



0x0008

</td>
<td>



If set, then this tuner supports the hardware seek functionality where the seek wraps around when it reaches the end of the frequency range.

</td>
</tr>
<tr>
<td>



`V4L2_TUNER_CAP_STEREO`

</td>
<td>



0x0010

</td>
<td>



Stereo audio reception is supported.

</td>
</tr>
<tr>
<td>



`V4L2_TUNER_CAP_LANG1`

</td>
<td>



0x0040

</td>
<td>



Reception of the primary language of a bilingual audio program is supported. Bilingual audio is a feature of two-channel systems, transmitting the primary language monaural on the main audio carrier and a secondary language monaural on a second carrier. Only `V4L2_TUNER_ANALOG_TV` tuners can have this capability.

</td>
</tr>
<tr>
<td>



`V4L2_TUNER_CAP_LANG2`

</td>
<td>



0x0020

</td>
<td>



Reception of the secondary language of a bilingual audio program is supported. Only `V4L2_TUNER_ANALOG_TV` tuners can have this capability.

</td>
</tr>
<tr>
<td>



`V4L2_TUNER_CAP_SAP`

</td>
<td>



0x0020

</td>
<td>



Reception of a secondary audio program is supported. This is a feature of the BTSC system which accompanies the NTSC video standard. Two audio carriers are available for mono or stereo transmissions of a primary language, and an independent third carrier for a monaural secondary language. Only `V4L2_TUNER_ANALOG_TV` tuners can have this capability.

> [!NOTE]
>
> The `V4L2_TUNER_CAP_LANG2` and `V4L2_TUNER_CAP_SAP` flags are synonyms. `V4L2_TUNER_CAP_SAP` applies when the tuner supports the `V4L2_STD_NTSC_M` video standard.

</td>
</tr>
<tr>
<td>



`V4L2_TUNER_CAP_RDS`

</td>
<td>



0x0080

</td>
<td>



RDS capture is supported. This capability is only valid for radio tuners.

</td>
</tr>
<tr>
<td>



`V4L2_TUNER_CAP_RDS_BLOCK_IO`

</td>
<td>



0x0100

</td>
<td>



The RDS data is passed as unparsed RDS blocks.

</td>
</tr>
<tr>
<td>



`V4L2_TUNER_CAP_RDS_CONTROLS`

</td>
<td>



0x0200

</td>
<td>



The RDS data is parsed by the hardware and set via controls.

</td>
</tr>
<tr>
<td>



`V4L2_TUNER_CAP_FREQ_BANDS`

</td>
<td>



0x0400

</td>
<td>



The [vidioc\_enum\_freq\_bands](<~kernel/userspace/userspace-api/media-v4l/vidioc-enum-freq-bands#rst-vidioc-enum-freq-bands>) ioctl can be used to enumerate the available frequency bands.

</td>
</tr>
<tr>
<td>



`V4L2_TUNER_CAP_HWSEEK_PROG_LIM`

</td>
<td>



0x0800

</td>
<td>



The range to search when using the hardware seek functionality is programmable, see [vidioc\_s\_hw\_freq\_seek](<~kernel/userspace/userspace-api/media-v4l/vidioc-s-hw-freq-seek#rst-vidioc-s-hw-freq-seek>) for details.

</td>
</tr>
<tr>
<td>



`V4L2_TUNER_CAP_1HZ`

</td>
<td>



0x1000

</td>
<td>



When set, tuning frequencies are expressed in units of 1 Hz instead of 62.5 kHz.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{6.6cm}|p{2.2cm}|p{8.5cm}| -->

<a id="rst-tuner-rxsubchans"></a>


<table>
<caption>

Tuner Audio Reception Flags

</caption>
<tbody>
<tr>
<td>



`V4L2_TUNER_SUB_MONO`

</td>
<td>



0x0001

</td>
<td>



The tuner receives a mono audio signal.

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



The tuner receives a stereo audio signal.

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



The tuner receives the primary language of a bilingual audio signal. Drivers must clear this flag when the current video standard is `V4L2_STD_NTSC_M`.

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



The tuner receives the secondary language of a bilingual audio signal (or a second audio program).

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



The tuner receives a Second Audio Program.

> [!NOTE]
>
> The `V4L2_TUNER_SUB_LANG2` and `V4L2_TUNER_SUB_SAP` flags are synonyms. The `V4L2_TUNER_SUB_SAP` flag applies when the current video standard is `V4L2_STD_NTSC_M`.

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



The tuner receives an RDS channel.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{6.6cm}|p{2.2cm}|p{8.5cm}| -->

<a id="rst-tuner-audmode"></a>


<table>
<caption>

Tuner Audio Modes

</caption>
<tbody>
<tr>
<td>



`V4L2_TUNER_MODE_MONO`

</td>
<td>



0

</td>
<td>



Play mono audio. When the tuner receives a stereo signal this a down-mix of the left and right channel. When the tuner receives a bilingual or SAP signal this mode selects the primary language.

</td>
</tr>
<tr>
<td>



`V4L2_TUNER_MODE_STEREO`

</td>
<td>



1

</td>
<td>



Play stereo audio. When the tuner receives bilingual audio it may play different languages on the left and right channel or the primary language is played on both channels.

Playing different languages in this mode is deprecated. New drivers should do this only in `MODE_LANG1_LANG2`.

When the tuner receives no stereo signal or does not support stereo reception the driver shall fall back to `MODE_MONO`.

</td>
</tr>
<tr>
<td>



`V4L2_TUNER_MODE_LANG1`

</td>
<td>



3

</td>
<td>



Play the primary language, mono or stereo. Only `V4L2_TUNER_ANALOG_TV` tuners support this mode.

</td>
</tr>
<tr>
<td>



`V4L2_TUNER_MODE_LANG2`

</td>
<td>



2

</td>
<td>



Play the secondary language, mono. When the tuner receives no bilingual audio or SAP, or their reception is not supported the driver shall fall back to mono or stereo mode. Only `V4L2_TUNER_ANALOG_TV` tuners support this mode.

</td>
</tr>
<tr>
<td>



`V4L2_TUNER_MODE_SAP`

</td>
<td>



2

</td>
<td>



Play the Second Audio Program. When the tuner receives no bilingual audio or SAP, or their reception is not supported the driver shall fall back to mono or stereo mode. Only `V4L2_TUNER_ANALOG_TV` tuners support this mode.

> [!NOTE]
>
> The `V4L2_TUNER_MODE_LANG2` and `V4L2_TUNER_MODE_SAP` are synonyms.

</td>
</tr>
<tr>
<td>



`V4L2_TUNER_MODE_LANG1_LANG2`

</td>
<td>



4

</td>
<td>



Play the primary language on the left channel, the secondary language on the right channel. When the tuner receives no bilingual audio or SAP, it shall fall back to `MODE_LANG1` or `MODE_MONO`. Only `V4L2_TUNER_ANALOG_TV` tuners support this mode.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \scriptsize -->

<!-- tabularcolumns: |p{1.5cm}|p{1.5cm}|p{2.9cm}|p{2.9cm}|p{2.9cm}|p{2.9cm}| -->

<a id="rst-tuner-matrix"></a>


<table>
<caption>

Tuner Audio Matrix

</caption>
<thead>
<tr>
<th>





</th>
<th colspan="5">



 Selected `V4L2_TUNER_MODE_`

</th>
</tr>
<tr>
<th>



Received `V4L2_TUNER_SUB_`

</th>
<th>



`MONO`

</th>
<th>



`STEREO`

</th>
<th>



`LANG1`

</th>
<th>



`LANG2 = SAP`

</th>
<th>



`LANG1_LANG2`<a id="rst-footnote-reference-1"></a>[1](#rst-f1)

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



`MONO`

</td>
<td>



Mono

</td>
<td>



Mono/Mono

</td>
<td>



Mono

</td>
<td>



Mono

</td>
<td>



Mono/Mono

</td>
</tr>
<tr>
<td>



`MONO | SAP`

</td>
<td>



Mono

</td>
<td>



Mono/Mono

</td>
<td>



Mono

</td>
<td>



SAP

</td>
<td>



Mono/SAP (preferred) or Mono/Mono

</td>
</tr>
<tr>
<td>



`STEREO`

</td>
<td>



L+R

</td>
<td>



L/R

</td>
<td>



Stereo L/R (preferred) or Mono L+R

</td>
<td>



Stereo L/R (preferred) or Mono L+R

</td>
<td>



L/R (preferred) or L+R/L+R

</td>
</tr>
<tr>
<td>



`STEREO | SAP`

</td>
<td>



L+R

</td>
<td>



L/R

</td>
<td>



Stereo L/R (preferred) or Mono L+R

</td>
<td>



SAP

</td>
<td>



L+R/SAP (preferred) or L/R or L+R/L+R

</td>
</tr>
<tr>
<td>



`LANG1 | LANG2`

</td>
<td>



Language 1

</td>
<td>



Lang1/Lang2 (deprecated<a id="rst-footnote-reference-2"></a>[2](#rst-f2)) or Lang1/Lang1

</td>
<td>



Language 1

</td>
<td>



Language 2

</td>
<td>



Lang1/Lang2 (preferred) or Lang1/Lang1

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  The struct `v4l2_tuner` `index` is out of bounds.

<a id="rst-f1"></a>



**[1]** This mode has been added in Linux 2.6.17 and may not be supported by older drivers.

<a id="rst-f2"></a>



**[2]** Playback of both languages in `MODE_STEREO` is deprecated. In the future drivers should produce only the primary language in this mode. Applications should request `MODE_LANG1_LANG2` to record both languages or a stereo signal.
