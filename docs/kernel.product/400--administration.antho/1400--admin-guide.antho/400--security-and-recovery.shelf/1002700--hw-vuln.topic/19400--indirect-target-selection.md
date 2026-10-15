---
title: "Indirect Target Selection (ITS)"
type: reference
description: "ITS is a vulnerability in some Intel CPUs that support Enhanced IBRS and were released before Alder Lake. ITS may allow an attacker to control the prediction of indirect branches and RETs located in the lower half of a cacheline."
---

<a id="rst-indirect-target-selection-its"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

ITS is a vulnerability in some Intel CPUs that support Enhanced IBRS and were released before Alder Lake. ITS may allow an attacker to control the prediction of indirect branches and RETs located in the lower half of a cacheline.

ITS is assigned CVE-2024-28956 with a CVSS score of 4.7 (Medium).

<a id="rst-scope-of-impact"></a>

## Scope of Impact

- **eIBRS Guest/Host Isolation**: Indirect branches in KVM/kernel may still be predicted with unintended target corresponding to a branch in the guest.

- **Intra-Mode BTI**: In-kernel training such as through cBPF or other native gadgets.

- **Indirect Branch Prediction Barrier (IBPB)**: After an IBPB, indirect branches may still be predicted with targets corresponding to direct branches executed prior to the IBPB. This is fixed by the IPU 2025.1 microcode, which should be available via distro updates. Alternatively microcode can be obtained from Intel's github repository <a id="rst-footnote-reference-1"></a>[1](#rst-f1).

<a id="rst-affected-cpus"></a>

## Affected CPUs

