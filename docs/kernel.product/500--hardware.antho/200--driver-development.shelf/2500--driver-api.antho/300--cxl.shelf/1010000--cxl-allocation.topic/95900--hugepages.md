---
title: "Huge Pages"
type: reference
description: "CXL Memory onlined as SystemRAM during early boot is eligible for use by CMA, as the NUMA node hosting that capacity will be Online at the time CMA carves out contiguous capacity."
---

<a id="rst-huge-pages"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-contiguous-memory-allocator"></a>

## Contiguous Memory Allocator

CXL Memory onlined as SystemRAM during early boot is eligible for use by CMA, as the NUMA node hosting that capacity will be `Online` at the time CMA carves out contiguous capacity.

CXL Memory deferred to the CXL Driver for configuration cannot have its capacity allocated by CMA - as the NUMA node hosting the capacity is `Offline` at `__init` time - when CMA carves out contiguous capacity.

<a id="rst-hugetlb"></a>

## HugeTLB

Different huge page sizes allow different memory configurations.

<a id="rst-mb-huge-pages"></a>

### 2MB Huge Pages

All CXL capacity regardless of configuration time or memory zone is eligible for use as 2MB huge pages.

<a id="rst-gb-huge-pages"></a>

### 1GB Huge Pages

CXL capacity onlined in `ZONE_NORMAL` is eligible for 1GB Gigantic Page allocation.

CXL capacity onlined in `ZONE_MOVABLE` is not eligible for 1GB Gigantic Page allocation.
