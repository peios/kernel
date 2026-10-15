---
title: "ASPEED video driver"
type: reference
description: "ASPEED Video Engine found on AST2400/2500/2600 SoC supports high performance video compressions with a wide range of video quality and compression ratio options. The adopted compressing algorithm is a modified JPEG algorithm."
---

<a id="rst-aspeed-video-driver"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<!-- This data file has been placed in the public domain. -->

<!-- Derived from the Unicode character mappings available from
<http://www.w3.org/2003/entities/xml/>.
Processed by unicode2rstsubs.py, part of Docutils:
<https://docutils.sourceforge.io>. -->

ASPEED Video Engine found on AST2400/2500/2600 SoC supports high performance video compressions with a wide range of video quality and compression ratio options. The adopted compressing algorithm is a modified JPEG algorithm.

There are 2 types of compressions in this IP.

- JPEG JFIF standard mode: for single frame and management compression

- ASPEED proprietary mode: for multi-frame and differential compression. Support 2-pass (high quality) video compression scheme (Patent pending by ASPEED). Provide visually lossless video compression quality or to reduce the network average loading under intranet KVM applications.

VIDIOC_S_FMT can be used to choose which format you want. V4L2_PIX_FMT_JPEG stands for JPEG JFIF standard mode; V4L2_PIX_FMT_AJPG stands for ASPEED proprietary mode.

More details on the ASPEED video hardware operations can be found in *chapter 6.2.16 KVM Video Driver* of SDK_User_Guide which available on [github](<https://github.com/AspeedTech-BMC/openbmc/releases/>).

The ASPEED video driver implements the following driver-specific control:

<a id="rst-v4l2-cid-aspeed-hq-mode"></a>

## `V4L2_CID_ASPEED_HQ_MODE`

> Enable/Disable ASPEED's High quality mode. This is a private control that can be used to enable high quality for aspeed proprietary mode.


<table>
<tbody>
<tr>
<td>


`(0)`

</td>
<td>


ASPEED HQ mode is disabled.

</td>
</tr>
<tr>
<td>


`(1)`

</td>
<td>


ASPEED HQ mode is enabled.

</td>
</tr>
</tbody>
</table>

<a id="rst-v4l2-cid-aspeed-hq-jpeg-quality"></a>

## `V4L2_CID_ASPEED_HQ_JPEG_QUALITY`

> Define the quality of ASPEED's High quality mode. This is a private control that can be used to decide compression quality if High quality mode enabled . Higher the value, better the quality and bigger the size.


<table>
<tbody>
<tr>
<td>


`(1)`

</td>
<td>


minimum

</td>
</tr>
<tr>
<td>


`(12)`

</td>
<td>


maximum

</td>
</tr>
<tr>
<td>


`(1)`

</td>
<td>


step

</td>
</tr>
<tr>
<td>


`(1)`

</td>
<td>


default

</td>
</tr>
</tbody>
</table>

**Copyright** © 2022 ASPEED Technology Inc.
