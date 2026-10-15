---
title: "ARM64 CPU Feature Registers"
type: reference
description: "Author: Suzuki K Poulose <suzuki.poulose@arm.com>"
---

<a id="rst-arm64-cpu-feature-registers"></a>

Author: Suzuki K Poulose &lt;[suzuki.poulose@arm.com](<mailto:suzuki.poulose@arm.com>)&gt;

This file describes the ABI for exporting the AArch64 CPU ID/feature registers to userspace. The availability of this ABI is advertised via the HWCAP_CPUID in HWCAPs.

<a id="rst-motivation"></a>

## 1. Motivation

The ARM architecture defines a set of feature registers, which describe the capabilities of the CPU/system. Access to these system registers is restricted from EL0 and there is no reliable way for an application to extract this information to make better decisions at runtime. There is limited information available to the application via HWCAPs, however there are some issues with their usage.

> - **a)** Any change to the HWCAPs requires an update to userspace (e.g libc) to detect the new changes, which can take a long time to appear in distributions. Exposing the registers allows applications to get the information without requiring updates to the toolchains.
>
> - **b)** Access to HWCAPs is sometimes limited (e.g prior to libc, or when ld is initialised at startup time).
>
> - **c)** HWCAPs cannot represent non-boolean information effectively. The architecture defines a canonical format for representing features in the ID registers; this is well defined and is capable of representing all valid architecture variations.

<a id="rst-requirements"></a>

## 2. Requirements

> - **a)** Safety:
>
>   Applications should be able to use the information provided by the infrastructure to run safely across the system. This has greater implications on a system with heterogeneous CPUs. The infrastructure exports a value that is safe across all the available CPU on the system.
>
>   e.g, If at least one CPU doesn't implement CRC32 instructions, while others do, we should report that the CRC32 is not implemented. Otherwise an application could crash when scheduled on the CPU which doesn't support CRC32.
>
> - **b)** Security:
>
>   Applications should only be able to receive information that is relevant to the normal operation in userspace. Hence, some of the fields are masked out(i.e, made invisible) and their values are set to indicate the feature is 'not supported'. See Section 4 for the list of visible features. Also, the kernel may manipulate the fields based on what it supports. e.g, If FP is not supported by the kernel, the values could indicate that the FP is not available (even when the CPU provides it).
>
> - **c)** Implementation Defined Features
>
>   The infrastructure doesn't expose any register which is IMPLEMENTATION DEFINED as per ARMv8-A Architecture.
>
> - **d)** CPU Identification:
>
>   MIDR_EL1 is exposed to help identify the processor. On a heterogeneous system, this could be racy (just like getcpu()). The process could be migrated to another CPU by the time it uses the register value, unless the CPU affinity is set. Hence, there is no guarantee that the value reflects the processor that it is currently executing on. REVIDR and AIDR are not exposed due to this constraint, as these registers only make sense in conjunction with the MIDR. Alternately, MIDR_EL1, REVIDR_EL1, and AIDR_EL1 are exposed via sysfs at:
>
>
>
>   ```text
>   /sys/devices/system/cpu/cpu$ID/regs/identification/
>                                                 \- midr_el1
>                                                 \- revidr_el1
>                                                 \- aidr_el1
>   ```

<a id="rst-implementation"></a>

## 3. Implementation

The infrastructure is built on the emulation of the 'MRS' instruction. Accessing a restricted system register from an application generates an exception and ends up in SIGILL being delivered to the process. The infrastructure hooks into the exception handler and emulates the operation if the source belongs to the supported system register space.

The infrastructure emulates only the following system register space:



```text
Op0=3, Op1=0, CRn=0, CRm=0,2,3,4,5,6,7
```

(See Table C5-6 'System instruction encodings for non-Debug System register accesses' in ARMv8 ARM DDI 0487A.h, for the list of registers).

The following rules are applied to the value returned by the infrastructure:

> - **a)** The value of an 'IMPLEMENTATION DEFINED' field is set to 0.
>
> - **b)** The value of a reserved field is populated with the reserved value as defined by the architecture.
>
> - **c)** The value of a 'visible' field holds the system wide safe value for the particular feature (except for MIDR_EL1, see section 4).
>
> - **d)** All other fields (i.e, invisible fields) are set to indicate the feature is missing (as defined by the architecture).

<a id="rst-list-of-registers-with-visible-features"></a>

## 4. List of registers with visible features

