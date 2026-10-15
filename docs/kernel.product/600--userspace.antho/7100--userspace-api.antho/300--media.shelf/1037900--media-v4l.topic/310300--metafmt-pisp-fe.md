---
title: "V4L2_META_FMT_RPI_FE_CFG"
type: reference
description: "The Raspberry Pi PiSP Front End image signal processor is configured by userspace by providing a buffer of configuration parameters to the rp1-cfe-fe-config output video device node using the v4l2_meta_format interface."
---

<!-- SPDX-License-Identifier: GPL-2.0 -->

<!-- c:namespace: V4L -->

<a id="rst-v4l2-meta-fmt-rpi-fe-cfg-1"></a>
<a id="rst-v4l2-meta-fmt-rpi-fe-cfg"></a>

## V4L2_META_FMT_RPI_FE_CFG

<a id="rst-raspberry-pi-pisp-front-end-configuration-format"></a>

### Raspberry Pi PiSP Front End configuration format

The Raspberry Pi PiSP Front End image signal processor is configured by userspace by providing a buffer of configuration parameters to the `rp1-cfe-fe-config` output video device node using the `v4l2_meta_format` interface.

The [Raspberry Pi PiSP technical specification](<https://datasheets.raspberrypi.com/camera/raspberry-pi-image-signal-processor-specification.pdf>)<a id="rst-raspberry-pi-pisp-technical-specification"></a> provide detailed description of the Front End configuration and programming model.

<a id="rst-v4l2-meta-fmt-rpi-fe-stats-1"></a>
<a id="rst-v4l2-meta-fmt-rpi-fe-stats"></a>

## V4L2_META_FMT_RPI_FE_STATS

<a id="rst-raspberry-pi-pisp-front-end-statistics-format"></a>

### Raspberry Pi PiSP Front End statistics format

The Raspberry Pi PiSP Front End image signal processor provides statistics data by writing to a buffer provided via the `rp1-cfe-fe-stats` capture video device node using the `v4l2_meta_format` interface.

The [Raspberry Pi PiSP technical specification](<https://datasheets.raspberrypi.com/camera/raspberry-pi-image-signal-processor-specification.pdf>)<a id="rst-raspberry-pi-pisp-technical-specification-1"></a> provide detailed description of the Front End configuration and programming model.
