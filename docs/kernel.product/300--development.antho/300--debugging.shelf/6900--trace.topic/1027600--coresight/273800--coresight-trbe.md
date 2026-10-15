---
title: "Trace Buffer Extension (TRBE)."
type: reference
description: "Trace Buffer Extension (TRBE) is a percpu hardware which captures in system memory, CPU traces generated from a corresponding percpu tracing unit. This gets plugged in as a coresight sink device because the corresponding trace generators…"
---

<a id="rst-trace-buffer-extension-trbe"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

> **Author:** Anshuman Khandual &lt;[anshuman.khandual@arm.com](<mailto:anshuman.khandual@arm.com>)&gt;
>
> **Date:** November 2020

<a id="rst-hardware-description"></a>

## Hardware Description

Trace Buffer Extension (TRBE) is a percpu hardware which captures in system memory, CPU traces generated from a corresponding percpu tracing unit. This gets plugged in as a coresight sink device because the corresponding trace generators (ETE), are plugged in as source device.

The TRBE is not compliant to CoreSight architecture specifications, but is driven via the CoreSight driver framework to support the ETE (which is CoreSight compliant) integration.

<a id="rst-sysfs-files-and-directories"></a>

## Sysfs files and directories

The TRBE devices appear on the existing coresight bus alongside the other coresight devices:



```text
>$ ls /sys/bus/coresight/devices
trbe0  trbe1  trbe2 trbe3
```

The `trbe<N>` named TRBEs are associated with a CPU.:



```text
>$ ls /sys/bus/coresight/devices/trbe0/
align flag
```

- ***Key file items are:-***

  - `align`: TRBE write pointer alignment

  - `flag`: TRBE updates memory with access and dirty flags
