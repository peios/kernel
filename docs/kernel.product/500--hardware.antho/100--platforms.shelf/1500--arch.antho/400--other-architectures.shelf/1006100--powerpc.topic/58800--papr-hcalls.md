---
title: "Hypercall Op-codes (hcalls)"
type: reference
description: "Virtualization on 64-bit Power Book3S Platforms is based on the PAPR specification 1 which describes the run-time environment for a guest operating system and how it should interact with the hypervisor for privileged operations. Currently…"
---

<a id="rst-hypercall-op-codes-hcalls"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-overview"></a>

## Overview

Virtualization on 64-bit Power Book3S Platforms is based on the PAPR specification <a id="rst-footnote-reference-1"></a>[1](#rst-footnote-1) which describes the run-time environment for a guest operating system and how it should interact with the hypervisor for privileged operations. Currently there are two PAPR compliant hypervisors:

- <strong>IBM PowerVM (PHYP)</strong>: IBM's proprietary hypervisor that supports AIX, IBM-i and  Linux as supported guests (termed as Logical Partitions or LPARS). It supports the full PAPR specification.

- <strong>Qemu/KVM</strong>: Supports PPC64 linux guests running on a PPC64 linux host. Though it only implements a subset of PAPR specification called LoPAPR <a id="rst-footnote-reference-2"></a>[2](#rst-footnote-2).

On PPC64 arch a guest kernel running on top of a PAPR hypervisor is called a <em>pSeries guest</em>. A pseries guest runs in a supervisor mode (HV=0) and must issue hypercalls to the hypervisor whenever it needs to perform an action that is hypervisor privileged <a id="rst-footnote-reference-3"></a>[3](#rst-footnote-3) or for other services managed by the hypervisor.

Hence a Hypercall (hcall) is essentially a request by the pseries guest asking hypervisor to perform a privileged operation on behalf of the guest. The guest issues a with necessary input operands. The hypervisor after performing the privilege operation returns a status code and output operands back to the guest.

<a id="rst-hcall-abi"></a>

## HCALL ABI

The ABI specification for a hcall between a pseries guest and PAPR hypervisor is covered in section 14.5.3 of ref <a id="rst-footnote-reference-4"></a>[2](#rst-footnote-2). Switch to the  Hypervisor context is done via the instruction <strong>HVCS</strong> that expects the Opcode for hcall is set in <em>r3</em> and any in-arguments for the hcall are provided in registers <em>r4-r12</em>. If values have to be passed through a memory buffer, the data stored in that buffer should be in Big-endian byte order.

Once control returns back to the guest after hypervisor has serviced the 'HVCS' instruction the return value of the hcall is available in <em>r3</em> and any out values are returned in registers <em>r4-r12</em>. Again like in case of in-arguments, any out values stored in a memory buffer will be in Big-endian byte order.

Powerpc arch code provides convenient wrappers named <strong>plpar\_hcall\_xxx</strong> defined in a arch specific header <a id="rst-footnote-reference-5"></a>[4](#rst-footnote-4) to issue hcalls from the linux kernel running as pseries guest.

<a id="rst-register-conventions"></a>

## Register Conventions

Any hcall should follow same register convention as described in section 2.2.1.1 of "64-Bit ELF V2 ABI Specification: Power Architecture"<a id="rst-footnote-reference-6"></a>[5](#rst-footnote-5). Table below summarizes these conventions:


<table>
<thead>
<tr>
<th>



Register Range

</th>
<th>



Volatile (Y/N)

</th>
<th>



Purpose

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



r0

</td>
<td>



Y

</td>
<td>



Optional-usage

</td>
</tr>
<tr>
<td>



r1

</td>
<td>



N

</td>
<td>



Stack Pointer

</td>
</tr>
<tr>
<td>



r2

</td>
<td>



N

</td>
<td>



TOC

</td>
</tr>
<tr>
<td>



r3

</td>
<td>



Y

</td>
<td>



hcall opcode/return value

</td>
</tr>
<tr>
<td>



r4-r10

</td>
<td>



Y

</td>
<td>



in and out values

</td>
</tr>
<tr>
<td>



r11

</td>
<td>



Y

</td>
<td>



Optional-usage/Environmental pointer

</td>
</tr>
<tr>
<td>



r12

</td>
<td>



Y

</td>
<td>



Optional-usage/Function entry address at global entry point

</td>
</tr>
<tr>
<td>



r13

</td>
<td>



N

</td>
<td>



Thread-Pointer

</td>
</tr>
<tr>
<td>



r14-r31

</td>
<td>



N

</td>
<td>



Local Variables

</td>
</tr>
<tr>
<td>



LR

</td>
<td>



Y

</td>
<td>



Link Register

</td>
</tr>
<tr>
<td>



CTR

</td>
<td>



Y

</td>
<td>



Loop Counter

</td>
</tr>
<tr>
<td>



XER

</td>
<td>



Y

</td>
<td>



Fixed-point exception register.

</td>
</tr>
<tr>
<td>



CR0-1

</td>
<td>



Y

</td>
<td>



Condition register fields.

</td>
</tr>
<tr>
<td>



CR2-4

</td>
<td>



N

</td>
<td>



Condition register fields.

</td>
</tr>
<tr>
<td>



CR5-7

</td>
<td>



Y

</td>
<td>



Condition register fields.

</td>
</tr>
<tr>
<td>



Others

</td>
<td>



N

</td>
<td>





</td>
</tr>
</tbody>
</table>

<a id="rst-drc-drc-indexes"></a>

## DRC &amp; DRC Indexes



```text
DR1                                  Guest
+--+        +------------+         +---------+
|  | <----> |            |         |  User   |
+--+  DRC1  |            |   DRC   |  Space  |
            |    PAPR    |  Index  +---------+
DR2         | Hypervisor |         |         |
+--+        |            | <-----> |  Kernel |
|  | <----> |            |  Hcall  |         |
+--+  DRC2  +------------+         +---------+
```

PAPR hypervisor terms shared hardware resources like PCI devices, NVDIMMs etc available for use by LPARs as Dynamic Resource (DR). When a DR is allocated to an LPAR, PHYP creates a data-structure called Dynamic Resource Connector (DRC) to manage LPAR access. An LPAR refers to a DRC via an opaque 32-bit number called DRC-Index. The DRC-index value is provided to the LPAR via device-tree where its present as an attribute in the device tree node associated with the DR.

<a id="rst-hcall-return-values"></a>

## HCALL Return-values

After servicing the hcall, hypervisor sets the return-value in <em>r3</em> indicating success or failure of the hcall. In case of a failure an error code indicates the cause for error. These codes are defined and documented in arch specific header <a id="rst-footnote-reference-7"></a>[4](#rst-footnote-4).

In some cases a hcall can potentially take a long time and need to be issued multiple times in order to be completely serviced. These hcalls will usually accept an opaque value <em>continue-token</em> within there argument list and a return value of <em>H\_CONTINUE</em> indicates that hypervisor hasn't still finished servicing the hcall yet.

To make such hcalls the guest need to set <em>continue-token == 0</em> for the initial call and use the hypervisor returned value of <em>continue-token</em> for each subsequent hcall until hypervisor returns a non <em>H\_CONTINUE</em> return value.

<a id="rst-hcall-op-codes"></a>

## HCALL Op-codes

Below is a partial list of HCALLs that are supported by PHYP. For the corresponding opcode values please look into the arch specific header <a id="rst-footnote-reference-8"></a>[4](#rst-footnote-4):

<strong>H\_SCM\_READ\_METADATA</strong>

Input: <em>drcIndex, offset, buffer-address, numBytesToRead</em><br>
Out: <em>numBytesRead</em><br>
Return Value: <em>H\_Success, H\_Parameter, H\_P2, H\_P3, H\_Hardware</em>

Given a DRC Index of an NVDIMM, read N-bytes from the metadata area associated with it, at a specified offset and copy it to provided buffer. The metadata area stores configuration information such as label information, bad-blocks etc. The metadata area is located out-of-band of NVDIMM storage area hence a separate access semantics is provided.

<strong>H\_SCM\_WRITE\_METADATA</strong>

Input: <em>drcIndex, offset, data, numBytesToWrite</em><br>
Out: <em>None</em><br>
Return Value: <em>H\_Success, H\_Parameter, H\_P2, H\_P4, H\_Hardware</em>

Given a DRC Index of an NVDIMM, write N-bytes to the metadata area associated with it, at the specified offset and from the provided buffer.

<strong>H\_SCM\_BIND\_MEM</strong>

Input: <em>drcIndex, startingScmBlockIndex, numScmBlocksToBind,</em><br>
<em>targetLogicalMemoryAddress, continue-token</em><br>
Out: <em>continue-token, targetLogicalMemoryAddress, numScmBlocksToBound</em><br>
Return Value: <em>H\_Success, H\_Parameter, H\_P2, H\_P3, H\_P4, H\_Overlap,</em><br>
<em>H\_Too\_Big, H\_P5, H\_Busy</em>

Given a DRC-Index of an NVDIMM, map a continuous SCM blocks range <em>(startingScmBlockIndex, startingScmBlockIndex+numScmBlocksToBind)</em> to the guest at <em>targetLogicalMemoryAddress</em> within guest physical address space. In case <em>targetLogicalMemoryAddress == 0xFFFFFFFF\_FFFFFFFF</em> then hypervisor assigns a target address to the guest. The HCALL can fail if the Guest has an active PTE entry to the SCM block being bound.

<strong>H\_SCM\_UNBIND\_MEM</strong> \| Input: drcIndex, startingScmLogicalMemoryAddress, numScmBlocksToUnbind \| Out: numScmBlocksUnbound \| Return Value: <em>H\_Success, H\_Parameter, H\_P2, H\_P3, H\_In\_Use, H\_Overlap,</em> \| <em>H\_Busy, H\_LongBusyOrder1mSec, H\_LongBusyOrder10mSec</em>

Given a DRC-Index of an NVDimm, unmap <em>numScmBlocksToUnbind</em> SCM blocks starting at <em>startingScmLogicalMemoryAddress</em> from guest physical address space. The HCALL can fail if the Guest has an active PTE entry to the SCM block being unbound.

<strong>H\_SCM\_QUERY\_BLOCK\_MEM\_BINDING</strong>

Input: <em>drcIndex, scmBlockIndex</em><br>
Out: <em>Guest-Physical-Address</em><br>
Return Value: <em>H\_Success, H\_Parameter, H\_P2, H\_NotFound</em>

Given a DRC-Index and an SCM Block index return the guest physical address to which the SCM block is mapped to.

<strong>H\_SCM\_QUERY\_LOGICAL\_MEM\_BINDING</strong>

Input: <em>Guest-Physical-Address</em><br>
Out: <em>drcIndex, scmBlockIndex</em><br>
Return Value: <em>H\_Success, H\_Parameter, H\_P2, H\_NotFound</em>

Given a guest physical address return which DRC Index and SCM block is mapped to that address.

<strong>H\_SCM\_UNBIND\_ALL</strong>

Input: <em>scmTargetScope, drcIndex</em><br>
Out: <em>None</em><br>
Return Value: <em>H\_Success, H\_Parameter, H\_P2, H\_P3, H\_In\_Use, H\_Busy,</em><br>
<em>H\_LongBusyOrder1mSec, H\_LongBusyOrder10mSec</em>

Depending on the Target scope unmap all SCM blocks belonging to all NVDIMMs or all SCM blocks belonging to a single NVDIMM identified by its drcIndex from the LPAR memory.

<strong>H\_SCM\_HEALTH</strong>

Input: drcIndex<br>
Out: <em>health-bitmap (r4), health-bit-valid-bitmap (r5)</em><br>
Return Value: <em>H\_Success, H\_Parameter, H\_Hardware</em>

Given a DRC Index return the info on predictive failure and overall health of the PMEM device. The asserted bits in the health-bitmap indicate one or more states (described in table below) of the PMEM device and health-bit-valid-bitmap indicate which bits in health-bitmap are valid. The bits are reported in reverse bit ordering for example a value of 0xC400000000000000 indicates bits 0, 1, and 5 are valid.

Health Bitmap Flags:


<table>
<thead>
<tr>
<th>



Bit

</th>
<th>



Definition

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



00

</td>
<td>



PMEM device is unable to persist memory contents. If the system is powered down, nothing will be saved.

</td>
</tr>
<tr>
<td>



01

</td>
<td>



PMEM device failed to persist memory contents. Either contents were not saved successfully on power down or were not restored properly on power up.

</td>
</tr>
<tr>
<td>



02

</td>
<td>



PMEM device contents are persisted from previous IPL. The data from the last boot were successfully restored.

</td>
</tr>
<tr>
<td>



03

</td>
<td>



PMEM device contents are not persisted from previous IPL. There was no data to restore from the last boot.

</td>
</tr>
<tr>
<td>



04

</td>
<td>



PMEM device memory life remaining is critically low

</td>
</tr>
<tr>
<td>



05

</td>
<td>



PMEM device will be garded off next IPL due to failure

</td>
</tr>
<tr>
<td>



06

</td>
<td>



PMEM device contents cannot persist due to current platform health status. A hardware failure may prevent data from being saved or restored.

</td>
</tr>
<tr>
<td>



07

</td>
<td>



PMEM device is unable to persist memory contents in certain conditions

</td>
</tr>
<tr>
<td>



08

</td>
<td>



PMEM device is encrypted

</td>
</tr>
<tr>
<td>



09

</td>
<td>



PMEM device has successfully completed a requested erase or secure erase procedure.

</td>
</tr>
<tr>
<td>



10:63

</td>
<td>



Reserved / Unused

</td>
</tr>
</tbody>
</table>

<strong>H\_SCM\_PERFORMANCE\_STATS</strong>

Input: drcIndex, resultBuffer Addr<br>
Out: None<br>
Return Value:  <em>H\_Success, H\_Parameter, H\_Unsupported, H\_Hardware, H\_Authority, H\_Privilege</em>

Given a DRC Index collect the performance statistics for NVDIMM and copy them to the resultBuffer.

<strong>H\_SCM\_FLUSH</strong>

Input: <em>drcIndex, continue-token</em><br>
Out: <em>continue-token</em><br>
Return Value: <em>H\_SUCCESS, H\_Parameter, H\_P2, H\_BUSY</em>

Given a DRC Index Flush the data to backend NVDIMM device.

The hcall returns H\_BUSY when the flush takes longer time and the hcall needs to be issued multiple times in order to be completely serviced. The <em>continue-token</em> from the output to be passed in the argument list of subsequent hcalls to the hypervisor until the hcall is completely serviced at which point H\_SUCCESS or other error is returned by the hypervisor.

<strong>H\_HTM</strong>

Input: flags, target, operation (op), op-param1, op-param2, op-param3<br>
Out: <em>dumphtmbufferdata</em><br>
Return Value: <em>H\_Success,H\_Busy,H\_LongBusyOrder,H\_Partial,H\_Parameter,
H\_P2,H\_P3,H\_P4,H\_P5,H\_P6,H\_State,H\_Not\_Available,H\_Authority</em>

H\_HTM supports setup, configuration, control and dumping of Hardware Trace Macro (HTM) function and its data. HTM buffer stores tracing data for functions like core instruction, core LLAT and nest.

<strong>H\_PKS\_GEN\_KEY</strong>

Input: authorization, objectlabel, objectlabellen, policy, out, outlen<br>
Out: <em>Hypervisor Generated Key, or None when the wrapping key policy is set</em><br>
Return Value: <em>H\_SUCCESS, H\_Function, H\_State, H\_R\_State, H\_Parameter, H\_P2,
H\_P3, H\_P4, H\_P5, H\_P6, H\_Authority, H\_Nomem, H\_Busy, H\_Resource,
H\_Aborted</em>

H\_PKS\_GEN\_KEY is used to have the hypervisor generate a new random key. This key is stored as an object in the Power LPAR Platform KeyStore with the provided object label. With the wrapping key policy set the key is only visible to the hypervisor, while the key's label would still be visible to the user. Generation of wrapping keys is supported only for a key size of 32 bytes.

<strong>H\_PKS\_WRAP\_OBJECT</strong>

Input: authorization, wrapkeylabel, wrapkeylabellen, objectwrapflags, in,<br>
&nbsp;&nbsp;&nbsp;&nbsp;inlen, out, outlen, continue-token<br>
Out: <em>continue-token, byte size of wrapped object, wrapped object</em><br>
Return Value: <em>H\_SUCCESS, H\_Function, H\_State, H\_R\_State, H\_Parameter, H\_P2,
H\_P3, H\_P4, H\_P5, H\_P6, H\_P7, H\_P8, H\_P9, H\_Authority, H\_Invalid\_Key,
H\_NOT\_FOUND, H\_Busy, H\_LongBusy, H\_Aborted</em>

H\_PKS\_WRAP\_OBJECT is used to wrap an object using a wrapping key stored in the Power LPAR Platform KeyStore and return the wrapped object to the caller. The caller provides a label to a wrapping key with the 'wrapping key' policy set, which must have been previously created with H\_PKS\_GEN\_KEY. The provided object is then encrypted with the wrapping key and additional metadata and the result is returned to the caller.

<strong>H\_PKS\_UNWRAP\_OBJECT</strong>

Input: authorization, objectwrapflags, in, inlen, out, outlen, continue-token<br>
Out: <em>continue-token, byte size of unwrapped object, unwrapped object</em><br>
Return Value: <em>H\_SUCCESS, H\_Function, H\_State, H\_R\_State, H\_Parameter, H\_P2,
H\_P3, H\_P4, H\_P5, H\_P6, H\_P7, H\_Authority, H\_Unsupported, H\_Bad\_Data,
H\_NOT\_FOUND, H\_Invalid\_Key, H\_Busy, H\_LongBusy, H\_Aborted</em>

H\_PKS\_UNWRAP\_OBJECT is used to unwrap an object that was previously warapped with H\_PKS\_WRAP\_OBJECT.

<a id="rst-references"></a>

## References

<a id="rst-footnote-1"></a>



**[1]** "Power Architecture Platform Reference" [https://en.wikipedia.org/wiki/Power\_Architecture\_Platform\_Reference](<https://en.wikipedia.org/wiki/Power_Architecture_Platform_Reference>)

<a id="rst-footnote-2"></a>



**[2]** "Linux on Power Architecture Platform Reference" [https://members.openpowerfoundation.org/document/dl/469](<https://members.openpowerfoundation.org/document/dl/469>)

<a id="rst-footnote-3"></a>



**[3]** "Definitions and Notation" Book III-Section 14.5.3 [https://openpowerfoundation.org/?resource\_lib=power-isa-version-3-0](<https://openpowerfoundation.org/?resource_lib=power-isa-version-3-0>)

<a id="rst-footnote-4"></a>



**[4]** arch/powerpc/include/asm/hvcall.h

<a id="rst-footnote-5"></a>



**[5]** "64-Bit ELF V2 ABI Specification: Power Architecture" [https://openpowerfoundation.org/?resource\_lib=64-bit-elf-v2-abi-specification-power-architecture](<https://openpowerfoundation.org/?resource_lib=64-bit-elf-v2-abi-specification-power-architecture>)
