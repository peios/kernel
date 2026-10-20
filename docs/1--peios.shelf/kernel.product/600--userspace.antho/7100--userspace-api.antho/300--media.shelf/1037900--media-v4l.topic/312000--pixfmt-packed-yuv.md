---
title: "Packed YUV formats"
type: reference
description: "Similarly to the packed RGB formats, the packed YUV formats store the Y, Cb and Cr components consecutively in memory. They may apply subsampling to the chroma components and thus differ in how they interlave the three components."
---

<a id="rst-packed-yuv-formats"></a>
<a id="rst-packed-yuv"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

Similarly to the packed RGB formats, the packed YUV formats store the Y, Cb and Cr components consecutively in memory. They may apply subsampling to the chroma components and thus differ in how they interlave the three components.

> [!NOTE]
>
> - In all the tables that follow, bit 7 is the most significant bit in a byte.
>
> - 'Y', 'Cb' and 'Cr' denote bits of the luma, blue chroma (also known as 'U') and red chroma (also known as 'V') components respectively. 'A' denotes bits of the alpha component (if supported by the format), and 'X' denotes padding bits.

<a id="rst-subsampling"></a>

## 4:4:4 Subsampling

These formats do not subsample the chroma components and store each pixels as a full triplet of Y, Cb and Cr values.

The next table lists the packed YUV 4:4:4 formats with less than 8 bits per component. They are named based on the order of the Y, Cb and Cr components as seen in a 16-bit word, which is then stored in memory in little endian byte order, and on the number of bits for each component. For instance the YUV565 format stores a pixel in a 16-bit word \[15:0\] laid out at as \[Y'<sub>4-0</sub> Cb<sub>5-0</sub> Cr<sub>4-0</sub>\], and stored in memory in two bytes, \[Cb<sub>2-0</sub> Cr<sub>4-0</sub>\] followed by \[Y'<sub>4-0</sub> Cb<sub>5-3</sub>\].

<!-- Source LaTeX layout: \begingroup
\scriptsize
\setlength{\tabcolsep}{2pt} -->

<!-- tabularcolumns: |p{3.5cm}|p{0.96cm}|p{0.52cm}|p{0.52cm}|p{0.52cm}|p{0.52cm}|p{0.52cm}|p{0.52cm}|p{0.52cm}|p{0.52cm}|p{0.52cm}|p{0.52cm}|p{0.52cm}|p{0.52cm}|p{0.52cm}|p{0.52cm}|p{0.52cm}|p{0.52cm}| -->


<table>
<caption>

Packed YUV 4:4:4 Image Formats (less than 8bpc)

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
</tr>
</thead>
<tbody>
<tr>
<td>



`V4L2_PIX_FMT_YUV444`

</td>
<td>



'Y444'

</td>
<td>



Cb<sub>3</sub>

</td>
<td>



Cb<sub>2</sub>

</td>
<td>



Cb<sub>1</sub>

</td>
<td>



Cb<sub>0</sub>

</td>
<td>



Cr<sub>3</sub>

</td>
<td>



Cr<sub>2</sub>

</td>
<td>



Cr<sub>1</sub>

</td>
<td>



Cr<sub>0</sub>

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



Y'<sub>3</sub>

</td>
<td>



Y'<sub>2</sub>

</td>
<td>



Y'<sub>1</sub>

</td>
<td>



<a id="rst-v4l2-pix-fmt-yuv444"></a>

Y'<sub>0</sub>

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_YUV555`

</td>
<td>



'YUVO'

</td>
<td>



Cb<sub>2</sub>

</td>
<td>



Cb<sub>1</sub>

</td>
<td>



Cb<sub>0</sub>

</td>
<td>



Cr<sub>4</sub>

</td>
<td>



Cr<sub>3</sub>

</td>
<td>



Cr<sub>2</sub>

</td>
<td>



Cr<sub>1</sub>

</td>
<td>



Cr<sub>0</sub>

</td>
<td>



a

</td>
<td>



Y'<sub>4</sub>

</td>
<td>



Y'<sub>3</sub>

</td>
<td>



Y'<sub>2</sub>

</td>
<td>



Y'<sub>1</sub>

</td>
<td>



Y'<sub>0</sub>

</td>
<td>



Cb<sub>4</sub>

</td>
<td>



<a id="rst-v4l2-pix-fmt-yuv555"></a>

Cb<sub>3</sub>

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_YUV565`

</td>
<td>



