---
title: "V4L2_META_FMT_D4XX ('D4XX')"
type: reference
description: "Intel D4xx UVC Cameras Metadata"
---

<a id="rst-v4l2-meta-fmt-d4xx-d4xx"></a>
<a id="rst-v4l2-meta-fmt-d4xx"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

Intel D4xx UVC Cameras Metadata

<a id="rst-description"></a>

## Description

Intel D4xx (D435, D455 and others) cameras include per-frame metadata in their UVC payload headers, following the Microsoft(R) UVC extension proposal \[[1](<#rst-target-1>)\]. That means, that the private D4XX metadata, following the standard UVC header, is organised in blocks. D4XX cameras implement several standard block types, proposed by Microsoft, and several proprietary ones. Supported standard metadata types are MetadataId_CaptureStats (ID 3), MetadataId_CameraExtrinsics (ID 4), and MetadataId_CameraIntrinsics (ID 5). For their description see \[[1](<#rst-target-1>)\]. This document describes proprietary metadata types, used by D4xx cameras.

V4L2_META_FMT_D4XX buffers follow the metadata buffer layout of V4L2_META_FMT_UVC with the only difference, that it also includes proprietary payload header data. D4xx cameras use bulk transfers and only send one payload per frame, therefore their headers cannot be larger than 255 bytes.

This document implements Intel Configuration version 3 \[[9](<#rst-target-9>)\].

Below are proprietary Microsoft style metadata types, used by D4xx cameras, where all fields are in little endian order:

<!-- tabularcolumns: |p{5.0cm}|p{12.5cm}| -->


<table>
<caption>D4xx metadata</caption>
<thead>
<tr>
<th>


**Field**

</th>
<th>


**Description**

</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2">


 *Depth Control*

</td>
</tr>
<tr>
<td>


\__u32 ID

</td>
<td>


0x80000000

</td>
</tr>
<tr>
<td>


\__u32 Size

</td>
<td>


Size in bytes, include ID (all protocol versions: 60)

</td>
</tr>
<tr>
<td>


\__u32 Version

</td>
<td>


Version of this structure. The documentation herein covers versions 1, 2 and 3. The version number will be incremented when new fields are added.

</td>
</tr>
<tr>
<td>


\__u32 Flags

</td>
<td>


A bitmask of flags: see \[[2](<#rst-target-2>)\] below

</td>
</tr>
<tr>
<td>


\__u32 Gain

</td>
<td>


Gain value in internal units, same as the V4L2_CID_GAIN control, used to capture the frame

</td>
</tr>
<tr>
<td>


\__u32 Exposure

</td>
<td>


Exposure time (in microseconds) used to capture the frame

</td>
</tr>
<tr>
<td>


\__u32 Laser power

</td>
<td>


Power of the laser LED 0-360, used for depth measurement

</td>
</tr>
<tr>
<td>


\__u32 AE mode

</td>
<td>


0: manual; 1: automatic exposure

</td>
</tr>
<tr>
<td>


\__u32 Exposure priority

</td>
<td>


Exposure priority value: 0 - constant frame rate

</td>
</tr>
<tr>
<td>


\__u32 AE ROI left

</td>
<td>


Left border of the AE Region of Interest (all ROI values are in pixels and lie between 0 and maximum width or height respectively)

</td>
</tr>
<tr>
<td>


\__u32 AE ROI right

</td>
<td>


Right border of the AE Region of Interest

</td>
</tr>
<tr>
<td>


\__u32 AE ROI top

</td>
<td>


Top border of the AE Region of Interest

</td>
</tr>
<tr>
<td>


\__u32 AE ROI bottom

</td>
<td>


Bottom border of the AE Region of Interest

</td>
</tr>
<tr>
<td>


\__u32 Preset

</td>
<td>


Preset selector value, default: 0, unless changed by the user

</td>
</tr>
<tr>
<td>


\__u8 Emitter mode (v3 only) (\__u32 Laser mode for v1) \[[8](<#rst-target-8>)\]

</td>
<td>


0: off, 1: on, same as \__u32 Laser mode for v1

</td>
</tr>
<tr>
<td>


\__u8 RFU byte (v3 only)

</td>
<td>


Spare byte for future use

</td>
</tr>
<tr>
<td>


\__u16 LED Power (v3 only)

</td>
<td>


Led power value 0-360 (F416 SKU)

</td>
</tr>
<tr>
<td colspan="2">


 *Capture Timing*

</td>
</tr>
<tr>
<td>


\__u32 ID

</td>
<td>


0x80000001

</td>
</tr>
<tr>
<td>


\__u32 Size

</td>
<td>


Size in bytes, include ID (all protocol versions: 40)

</td>
</tr>
<tr>
<td>


\__u32 Version

</td>
<td>


Version of this structure. The documentation herein corresponds to version xxx. The version number will be incremented when new fields are added.

</td>
</tr>
<tr>
<td>


\__u32 Flags

</td>
<td>


A bitmask of flags: see \[[3](<#rst-target-3>)\] below

</td>
</tr>
<tr>
<td>


\__u32 Frame counter

</td>
<td>


Monotonically increasing counter

</td>
</tr>
<tr>
<td>


\__u32 Optical time

</td>
<td>


Time in microseconds from the beginning of a frame till its middle

</td>
</tr>
<tr>
<td>


\__u32 Readout time

</td>
<td>


Time, used to read out a frame in microseconds

</td>
</tr>
<tr>
<td>


\__u32 Exposure time

</td>
<td>


Frame exposure time in microseconds

</td>
</tr>
<tr>
<td>


\__u32 Frame interval

</td>
<td>


In microseconds = 1000000 / framerate

</td>
</tr>
<tr>
<td>


\__u32 Pipe latency

</td>
<td>


Time in microseconds from start of frame to data in USB buffer

</td>
</tr>
<tr>
<td colspan="2">


 *Configuration*

</td>
</tr>
<tr>
<td>


\__u32 ID

</td>
<td>


0x80000002

</td>
</tr>
<tr>
<td>


\__u32 Size

</td>
<td>


Size in bytes, include ID (v1:36, v3:40)

</td>
</tr>
<tr>
<td>


\__u32 Version

</td>
<td>


Version of this structure. The documentation herein corresponds to version xxx. The version number will be incremented when new fields are added.

</td>
</tr>
<tr>
<td>


\__u32 Flags

</td>
<td>


A bitmask of flags: see \[[4](<#rst-target-4>)\] below

</td>
</tr>
<tr>
<td>


\__u8 Hardware type

</td>
<td>


Camera hardware version \[[5](<#rst-target-5>)\]

</td>
</tr>
<tr>
<td>


\__u8 SKU ID

</td>
<td>


Camera hardware configuration \[[6](<#rst-target-6>)\]

</td>
</tr>
<tr>
<td>


\__u32 Cookie

</td>
<td>


Internal synchronisation

</td>
</tr>
<tr>
<td>


\__u16 Format

</td>
<td>


Image format code \[[7](<#rst-target-7>)\]

</td>
</tr>
<tr>
<td>


\__u16 Width

</td>
<td>


Width in pixels

</td>
</tr>
<tr>
<td>


\__u16 Height

</td>
<td>


Height in pixels

</td>
</tr>
<tr>
<td>


\__u16 Framerate

</td>
<td>


Requested frame rate per second

</td>
</tr>
<tr>
<td>


\__u16 Trigger

</td>
<td>


Byte 0: bit 0: depth and RGB are synchronised, bit 1: external trigger

</td>
</tr>
<tr>
<td>


\__u16 Calibration count (v3 only)

</td>
<td>


Calibration counter, see \[[4](<#rst-target-4>)\] below

</td>
</tr>
<tr>
<td>


\__u8 GPIO input data (v3 only)

</td>
<td>


GPIO readout, see \[[4](<#rst-target-4>)\] below (Supported from FW 5.12.7.0)

</td>
</tr>
<tr>
<td>


\__u32 Sub-preset info (v3 only)

</td>
<td>


Sub-preset choice information, see \[[4](<#rst-target-4>)\] below

</td>
</tr>
<tr>
<td>


\__u8 reserved (v3 only)

</td>
<td>


RFU byte.

</td>
</tr>
</tbody>
</table>

<a id="rst-target-1"></a>

\[1\] [https://docs.microsoft.com/en-us/windows-hardware/drivers/stream/uvc-extensions-1-5](<https://docs.microsoft.com/en-us/windows-hardware/drivers/stream/uvc-extensions-1-5>)

<a id="rst-target-2"></a>

\[2\] Depth Control flags specify which fields are valid:



```text
0x00000001 Gain
0x00000002 Exposure
0x00000004 Laser power
0x00000008 AE mode
0x00000010 Exposure priority
0x00000020 AE ROI
0x00000040 Preset
0x00000080 Emitter mode
0x00000100 LED Power
```

<a id="rst-target-3"></a>

\[3\] Capture Timing flags specify which fields are valid:



```text
0x00000001 Frame counter
0x00000002 Optical time
0x00000004 Readout time
0x00000008 Exposure time
0x00000010 Frame interval
0x00000020 Pipe latency
```

<a id="rst-target-4"></a>

\[4\] Configuration flags specify which fields are valid:



```text
0x00000001 Hardware type
0x00000002 SKU ID
0x00000004 Cookie
0x00000008 Format
0x00000010 Width
0x00000020 Height
0x00000040 Framerate
0x00000080 Trigger
0x00000100 Cal count
0x00000200 GPIO Input Data
0x00000400 Sub-preset Info
```

<a id="rst-target-5"></a>

\[5\] Camera model:



```text
0 DS5
1 IVCAM2
```

<a id="rst-target-6"></a>

\[6\] 8-bit camera hardware configuration bitfield:



```text
[1:0] depthCamera
      00: no depth
      01: standard depth
      10: wide depth
      11: reserved
[2]   depthIsActive - has a laser projector
[3]   RGB presence
[4]   Inertial Measurement Unit (IMU) presence
[5]   projectorType
      0: HPTG
      1: Princeton
[6]   0: a projector, 1: an LED
[7]   reserved
```

<a id="rst-target-7"></a>

\[7\] Image format codes per video streaming interface:

Depth:



```text
1 Z16
2 Z
```

Left sensor:



```text
1 Y8
2 UYVY
3 R8L8
4 Calibration
5 W10
```

Fish Eye sensor:



```text
1 RAW8
```

<a id="rst-target-8"></a>

\[8\] The "Laser mode" has been replaced in version 3 by three different fields. "Laser" has been renamed to "Emitter" as there are multiple technologies for camera projectors. As we have another field for "Laser Power" we introduced "LED Power" for extra emitter.

- **The "Laser mode" \__u32 fields has been split into: ::**

  1 \__u8 Emitter mode 2 \__u8 RFU byte 3 \__u16 LED Power

This is a change between versions 1 and 3. All versions 1, 2 and 3 are backward compatible with the same data format and they are supported. See \[[2](<#rst-target-2>)\] for which attributes are valid.

<a id="rst-target-9"></a>

\[9\] LibRealSense SDK metadata source: [https://github.com/IntelRealSense/librealsense/blob/master/src/metadata.h](<https://github.com/IntelRealSense/librealsense/blob/master/src/metadata.h>)
