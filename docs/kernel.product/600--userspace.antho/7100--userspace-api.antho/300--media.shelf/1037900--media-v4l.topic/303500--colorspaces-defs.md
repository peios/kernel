---
title: "Defining Colorspaces in V4L2"
type: reference
description: "In V4L2 colorspaces are defined by four values. The first is the colorspace identifier (enum v4l2_colorspace) which defines the chromaticities, the default transfer function, the default Y'CbCr encoding and the default quantization method.…"
---

<a id="rst-defining-colorspaces-in-v4l2"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

In V4L2 colorspaces are defined by four values. The first is the colorspace identifier (enum `v4l2_colorspace`) which defines the chromaticities, the default transfer function, the default Y'CbCr encoding and the default quantization method. The second is the transfer function identifier (enum `v4l2_xfer_func`) to specify non-standard transfer functions. The third is the Y'CbCr encoding identifier (enum `v4l2_ycbcr_encoding`) to specify non-standard Y'CbCr encodings and the fourth is the quantization identifier (enum `v4l2_quantization`) to specify non-standard quantization methods. Most of the time only the colorspace field of struct `v4l2_pix_format` or struct `v4l2_pix_format_mplane` needs to be filled in.

<a id="rst-hsv-colorspace"></a>

On [HSV formats](<~kernel/userspace/userspace-api/media-v4l/hsv-formats#rst-hsv-formats>) the *Hue* is defined as the angle on the cylindrical color representation. Usually this angle is measured in degrees, i.e. 0-360. When we map this angle value into 8 bits, there are two basic ways to do it: Divide the angular value by 2 (0-179), or use the whole range, 0-255, dividing the angular value by 1.41. The enum `v4l2_hsv_encoding` specifies which encoding is used.

> [!NOTE]
>
> The default R'G'B' quantization is full range for all colorspaces. HSV formats are always full range.

<!-- tabularcolumns: |p{6.7cm}|p{10.8cm}| -->





<a id="c-v4l2_colorspace"></a>

```c
v4l2_colorspace
```


<table>
<caption>V4L2 Colorspaces</caption>
<thead>
<tr>
<th>


Identifier

</th>
<th>


Details

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


`V4L2_COLORSPACE_DEFAULT`

</td>
<td>


The default colorspace. This can be used by applications to let the driver fill in the colorspace.

</td>
</tr>
<tr>
<td>


`V4L2_COLORSPACE_SMPTE170M`

</td>
<td>


See [col-smpte-170m](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/colorspaces-details.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>).

</td>
</tr>
<tr>
<td>


`V4L2_COLORSPACE_REC709`

</td>
<td>


See [col-rec709](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/colorspaces-details.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>).

</td>
</tr>
<tr>
<td>


`V4L2_COLORSPACE_SRGB`

</td>
<td>


See [col-srgb](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/colorspaces-details.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>).

</td>
</tr>
<tr>
<td>


`V4L2_COLORSPACE_OPRGB`

</td>
<td>


See [col-oprgb](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/colorspaces-details.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>).

</td>
</tr>
<tr>
<td>


`V4L2_COLORSPACE_BT2020`

</td>
<td>


See [col-bt2020](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/colorspaces-details.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>).

</td>
</tr>
<tr>
<td>


`V4L2_COLORSPACE_DCI_P3`

</td>
<td>


See [col-dcip3](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/colorspaces-details.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>).

</td>
</tr>
<tr>
<td>


`V4L2_COLORSPACE_SMPTE240M`

</td>
<td>


See [col-smpte-240m](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/colorspaces-details.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>).

</td>
</tr>
<tr>
<td>


`V4L2_COLORSPACE_470_SYSTEM_M`

</td>
<td>


See [col-sysm](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/colorspaces-details.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>).

</td>
</tr>
<tr>
<td>


`V4L2_COLORSPACE_470_SYSTEM_BG`

</td>
<td>


See [col-sysbg](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/colorspaces-details.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>).

</td>
</tr>
<tr>
<td>


`V4L2_COLORSPACE_JPEG`

</td>
<td>


See [col-jpeg](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/colorspaces-details.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>).

</td>
</tr>
<tr>
<td>


`V4L2_COLORSPACE_RAW`

</td>
<td>


The raw colorspace. This is used for raw image capture where the image is minimally processed and is using the internal colorspace of the device. The software that processes an image using this 'colorspace' will have to know the internals of the capture device.

</td>
</tr>
</tbody>
</table>





<a id="c-v4l2_xfer_func"></a>

```c
v4l2_xfer_func
```

<!-- tabularcolumns: |p{5.5cm}|p{12.0cm}| -->


<table>
<caption>V4L2 Transfer Function</caption>
<thead>
<tr>
<th>


Identifier

</th>
<th>


Details

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


`V4L2_XFER_FUNC_DEFAULT`

</td>
<td>


Use the default transfer function as defined by the colorspace.

</td>
</tr>
<tr>
<td>


`V4L2_XFER_FUNC_709`

</td>
<td>


Use the Rec. 709 transfer function.

</td>
</tr>
<tr>
<td>


`V4L2_XFER_FUNC_SRGB`

</td>
<td>


Use the sRGB transfer function.

</td>
</tr>
<tr>
<td>


`V4L2_XFER_FUNC_OPRGB`

</td>
<td>


Use the opRGB transfer function.

</td>
</tr>
<tr>
<td>


`V4L2_XFER_FUNC_SMPTE240M`

</td>
<td>


Use the SMPTE 240M transfer function.

</td>
</tr>
<tr>
<td>


`V4L2_XFER_FUNC_NONE`

</td>
<td>


Do not use a transfer function (i.e. use linear RGB values).

</td>
</tr>
<tr>
<td>


`V4L2_XFER_FUNC_DCI_P3`

</td>
<td>


Use the DCI-P3 transfer function.

</td>
</tr>
<tr>
<td>


`V4L2_XFER_FUNC_SMPTE2084`

</td>
<td>


Use the SMPTE 2084 transfer function. See [xf-smpte-2084](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/colorspaces-details.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>).

</td>
</tr>
</tbody>
</table>





<a id="c-v4l2_ycbcr_encoding"></a>

```c
v4l2_ycbcr_encoding
```

<!-- tabularcolumns: |p{7.2cm}|p{10.3cm}| -->


<table>
<caption>V4L2 Y&#x27;CbCr Encodings</caption>
<thead>
<tr>
<th>


Identifier

</th>
<th>


Details

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


`V4L2_YCBCR_ENC_DEFAULT`

</td>
<td>


Use the default Y'CbCr encoding as defined by the colorspace.

</td>
</tr>
<tr>
<td>


`V4L2_YCBCR_ENC_601`

</td>
<td>


Use the BT.601 Y'CbCr encoding.

</td>
</tr>
<tr>
<td>


`V4L2_YCBCR_ENC_709`

</td>
<td>


Use the Rec. 709 Y'CbCr encoding.

</td>
</tr>
<tr>
<td>


`V4L2_YCBCR_ENC_XV601`

</td>
<td>


Use the extended gamut xvYCC BT.601 encoding.

</td>
</tr>
<tr>
<td>


`V4L2_YCBCR_ENC_XV709`

</td>
<td>


Use the extended gamut xvYCC Rec. 709 encoding.

</td>
</tr>
<tr>
<td>


`V4L2_YCBCR_ENC_BT2020`

</td>
<td>


Use the default non-constant luminance BT.2020 Y'CbCr encoding.

</td>
</tr>
<tr>
<td>


`V4L2_YCBCR_ENC_BT2020_CONST_LUM`

</td>
<td>


Use the constant luminance BT.2020 Yc'CbcCrc encoding.

</td>
</tr>
<tr>
<td>


`V4L2_YCBCR_ENC_SMPTE_240M`

</td>
<td>


Use the SMPTE 240M Y'CbCr encoding.

</td>
</tr>
</tbody>
</table>





<a id="c-v4l2_hsv_encoding"></a>

```c
v4l2_hsv_encoding
```

<!-- tabularcolumns: |p{6.5cm}|p{11.0cm}| -->


<table>
<caption>V4L2 HSV Encodings</caption>
<thead>
<tr>
<th>


Identifier

</th>
<th>


Details

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


`V4L2_HSV_ENC_180`

</td>
<td>


For the Hue, each LSB is two degrees.

</td>
</tr>
<tr>
<td>


`V4L2_HSV_ENC_256`

</td>
<td>


For the Hue, the 360 degrees are mapped into 8 bits, i.e. each LSB is roughly 1.41 degrees.

</td>
</tr>
</tbody>
</table>





<a id="c-v4l2_quantization"></a>

```c
v4l2_quantization
```

<!-- tabularcolumns: |p{6.5cm}|p{11.0cm}| -->


<table>
<caption>V4L2 Quantization Methods</caption>
<thead>
<tr>
<th>


Identifier

</th>
<th>


Details

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


`V4L2_QUANTIZATION_DEFAULT`

</td>
<td>


Use the default quantization encoding as defined by the colorspace. This is always full range for R'G'B' and HSV. It is usually limited range for Y'CbCr.

</td>
</tr>
<tr>
<td>


`V4L2_QUANTIZATION_FULL_RANGE`

</td>
<td>


Use the full range quantization encoding. I.e. the range \[0…1\] is mapped to \[0…255\] (with possible clipping to \[1…254\] to avoid the 0x00 and 0xff values). Cb and Cr are mapped from \[-0.5…0.5\] to \[0…255\] (with possible clipping to \[1…254\] to avoid the 0x00 and 0xff values).

</td>
</tr>
<tr>
<td>


`V4L2_QUANTIZATION_LIM_RANGE`

</td>
<td>


Use the limited range quantization encoding. I.e. the range \[0…1\] is mapped to \[16…235\]. Cb and Cr are mapped from \[-0.5…0.5\] to \[16…240\]. Limited Range cannot be used with HSV.

</td>
</tr>
</tbody>
</table>
