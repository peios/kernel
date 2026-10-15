---
title: "Digital TV (DVB) devices"
type: reference
description: "Digital TV devices are implemented by several different drivers:"
---

<a id="rst-digital-tv-dvb-devices"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

Digital TV devices are implemented by several different drivers:

- A bridge driver that is responsible to talk with the bus where the other devices are connected (PCI, USB, SPI), bind to the other drivers and implement the digital demux logic (either in software or in hardware);

- Frontend drivers that are usually implemented as two separate drivers:

  - A tuner driver that implements the logic which commands the part of the hardware responsible for tuning into a digital TV transponder or physical channel. The output of a tuner is usually a baseband or Intermediate Frequency (IF) signal;

  - A demodulator driver (a.k.a "demod") that implements the logic which commands the digital TV decoding hardware. The output of a demod is a digital stream, with multiple audio, video and data channels typically multiplexed using MPEG Transport Stream <a id="rst-footnote-reference-1"></a>[1](#rst-f1).

On most hardware, the frontend drivers talk with the bridge driver using an I2C bus.

<a id="rst-f1"></a>



**[1]** Some standards use TCP/IP for multiplexing data, like DVB-H (an abandoned standard, not used anymore) and ATSC version 3.0 current proposals. Currently, the DVB subsystem doesn't implement those standards.

- [Digital TV Common functions](<~kernel/hardware/driver-api/media/dtv-common>)
- [Digital TV Frontend kABI](<~kernel/hardware/driver-api/media/dtv-frontend>)
- [Digital TV Demux kABI](<~kernel/hardware/driver-api/media/dtv-demux>)
- [Digital TV Conditional Access kABI](<~kernel/hardware/driver-api/media/dtv-ca>)
- [Digital TV Network kABI](<~kernel/hardware/driver-api/media/dtv-net>)
