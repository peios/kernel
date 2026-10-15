---
title: "Video Output Interface"
type: reference
description: "Video output devices encode stills or image sequences as analog video signal. With this interface applications can control the encoding process and move images from user space to the driver."
---

<a id="rst-video-output-interface"></a>
<a id="rst-output"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

Video output devices encode stills or image sequences as analog video signal. With this interface applications can control the encoding process and move images from user space to the driver.

Conventionally V4L2 video output devices are accessed through character device special files named `/dev/video` and `/dev/video0` to `/dev/video63` with major number 81 and minor numbers 0 to 63. `/dev/video` is typically a symbolic link to the preferred video device.

> [!NOTE]
>
> The same device file names are used also for video capture devices.

<a id="rst-querying-capabilities"></a>

## Querying Capabilities

Devices supporting the video output interface set the `V4L2_CAP_VIDEO_OUTPUT` or `V4L2_CAP_VIDEO_OUTPUT_MPLANE` flag in the `capabilities` field of struct `v4l2_capability` returned by the [ioctl VIDIOC_QUERYCAP](<~kernel/userspace/userspace-api/media-v4l/vidioc-querycap#rst-vidioc-querycap>) ioctl. As secondary device functions they may also support the [raw VBI output](<~kernel/userspace/userspace-api/media-v4l/dev-raw-vbi#rst-raw-vbi>) (`V4L2_CAP_VBI_OUTPUT`) interface. At least one of the read/write or streaming I/O methods must be supported. Modulators and audio outputs are optional.

<a id="rst-supplemental-functions"></a>

## Supplemental Functions

Video output devices shall support [audio output](<~kernel/userspace/userspace-api/media-v4l/audio#rst-audio>), [modulator](<~kernel/userspace/userspace-api/media-v4l/tuner#rst-tuner>), [controls](<~kernel/userspace/userspace-api/media-v4l/control#rst-control>), [cropping and scaling](<~kernel/userspace/userspace-api/media-v4l/crop#rst-crop>) and [streaming parameter](<~kernel/userspace/userspace-api/media-v4l/streaming-par#rst-streaming-par>) ioctls as needed. The [video output](<~kernel/userspace/userspace-api/media-v4l/video#rst-video>) ioctls must be supported by all video output devices.

<a id="rst-image-format-negotiation"></a>

## Image Format Negotiation

The output is determined by cropping and image format parameters. The former select an area of the video picture where the image will appear, the latter how images are stored in memory, i. e. in RGB or YUV format, the number of bits per pixel or width and height. Together they also define how images are scaled in the process.

As usual these parameters are *not* reset at `open()` time to permit Unix tool chains, programming a device and then writing to it as if it was a plain file. Well written V4L2 applications ensure they really get what they want, including cropping and scaling.

Cropping initialization at minimum requires to reset the parameters to defaults. An example is given in [Image Cropping, Insertion and Scaling -- the CROP API](<~kernel/userspace/userspace-api/media-v4l/crop#rst-crop>).

To query the current image format applications set the `type` field of a struct `v4l2_format` to `V4L2_BUF_TYPE_VIDEO_OUTPUT` or `V4L2_BUF_TYPE_VIDEO_OUTPUT_MPLANE` and call the [VIDIOC_G_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) ioctl with a pointer to this structure. Drivers fill the struct `v4l2_pix_format` `pix` or the struct `v4l2_pix_format_mplane` `pix_mp` member of the `fmt` union.

To request different parameters applications set the `type` field of a struct `v4l2_format` as above and initialize all fields of the struct `v4l2_pix_format` `vbi` member of the `fmt` union, or better just modify the results of [VIDIOC_G_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>), and call the [VIDIOC_S_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) ioctl with a pointer to this structure. Drivers may adjust the parameters and finally return the actual parameters as [VIDIOC_G_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) does.

Like [VIDIOC_S_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) the [VIDIOC_TRY_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) ioctl can be used to learn about hardware limitations without disabling I/O or possibly time consuming hardware preparations.

The contents of struct `v4l2_pix_format` and struct `v4l2_pix_format_mplane` are discussed in [Image Formats](<~kernel/userspace/userspace-api/media-v4l/pixfmt#rst-pixfmt>). See also the specification of the [VIDIOC_G_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>), [VIDIOC_S_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) and [VIDIOC_TRY_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) ioctls for details. Video output devices must implement both the [VIDIOC_G_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) and [VIDIOC_S_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) ioctl, even if [VIDIOC_S_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) ignores all requests and always returns default parameters as [VIDIOC_G_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) does. [VIDIOC_TRY_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) is optional.

<a id="rst-writing-images"></a>

## Writing Images

A video output device may support the [write() function](<~kernel/userspace/userspace-api/media-v4l/rw#rst-rw>) and/or streaming ([memory mapping](<~kernel/userspace/userspace-api/media-v4l/mmap#rst-mmap>) or [user pointer](<~kernel/userspace/userspace-api/media-v4l/userp#rst-userp>)) I/O. See [Input/Output](<~kernel/userspace/userspace-api/media-v4l/io#rst-io>) for details.
