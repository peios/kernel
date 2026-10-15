---
title: "RGB Formats"
type: reference
description: "These formats encode each pixel as a triplet of RGB values. They are packed formats, meaning that the RGB values for one pixel are stored consecutively in memory and each pixel consumes an integer number of bytes. When the number of bits…"
---

<a id="rst-rgb-formats"></a>
<a id="rst-pixfmt-rgb"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

These formats encode each pixel as a triplet of RGB values. They are packed formats, meaning that the RGB values for one pixel are stored consecutively in memory and each pixel consumes an integer number of bytes. When the number of bits required to store a pixel is not aligned to a byte boundary, the data is padded with additional bits to fill the remaining byte.

The formats differ by the number of bits per RGB component (typically but not always the same for all components), the order of components in memory, and the presence of an alpha component or additional padding bits.

The usage and value of the alpha bits in formats that support them (named ARGB or a permutation thereof, collectively referred to as alpha formats) depend on the device type and hardware operation. [Capture](<~kernel/userspace/userspace-api/media-v4l/dev-capture#rst-capture>) devices (including capture queues of mem-to-mem devices) fill the alpha component in memory. When the device captures an alpha channel the alpha component will have a meaningful value. Otherwise, when the device doesn't capture an alpha channel but can set the alpha bit to a user-configurable value, the [V4L2\_CID\_ALPHA\_COMPONENT](<~kernel/userspace/userspace-api/media-v4l/control#rst-v4l2-alpha-component>) control is used to specify that alpha value, and the alpha component of all pixels will be set to the value specified by that control. Otherwise a corresponding format without an alpha component (XRGB or XBGR) must be used instead of an alpha format.

[Output](<~kernel/userspace/userspace-api/media-v4l/dev-output#rst-output>) devices (including output queues of mem-to-mem devices and [video output overlay](<~kernel/userspace/userspace-api/media-v4l/dev-osd#rst-osd>) devices) read the alpha component from memory. When the device processes the alpha channel the alpha component must be filled with meaningful values by applications. Otherwise a corresponding format without an alpha component (XRGB or XBGR) must be used instead of an alpha format.

Formats that contain padding bits are named XRGB (or a permutation thereof). The padding bits contain undefined values and must be ignored by applications, devices and drivers, for both [capture](<~kernel/userspace/userspace-api/media-v4l/dev-capture#rst-capture>) and [output](<~kernel/userspace/userspace-api/media-v4l/dev-output#rst-output>) devices.

> [!NOTE]
>
> - In all the tables that follow, bit 7 is the most significant bit in a byte.
>
> - 'r', 'g' and 'b' denote bits of the red, green and blue components respectively. 'a' denotes bits of the alpha component (if supported by the format), and 'x' denotes padding bits.

<a id="rst-less-than-8-bits-per-component"></a>

## Less Than 8 Bits Per Component

These formats store an RGB triplet in one, two or four bytes. They are named based on the order of the RGB components as seen in a 8-, 16- or 32-bit word, which is then stored in memory in little endian byte order (unless otherwise noted by the presence of bit 31 in the 4CC value), and on the number of bits for each component. For instance, the RGB565 format stores a pixel in a 16-bit word \[15:0\] laid out at as \[R<sub>4</sub> R<sub>3</sub> R<sub>2</sub> R<sub>1</sub> R<sub>0</sub> G<sub>5</sub> G<sub>4</sub> G<sub>3</sub> G<sub>2</sub> G<sub>1</sub> G<sub>0</sub> B<sub>4</sub> B<sub>3</sub> B<sub>2</sub> B<sub>1</sub> B<sub>0</sub>\], and stored in memory in two bytes, \[R<sub>4</sub> R<sub>3</sub> R<sub>2</sub> R<sub>1</sub> R<sub>0</sub> G<sub>5</sub> G<sub>4</sub> G<sub>3</sub>\] followed by \[G<sub>2</sub> G<sub>1</sub> G<sub>0</sub> B<sub>4</sub> B<sub>3</sub> B<sub>2</sub> B<sub>1</sub> B<sub>0</sub>\].

<!-- Source LaTeX layout: \begingroup
\tiny
\setlength{\tabcolsep}{2pt} -->

<!-- tabularcolumns: |p{2.8cm}|p{2.0cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}| -->


<table>
<caption>

RGB Formats With Less Than 8 Bits Per Component

</caption>
<thead>
<tr>
<th>



Identifier

</th>
<th>



Code

</th>
<th colspan="8">



 Byte 0 in memory

</th>
<th colspan="8">



 Byte 1

</th>
<th colspan="8">



 Byte 2

</th>
<th colspan="8">



 Byte 3

</th>
</tr>
<tr>
<th>





</th>
<th>





</th>
<th>



7

</th>
<th>



6

</th>
<th>



5

</th>
<th>



4

</th>
<th>



3

</th>
<th>



2

</th>
<th>



1

</th>
<th>



0

</th>
<th>



7

</th>
<th>



6

</th>
<th>



5

</th>
<th>



4

</th>
<th>



3

</th>
<th>



2

</th>
<th>



1

</th>
<th>



0

</th>
<th>



7

</th>
<th>



6

</th>
<th>



5

</th>
<th>



4

</th>
<th>



3

</th>
<th>



2

</th>
<th>



1

</th>
<th>



0

</th>
<th>



7

</th>
<th>



6

</th>
<th>



5

</th>
<th>



4

</th>
<th>



3

</th>
<th>



2

</th>
<th>



1

</th>
<th>



0

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



`V4L2_PIX_FMT_RGB332`

</td>
<td>



'RGB1'

</td>
<td>



r<sub>2</sub>

</td>
<td>



r<sub>1</sub>

</td>
<td>



r<sub>0</sub>

</td>
<td>



g<sub>2</sub>

</td>
<td>



g<sub>1</sub>

</td>
<td>



g<sub>0</sub>

</td>
<td>



b<sub>1</sub>

</td>
<td>



b<sub>0</sub>

</td>
<td colspan="24">





</td>
</tr>
<tr>
<td>

<a id="rst-v4l2-pix-fmt-rgb332"></a>

`V4L2_PIX_FMT_ARGB444`

</td>
<td>



'AR12'

</td>
<td>



g<sub>3</sub>

</td>
<td>



g<sub>2</sub>

</td>
<td>



g<sub>1</sub>

</td>
<td>



g<sub>0</sub>

</td>
<td>



b<sub>3</sub>

</td>
<td>



b<sub>2</sub>

</td>
<td>



b<sub>1</sub>

</td>
<td>



b<sub>0</sub>

</td>
<td>



a<sub>3</sub>

</td>
<td>



a<sub>2</sub>

</td>
<td>



a<sub>1</sub>

</td>
<td>



a<sub>0</sub>

</td>
<td>



r<sub>3</sub>

</td>
<td>



r<sub>2</sub>

</td>
<td>



r<sub>1</sub>

</td>
<td>



r<sub>0</sub>

</td>
<td colspan="16">





</td>
</tr>
<tr>
<td>

<a id="rst-v4l2-pix-fmt-argb444"></a>

`V4L2_PIX_FMT_XRGB444`

</td>
<td>



'XR12'

</td>
<td>



g<sub>3</sub>

</td>
<td>



g<sub>2</sub>

</td>
<td>



g<sub>1</sub>

</td>
<td>



g<sub>0</sub>

</td>
<td>



b<sub>3</sub>

</td>
<td>



b<sub>2</sub>

</td>
<td>



b<sub>1</sub>

</td>
<td>



b<sub>0</sub>

</td>
<td>



x

</td>
<td>



x

</td>
<td>



x

</td>
<td>



x

</td>
<td>



r<sub>3</sub>

</td>
<td>



r<sub>2</sub>

</td>
<td>



r<sub>1</sub>

</td>
<td>



r<sub>0</sub>

</td>
<td colspan="16">





</td>
</tr>
<tr>
<td>

<a id="rst-v4l2-pix-fmt-xrgb444"></a>

`V4L2_PIX_FMT_RGBA444`

</td>
<td>



'RA12'

</td>
<td>



b<sub>3</sub>

</td>
<td>



b<sub>2</sub>

</td>
<td>



b<sub>1</sub>

</td>
<td>



b<sub>0</sub>

</td>
<td>



a<sub>3</sub>

</td>
<td>



a<sub>2</sub>

</td>
<td>



a<sub>1</sub>

</td>
<td>



a<sub>0</sub>

</td>
<td>



r<sub>3</sub>

</td>
<td>



r<sub>2</sub>

</td>
<td>



r<sub>1</sub>

</td>
<td>



r<sub>0</sub>

</td>
<td>



g<sub>3</sub>

</td>
<td>



g<sub>2</sub>

</td>
<td>



g<sub>1</sub>

</td>
<td>



g<sub>0</sub>

</td>
<td colspan="16">





</td>
</tr>
<tr>
<td>

<a id="rst-v4l2-pix-fmt-rgba444"></a>

`V4L2_PIX_FMT_RGBX444`

</td>
<td>



'RX12'

</td>
<td>



b<sub>3</sub>

</td>
<td>



b<sub>2</sub>

</td>
<td>



b<sub>1</sub>

</td>
<td>



b<sub>0</sub>

</td>
<td>



x

</td>
<td>



x

</td>
<td>



x

</td>
<td>



x

</td>
<td>



r<sub>3</sub>

</td>
<td>



r<sub>2</sub>

</td>
<td>



r<sub>1</sub>

</td>
<td>



r<sub>0</sub>

</td>
<td>



g<sub>3</sub>

</td>
<td>



g<sub>2</sub>

</td>
<td>



g<sub>1</sub>

</td>
<td>



g<sub>0</sub>

</td>
<td colspan="16">





</td>
</tr>
<tr>
<td>

<a id="rst-v4l2-pix-fmt-rgbx444"></a>

`V4L2_PIX_FMT_ABGR444`

</td>
<td>



'AB12'

</td>
<td>



g<sub>3</sub>

</td>
<td>



g<sub>2</sub>

</td>
<td>



g<sub>1</sub>

</td>
<td>



g<sub>0</sub>

</td>
<td>



r<sub>3</sub>

</td>
<td>



r<sub>2</sub>

</td>
<td>



r<sub>1</sub>

</td>
<td>



r<sub>0</sub>

</td>
<td>



a<sub>3</sub>

</td>
<td>



a<sub>2</sub>

</td>
<td>



a<sub>1</sub>

</td>
<td>



a<sub>0</sub>

</td>
<td>



b<sub>3</sub>

</td>
<td>



b<sub>2</sub>

</td>
<td>



b<sub>1</sub>

</td>
<td>



b<sub>0</sub>

</td>
<td colspan="16">





</td>
</tr>
<tr>
<td>

<a id="rst-v4l2-pix-fmt-abgr444"></a>

`V4L2_PIX_FMT_XBGR444`

</td>
<td>



'XB12'

</td>
<td>



g<sub>3</sub>

</td>
<td>



g<sub>2</sub>

</td>
<td>



g<sub>1</sub>

</td>
<td>



g<sub>0</sub>

</td>
<td>



r<sub>3</sub>

</td>
<td>



r<sub>2</sub>

</td>
<td>



r<sub>1</sub>

</td>
<td>



r<sub>0</sub>

</td>
<td>



x

</td>
<td>



x

</td>
<td>



x

</td>
<td>



x

</td>
<td>



b<sub>3</sub>

</td>
<td>



b<sub>2</sub>

</td>
<td>



b<sub>1</sub>

</td>
<td>



b<sub>0</sub>

</td>
<td colspan="16">





</td>
</tr>
<tr>
<td>

<a id="rst-v4l2-pix-fmt-xbgr444"></a>

`V4L2_PIX_FMT_BGRA444`

</td>
<td>



'BA12'

</td>
<td>



r<sub>3</sub>

</td>
<td>



r<sub>2</sub>

</td>
<td>



r<sub>1</sub>

</td>
<td>



r<sub>0</sub>

</td>
<td>



a<sub>3</sub>

</td>
<td>



a<sub>2</sub>

</td>
<td>



a<sub>1</sub>

</td>
<td>



a<sub>0</sub>

</td>
<td>



b<sub>3</sub>

</td>
<td>



b<sub>2</sub>

</td>
<td>



b<sub>1</sub>

</td>
<td>



b<sub>0</sub>

</td>
<td>



g<sub>3</sub>

</td>
<td>



g<sub>2</sub>

</td>
<td>



g<sub>1</sub>

</td>
<td>



g<sub>0</sub>

</td>
<td colspan="16">





</td>
</tr>
<tr>
<td>

<a id="rst-v4l2-pix-fmt-bgra444"></a>

`V4L2_PIX_FMT_BGRX444`

</td>
<td>



'BX12'

</td>
<td>



r<sub>3</sub>

</td>
<td>



r<sub>2</sub>

</td>
<td>



r<sub>1</sub>

</td>
<td>



r<sub>0</sub>

</td>
<td>



x

</td>
<td>



x

</td>
<td>



x

</td>
<td>



x

</td>
<td>



b<sub>3</sub>

</td>
<td>



b<sub>2</sub>

</td>
<td>



b<sub>1</sub>

</td>
<td>



b<sub>0</sub>

</td>
<td>



g<sub>3</sub>

</td>
<td>



g<sub>2</sub>

</td>
<td>



g<sub>1</sub>

</td>
<td>



g<sub>0</sub>

</td>
<td colspan="16">





</td>
</tr>
<tr>
<td>

<a id="rst-v4l2-pix-fmt-bgrx444"></a>

`V4L2_PIX_FMT_ARGB555`

</td>
<td>



'AR15'

</td>
<td>



g<sub>2</sub>

</td>
<td>



g<sub>1</sub>

</td>
<td>



g<sub>0</sub>

</td>
<td>



b<sub>4</sub>

</td>
<td>



b<sub>3</sub>

</td>
<td>



b<sub>2</sub>

</td>
<td>



b<sub>1</sub>

</td>
<td>



b<sub>0</sub>

</td>
<td>



a

</td>
<td>



r<sub>4</sub>

</td>
<td>



r<sub>3</sub>

</td>
<td>



r<sub>2</sub>

</td>
<td>



r<sub>1</sub>

</td>
<td>



r<sub>0</sub>

</td>
<td>



g<sub>4</sub>

</td>
<td>



g<sub>3</sub>

</td>
<td colspan="16">





</td>
</tr>
<tr>
<td>

<a id="rst-v4l2-pix-fmt-argb555"></a>

`V4L2_PIX_FMT_XRGB555`

</td>
<td>



'XR15'

</td>
<td>



g<sub>2</sub>

</td>
<td>



g<sub>1</sub>

</td>
<td>



g<sub>0</sub>

</td>
<td>



b<sub>4</sub>

</td>
<td>



b<sub>3</sub>

</td>
<td>



b<sub>2</sub>

</td>
<td>



b<sub>1</sub>

</td>
<td>



b<sub>0</sub>

</td>
<td>



x

</td>
<td>



r<sub>4</sub>

</td>
<td>



r<sub>3</sub>

</td>
<td>



r<sub>2</sub>

</td>
<td>



r<sub>1</sub>

</td>
<td>



r<sub>0</sub>

</td>
<td>



g<sub>4</sub>

</td>
<td>



g<sub>3</sub>

</td>
<td colspan="16">





</td>
</tr>
<tr>
<td>

<a id="rst-v4l2-pix-fmt-xrgb555"></a>

`V4L2_PIX_FMT_RGBA555`

</td>
<td>



'RA15'

</td>
<td>



g<sub>1</sub>

</td>
<td>



g<sub>0</sub>

</td>
<td>



b<sub>4</sub>

</td>
<td>



b<sub>3</sub>

</td>
<td>



b<sub>2</sub>

</td>
<td>



b<sub>1</sub>

</td>
<td>



b<sub>0</sub>

</td>
<td>



a

</td>
<td>



r<sub>4</sub>

</td>
<td>



r<sub>3</sub>

</td>
<td>



r<sub>2</sub>

</td>
<td>



r<sub>1</sub>

</td>
<td>



r<sub>0</sub>

</td>
<td>



g<sub>4</sub>

</td>
<td>



g<sub>3</sub>

</td>
<td>



g<sub>2</sub>

</td>
<td colspan="16">





</td>
</tr>
<tr>
<td>

<a id="rst-v4l2-pix-fmt-rgba555"></a>

`V4L2_PIX_FMT_RGBX555`

</td>
<td>



'RX15'

</td>
<td>



g<sub>1</sub>

</td>
<td>



g<sub>0</sub>

</td>
<td>



b<sub>4</sub>

</td>
<td>



b<sub>3</sub>

</td>
<td>



b<sub>2</sub>

</td>
<td>



b<sub>1</sub>

</td>
<td>



b<sub>0</sub>

</td>
<td>



x

</td>
<td>



r<sub>4</sub>

</td>
<td>



r<sub>3</sub>

</td>
<td>



r<sub>2</sub>

</td>
<td>



r<sub>1</sub>

</td>
<td>



r<sub>0</sub>

</td>
<td>



g<sub>4</sub>

</td>
<td>



g<sub>3</sub>

</td>
<td>



g<sub>2</sub>

</td>
<td colspan="16">





</td>
</tr>
<tr>
<td>

<a id="rst-v4l2-pix-fmt-rgbx555"></a>

`V4L2_PIX_FMT_ABGR555`

</td>
<td>



'AB15'

</td>
<td>



g<sub>2</sub>

</td>
<td>



g<sub>1</sub>

</td>
<td>



g<sub>0</sub>

</td>
<td>



r<sub>4</sub>

</td>
<td>



r<sub>3</sub>

</td>
<td>



r<sub>2</sub>

</td>
<td>



r<sub>1</sub>

</td>
<td>



r<sub>0</sub>

</td>
<td>



a

</td>
<td>



b<sub>4</sub>

</td>
<td>



b<sub>3</sub>

</td>
<td>



b<sub>2</sub>

</td>
<td>



b<sub>1</sub>

</td>
<td>



b<sub>0</sub>

</td>
<td>



g<sub>4</sub>

</td>
<td>



g<sub>3</sub>

</td>
<td colspan="16">





</td>
</tr>
<tr>
<td>

<a id="rst-v4l2-pix-fmt-abgr555"></a>

`V4L2_PIX_FMT_XBGR555`

</td>
<td>



'XB15'

</td>
<td>



g<sub>2</sub>

</td>
<td>



g<sub>1</sub>

</td>
<td>



g<sub>0</sub>

</td>
<td>



r<sub>4</sub>

</td>
<td>



r<sub>3</sub>

</td>
<td>



r<sub>2</sub>

</td>
<td>



r<sub>1</sub>

</td>
<td>



r<sub>0</sub>

</td>
<td>



x

</td>
<td>



b<sub>4</sub>

</td>
<td>



b<sub>3</sub>

</td>
<td>



b<sub>2</sub>

</td>
<td>



b<sub>1</sub>

</td>
<td>



b<sub>0</sub>

</td>
<td>



g<sub>4</sub>

</td>
<td>



g<sub>3</sub>

</td>
<td colspan="16">





</td>
</tr>
<tr>
<td>

<a id="rst-v4l2-pix-fmt-xbgr555"></a>

`V4L2_PIX_FMT_BGRA555`

</td>
<td>



'BA15'

</td>
<td>



g<sub>1</sub>

</td>
<td>



g<sub>0</sub>

</td>
<td>



r<sub>4</sub>

</td>
<td>



r<sub>3</sub>

</td>
<td>



r<sub>2</sub>

</td>
<td>



r<sub>1</sub>

</td>
<td>



r<sub>0</sub>

</td>
<td>



a

</td>
<td>



b<sub>4</sub>

</td>
<td>



b<sub>3</sub>

</td>
<td>



b<sub>2</sub>

</td>
<td>



b<sub>1</sub>

</td>
<td>



b<sub>0</sub>

</td>
<td>



g<sub>4</sub>

</td>
<td>



g<sub>3</sub>

</td>
<td>



g<sub>2</sub>

</td>
<td colspan="16">





</td>
</tr>
<tr>
<td>

<a id="rst-v4l2-pix-fmt-bgra555"></a>

`V4L2_PIX_FMT_BGRX555`

</td>
<td>



'BX15'

</td>
<td>



g<sub>1</sub>

</td>
<td>



g<sub>0</sub>

</td>
<td>



r<sub>4</sub>

</td>
<td>



r<sub>3</sub>

</td>
<td>



r<sub>2</sub>

</td>
<td>



r<sub>1</sub>

</td>
<td>



r<sub>0</sub>

</td>
<td>



x

</td>
<td>



b<sub>4</sub>

</td>
<td>



b<sub>3</sub>

</td>
<td>



b<sub>2</sub>

</td>
<td>



b<sub>1</sub>

</td>
<td>



b<sub>0</sub>

</td>
<td>



g<sub>4</sub>

</td>
<td>



g<sub>3</sub>

</td>
<td>



g<sub>2</sub>

</td>
<td colspan="16">





</td>
</tr>
<tr>
<td>

<a id="rst-v4l2-pix-fmt-bgrx555"></a>

`V4L2_PIX_FMT_RGB565`

</td>
<td>



'RGBP'

</td>
<td>



g<sub>2</sub>

</td>
<td>



g<sub>1</sub>

</td>
<td>



g<sub>0</sub>

</td>
<td>



b<sub>4</sub>

</td>
<td>



b<sub>3</sub>

</td>
<td>



b<sub>2</sub>

</td>
<td>



b<sub>1</sub>

</td>
<td>



b<sub>0</sub>

</td>
<td>



r<sub>4</sub>

</td>
<td>



r<sub>3</sub>

</td>
<td>



r<sub>2</sub>

</td>
<td>



r<sub>1</sub>

</td>
<td>



r<sub>0</sub>

</td>
<td>



g<sub>5</sub>

</td>
<td>



g<sub>4</sub>

</td>
<td>



g<sub>3</sub>

</td>
<td colspan="16">





</td>
</tr>
<tr>
<td>

<a id="rst-v4l2-pix-fmt-rgb565"></a>

`V4L2_PIX_FMT_ARGB555X`

</td>
<td>



'AR15' \| (1 &lt;&lt; 31)

</td>
<td>



a

</td>
<td>



r<sub>4</sub>

</td>
<td>



r<sub>3</sub>

</td>
<td>



r<sub>2</sub>

</td>
<td>



r<sub>1</sub>

</td>
<td>



r<sub>0</sub>

</td>
<td>



g<sub>4</sub>

</td>
<td>



g<sub>3</sub>

</td>
<td>



g<sub>2</sub>

</td>
<td>



g<sub>1</sub>

</td>
<td>



g<sub>0</sub>

</td>
<td>



b<sub>4</sub>

</td>
<td>



b<sub>3</sub>

</td>
<td>



b<sub>2</sub>

</td>
<td>



b<sub>1</sub>

</td>
<td>



b<sub>0</sub>

</td>
<td colspan="16">





</td>
</tr>
<tr>
<td>

<a id="rst-v4l2-pix-fmt-argb555x"></a>

`V4L2_PIX_FMT_XRGB555X`

</td>
<td>



'XR15' \| (1 &lt;&lt; 31)

</td>
<td>



x

</td>
<td>



r<sub>4</sub>

</td>
<td>



r<sub>3</sub>

</td>
<td>



r<sub>2</sub>

</td>
<td>



r<sub>1</sub>

</td>
<td>



r<sub>0</sub>

</td>
<td>



g<sub>4</sub>

</td>
<td>



g<sub>3</sub>

</td>
<td>



g<sub>2</sub>

</td>
<td>



g<sub>1</sub>

</td>
<td>



g<sub>0</sub>

</td>
<td>



b<sub>4</sub>

</td>
<td>



b<sub>3</sub>

</td>
<td>



b<sub>2</sub>

</td>
<td>



b<sub>1</sub>

</td>
<td>



b<sub>0</sub>

</td>
<td colspan="16">





</td>
</tr>
<tr>
<td>

<a id="rst-v4l2-pix-fmt-xrgb555x"></a>

`V4L2_PIX_FMT_RGB565X`

</td>
<td>



'RGBR'

</td>
<td>



r<sub>4</sub>

</td>
<td>



r<sub>3</sub>

</td>
<td>



r<sub>2</sub>

</td>
<td>



r<sub>1</sub>

</td>
<td>



r<sub>0</sub>

</td>
<td>



g<sub>5</sub>

</td>
<td>



g<sub>4</sub>

</td>
<td>



g<sub>3</sub>

</td>
<td>



g<sub>2</sub>

</td>
<td>



g<sub>1</sub>

</td>
<td>



g<sub>0</sub>

</td>
<td>



b<sub>4</sub>

</td>
<td>



b<sub>3</sub>

</td>
<td>



b<sub>2</sub>

</td>
<td>



b<sub>1</sub>

</td>
<td>



b<sub>0</sub>

</td>
<td colspan="16">





</td>
</tr>
<tr>
<td>

<a id="rst-v4l2-pix-fmt-rgb565x"></a>

`V4L2_PIX_FMT_BGR666`

</td>
<td>



'BGRH'

</td>
<td>



b<sub>5</sub>

</td>
<td>



b<sub>4</sub>

</td>
<td>



b<sub>3</sub>

</td>
<td>



b<sub>2</sub>

</td>
<td>



b<sub>1</sub>

</td>
<td>



b<sub>0</sub>

</td>
<td>



g<sub>5</sub>

</td>
<td>



g<sub>4</sub>

</td>
<td>



g<sub>3</sub>

</td>
<td>



g<sub>2</sub>

</td>
<td>



g<sub>1</sub>

</td>
<td>



g<sub>0</sub>

</td>
<td>



r<sub>5</sub>

</td>
<td>



r<sub>4</sub>

</td>
<td>



r<sub>3</sub>

</td>
<td>



r<sub>2</sub>

</td>
<td>



r<sub>1</sub>

</td>
<td>



r<sub>0</sub>

</td>
<td>



x

</td>
<td>



x

</td>
<td>



x

</td>
<td>



x

</td>
<td>



x

</td>
<td>



x

</td>
<td>



x

</td>
<td>



x

</td>
<td>



x

</td>
<td>



x

</td>
<td>



x

</td>
<td>



x

</td>
<td>



x

</td>
<td>



<a id="rst-v4l2-pix-fmt-bgr666"></a>

x

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \endgroup -->

<a id="rst-bits-per-component"></a>

## 8 Bits Per Component

These formats store an RGB triplet in three or four bytes. They are named based on the order of the RGB components as stored in memory, and on the total number of bits per pixel. For instance, RGB24 format stores a pixel with \[R<sub>7</sub> R<sub>6</sub> R<sub>5</sub> R<sub>4</sub> R<sub>3</sub> R<sub>2</sub> R<sub>1</sub> R<sub>0</sub>\] in the first byte, \[G<sub>7</sub> G<sub>6</sub> G<sub>5</sub> G<sub>4</sub> G<sub>3</sub> G<sub>2</sub> G<sub>1</sub> G<sub>0</sub>\] in the second byte and \[B<sub>7</sub> B<sub>6</sub> B<sub>5</sub> B<sub>4</sub> B<sub>3</sub> B<sub>2</sub> B<sub>1</sub> B<sub>0</sub>\] in the third byte. This differs from the DRM format nomenclature that instead use the order of components as seen in a 24- or 32-bit little endian word.

<!-- Source LaTeX layout: \small -->


<table>
<caption>

RGB Formats With 8 Bits Per Component

</caption>
<thead>
<tr>
<th>



Identifier

</th>
<th>



Code

</th>
<th>



Byte 0 in memory

</th>
<th>



Byte 1

</th>
<th>



Byte 2

</th>
<th>



Byte 3

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



`V4L2_PIX_FMT_BGR24`

</td>
<td>



'BGR3'

</td>
<td>



B<sub>7-0</sub>

</td>
<td>



G<sub>7-0</sub>

</td>
<td>



R<sub>7-0</sub>

</td>
<td>





</td>
</tr>
<tr>
<td>

<a id="rst-v4l2-pix-fmt-bgr24"></a>

`V4L2_PIX_FMT_RGB24`

</td>
<td>



'RGB3'

</td>
<td>



R<sub>7-0</sub>

</td>
<td>



G<sub>7-0</sub>

</td>
<td>



B<sub>7-0</sub>

</td>
<td>





</td>
</tr>
<tr>
<td>

<a id="rst-v4l2-pix-fmt-rgb24"></a>

`V4L2_PIX_FMT_ABGR32`

</td>
<td>



'AR24'

</td>
<td>



B<sub>7-0</sub>

</td>
<td>



G<sub>7-0</sub>

</td>
<td>



R<sub>7-0</sub>

</td>
<td>



<a id="rst-v4l2-pix-fmt-abgr32"></a>

A<sub>7-0</sub>

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_XBGR32`

</td>
<td>



'XR24'

</td>
<td>



B<sub>7-0</sub>

</td>
<td>



G<sub>7-0</sub>

</td>
<td>



R<sub>7-0</sub>

</td>
<td>



<a id="rst-v4l2-pix-fmt-xbgr32"></a>

X<sub>7-0</sub>

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_BGRA32`

</td>
<td>



'RA24'

</td>
<td>



A<sub>7-0</sub>

</td>
<td>



B<sub>7-0</sub>

</td>
<td>



G<sub>7-0</sub>

</td>
<td>



<a id="rst-v4l2-pix-fmt-bgra32"></a>

R<sub>7-0</sub>

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_BGRX32`

</td>
<td>



'RX24'

</td>
<td>



X<sub>7-0</sub>

</td>
<td>



B<sub>7-0</sub>

</td>
<td>



G<sub>7-0</sub>

</td>
<td>



<a id="rst-v4l2-pix-fmt-bgrx32"></a>

R<sub>7-0</sub>

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_RGBA32`

</td>
<td>



'AB24'

</td>
<td>



R<sub>7-0</sub>

</td>
<td>



G<sub>7-0</sub>

</td>
<td>



B<sub>7-0</sub>

</td>
<td>



<a id="rst-v4l2-pix-fmt-rgba32"></a>

A<sub>7-0</sub>

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_RGBX32`

</td>
<td>



'XB24'

</td>
<td>



R<sub>7-0</sub>

</td>
<td>



G<sub>7-0</sub>

</td>
<td>



B<sub>7-0</sub>

</td>
<td>



<a id="rst-v4l2-pix-fmt-rgbx32"></a>

X<sub>7-0</sub>

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_ARGB32`

</td>
<td>



'BA24'

</td>
<td>



A<sub>7-0</sub>

</td>
<td>



R<sub>7-0</sub>

</td>
<td>



G<sub>7-0</sub>

</td>
<td>



<a id="rst-v4l2-pix-fmt-argb32"></a>

B<sub>7-0</sub>

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_XRGB32`

</td>
<td>



'BX24'

</td>
<td>



X<sub>7-0</sub>

</td>
<td>



R<sub>7-0</sub>

</td>
<td>



G<sub>7-0</sub>

</td>
<td>



<a id="rst-v4l2-pix-fmt-xrgb32"></a>

B<sub>7-0</sub>

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

<a id="rst-bits-per-component-1"></a>

## 10 Bits Per Component

These formats store a 30-bit RGB triplet with an optional 2 bit alpha in four bytes. They are named based on the order of the RGB components as seen in a 32-bit word, which is then stored in memory in little endian byte order (unless otherwise noted by the presence of bit 31 in the 4CC value), and on the number of bits for each component.

<!-- Source LaTeX layout: \begingroup
\tiny
\setlength{\tabcolsep}{2pt} -->

<!-- tabularcolumns: |p{3.2cm}|p{0.8cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}| -->


<table>
<caption>

RGB Formats 10 Bits Per Color Component

</caption>
<thead>
<tr>
<th>



Identifier

</th>
<th>



Code

</th>
<th colspan="8">



 Byte 0 in memory

</th>
<th colspan="8">



 Byte 1

</th>
<th colspan="8">



 Byte 2

</th>
<th colspan="8">



 Byte 3

</th>
</tr>
<tr>
<th>





</th>
<th>





</th>
<th>



7

</th>
<th>



6

</th>
<th>



5

</th>
<th>



4

</th>
<th>



3

</th>
<th>



2

</th>
<th>



1

</th>
<th>



0

</th>
<th>



7

</th>
<th>



6

</th>
<th>



5

</th>
<th>



4

</th>
<th>



3

</th>
<th>



2

</th>
<th>



1

</th>
<th>



0

</th>
<th>



7

</th>
<th>



6

</th>
<th>



5

</th>
<th>



4

</th>
<th>



3

</th>
<th>



2

</th>
<th>



1

</th>
<th>



0

</th>
<th>



7

</th>
<th>



6

</th>
<th>



5

</th>
<th>



4

</th>
<th>



3

</th>
<th>



2

</th>
<th>



1

</th>
<th>



0

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



`V4L2_PIX_FMT_RGBX1010102`

</td>
<td>



'RX30'

</td>
<td>



b<sub>5</sub>

</td>
<td>



b<sub>4</sub>

</td>
<td>



b<sub>3</sub>

</td>
<td>



b<sub>2</sub>

</td>
<td>



b<sub>1</sub>

</td>
<td>



b<sub>0</sub>

</td>
<td>



x

</td>
<td>



x

</td>
<td>



g<sub>3</sub>

</td>
<td>



g<sub>2</sub>

</td>
<td>



g<sub>1</sub>

</td>
<td>



g<sub>0</sub>

</td>
<td>



b<sub>9</sub>

</td>
<td>



b<sub>8</sub>

</td>
<td>



b<sub>7</sub>

</td>
<td>



b<sub>6</sub>

</td>
<td>



r<sub>1</sub>

</td>
<td>



r<sub>0</sub>

</td>
<td>



g<sub>9</sub>

</td>
<td>



g<sub>8</sub>

</td>
<td>



g<sub>7</sub>

</td>
<td>



g<sub>6</sub>

</td>
<td>



g<sub>5</sub>

</td>
<td>



g<sub>4</sub>

</td>
<td>



r<sub>9</sub>

</td>
<td>



r<sub>8</sub>

</td>
<td>



r<sub>7</sub>

</td>
<td>



r<sub>6</sub>

</td>
<td>



r<sub>5</sub>

</td>
<td>



r<sub>4</sub>

</td>
<td>



r<sub>3</sub>

</td>
<td>



<a id="rst-v4l2-pix-fmt-rgbx1010102"></a>

r<sub>2</sub>

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_RGBA1010102`

</td>
<td>



'RA30'

</td>
<td>



b<sub>5</sub>

</td>
<td>



b<sub>4</sub>

</td>
<td>



b<sub>3</sub>

</td>
<td>



b<sub>2</sub>

</td>
<td>



b<sub>1</sub>

</td>
<td>



b<sub>0</sub>

</td>
<td>



a<sub>1</sub>

</td>
<td>



a<sub>0</sub>

</td>
<td>



g<sub>3</sub>

</td>
<td>



g<sub>2</sub>

</td>
<td>



g<sub>1</sub>

</td>
<td>



g<sub>0</sub>

</td>
<td>



b<sub>9</sub>

</td>
<td>



b<sub>8</sub>

</td>
<td>



b<sub>7</sub>

</td>
<td>



b<sub>6</sub>

</td>
<td>



r<sub>1</sub>

</td>
<td>



r<sub>0</sub>

</td>
<td>



g<sub>9</sub>

</td>
<td>



g<sub>8</sub>

</td>
<td>



g<sub>7</sub>

</td>
<td>



g<sub>6</sub>

</td>
<td>



g<sub>5</sub>

</td>
<td>



g<sub>4</sub>

</td>
<td>



r<sub>9</sub>

</td>
<td>



r<sub>8</sub>

</td>
<td>



r<sub>7</sub>

</td>
<td>



r<sub>6</sub>

</td>
<td>



r<sub>5</sub>

</td>
<td>



r<sub>4</sub>

</td>
<td>



r<sub>3</sub>

</td>
<td>



<a id="rst-v4l2-pix-fmt-rgba1010102"></a>

r<sub>2</sub>

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_ARGB2101010`

</td>
<td>



'AR30'

</td>
<td>



b<sub>7</sub>

</td>
<td>



b<sub>6</sub>

</td>
<td>



b<sub>5</sub>

</td>
<td>



b<sub>4</sub>

</td>
<td>



b<sub>3</sub>

</td>
<td>



b<sub>2</sub>

</td>
<td>



b<sub>1</sub>

</td>
<td>



b<sub>0</sub>

</td>
<td>



g<sub>5</sub>

</td>
<td>



g<sub>4</sub>

</td>
<td>



g<sub>3</sub>

</td>
<td>



g<sub>2</sub>

</td>
<td>



g<sub>1</sub>

</td>
<td>



g<sub>0</sub>

</td>
<td>



b<sub>9</sub>

</td>
<td>



b<sub>8</sub>

</td>
<td>



r<sub>3</sub>

</td>
<td>



r<sub>2</sub>

</td>
<td>



r<sub>1</sub>

</td>
<td>



r<sub>0</sub>

</td>
<td>



g<sub>9</sub>

</td>
<td>



g<sub>8</sub>

</td>
<td>



g<sub>7</sub>

</td>
<td>



g<sub>6</sub>

</td>
<td>



a<sub>1</sub>

</td>
<td>



a<sub>0</sub>

</td>
<td>



r<sub>9</sub>

</td>
<td>



r<sub>8</sub>

</td>
<td>



r<sub>7</sub>

</td>
<td>



r<sub>6</sub>

</td>
<td>



r<sub>5</sub>

</td>
<td>



<a id="rst-v4l2-pix-fmt-argb2101010"></a>

r<sub>4</sub>

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \endgroup -->

<a id="rst-bits-per-component-2"></a>

## 12 Bits Per Component

These formats store an RGB triplet in six or eight bytes, with 12 bits per component. Expand the bits per component to 16 bits, data in the high bits, zeros in the low bits, arranged in little endian order.

<!-- Source LaTeX layout: \small -->


<table>
<caption>

RGB Formats With 12 Bits Per Component

</caption>
<thead>
<tr>
<th>



Identifier

</th>
<th>



Code

</th>
<th>



Byte 1-0

</th>
<th>



Byte 3-2

</th>
<th>



Byte 5-4

</th>
<th>



Byte 7-6

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



`V4L2_PIX_FMT_BGR48_12`

</td>
<td>



'B312'

</td>
<td>



B<sub>15-4</sub>

</td>
<td>



G<sub>15-4</sub>

</td>
<td>



R<sub>15-4</sub>

</td>
<td>





</td>
</tr>
<tr>
<td>

<a id="rst-v4l2-pix-fmt-bgr48-12"></a>

`V4L2_PIX_FMT_ABGR64_12`

</td>
<td>



'B412'

</td>
<td>



B<sub>15-4</sub>

</td>
<td>



G<sub>15-4</sub>

</td>
<td>



R<sub>15-4</sub>

</td>
<td>



<a id="rst-v4l2-pix-fmt-abgr64-12"></a>

A<sub>15-4</sub>

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

<a id="rst-bits-per-component-3"></a>

## 16 Bits Per Component

These formats store an RGB triplet in six bytes, with 16 bits per component stored in memory in little endian byte order. They are named based on the order of the RGB components as stored in memory. For instance, RGB48 stores R<sub>7:0</sub> and R<sub>15:8</sub> in bytes 0 and 1 respectively. This differs from the DRM format nomenclature that instead uses the order of components as seen in the 48-bits little endian word.

<!-- Source LaTeX layout: \small -->


<table>
<caption>

RGB Formats With 16 Bits Per Component

</caption>
<thead>
<tr>
<th>



Identifier

</th>
<th>



Code

</th>
<th>



Byte 0

</th>
<th>



Byte 1

</th>
<th>



Byte 2

</th>
<th>



Byte 3

</th>
<th>



Byte 4

</th>
<th>



Byte 5

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



`V4L2_PIX_FMT_BGR48`

</td>
<td>



'BGR6'

</td>
<td>



B<sub>7-0</sub>

</td>
<td>



B<sub>15-8</sub>

</td>
<td>



G<sub>7-0</sub>

</td>
<td>



G<sub>15-8</sub>

</td>
<td>



R<sub>7-0</sub>

</td>
<td>



<a id="rst-v4l2-pix-fmt-bgr48"></a>

R<sub>15-8</sub>

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_RGB48`

</td>
<td>



'RGB6'

</td>
<td>



R<sub>7-0</sub>

</td>
<td>



R<sub>15-8</sub>

</td>
<td>



G<sub>7-0</sub>

</td>
<td>



G<sub>15-8</sub>

</td>
<td>



B<sub>7-0</sub>

</td>
<td>



<a id="rst-v4l2-pix-fmt-rgb48"></a>

B<sub>15-8</sub>

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

<a id="rst-deprecated-rgb-formats"></a>

## Deprecated RGB Formats

Formats defined in [pixfmt-rgb-deprecated](<#rst-pixfmt-rgb-deprecated>) are deprecated and must not be used by new drivers. They are documented here for reference. The meaning of their alpha bits `(a)` is ill-defined and they are interpreted as in either the corresponding ARGB or XRGB format, depending on the driver.

<!-- Source LaTeX layout: \begingroup
\tiny
\setlength{\tabcolsep}{2pt} -->

<!-- tabularcolumns: |p{2.6cm}|p{0.70cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}|p{0.22cm}| -->

<a id="rst-pixfmt-rgb-deprecated"></a>


<table>
<caption>

Deprecated Packed RGB Image Formats

</caption>
<thead>
<tr>
<th>



Identifier

</th>
<th>



Code

</th>
<th colspan="8">



 Byte 0 in memory

</th>
<th colspan="8">



 Byte 1

</th>
<th colspan="8">



 Byte 2

</th>
<th colspan="8">



 Byte 3

</th>
</tr>
<tr>
<th>





</th>
<th>





</th>
<th>



7

</th>
<th>



6

</th>
<th>



5

</th>
<th>



4

</th>
<th>



3

</th>
<th>



2

</th>
<th>



1

</th>
<th>



0

</th>
<th>



7

</th>
<th>



6

</th>
<th>



5

</th>
<th>



4

</th>
<th>



3

</th>
<th>



2

</th>
<th>



1

</th>
<th>



0

</th>
<th>



7

</th>
<th>



6

</th>
<th>



5

</th>
<th>



4

</th>
<th>



3

</th>
<th>



2

</th>
<th>



1

</th>
<th>



0

</th>
<th>



7

</th>
<th>



6

</th>
<th>



5

</th>
<th>



4

</th>
<th>



3

</th>
<th>



2

</th>
<th>



1

</th>
<th>



0

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



`V4L2_PIX_FMT_RGB444`

</td>
<td>



'R444'

</td>
<td>



g<sub>3</sub>

</td>
<td>



g<sub>2</sub>

</td>
<td>



g<sub>1</sub>

</td>
<td>



g<sub>0</sub>

</td>
<td>



b<sub>3</sub>

</td>
<td>



b<sub>2</sub>

</td>
<td>



b<sub>1</sub>

</td>
<td>



b<sub>0</sub>

</td>
<td>



a<sub>3</sub>

</td>
<td>



a<sub>2</sub>

</td>
<td>



a<sub>1</sub>

</td>
<td>



a<sub>0</sub>

</td>
<td>



r<sub>3</sub>

</td>
<td>



r<sub>2</sub>

</td>
<td>



r<sub>1</sub>

</td>
<td>



r<sub>0</sub>

</td>
<td colspan="16">





</td>
</tr>
<tr>
<td>

<a id="rst-v4l2-pix-fmt-rgb444"></a>

`V4L2_PIX_FMT_RGB555`

</td>
<td>



'RGBO'

</td>
<td>



g<sub>2</sub>

</td>
<td>



g<sub>1</sub>

</td>
<td>



g<sub>0</sub>

</td>
<td>



b<sub>4</sub>

</td>
<td>



b<sub>3</sub>

</td>
<td>



b<sub>2</sub>

</td>
<td>



b<sub>1</sub>

</td>
<td>



b<sub>0</sub>

</td>
<td>



a

</td>
<td>



r<sub>4</sub>

</td>
<td>



r<sub>3</sub>

</td>
<td>



r<sub>2</sub>

</td>
<td>



r<sub>1</sub>

</td>
<td>



r<sub>0</sub>

</td>
<td>



g<sub>4</sub>

</td>
<td>



g<sub>3</sub>

</td>
<td colspan="16">





</td>
</tr>
<tr>
<td>

<a id="rst-v4l2-pix-fmt-rgb555"></a>

`V4L2_PIX_FMT_RGB555X`

</td>
<td>



'RGBQ'

</td>
<td>



a

</td>
<td>



r<sub>4</sub>

</td>
<td>



r<sub>3</sub>

</td>
<td>



r<sub>2</sub>

</td>
<td>



r<sub>1</sub>

</td>
<td>



r<sub>0</sub>

</td>
<td>



g<sub>4</sub>

</td>
<td>



g<sub>3</sub>

</td>
<td>



g<sub>2</sub>

</td>
<td>



g<sub>1</sub>

</td>
<td>



g<sub>0</sub>

</td>
<td>



b<sub>4</sub>

</td>
<td>



b<sub>3</sub>

</td>
<td>



b<sub>2</sub>

</td>
<td>



b<sub>1</sub>

</td>
<td>



b<sub>0</sub>

</td>
<td colspan="16">





</td>
</tr>
<tr>
<td>

<a id="rst-v4l2-pix-fmt-rgb555x"></a>

`V4L2_PIX_FMT_BGR32`

</td>
<td>



'BGR4'

</td>
<td>



b<sub>7</sub>

</td>
<td>



b<sub>6</sub>

</td>
<td>



b<sub>5</sub>

</td>
<td>



b<sub>4</sub>

</td>
<td>



b<sub>3</sub>

</td>
<td>



b<sub>2</sub>

</td>
<td>



b<sub>1</sub>

</td>
<td>



b<sub>0</sub>

</td>
<td>



g<sub>7</sub>

</td>
<td>



g<sub>6</sub>

</td>
<td>



g<sub>5</sub>

</td>
<td>



g<sub>4</sub>

</td>
<td>



g<sub>3</sub>

</td>
<td>



g<sub>2</sub>

</td>
<td>



g<sub>1</sub>

</td>
<td>



g<sub>0</sub>

</td>
<td>



r<sub>7</sub>

</td>
<td>



r<sub>6</sub>

</td>
<td>



r<sub>5</sub>

</td>
<td>



r<sub>4</sub>

</td>
<td>



r<sub>3</sub>

</td>
<td>



r<sub>2</sub>

</td>
<td>



r<sub>1</sub>

</td>
<td>



r<sub>0</sub>

</td>
<td>



a<sub>7</sub>

</td>
<td>



a<sub>6</sub>

</td>
<td>



a<sub>5</sub>

</td>
<td>



a<sub>4</sub>

</td>
<td>



a<sub>3</sub>

</td>
<td>



a<sub>2</sub>

</td>
<td>



a<sub>1</sub>

</td>
<td>



<a id="rst-v4l2-pix-fmt-bgr32"></a>

a<sub>0</sub>

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_RGB32`

</td>
<td>



'RGB4'

</td>
<td>



a<sub>7</sub>

</td>
<td>



a<sub>6</sub>

</td>
<td>



a<sub>5</sub>

</td>
<td>



a<sub>4</sub>

</td>
<td>



a<sub>3</sub>

</td>
<td>



a<sub>2</sub>

</td>
<td>



a<sub>1</sub>

</td>
<td>



a<sub>0</sub>

</td>
<td>



r<sub>7</sub>

</td>
<td>



r<sub>6</sub>

</td>
<td>



r<sub>5</sub>

</td>
<td>



r<sub>4</sub>

</td>
<td>



r<sub>3</sub>

</td>
<td>



r<sub>2</sub>

</td>
<td>



r<sub>1</sub>

</td>
<td>



r<sub>0</sub>

</td>
<td>



g<sub>7</sub>

</td>
<td>



g<sub>6</sub>

</td>
<td>



g<sub>5</sub>

</td>
<td>



g<sub>4</sub>

</td>
<td>



g<sub>3</sub>

</td>
<td>



g<sub>2</sub>

</td>
<td>



g<sub>1</sub>

</td>
<td>



g<sub>0</sub>

</td>
<td>



b<sub>7</sub>

</td>
<td>



b<sub>6</sub>

</td>
<td>



b<sub>5</sub>

</td>
<td>



b<sub>4</sub>

</td>
<td>



b<sub>3</sub>

</td>
<td>



b<sub>2</sub>

</td>
<td>



b<sub>1</sub>

</td>
<td>



<a id="rst-v4l2-pix-fmt-rgb32"></a>

b<sub>0</sub>

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \endgroup -->

A test utility to determine which RGB formats a driver actually supports is available from the LinuxTV v4l-dvb repository. See [https://linuxtv.org/repo/](<https://linuxtv.org/repo/>) for access instructions.
