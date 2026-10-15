---
title: "JPEG Control Reference"
type: reference
description: "The JPEG class includes controls for common features of JPEG encoders and decoders. Currently it includes features for codecs implementing progressive baseline DCT compression process with Huffman entropy coding."
---

<a id="rst-jpeg-control-reference"></a>
<a id="rst-jpeg-controls"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

The JPEG class includes controls for common features of JPEG encoders and decoders. Currently it includes features for codecs implementing progressive baseline DCT compression process with Huffman entropy coding.

<a id="rst-jpeg-control-ids"></a>
<a id="rst-jpeg-control-id"></a>

## JPEG Control IDs

- **`V4L2_CID_JPEG_CLASS (class)`**

  The JPEG class descriptor. Calling [vidioc_queryctrl](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-queryctrl.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) for this control will return a description of this control class.

- **`V4L2_CID_JPEG_CHROMA_SUBSAMPLING (menu)`**

  The chroma subsampling factors describe how each component of an input image is sampled, in respect to maximum sample rate in each spatial dimension. See [ITU-T.81](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-itu-t81>), clause A.1.1. for more details. The `V4L2_CID_JPEG_CHROMA_SUBSAMPLING` control determines how Cb and Cr components are downsampled after converting an input image from RGB to Y'CbCr color space.

<!-- tabularcolumns: |p{7.5cm}|p{10.0cm}| -->


<table>
<tbody>
<tr>
<td>


`V4L2_JPEG_CHROMA_SUBSAMPLING_444`

</td>
<td>


No chroma subsampling, each pixel has Y, Cr and Cb values.

</td>
</tr>
<tr>
<td>


`V4L2_JPEG_CHROMA_SUBSAMPLING_422`

</td>
<td>


Horizontally subsample Cr, Cb components by a factor of 2.

</td>
</tr>
<tr>
<td>


`V4L2_JPEG_CHROMA_SUBSAMPLING_420`

</td>
<td>


Subsample Cr, Cb components horizontally and vertically by 2.

</td>
</tr>
<tr>
<td>


`V4L2_JPEG_CHROMA_SUBSAMPLING_411`

</td>
<td>


Horizontally subsample Cr, Cb components by a factor of 4.

</td>
</tr>
<tr>
<td>


`V4L2_JPEG_CHROMA_SUBSAMPLING_410`

</td>
<td>


Subsample Cr, Cb components horizontally by 4 and vertically by 2.

</td>
</tr>
<tr>
<td>


`V4L2_JPEG_CHROMA_SUBSAMPLING_GRAY`

</td>
<td>


Use only luminance component.

</td>
</tr>
</tbody>
</table>

- **`V4L2_CID_JPEG_RESTART_INTERVAL (integer)`**

  The restart interval determines an interval of inserting RSTm markers (m = 0..7). The purpose of these markers is to additionally reinitialize the encoder process, in order to process blocks of an image independently. For the lossy compression processes the restart interval unit is MCU (Minimum Coded Unit) and its value is contained in DRI (Define Restart Interval) marker. If `V4L2_CID_JPEG_RESTART_INTERVAL` control is set to 0, DRI and RSTm markers will not be inserted.

<a id="rst-jpeg-quality-control"></a>

- **`V4L2_CID_JPEG_COMPRESSION_QUALITY (integer)`**

  Determines trade-off between image quality and size. It provides simpler method for applications to control image quality, without a need for direct reconfiguration of luminance and chrominance quantization tables. In cases where a driver uses quantization tables configured directly by an application, using interfaces defined elsewhere, `V4L2_CID_JPEG_COMPRESSION_QUALITY` control should be set by driver to 0.

  The value range of this control is driver-specific. Only positive, non-zero values are meaningful. The recommended range is 1 - 100, where larger values correspond to better image quality.

<a id="rst-jpeg-active-marker-control"></a>

- **`V4L2_CID_JPEG_ACTIVE_MARKER (bitmask)`**

  Specify which JPEG markers are included in compressed stream. This control is valid only for encoders.


<table>
<tbody>
<tr>
<td>


`V4L2_JPEG_ACTIVE_MARKER_APP0`

</td>
<td>


Application data segment APP<sub>0</sub>.

</td>
</tr>
<tr>
<td>


`V4L2_JPEG_ACTIVE_MARKER_APP1`

</td>
<td>


Application data segment APP<sub>1</sub>.

</td>
</tr>
<tr>
<td>


`V4L2_JPEG_ACTIVE_MARKER_COM`

</td>
<td>


Comment segment.

</td>
</tr>
<tr>
<td>


`V4L2_JPEG_ACTIVE_MARKER_DQT`

</td>
<td>


Quantization tables segment.

</td>
</tr>
<tr>
<td>


`V4L2_JPEG_ACTIVE_MARKER_DHT`

</td>
<td>


Huffman tables segment.

</td>
</tr>
</tbody>
</table>

For more details about JPEG specification, refer to [ITU-T.81](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-itu-t81>), [JFIF](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-jfif-1>), [W3C JPEG JFIF](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-w3c-jpeg-jfif>).
