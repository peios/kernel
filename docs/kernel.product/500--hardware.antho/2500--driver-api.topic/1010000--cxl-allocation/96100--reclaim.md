---
title: "Reclaim"
type: reference
description: "Another way CXL memory can be utilized indirectly is via the reclaim system in mm/vmscan.c. Reclaim is engaged when memory capacity on the system becomes pressured based on global and cgroup-local watermark settings."
---

<a id="rst-reclaim"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

Another way CXL memory can be utilized *indirectly* is via the reclaim system in `mm/vmscan.c`.  Reclaim is engaged when memory capacity on the system becomes pressured based on global and cgroup-local `watermark` settings.

In this section we won't discuss the `watermark` configurations, just how CXL memory can be consumed by various pieces of reclaim system.

<a id="rst-demotion"></a>

## Demotion

By default, the reclaim system will prefer swap (or zswap) when reclaiming memory.  Enabling `kernel/mm/numa/demotion_enabled` will cause vmscan to opportunistically prefer distant NUMA nodes to swap or zswap, if capacity is available.

Demotion engages the `mm/memory_tier.c` component to determine the next demotion node.  The next demotion node is based on the `HMAT` or `CDAT` performance data.

<a id="rst-cpusets-mems-allowed-quirk"></a>

### cpusets.mems_allowed quirk

In Linux v6.15 and below, demotion does not respect `cpusets.mems_allowed` when migrating pages.  As a result, if demotion is enabled, vmscan cannot guarantee isolation of a container's memory from nodes not set in mems_allowed.

In Linux v6.XX and up, demotion does attempt to respect `cpusets.mems_allowed`; however, certain classes of shared memory originally instantiated by another cgroup (such as common libraries - e.g. libc) may still be demoted.  As a result, the mems_allowed interface still cannot provide perfect isolation from the remote nodes.

<a id="rst-zswap-and-node-preference"></a>

## ZSwap and Node Preference

In Linux v6.15 and below, ZSwap allocates memory from the local node of the processor for the new pages being compressed.  Since pages being compressed are typically cold, the result is a cold page becomes promoted - only to be later demoted as it ages off the LRU.

In Linux v6.XX, ZSwap tries to prefer the node of the page being compressed as the allocation target for the compression page.  This helps prevent thrashing.

<a id="rst-demotion-with-zswap"></a>

## Demotion with ZSwap

When enabling both Demotion and ZSwap, you create a situation where ZSwap will prefer the slowest form of CXL memory by default until that tier of memory is exhausted.
