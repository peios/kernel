---
title: "Detailed Colorspace Descriptions"
type: reference
description: "The smpte170m standard defines the colorspace used by NTSC and PAL and by SDTV in general. The default transfer function is V4L2_XFER_FUNC_709. The default Y'CbCr encoding is V4L2_YCBCR_ENC_601. The default Y'CbCr quantization is limited…"
---

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-detailed-colorspace-descriptions"></a>

## Detailed Colorspace Descriptions

<a id="rst-colorspace-smpte-170m-v4l2-colorspace-smpte170m"></a>
<a id="rst-col-smpte-170m"></a>

### Colorspace SMPTE 170M (V4L2\_COLORSPACE\_SMPTE170M)

The [smpte170m](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-smpte170m>) standard defines the colorspace used by NTSC and PAL and by SDTV in general. The default transfer function is `V4L2_XFER_FUNC_709`. The default Y'CbCr encoding is `V4L2_YCBCR_ENC_601`. The default Y'CbCr quantization is limited range. The chromaticities of the primary colors and the white reference are:


<table>
<caption>

SMPTE 170M Chromaticities

</caption>
<thead>
<tr>
<th>



Color

</th>
<th>



x

</th>
<th>



y

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



Red

</td>
<td>



0.630

</td>
<td>



0.340

</td>
</tr>
<tr>
<td>



Green

</td>
<td>



0.310

</td>
<td>



0.595

</td>
</tr>
<tr>
<td>



Blue

</td>
<td>



0.155

</td>
<td>



0.070

</td>
</tr>
<tr>
<td>



White Reference (D65)

</td>
<td>



0.3127

</td>
<td>



0.3290

</td>
</tr>
</tbody>
</table>

The red, green and blue chromaticities are also often referred to as the SMPTE C set, so this colorspace is sometimes called SMPTE C as well.

The transfer function defined for SMPTE 170M is the same as the one defined in Rec. 709.

```math
L' = -1.099(-L)^{0.45} + 0.099 \text{, for } L \le-0.018
```

```math
L' = 4.5L \text{, for } -0.018 < L < 0.018
```

```math
L' = 1.099L^{0.45} - 0.099 \text{, for } L \ge 0.018
```

Inverse Transfer function:

```math
L = -\left( \frac{L' - 0.099}{-1.099} \right) ^{\frac{1}{0.45}} \text{, for } L' \le -0.081
```

```math
L = \frac{L'}{4.5} \text{, for } -0.081 < L' < 0.081
```

```math
L = \left(\frac{L' + 0.099}{1.099}\right)^{\frac{1}{0.45} } \text{, for } L' \ge 0.081
```