Below is the list of ITS affected CPUs <a id="rst-footnote-reference-2"></a>[2](#rst-f2) <a id="rst-footnote-reference-3"></a>[3](#rst-f3):

>
> <table>
> <thead>
> <tr>
> <th>
>
>
> Common name
>
> </th>
> <th>
>
>
> Family_Model
>
> </th>
> <th>
>
>
> eIBRS Guest/Host Isolation
>
> </th>
> <th>
>
>
> Intra-mode BTI
>
> </th>
> </tr>
> </thead>
> <tbody>
> <tr>
> <td>
>
>
> SKYLAKE_X (step &gt;= 6)
>
> </td>
> <td>
>
>
> 06_55H
>
> </td>
> <td>
>
>
> Affected
>
> </td>
> <td>
>
>
> Affected
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> ICELAKE_X
>
> </td>
> <td>
>
>
> 06_6AH
>
> </td>
> <td>
>
>
> Not affected
>
> </td>
> <td>
>
>
> Affected
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> ICELAKE_D
>
> </td>
> <td>
>
>
> 06_6CH
>
> </td>
> <td>
>
>
> Not affected
>
> </td>
> <td>
>
>
> Affected
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> ICELAKE_L
>
> </td>
> <td>
>
>
> 06_7EH
>
> </td>
> <td>
>
>
> Not affected
>
> </td>
> <td>
>
>
> Affected
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> TIGERLAKE_L
>
> </td>
> <td>
>
>
> 06_8CH
>
> </td>
> <td>
>
>
> Not affected
>
> </td>
> <td>
>
>
> Affected
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> TIGERLAKE
>
> </td>
> <td>
>
>
> 06_8DH
>
> </td>
> <td>
>
>
> Not affected
>
> </td>
> <td>
>
>
> Affected
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> KABYLAKE_L (step &gt;= 12)
>
> </td>
> <td>
>
>
> 06_8EH
>
> </td>
> <td>
>
>
> Affected
>
> </td>
> <td>
>
>
> Affected
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> KABYLAKE (step &gt;= 13)
>
> </td>
> <td>
>
>
> 06_9EH
>
> </td>
> <td>
>
>
> Affected
>
> </td>
> <td>
>
>
> Affected
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> COMETLAKE
>
> </td>
> <td>
>
>
> 06_A5H
>
> </td>
> <td>
>
>
> Affected
>
> </td>
> <td>
>
>
> Affected
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> COMETLAKE_L
>
> </td>
> <td>
>
>
> 06_A6H
>
> </td>
> <td>
>
>
> Affected
>
> </td>
> <td>
>
>
> Affected
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> ROCKETLAKE
>
> </td>
> <td>
>
>
> 06_A7H
>
> </td>
> <td>
>
>
> Not affected
>
> </td>
> <td>
>
>
> Affected
>
> </td>
> </tr>
> </tbody>
> </table>

- All affected CPUs enumerate Enhanced IBRS feature.

- IBPB isolation is affected on all ITS affected CPUs, and need a microcode update for mitigation.

- None of the affected CPUs enumerate BHI_CTRL which was introduced in Golden Cove (Alder Lake and Sapphire Rapids). This can help guests to determine the host's affected status.

- Intel Atom CPUs are not affected by ITS.

<a id="rst-mitigation"></a>

## Mitigation

As only the indirect branches and RETs that have their last byte of instruction in the lower half of the cacheline are vulnerable to ITS, the basic idea behind the mitigation is to not allow indirect branches in the lower half.

This is achieved by relying on existing retpoline support in the kernel, and in compilers. ITS-vulnerable retpoline sites are runtime patched to point to newly added ITS-safe thunks. These safe thunks consists of indirect branch in the second half of the cacheline. Not all retpoline sites are patched to thunks, if a retpoline site is evaluated to be ITS-safe, it is replaced with an inline indirect branch.

<a id="rst-dynamic-thunks"></a>

### Dynamic thunks

From a dynamically allocated pool of safe-thunks, each vulnerable site is replaced with a new thunk, such that they get a unique address. This could improve the branch prediction accuracy. Also, it is a defense-in-depth measure against aliasing.

Note, for simplicity, indirect branches in eBPF programs are always replaced with a jump to a static thunk in \__x86_indirect_its_thunk_array. If required, in future this can be changed to use dynamic thunks.

All vulnerable RETs are replaced with a static thunk, they do not use dynamic thunks. This is because RETs get their prediction from RSB mostly that does not depend on source address. RETs that underflow RSB may benefit from dynamic thunks. But, RETs significantly outnumber indirect branches, and any benefit from a unique source address could be outweighed by the increased icache footprint and iTLB pressure.

<a id="rst-retpoline"></a>

### Retpoline

Retpoline sequence also mitigates ITS-unsafe indirect branches. For this reason, when retpoline is enabled, ITS mitigation only relocates the RETs to safe thunks. Unless user requested the RSB-stuffing mitigation.

<a id="rst-rsb-stuffing"></a>

### RSB Stuffing

RSB-stuffing via Call Depth Tracking is a mitigation for Retbleed RSB-underflow attacks. And it also mitigates RETs that are vulnerable to ITS.

<a id="rst-mitigation-in-guests"></a>

#### Mitigation in guests

All guests deploy ITS mitigation by default, irrespective of eIBRS enumeration and Family/Model of the guest. This is because eIBRS feature could be hidden from a guest. One exception to this is when a guest enumerates BHI_DIS_S, which indicates that the guest is running on an unaffected host.

To prevent guests from unnecessarily deploying the mitigation on unaffected platforms, Intel has defined ITS_NO bit(62) in MSR IA32_ARCH_CAPABILITIES. When a guest sees this bit set, it should not enumerate the ITS bug. Note, this bit is not set by any hardware, but is **intended for VMMs to synthesize** it for guests as per the host's affected status.

<a id="rst-mitigation-options"></a>

#### Mitigation options

The ITS mitigation can be controlled using the "indirect_target_selection" kernel parameter. The available options are:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> on
>
> </td>
> <td>
>
>
> (default)  Deploy the "Aligned branch/return thunks" mitigation. If spectre_v2 mitigation enables retpoline, aligned-thunks are only deployed for the affected RET instructions. Retpoline mitigates indirect branches.
>
> </td>
> </tr>
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
> Disable ITS mitigation.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> vmexit
>
> </td>
> <td>
>
>
> Equivalent to "=on" if the CPU is affected by guest/host isolation part of ITS. Otherwise, mitigation is not deployed. This option is useful when host userspace is not in the threat model, and only attacks from guest to host are considered.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> stuff
>
> </td>
> <td>
>
>
> Deploy RSB-fill mitigation when retpoline is also deployed. Otherwise, deploy the default mitigation. When retpoline mitigation is enabled, RSB-stuffing via Call-Depth-Tracking also mitigates ITS.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> force
>
> </td>
> <td>
>
>
> Force the ITS bug and deploy the default mitigation.
>
> </td>
> </tr>
> </tbody>
> </table>

<a id="rst-sysfs-reporting"></a>

## Sysfs reporting

The sysfs file showing ITS mitigation status is:

> /sys/devices/system/cpu/vulnerabilities/indirect_target_selection

Note, microcode mitigation status is not reported in this file.

The possible values in this file are:


<table>
<tbody>
<tr>
<td>


Not affected

</td>
<td>


The processor is not vulnerable.

</td>
</tr>
<tr>
<td>


Vulnerable

</td>
<td>


System is vulnerable and no mitigation has been applied.

</td>
</tr>
<tr>
<td>


Vulnerable, KVM: Not affected

</td>
<td>


System is vulnerable to intra-mode BTI, but not affected by eIBRS guest/host isolation.

</td>
</tr>
<tr>
<td>


Mitigation: Aligned branch/return thunks

</td>
<td>


The mitigation is enabled, affected indirect branches and RETs are relocated to safe thunks.

</td>
</tr>
<tr>
<td>


Mitigation: Retpolines, Stuffing RSB

</td>
<td>


The mitigation is enabled using retpoline and RSB stuffing.

</td>
</tr>
</tbody>
</table>

<a id="rst-references"></a>

## References

<a id="rst-f1"></a>



**[1]** Microcode repository - [https://github.com/intel/Intel-Linux-Processor-Microcode-Data-Files](<https://github.com/intel/Intel-Linux-Processor-Microcode-Data-Files>)

<a id="rst-f2"></a>



**[2]** Affected Processors list - [https://www.intel.com/content/www/us/en/developer/topic-technology/software-security-guidance/processors-affected-consolidated-product-cpu-model.html](<https://www.intel.com/content/www/us/en/developer/topic-technology/software-security-guidance/processors-affected-consolidated-product-cpu-model.html>)

<a id="rst-f3"></a>



**[3]** Affected Processors list (machine readable) - [https://github.com/intel/Intel-affected-processor-list](<https://github.com/intel/Intel-affected-processor-list>)
