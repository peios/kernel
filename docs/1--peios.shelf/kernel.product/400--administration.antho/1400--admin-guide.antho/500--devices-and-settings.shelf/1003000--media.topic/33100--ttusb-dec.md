---
title: "TechnoTrend/Hauppauge DEC USB Driver"
type: reference
description: "Supported:"
---

<a id="rst-technotrend-hauppauge-dec-usb-driver"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-driver-status"></a>

## Driver Status

Supported:

> - DEC2000-t
>
> - DEC2450-t
>
> - DEC3000-s
>
> - Video Streaming
>
> - Audio Streaming
>
> - Section Filters
>
> - Channel Zapping
>
> - Hotplug firmware loader

To Do:

> - Tuner status information
>
> - DVB network interface
>
> - Streaming video PC-&gt;DEC
>
> - Conax support for 2450-t

<a id="rst-getting-the-firmware"></a>

## Getting the Firmware

To download the firmware, use the following commands:



```none
scripts/get_dvb_firmware dec2000t
scripts/get_dvb_firmware dec2540t
scripts/get_dvb_firmware dec3000s
```

<a id="rst-hotplug-firmware-loading"></a>

## Hotplug Firmware Loading

Since 2.6 kernels, the firmware is loaded at the point that the driver module is loaded.

Copy the three files downloaded above into the /usr/lib/hotplug/firmware or /lib/firmware directory (depending on configuration of firmware hotplug).
