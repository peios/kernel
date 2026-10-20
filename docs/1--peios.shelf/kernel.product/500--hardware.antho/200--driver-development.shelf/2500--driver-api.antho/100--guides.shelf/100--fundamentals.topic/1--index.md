---
title: "Driver development"
type: guide
description: "Start with the driver model, then find the subsystem API you need."
---

<a id="rst-driver-implementer-s-api-guide"></a>
<a id="rst-general-information-for-driver-authors"></a>
<a id="rst-useful-support-libraries"></a>
<a id="rst-bus-level-documentation"></a>
<a id="rst-subsystem-specific-apis"></a>

Driver development combines common kernel facilities with the interfaces of a
particular bus or device subsystem.

Start with the [Device and driver model](<~kernel/hardware/driver-api/driver-model/index>)
and [Driver basics](<~kernel/hardware/driver-api/fundamentals/basics>). Then use the guides for
[Device I/O](<~kernel/hardware/driver-api/io-and-dma/device-io>),
[DMA engines](<~kernel/hardware/driver-api/dmaengine/index>) and
[Firmware loading](<~kernel/hardware/driver-api/firmware/index>) as needed.

The remaining shelves collect subsystem APIs, platform services and media
interfaces. CXL has its own group covering the programming model, allocation,
devices and platform integration.

Use [Hardware and drivers](<~kernel/hardware/start-here/overview>) for device-family
documentation and [Kernel development](<~kernel/development/start-here/overview>)
for build and test guidance.
