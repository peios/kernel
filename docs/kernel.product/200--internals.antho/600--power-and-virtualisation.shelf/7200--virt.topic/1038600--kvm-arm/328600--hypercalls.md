---
title: "KVM/arm64-specific hypercalls exposed to guests"
type: reference
description: "This file documents the KVM/arm64-specific hypercalls which may be exposed by KVM/arm64 to guest operating systems. These hypercalls are issued using the HVC instruction according to version 1.1 of the Arm SMC Calling Convention…"
---

<a id="rst-kvm-arm64-specific-hypercalls-exposed-to-guests"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

This file documents the KVM/arm64-specific hypercalls which may be exposed by KVM/arm64 to guest operating systems. These hypercalls are issued using the HVC instruction according to version 1.1 of the Arm SMC Calling Convention (DEN0028/C):

[https://developer.arm.com/docs/den0028/c](<https://developer.arm.com/docs/den0028/c>)

All KVM/arm64-specific hypercalls are allocated within the "Vendor Specific Hypervisor Service Call" range with a UID of `28b46fb6-2ec5-11e9-a9ca-4b564d003a74`. This UID should be queried by the guest using the standard "Call UID" function for the service range in order to determine that the KVM/arm64-specific hypercalls are available.

<a id="rst-arm-smccc-vendor-hyp-kvm-features-func-id"></a>

## `ARM_SMCCC_VENDOR_HYP_KVM_FEATURES_FUNC_ID`

Provides a discovery mechanism for other KVM/arm64 hypercalls.


<table>
<tbody>
<tr>
<td>


Presence:

</td>
<td colspan="3">


Mandatory for the KVM/arm64 UID

</td>
</tr>
<tr>
<td>


Calling convention:

</td>
<td colspan="3">


HVC32

</td>
</tr>
<tr>
<td>


Function ID:

</td>
<td>


(uint32)

</td>
<td colspan="2">


0x86000000

</td>
</tr>
<tr>
<td>


Arguments:

</td>
<td colspan="3">


None

</td>
</tr>
<tr>
<td rowspan="4">


Return Values:

</td>
<td>


(uint32)

</td>
<td>


R0

</td>
<td>


Bitmap of available function numbers 0-31

</td>
</tr>
<tr>
<td>


(uint32)

</td>
<td>


R1

</td>
<td>


Bitmap of available function numbers 32-63

</td>
</tr>
<tr>
<td>


(uint32)

</td>
<td>


R2

</td>
<td>


Bitmap of available function numbers 64-95

</td>
</tr>
<tr>
<td>


(uint32)

</td>
<td>


R3

</td>
<td>


Bitmap of available function numbers 96-127

</td>
</tr>
</tbody>
</table>

<a id="rst-arm-smccc-vendor-hyp-kvm-ptp-func-id"></a>

## `ARM_SMCCC_VENDOR_HYP_KVM_PTP_FUNC_ID`

See [ptp_kvm.rst](~kernel/internals/virt/kvm-arm/ptp-kvm)

<a id="rst-arm-smccc-kvm-func-hyp-meminfo"></a>

## `ARM_SMCCC_KVM_FUNC_HYP_MEMINFO`

Query the memory protection parameters for a pKVM protected virtual machine.


<table>
<tbody>
<tr>
<td>


Presence:

</td>
<td colspan="3">


Optional; pKVM protected guests only.

</td>
</tr>
<tr>
<td>


Calling convention:

</td>
<td colspan="3">


HVC64

</td>
</tr>
<tr>
<td>


Function ID:

</td>
<td>


(uint32)

</td>
<td colspan="2">


0xC6000002

</td>
</tr>
<tr>
<td rowspan="3">


Arguments:

</td>
<td>


(uint64)

</td>
<td>


R1

</td>
<td>


Reserved / Must be zero

</td>
</tr>
<tr>
<td>


(uint64)

</td>
<td>


R2

</td>
<td>


Reserved / Must be zero

</td>
</tr>
<tr>
<td>


(uint64)

</td>
<td>


R3

</td>
<td>


Reserved / Must be zero

</td>
</tr>
<tr>
<td>


Return Values:

</td>
<td>


(int64)

</td>
<td>


R0

</td>
<td>


`INVALID_PARAMETER (-3)` on error, else memory protection granule in bytes

</td>
</tr>
</tbody>
</table>

<a id="rst-arm-smccc-kvm-func-mem-share"></a>

## `ARM_SMCCC_KVM_FUNC_MEM_SHARE`

Share a region of memory with the KVM host, granting it read, write and execute permissions. The size of the region is equal to the memory protection granule advertised by `ARM_SMCCC_KVM_FUNC_HYP_MEMINFO`.


<table>
<tbody>
<tr>
<td>


Presence:

</td>
<td colspan="3">


Optional; pKVM protected guests only.

</td>
</tr>
<tr>
<td>


Calling convention:

</td>
<td colspan="3">


HVC64

</td>
</tr>
<tr>
<td>


Function ID:

</td>
<td>


(uint32)

</td>
<td colspan="2">


0xC6000003

</td>
</tr>
<tr>
<td rowspan="3">


Arguments:

</td>
<td>


(uint64)

</td>
<td>


R1

</td>
<td>


Base IPA of memory region to share

</td>
</tr>
<tr>
<td>


(uint64)

</td>
<td>


R2

</td>
<td>


Reserved / Must be zero

</td>
</tr>
<tr>
<td>


(uint64)

</td>
<td>


R3

</td>
<td>


Reserved / Must be zero

</td>
</tr>
<tr>
<td rowspan="2">


Return Values:

</td>
<td rowspan="2">


(int64)

</td>
<td rowspan="2">


R0

</td>
<td>


`SUCCESS (0)`

</td>
</tr>
<tr>
<td>


`INVALID_PARAMETER (-3)`

</td>
</tr>
</tbody>
</table>

<a id="rst-arm-smccc-kvm-func-mem-unshare"></a>

## `ARM_SMCCC_KVM_FUNC_MEM_UNSHARE`

Revoke access permission from the KVM host to a memory region previously shared with `ARM_SMCCC_KVM_FUNC_MEM_SHARE`. The size of the region is equal to the memory protection granule advertised by `ARM_SMCCC_KVM_FUNC_HYP_MEMINFO`.


<table>
<tbody>
<tr>
<td>


Presence:

</td>
<td colspan="3">


Optional; pKVM protected guests only.

</td>
</tr>
<tr>
<td>


Calling convention:

</td>
<td colspan="3">


HVC64

</td>
</tr>
<tr>
<td>


Function ID:

</td>
<td>


(uint32)

</td>
<td colspan="2">


0xC6000004

</td>
</tr>
<tr>
<td rowspan="3">


Arguments:

</td>
<td>


(uint64)

</td>
<td>


R1

</td>
<td>


Base IPA of memory region to unshare

</td>
</tr>
<tr>
<td>


(uint64)

</td>
<td>


R2

</td>
<td>


Reserved / Must be zero

</td>
</tr>
<tr>
<td>


(uint64)

</td>
<td>


R3

</td>
<td>


Reserved / Must be zero

</td>
</tr>
<tr>
<td rowspan="2">


Return Values:

</td>
<td rowspan="2">


(int64)

</td>
<td rowspan="2">


R0

</td>
<td>


`SUCCESS (0)`

</td>
</tr>
<tr>
<td>


`INVALID_PARAMETER (-3)`

</td>
</tr>
</tbody>
</table>

<a id="rst-arm-smccc-kvm-func-mmio-guard"></a>

## `ARM_SMCCC_KVM_FUNC_MMIO_GUARD`

Request that a given memory region is handled as MMIO by the hypervisor, allowing accesses to this region to be emulated by the KVM host. The size of the region is equal to the memory protection granule advertised by `ARM_SMCCC_KVM_FUNC_HYP_MEMINFO`.


<table>
<tbody>
<tr>
<td>


Presence:

</td>
<td colspan="3">


Optional; pKVM protected guests only.

</td>
</tr>
<tr>
<td>


Calling convention:

</td>
<td colspan="3">


HVC64

</td>
</tr>
<tr>
<td>


Function ID:

</td>
<td>


(uint32)

</td>
<td colspan="2">


0xC6000007

</td>
</tr>
<tr>
<td rowspan="3">


Arguments:

</td>
<td>


(uint64)

</td>
<td>


R1

</td>
<td>


Base IPA of MMIO memory region

</td>
</tr>
<tr>
<td>


(uint64)

</td>
<td>


R2

</td>
<td>


Reserved / Must be zero

</td>
</tr>
<tr>
<td>


(uint64)

</td>
<td>


R3

</td>
<td>


Reserved / Must be zero

</td>
</tr>
<tr>
<td rowspan="2">


Return Values:

</td>
<td rowspan="2">


(int64)

</td>
<td rowspan="2">


R0

</td>
<td>


`SUCCESS (0)`

</td>
</tr>
<tr>
<td>


`INVALID_PARAMETER (-3)`

</td>
</tr>
</tbody>
</table>

<a id="rst-arm-smccc-vendor-hyp-kvm-discover-impl-ver-func-id"></a>

## `ARM_SMCCC_VENDOR_HYP_KVM_DISCOVER_IMPL_VER_FUNC_ID`

Request the target CPU implementation version information and the number of target implementations for the Guest VM.


<table>
<tbody>
<tr>
<td>


Presence:

</td>
<td colspan="3">


Optional;  KVM/ARM64 Guests only

</td>
</tr>
<tr>
<td>


Calling convention:

</td>
<td colspan="3">


HVC64

</td>
</tr>
<tr>
<td>


Function ID:

</td>
<td>


(uint32)

</td>
<td colspan="2">


0xC6000040

</td>
</tr>
<tr>
<td>


Arguments:

</td>
<td colspan="3">


None

</td>
</tr>
<tr>
<td rowspan="7">


Return Values:

</td>
<td rowspan="2">


(int64)

</td>
<td rowspan="2">


R0

</td>
<td>


`SUCCESS (0)`

</td>
</tr>
<tr>
<td>


`NOT_SUPPORTED (-1)`

</td>
</tr>
<tr>
<td rowspan="3">


(uint64)

</td>
<td rowspan="3">


R1

</td>
<td>


Bits \[63:32\] Reserved/Must be zero

</td>
</tr>
<tr>
<td>


Bits \[31:16\] Major version

</td>
</tr>
<tr>
<td>


Bits \[15:0\] Minor version

</td>
</tr>
<tr>
<td>


(uint64)

</td>
<td>


R2

</td>
<td>


Number of target implementations

</td>
</tr>
<tr>
<td>


(uint64)

</td>
<td>


R3

</td>
<td>


Reserved / Must be zero

</td>
</tr>
</tbody>
</table>

<a id="rst-arm-smccc-vendor-hyp-kvm-discover-impl-cpus-func-id"></a>

## `ARM_SMCCC_VENDOR_HYP_KVM_DISCOVER_IMPL_CPUS_FUNC_ID`

Request the target CPU implementation information for the Guest VM. The Guest kernel will use this information to enable the associated errata.


<table>
<tbody>
<tr>
<td>


Presence:

</td>
<td colspan="3">


Optional;  KVM/ARM64 Guests only

</td>
</tr>
<tr>
<td>


Calling convention:

</td>
<td colspan="3">


HVC64

</td>
</tr>
<tr>
<td>


Function ID:

</td>
<td>


(uint32)

</td>
<td colspan="2">


0xC6000041

</td>
</tr>
<tr>
<td rowspan="3">


Arguments:

</td>
<td>


(uint64)

</td>
<td>


R1

</td>
<td>


selected implementation index

</td>
</tr>
<tr>
<td>


(uint64)

</td>
<td>


R2

</td>
<td>


Reserved / Must be zero

</td>
</tr>
<tr>
<td>


(uint64)

</td>
<td>


R3

</td>
<td>


Reserved / Must be zero

</td>
</tr>
<tr>
<td rowspan="5">


Return Values:

</td>
<td rowspan="2">


(int64)

</td>
<td rowspan="2">


R0

</td>
<td>


`SUCCESS (0)`

</td>
</tr>
<tr>
<td>


`INVALID_PARAMETER (-3)`

</td>
</tr>
<tr>
<td>


(uint64)

</td>
<td>


R1

</td>
<td>


MIDR_EL1 of the selected implementation

</td>
</tr>
<tr>
<td>


(uint64)

</td>
<td>


R2

</td>
<td>


REVIDR_EL1 of the selected implementation

</td>
</tr>
<tr>
<td>


(uint64)

</td>
<td>


R3

</td>
<td>


AIDR_EL1  of the selected implementation

</td>
</tr>
</tbody>
</table>
