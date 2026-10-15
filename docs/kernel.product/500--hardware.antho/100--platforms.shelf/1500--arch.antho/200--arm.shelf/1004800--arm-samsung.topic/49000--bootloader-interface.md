---
title: "Interface between kernel and boot loaders on Exynos boards"
type: reference
description: "Author: Krzysztof Kozlowski"
---

<a id="rst-interface-between-kernel-and-boot-loaders-on-exynos-boards"></a>

Author: Krzysztof Kozlowski

Date  : 6 June 2015

The document tries to describe currently used interface between Linux kernel and boot loaders on Samsung Exynos based boards. This is not a definition of interface but rather a description of existing state, a reference for information purpose only.

In the document "boot loader" means any of following: U-boot, proprietary SBOOT or any other firmware for ARMv7 and ARMv8 initializing the board before executing kernel.

1. Non-Secure mode

Address:      sysram_ns_base_addr


<table>
<thead>
<tr>
<th>


Offset

</th>
<th>


Value

</th>
<th>


Purpose

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


0x08

</td>
<td>


exynos_cpu_resume_ns, mcpm_entry_point

</td>
<td>


System suspend

</td>
</tr>
<tr>
<td>


0x0c

</td>
<td>


0x00000bad (Magic cookie)

</td>
<td>


System suspend

</td>
</tr>
<tr>
<td>


0x1c

</td>
<td>


exynos4_secondary_startup

</td>
<td>


Secondary CPU boot

</td>
</tr>
<tr>
<td>


0x1c + 4\*cpu

</td>
<td>


exynos4_secondary_startup (Exynos4412)

</td>
<td>


Secondary CPU boot

</td>
</tr>
<tr>
<td>


0x20

</td>
<td>


0xfcba0d10 (Magic cookie)

</td>
<td>


AFTR

</td>
</tr>
<tr>
<td>


0x24

</td>
<td>


exynos_cpu_resume_ns

</td>
<td>


AFTR

</td>
</tr>
<tr>
<td>


0x28 + 4\*cpu

</td>
<td>


0x8 (Magic cookie, Exynos3250)

</td>
<td>


AFTR

</td>
</tr>
<tr>
<td>


0x28

</td>
<td>


0x0 or last value during resume (Exynos542x)

</td>
<td>


System suspend

</td>
</tr>
</tbody>
</table>

2. Secure mode

Address:      sysram_base_addr


<table>
<thead>
<tr>
<th>


Offset

</th>
<th>


Value

</th>
<th>


Purpose

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


0x00

</td>
<td>


exynos4_secondary_startup

</td>
<td>


Secondary CPU boot

</td>
</tr>
<tr>
<td>


0x04

</td>
<td>


exynos4_secondary_startup (Exynos542x)

</td>
<td>


Secondary CPU boot

</td>
</tr>
<tr>
<td>


4\*cpu

</td>
<td>


exynos4_secondary_startup (Exynos4412)

</td>
<td>


Secondary CPU boot

</td>
</tr>
<tr>
<td>


0x20

</td>
<td>


exynos_cpu_resume (Exynos4210 r1.0)

</td>
<td>


AFTR

</td>
</tr>
<tr>
<td>


0x24

</td>
<td>


0xfcba0d10 (Magic cookie, Exynos4210 r1.0)

</td>
<td>


AFTR

</td>
</tr>
</tbody>
</table>

Address:      pmu_base_addr


<table>
<thead>
<tr>
<th>


Offset

</th>
<th>


Value

</th>
<th>


Purpose

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


0x0800

</td>
<td>


exynos_cpu_resume

</td>
<td>


AFTR, suspend

</td>
</tr>
<tr>
<td>


0x0800

</td>
<td>


mcpm_entry_point (Exynos542x with MCPM)

</td>
<td>


AFTR, suspend

</td>
</tr>
<tr>
<td>


0x0804

</td>
<td>


0xfcba0d10 (Magic cookie)

</td>
<td>


AFTR

</td>
</tr>
<tr>
<td>


0x0804

</td>
<td>


0x00000bad (Magic cookie)

</td>
<td>


System suspend

</td>
</tr>
<tr>
<td>


0x0814

</td>
<td>


exynos4_secondary_startup (Exynos4210 r1.1)

</td>
<td>


Secondary CPU boot

</td>
</tr>
<tr>
<td>


0x0818

</td>
<td>


0xfcba0d10 (Magic cookie, Exynos4210 r1.1)

</td>
<td>


AFTR

</td>
</tr>
<tr>
<td>


0x081C

</td>
<td>


exynos_cpu_resume (Exynos4210 r1.1)

</td>
<td>


AFTR

</td>
</tr>
</tbody>
</table>

3. Other (regardless of secure/non-secure mode)

Address:      pmu_base_addr


<table>
<thead>
<tr>
<th>


Offset

</th>
<th>


Value

</th>
<th>


Purpose

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


0x0908

</td>
<td>


Non-zero

</td>
<td>


Secondary CPU boot up indicator on Exynos3250 and Exynos542x

</td>
</tr>
</tbody>
</table>

4. Glossary

AFTR - ARM Off Top Running, a low power mode, Cortex cores and many other modules are power gated, except the TOP modules MCPM - Multi-Cluster Power Management
