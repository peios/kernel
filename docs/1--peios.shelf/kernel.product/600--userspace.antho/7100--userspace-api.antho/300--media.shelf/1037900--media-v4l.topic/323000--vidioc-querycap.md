---
title: "ioctl VIDIOC_QUERYCAP"
type: reference
description: "VIDIOC_QUERYCAP - Query device capabilities"
---

<a id="rst-ioctl-vidioc-querycap"></a>
<a id="rst-vidioc-querycap"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_QUERYCAP - Query device capabilities

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_QUERYCAP"></a>

```c
VIDIOC_QUERYCAP
```

`int ioctl(int fd, VIDIOC_QUERYCAP, struct v4l2_capability *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_capability`.

<a id="rst-description"></a>

## Description

All V4L2 devices support the `VIDIOC_QUERYCAP` ioctl. It is used to identify kernel devices compatible with this specification and to obtain information about driver and hardware capabilities. The ioctl takes a pointer to a struct `v4l2_capability` which is filled by the driver. When the driver is not compatible with this specification the ioctl returns an `EINVAL` error code.





<a id="c-v4l2_capability"></a>

```c
v4l2_capability
```

<!-- tabularcolumns: |p{1.4cm}|p{2.8cm}|p{13.1cm}| -->


<table>
<caption>struct v4l2_capability</caption>
<tbody>
<tr>
<td>


\__u8

</td>
<td>


`driver`\[16\]

</td>
<td>


Name of the driver, a unique NUL-terminated ASCII string. For example: "bttv". Driver specific applications can use this information to verify the driver identity. It is also useful to work around known bugs, or to identify drivers in error reports.

Storing strings in fixed sized arrays is bad practice but unavoidable here. Drivers and applications should take precautions to never read or write beyond the end of the array and to make sure the strings are properly NUL-terminated.

</td>
</tr>
<tr>
<td>


\__u8

</td>
<td>


`card`\[32\]

</td>
<td>


Name of the device, a NUL-terminated UTF-8 string. For example: "Yoyodyne TV/FM". One driver may support different brands or models of video hardware. This information is intended for users, for example in a menu of available devices. Since multiple TV cards of the same brand may be installed which are supported by the same driver, this name should be combined with the character device file name (e. g. `/dev/video2`) or the `bus_info` string to avoid ambiguities.

</td>
</tr>
<tr>
<td>


\__u8

</td>
<td>


`bus_info`\[32\]

</td>
<td>


Location of the device in the system, a NUL-terminated ASCII string. For example: "PCI:0000:05:06.0". This information is intended for users, to distinguish multiple identical devices. If no such information is available the field must simply count the devices controlled by the driver ("platform:vivid-000"). The bus_info must start with "PCI:" for PCI boards, "PCIe:" for PCI Express boards, "usb-" for USB devices, "I2C:" for i2c devices, "ISA:" for ISA devices, "parport" for parallel port devices and "platform:" for platform devices.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`version`

</td>
<td>


Version number of the driver.

Starting with kernel 3.1, the version reported is provided by the V4L2 subsystem following the kernel numbering scheme. However, it may not always return the same version as the kernel if, for example, a stable or distribution-modified kernel uses the V4L2 stack from a newer kernel.

The version number is formatted using the `KERNEL_VERSION()` macro. For example if the media stack corresponds to the V4L2 version shipped with Kernel 4.14, it would be equivalent to:

</td>
</tr>
<tr>
<td colspan="3">


`#define KERNEL_VERSION(a,b,c) (((a) << 16) + ((b) << 8) + (c))`

`__u32 version = KERNEL_VERSION(4, 14, 0);`

`printf ("Version: %u.%u.%u\\n",`

`(version >> 16) & 0xFF, (version >> 8) & 0xFF, version & 0xFF);`

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`capabilities`

</td>
<td>


