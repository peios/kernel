---
title: "ioctl VIDIOC_G_PARM, VIDIOC_S_PARM"
type: reference
description: "VIDIOC_G_PARM - VIDIOC_S_PARM - Get or set streaming parameters"
---

<a id="rst-ioctl-vidioc-g-parm-vidioc-s-parm"></a>
<a id="rst-vidioc-g-parm"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_G_PARM - VIDIOC_S_PARM - Get or set streaming parameters

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_G_PARM"></a>

```c
VIDIOC_G_PARM
```

`int ioctl(int fd, VIDIOC_G_PARM, v4l2_streamparm *argp)`





<a id="c-VIDIOC_S_PARM"></a>

```c
VIDIOC_S_PARM
```

`int ioctl(int fd, VIDIOC_S_PARM, v4l2_streamparm *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_streamparm`.

<a id="rst-description"></a>

## Description

Applications can request a different frame interval. The capture or output device will be reconfigured to support the requested frame interval if possible. Optionally drivers may choose to skip or repeat frames to achieve the requested frame interval.

For stateful encoders (see [Memory-to-Memory Stateful Video Encoder Interface](<~kernel/userspace/userspace-api/media-v4l/dev-encoder#rst-encoder>)) this represents the frame interval that is typically embedded in the encoded video stream.

Changing the frame interval shall never change the format. Changing the format, on the other hand, may change the frame interval.

Further these ioctls can be used to determine the number of buffers used internally by a driver in read/write mode. For implications see the section discussing the `read()` function.

To get and set the streaming parameters applications call the [VIDIOC_G_PARM](<#rst-vidioc-g-parm>) and [VIDIOC_S_PARM](<#rst-vidioc-g-parm>) ioctl, respectively. They take a pointer to a struct `v4l2_streamparm` which contains a union holding separate parameters for input and output devices.

<!-- tabularcolumns: |p{3.7cm}|p{3.5cm}|p{10.1cm}| -->





<a id="c-v4l2_streamparm"></a>

```c
v4l2_streamparm
```


<table>
<caption>struct v4l2_streamparm</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`type`

</td>
<td>


The buffer (stream) type, same as struct `v4l2_format` `type`, set by the application. See `v4l2_buf_type`.

</td>
</tr>
<tr>
<td>


union \{

</td>
<td colspan="2">


`parm`

</td>
</tr>
<tr>
<td>


struct `v4l2_captureparm`

</td>
<td>


`capture`

</td>
<td>


Parameters for capture devices, used when `type` is `V4L2_BUF_TYPE_VIDEO_CAPTURE` or `V4L2_BUF_TYPE_VIDEO_CAPTURE_MPLANE`.

</td>
</tr>
<tr>
<td>


struct `v4l2_outputparm`

</td>
<td>


`output`

</td>
<td>


Parameters for output devices, used when `type` is `V4L2_BUF_TYPE_VIDEO_OUTPUT` or `V4L2_BUF_TYPE_VIDEO_OUTPUT_MPLANE`.

</td>
</tr>
<tr>
<td>


\__u8

</td>
<td>


`raw_data`\[200\]

</td>
<td>


A place holder for future extensions.

</td>
</tr>
<tr>
<td colspan="3">


\}

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->





<a id="c-v4l2_captureparm"></a>

```c
v4l2_captureparm
```


<table>
<caption>struct v4l2_captureparm</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`capability`

</td>
<td>


See [parm-caps](<#rst-parm-caps>).

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`capturemode`

</td>
<td>


Set by drivers and applications, see [parm-flags](<#rst-parm-flags>).

</td>
</tr>
<tr>
<td>


struct `v4l2_fract`

</td>
<td>


`timeperframe`

</td>
<td>


This is the desired period between successive frames captured by the driver, in seconds.

</td>
</tr>
<tr>
<td colspan="3">


This will configure the speed at which the video source (e.g. a sensor) generates video frames. If the speed is fixed, then the driver may choose to skip or repeat frames in order to achieve the requested frame rate.

For stateful encoders (see [Memory-to-Memory Stateful Video Encoder Interface](<~kernel/userspace/userspace-api/media-v4l/dev-encoder#rst-encoder>)) this represents the frame interval that is typically embedded in the encoded video stream.

Applications store here the desired frame period, drivers return the actual frame period.

Changing the video standard (also implicitly by switching the video input) may reset this parameter to the nominal frame period. To reset manually applications can just set this field to zero.

Drivers support this function only when they set the `V4L2_CAP_TIMEPERFRAME` flag in the `capability` field.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`extendedmode`

</td>
<td>


Custom (driver specific) streaming parameters. When unused, applications and drivers must set this field to zero. Applications using this field should check the driver name and version, see [Querying Capabilities](<~kernel/userspace/userspace-api/media-v4l/querycap#rst-querycap>).

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`readbuffers`

</td>
<td>


Applications set this field to the desired number of buffers used internally by the driver in `read()` mode. Drivers return the actual number of buffers. When an application requests zero buffers, drivers should just return the current setting rather than the minimum or an error code. For details see [Read/Write](<~kernel/userspace/userspace-api/media-v4l/rw#rst-rw>).

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`reserved`\[4\]

</td>
<td>


Reserved for future extensions. Drivers and applications must set the array to zero.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->





<a id="c-v4l2_outputparm"></a>

```c
v4l2_outputparm
```


<table>
<caption>struct v4l2_outputparm</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`capability`

</td>
<td>


See [parm-caps](<#rst-parm-caps>).

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`outputmode`

</td>
<td>


Set by drivers and applications, see [parm-flags](<#rst-parm-flags>).

</td>
</tr>
<tr>
<td>


struct `v4l2_fract`

</td>
<td>


`timeperframe`

</td>
<td>


This is the desired period between successive frames output by the driver, in seconds.

</td>
</tr>
<tr>
<td colspan="3">


The field is intended to repeat frames on the driver side in `write()` mode (in streaming mode timestamps can be used to throttle the output), saving I/O bandwidth.

For stateful encoders (see [Memory-to-Memory Stateful Video Encoder Interface](<~kernel/userspace/userspace-api/media-v4l/dev-encoder#rst-encoder>)) this represents the frame interval that is typically embedded in the encoded video stream and it provides a hint to the encoder of the speed at which raw frames are queued up to the encoder.

Applications store here the desired frame period, drivers return the actual frame period.

Changing the video standard (also implicitly by switching the video output) may reset this parameter to the nominal frame period. To reset manually applications can just set this field to zero.

Drivers support this function only when they set the `V4L2_CAP_TIMEPERFRAME` flag in the `capability` field.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`extendedmode`

</td>
<td>


Custom (driver specific) streaming parameters. When unused, applications and drivers must set this field to zero. Applications using this field should check the driver name and version, see [Querying Capabilities](<~kernel/userspace/userspace-api/media-v4l/querycap#rst-querycap>).

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`writebuffers`

</td>
<td>


Applications set this field to the desired number of buffers used internally by the driver in `write()` mode. Drivers return the actual number of buffers. When an application requests zero buffers, drivers should just return the current setting rather than the minimum or an error code. For details see [Read/Write](<~kernel/userspace/userspace-api/media-v4l/rw#rst-rw>).

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`reserved`\[4\]

</td>
<td>


Reserved for future extensions. Drivers and applications must set the array to zero.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{6.6cm}|p{2.2cm}|p{8.5cm}| -->

<a id="rst-parm-caps"></a>


<table>
<caption>Streaming Parameters Capabilities</caption>
<tbody>
<tr>
<td>


`V4L2_CAP_TIMEPERFRAME`

</td>
<td>


0x1000

</td>
<td>


The frame period can be modified by setting the `timeperframe` field.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{6.6cm}|p{2.2cm}|p{8.5cm}| -->

<a id="rst-parm-flags"></a>


<table>
<caption>Capture Parameters Flags</caption>
<tbody>
<tr>
<td>


`V4L2_MODE_HIGHQUALITY`

</td>
<td>


0x0001

</td>
<td>


High quality imaging mode. High quality mode is intended for still imaging applications. The idea is to get the best possible image quality that the hardware can deliver. It is not defined how the driver writer may achieve that; it will depend on the hardware and the ingenuity of the driver writer. High quality mode is a different mode from the regular motion video capture modes. In high quality mode:

- The driver may be able to capture higher resolutions than for motion capture.

- The driver may support fewer pixel formats than motion capture (eg; true color).

- The driver may capture and arithmetically combine multiple successive fields or frames to remove color edge artifacts and reduce the noise in the video data.

- The driver may capture images in slices like a scanner in order to handle larger format images than would otherwise be possible.

- An image capture operation may be significantly slower than motion capture.

- Moving objects in the image might have excessive motion blur.

- Capture might only work through the `read()` call.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
