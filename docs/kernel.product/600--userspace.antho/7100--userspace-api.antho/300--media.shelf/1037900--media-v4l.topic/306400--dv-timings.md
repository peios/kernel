---
title: "Digital Video (DV) Timings"
type: reference
description: "The video standards discussed so far have been dealing with Analog TV and the corresponding video timings. Today there are many more different hardware interfaces such as High Definition TV interfaces (HDMI), VGA, DVI connectors etc., that…"
---

<a id="rst-digital-video-dv-timings"></a>
<a id="rst-dv-timings"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

The video standards discussed so far have been dealing with Analog TV and the corresponding video timings. Today there are many more different hardware interfaces such as High Definition TV interfaces (HDMI), VGA, DVI connectors etc., that carry video signals and there is a need to extend the API to select the video timings for these interfaces. Since it is not possible to extend the [v4l2_std_id](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-enumstd.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) due to the limited bits available, a new set of ioctls was added to set/get video timings at the input and output.

These ioctls deal with the detailed digital video timings that define each video format. This includes parameters such as the active video width and height, signal polarities, frontporches, backporches, sync widths etc. The `linux/v4l2-dv-timings.h` header can be used to get the timings of the formats in the [CEA-861-E](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-cea861>) and [VESA DMT](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-vesadmt>) standards.

To enumerate and query the attributes of the DV timings supported by a device applications use the [ioctl VIDIOC_ENUM_DV_TIMINGS, VIDIOC_SUBDEV_ENUM_DV_TIMINGS](<~kernel/userspace/userspace-api/media-v4l/vidioc-enum-dv-timings#rst-vidioc-enum-dv-timings>) and [ioctl VIDIOC_DV_TIMINGS_CAP, VIDIOC_SUBDEV_DV_TIMINGS_CAP](<~kernel/userspace/userspace-api/media-v4l/vidioc-dv-timings-cap#rst-vidioc-dv-timings-cap>) ioctls. To set DV timings for the device applications use the [VIDIOC_S_DV_TIMINGS](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-dv-timings#rst-vidioc-g-dv-timings>) ioctl and to get current DV timings they use the [VIDIOC_G_DV_TIMINGS](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-dv-timings#rst-vidioc-g-dv-timings>) ioctl. To detect the DV timings as seen by the video receiver applications use the [ioctl VIDIOC_QUERY_DV_TIMINGS](<~kernel/userspace/userspace-api/media-v4l/vidioc-query-dv-timings#rst-vidioc-query-dv-timings>) ioctl.

When the hardware detects a video source change (e.g. the video signal appears or disappears, or the video resolution changes), then it will issue a `V4L2_EVENT_SOURCE_CHANGE` event. Use the [ioctl VIDIOC_SUBSCRIBE_EVENT](<~kernel/userspace/userspace-api/media-v4l/vidioc-subscribe-event#rst-vidioc-subscribe-event>) and the [ioctl VIDIOC_DQEVENT](<~kernel/userspace/userspace-api/media-v4l/vidioc-dqevent#rst-vidioc-dqevent>) to check if this event was reported.

If the video signal changed, then the application has to stop streaming, free all buffers, and call the [ioctl VIDIOC_QUERY_DV_TIMINGS](<~kernel/userspace/userspace-api/media-v4l/vidioc-query-dv-timings#rst-vidioc-query-dv-timings>) to obtain the new video timings, and if they are valid, it can set those by calling the [ioctl VIDIOC_S_DV_TIMINGS](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-dv-timings#rst-vidioc-g-dv-timings>). This will also update the format, so use the [ioctl VIDIOC_G_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) to obtain the new format. Now the application can allocate new buffers and start streaming again.

The [ioctl VIDIOC_QUERY_DV_TIMINGS](<~kernel/userspace/userspace-api/media-v4l/vidioc-query-dv-timings#rst-vidioc-query-dv-timings>) will just report what the hardware detects, it will never change the configuration. If the currently set timings and the actually detected timings differ, then typically this will mean that you will not be able to capture any video. The correct approach is to rely on the `V4L2_EVENT_SOURCE_CHANGE` event so you know when something changed.

Applications can make use of the [input-capabilities](<~kernel/userspace/userspace-api/media-v4l/vidioc-enuminput#rst-input-capabilities>) and [output-capabilities](<~kernel/userspace/userspace-api/media-v4l/vidioc-enumoutput#rst-output-capabilities>) flags to determine whether the digital video ioctls can be used with the given input or output.
