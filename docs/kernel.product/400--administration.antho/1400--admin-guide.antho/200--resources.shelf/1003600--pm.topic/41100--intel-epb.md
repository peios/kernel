---
title: "Intel Performance and Energy Bias Hint"
type: reference
description: "The Intel Performance and Energy Bias Hint (EPB) value for a given (logical) CPU can be checked or updated through a sysfs attribute (file) under /sys/devices/system/cpu/cpu<N>/power/, where the CPU number <N> is allocated at the system…"
---

<a id="rst-intel-performance-and-energy-bias-hint"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<!-- This data file has been placed in the public domain. -->

<!-- Derived from the Unicode character mappings available from
<http://www.w3.org/2003/entities/xml/>.
Processed by unicode2rstsubs.py, part of Docutils:
<https://docutils.sourceforge.io>. -->

**Copyright:** © 2019 Intel Corporation

**Author:** Rafael J. Wysocki &lt;[rafael.j.wysocki@intel.com](<mailto:rafael.j.wysocki@intel.com>)&gt;

```{kernel-doc} arch/x86/kernel/cpu/intel_epb.c
:doc: overview
```

<a id="rst-intel-performance-and-energy-bias-attribute-in-sysfs"></a>

## Intel Performance and Energy Bias Attribute in `sysfs`

The Intel Performance and Energy Bias Hint (EPB) value for a given (logical) CPU can be checked or updated through a `sysfs` attribute (file) under `/sys/devices/system/cpu/cpu<N>/power/`, where the CPU number `<N>` is allocated at the system initialization time:

- **`energy_perf_bias`**

  Shows the current EPB value for the CPU in a sliding scale 0 - 15, where a value of 0 corresponds to a hint preference for highest performance and a value of 15 corresponds to the maximum energy savings.

  In order to update the EPB value for the CPU, this attribute can be written to, either with a number in the 0 - 15 sliding scale above, or with one of the strings: "performance", "balance-performance", "normal", "balance-power", "power" that represent values reflected by their meaning.

  This attribute is present for all online CPUs supporting the EPB feature.

Note that while the EPB interface to the processor is defined at the logical CPU level, the physical register backing it may be shared by multiple CPUs (for example, SMT siblings or cores in one package).  For this reason, updating the EPB value for one CPU may cause the EPB values for other CPUs to change.
