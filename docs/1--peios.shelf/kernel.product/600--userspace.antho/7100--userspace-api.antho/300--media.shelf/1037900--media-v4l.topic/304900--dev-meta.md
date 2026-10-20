---
title: "Metadata Interface"
type: reference
description: "Metadata refers to any non-image data that supplements video frames with additional information. This may include statistics computed over the image, frame capture parameters supplied by the image source or device specific parameters for…"
---

<a id="rst-metadata-interface"></a>
<a id="rst-metadata"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

Metadata refers to any non-image data that supplements video frames with additional information. This may include statistics computed over the image, frame capture parameters supplied by the image source or device specific parameters for specifying how the device processes images. This interface is intended for transfer of metadata between the userspace and the hardware and control of that operation.

The metadata interface is implemented on video device nodes. The device can be dedicated to metadata or can support both video and metadata as specified in its reported capabilities.

<a id="rst-querying-capabilities"></a>

## Querying Capabilities

Device nodes supporting the metadata capture interface set the `V4L2_CAP_META_CAPTURE` flag in the `device_caps` field of the `v4l2_capability` structure returned by the `VIDIOC_QUERYCAP()` ioctl. That flag means the device can capture metadata to memory. Similarly, device nodes supporting metadata output interface set the `V4L2_CAP_META_OUTPUT` flag in the `device_caps` field of `v4l2_capability` structure. That flag means the device can read metadata from memory.

At least one of the read/write or streaming I/O methods must be supported.

<a id="rst-data-format-negotiation"></a>

## Data Format Negotiation

The metadata device uses the [Data Formats](<~kernel/userspace/userspace-api/media-v4l/format#rst-format>) ioctls to select the capture format. The metadata buffer content format is bound to that selected format. In addition to the basic [Data Formats](<~kernel/userspace/userspace-api/media-v4l/format#rst-format>) ioctls, the `VIDIOC_ENUM_FMT()` ioctl must be supported as well.

To use the [Data Formats](<~kernel/userspace/userspace-api/media-v4l/format#rst-format>) ioctls applications set the `type` field of the `v4l2_format` structure to `V4L2_BUF_TYPE_META_CAPTURE` or to `V4L2_BUF_TYPE_META_OUTPUT` and use the `v4l2_meta_format` `meta` member of the `fmt` union as needed per the desired operation. Both drivers and applications must set the remainder of the `v4l2_format` structure to 0.

Devices that capture metadata by line have the struct v4l2_fmtdesc `V4L2_FMT_FLAG_META_LINE_BASED` flag set for `VIDIOC_ENUM_FMT()`. Such devices can typically also [capture image data](<~kernel/userspace/userspace-api/media-v4l/dev-capture#rst-capture>). This primarily involves devices that receive the data from a different devices such as a camera sensor.





<a id="c-v4l2_meta_format"></a>

```c
v4l2_meta_format
```

<!-- tabularcolumns: |p{1.4cm}|p{2.4cm}|p{13.5cm}| -->


<table>
<caption>struct v4l2_meta_format</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`dataformat`

</td>
<td>


The data format, set by the application. This is a little endian [four character code](<~kernel/userspace/userspace-api/media-v4l/vidioc-enum-fmt#rst-v4l2-fourcc>). V4L2 defines metadata formats in [Metadata Formats](<~kernel/userspace/userspace-api/media-v4l/meta-formats#rst-meta-formats>).

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`buffersize`

</td>
<td>


Maximum buffer size in bytes required for data. The value is set by the driver.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`width`

</td>
<td>


Width of a line of metadata in Data Units. Valid when :c:type\`v4l2_fmtdesc\` flag `V4L2_FMT_FLAG_META_LINE_BASED` is set, otherwise zero. See `VIDIOC_ENUM_FMT()`.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`height`

</td>
<td>


Number of rows of metadata. Valid when :c:type\`v4l2_fmtdesc\` flag `V4L2_FMT_FLAG_META_LINE_BASED` is set, otherwise zero. See `VIDIOC_ENUM_FMT()`.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`bytesperline`

</td>
<td>


Offset in bytes between the beginning of two consecutive lines. Valid when :c:type\`v4l2_fmtdesc\` flag `V4L2_FMT_FLAG_META_LINE_BASED` is set, otherwise zero. See `VIDIOC_ENUM_FMT()`.

</td>
</tr>
</tbody>
</table>
