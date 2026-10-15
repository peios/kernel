---
title: "DAX Driver Operation"
type: reference
description: "The Direct Access Device driver was originally designed to provide a memory-like access mechanism to memory-like block-devices. It was extended to support CXL Memory Devices, which provide user-configured memory devices."
---

<a id="rst-dax-driver-operation"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

The `Direct Access Device` driver was originally designed to provide a memory-like access mechanism to memory-like block-devices.  It was extended to support CXL Memory Devices, which provide user-configured memory devices.

The CXL subsystem depends on the DAX subsystem to either:

- Generate a file-like interface to userland via `/dev/daxN.Y`, or

- Engage the memory-hotplug interface to add CXL memory to page allocator.

The DAX subsystem exposes this ability through the `cxl_dax_region` driver. A `dax_region` provides the translation between a CXL `memory_region` and a `DAX Device`.

<a id="rst-dax-device"></a>

## DAX Device

A `DAX Device` is a file-like interface exposed in `/dev/daxN.Y`. A memory region exposed via dax device can be accessed via userland software via the `mmap()` system-call.  The result is direct mappings to the CXL capacity in the task's page tables.

Users wishing to manually handle allocation of CXL memory should use this interface.

<a id="rst-kmem-conversion"></a>

## kmem conversion

The `dax_kmem` driver converts a `DAX Device` into a series of `hotplug memory blocks` managed by `kernel/memory-hotplug.c`.  This capacity will be exposed to the kernel page allocator in the user-selected memory zone.

The `memmap_on_memory` setting (both global and DAX device local) dictates where the kernell will allocate the `struct folio` descriptors for this memory will come from.  If `memmap_on_memory` is set, memory hotplug will set aside a portion of the memory block capacity to allocate folios. If unset, the memory is allocated via a normal `GFP_KERNEL` allocation - and as a result will most likely land on the local NUM node of the CPU executing the hotplug operation.