The luminance (Y') and color difference (Cb and Cr) are obtained with the following `V4L2_YCBCR_ENC_601` encoding:

```math
Y' = 0.2990R' + 0.5870G' + 0.1140B'
```

```math
Cb = -0.1687R' - 0.3313G' + 0.5B'
```

```math
Cr = 0.5R' - 0.4187G' - 0.0813B'
```

Y' is clamped to the range \[0…1\] and Cb and Cr are clamped to the range \[-0.5…0.5\]. This conversion to Y'CbCr is identical to the one defined in the [itu601](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-itu601>) standard and this colorspace is sometimes called BT.601 as well, even though BT.601 does not mention any color primaries.

The default quantization is limited range, but full range is possible although rarely seen.

<a id="rst-colorspace-rec-709-v4l2-colorspace-rec709"></a>
<a id="rst-col-rec709"></a>

### Colorspace Rec. 709 (V4L2\_COLORSPACE\_REC709)

The [itu709](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-itu709>) standard defines the colorspace used by HDTV in general. The default transfer function is `V4L2_XFER_FUNC_709`. The default Y'CbCr encoding is `V4L2_YCBCR_ENC_709`. The default Y'CbCr quantization is limited range. The chromaticities of the primary colors and the white reference are:


<table>
<caption>

Rec. 709 Chromaticities

</caption>
<thead>
<tr>
<th>



Color

</th>
<th>



x

</th>
<th>



y

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



Red

</td>
<td>



0.640

</td>
<td>



0.330

</td>
</tr>
<tr>
<td>



Green

</td>
<td>



0.300

</td>
<td>



0.600

</td>
</tr>
<tr>
<td>



Blue

</td>
<td>



0.150

</td>
<td>



0.060

</td>
</tr>
<tr>
<td>



White Reference (D65)

</td>
<td>



0.3127

</td>
<td>



0.3290

</td>
</tr>
</tbody>
</table>

The full name of this standard is Rec. ITU-R BT.709-5.

Transfer function. Normally L is in the range \[0…1\], but for the extended gamut xvYCC encoding values outside that range are allowed.

```math
L' = -1.099(-L)^{0.45} + 0.099 \text{, for } L \le -0.018
```

```math
L' = 4.5L \text{, for } -0.018 < L < 0.018
```

```math
L' = 1.099L^{0.45} - 0.099 \text{, for } L \ge 0.018
```

Inverse Transfer function:

```math
L = -\left( \frac{L' - 0.099}{-1.099} \right)^\frac{1}{0.45} \text{, for } L' \le -0.081
```

```math
L = \frac{L'}{4.5}\text{, for } -0.081 < L' < 0.081
```

```math
L = \left(\frac{L' + 0.099}{1.099}\right)^{\frac{1}{0.45} } \text{, for } L' \ge 0.081
```

The luminance (Y') and color difference (Cb and Cr) are obtained with the following `V4L2_YCBCR_ENC_709` encoding:

```math
Y' = 0.2126R' + 0.7152G' + 0.0722B'
```

```math
Cb = -0.1146R' - 0.3854G' + 0.5B'
```

```math
Cr = 0.5R' - 0.4542G' - 0.0458B'
```

Y' is clamped to the range \[0…1\] and Cb and Cr are clamped to the range \[-0.5…0.5\].

The default quantization is limited range, but full range is possible although rarely seen.

The `V4L2_YCBCR_ENC_709` encoding described above is the default for this colorspace, but it can be overridden with `V4L2_YCBCR_ENC_601`, in which case the BT.601 Y'CbCr encoding is used.

Two additional extended gamut Y'CbCr encodings are also possible with this colorspace:

The xvYCC 709 encoding (`V4L2_YCBCR_ENC_XV709`, [xvycc](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-xvycc-1>)) is similar to the Rec. 709 encoding, but it allows for R', G' and B' values that are outside the range \[0…1\]. The resulting Y', Cb and Cr values are scaled and offset according to the limited range formula:

```math
Y' = \frac{219}{256} * (0.2126R' + 0.7152G' + 0.0722B') + \frac{16}{256}
```

```math
Cb = \frac{224}{256} * (-0.1146R' - 0.3854G' + 0.5B')
```

```math
Cr = \frac{224}{256} * (0.5R' - 0.4542G' - 0.0458B')
```

The xvYCC 601 encoding (`V4L2_YCBCR_ENC_XV601`, [xvycc](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-xvycc-1>)) is similar to the BT.601 encoding, but it allows for R', G' and B' values that are outside the range \[0…1\]. The resulting Y', Cb and Cr values are scaled and offset according to the limited range formula:

```math
Y' = \frac{219}{256} * (0.2990R' + 0.5870G' + 0.1140B') + \frac{16}{256}
```

```math
Cb = \frac{224}{256} * (-0.1687R' - 0.3313G' + 0.5B')
```

```math
Cr = \frac{224}{256} * (0.5R' - 0.4187G' - 0.0813B')
```

Y' is clamped to the range \[0…1\] and Cb and Cr are clamped to the range \[-0.5…0.5\] and quantized without further scaling or offsets. The non-standard xvYCC 709 or xvYCC 601 encodings can be used by selecting `V4L2_YCBCR_ENC_XV709` or `V4L2_YCBCR_ENC_XV601`. As seen by the xvYCC formulas these encodings always use limited range quantization, there is no full range variant. The whole point of these extended gamut encodings is that values outside the limited range are still valid, although they map to R', G' and B' values outside the \[0…1\] range and are therefore outside the Rec. 709 colorspace gamut.

<a id="rst-colorspace-srgb-v4l2-colorspace-srgb"></a>
<a id="rst-col-srgb"></a>

### Colorspace sRGB (V4L2\_COLORSPACE\_SRGB)

The [srgb](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-srgb-1>) standard defines the colorspace used by most webcams and computer graphics. The default transfer function is `V4L2_XFER_FUNC_SRGB`. The default Y'CbCr encoding is `V4L2_YCBCR_ENC_601`. The default Y'CbCr quantization is limited range.

Note that the [sycc](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-sycc-1>) standard specifies full range quantization, however all current capture hardware supported by the kernel convert R'G'B' to limited range Y'CbCr. So choosing full range as the default would break how applications interpret the quantization range.

The chromaticities of the primary colors and the white reference are:


<table>
<caption>

sRGB Chromaticities

</caption>
<thead>
<tr>
<th>



Color

</th>
<th>



x

</th>
<th>



y

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



Red

</td>
<td>



0.640

</td>
<td>



0.330

</td>
</tr>
<tr>
<td>



Green

</td>
<td>



0.300

</td>
<td>



0.600

</td>
</tr>
<tr>
<td>



Blue

</td>
<td>



0.150

</td>
<td>



0.060

</td>
</tr>
<tr>
<td>



White Reference (D65)

</td>
<td>



0.3127

</td>
<td>



0.3290

</td>
</tr>
</tbody>
</table>

These chromaticities are identical to the Rec. 709 colorspace.

Transfer function. Note that negative values for L are only used by the Y'CbCr conversion.

```math
L' = -1.055(-L)^{\frac{1}{2.4} } + 0.055\text{, for }L < -0.0031308
```

```math
L' = 12.92L\text{, for }-0.0031308 \le L \le 0.0031308
```

```math
L' = 1.055L ^{\frac{1}{2.4} } - 0.055\text{, for }0.0031308 < L \le 1
```

Inverse Transfer function:

```math
L = -((-L' + 0.055) / 1.055) ^{2.4}\text{, for }L' < -0.04045
```

```math
L = L' / 12.92\text{, for }-0.04045 \le L' \le 0.04045
```

```math
L = ((L' + 0.055) / 1.055) ^{2.4}\text{, for }L' > 0.04045
```

The luminance (Y') and color difference (Cb and Cr) are obtained with the following `V4L2_YCBCR_ENC_601` encoding as defined by [sycc](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-sycc-1>):

```math
Y' = 0.2990R' + 0.5870G' + 0.1140B'
```

```math
Cb = -0.1687R' - 0.3313G' + 0.5B'
```

```math
Cr = 0.5R' - 0.4187G' - 0.0813B'
```

Y' is clamped to the range \[0…1\] and Cb and Cr are clamped to the range \[-0.5…0.5\]. This transform is identical to one defined in SMPTE 170M/BT.601. The Y'CbCr quantization is limited range.

<a id="rst-colorspace-oprgb-v4l2-colorspace-oprgb"></a>
<a id="rst-col-oprgb"></a>

### Colorspace opRGB (V4L2\_COLORSPACE\_OPRGB)

The [oprgb](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-oprgb-1>) standard defines the colorspace used by computer graphics that use the opRGB colorspace. The default transfer function is `V4L2_XFER_FUNC_OPRGB`. The default Y'CbCr encoding is `V4L2_YCBCR_ENC_601`. The default Y'CbCr quantization is limited range.

Note that the [oprgb](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-oprgb-1>) standard specifies full range quantization, however all current capture hardware supported by the kernel convert R'G'B' to limited range Y'CbCr. So choosing full range as the default would break how applications interpret the quantization range.

The chromaticities of the primary colors and the white reference are:


<table>
<caption>

opRGB Chromaticities

</caption>
<thead>
<tr>
<th>



Color

</th>
<th>



x

</th>
<th>



y

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



Red

</td>
<td>



0.6400

</td>
<td>



0.3300

</td>
</tr>
<tr>
<td>



Green

</td>
<td>



0.2100

</td>
<td>



0.7100

</td>
</tr>
<tr>
<td>



Blue

</td>
<td>



0.1500

</td>
<td>



0.0600

</td>
</tr>
<tr>
<td>



White Reference (D65)

</td>
<td>



0.3127

</td>
<td>



0.3290

</td>
</tr>
</tbody>
</table>

Transfer function:

```math
L' = L ^{\frac{1}{2.19921875}}
```

Inverse Transfer function:

```math
L = L'^{(2.19921875)}
```

The luminance (Y') and color difference (Cb and Cr) are obtained with the following `V4L2_YCBCR_ENC_601` encoding:

```math
Y' = 0.2990R' + 0.5870G' + 0.1140B'
```

```math
Cb = -0.1687R' - 0.3313G' + 0.5B'
```

```math
Cr = 0.5R' - 0.4187G' - 0.0813B'
```

Y' is clamped to the range \[0…1\] and Cb and Cr are clamped to the range \[-0.5…0.5\]. This transform is identical to one defined in SMPTE 170M/BT.601. The Y'CbCr quantization is limited range.

<a id="rst-colorspace-bt-2020-v4l2-colorspace-bt2020"></a>
<a id="rst-col-bt2020"></a>

### Colorspace BT.2020 (V4L2\_COLORSPACE\_BT2020)

The [itu2020](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-itu2020>) standard defines the colorspace used by Ultra-high definition television (UHDTV). The default transfer function is `V4L2_XFER_FUNC_709`. The default Y'CbCr encoding is `V4L2_YCBCR_ENC_BT2020`. The default Y'CbCr quantization is limited range. The chromaticities of the primary colors and the white reference are:


<table>
<caption>

BT.2020 Chromaticities

</caption>
<thead>
<tr>
<th>



Color

</th>
<th>



x

</th>
<th>



y

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



Red

</td>
<td>



0.708

</td>
<td>



0.292

</td>
</tr>
<tr>
<td>



Green

</td>
<td>



0.170

</td>
<td>



0.797

</td>
</tr>
<tr>
<td>



Blue

</td>
<td>



0.131

</td>
<td>



0.046

</td>
</tr>
<tr>
<td>



White Reference (D65)

</td>
<td>



0.3127

</td>
<td>



0.3290

</td>
</tr>
</tbody>
</table>

Transfer function (same as Rec. 709):

```math
L' = 4.5L\text{, for }0 \le L < 0.018
```

```math
L' = 1.099L ^{0.45} - 0.099\text{, for } 0.018 \le L \le 1
```

Inverse Transfer function:

```math
L = L' / 4.5\text{, for } L' < 0.081
```

```math
L = \left( \frac{L' + 0.099}{1.099}\right) ^{\frac{1}{0.45} }\text{, for } L' \ge 0.081
```

Please note that while Rec. 709 is defined as the default transfer function by the [itu2020](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-itu2020>) standard, in practice this colorspace is often used with the [Transfer Function SMPTE 2084 (V4L2\_XFER\_FUNC\_SMPTE2084)](<#rst-xf-smpte-2084>). In particular Ultra HD Blu-ray discs use this combination.

The luminance (Y') and color difference (Cb and Cr) are obtained with the following `V4L2_YCBCR_ENC_BT2020` encoding:

```math
Y' = 0.2627R' + 0.6780G' + 0.0593B'
```

```math
Cb = -0.1396R' - 0.3604G' + 0.5B'
```

```math
Cr = 0.5R' - 0.4598G' - 0.0402B'
```

Y' is clamped to the range \[0…1\] and Cb and Cr are clamped to the range \[-0.5…0.5\]. The Y'CbCr quantization is limited range.

There is also an alternate constant luminance R'G'B' to Yc'CbcCrc (`V4L2_YCBCR_ENC_BT2020_CONST_LUM`) encoding:

Luma:

```math
\begin{align*}
Yc' = (0.2627R + 0.6780G + 0.0593B)'& \\
B' - Yc' \le 0:& \\
    &Cbc = (B' - Yc') / 1.9404 \\
B' - Yc' > 0: & \\
    &Cbc = (B' - Yc') / 1.5816 \\
R' - Yc' \le 0:& \\
    &Crc = (R' - Y') / 1.7184 \\
R' - Yc' > 0:& \\
    &Crc = (R' - Y') / 0.9936
\end{align*}
```

Yc' is clamped to the range \[0…1\] and Cbc and Crc are clamped to the range \[-0.5…0.5\]. The Yc'CbcCrc quantization is limited range.

<a id="rst-colorspace-dci-p3-v4l2-colorspace-dci-p3"></a>
<a id="rst-col-dcip3"></a>

### Colorspace DCI-P3 (V4L2\_COLORSPACE\_DCI\_P3)

The [smpte431](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-smpte431>) standard defines the colorspace used by cinema projectors that use the DCI-P3 colorspace. The default transfer function is `V4L2_XFER_FUNC_DCI_P3`. The default Y'CbCr encoding is `V4L2_YCBCR_ENC_709`. The default Y'CbCr quantization is limited range.

> [!NOTE]
>
> Note that this colorspace standard does not specify a Y'CbCr encoding since it is not meant to be encoded to Y'CbCr. So this default Y'CbCr encoding was picked because it is the HDTV encoding.

The chromaticities of the primary colors and the white reference are:


<table>
<caption>

DCI-P3 Chromaticities

</caption>
<thead>
<tr>
<th>



Color

</th>
<th>



x

</th>
<th>



y

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



Red

</td>
<td>



0.6800

</td>
<td>



0.3200

</td>
</tr>
<tr>
<td>



Green

</td>
<td>



0.2650

</td>
<td>



0.6900

</td>
</tr>
<tr>
<td>



Blue

</td>
<td>



0.1500

</td>
<td>



0.0600

</td>
</tr>
<tr>
<td>



White Reference

</td>
<td>



0.3140

</td>
<td>



0.3510

</td>
</tr>
</tbody>
</table>

Transfer function:

```math
L' = L^{\frac{1}{2.6}}
```

Inverse Transfer function:

```math
L = L'^{(2.6)}
```

Y'CbCr encoding is not specified. V4L2 defaults to Rec. 709.

<a id="rst-colorspace-smpte-240m-v4l2-colorspace-smpte240m"></a>
<a id="rst-col-smpte-240m"></a>

### Colorspace SMPTE 240M (V4L2\_COLORSPACE\_SMPTE240M)

The [smpte240m](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-smpte240m>) standard was an interim standard used during the early days of HDTV (1988-1998). It has been superseded by Rec. 709. The default transfer function is `V4L2_XFER_FUNC_SMPTE240M`. The default Y'CbCr encoding is `V4L2_YCBCR_ENC_SMPTE240M`. The default Y'CbCr quantization is limited range. The chromaticities of the primary colors and the white reference are:


<table>
<caption>

SMPTE 240M Chromaticities

</caption>
<thead>
<tr>
<th>



Color

</th>
<th>



x

</th>
<th>



y

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



Red

</td>
<td>



0.630

</td>
<td>



0.340

</td>
</tr>
<tr>
<td>



Green

</td>
<td>



0.310

</td>
<td>



0.595

</td>
</tr>
<tr>
<td>



Blue

</td>
<td>



0.155

</td>
<td>



0.070

</td>
</tr>
<tr>
<td>



White Reference (D65)

</td>
<td>



0.3127

</td>
<td>



0.3290

</td>
</tr>
</tbody>
</table>

These chromaticities are identical to the SMPTE 170M colorspace.

Transfer function:

```math
L' = 4L\text{, for } 0 \le L < 0.0228
```

```math
L' = 1.1115L ^{0.45} - 0.1115\text{, for } 0.0228 \le L \le 1
```

Inverse Transfer function:

```math
L = \frac{L'}{4}\text{, for } 0 \le L' < 0.0913
```

```math
L = \left( \frac{L' + 0.1115}{1.1115}\right) ^{\frac{1}{0.45} }\text{, for } L' \ge 0.0913
```

The luminance (Y') and color difference (Cb and Cr) are obtained with the following `V4L2_YCBCR_ENC_SMPTE240M` encoding:

```math
Y' = 0.2122R' + 0.7013G' + 0.0865B'
```

```math
Cb = -0.1161R' - 0.3839G' + 0.5B'
```

```math
Cr = 0.5R' - 0.4451G' - 0.0549B'
```

Y' is clamped to the range \[0…1\] and Cb and Cr are clamped to the range \[-0.5…0.5\]. The Y'CbCr quantization is limited range.

<a id="rst-colorspace-ntsc-1953-v4l2-colorspace-470-system-m"></a>
<a id="rst-col-sysm"></a>

### Colorspace NTSC 1953 (V4L2\_COLORSPACE\_470\_SYSTEM\_M)

This standard defines the colorspace used by NTSC in 1953. In practice this colorspace is obsolete and SMPTE 170M should be used instead. The default transfer function is `V4L2_XFER_FUNC_709`. The default Y'CbCr encoding is `V4L2_YCBCR_ENC_601`. The default Y'CbCr quantization is limited range. The chromaticities of the primary colors and the white reference are:


<table>
<caption>

NTSC 1953 Chromaticities

</caption>
<thead>
<tr>
<th>



Color

</th>
<th>



x

</th>
<th>



y

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



Red

</td>
<td>



0.67

</td>
<td>



0.33

</td>
</tr>
<tr>
<td>



Green

</td>
<td>



0.21

</td>
<td>



0.71

</td>
</tr>
<tr>
<td>



Blue

</td>
<td>



0.14

</td>
<td>



0.08

</td>
</tr>
<tr>
<td>



White Reference (C)

</td>
<td>



0.310

</td>
<td>



0.316

</td>
</tr>
</tbody>
</table>

> [!NOTE]
>
> This colorspace uses Illuminant C instead of D65 as the white reference. To correctly convert an image in this colorspace to another that uses D65 you need to apply a chromatic adaptation algorithm such as the Bradford method.

The transfer function was never properly defined for NTSC 1953. The Rec. 709 transfer function is recommended in the literature:

```math
L' = 4.5L\text{, for } 0 \le L < 0.018
```

```math
L' = 1.099L ^{0.45} - 0.099\text{, for } 0.018 \le L \le 1
```

Inverse Transfer function:

```math
L = \frac{L'}{4.5} \text{, for } L' < 0.081
```

```math
L = \left( \frac{L' + 0.099}{1.099}\right) ^{\frac{1}{0.45} }\text{, for } L' \ge 0.081
```

The luminance (Y') and color difference (Cb and Cr) are obtained with the following `V4L2_YCBCR_ENC_601` encoding:

```math
Y' = 0.2990R' + 0.5870G' + 0.1140B'
```

```math
Cb = -0.1687R' - 0.3313G' + 0.5B'
```

```math
Cr = 0.5R' - 0.4187G' - 0.0813B'
```

Y' is clamped to the range \[0…1\] and Cb and Cr are clamped to the range \[-0.5…0.5\]. The Y'CbCr quantization is limited range. This transform is identical to one defined in SMPTE 170M/BT.601.

<a id="rst-colorspace-ebu-tech-3213-v4l2-colorspace-470-system-bg"></a>
<a id="rst-col-sysbg"></a>

### Colorspace EBU Tech. 3213 (V4L2\_COLORSPACE\_470\_SYSTEM\_BG)

The [tech3213](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-tech3213>) standard defines the colorspace used by PAL/SECAM in 1975. Note that this colorspace is not supported by the HDMI interface. Instead [tech3321](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-tech3321>) recommends that Rec. 709 is used instead for HDMI. The default transfer function is `V4L2_XFER_FUNC_709`. The default Y'CbCr encoding is `V4L2_YCBCR_ENC_601`. The default Y'CbCr quantization is limited range. The chromaticities of the primary colors and the white reference are:


<table>
<caption>

EBU Tech. 3213 Chromaticities

</caption>
<thead>
<tr>
<th>



Color

</th>
<th>



x

</th>
<th>



y

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



Red

</td>
<td>



0.64

</td>
<td>



0.33

</td>
</tr>
<tr>
<td>



Green

</td>
<td>



0.29

</td>
<td>



0.60

</td>
</tr>
<tr>
<td>



Blue

</td>
<td>



0.15

</td>
<td>



0.06

</td>
</tr>
<tr>
<td>



White Reference (D65)

</td>
<td>



0.3127

</td>
<td>



0.3290

</td>
</tr>
</tbody>
</table>

The transfer function was never properly defined for this colorspace. The Rec. 709 transfer function is recommended in the literature:

```math
L' = 4.5L\text{, for } 0 \le L < 0.018
```

```math
L' = 1.099L ^{0.45} - 0.099\text{, for } 0.018 \le L \le 1
```

Inverse Transfer function:

```math
L = \frac{L'}{4.5} \text{, for } L' < 0.081
```

```math
L = \left(\frac{L' + 0.099}{1.099} \right) ^{\frac{1}{0.45} }\text{, for } L' \ge 0.081
```

The luminance (Y') and color difference (Cb and Cr) are obtained with the following `V4L2_YCBCR_ENC_601` encoding:

```math
Y' = 0.2990R' + 0.5870G' + 0.1140B'
```

```math
Cb = -0.1687R' - 0.3313G' + 0.5B'
```

```math
Cr = 0.5R' - 0.4187G' - 0.0813B'
```

Y' is clamped to the range \[0…1\] and Cb and Cr are clamped to the range \[-0.5…0.5\]. The Y'CbCr quantization is limited range. This transform is identical to one defined in SMPTE 170M/BT.601.

<a id="rst-colorspace-jpeg-v4l2-colorspace-jpeg"></a>
<a id="rst-col-jpeg"></a>

### Colorspace JPEG (V4L2\_COLORSPACE\_JPEG)

This colorspace defines the colorspace used by most (Motion-)JPEG formats. The chromaticities of the primary colors and the white reference are identical to sRGB. The transfer function use is `V4L2_XFER_FUNC_SRGB`. The Y'CbCr encoding is `V4L2_YCBCR_ENC_601` with full range quantization where Y' is scaled to \[0…255\] and Cb/Cr are scaled to \[-128…128\] and then clipped to \[-128…127\].

> [!NOTE]
>
> The JPEG standard does not actually store colorspace information. So if something other than sRGB is used, then the driver will have to set that information explicitly. Effectively `V4L2_COLORSPACE_JPEG` can be considered to be an abbreviation for `V4L2_COLORSPACE_SRGB`, `V4L2_XFER_FUNC_SRGB`, `V4L2_YCBCR_ENC_601` and `V4L2_QUANTIZATION_FULL_RANGE`.

<a id="rst-detailed-transfer-function-descriptions"></a>

## Detailed Transfer Function Descriptions

<a id="rst-transfer-function-smpte-2084-v4l2-xfer-func-smpte2084"></a>
<a id="rst-xf-smpte-2084"></a>

### Transfer Function SMPTE 2084 (V4L2\_XFER\_FUNC\_SMPTE2084)

The [smpte2084](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-smpte2084>) standard defines the transfer function used by High Dynamic Range content.

- **Constants:**

  m1 = (2610 / 4096) / 4

  m2 = (2523 / 4096) \* 128

  c1 = 3424 / 4096

  c2 = (2413 / 4096) \* 32

  c3 = (2392 / 4096) \* 32

- **Transfer function:**

  L' = ((c1 + c2 \* L<sup>m1</sup>) / (1 + c3 \* L<sup>m1</sup>))<sup>m2</sup>

- **Inverse Transfer function:**

  L = (max(L'<sup>1/m2</sup> - c1, 0) / (c2 - c3 \* L'<sup>1/m2</sup>))<sup>1/m1</sup>

Take care when converting between this transfer function and non-HDR transfer functions: the linear RGB values \[0…1\] of HDR content map to a luminance range of 0 to 10000 cd/m<sup>2</sup> whereas the linear RGB values of non-HDR (aka Standard Dynamic Range or SDR) map to a luminance range of 0 to 100 cd/m<sup>2</sup>.

To go from SDR to HDR you will have to divide L by 100 first. To go in the other direction you will have to multiply L by 100. Of course, this clamps all luminance values over 100 cd/m<sup>2</sup> to 100 cd/m<sup>2</sup>.

There are better methods, see e.g. [colimg](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-colimg-1>) for more in-depth information about this.
