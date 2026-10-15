---
title: "Page Cache"
type: reference
description: "The page cache is the primary way that the user and the rest of the kernel interact with filesystems. It can be bypassed (e.g. with O_DIRECT), but normal reads, writes and mmaps go through the page cache."
---

<a id="rst-page-cache"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

The page cache is the primary way that the user and the rest of the kernel interact with filesystems.  It can be bypassed (e.g. with O_DIRECT), but normal reads, writes and mmaps go through the page cache.

<a id="rst-folios"></a>

## Folios

The folio is the unit of memory management within the page cache. Operations
