---
title: "Glossary"
type: reference
description: "A Device Driver that implements the main logic to talk with media hardware."
---

<a id="rst-glossary"></a>

<!-- SPDX-License-Identifier: GPL-2.0 OR GFDL-1.1-no-invariants-or-later -->

> [!NOTE]
>
> The goal of this section is to standardize the terms used within the media userspace API documentation. This is Work In Progress.

<!-- Please keep the glossary entries in alphabetical order -->



- **<a id="rst-term-bridge-driver"></a>Bridge Driver**

  A [Device Driver](<#rst-term-device-driver>) that implements the main logic to talk with media hardware.

- **<a id="rst-term-cec-api"></a>CEC API**

  <strong>Consumer Electronics Control API</strong>

  An API designed to receive and transmit data via an HDMI CEC interface.

  See [cec](<~kernel/userspace/userspace-api/media-cec/cec-api#rst-cec>).

- **<a id="rst-term-data-unit"></a>Data Unit**

  Unit of data transported by a bus. On parallel buses, the data unit consists of one or more related samples while on serial buses the data unit is logical. If the data unit is image data, it may also be called a pixel.

- **<a id="rst-term-device-driver"></a>Device Driver**

  Part of the Linux Kernel that implements support for a hardware component.

- **<a id="rst-term-device-node"></a>Device Node**

  A character device node in the file system used to control and transfer data in and out of a Kernel driver.

- **<a id="rst-term-digital-tv-api"></a>Digital TV API**

  <strong>Previously known as DVB API</strong>

  An API designed to control a subset of the [Media Hardware](<#rst-term-media-hardware>) that implements digital TV (e. g. DVB, ATSC, ISDB, etc).

  See [dvbapi](<~kernel/userspace/userspace-api/media-dvb/dvbapi#rst-dvbapi>).

- **<a id="rst-term-dsp"></a>DSP**

  <strong>Digital Signal Processor</strong>

  A specialized [Microprocessor](<#rst-term-microprocessor>), with its architecture optimized for the operational needs of digital signal processing.

- **<a id="rst-term-fpga"></a>FPGA**

  <strong>Field-programmable Gate Array</strong>

  An [IC](<#rst-term-ic>) circuit designed to be configured by a customer or a designer after manufacturing.

  See [https://en.wikipedia.org/wiki/Field-programmable\_gate\_array](<https://en.wikipedia.org/wiki/Field-programmable_gate_array>).

- **<a id="rst-term-hardware-component"></a>Hardware Component**

  A subset of the [Media Hardware](<#rst-term-media-hardware>). For example an [I²C](<#rst-term-i2c>) or [SPI](<#rst-term-spi>) device, or an [IP Block](<#rst-term-ip-block>) inside an [SoC](<#rst-term-soc>) or [FPGA](<#rst-term-fpga>).

- **<a id="rst-term-hardware-peripheral"></a>Hardware Peripheral**

  A group of [hardware components](<#rst-term-hardware-component>) that together make a larger user-facing functional peripheral. For instance, the [SoC](<#rst-term-soc>) [ISP](<#rst-term-isp>) [IP Block](<#rst-term-ip-block>) and the external camera sensors together make a camera hardware peripheral.

  Also known as [Peripheral](<#rst-term-peripheral>).

- **<a id="rst-term-i2c"></a>I²C**

  <strong>Inter-Integrated Circuit</strong>

  A  multi-master, multi-slave, packet switched, single-ended, serial computer bus used to control some hardware components like sub-device hardware components.

  See [http://www.nxp.com/docs/en/user-guide/UM10204.pdf](<http://www.nxp.com/docs/en/user-guide/UM10204.pdf>).

- **<a id="rst-term-ic"></a>IC**

  <strong>Integrated circuit</strong>

  A set of electronic circuits on one small flat piece of semiconductor material, normally silicon.

  Also known as chip.

- **<a id="rst-term-ip-block"></a>IP Block**

  <strong>Intellectual property core</strong>

  In electronic design a semiconductor intellectual property core, is a reusable unit of logic, cell, or integrated circuit layout design that is the intellectual property of one party. IP Blocks may be licensed to another party or can be owned and used by a single party alone.

  See [https://en.wikipedia.org/wiki/Semiconductor\_intellectual\_property\_core](<https://en.wikipedia.org/wiki/Semiconductor_intellectual_property_core>)).

- **<a id="rst-term-isp"></a>ISP**

  <strong>Image Signal Processor</strong>

  A specialized processor that implements a set of algorithms for processing image data. ISPs may implement algorithms for lens shading correction, demosaicing, scaling and pixel format conversion as well as produce statistics for the use of the control algorithms (e.g. automatic exposure, white balance and focus).

- **<a id="rst-term-media-api"></a>Media API**

  A set of userspace APIs used to control the media hardware. It is composed by:

  > - [CEC API](<#rst-term-cec-api>);
  >
  > - [Digital TV API](<#rst-term-digital-tv-api>);
  >
  > - [MC API](<#rst-term-mc-api>);
  >
  > - [RC API](<#rst-term-rc-api>); and
  >
  > - [V4L2 API](<#rst-term-v4l2-api>).

  See [Documentation/userspace-api/media/index.rst](~kernel/userspace/userspace-api/media/index).

- **<a id="rst-term-mc-api"></a>MC API**

  <strong>Media Controller API</strong>

  An API designed to expose and control the relationships between multimedia devices and sub-devices.

  See [media\_controller](<~kernel/userspace/userspace-api/media-mediactl/media-controller#rst-media-controller>).

- **<a id="rst-term-mc-centric"></a>MC-centric**

  [V4L2 Hardware](<#rst-term-v4l2-hardware>) device driver that requires [MC API](<#rst-term-mc-api>).

  Such drivers have `V4L2_CAP_IO_MC` device\_caps field set (see [vidioc\_querycap](<~kernel/userspace/userspace-api/media-v4l/vidioc-querycap#rst-vidioc-querycap>)).

  See [v4l2\_hardware\_control](<~kernel/userspace/userspace-api/media-v4l/open#rst-v4l2-hardware-control>) for more details.

- **<a id="rst-term-media-hardware"></a>Media Hardware**

  Subset of the hardware that is supported by the Linux Media API.

  This includes audio and video capture and playback hardware, digital and analog TV, camera sensors, ISPs, remote controllers, codecs, HDMI Consumer Electronics Control, HDMI capture, etc.

- **<a id="rst-term-microprocessor"></a>Microprocessor**

  Electronic circuitry that carries out the instructions of a computer program by performing the basic arithmetic, logical, control and input/output (I/O) operations specified by the instructions on a single integrated circuit.

- **<a id="rst-term-peripheral"></a>Peripheral**

  The same as [Hardware Peripheral](<#rst-term-hardware-peripheral>).

- **<a id="rst-term-rc-api"></a>RC API**

  <strong>Remote Controller API</strong>

  An API designed to receive and transmit data from remote controllers.

  See [remote\_controllers](<~kernel/userspace/userspace-api/media-rc/remote-controllers#rst-remote-controllers>).

- **<a id="rst-term-smbus"></a>SMBus**

  A subset of I²C, which defines a stricter usage of the bus.

- **<a id="rst-term-spi"></a>SPI**

  <strong>Serial Peripheral Interface Bus</strong>

  Synchronous serial communication interface specification used for short distance communication, primarily in embedded systems.

- **<a id="rst-term-soc"></a>SoC**

  <strong>System on a Chip</strong>

  An integrated circuit that integrates all components of a computer or other electronic systems.

- **<a id="rst-term-stream"></a>Stream**

  A distinct flow of data (image data or metadata) from an initial source to a final sink. The initial source may be e.g. an image sensor and the final sink e.g. a memory buffer.

- **<a id="rst-term-v4l2-api"></a>V4L2 API**

  <strong>V4L2 userspace API</strong>

  The userspace API defined in [v4l2spec](<~kernel/userspace/userspace-api/media-v4l/v4l2#rst-v4l2spec>), which is used to control a V4L2 hardware.

- **<a id="rst-term-v4l2-device-node"></a>V4L2 Device Node**

  A [Device Node](<#rst-term-device-node>) that is associated to a V4L driver.

  The V4L2 device node naming is specified at [v4l2\_device\_naming](<~kernel/userspace/userspace-api/media-v4l/open#rst-v4l2-device-naming>).

- **<a id="rst-term-v4l2-hardware"></a>V4L2 Hardware**

  Part of the media hardware which is supported by the [V4L2 API](<#rst-term-v4l2-api>).

- **<a id="rst-term-v4l2-sub-device"></a>V4L2 Sub-device**

  V4L2 hardware components that aren't controlled by a [Bridge Driver](<#rst-term-bridge-driver>). See [Sub-device Interface](<~kernel/userspace/userspace-api/media-v4l/dev-subdev#rst-subdev>).

- **<a id="rst-term-video-node-centric"></a>Video-node-centric**

  V4L2 device driver that doesn't require a media controller to be used.

  Such drivers have the `V4L2_CAP_IO_MC` device\_caps field unset (see [vidioc\_querycap](<~kernel/userspace/userspace-api/media-v4l/vidioc-querycap#rst-vidioc-querycap>)).

- **<a id="rst-term-v4l2-sub-device-api"></a>V4L2 Sub-device API**

  Part of the [V4L2 API](<#rst-term-v4l2-api>) which control [V4L2 sub-devices](<#rst-term-v4l2-sub-device>), like sensors, HDMI receivers, scalers, deinterlacers.

  See [v4l2\_hardware\_control](<~kernel/userspace/userspace-api/media-v4l/open#rst-v4l2-hardware-control>) for more details.
