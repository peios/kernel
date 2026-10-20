---
title: "V4L2_META_FMT_UVC ('UVCH')"
type: reference
description: "UVC Payload Header Data"
---

<a id="rst-v4l2-meta-fmt-uvc-uvch"></a>
<a id="rst-v4l2-meta-fmt-uvc"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

UVC Payload Header Data

<a id="rst-description"></a>

## Description

This format describes standard UVC metadata, extracted from UVC packet headers and provided by the UVC driver through metadata video nodes. That data includes exact copies of the standard part of UVC Payload Header contents and auxiliary timing information, required for precise interpretation of timestamps, contained in those headers. See section "2.4.3.3 Video and Still Image Payload Headers" of the "UVC 1.5 Class specification" for details.

Each UVC payload header can be between 2 and 12 bytes large. Buffers can contain multiple headers, if multiple such headers have been transmitted by the camera for the respective frame. However, the driver may drop headers when the buffer is full, when they contain no useful information (e.g. those without the SCR field or with that field identical to the previous header), or generally to perform rate limiting when the device sends a large number of headers.

Each individual block contains the following fields:


<table>
<caption>UVC Metadata Block</caption>
<thead>
<tr>
<th>


Field

</th>
<th>


Description

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


\__u64 ts;

</td>
<td>


system timestamp in host byte order, measured by the driver upon reception of the payload

</td>
</tr>
<tr>
<td>


\__u16 sof;

</td>
<td>


USB Frame Number in host byte order, also obtained by the driver as close as possible to the above timestamp to enable correlation between them

</td>
</tr>
<tr>
<td colspan="2">


 *The rest is an exact copy of the UVC payload header:*

</td>
</tr>
<tr>
<td>


\__u8 length;

</td>
<td>


length of the rest of the block, including this field. Please note that regardless of this value, for V4L2_META_FMT_UVC the kernel will never copy more than 2-12 bytes.

</td>
</tr>
<tr>
<td>


\__u8 flags;

</td>
<td>


Flags, indicating presence of other standard UVC fields

</td>
</tr>
<tr>
<td>


\__u8 buf\[\];

</td>
<td>


The rest of the header, possibly including UVC PTS and SCR fields

</td>
</tr>
</tbody>
</table>
