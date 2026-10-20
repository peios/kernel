---
title: "Compute Express Link"
type: reference
description: "CXL device configuration has a complex handoff between platform (Hardware, BIOS, EFI), OS (early boot, core kernel, driver), and user policy decisions that have impacts on each other. The docs here break up configurations steps."
---

<a id="rst-compute-express-link"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

CXL device configuration has a complex handoff between platform (Hardware, BIOS, EFI), OS (early boot, core kernel, driver), and user policy decisions that have impacts on each other.  The docs here break up configurations steps.

**Overview**

- [Compute Express Link Driver Theory of Operation](<~kernel/hardware/driver-api/cxl/theory-of-operation>)
- [Compute Express Link Subsystem Maturity Map](<~kernel/hardware/driver-api/cxl/maturity-map>)
- [Compute Express Link: Linux Conventions](<~kernel/hardware/driver-api/cxl/conventions>)

**Device Reference**

- [Devices and Protocols](<~kernel/hardware/driver-api/cxl-devices/device-types>)

**Platform Configuration**

- [BIOS/EFI Configuration](<~kernel/hardware/driver-api/cxl-platform/bios-and-efi>)
- [ACPI Tables](<~kernel/hardware/driver-api/cxl-platform/acpi>)
- [Coherent Device Attribute Table (CDAT)](<~kernel/hardware/driver-api/cxl-platform/cdat>)
- [Example Platform Configurations](<~kernel/hardware/driver-api/cxl-platform/example-configs>)
- [CXL Device Hotplug](<~kernel/hardware/driver-api/cxl-platform/device-hotplug>)

**Linux Kernel Configuration**

- [Overview](<~kernel/hardware/driver-api/cxl-linux/overview>)
- [Linux Init (Early Boot)](<~kernel/hardware/driver-api/cxl-linux/early-boot>)
- [CXL Driver Operation](<~kernel/hardware/driver-api/cxl-linux/cxl-driver>)
- [DAX Driver Operation](<~kernel/hardware/driver-api/cxl-linux/dax-driver>)
- [Memory Hotplug](<~kernel/hardware/driver-api/cxl-linux/memory-hotplug>)
- [CXL Access Coordinates Computation](<~kernel/hardware/driver-api/cxl-linux/access-coordinates>)

**Memory Allocation**

- [DAX Devices](<~kernel/hardware/driver-api/cxl-allocation/dax>)
- [The Page Allocator](<~kernel/hardware/driver-api/cxl-allocation/page-allocator>)
- [Reclaim](<~kernel/hardware/driver-api/cxl-allocation/reclaim>)
- [Huge Pages](<~kernel/hardware/driver-api/cxl-allocation/hugepages>)