> 1. ID_AA64ISAR0_EL1 - Instruction Set Attribute Register 0
>
>
>    <table>
>    <tbody>
>    <tr>
>    <td>
>
>
>    Name
>
>    </td>
>    <td>
>
>
>    bits
>
>    </td>
>    <td>
>
>
>    visible
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    RNDR
>
>    </td>
>    <td>
>
>
>    \[63-60\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    TS
>
>    </td>
>    <td>
>
>
>    \[55-52\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    FHM
>
>    </td>
>    <td>
>
>
>    \[51-48\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    DP
>
>    </td>
>    <td>
>
>
>    \[47-44\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    SM4
>
>    </td>
>    <td>
>
>
>    \[43-40\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    SM3
>
>    </td>
>    <td>
>
>
>    \[39-36\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    SHA3
>
>    </td>
>    <td>
>
>
>    \[35-32\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    RDM
>
>    </td>
>    <td>
>
>
>    \[31-28\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    ATOMICS
>
>    </td>
>    <td>
>
>
>    \[23-20\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    CRC32
>
>    </td>
>    <td>
>
>
>    \[19-16\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    SHA2
>
>    </td>
>    <td>
>
>
>    \[15-12\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    SHA1
>
>    </td>
>    <td>
>
>
>    \[11-8\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    AES
>
>    </td>
>    <td>
>
>
>    \[7-4\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    </tbody>
>    </table>
>
> 2. ID_AA64PFR0_EL1 - Processor Feature Register 0
>
>
>    <table>
>    <tbody>
>    <tr>
>    <td>
>
>
>    Name
>
>    </td>
>    <td>
>
>
>    bits
>
>    </td>
>    <td>
>
>
>    visible
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    DIT
>
>    </td>
>    <td>
>
>
>    \[51-48\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    MPAM
>
>    </td>
>    <td>
>
>
>    \[43-40\]
>
>    </td>
>    <td>
>
>
>    n
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    SVE
>
>    </td>
>    <td>
>
>
>    \[35-32\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    GIC
>
>    </td>
>    <td>
>
>
>    \[27-24\]
>
>    </td>
>    <td>
>
>
>    n
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    AdvSIMD
>
>    </td>
>    <td>
>
>
>    \[23-20\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    FP
>
>    </td>
>    <td>
>
>
>    \[19-16\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    EL3
>
>    </td>
>    <td>
>
>
>    \[15-12\]
>
>    </td>
>    <td>
>
>
>    n
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    EL2
>
>    </td>
>    <td>
>
>
>    \[11-8\]
>
>    </td>
>    <td>
>
>
>    n
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    EL1
>
>    </td>
>    <td>
>
>
>    \[7-4\]
>
>    </td>
>    <td>
>
>
>    n
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    EL0
>
>    </td>
>    <td>
>
>
>    \[3-0\]
>
>    </td>
>    <td>
>
>
>    n
>
>    </td>
>    </tr>
>    </tbody>
>    </table>
>
> 3. ID_AA64PFR1_EL1 - Processor Feature Register 1
>
>
>    <table>
>    <tbody>
>    <tr>
>    <td>
>
>
>    Name
>
>    </td>
>    <td>
>
>
>    bits
>
>    </td>
>    <td>
>
>
>    visible
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    SME
>
>    </td>
>    <td>
>
>
>    \[27-24\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    MTE
>
>    </td>
>    <td>
>
>
>    \[11-8\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    SSBS
>
>    </td>
>    <td>
>
>
>    \[7-4\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    BT
>
>    </td>
>    <td>
>
>
>    \[3-0\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    </tbody>
>    </table>
>
> 4. MIDR_EL1 - Main ID Register
>
>
>    <table>
>    <tbody>
>    <tr>
>    <td>
>
>
>    Name
>
>    </td>
>    <td>
>
>
>    bits
>
>    </td>
>    <td>
>
>
>    visible
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    Implementer
>
>    </td>
>    <td>
>
>
>    \[31-24\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    Variant
>
>    </td>
>    <td>
>
>
>    \[23-20\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    Architecture
>
>    </td>
>    <td>
>
>
>    \[19-16\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    PartNum
>
>    </td>
>    <td>
>
>
>    \[15-4\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    Revision
>
>    </td>
>    <td>
>
>
>    \[3-0\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    </tbody>
>    </table>
>
> > NOTE: The 'visible' fields of MIDR_EL1 will contain the value as available on the CPU where it is fetched and is not a system wide safe value.
>
> 5. ID_AA64ISAR1_EL1 - Instruction set attribute register 1
>
>
>    <table>
>    <tbody>
>    <tr>
>    <td>
>
>
>    Name
>
>    </td>
>    <td>
>
>
>    bits
>
>    </td>
>    <td>
>
>
>    visible
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    I8MM
>
>    </td>
>    <td>
>
>
>    \[55-52\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    DGH
>
>    </td>
>    <td>
>
>
>    \[51-48\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    BF16
>
>    </td>
>    <td>
>
>
>    \[47-44\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    SB
>
>    </td>
>    <td>
>
>
>    \[39-36\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    FRINTTS
>
>    </td>
>    <td>
>
>
>    \[35-32\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    GPI
>
>    </td>
>    <td>
>
>
>    \[31-28\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    GPA
>
>    </td>
>    <td>
>
>
>    \[27-24\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    LRCPC
>
>    </td>
>    <td>
>
>
>    \[23-20\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    FCMA
>
>    </td>
>    <td>
>
>
>    \[19-16\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    JSCVT
>
>    </td>
>    <td>
>
>
>    \[15-12\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    API
>
>    </td>
>    <td>
>
>
>    \[11-8\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    APA
>
>    </td>
>    <td>
>
>
>    \[7-4\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    DPB
>
>    </td>
>    <td>
>
>
>    \[3-0\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    </tbody>
>    </table>
>
> 6. ID_AA64MMFR0_EL1 - Memory model feature register 0
>
>
>    <table>
>    <tbody>
>    <tr>
>    <td>
>
>
>    Name
>
>    </td>
>    <td>
>
>
>    bits
>
>    </td>
>    <td>
>
>
>    visible
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    ECV
>
>    </td>
>    <td>
>
>
>    \[63-60\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    </tbody>
>    </table>
>
> 7. ID_AA64MMFR2_EL1 - Memory model feature register 2
>
>
>    <table>
>    <tbody>
>    <tr>
>    <td>
>
>
>    Name
>
>    </td>
>    <td>
>
>
>    bits
>
>    </td>
>    <td>
>
>
>    visible
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    AT
>
>    </td>
>    <td>
>
>
>    \[35-32\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    </tbody>
>    </table>
>
> 8. ID_AA64ZFR0_EL1 - SVE feature ID register 0
>
>
>    <table>
>    <tbody>
>    <tr>
>    <td>
>
>
>    Name
>
>    </td>
>    <td>
>
>
>    bits
>
>    </td>
>    <td>
>
>
>    visible
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    F64MM
>
>    </td>
>    <td>
>
>
>    \[59-56\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    F32MM
>
>    </td>
>    <td>
>
>
>    \[55-52\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    I8MM
>
>    </td>
>    <td>
>
>
>    \[47-44\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    SM4
>
>    </td>
>    <td>
>
>
>    \[43-40\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    SHA3
>
>    </td>
>    <td>
>
>
>    \[35-32\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    B16B16
>
>    </td>
>    <td>
>
>
>    \[27-24\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    BF16
>
>    </td>
>    <td>
>
>
>    \[23-20\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    BitPerm
>
>    </td>
>    <td>
>
>
>    \[19-16\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    AES
>
>    </td>
>    <td>
>
>
>    \[7-4\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    SVEVer
>
>    </td>
>    <td>
>
>
>    \[3-0\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    </tbody>
>    </table>
>
> 8. ID_AA64MMFR1_EL1 - Memory model feature register 1
>
>
>    <table>
>    <tbody>
>    <tr>
>    <td>
>
>
>    Name
>
>    </td>
>    <td>
>
>
>    bits
>
>    </td>
>    <td>
>
>
>    visible
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    AFP
>
>    </td>
>    <td>
>
>
>    \[47-44\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    </tbody>
>    </table>
>
> 9. ID_AA64ISAR2_EL1 - Instruction set attribute register 2
>
>
>    <table>
>    <tbody>
>    <tr>
>    <td>
>
>
>    Name
>
>    </td>
>    <td>
>
>
>    bits
>
>    </td>
>    <td>
>
>
>    visible
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    CSSC
>
>    </td>
>    <td>
>
>
>    \[55-52\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    RPRFM
>
>    </td>
>    <td>
>
>
>    \[51-48\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    BC
>
>    </td>
>    <td>
>
>
>    \[23-20\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    MOPS
>
>    </td>
>    <td>
>
>
>    \[19-16\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    APA3
>
>    </td>
>    <td>
>
>
>    \[15-12\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    GPA3
>
>    </td>
>    <td>
>
>
>    \[11-8\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    RPRES
>
>    </td>
>    <td>
>
>
>    \[7-4\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    <tr>
>    <td>
>
>
>    WFXT
>
>    </td>
>    <td>
>
>
>    \[3-0\]
>
>    </td>
>    <td>
>
>
>    y
>
>    </td>
>    </tr>
>    </tbody>
>    </table>
>
> 10. MVFR0_EL1 - AArch32 Media and VFP Feature Register 0
>
> >
> > <table>
> > <tbody>
> > <tr>
> > <td>
> >
> >
> > Name
> >
> > </td>
> > <td>
> >
> >
> > bits
> >
> > </td>
> > <td>
> >
> >
> > visible
> >
> > </td>
> > </tr>
> > <tr>
> > <td>
> >
> >
> > FPDP
> >
> > </td>
> > <td>
> >
> >
> > \[11-8\]
> >
> > </td>
> > <td>
> >
> >
> > y
> >
> > </td>
> > </tr>
> > </tbody>
> > </table>
>
> 11. MVFR1_EL1 - AArch32 Media and VFP Feature Register 1
>
> >
> > <table>
> > <tbody>
> > <tr>
> > <td>
> >
> >
> > Name
> >
> > </td>
> > <td>
> >
> >
> > bits
> >
> > </td>
> > <td>
> >
> >
> > visible
> >
> > </td>
> > </tr>
> > <tr>
> > <td>
> >
> >
> > SIMDFMAC
> >
> > </td>
> > <td>
> >
> >
> > \[31-28\]
> >
> > </td>
> > <td>
> >
> >
> > y
> >
> > </td>
> > </tr>
> > <tr>
> > <td>
> >
> >
> > SIMDSP
> >
> > </td>
> > <td>
> >
> >
> > \[19-16\]
> >
> > </td>
> > <td>
> >
> >
> > y
> >
> > </td>
> > </tr>
> > <tr>
> > <td>
> >
> >
> > SIMDInt
> >
> > </td>
> > <td>
> >
> >
> > \[15-12\]
> >
> > </td>
> > <td>
> >
> >
> > y
> >
> > </td>
> > </tr>
> > <tr>
> > <td>
> >
> >
> > SIMDLS
> >
> > </td>
> > <td>
> >
> >
> > \[11-8\]
> >
> > </td>
> > <td>
> >
> >
> > y
> >
> > </td>
> > </tr>
> > </tbody>
> > </table>
>
> 12. ID_ISAR5_EL1 - AArch32 Instruction Set Attribute Register 5
>
> >
> > <table>
> > <tbody>
> > <tr>
> > <td>
> >
> >
> > Name
> >
> > </td>
> > <td>
> >
> >
> > bits
> >
> > </td>
> > <td>
> >
> >
> > visible
> >
> > </td>
> > </tr>
> > <tr>
> > <td>
> >
> >
> > CRC32
> >
> > </td>
> > <td>
> >
> >
> > \[19-16\]
> >
> > </td>
> > <td>
> >
> >
> > y
> >
> > </td>
> > </tr>
> > <tr>
> > <td>
> >
> >
> > SHA2
> >
> > </td>
> > <td>
> >
> >
> > \[15-12\]
> >
> > </td>
> > <td>
> >
> >
> > y
> >
> > </td>
> > </tr>
> > <tr>
> > <td>
> >
> >
> > SHA1
> >
> > </td>
> > <td>
> >
> >
> > \[11-8\]
> >
> > </td>
> > <td>
> >
> >
> > y
> >
> > </td>
> > </tr>
> > <tr>
> > <td>
> >
> >
> > AES
> >
> > </td>
> > <td>
> >
> >
> > \[7-4\]
> >
> > </td>
> > <td>
> >
> >
> > y
> >
> > </td>
> > </tr>
> > </tbody>
> > </table>

<a id="rst-appendix-i-example"></a>

## Appendix I: Example



```text
/*
 * Sample program to demonstrate the MRS emulation ABI.
 *
 * Copyright (C) 2015-2016, ARM Ltd
 *
 * Author: Suzuki K Poulose <suzuki.poulose@arm.com>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 */

#include <asm/hwcap.h>
#include <stdio.h>
#include <sys/auxv.h>

#define get_cpu_ftr(id) ({                                    \
              unsigned long __val;                            \
              asm("mrs %0, "#id : "=r" (__val));              \
              printf("%-20s: 0x%016lx\n", #id, __val);        \
      })

int main(void)
{

      if (!(getauxval(AT_HWCAP) & HWCAP_CPUID)) {
              fputs("CPUID registers unavailable\n", stderr);
              return 1;
      }

      get_cpu_ftr(ID_AA64ISAR0_EL1);
      get_cpu_ftr(ID_AA64ISAR1_EL1);
      get_cpu_ftr(ID_AA64MMFR0_EL1);
      get_cpu_ftr(ID_AA64MMFR1_EL1);
      get_cpu_ftr(ID_AA64PFR0_EL1);
      get_cpu_ftr(ID_AA64PFR1_EL1);
      get_cpu_ftr(ID_AA64DFR0_EL1);
      get_cpu_ftr(ID_AA64DFR1_EL1);

      get_cpu_ftr(MIDR_EL1);
      get_cpu_ftr(MPIDR_EL1);
      get_cpu_ftr(REVIDR_EL1);

#if 0
      /* Unexposed register access causes SIGILL */
      get_cpu_ftr(ID_MMFR0_EL1);
#endif

      return 0;
}
```