'YUVP'

</td>
<td>



Cb<sub>2</sub>

</td>
<td>



Cb<sub>1</sub>

</td>
<td>



Cb<sub>0</sub>

</td>
<td>



Cr<sub>4</sub>

</td>
<td>



Cr<sub>3</sub>

</td>
<td>



Cr<sub>2</sub>

</td>
<td>



Cr<sub>1</sub>

</td>
<td>



Cr<sub>0</sub>

</td>
<td>



Y'<sub>4</sub>

</td>
<td>



Y'<sub>3</sub>

</td>
<td>



Y'<sub>2</sub>

</td>
<td>



Y'<sub>1</sub>

</td>
<td>



Y'<sub>0</sub>

</td>
<td>



Cb<sub>5</sub>

</td>
<td>



Cb<sub>4</sub>

</td>
<td>



<a id="rst-v4l2-pix-fmt-yuv565"></a>

Cb<sub>3</sub>

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \endgroup -->

> [!NOTE]
>
> For the YUV444 and YUV555 formats, the value of alpha bits is undefined when reading from the driver, ignored when writing to the driver, except when alpha blending has been negotiated for a [Video Overlay](<~kernel/userspace/userspace-api/media-v4l/dev-overlay#rst-overlay>) or [Video Output Overlay](<~kernel/userspace/userspace-api/media-v4l/dev-osd#rst-osd>).

The next table lists the packed YUV 4:4:4 formats with 8 bits per component. They are named based on the order of the Y, Cb and Cr components as stored in memory, and on the total number of bits per pixel. For instance, the VUYX32 format stores a pixel with Cr<sub>7-0</sub> in the first byte, Cb<sub>7-0</sub> in the second byte and Y'<sub>7-0</sub> in the third byte.


<table>
<caption>

Packed YUV Image Formats (8bpc)

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
</tr>
</thead>
<tbody>
<tr>
<td>



`V4L2_PIX_FMT_YUV32`

</td>
<td>



'YUV4'

</td>
<td>



A<sub>7-0</sub>

</td>
<td>



Y'<sub>7-0</sub>

</td>
<td>



Cb<sub>7-0</sub>

</td>
<td>



<a id="rst-v4l2-pix-fmt-yuv32"></a>

Cr<sub>7-0</sub>

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_AYUV32`

</td>
<td>



'AYUV'

</td>
<td>



A<sub>7-0</sub>

</td>
<td>



Y'<sub>7-0</sub>

</td>
<td>



Cb<sub>7-0</sub>

</td>
<td>



<a id="rst-v4l2-pix-fmt-ayuv32"></a>

Cr<sub>7-0</sub>

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_XYUV32`

</td>
<td>



'XYUV'

</td>
<td>



X<sub>7-0</sub>

</td>
<td>



Y'<sub>7-0</sub>

</td>
<td>



Cb<sub>7-0</sub>

</td>
<td>



<a id="rst-v4l2-pix-fmt-xyuv32"></a>

Cr<sub>7-0</sub>

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_VUYA32`

</td>
<td>



'VUYA'

</td>
<td>



Cr<sub>7-0</sub>

</td>
<td>



Cb<sub>7-0</sub>

</td>
<td>



Y'<sub>7-0</sub>

</td>
<td>



<a id="rst-v4l2-pix-fmt-vuya32"></a>

A<sub>7-0</sub>

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_VUYX32`

</td>
<td>



'VUYX'

</td>
<td>



Cr<sub>7-0</sub>

</td>
<td>



Cb<sub>7-0</sub>

</td>
<td>



Y'<sub>7-0</sub>

</td>
<td>



<a id="rst-v4l2-pix-fmt-vuyx32"></a>

X<sub>7-0</sub>

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_YUVA32`

</td>
<td>



'YUVA'

</td>
<td>



Y'<sub>7-0</sub>

</td>
<td>



Cb<sub>7-0</sub>

</td>
<td>



Cr<sub>7-0</sub>

</td>
<td>



<a id="rst-v4l2-pix-fmt-yuva32"></a>

A<sub>7-0</sub>

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_YUVX32`

</td>
<td>



'YUVX'

</td>
<td>



Y'<sub>7-0</sub>

</td>
<td>



Cb<sub>7-0</sub>

</td>
<td>



Cr<sub>7-0</sub>

</td>
<td>



<a id="rst-v4l2-pix-fmt-yuvx32"></a>

X<sub>7-0</sub>

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_YUV24`

</td>
<td>



'YUV3'

</td>
<td>



Y'<sub>7-0</sub>

</td>
<td>



Cb<sub>7-0</sub>

</td>
<td>



Cr<sub>7-0</sub>

</td>
<td>



<a id="rst-v4l2-pix-fmt-yuv24"></a>

\-

</td>
</tr>
</tbody>
</table>

> [!NOTE]
>
> - The alpha component is expected to contain a meaningful value that can be used by drivers and applications.
>
> - The padding bits contain undefined values that must be ignored by all applications and drivers.

The next table lists the packed YUV 4:4:4 formats with 12 bits per component. Expand the bits per component to 16 bits, data in the high bits, zeros in the low bits, arranged in little endian order, storing 1 pixel in 6 bytes.


<table>
<caption>

Packed YUV 4:4:4 Image Formats (12bpc)

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
<th>



Byte 9-8

</th>
<th>



Byte 11-10

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



`V4L2_PIX_FMT_YUV48_12`

</td>
<td>



'Y312'

</td>
<td>



Y'<sub>0</sub>

</td>
<td>



Cb<sub>0</sub>

</td>
<td>



Cr<sub>0</sub>

</td>
<td>



Y'<sub>1</sub>

</td>
<td>



Cb<sub>1</sub>

</td>
<td>



<a id="rst-v4l2-pix-fmt-yuv48-12"></a>

Cr<sub>1</sub>

</td>
</tr>
</tbody>
</table>

<a id="rst-subsampling-1"></a>

## 4:2:2 Subsampling

These formats, commonly referred to as YUYV or YUY2, subsample the chroma components horizontally by 2, storing 2 pixels in a container. The container is 32-bits for 8-bit formats, and 64-bits for 10+-bit formats.

The packed YUYV formats with more than 8 bits per component are stored as four 16-bit little-endian words. Each word's most significant bits contain one component, and the least significant bits are zero padding.

<!-- Source LaTeX layout: \footnotesize -->

<!-- tabularcolumns: |p{3.4cm}|p{1.2cm}|p{0.8cm}|p{0.8cm}|p{0.8cm}|p{0.8cm}|p{0.8cm}|p{0.8cm}|p{0.8cm}|p{0.8cm}| -->


<table>
<caption>

Packed YUV 4:2:2 Formats in 32-bit container

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
<th>



Byte 6

</th>
<th>



Byte 7

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



`V4L2_PIX_FMT_UYVY`

</td>
<td>



'UYVY'

</td>
<td>



Cb<sub>0</sub>

</td>
<td>



Y'<sub>0</sub>

</td>
<td>



Cr<sub>0</sub>

</td>
<td>



Y'<sub>1</sub>

</td>
<td>



Cb<sub>2</sub>

</td>
<td>



Y'<sub>2</sub>

</td>
<td>



Cr<sub>2</sub>

</td>
<td>



<a id="rst-v4l2-pix-fmt-uyvy"></a>

Y'<sub>3</sub>

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_VYUY`

</td>
<td>



'VYUY'

</td>
<td>



Cr<sub>0</sub>

</td>
<td>



Y'<sub>0</sub>

</td>
<td>



Cb<sub>0</sub>

</td>
<td>



Y'<sub>1</sub>

</td>
<td>



Cr<sub>2</sub>

</td>
<td>



Y'<sub>2</sub>

</td>
<td>



Cb<sub>2</sub>

</td>
<td>



<a id="rst-v4l2-pix-fmt-vyuy"></a>

Y'<sub>3</sub>

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_YUYV`

</td>
<td>



'YUYV'

</td>
<td>



Y'<sub>0</sub>

</td>
<td>



Cb<sub>0</sub>

</td>
<td>



Y'<sub>1</sub>

</td>
<td>



Cr<sub>0</sub>

</td>
<td>



Y'<sub>2</sub>

</td>
<td>



Cb<sub>2</sub>

</td>
<td>



Y'<sub>3</sub>

</td>
<td>



<a id="rst-v4l2-pix-fmt-yuyv"></a>

Cr<sub>2</sub>

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_YVYU`

</td>
<td>



'YVYU'

</td>
<td>



Y'<sub>0</sub>

</td>
<td>



Cr<sub>0</sub>

</td>
<td>



Y'<sub>1</sub>

</td>
<td>



Cb<sub>0</sub>

</td>
<td>



Y'<sub>2</sub>

</td>
<td>



Cr<sub>2</sub>

</td>
<td>



Y'<sub>3</sub>

</td>
<td>



<a id="rst-v4l2-pix-fmt-yvyu"></a>

Cb<sub>2</sub>

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{3.4cm}|p{1.2cm}|p{0.8cm}|p{0.8cm}|p{0.8cm}|p{0.8cm}|p{0.8cm}|p{0.8cm}|p{0.8cm}|p{0.8cm}| -->


<table>
<caption>

Packed YUV 4:2:2 Formats in 64-bit container

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



Word 0

</th>
<th>



Word 1

</th>
<th>



Word 2

</th>
<th>



Word 3

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



`V4L2_PIX_FMT_Y210`

</td>
<td>



'Y210'

</td>
<td>



Y'<sub>0</sub> (bits 15-6)

</td>
<td>



Cb<sub>0</sub> (bits 15-6)

</td>
<td>



Y'<sub>1</sub> (bits 15-6)

</td>
<td>



<a id="rst-v4l2-pix-fmt-y210"></a>

Cr<sub>0</sub> (bits 15-6)

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_Y212`

</td>
<td>



'Y212'

</td>
<td>



Y'<sub>0</sub> (bits 15-4)

</td>
<td>



Cb<sub>0</sub> (bits 15-4)

</td>
<td>



Y'<sub>1</sub> (bits 15-4)

</td>
<td>



<a id="rst-v4l2-pix-fmt-y212"></a>

Cr<sub>0</sub> (bits 15-4)

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_Y216`

</td>
<td>



'Y216'

</td>
<td>



Y'<sub>0</sub> (bits 15-0)

</td>
<td>



Cb<sub>0</sub> (bits 15-0)

</td>
<td>



Y'<sub>1</sub> (bits 15-0)

</td>
<td>



<a id="rst-v4l2-pix-fmt-y216"></a>

Cr<sub>0</sub> (bits 15-0)

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

<strong>Color Sample Location:</strong> Chroma samples are [interstitially sited](<~kernel/userspace/userspace-api/media-v4l/yuv-formats#rst-yuv-chroma-centered>) horizontally.

<a id="rst-subsampling-2"></a>

## 4:1:1 Subsampling

This format subsamples the chroma components horizontally by 4, storing 8 pixels in 12 bytes.

<!-- Source LaTeX layout: \scriptsize -->

<!-- tabularcolumns: |p{2.9cm}|p{0.8cm}|p{0.5cm}|p{0.5cm}|p{0.5cm}|p{0.5cm}|p{0.5cm}|p{0.5cm}|p{0.5cm}|p{0.5cm}|p{0.5cm}|p{0.5cm}|p{0.5cm}|p{0.5cm}| -->


<table>
<caption>

Packed YUV 4:1:1 Formats

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
<th>



Byte 6

</th>
<th>



Byte 7

</th>
<th>



Byte 8

</th>
<th>



Byte 9

</th>
<th>



Byte 10

</th>
<th>



Byte 11

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



`V4L2_PIX_FMT_Y41P`

</td>
<td>



'Y41P'

</td>
<td>



Cb<sub>0</sub>

</td>
<td>



Y'<sub>0</sub>

</td>
<td>



Cr<sub>0</sub>

</td>
<td>



Y'<sub>1</sub>

</td>
<td>



Cb<sub>4</sub>

</td>
<td>



Y'<sub>2</sub>

</td>
<td>



Cr<sub>4</sub>

</td>
<td>



Y'<sub>3</sub>

</td>
<td>



Y'<sub>4</sub>

</td>
<td>



Y'<sub>5</sub>

</td>
<td>



Y'<sub>6</sub>

</td>
<td>



<a id="rst-v4l2-pix-fmt-y41p"></a>

Y'<sub>7</sub>

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

> [!NOTE]
>
> Do not confuse `V4L2_PIX_FMT_Y41P` with [V4L2\_PIX\_FMT\_YUV411P](<~kernel/userspace/userspace-api/media-v4l/pixfmt-yuv-planar#rst-v4l2-pix-fmt-yuv411p>). Y41P is derived from "YUV 4:1:1 <strong>packed</strong>", while YUV411P stands for "YUV 4:1:1 <strong>planar</strong>".

<strong>Color Sample Location:</strong> Chroma samples are [interstitially sited](<~kernel/userspace/userspace-api/media-v4l/yuv-formats#rst-yuv-chroma-centered>) horizontally.
