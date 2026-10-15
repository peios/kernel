---
title: "V4L2_META_FMT_RPI_BE_CFG"
type: reference
description: "The Raspberry Pi PiSP Back End memory-to-memory image signal processor is configured by userspace by providing a buffer of configuration parameters to the pispbe-config output video device node using the v4l2_meta_format interface."
---

<a id="rst-v4l2-meta-fmt-rpi-be-cfg-1"></a>
<a id="rst-v4l2-meta-fmt-rpi-be-cfg"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<!-- c:namespace: V4L -->

<a id="rst-raspberry-pi-pisp-back-end-configuration-format"></a>

## Raspberry Pi PiSP Back End configuration format

The Raspberry Pi PiSP Back End memory-to-memory image signal processor is configured by userspace by providing a buffer of configuration parameters to the `pispbe-config` output video device node using the `v4l2_meta_format` interface.

The PiSP Back End processes images in tiles, and its configuration requires specifying two different sets of parameters by populating the members of `pisp_be_tiles_config` defined in the `pisp_be_config.h` header file.

The [Raspberry Pi PiSP technical specification](<https://datasheets.raspberrypi.com/camera/raspberry-pi-image-signal-processor-specification.pdf>)<a id="rst-raspberry-pi-pisp-technical-specification"></a> provide detailed description of the ISP back end configuration and programming model.

<a id="rst-global-configuration-data"></a>

### Global configuration data

The global configuration data describe how the pixels in a particular image are to be processed and is therefore shared across all the tiles of the image. So for example, LSC (Lens Shading Correction) or Denoise parameters would be common across all tiles from the same frame.

Global configuration data are passed to the ISP by populating the member of `pisp_be_config`.

<a id="rst-tile-parameters"></a>

### Tile parameters

As the ISP processes images in tiles, each set of tiles parameters describe how a single tile in an image is going to be processed. A single set of tile parameters consist of 160 bytes of data and to process a batch of tiles several sets of tiles parameters are required.

Tiles parameters are passed to the ISP by populating the member of `pisp_tile` and the `num_tiles` fields of `pisp_be_tiles_config`.

<a id="rst-raspberry-pi-pisp-back-end-uapi-data-types"></a>

## Raspberry Pi PiSP Back End uAPI data types

This section describes the data types exposed to userspace by the Raspberry Pi PiSP Back End. The section is informative only, for a detailed description of each field refer to the [Raspberry Pi PiSP technical specification](<https://datasheets.raspberrypi.com/camera/raspberry-pi-image-signal-processor-specification.pdf>)<a id="rst-raspberry-pi-pisp-technical-specification-1"></a>.

```{kernel-doc} include/uapi/linux/media/raspberrypi/pisp_be_config.h

```
