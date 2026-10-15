---
title: "Video Memory-To-Memory Interface"
type: reference
description: "A V4L2 memory-to-memory device can compress, decompress, transform, or otherwise convert video data from one format into another format, in memory. Such memory-to-memory devices set the V4L2_CAP_VIDEO_M2M or V4L2_CAP_VIDEO_M2M_MPLANE…"
---

<a id="rst-video-memory-to-memory-interface"></a>
<a id="rst-mem2mem"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

A V4L2 memory-to-memory device can compress, decompress, transform, or otherwise convert video data from one format into another format, in memory. Such memory-to-memory devices set the `V4L2_CAP_VIDEO_M2M` or `V4L2_CAP_VIDEO_M2M_MPLANE` capability. Examples of memory-to-memory devices are codecs, scalers, deinterlacers or format converters (i.e. converting from YUV to RGB).

A memory-to-memory video node acts just like a normal video node, but it supports both output (sending frames from memory to the hardware) and capture (receiving the processed frames from the hardware into memory) stream I/O. An application will have to setup the stream I/O for both sides and finally call [VIDIOC_STREAMON](<~kernel/userspace/userspace-api/media-v4l/vidioc-streamon#rst-vidioc-streamon>) for both capture and output to start the hardware.

Memory-to-memory devices function as a shared resource: you can open the video node multiple times, each application setting up their own properties that are local to the file handle, and each can use it independently from the others. The driver will arbitrate access to the hardware and reprogram it whenever another file handler gets access. This is different from the usual video node behavior where the video properties are global to the device (i.e. changing something through one file handle is visible through another file handle).

One of the most common memory-to-memory device is the codec. Codecs are more complicated than most and require additional setup for their codec parameters. This is done through codec controls. See [codec-controls](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/ext-ctrls-codec.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>). More details on how to use codec memory-to-memory devices are given in the following sections.

- [Memory-to-Memory Stateful Video Decoder Interface](<~kernel/userspace/userspace-api/media-v4l/dev-decoder>)
- [Memory-to-Memory Stateful Video Encoder Interface](<~kernel/userspace/userspace-api/media-v4l/dev-encoder>)
- [Memory-to-memory Stateless Video Decoder Interface](<~kernel/userspace/userspace-api/media-v4l/dev-stateless-decoder>)
