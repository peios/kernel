---
title: "Core API Documentation"
type: reference
description: "This is the beginning of a manual for core kernel APIs. The conversion (and writing!) of documents for this manual is much appreciated!"
---

<a id="rst-core-api-documentation"></a>

This is the beginning of a manual for core kernel APIs.  The conversion (and writing\!) of documents for this manual is much appreciated\!

<a id="rst-core-utilities"></a>

## Core utilities

This section has general and "core core" documentation.  The first is a massive grab-bag of kerneldoc info left over from the docbook days; it should really be broken up someday when somebody finds the energy to do it.

- [The Linux Kernel API](<~kernel/internals/core-api/kernel-api>)
- [Workqueue](<~kernel/internals/core-api/workqueue>)
- [General notification mechanism](<~kernel/internals/core-api/watch-queue>)
- [Message logging with printk](<~kernel/internals/core-api/printk-basics>)
- [How to get printk format specifiers right](<~kernel/internals/core-api/printk-formats>)
- [Printk Index](<~kernel/internals/core-api/printk-index>)
- [Symbol Namespaces](<~kernel/internals/core-api/symbol-namespaces>)
- [Assembler Annotations](<~kernel/internals/core-api/asm-annotations>)
- [Real-time preemption](<~kernel/internals/core-api/real-time/index>)
- [Housekeeping](<~kernel/internals/core-api/housekeeping>)

<a id="rst-data-structures-and-low-level-utilities"></a>

## Data structures and low-level utilities

Library functionality that is used throughout the kernel.

- [Everything you never wanted to know about kobjects, ksets, and ktypes](<~kernel/internals/core-api/kobject>)
- [Adding reference counters (krefs) to kernel objects](<~kernel/internals/core-api/kref>)
- [Scope-based Cleanup Helpers](<~kernel/internals/core-api/cleanup>)
- [Generic Associative Array Implementation](<~kernel/internals/core-api/assoc-array>)
- [Folio Queue](<~kernel/internals/core-api/folio-queue>)
- [XArray](<~kernel/internals/core-api/xarray>)
- [Maple Tree](<~kernel/internals/core-api/maple-tree>)
- [ID Allocation](<~kernel/internals/core-api/idr>)
- [Circular Buffers](<~kernel/internals/core-api/circular-buffers>)
- [Red-black Trees (rbtree) in Linux](<~kernel/internals/core-api/rbtree>)
- [Generic radix trees/sparse arrays](<~kernel/internals/core-api/generic-radix-tree>)
- [Generic bitfield packing and unpacking functions](<~kernel/internals/core-api/packing>)
- [this_cpu operations](<~kernel/internals/core-api/this-cpu-ops>)
- [ktime accessors](<~kernel/internals/core-api/timekeeping>)
- [The errseq_t datatype](<~kernel/internals/core-api/errseq>)
- [atomic_t](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/core-api/wrappers/atomic_t.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)
- [atomic_bitops](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/core-api/wrappers/atomic_bitops.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)
- [Floating-point API](<~kernel/internals/core-api/floating-point>)
- [Union-Find in Linux](<~kernel/internals/core-api/union-find>)
- [Min Heap API](<~kernel/internals/core-api/min-heap>)
- [Generic parser](<~kernel/internals/core-api/parser>)
- [Linked Lists in Linux](<~kernel/internals/core-api/list>)

<a id="rst-low-level-entry-and-exit"></a>

## Low level entry and exit

- [Entry/exit handling for exceptions, interrupts, syscalls and KVM](<~kernel/internals/core-api/entry>)

<a id="rst-concurrency-primitives"></a>

## Concurrency primitives

How Linux keeps everything from happening at the same time.  See [Documentation/locking/index.rst](https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/locking/index.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92) for more related documentation.

- [refcount_t API compared to atomic_t](<~kernel/internals/core-api/refcount-vs-atomic>)
- [IRQs](<~kernel/internals/core-api/irq/index>)
- [Semantics and Behavior of Local Atomic Operations](<~kernel/internals/core-api/local-ops>)
- [The padata parallel execution mechanism](<~kernel/internals/core-api/padata>)
- [RCU Handbook](<~kernel/internals/rcu/index>)
- [memory-barriers](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/core-api/wrappers/memory-barriers.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)

<a id="rst-low-level-hardware-management"></a>

## Low-level hardware management

Cache management, managing CPU hotplug, etc.

- [Cache and TLB Flushing Under Linux](<~kernel/internals/core-api/cachetlb>)
- [CPU hotplug in the Kernel](<~kernel/internals/core-api/cpu-hotplug>)
- [Memory hotplug](<~kernel/internals/core-api/memory-hotplug>)
- [Linux generic IRQ handling](<~kernel/internals/core-api/genericirq>)
- [Memory Protection Keys](<~kernel/internals/core-api/protection-keys>)

<a id="rst-memory-management"></a>

## Memory management

How to allocate and use memory in the kernel.  Note that there is a lot more memory-management documentation in [Documentation/mm/index.rst](~kernel/internals/mm/index).

- [Memory Allocation Guide](<~kernel/internals/core-api/memory-allocation>)
- [Unaligned Memory Accesses](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/core-api/unaligned-memory-access.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)
- [Dynamic DMA mapping using the generic device](<~kernel/internals/core-api/dma-api>)
- [Dynamic DMA mapping Guide](<~kernel/internals/core-api/dma-api-howto>)
- [DMA attributes](<~kernel/internals/core-api/dma-attributes>)
- [DMA with ISA and LPC devices](<~kernel/internals/core-api/dma-isa-lpc>)
- [DMA and swiotlb](<~kernel/internals/core-api/swiotlb>)
- [Memory Management APIs](<~kernel/internals/core-api/mm-api>)
- [Cgroup Kernel APIs](<~kernel/internals/core-api/cgroup>)
- [The genalloc/genpool subsystem](<~kernel/internals/core-api/genalloc>)
- [pin_user_pages() and related calls](<~kernel/internals/core-api/pin-user-pages>)
- [Boot time memory management](<~kernel/internals/core-api/boot-time-mm>)
- [GFP masks used from FS/IO context](<~kernel/internals/core-api/gfp-mask-from-fs-io>)
- [Kexec Handover Subsystem](<~kernel/internals/core-api/kho/index>)

<a id="rst-interfaces-for-kernel-debugging"></a>

## Interfaces for kernel debugging

- [The object-lifetime debugging infrastructure](<~kernel/internals/core-api/debug-objects>)
- [The Linux Kernel Tracepoint API](<~kernel/internals/core-api/tracepoint>)
- [Using physical DMA provided by OHCI-1394 FireWire controllers for debugging](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/core-api/debugging-via-ohci1394.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)

<a id="rst-everything-else"></a>

## Everything else

Documents that don't fit elsewhere or which have yet to be categorized.

- [Reed-Solomon Library Programming Interface](<~kernel/internals/core-api/librs>)
- [Live Update Orchestrator](<~kernel/internals/core-api/liveupdate>)
- [Netlink notes for kernel developers](<~kernel/internals/core-api/netlink>)