Available capabilities of the physical device as a whole, see [device-capabilities](<#rst-device-capabilities>). The same physical device can export multiple devices in /dev (e.g. /dev/videoX, /dev/vbiY and /dev/radioZ). The `capabilities` field should contain a union of all capabilities available around the several V4L2 devices exported to userspace. For all those devices the `capabilities` field returns the same set of capabilities. This allows applications to open just one of the devices (typically the video device) and discover whether video, vbi and/or radio are also supported.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`device_caps`

</td>
<td>


Device capabilities of the opened device, see [device-capabilities](<#rst-device-capabilities>). Should contain the available capabilities of that specific device node. So, for example, `device_caps` of a radio device will only contain radio related capabilities and no video or vbi capabilities. This field is only set if the `capabilities` field contains the `V4L2_CAP_DEVICE_CAPS` capability. Only the `capabilities` field can have the `V4L2_CAP_DEVICE_CAPS` capability, `device_caps` will never set `V4L2_CAP_DEVICE_CAPS`.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`reserved`\[3\]

</td>
<td>


Reserved for future extensions. Drivers must set this array to zero.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{7.0cm}|p{2.6cm}|p{7.7cm}| -->

<a id="rst-device-capabilities"></a>


<table>
<caption>Device Capabilities Flags</caption>
<tbody>
<tr>
<td>


`V4L2_CAP_VIDEO_CAPTURE`

</td>
<td>


0x00000001

</td>
<td>


The device supports the single-planar API through the [Video Capture](<~kernel/userspace/userspace-api/media-v4l/dev-capture#rst-capture>) interface.

</td>
</tr>
<tr>
<td>


`V4L2_CAP_VIDEO_CAPTURE_MPLANE`

</td>
<td>


0x00001000

</td>
<td>


The device supports the [multi-planar API](<~kernel/userspace/userspace-api/media-v4l/planar-apis#rst-planar-apis>) through the [Video Capture](<~kernel/userspace/userspace-api/media-v4l/dev-capture#rst-capture>) interface.

</td>
</tr>
<tr>
<td>


`V4L2_CAP_VIDEO_OUTPUT`

</td>
<td>


0x00000002

</td>
<td>


The device supports the single-planar API through the [Video Output](<~kernel/userspace/userspace-api/media-v4l/dev-output#rst-output>) interface.

</td>
</tr>
<tr>
<td>


`V4L2_CAP_VIDEO_OUTPUT_MPLANE`

</td>
<td>


0x00002000

</td>
<td>


The device supports the [multi-planar API](<~kernel/userspace/userspace-api/media-v4l/planar-apis#rst-planar-apis>) through the [Video Output](<~kernel/userspace/userspace-api/media-v4l/dev-output#rst-output>) interface.

</td>
</tr>
<tr>
<td>


`V4L2_CAP_VIDEO_M2M`

</td>
<td>


0x00008000

</td>
<td>


The device supports the single-planar API through the Video Memory-To-Memory interface.

</td>
</tr>
<tr>
<td>


`V4L2_CAP_VIDEO_M2M_MPLANE`

</td>
<td>


0x00004000

</td>
<td>


The device supports the [multi-planar API](<~kernel/userspace/userspace-api/media-v4l/planar-apis#rst-planar-apis>) through the Video Memory-To-Memory interface.

</td>
</tr>
<tr>
<td>


`V4L2_CAP_VIDEO_OVERLAY`

</td>
<td>


0x00000004

</td>
<td>


The device supports the [Video Overlay](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/dev-overlay.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) interface. A video overlay device typically stores captured images directly in the video memory of a graphics card, with hardware clipping and scaling.

</td>
</tr>
<tr>
<td>


`V4L2_CAP_VBI_CAPTURE`

</td>
<td>


0x00000010

</td>
<td>


The device supports the [Raw VBI Capture](<~kernel/userspace/userspace-api/media-v4l/dev-raw-vbi#rst-raw-vbi>) interface, providing Teletext and Closed Caption data.

</td>
</tr>
<tr>
<td>


`V4L2_CAP_VBI_OUTPUT`

</td>
<td>


0x00000020

</td>
<td>


The device supports the [Raw VBI Output](<~kernel/userspace/userspace-api/media-v4l/dev-raw-vbi#rst-raw-vbi>) interface.

</td>
</tr>
<tr>
<td>


`V4L2_CAP_SLICED_VBI_CAPTURE`

</td>
<td>


0x00000040

</td>
<td>


The device supports the [Sliced VBI Capture](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/dev-sliced-vbi.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) interface.

</td>
</tr>
<tr>
<td>


`V4L2_CAP_SLICED_VBI_OUTPUT`

</td>
<td>


0x00000080

</td>
<td>


The device supports the [Sliced VBI Output](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/dev-sliced-vbi.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) interface.

</td>
</tr>
<tr>
<td>


`V4L2_CAP_RDS_CAPTURE`

</td>
<td>


0x00000100

</td>
<td>


The device supports the [RDS](<~kernel/userspace/userspace-api/media-v4l/dev-rds#rst-rds>) capture interface.

</td>
</tr>
<tr>
<td>


`V4L2_CAP_VIDEO_OUTPUT_OVERLAY`

</td>
<td>


0x00000200

</td>
<td>


The device supports the [Video Output Overlay](<~kernel/userspace/userspace-api/media-v4l/dev-osd#rst-osd>) (OSD) interface. Unlike the *Video Overlay* interface, this is a secondary function of video output devices and overlays an image onto an outgoing video signal. When the driver sets this flag, it must clear the `V4L2_CAP_VIDEO_OVERLAY` flag and vice versa. <a id="rst-footnote-reference-1"></a>[1](#rst-f1)

</td>
</tr>
<tr>
<td>


`V4L2_CAP_HW_FREQ_SEEK`

</td>
<td>


0x00000400

</td>
<td>


The device supports the [ioctl VIDIOC_S_HW_FREQ_SEEK](<~kernel/userspace/userspace-api/media-v4l/vidioc-s-hw-freq-seek#rst-vidioc-s-hw-freq-seek>) ioctl for hardware frequency seeking.

</td>
</tr>
<tr>
<td>


`V4L2_CAP_RDS_OUTPUT`

</td>
<td>


0x00000800

</td>
<td>


The device supports the [RDS](<~kernel/userspace/userspace-api/media-v4l/dev-rds#rst-rds>) output interface.

</td>
</tr>
<tr>
<td>


`V4L2_CAP_TUNER`

</td>
<td>


0x00010000

</td>
<td>


The device has some sort of tuner to receive RF-modulated video signals. For more information about tuner programming see [Tuners and Modulators](<~kernel/userspace/userspace-api/media-v4l/tuner#rst-tuner>).

</td>
</tr>
<tr>
<td>


`V4L2_CAP_AUDIO`

</td>
<td>


0x00020000

</td>
<td>


The device has audio inputs or outputs. It may or may not support audio recording or playback, in PCM or compressed formats. PCM audio support must be implemented as ALSA or OSS interface. For more information on audio inputs and outputs see [Audio Inputs and Outputs](<~kernel/userspace/userspace-api/media-v4l/audio#rst-audio>).

</td>
</tr>
<tr>
<td>


`V4L2_CAP_RADIO`

</td>
<td>


0x00040000

</td>
<td>


This is a radio receiver.

</td>
</tr>
<tr>
<td>


`V4L2_CAP_MODULATOR`

</td>
<td>


0x00080000

</td>
<td>


The device has some sort of modulator to emit RF-modulated video/audio signals. For more information about modulator programming see [Tuners and Modulators](<~kernel/userspace/userspace-api/media-v4l/tuner#rst-tuner>).

</td>
</tr>
<tr>
<td>


`V4L2_CAP_SDR_CAPTURE`

</td>
<td>


0x00100000

</td>
<td>


The device supports the [SDR Capture](<~kernel/userspace/userspace-api/media-v4l/dev-sdr#rst-sdr>) interface.

</td>
</tr>
<tr>
<td>


`V4L2_CAP_EXT_PIX_FORMAT`

</td>
<td>


0x00200000

</td>
<td>


The device supports the struct `v4l2_pix_format` extended fields.

</td>
</tr>
<tr>
<td>


`V4L2_CAP_SDR_OUTPUT`

</td>
<td>


0x00400000

</td>
<td>


The device supports the [SDR Output](<~kernel/userspace/userspace-api/media-v4l/dev-sdr#rst-sdr>) interface.

</td>
</tr>
<tr>
<td>


`V4L2_CAP_META_CAPTURE`

</td>
<td>


0x00800000

</td>
<td>


The device supports the [Metadata Interface](<~kernel/userspace/userspace-api/media-v4l/dev-meta#rst-metadata>) capture interface.

</td>
</tr>
<tr>
<td>


`V4L2_CAP_READWRITE`

</td>
<td>


0x01000000

</td>
<td>


The device supports the `read()` and/or `write()` I/O methods.

</td>
</tr>
<tr>
<td>


`V4L2_CAP_EDID`

</td>
<td>


0x02000000

</td>
<td>


The device stores the EDID for a video input, or retrieves the EDID for a video output. It is a standalone EDID device, so no video streaming etc. will take place.

For a video input this is typically an eeprom that supports the [VESA Enhanced Display Data Channel Standard](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-vesaeddc>). It can be something else as well, for example a micro controller.

For a video output this is typically read from an external device such as an HDMI splitter accessed by a serial port.

</td>
</tr>
<tr>
<td>


`V4L2_CAP_STREAMING`

</td>
<td>


0x04000000

</td>
<td>


The device supports the [streaming](<~kernel/userspace/userspace-api/media-v4l/mmap#rst-mmap>) I/O method.

</td>
</tr>
<tr>
<td>


`V4L2_CAP_META_OUTPUT`

</td>
<td>


0x08000000

</td>
<td>


The device supports the [Metadata Interface](<~kernel/userspace/userspace-api/media-v4l/dev-meta#rst-metadata>) output interface.

</td>
</tr>
<tr>
<td>


`V4L2_CAP_TOUCH`

</td>
<td>


0x10000000

</td>
<td>


This is a touch device.

</td>
</tr>
<tr>
<td>


`V4L2_CAP_IO_MC`

</td>
<td>


0x20000000

</td>
<td>


There is only one input and/or output seen from userspace. The whole video topology configuration, including which I/O entity is routed to the input/output, is configured by userspace via the Media Controller. See [Part IV - Media Controller API](<~kernel/userspace/userspace-api/media-mediactl/media-controller#rst-media-controller>).

</td>
</tr>
<tr>
<td>


`V4L2_CAP_DEVICE_CAPS`

</td>
<td>


0x80000000

</td>
<td>


The driver fills the `device_caps` field. This capability can only appear in the `capabilities` field and never in the `device_caps` field.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

<a id="rst-f1"></a>



**[1]** The struct `v4l2_framebuffer` lacks an enum `v4l2_buf_type` field, therefore the type of overlay is implied by the driver capabilities.
