---
title: "The trace performance monitoring and diagnostics aggregator(TPDA)"
type: reference
description: "TPDA - The trace performance monitoring and diagnostics aggregator or TPDA in short serves as an arbitration and packetization engine for the performance monitoring and diagnostics network specification. The primary use case of the TPDA is…"
---

<a id="rst-the-trace-performance-monitoring-and-diagnostics-aggregator-tpda"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

> **Author:** Jinlong Mao &lt;[quic_jinlmao@quicinc.com](<mailto:quic_jinlmao@quicinc.com>)&gt;
>
> **Date:** January 2023

<a id="rst-hardware-description"></a>

## Hardware Description

TPDA - The trace performance monitoring and diagnostics aggregator or TPDA in short serves as an arbitration and packetization engine for the performance monitoring and diagnostics network specification. The primary use case of the TPDA is to provide packetization, funneling and timestamping of Monitor data.

<a id="rst-sysfs-files-and-directories"></a>

## Sysfs files and directories

Root: `/sys/bus/coresight/devices/tpda<N>`

<a id="rst-config-details"></a>

## Config details

The tpdm and tpda nodes should be observed at the coresight path "/sys/bus/coresight/devices". e.g. /sys/bus/coresight/devices \# ls -l \| grep tpd tpda0 -&gt; ../../../[devices/platform/soc@0/6004000.tpda/tpda0](<mailto:devices/platform/soc@0/6004000.tpda/tpda0>) tpdm0 -&gt; ../../../[devices/platform/soc@0/6c08000.mm.tpdm/tpdm0](<mailto:devices/platform/soc@0/6c08000.mm.tpdm/tpdm0>)

We can use the commands are similar to the below to validate TPDMs. Enable coresight sink first. The port of tpda which is connected to the tpdm will be enabled after commands below.

echo 1 &gt; /sys/bus/coresight/devices/tmc_etf0/enable_sink echo 1 &gt; /sys/bus/coresight/devices/tpdm0/enable_source echo 1 &gt; /sys/bus/coresight/devices/tpdm0/integration_test echo 2 &gt; /sys/bus/coresight/devices/tpdm0/integration_test

The test data will be collected in the coresight sink which is enabled. If rwp register of the sink is keeping updating when do integration_test (by cat tmc_etf0/mgmt/rwp), it means there is data generated from TPDM to sink.

There must be a tpda between tpdm and the sink. When there are some other trace event hw components in the same HW block with tpdm, tpdm and these hw components will connect to the coresight funnel. When there is only tpdm trace hw in the HW block, tpdm will connect to tpda directly.
