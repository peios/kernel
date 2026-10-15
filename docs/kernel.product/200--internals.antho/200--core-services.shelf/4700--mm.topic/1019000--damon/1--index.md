---
title: "DAMON: Data Access MONitoring and Access-aware System Operations"
type: reference
description: "DAMON is a Linux kernel subsystem for efficient data access monitoring <damon_design_monitoring> and access-aware system operations <damon_design_damos>. It is designed for being"
---

<a id="rst-damon-data-access-monitoring-and-access-aware-system-operations"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

DAMON is a Linux kernel subsystem for efficient [data access monitoring](<~kernel/internals/mm/damon/design#rst-damon-design-monitoring>) and [access-aware system operations](<~kernel/internals/mm/damon/design#rst-damon-design-damos>).  It is designed for being

> - *accurate* (for DRAM level memory management),
>
> - *light-weight* (for production online usages),
>
> - *scalable* (in terms of memory size),
>
> - *tunable* (for flexible usages), and
>
> - *autoamted* (for production operation without manual tunings).

- [Frequently Asked Questions](<~kernel/internals/mm/damon/faq>)
- [Design](<~kernel/internals/mm/damon/design>)
- [API Reference](<~kernel/internals/mm/damon/api>)
- [DAMON Maintainer Entry Profile](<~kernel/internals/mm/damon/maintainer-profile>)

To utilize and control DAMON from the user-space, please refer to the administration [guide](<~kernel/administration/admin-guide/mm-damon/index>).

If you prefer academic papers for reading and citations, please use the papers from [HPDC'22](<https://dl.acm.org/doi/abs/10.1145/3502181.3531466>)<a id="rst-hpdc-22"></a> and [Middleware19 Industry](<https://dl.acm.org/doi/abs/10.1145/3366626.3368125>)<a id="rst-middleware19-industry"></a> . Note that those cover DAMON implementations in Linux v5.16 and v5.15, respectively.
