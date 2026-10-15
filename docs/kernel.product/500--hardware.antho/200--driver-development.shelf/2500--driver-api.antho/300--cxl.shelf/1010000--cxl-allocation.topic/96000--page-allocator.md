---
title: "The Page Allocator"
type: reference
description: "The kernel page allocator services all general page allocation requests, such as kmalloc. CXL configuration steps affect the behavior of the page allocator based on the selected Memory Zone and NUMA node the capacity is placed in."
---

<a id="rst-the-page-allocator"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

The kernel page allocator services all general page allocation requests, such as `kmalloc`.  CXL configuration steps affect the behavior of the page allocator based on the selected `Memory Zone` and `NUMA node` the capacity is placed in.

This section mostly focuses on how these configurations affect the page allocator (as of Linux v6.15) rather than the overall page allocator behavior.

<a id="rst-numa-nodes-and-mempolicy"></a>

## NUMA nodes and mempolicy

Unless a task explicitly registers a mempolicy, the default memory policy of the linux kernel is to allocate memory from the `local NUMA node` first, and fall back to other nodes only if the local node is pressured.

Generally, we expect to see local DRAM and CXL memory on separate NUMA nodes, with the CXL memory being non-local.  Technically, however, it is possible for a compute node to have no local DRAM, and for CXL memory to be the `local` capacity for that compute node.

<a id="rst-memory-zones"></a>

## Memory Zones

CXL capacity may be onlined in `ZONE_NORMAL` or `ZONE_MOVABLE`.

As of v6.15, the page allocator attempts to allocate from the highest available and compatible ZONE for an allocation from the local node first.

An example of a `zone incompatibility` is attempting to service an allocation marked `GFP_KERNEL` from `ZONE_MOVABLE`.  Kernel allocations are typically not migratable, and as a result can only be serviced from `ZONE_NORMAL` or lower.

To simplify this, the page allocator will prefer `ZONE_MOVABLE` over `ZONE_NORMAL` by default, but if `ZONE_MOVABLE` is depleted, it will fallback to allocate from `ZONE_NORMAL`.

<a id="rst-cgroups-and-cpusets"></a>

## CGroups and CPUSets

Finally, assuming CXL memory is reachable via the page allocation (i.e. onlined in `ZONE_NORMAL`), the `cpusets.mems_allowed` may be used by containers to limit the accessibility of certain NUMA nodes for tasks in that container.  Users may wish to utilize this in multi-tenant systems where some tasks prefer not to use slower memory.

In the reclaim section we'll discuss some limitations of this interface to prevent demotions of shared data to CXL memory (if demotions are enabled).
