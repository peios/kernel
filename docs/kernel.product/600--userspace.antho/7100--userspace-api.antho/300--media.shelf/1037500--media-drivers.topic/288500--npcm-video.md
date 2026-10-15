---
title: "NPCM video driver"
type: reference
description: "This driver is used to control the Video Capture/Differentiation (VCD) engine and Encoding Compression Engine (ECE) present on Nuvoton NPCM SoCs. The VCD can capture a frame from digital video input and compare two frames in memory, and…"
---

<a id="rst-npcm-video-driver"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<!-- This data file has been placed in the public domain. -->

<!-- Derived from the Unicode character mappings available from
<http://www.w3.org/2003/entities/xml/>.
Processed by unicode2rstsubs.py, part of Docutils:
<https://docutils.sourceforge.io>. -->

This driver is used to control the Video Capture/Differentiation (VCD) engine and Encoding Compression Engine (ECE) present on Nuvoton NPCM SoCs. The VCD can capture a frame from digital video input and compare two frames in memory, and the ECE can compress the frame data into HEXTILE format.

<a id="rst-driver-specific-controls"></a>

## Driver-specific Controls

<a id="rst-v4l2-cid-npcm-capture-mode"></a>

### V4L2_CID_NPCM_CAPTURE_MODE

The VCD engine supports two modes:

- COMPLETE mode:

  Capture the next complete frame into memory.

- DIFF mode:

  Compare the incoming frame with the frame stored in memory, and updates the differentiated frame in memory.

Application can use `V4L2_CID_NPCM_CAPTURE_MODE` control to set the VCD mode with different control values (enum v4l2_npcm_capture_mode):

- `V4L2_NPCM_CAPTURE_MODE_COMPLETE`: will set VCD to COMPLETE mode.

- `V4L2_NPCM_CAPTURE_MODE_DIFF`: will set VCD to DIFF mode.

<a id="rst-v4l2-cid-npcm-rect-count"></a>

### V4L2_CID_NPCM_RECT_COUNT

If using V4L2_PIX_FMT_HEXTILE format, VCD will capture frame data and then ECE will compress the data into HEXTILE rectangles and store them in V4L2 video buffer with the layout defined in Remote Framebuffer Protocol:



```text
(RFC 6143, https://www.rfc-editor.org/rfc/rfc6143.html#section-7.6.1)

+--------------+--------------+-------------------+
| No. of bytes | Type [Value] | Description       |
+--------------+--------------+-------------------+
| 2            | U16          | x-position        |
| 2            | U16          | y-position        |
| 2            | U16          | width             |
| 2            | U16          | height            |
| 4            | S32          | encoding-type (5) |
+--------------+--------------+-------------------+
|             HEXTILE rectangle data              |
+-------------------------------------------------+
```

Application can get the video buffer through VIDIOC_DQBUF, and followed by calling `V4L2_CID_NPCM_RECT_COUNT` control to get the number of HEXTILE rectangles in this buffer.

<a id="rst-references"></a>

## References

include/uapi/linux/npcm-video.h

**Copyright** © 2022 Nuvoton Technologies
