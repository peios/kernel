---
title: "Single- and multi-planar APIs"
type: reference
description: "Some devices require data for each input or output video frame to be placed in discontiguous memory buffers. In such cases, one video frame has to be addressed using more than one memory address, i.e. one pointer per \"plane\". A plane is a…"
---

<a id="rst-single-and-multi-planar-apis"></a>
<a id="rst-planar-apis"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

Some devices require data for each input or output video frame to be placed in discontiguous memory buffers. In such cases, one video frame has to be addressed using more than one memory address, i.e. one pointer per "plane". A plane is a sub-buffer of the current frame. For examples of such formats see [Image Formats](<~kernel/userspace/userspace-api/media-v4l/pixfmt#rst-pixfmt>).

Initially, V4L2 API did not support multi-planar buffers and a set of extensions has been introduced to handle them. Those extensions constitute what is being referred to as the "multi-planar API".

Some of the V4L2 API calls and structures are interpreted differently, depending on whether single- or multi-planar API is being used. An application can choose whether to use one or the other by passing a corresponding buffer type to its ioctl calls. Multi-planar versions of buffer types are suffixed with an `_MPLANE` string. For a list of available multi-planar buffer types see enum `v4l2_buf_type`.

<a id="rst-multi-planar-formats"></a>

## Multi-planar formats

Multi-planar API introduces new multi-planar formats. Those formats use a separate set of FourCC codes. It is important to distinguish between the multi-planar API and a multi-planar format. Multi-planar API calls can handle all single-planar formats as well (as long as they are passed in multi-planar API structures), while the single-planar API cannot handle multi-planar formats.

<a id="rst-calls-that-distinguish-between-single-and-multi-planar-apis"></a>

## Calls that distinguish between single and multi-planar APIs

- **[VIDIOC_QUERYCAP](<~kernel/userspace/userspace-api/media-v4l/vidioc-querycap#rst-vidioc-querycap>)**

  Two additional multi-planar capabilities are added. They can be set together with non-multi-planar ones for devices that handle both single- and multi-planar formats.

- **[VIDIOC_G_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>), [VIDIOC_S_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>), [VIDIOC_TRY_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>)**

  New structures for describing multi-planar formats are added: struct `v4l2_pix_format_mplane` and struct `v4l2_plane_pix_format`. Drivers may define new multi-planar formats, which have distinct FourCC codes from the existing single-planar ones.

- **[VIDIOC_QBUF](<~kernel/userspace/userspace-api/media-v4l/vidioc-qbuf#rst-vidioc-qbuf>), [VIDIOC_DQBUF](<~kernel/userspace/userspace-api/media-v4l/vidioc-qbuf#rst-vidioc-qbuf>), [VIDIOC_QUERYBUF](<~kernel/userspace/userspace-api/media-v4l/vidioc-querybuf#rst-vidioc-querybuf>)**

  A new struct `v4l2_plane` structure for describing planes is added. Arrays of this structure are passed in the new `m.planes` field of struct `v4l2_buffer`.

- **[VIDIOC_REQBUFS](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-reqbufs.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)**

  Will allocate multi-planar buffers as requested.
