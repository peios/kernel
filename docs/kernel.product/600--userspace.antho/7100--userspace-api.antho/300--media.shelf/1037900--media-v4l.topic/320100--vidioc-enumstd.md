---
title: "ioctl VIDIOC_ENUMSTD, VIDIOC_SUBDEV_ENUMSTD"
type: reference
description: "VIDIOC_ENUMSTD - VIDIOC_SUBDEV_ENUMSTD - Enumerate supported video standards"
---

<a id="rst-ioctl-vidioc-enumstd-vidioc-subdev-enumstd"></a>
<a id="rst-vidioc-enumstd"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC\_ENUMSTD - VIDIOC\_SUBDEV\_ENUMSTD - Enumerate supported video standards

<a id="rst-synopsis"></a>

## Synopsis

<a id="c-VIDIOC_ENUMSTD"></a>



```c
VIDIOC_ENUMSTD
```

`int ioctl(int fd, VIDIOC_ENUMSTD, struct v4l2_standard *argp)`

<a id="c-VIDIOC_SUBDEV_ENUMSTD"></a>



```c
VIDIOC_SUBDEV_ENUMSTD
```

`int ioctl(int fd, VIDIOC_SUBDEV_ENUMSTD, struct v4l2_standard *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_standard`.

<a id="rst-description"></a>

## Description

