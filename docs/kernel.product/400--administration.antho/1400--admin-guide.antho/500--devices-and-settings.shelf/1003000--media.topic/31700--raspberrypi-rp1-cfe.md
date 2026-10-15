---
title: "Raspberry Pi PiSP Camera Front End (rp1-cfe)"
type: reference
description: "The PiSP Camera Front End (CFE) is a module which combines a CSI-2 receiver with a simple ISP, called the Front End (FE)."
---

<a id="rst-raspberry-pi-pisp-camera-front-end-rp1-cfe"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-the-pisp-camera-front-end"></a>

## The PiSP Camera Front End

The PiSP Camera Front End (CFE) is a module which combines a CSI-2 receiver with a simple ISP, called the Front End (FE).

The CFE has four DMA engines and can write frames from four separate streams received from the CSI-2 to the memory. One of those streams can also be routed directly to the FE, which can do minimal image processing, write two versions (e.g. non-scaled and downscaled versions) of the received frames to memory and provide statistics of the received frames.

The FE registers are documented in the [Raspberry Pi Image Signal Processor (ISP) Specification document](<https://datasheets.raspberrypi.com/camera/raspberry-pi-image-signal-processor-specification.pdf>)<a id="rst-raspberry-pi-image-signal-processor-isp-specification-document"></a>, and example code for FE can be found in [libpisp](<https://github.com/raspberrypi/libpisp>)<a id="rst-libpisp"></a>.

<a id="rst-the-rp1-cfe-driver"></a>

## The rp1-cfe driver

The Raspberry Pi PiSP Camera Front End (rp1-cfe) driver is located under drivers/media/platform/raspberrypi/rp1-cfe. It uses the `V4L2 API` to register a number of video capture and output devices, the `V4L2 subdev API` to register subdevices for the CSI-2 received and the FE that connects the video devices in a single media graph realized using the `Media Controller (MC) API`.

The media topology registered by the `rp1-cfe` driver, in this particular example connected to an imx219 sensor, is the following one:

<a id="rst-rp1-cfe-topology"></a>

```mermaid
flowchart TB
  n0["pad 0<br/>csi2<br/>/dev/v4l-subdev0<br/>pad 1<br/>pad 2<br/>pad 3<br/>pad 4"]
  n1["rp1-cfe-csi2-ch0<br/>/dev/video0"]
  n2["pad 0<br/>pad 1<br/>pisp-fe<br/>/dev/v4l-subdev1<br/>pad 2<br/>pad 3<br/>pad 4"]
  n3["rp1-cfe-csi2-ch1<br/>/dev/video1"]
  n4["rp1-cfe-csi2-ch2<br/>/dev/video2"]
  n5["rp1-cfe-csi2-ch3<br/>/dev/video3"]
  n6["rp1-cfe-fe-image0<br/>/dev/video4"]
  n7["rp1-cfe-fe-image1<br/>/dev/video5"]
  n8["rp1-cfe-fe-stats<br/>/dev/video6"]
  n9["imx219 6-0010<br/>/dev/v4l-subdev2<br/>pad 0"]
  n10["rp1-cfe-fe-config<br/>/dev/video7"]
  n0 -->|"from pad 1"| n1
  n0 -->|"pad 1 → pad 0"| n2
  n0 -->|"from pad 2"| n3
  n0 -->|"pad 2 → pad 0"| n2
  n0 -->|"from pad 3"| n4
  n0 -->|"pad 3 → pad 0"| n2
  n0 -->|"from pad 4"| n5
  n0 -->|"pad 4 → pad 0"| n2
  n2 -->|"from pad 2"| n6
  n2 -->|"from pad 3"| n7
  n2 -->|"from pad 4"| n8
  n9 -->|"pad 0 → pad 0"| n0
  n10 -->|"to pad 1"| n2
  style n0 fill:green,color:#111
  style n1 fill:yellow,color:#111
  style n2 fill:green,color:#111
  style n3 fill:yellow,color:#111
  style n4 fill:yellow,color:#111
  style n5 fill:yellow,color:#111
  style n6 fill:yellow,color:#111
  style n7 fill:yellow,color:#111
  style n8 fill:yellow,color:#111
  style n9 fill:green,color:#111
  style n10 fill:yellow,color:#111
  linkStyle 0 stroke-dasharray:6 4
  linkStyle 3 stroke-dasharray:6 4
  linkStyle 4 stroke-dasharray:6 4
  linkStyle 5 stroke-dasharray:6 4
  linkStyle 6 stroke-dasharray:6 4
  linkStyle 7 stroke-dasharray:6 4
  linkStyle 9 stroke-dasharray:6 4
  linkStyle 11 stroke-width:3px
```

Diagram of an example media pipeline topology

The media graph contains the following video device nodes:

- rp1-cfe-csi2-ch0: capture device for the first CSI-2 stream

- rp1-cfe-csi2-ch1: capture device for the second CSI-2 stream

- rp1-cfe-csi2-ch2: capture device for the third CSI-2 stream

- rp1-cfe-csi2-ch3: capture device for the fourth CSI-2 stream

- rp1-cfe-fe-image0: capture device for the first FE output

- rp1-cfe-fe-image1: capture device for the second FE output

- rp1-cfe-fe-stats: capture device for the FE statistics

- rp1-cfe-fe-config: output device for FE configuration

<a id="rst-rp1-cfe-csi2-chx"></a>

### rp1-cfe-csi2-chX

The rp1-cfe-csi2-chX capture devices are normal V4L2 capture devices which can be used to capture video frames or metadata received from the CSI-2.

<a id="rst-rp1-cfe-fe-image0-rp1-cfe-fe-image1"></a>

### rp1-cfe-fe-image0, rp1-cfe-fe-image1

The rp1-cfe-fe-image0 and rp1-cfe-fe-image1 capture devices are used to write the processed frames to memory.

<a id="rst-rp1-cfe-fe-stats"></a>

### rp1-cfe-fe-stats

The format of the FE statistics buffer is defined by `pisp_statistics` C structure and the meaning of each parameter is described in the `PiSP specification` document.

<a id="rst-rp1-cfe-fe-config"></a>

### rp1-cfe-fe-config

The format of the FE configuration buffer is defined by `pisp_fe_config` C structure and the meaning of each parameter is described in the `PiSP specification` document.
