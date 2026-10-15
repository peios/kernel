---
title: "TSX Async Abort (TAA) mitigation"
type: reference
description: "TSX Async Abort (TAA) is a side channel attack on internal buffers in some Intel processors similar to Microachitectural Data Sampling (MDS). In this case certain loads may speculatively pass invalid data to dependent operations when an…"
---

<a id="rst-tsx-async-abort-taa-mitigation"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-overview"></a>
<a id="rst-tsx-async-abort"></a>

## Overview

TSX Async Abort (TAA) is a side channel attack on internal buffers in some Intel processors similar to Microachitectural Data Sampling (MDS).  In this case certain loads may speculatively pass invalid data to dependent operations when an asynchronous abort condition is pending in a Transactional Synchronization Extensions (TSX) transaction.  This includes loads with no fault or assist condition. Such loads may speculatively expose stale data from the same uarch data structures as in MDS, with same scope of exposure i.e. same-thread and cross-thread. This issue affects all current processors that support TSX.

<a id="rst-mitigation-strategy"></a>

## Mitigation strategy

a) TSX disable - one of the mitigations is to disable TSX. A new MSR IA32_TSX_CTRL will be available in future and current processors after microcode update which can be used to disable TSX. In addition, it controls the enumeration of the TSX feature bits (RTM and HLE) in CPUID.

