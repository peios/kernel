---
title: "Register File Data Sampling (RFDS)"
type: reference
description: "Register File Data Sampling (RFDS) is a microarchitectural vulnerability that only affects Intel Atom parts(also branded as E-cores). RFDS may allow a malicious actor to infer data values previously used in floating point registers, vector…"
---

<a id="rst-register-file-data-sampling-rfds"></a>

Register File Data Sampling (RFDS) is a microarchitectural vulnerability that only affects Intel Atom parts(also branded as E-cores). RFDS may allow a malicious actor to infer data values previously used in floating point registers, vector registers, or integer registers. RFDS does not provide the ability to choose which data is inferred. CVE-2023-28746 is assigned to RFDS.

<a id="rst-affected-processors"></a>

## Affected Processors

Below is the list of affected Intel processors <a id="rst-footnote-reference-1"></a>[1](#rst-f1):

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
> </tr>
> </thead>
> <tbody>
> <tr>
> <td>
>
>
> ATOM_GOLDMONT
>
> </td>
> <td>
>
>
> 06_5CH
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> ATOM_GOLDMONT_D
>
> </td>
> <td>
>
>
> 06_5FH
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> ATOM_GOLDMONT_PLUS
>
> </td>
> <td>
>
>
> 06_7AH
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> ATOM_TREMONT_D
>
> </td>
> <td>
>
>
> 06_86H
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> ATOM_TREMONT
>
> </td>
> <td>
>
>
> 06_96H
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> ALDERLAKE
>
> </td>
> <td>
>
>
> 06_97H
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> ALDERLAKE_L
>
> </td>
> <td>
>
>
> 06_9AH
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> ATOM_TREMONT_L
>
> </td>
> <td>
>
>
> 06_9CH
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> RAPTORLAKE
>
> </td>
> <td>
>
>
> 06_B7H
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> RAPTORLAKE_P
>
> </td>
> <td>
>
>
> 06_BAH
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> ATOM_GRACEMONT
>
> </td>
> <td>
>
>
> 06_BEH
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> RAPTORLAKE_S
>
> </td>
> <td>
>
>
> 06_BFH
>
> </td>
> </tr>
> </tbody>
> </table>

<a id="rst-mitigation"></a>

## Mitigation

Intel released a microcode update that enables software to clear sensitive information using the VERW instruction. Like MDS, RFDS deploys the same mitigation strategy to force the CPU to clear the affected buffers before an attacker can extract the secrets. This is achieved by using the otherwise unused and obsolete VERW instruction in combination with a microcode update. The microcode clears the affected CPU buffers when the VERW instruction is executed.

<a id="rst-mitigation-points"></a>

### Mitigation points

VERW is executed by the kernel before returning to user space, and by KVM before VMentry. None of the affected cores support SMT, so VERW is not required at C-state transitions.

<a id="rst-new-bits-in-ia32-arch-capabilities"></a>

### New bits in IA32_ARCH_CAPABILITIES

Newer processors and microcode update on existing affected processors added new bits to IA32_ARCH_CAPABILITIES MSR. These bits can be used to enumerate vulnerability and mitigation capability:

- Bit 27 - RFDS_NO - When set, processor is not affected by RFDS.

- Bit 28 - RFDS_CLEAR - When set, processor is affected by RFDS, and has the microcode that clears the affected buffers on VERW execution.

<a id="rst-mitigation-control-on-the-kernel-command-line"></a>

### Mitigation control on the kernel command line

The kernel command line allows to control RFDS mitigation at boot time with the parameter "reg_file_data_sampling=". The valid arguments are:

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
> If the CPU is vulnerable, enable mitigation; CPU buffer clearing on exit to userspace and before entering a VM.
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
> Disables mitigation.
>
> </td>
> </tr>
> </tbody>
> </table>

Mitigation default is selected by CONFIG_MITIGATION_RFDS.

<a id="rst-mitigation-status-information"></a>

### Mitigation status information

The Linux kernel provides a sysfs interface to enumerate the current vulnerability status of the system: whether the system is vulnerable, and which mitigations are active. The relevant sysfs file is:

> /sys/devices/system/cpu/vulnerabilities/reg_file_data_sampling

The possible values in this file are:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> 'Not affected'
>
> </td>
> <td>
>
>
> The processor is not vulnerable
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 'Vulnerable'
>
> </td>
> <td>
>
>
> The processor is vulnerable, but no mitigation enabled
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 'Vulnerable: No microcode'
>
> </td>
> <td>
>
>
> The processor is vulnerable but microcode is not updated.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 'Mitigation: Clear Register File'
>
> </td>
> <td>
>
>
> The processor is vulnerable and the CPU buffer clearing mitigation is enabled.
>
> </td>
> </tr>
> </tbody>
> </table>

<a id="rst-references"></a>

### References

<a id="rst-f1"></a>



**[1]** Affected Processors [https://www.intel.com/content/www/us/en/developer/topic-technology/software-security-guidance/processors-affected-consolidated-product-cpu-model.html](<https://www.intel.com/content/www/us/en/developer/topic-technology/software-security-guidance/processors-affected-consolidated-product-cpu-model.html>)
