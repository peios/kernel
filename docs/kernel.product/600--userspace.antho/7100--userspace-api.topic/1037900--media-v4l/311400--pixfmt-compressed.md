---
title: "Compressed Formats"
type: reference
description: "Reference for Compressed Formats."
---

<a id="rst-compressed-formats"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-compressed-formats-1"></a>



<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{5.8cm}|p{1.2cm}|p{10.3cm}| -->


<table>
<caption>

Compressed Image Formats

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



Details

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



`V4L2_PIX_FMT_JPEG`

</td>
<td>



'JPEG'

</td>
<td>



<a id="rst-v4l2-pix-fmt-jpeg"></a>

TBD. See also [VIDIOC\_G\_JPEGCOMP](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-jpegcomp#rst-vidioc-g-jpegcomp>), [VIDIOC\_S\_JPEGCOMP](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-jpegcomp#rst-vidioc-g-jpegcomp>).

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_MPEG`

</td>
<td>



'MPEG'

</td>
<td>



<a id="rst-v4l2-pix-fmt-mpeg"></a>

MPEG multiplexed stream. The actual format is determined by extended control `V4L2_CID_MPEG_STREAM_TYPE`, see [Codec Control IDs](<~kernel/userspace/userspace-api/media-v4l/ext-ctrls-codec#rst-mpeg-control-id>).

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_H264`

</td>
<td>



'H264'

</td>
<td>



<a id="rst-v4l2-pix-fmt-h264"></a>

H264 Access Unit. The decoder expects one Access Unit per buffer. The encoder generates one Access Unit per buffer. If [vidioc\_enum\_fmt](<~kernel/userspace/userspace-api/media-v4l/vidioc-enum-fmt#rst-vidioc-enum-fmt>) reports `V4L2_FMT_FLAG_CONTINUOUS_BYTESTREAM` then the decoder has no requirements since it can parse all the information from the raw bytestream.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_H264_NO_SC`

</td>
<td>



'AVC1'

</td>
<td>



<a id="rst-v4l2-pix-fmt-h264-no-sc"></a>

H264 video elementary stream without start codes.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_H264_MVC`

</td>
<td>



'M264'

</td>
<td>



<a id="rst-v4l2-pix-fmt-h264-mvc"></a>

H264 MVC video elementary stream.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_H264_SLICE`

</td>
<td>



'S264'

</td>
<td>



<a id="rst-v4l2-pix-fmt-h264-slice"></a>

H264 parsed slice data, including slice headers, either with or without the start code, as extracted from the H264 bitstream. This format is adapted for stateless video decoders that implement an H264 pipeline with the [stateless\_decoder](<~kernel/userspace/userspace-api/media-v4l/dev-stateless-decoder#rst-stateless-decoder>). This pixelformat has two modifiers that must be set at least once through the `V4L2_CID_STATELESS_H264_DECODE_MODE` and `V4L2_CID_STATELESS_H264_START_CODE` controls. In addition, metadata associated with the frame to decode are required to be passed through the `V4L2_CID_STATELESS_H264_SPS`, `V4L2_CID_STATELESS_H264_PPS`, `V4L2_CID_STATELESS_H264_SCALING_MATRIX`, `V4L2_CID_STATELESS_H264_SLICE_PARAMS` and `V4L2_CID_STATELESS_H264_DECODE_PARAMS` controls.  See the [associated Codec Control IDs](<~kernel/userspace/userspace-api/media-v4l/ext-ctrls-codec-stateless#rst-v4l2-codec-stateless-h264>). Exactly one output and one capture buffer must be provided for use with this pixel format. The output buffer must contain the appropriate number of macroblocks to decode a full corresponding frame to the matching capture buffer.

The syntax for this format is documented in [h264](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-h264>), section 7.3.2.8 "Slice layer without partitioning RBSP syntax" and the following sections.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_H263`

</td>
<td>



'H263'

</td>
<td>



<a id="rst-v4l2-pix-fmt-h263"></a>

H263 video elementary stream.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_SPK`

</td>
<td>



'SPK0'

</td>
<td>



<a id="rst-v4l2-pix-fmt-spk"></a>

Sorenson Spark is an implementation of H.263 for use in Flash Video and Adobe Flash files

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_MPEG1`

</td>
<td>



'MPG1'

</td>
<td>



<a id="rst-v4l2-pix-fmt-mpeg1"></a>

MPEG1 Picture. Each buffer starts with a Picture header, followed by other headers as needed and ending with the Picture data. If [vidioc\_enum\_fmt](<~kernel/userspace/userspace-api/media-v4l/vidioc-enum-fmt#rst-vidioc-enum-fmt>) reports `V4L2_FMT_FLAG_CONTINUOUS_BYTESTREAM` then the decoder has no requirements since it can parse all the information from the raw bytestream.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_MPEG2`

</td>
<td>



'MPG2'

</td>
<td>



<a id="rst-v4l2-pix-fmt-mpeg2"></a>

MPEG2 Picture. Each buffer starts with a Picture header, followed by other headers as needed and ending with the Picture data. If [vidioc\_enum\_fmt](<~kernel/userspace/userspace-api/media-v4l/vidioc-enum-fmt#rst-vidioc-enum-fmt>) reports `V4L2_FMT_FLAG_CONTINUOUS_BYTESTREAM` then the decoder has no requirements since it can parse all the information from the raw bytestream.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_MPEG2_SLICE`

</td>
<td>



'MG2S'

</td>
<td>



<a id="rst-v4l2-pix-fmt-mpeg2-slice"></a>

MPEG-2 parsed slice data, as extracted from the MPEG-2 bitstream. This format is adapted for stateless video decoders that implement a MPEG-2 pipeline with the [stateless\_decoder](<~kernel/userspace/userspace-api/media-v4l/dev-stateless-decoder#rst-stateless-decoder>). Metadata associated with the frame to decode is required to be passed through the `V4L2_CID_STATELESS_MPEG2_SEQUENCE` and `V4L2_CID_STATELESS_MPEG2_PICTURE` controls. Quantisation matrices can optionally be specified through the `V4L2_CID_STATELESS_MPEG2_QUANTISATION` control. See the [associated Codec Control IDs](<~kernel/userspace/userspace-api/media-v4l/ext-ctrls-codec-stateless#rst-v4l2-codec-stateless-mpeg2>). Exactly one output and one capture buffer must be provided for use with this pixel format. The output buffer must contain the appropriate number of macroblocks to decode a full corresponding frame to the matching capture buffer.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_MPEG4`

</td>
<td>



'MPG4'

</td>
<td>



<a id="rst-v4l2-pix-fmt-mpeg4"></a>

MPEG4 video elementary stream.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_XVID`

</td>
<td>



'XVID'

</td>
<td>



<a id="rst-v4l2-pix-fmt-xvid"></a>

Xvid video elementary stream.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_VC1_ANNEX_G`

</td>
<td>



'VC1G'

</td>
<td>



<a id="rst-v4l2-pix-fmt-vc1-annex-g"></a>

VC1, SMPTE 421M Annex G compliant stream.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_VC1_ANNEX_L`

</td>
<td>



'VC1L'

</td>
<td>



<a id="rst-v4l2-pix-fmt-vc1-annex-l"></a>

VC1, SMPTE 421M Annex L compliant stream.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_VP8`

</td>
<td>



'VP80'

</td>
<td>



<a id="rst-v4l2-pix-fmt-vp8"></a>

VP8 compressed video frame. The encoder generates one compressed frame per buffer, and the decoder requires one compressed frame per buffer.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_VP8_FRAME`

</td>
<td>



'VP8F'

</td>
<td>



<a id="rst-v4l2-pix-fmt-vp8-frame"></a>

VP8 parsed frame, including the frame header, as extracted from the container. This format is adapted for stateless video decoders that implement an VP8 pipeline with the [stateless\_decoder](<~kernel/userspace/userspace-api/media-v4l/dev-stateless-decoder#rst-stateless-decoder>). Metadata associated with the frame to decode is required to be passed through the `V4L2_CID_STATELESS_VP8_FRAME` control. See the [associated Codec Control IDs](<~kernel/userspace/userspace-api/media-v4l/ext-ctrls-codec-stateless#rst-v4l2-codec-stateless-vp8>). Exactly one output and one capture buffer must be provided for use with this pixel format. The output buffer must contain the appropriate number of macroblocks to decode a full corresponding frame to the matching capture buffer.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_VP9`

</td>
<td>



'VP90'

</td>
<td>



<a id="rst-v4l2-pix-fmt-vp9"></a>

VP9 compressed video frame. The encoder generates one compressed frame per buffer, and the decoder requires one compressed frame per buffer.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_VP9_FRAME`

</td>
<td>



'VP9F'

</td>
<td>



<a id="rst-v4l2-pix-fmt-vp9-frame"></a>

VP9 parsed frame, including the frame header, as extracted from the container. This format is adapted for stateless video decoders that implement a VP9 pipeline with the [stateless\_decoder](<~kernel/userspace/userspace-api/media-v4l/dev-stateless-decoder#rst-stateless-decoder>). Metadata associated with the frame to decode is required to be passed through the `V4L2_CID_STATELESS_VP9_FRAME` and the `V4L2_CID_STATELESS_VP9_COMPRESSED_HDR` controls. See the [associated Codec Control IDs](<~kernel/userspace/userspace-api/media-v4l/ext-ctrls-codec-stateless#rst-v4l2-codec-stateless-vp9>). Exactly one output and one capture buffer must be provided for use with this pixel format. The output buffer must contain the appropriate number of macroblocks to decode a full corresponding frame to the matching capture buffer.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_HEVC`

</td>
<td>



'HEVC'

</td>
<td>



<a id="rst-v4l2-pix-fmt-hevc"></a>

HEVC/H.265 Access Unit. The decoder expects one Access Unit per buffer. The encoder generates one Access Unit per buffer. If [vidioc\_enum\_fmt](<~kernel/userspace/userspace-api/media-v4l/vidioc-enum-fmt#rst-vidioc-enum-fmt>) reports `V4L2_FMT_FLAG_CONTINUOUS_BYTESTREAM` then the decoder has no requirements since it can parse all the information from the raw bytestream.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_HEVC_SLICE`

</td>
<td>



'S265'

</td>
<td>



<a id="rst-v4l2-pix-fmt-hevc-slice"></a>

HEVC parsed slice data, as extracted from the HEVC bitstream. This format is adapted for stateless video decoders that implement a HEVC pipeline (using the [mem2mem](<~kernel/userspace/userspace-api/media-v4l/dev-mem2mem#rst-mem2mem>) and [media-request-api](<~kernel/userspace/userspace-api/media-mediactl/request-api#rst-media-request-api>)). This pixelformat has two modifiers that must be set at least once through the `V4L2_CID_MPEG_VIDEO_HEVC_DECODE_MODE` and `V4L2_CID_MPEG_VIDEO_HEVC_START_CODE` controls. Metadata associated with the frame to decode is required to be passed through the following controls: `V4L2_CID_MPEG_VIDEO_HEVC_SPS`, `V4L2_CID_MPEG_VIDEO_HEVC_PPS`, and `V4L2_CID_MPEG_VIDEO_HEVC_SLICE_PARAMS`. See the [associated Codec Control IDs](<~kernel/userspace/userspace-api/media-v4l/ext-ctrls-codec-stateless#rst-v4l2-codec-stateless-hevc>). Buffers associated with this pixel format must contain the appropriate number of macroblocks to decode a full corresponding frame.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_FWHT`

</td>
<td>



'FWHT'

</td>
<td>



<a id="rst-v4l2-pix-fmt-fwht"></a>

Video elementary stream using a codec based on the Fast Walsh Hadamard Transform. This codec is implemented by the vicodec ('Virtual Codec') driver. See the codec-fwht.h header for more details. [vidioc\_enum\_fmt](<~kernel/userspace/userspace-api/media-v4l/vidioc-enum-fmt#rst-vidioc-enum-fmt>) reports `V4L2_FMT_FLAG_CONTINUOUS_BYTESTREAM` since the decoder can parse all the information from the raw bytestream.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_FWHT_STATELESS`

</td>
<td>



'SFWH'

</td>
<td>



<a id="rst-v4l2-pix-fmt-fwht-stateless"></a>

Same format as V4L2\_PIX\_FMT\_FWHT but requires stateless codec implementation. Metadata associated with the frame to decode is required to be passed through the `V4L2_CID_STATELESS_FWHT_PARAMS` control. See the [associated Codec Control ID](<~kernel/userspace/userspace-api/media-v4l/ext-ctrls-codec-stateless#rst-codec-stateless-fwht>).

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_RV30`

</td>
<td>



'RV30'

</td>
<td>



<a id="rst-v4l2-pix-fmt-rv30"></a>

RealVideo, or also spelled as Real Video, is a suite of proprietary video compression formats developed by RealNetworks - the specific format changes with the version. RealVideo codecs are identified by four-character codes. RV30 corresponds to RealVideo 8, suspected to be based largely on an early draft of H.264

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_RV40`

</td>
<td>



'RV40'

</td>
<td>



<a id="rst-v4l2-pix-fmt-rv40"></a>

RV40 represents RealVideo 9 and RealVideo 10. RealVideo 9, suspected to be based on H.264. RealVideo 10, aka RV9 EHQ, This refers to an improved encoder for the RV9 format that is fully backwards compatible with RV9 players - the format and decoder did not change, only the encoder did. As a result, it uses the same FourCC.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_AV1_FRAME`

</td>
<td>



'AV1F'

</td>
<td>



<a id="rst-v4l2-pix-fmt-av1-frame"></a>

AV1 parsed frame, including the frame header, as extracted from the container. This format is adapted for stateless video decoders that implement a AV1 pipeline with the [stateless\_decoder](<~kernel/userspace/userspace-api/media-v4l/dev-stateless-decoder#rst-stateless-decoder>). Metadata associated with the frame to decode is required to be passed through the `V4L2_CID_STATELESS_AV1_SEQUENCE`, `V4L2_CID_STATELESS_AV1_FRAME`, and `V4L2_CID_STATELESS_AV1_TILE_GROUP_ENTRY` controls. See the [associated Codec Control IDs](<~kernel/userspace/userspace-api/media-v4l/ext-ctrls-codec-stateless#rst-v4l2-codec-stateless-av1>). Exactly one output and one capture buffer must be provided for use with this pixel format. The output buffer must contain the appropriate number of macroblocks to decode a full corresponding frame to the matching capture buffer.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_AV1`

</td>
<td>



'AV01'

</td>
<td>



<a id="rst-v4l2-pix-fmt-av1"></a>

AV1 compressed video frame. This format is adapted for implementing AV1 pipeline. The decoder implements stateful video decoder and expects one temporal unit per buffer in OBU stream format. The encoder generates one Temporal Unit per buffer.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->