To query the attributes of a video standard, especially a custom (driver defined) one, applications initialize the `index` field of struct `v4l2_standard` and call the [ioctl VIDIOC\_ENUMSTD, VIDIOC\_SUBDEV\_ENUMSTD](<#rst-vidioc-enumstd>) ioctl with a pointer to this structure. Drivers fill the rest of the structure or return an `EINVAL` error code when the index is out of bounds. To enumerate all standards applications shall begin at index zero, incrementing by one until the driver returns `EINVAL`. Drivers may enumerate a different set of standards after switching the video input or output. <a id="rst-footnote-reference-1"></a>[1](#rst-f1)

<a id="c-v4l2_standard"></a>



```c
v4l2_standard
```

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->


<table>
<caption>

struct v4l2\_standard

</caption>
<tbody>
<tr>
<td>



\_\_u32

</td>
<td>



`index`

</td>
<td>



Number of the video standard, set by the application.

</td>
</tr>
<tr>
<td>



[v4l2\_std\_id](<#rst-v4l2-std-id>)

</td>
<td>



`id`

</td>
<td>



The bits in this field identify the standard as one of the common standards listed in [v4l2-std-id](<#rst-v4l2-std-id>), or if bits 32 to 63 are set as custom standards. Multiple bits can be set if the hardware does not distinguish between these standards, however separate indices do not indicate the opposite. The `id` must be unique. No other enumerated struct `v4l2_standard` structure, for this input or output anyway, can contain the same set of bits.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`name`\[24\]

</td>
<td>



Name of the standard, a NUL-terminated ASCII string, for example: "PAL-B/G", "NTSC Japan". This information is intended for the user.

</td>
</tr>
<tr>
<td>



struct `v4l2_fract`

</td>
<td>



`frameperiod`

</td>
<td>



The frame period (not field period) is numerator / denominator. For example M/NTSC has a frame period of 1001 / 30000 seconds.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`framelines`

</td>
<td>



Total lines per frame including blanking, e. g. 625 for B/PAL.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`reserved`\[4\]

</td>
<td>



Reserved for future extensions. Drivers must set the array to zero.

</td>
</tr>
</tbody>
</table>

<a id="c-v4l2_fract"></a>



```c
v4l2_fract
```

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->


<table>
<caption>

struct v4l2\_fract

</caption>
<tbody>
<tr>
<td>



\_\_u32

</td>
<td>



`numerator`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`denominator`

</td>
<td>





</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->

<a id="rst-v4l2-std-id"></a>


<table>
<caption>

typedef v4l2\_std\_id

</caption>
<tbody>
<tr>
<td>



\_\_u64

</td>
<td>



`v4l2_std_id`

</td>
<td>



This type is a set, each bit representing another video standard as listed below and in [video-standards](<#rst-video-standards>). The 32 most significant bits are reserved for custom (driver defined) video standards.

</td>
</tr>
</tbody>
</table>



```c
#define V4L2_STD_PAL_B          ((v4l2_std_id)0x00000001)
#define V4L2_STD_PAL_B1         ((v4l2_std_id)0x00000002)
#define V4L2_STD_PAL_G          ((v4l2_std_id)0x00000004)
#define V4L2_STD_PAL_H          ((v4l2_std_id)0x00000008)
#define V4L2_STD_PAL_I          ((v4l2_std_id)0x00000010)
#define V4L2_STD_PAL_D          ((v4l2_std_id)0x00000020)
#define V4L2_STD_PAL_D1         ((v4l2_std_id)0x00000040)
#define V4L2_STD_PAL_K          ((v4l2_std_id)0x00000080)

#define V4L2_STD_PAL_M          ((v4l2_std_id)0x00000100)
#define V4L2_STD_PAL_N          ((v4l2_std_id)0x00000200)
#define V4L2_STD_PAL_Nc         ((v4l2_std_id)0x00000400)
#define V4L2_STD_PAL_60         ((v4l2_std_id)0x00000800)
```

`V4L2_STD_PAL_60` is a hybrid standard with 525 lines, 60 Hz refresh rate, and PAL color modulation with a 4.43 MHz color subcarrier. Some PAL video recorders can play back NTSC tapes in this mode for display on a 50/60 Hz agnostic PAL TV.



```c
#define V4L2_STD_NTSC_M         ((v4l2_std_id)0x00001000)
#define V4L2_STD_NTSC_M_JP      ((v4l2_std_id)0x00002000)
#define V4L2_STD_NTSC_443       ((v4l2_std_id)0x00004000)
```

`V4L2_STD_NTSC_443` is a hybrid standard with 525 lines, 60 Hz refresh rate, and NTSC color modulation with a 4.43 MHz color subcarrier.



```c
#define V4L2_STD_NTSC_M_KR      ((v4l2_std_id)0x00008000)

#define V4L2_STD_SECAM_B        ((v4l2_std_id)0x00010000)
#define V4L2_STD_SECAM_D        ((v4l2_std_id)0x00020000)
#define V4L2_STD_SECAM_G        ((v4l2_std_id)0x00040000)
#define V4L2_STD_SECAM_H        ((v4l2_std_id)0x00080000)
#define V4L2_STD_SECAM_K        ((v4l2_std_id)0x00100000)
#define V4L2_STD_SECAM_K1       ((v4l2_std_id)0x00200000)
#define V4L2_STD_SECAM_L        ((v4l2_std_id)0x00400000)
#define V4L2_STD_SECAM_LC       ((v4l2_std_id)0x00800000)

/* ATSC/HDTV */
#define V4L2_STD_ATSC_8_VSB     ((v4l2_std_id)0x01000000)
#define V4L2_STD_ATSC_16_VSB    ((v4l2_std_id)0x02000000)
```

`V4L2_STD_ATSC_8_VSB` and `V4L2_STD_ATSC_16_VSB` are U.S. terrestrial digital TV standards. Presently the V4L2 API does not support digital TV. See also the Linux DVB API at [https://linuxtv.org](<https://linuxtv.org>).



```c
#define V4L2_STD_PAL_BG         (V4L2_STD_PAL_B         |
                 V4L2_STD_PAL_B1        |
                 V4L2_STD_PAL_G)
#define V4L2_STD_B              (V4L2_STD_PAL_B         |
                 V4L2_STD_PAL_B1        |
                 V4L2_STD_SECAM_B)
#define V4L2_STD_GH             (V4L2_STD_PAL_G         |
                 V4L2_STD_PAL_H         |
                 V4L2_STD_SECAM_G       |
                 V4L2_STD_SECAM_H)
#define V4L2_STD_PAL_DK         (V4L2_STD_PAL_D         |
                 V4L2_STD_PAL_D1        |
                 V4L2_STD_PAL_K)
#define V4L2_STD_PAL            (V4L2_STD_PAL_BG        |
                 V4L2_STD_PAL_DK        |
                 V4L2_STD_PAL_H         |
                 V4L2_STD_PAL_I)
#define V4L2_STD_NTSC           (V4L2_STD_NTSC_M        |
                 V4L2_STD_NTSC_M_JP     |
                 V4L2_STD_NTSC_M_KR)
#define V4L2_STD_MN             (V4L2_STD_PAL_M         |
                 V4L2_STD_PAL_N         |
                 V4L2_STD_PAL_Nc        |
                 V4L2_STD_NTSC)
#define V4L2_STD_SECAM_DK       (V4L2_STD_SECAM_D       |
                 V4L2_STD_SECAM_K       |
                 V4L2_STD_SECAM_K1)
#define V4L2_STD_DK             (V4L2_STD_PAL_DK        |
                 V4L2_STD_SECAM_DK)

#define V4L2_STD_SECAM          (V4L2_STD_SECAM_B       |
                 V4L2_STD_SECAM_G       |
                 V4L2_STD_SECAM_H       |
                 V4L2_STD_SECAM_DK      |
                 V4L2_STD_SECAM_L       |
                 V4L2_STD_SECAM_LC)

#define V4L2_STD_525_60         (V4L2_STD_PAL_M         |
                 V4L2_STD_PAL_60        |
                 V4L2_STD_NTSC          |
                 V4L2_STD_NTSC_443)
#define V4L2_STD_625_50         (V4L2_STD_PAL           |
                 V4L2_STD_PAL_N         |
                 V4L2_STD_PAL_Nc        |
                 V4L2_STD_SECAM)

#define V4L2_STD_UNKNOWN        0
#define V4L2_STD_ALL            (V4L2_STD_525_60        |
                 V4L2_STD_625_50)
```

<!-- Source LaTeX layout: \begingroup
\tiny
\setlength{\tabcolsep}{2pt} -->

<!-- NTSC/M   PAL/M    /N       /B       /D       /H       /I        SECAM/B    /D       /K1     /L -->

<!-- tabularcolumns: |p{1.43cm}|p{1.38cm}|p{1.59cm}|p{1.7cm}|p{1.7cm}|p{1.17cm}|p{0.64cm}|p{1.71cm}|p{1.6cm}|p{1.07cm}|p{1.07cm}|p{1.07cm}| -->

<a id="rst-video-standards"></a>


<table>
<caption>

Video Standards (based on [itu470](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-itu470>))

</caption>
<thead>
<tr>
<th>



Characteristics

</th>
<th>



M/NTSC <a id="rst-footnote-reference-2"></a>[2](#rst-f2)

</th>
<th>



M/PAL

</th>
<th>



N/PAL <a id="rst-footnote-reference-3"></a>[3](#rst-f3)

</th>
<th>



B, B1, G/PAL

</th>
<th>



D, D1, K/PAL

</th>
<th>



H/PAL

</th>
<th>



I/PAL

</th>
<th>



B, G/SECAM

</th>
<th>



D, K/SECAM

</th>
<th>



K1/SECAM

</th>
<th>



L/SECAM

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



Frame lines

</td>
<td colspan="2">



 525

</td>
<td colspan="9">



 625

</td>
</tr>
<tr>
<td>



Frame period (s)

</td>
<td colspan="2">



 1001/30000

</td>
<td colspan="9">



 1/25

</td>
</tr>
<tr>
<td>



Chrominance sub-carrier frequency (Hz)

</td>
<td>



3579545 ± 10

</td>
<td>



3579611.49 ± 10

</td>
<td>



4433618.75 ± 5

(3582056.25 ± 5)

</td>
<td colspan="4">



 4433618.75 ± 5

</td>
<td>



4433618.75 ± 1

</td>
<td colspan="3">



 f<sub>OR</sub> = 4406250 ± 2000,

f<sub>OB</sub> = 4250000 ± 2000

</td>
</tr>
<tr>
<td>



Nominal radio-frequency channel bandwidth (MHz)

</td>
<td>



6

</td>
<td>



6

</td>
<td>



6

</td>
<td>



B: 7; B1, G: 8

</td>
<td>



8

</td>
<td>



8

</td>
<td>



8

</td>
<td>



8

</td>
<td>



8

</td>
<td>



8

</td>
<td>



8

</td>
</tr>
<tr>
<td>



Sound carrier relative to vision carrier (MHz)

</td>
<td>



4.5

</td>
<td>



4.5

</td>
<td>



4.5

</td>
<td>



5.5 ± 0.001  <a id="rst-footnote-reference-4"></a>[4](#rst-f4)  <a id="rst-footnote-reference-5"></a>[5](#rst-f5)  <a id="rst-footnote-reference-6"></a>[6](#rst-f6)  <a id="rst-footnote-reference-7"></a>[7](#rst-f7)

</td>
<td>



6.5 ± 0.001

</td>
<td>



5.5

</td>
<td>



5.9996 ± 0.0005

</td>
<td>



5.5 ± 0.001

</td>
<td>



6.5 ± 0.001

</td>
<td>



6.5

</td>
<td>



6.5 <a id="rst-footnote-reference-8"></a>[8](#rst-f8)

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \endgroup -->

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  The struct `v4l2_standard` `index` is out of bounds.

- **ENODATA**

  Standard video timings are not supported for this input or output.

<a id="rst-f1"></a>



**[1]** The supported standards may overlap and we need an unambiguous set to find the current standard returned by [VIDIOC\_G\_STD](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-std#rst-vidioc-g-std>).

<a id="rst-f2"></a>



**[2]** Japan uses a standard similar to M/NTSC (V4L2\_STD\_NTSC\_M\_JP).

<a id="rst-f3"></a>



**[3]** The values in brackets apply to the combination N/PAL a.k.a. N<sub>C</sub> used in Argentina (V4L2\_STD\_PAL\_Nc).

<a id="rst-f4"></a>



**[4]** In the Federal Republic of Germany, Austria, Italy, the Netherlands, Slovakia and Switzerland a system of two sound carriers is used, the frequency of the second carrier being 242.1875 kHz above the frequency of the first sound carrier. For stereophonic sound transmissions a similar system is used in Australia.

<a id="rst-f5"></a>



**[5]** New Zealand uses a sound carrier displaced 5.4996 ± 0.0005 MHz from the vision carrier.

<a id="rst-f6"></a>



**[6]** In Denmark, Finland, New Zealand, Sweden and Spain a system of two sound carriers is used. In Iceland, Norway and Poland the same system is being introduced. The second carrier is 5.85 MHz above the vision carrier and is DQPSK modulated with 728 kbit/s sound and data multiplex. (NICAM system)

<a id="rst-f7"></a>



**[7]** In the United Kingdom, a system of two sound carriers is used. The second sound carrier is 6.552 MHz above the vision carrier and is DQPSK modulated with a 728 kbit/s sound and data multiplex able to carry two sound channels. (NICAM system)

<a id="rst-f8"></a>



**[8]** In France, a digital carrier 5.85 MHz away from the vision carrier may be used in addition to the main sound carrier. It is modulated in differentially encoded QPSK with a 728 kbit/s sound and data multiplexer capable of carrying two sound channels. (NICAM system)
