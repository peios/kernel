---
title: "Working with hardware"
type: guide
description: "Find driver guidance, device references and hardware descriptions."
---

Begin with [Driver development](<~kernel/hardware/driver-api/fundamentals/index>) when writing
or extending a driver. The driver model, I/O and DMA guides explain shared
mechanisms; subsystem topics describe the interfaces for a particular device class.

For an existing device, browse the shelves for buses and interconnects,
graphics and input, storage, or platform devices and sensors. Examples include
[PCI](<~kernel/hardware/pci/index>), [USB](<~kernel/hardware/usb/index>),
[Graphics](<~kernel/hardware/gpu/index>) and [Sound](<~kernel/hardware/sound/index>).

For platform bring-up and hardware description, use
[Processor architectures](<~kernel/hardware/arch/overview/index>),
[Firmware](<~kernel/hardware/firmware-guide/index>) and
[Device tree](<~kernel/hardware/devicetree/index>).
The [Device-tree binding reference](<~kernel/hardware/devicetree-bindings>)
contains the generated schema catalogue, grouped by device class.

These references describe the source tree. A documented architecture or device
is not a declaration that a particular Peios release supports or qualifies it.