b) Clear CPU buffers - similar to MDS, clearing the CPU buffers mitigates this vulnerability. More details on this approach can be found in [Documentation/admin-guide/hw-vuln/mds.rst](<~kernel/hardware/arch/x86/mds#rst-mds>).

<a id="rst-kernel-internal-mitigation-modes"></a>

## Kernel internal mitigation modes

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> off
>
> </td>
> <td>
>
>
> Mitigation is disabled. Either the CPU is not affected or tsx_async_abort=off is supplied on the kernel command line.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> tsx disabled
>
> </td>
> <td>
>
>
> Mitigation is enabled. TSX feature is disabled by default at bootup on processors that support TSX control.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> verw
>
> </td>
> <td>
>
>
> Mitigation is enabled. CPU is affected and MD_CLEAR is advertised in CPUID.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> ucode needed
>
> </td>
> <td>
>
>
> Mitigation is enabled. CPU is affected and MD_CLEAR is not advertised in CPUID. That is mainly for virtualization scenarios where the host has the updated microcode but the hypervisor does not expose MD_CLEAR in CPUID. It's a best effort approach without guarantee.
>
> </td>
> </tr>
> </tbody>
> </table>

If the CPU is affected and the "tsx_async_abort" kernel command line parameter is not provided then the kernel selects an appropriate mitigation depending on the status of RTM and MD_CLEAR CPUID bits.

Below tables indicate the impact of tsx=on\|off\|auto cmdline options on state of TAA mitigation, VERW behavior and TSX feature for various combinations of MSR_IA32_ARCH_CAPABILITIES bits.

1. "tsx=off"


<table>
<thead>
<tr>
<th colspan="3">


MSR_IA32_ARCH_CAPABILITIES bits

</th>
<th colspan="4">


Result with cmdline tsx=off

</th>
</tr>
<tr>
<th>


TAA_NO

</th>
<th>


MDS_NO

</th>
<th>


TSX_CTRL_MSR

</th>
<th>


TSX state after bootup

</th>
<th>


VERW can clear CPU buffers

</th>
<th>


TAA mitigation tsx_async_abort=off

</th>
<th>


TAA mitigation tsx_async_abort=full

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


0

</td>
<td>


0

</td>
<td>


0

</td>
<td>


HW default

</td>
<td>


Yes

</td>
<td>


Same as MDS

</td>
<td>


Same as MDS

</td>
</tr>
<tr>
<td>


0

</td>
<td>


0

</td>
<td>


1

</td>
<td>


Invalid case

</td>
<td>


Invalid case

</td>
<td>


Invalid case

</td>
<td>


Invalid case

</td>
</tr>
<tr>
<td>


0

</td>
<td>


1

</td>
<td>


0

</td>
<td>


HW default

</td>
<td>


No

</td>
<td>


Need ucode update

</td>
<td>


Need ucode update

</td>
</tr>
<tr>
<td>


0

</td>
<td>


1

</td>
<td>


1

</td>
<td>


Disabled

</td>
<td>


Yes

</td>
<td>


TSX disabled

</td>
<td>


TSX disabled

</td>
</tr>
<tr>
<td>


1

</td>
<td>


X

</td>
<td>


1

</td>
<td>


Disabled

</td>
<td>


X

</td>
<td>


None needed

</td>
<td>


None needed

</td>
</tr>
</tbody>
</table>

2. "tsx=on"


<table>
<thead>
<tr>
<th colspan="3">


MSR_IA32_ARCH_CAPABILITIES bits

</th>
<th colspan="4">


Result with cmdline tsx=on

</th>
</tr>
<tr>
<th>


TAA_NO

</th>
<th>


MDS_NO

</th>
<th>


TSX_CTRL_MSR

</th>
<th>


TSX state after bootup

</th>
<th>


VERW can clear CPU buffers

</th>
<th>


TAA mitigation tsx_async_abort=off

</th>
<th>


TAA mitigation tsx_async_abort=full

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


0

</td>
<td>


0

</td>
<td>


0

</td>
<td>


HW default

</td>
<td>


Yes

</td>
<td>


Same as MDS

</td>
<td>


Same as MDS

</td>
</tr>
<tr>
<td>


0

</td>
<td>


0

</td>
<td>


1

</td>
<td>


Invalid case

</td>
<td>


Invalid case

</td>
<td>


Invalid case

</td>
<td>


Invalid case

</td>
</tr>
<tr>
<td>


0

</td>
<td>


1

</td>
<td>


0

</td>
<td>


HW default

</td>
<td>


No

</td>
<td>


Need ucode update

</td>
<td>


Need ucode update

</td>
</tr>
<tr>
<td>


0

</td>
<td>


1

</td>
<td>


1

</td>
<td>


Enabled

</td>
<td>


Yes

</td>
<td>


None

</td>
<td>


Same as MDS

</td>
</tr>
<tr>
<td>


1

</td>
<td>


X

</td>
<td>


1

</td>
<td>


Enabled

</td>
<td>


X

</td>
<td>


None needed

</td>
<td>


None needed

</td>
</tr>
</tbody>
</table>

3. "tsx=auto"


<table>
<thead>
<tr>
<th colspan="3">


MSR_IA32_ARCH_CAPABILITIES bits

</th>
<th colspan="4">


Result with cmdline tsx=auto

</th>
</tr>
<tr>
<th>


TAA_NO

</th>
<th>


MDS_NO

</th>
<th>


TSX_CTRL_MSR

</th>
<th>


TSX state after bootup

</th>
<th>


VERW can clear CPU buffers

</th>
<th>


TAA mitigation tsx_async_abort=off

</th>
<th>


TAA mitigation tsx_async_abort=full

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


0

</td>
<td>


0

</td>
<td>


0

</td>
<td>


HW default

</td>
<td>


Yes

</td>
<td>


Same as MDS

</td>
<td>


Same as MDS

</td>
</tr>
<tr>
<td>


0

</td>
<td>


0

</td>
<td>


1

</td>
<td>


Invalid case

</td>
<td>


Invalid case

</td>
<td>


Invalid case

</td>
<td>


Invalid case

</td>
</tr>
<tr>
<td>


0

</td>
<td>


1

</td>
<td>


0

</td>
<td>


HW default

</td>
<td>


No

</td>
<td>


Need ucode update

</td>
<td>


Need ucode update

</td>
</tr>
<tr>
<td>


0

</td>
<td>


1

</td>
<td>


1

</td>
<td>


Disabled

</td>
<td>


Yes

</td>
<td>


TSX disabled

</td>
<td>


TSX disabled

</td>
</tr>
<tr>
<td>


1

</td>
<td>


X

</td>
<td>


1

</td>
<td>


Enabled

</td>
<td>


X

</td>
<td>


None needed

</td>
<td>


None needed

</td>
</tr>
</tbody>
</table>

In the tables, TSX_CTRL_MSR is a new bit in MSR_IA32_ARCH_CAPABILITIES that indicates whether MSR_IA32_TSX_CTRL is supported.

There are two control bits in IA32_TSX_CTRL MSR:

> - **Bit 0: When set it disables the Restricted Transactional Memory (RTM)**
>
>   sub-feature of TSX (will force all transactions to abort on the XBEGIN instruction).
>
> - **Bit 1: When set it disables the enumeration of the RTM and HLE feature**
>
>   (i.e. it will make CPUID(EAX=7).EBX\{bit4\} and CPUID(EAX=7).EBX\{bit11\} read as 0).
