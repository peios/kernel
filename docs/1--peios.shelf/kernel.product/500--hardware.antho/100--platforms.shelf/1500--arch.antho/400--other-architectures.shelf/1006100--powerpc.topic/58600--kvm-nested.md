---
title: "Nested KVM on POWER"
type: reference
description: "This document explains how a guest operating system can act as a hypervisor and run nested guests through the use of hypercalls, if the hypervisor has implemented them. The terms L0, L1, and L2 are used to refer to different software…"
---

<a id="rst-nested-kvm-on-power"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-introduction"></a>

## Introduction

This document explains how a guest operating system can act as a hypervisor and run nested guests through the use of hypercalls, if the hypervisor has implemented them. The terms L0, L1, and L2 are used to refer to different software entities. L0 is the hypervisor mode entity that would normally be called the "host" or "hypervisor". L1 is a guest virtual machine that is directly run under L0 and is initiated and controlled by L0. L2 is a guest virtual machine that is initiated and controlled by L1 acting as a hypervisor.

<a id="rst-existing-api"></a>

## Existing API

Linux/KVM has had support for Nesting as an L0 or L1 since 2018

The L0 code was added:



```text
commit 8e3f5fc1045dc49fd175b978c5457f5f51e7a2ce
Author: Paul Mackerras <paulus@ozlabs.org>
Date:   Mon Oct 8 16:31:03 2018 +1100
KVM: PPC: Book3S HV: Framework and hcall stubs for nested virtualization
```

The L1 code was added:



```text
commit 360cae313702cdd0b90f82c261a8302fecef030a
Author: Paul Mackerras <paulus@ozlabs.org>
Date:   Mon Oct 8 16:31:04 2018 +1100
KVM: PPC: Book3S HV: Nested guest entry via hypercall
```

This API works primarily using a single hcall h_enter_nested(). This call made by the L1 to tell the L0 to start an L2 vCPU with the given state. The L0 then starts this L2 and runs until an L2 exit condition is reached. Once the L2 exits, the state of the L2 is given back to the L1 by the L0. The full L2 vCPU state is always transferred from and to L1 when the L2 is run. The L0 doesn't keep any state on the L2 vCPU (except in the short sequence in the L0 on L1 -&gt; L2 entry and L2 -&gt; L1 exit).

The only state kept by the L0 is the partition table. The L1 registers it's partition table using the h_set_partition_table() hcall. All other state held by the L0 about the L2s is cached state (such as shadow page tables).

The L1 may run any L2 or vCPU without first informing the L0. It simply starts the vCPU using h_enter_nested(). The creation of L2s and vCPUs is done implicitly whenever h_enter_nested() is called.

In this document, we call this existing API the v1 API.

<a id="rst-new-papr-api"></a>

## New PAPR API

The new PAPR API changes from the v1 API such that the creating L2 and associated vCPUs is explicit. In this document, we call this the v2 API.

h_enter_nested() is replaced with H_GUEST_VCPU_RUN().  Before this can be called the L1 must explicitly create the L2 using h_guest_create() and any associated vCPUs() created with h_guest_create_vCPU(). Getting and setting vCPU state can also be performed using h_guest\_\{g\|s\}et hcall.

The basic execution flow is for an L1 to create an L2, run it, and delete it is:

- L1 and L0 negotiate capabilities with H_GUEST\_\{G,S\}ET_CAPABILITIES() (normally at L1 boot time).

- L1 requests the L0 create an L2 with H_GUEST_CREATE() and receives a token

- L1 requests the L0 create an L2 vCPU with H_GUEST_CREATE_VCPU()

- L1 and L0 communicate the vCPU state using the H_GUEST\_\{G,S\}ET() hcall

- L1 requests the L0 runs the vCPU running H_GUEST_VCPU_RUN() hcall

- L1 deletes L2 with H_GUEST_DELETE()

More details of the individual hcalls follows:

<a id="rst-hcall-details"></a>

## HCALL Details

This documentation is provided to give an overall understating of the API. It doesn't aim to provide all the details required to implement an L1 or L0. Latest version of PAPR can be referred to for more details.

All these HCALLs are made by the L1 to the L0.

<a id="rst-h-guest-get-capabilities"></a>

### H_GUEST_GET_CAPABILITIES()

This is called to get the capabilities of the L0 nested hypervisor. This includes capabilities such the CPU versions (eg POWER9, POWER10) that are supported as L2s:



```text
H_GUEST_GET_CAPABILITIES(uint64 flags)

Parameters:
  Input:
    flags: Reserved
  Output:
    R3: Return code
    R4: Hypervisor Supported Capabilities bitmap 1
```

<a id="rst-h-guest-set-capabilities"></a>

### H_GUEST_SET_CAPABILITIES()

This is called to inform the L0 of the capabilities of the L1 hypervisor. The set of flags passed here are the same as H_GUEST_GET_CAPABILITIES()

Typically, GET will be called first and then SET will be called with a subset of the flags returned from GET. This process allows the L0 and L1 to negotiate an agreed set of capabilities:



```text
H_GUEST_SET_CAPABILITIES(uint64 flags,
                         uint64 capabilitiesBitmap1)
Parameters:
  Input:
    flags: Reserved
    capabilitiesBitmap1: Only capabilities advertised through
                         H_GUEST_GET_CAPABILITIES
  Output:
    R3: Return code
    R4: If R3 = H_P2: The number of invalid bitmaps
    R5: If R3 = H_P2: The index of first invalid bitmap
```

<a id="rst-h-guest-create"></a>

### H_GUEST_CREATE()

This is called to create an L2. A unique ID of the L2 created (similar to an LPID) is returned, which can be used on subsequent HCALLs to identify the L2:



```text
H_GUEST_CREATE(uint64 flags,
               uint64 continueToken);
Parameters:
  Input:
    flags: Reserved
    continueToken: Initial call set to -1. Subsequent calls,
                   after H_Busy or H_LongBusyOrder has been
                   returned, value that was returned in R4.
  Output:
    R3: Return code. Notable:
      H_Not_Enough_Resources: Unable to create Guest VCPU due to not
      enough Hypervisor memory. See H_GUEST_CREATE_GET_STATE(flags =
      takeOwnershipOfVcpuState)
    R4: If R3 = H_Busy or_H_LongBusyOrder -> continueToken
```

<a id="rst-h-guest-create-vcpu"></a>

### H_GUEST_CREATE_VCPU()

This is called to create a vCPU associated with an L2. The L2 id (returned from H_GUEST_CREATE()) should be passed it. Also passed in is a unique (for this L2) vCPUid. This vCPUid is allocated by the L1:



```text
H_GUEST_CREATE_VCPU(uint64 flags,
                    uint64 guestId,
                    uint64 vcpuId);
Parameters:
  Input:
    flags: Reserved
    guestId: ID obtained from H_GUEST_CREATE
    vcpuId: ID of the vCPU to be created. This must be within the
            range of 0 to 2047
  Output:
    R3: Return code. Notable:
      H_Not_Enough_Resources: Unable to create Guest VCPU due to not
      enough Hypervisor memory. See H_GUEST_CREATE_GET_STATE(flags =
      takeOwnershipOfVcpuState)
```

<a id="rst-h-guest-get-state"></a>

### H_GUEST_GET_STATE()

This is called to get state associated with an L2 (Guest-wide or vCPU specific). This info is passed via the Guest State Buffer (GSB), a standard format as explained later in this doc, necessary details below:

This can get either L2 wide or vcpu specific information. Examples of L2 wide is the timebase offset or process scoped page table info. Examples of vCPU specific are GPRs or VSRs. A bit in the flags parameter specifies if this call is L2 wide or vCPU specific and the IDs in the GSB must match this.

The L1 provides a pointer to the GSB as a parameter to this call. Also provided is the L2 and vCPU IDs associated with the state to set.

The L1 writes only the IDs and sizes in the GSB.  L0 writes the associated values for each ID in the GSB:



```text
H_GUEST_GET_STATE(uint64 flags,
                         uint64 guestId,
                         uint64 vcpuId,
                         uint64 dataBuffer,
                         uint64 dataBufferSizeInBytes);
Parameters:
  Input:
    flags:
       Bit 0: getGuestWideState: Request state of the Guest instead
         of an individual VCPU.
       Bit 1: getHostWideState: Request stats of the Host. This causes
         the guestId and vcpuId parameters to be ignored and attempting
         to get the VCPU/Guest state will cause an error.
       Bits 2-63: Reserved
    guestId: ID obtained from H_GUEST_CREATE
    vcpuId: ID of the vCPU pass to H_GUEST_CREATE_VCPU
    dataBuffer: A L1 real address of the GSB.
      If takeOwnershipOfVcpuState, size must be at least the size
      returned by ID=0x0001
    dataBufferSizeInBytes: Size of dataBuffer
  Output:
    R3: Return code
    R4: If R3 = H_Invalid_Element_Id: The array index of the bad
          element ID.
        If R3 = H_Invalid_Element_Size: The array index of the bad
           element size.
        If R3 = H_Invalid_Element_Value: The array index of the bad
           element value.
```

<a id="rst-h-guest-set-state"></a>

### H_GUEST_SET_STATE()

This is called to set L2 wide or vCPU specific L2 state. This info is passed via the Guest State Buffer (GSB), necessary details below:

This can set either L2 wide or vcpu specific information. Examples of L2 wide is the timebase offset or process scoped page table info. Examples of vCPU specific are GPRs or VSRs. A bit in the flags parameter specifies if this call is L2 wide or vCPU specific and the IDs in the GSB must match this.

The L1 provides a pointer to the GSB as a parameter to this call. Also provided is the L2 and vCPU IDs associated with the state to set.

The L1 writes all values in the GSB and the L0 only reads the GSB for this call:



```text
H_GUEST_SET_STATE(uint64 flags,
                  uint64 guestId,
                  uint64 vcpuId,
                  uint64 dataBuffer,
                  uint64 dataBufferSizeInBytes);
Parameters:
  Input:
    flags:
       Bit 0: getGuestWideState: Request state of the Guest instead
         of an individual VCPU.
       Bit 1: returnOwnershipOfVcpuState Return Guest VCPU state. See
         GET_STATE takeOwnershipOfVcpuState
       Bits 2-63: Reserved
    guestId: ID obtained from H_GUEST_CREATE
    vcpuId: ID of the vCPU pass to H_GUEST_CREATE_VCPU
    dataBuffer: A L1 real address of the GSB.
      If takeOwnershipOfVcpuState, size must be at least the size
      returned by ID=0x0001
    dataBufferSizeInBytes: Size of dataBuffer
  Output:
    R3: Return code
    R4: If R3 = H_Invalid_Element_Id: The array index of the bad
          element ID.
        If R3 = H_Invalid_Element_Size: The array index of the bad
           element size.
        If R3 = H_Invalid_Element_Value: The array index of the bad
           element value.
```

<a id="rst-h-guest-run-vcpu"></a>

### H_GUEST_RUN_VCPU()

This is called to run an L2 vCPU. The L2 and vCPU IDs are passed in as parameters. The vCPU runs with the state set previously using H_GUEST_SET_STATE(). When the L2 exits, the L1 will resume from this hcall.

This hcall also has associated input and output GSBs. Unlike H_GUEST\_\{S,G\}ET_STATE(), these GSB pointers are not passed in as parameters to the hcall (This was done in the interest of performance). The locations of these GSBs must be preregistered using the H_GUEST_SET_STATE() call with ID 0x0c00 and 0x0c01 (see table below).

The input GSB may contain only VCPU specific elements to be set. This GSB may also contain zero elements (ie 0 in the first 4 bytes of the GSB) if nothing needs to be set.

On exit from the hcall, the output buffer is filled with elements determined by the L0. The reason for the exit is contained in GPR4 (ie NIP is put in GPR4).  The elements returned depend on the exit type. For example, if the exit reason is the L2 doing a hcall (GPR4 = 0xc00), then GPR3-12 are provided in the output GSB as this is the state likely needed to service the hcall. If additional state is needed, H_GUEST_GET_STATE() may be called by the L1.

To synthesize interrupts in the L2, when calling H_GUEST_RUN_VCPU() the L1 may set a flag (as a hcall parameter) and the L0 will synthesize the interrupt in the L2. Alternatively, the L1 may synthesize the interrupt itself using H_GUEST_SET_STATE() or the H_GUEST_RUN_VCPU() input GSB to set the state appropriately:



```text
H_GUEST_RUN_VCPU(uint64 flags,
                 uint64 guestId,
                 uint64 vcpuId,
                 uint64 dataBuffer,
                 uint64 dataBufferSizeInBytes);
Parameters:
  Input:
    flags:
       Bit 0: generateExternalInterrupt: Generate an external interrupt
       Bit 1: generatePrivilegedDoorbell: Generate a Privileged Doorbell
       Bit 2: sendToSystemReset”: Generate a System Reset Interrupt
       Bits 3-63: Reserved
    guestId: ID obtained from H_GUEST_CREATE
    vcpuId: ID of the vCPU pass to H_GUEST_CREATE_VCPU
  Output:
    R3: Return code
    R4: If R3 = H_Success: The reason L1 VCPU exited (ie. NIA)
          0x000: The VCPU stopped running for an unspecified reason. An
            example of this is the Hypervisor stopping a VCPU running
            due to an outstanding interrupt for the Host Partition.
          0x980: HDEC
          0xC00: HCALL
          0xE00: HDSI
          0xE20: HISI
          0xE40: HEA
          0xF80: HV Fac Unavail
        If R3 = H_Invalid_Element_Id, H_Invalid_Element_Size, or
          H_Invalid_Element_Value: R4 is offset of the invalid element
          in the input buffer.
```

<a id="rst-h-guest-delete"></a>

### H_GUEST_DELETE()

This is called to delete an L2. All associated vCPUs are also deleted. No specific vCPU delete call is provided.

A flag may be provided to delete all guests. This is used to reset the L0 in the case of kdump/kexec:



```text
H_GUEST_DELETE(uint64 flags,
               uint64 guestId)
Parameters:
  Input:
    flags:
       Bit 0: deleteAllGuests: deletes all guests
       Bits 1-63: Reserved
    guestId: ID obtained from H_GUEST_CREATE
  Output:
    R3: Return code
```

<a id="rst-guest-state-buffer"></a>

## Guest State Buffer

The Guest State Buffer (GSB) is the main method of communicating state about the L2 between the L1 and L0 via H_GUEST\_\{G,S\}ET() and H_GUEST_VCPU_RUN() calls.

State may be associated with a whole L2 (eg timebase offset) or a specific L2 vCPU (eg. GPR state). Only L2 VCPU state maybe be set by H_GUEST_VCPU_RUN().

All data in the GSB is big endian (as is standard in PAPR)

The Guest state buffer has a header which gives the number of elements, followed by the GSB elements themselves.

GSB header:


<table>
<thead>
<tr>
<th>


Offset Bytes

</th>
<th>


Size Bytes

</th>
<th>


Purpose

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


0

</td>
<td>


4

</td>
<td>


Number of elements

</td>
</tr>
<tr>
<td>


4

</td>
<td>




</td>
<td>


Guest state buffer elements

</td>
</tr>
</tbody>
</table>

GSB element:


<table>
<thead>
<tr>
<th>


Offset Bytes

</th>
<th>


Size Bytes

</th>
<th>


Purpose

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


0

</td>
<td>


2

</td>
<td>


ID

</td>
</tr>
<tr>
<td>


2

</td>
<td>


2

</td>
<td>


Size of Value

</td>
</tr>
<tr>
<td>


4

</td>
<td>


As above

</td>
<td>


Value

</td>
</tr>
</tbody>
</table>

The ID in the GSB element specifies what is to be set. This includes archtected state like GPRs, VSRs, SPRs, plus also some meta data about the partition like the timebase offset and partition scoped page table information.


<table>
<thead>
<tr>
<th>


ID

</th>
<th>


Size Bytes

</th>
<th>


RW

</th>
<th>


(H)ost (G)uest (T)hread Scope

</th>
<th>


Details

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


0x0000

</td>
<td>




</td>
<td>


RW

</td>
<td>


TG

</td>
<td>


NOP element

</td>
</tr>
<tr>
<td>


0x0001

</td>
<td>


0x08

</td>
<td>


R

</td>
<td>


G

</td>
<td>


Size of L0 vCPU state. See: H_GUEST_GET_STATE: flags = takeOwnershipOfVcpuState

</td>
</tr>
<tr>
<td>


0x0002

</td>
<td>


0x08

</td>
<td>


R

</td>
<td>


G

</td>
<td>


Size Run vCPU out buffer

</td>
</tr>
<tr>
<td>


0x0003

</td>
<td>


0x04

</td>
<td>


RW

</td>
<td>


G

</td>
<td>


Logical PVR

</td>
</tr>
<tr>
<td>


0x0004

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


G

</td>
<td>


TB Offset (L1 relative)

</td>
</tr>
<tr>
<td>


0x0005

</td>
<td>


0x18

</td>
<td>


RW

</td>
<td>


G

</td>
<td>


Partition scoped page tbl info:

- 0x00 Addr part scope table

- 0x08 Num addr bits

- 0x10 Size root dir

</td>
</tr>
<tr>
<td>


0x0006

</td>
<td>


0x10

</td>
<td>


RW

</td>
<td>


G

</td>
<td>


Process Table Information:

- 0x0 Addr proc scope table

- 0x8 Table size.

</td>
</tr>
<tr>
<td>


0x0007- 0x07FF

</td>
<td>




</td>
<td>




</td>
<td>




</td>
<td>


Reserved

</td>
</tr>
<tr>
<td>


0x0800

</td>
<td>


0x08

</td>
<td>


R

</td>
<td>


H

</td>
<td>


Current usage in bytes of the L0's Guest Management Space for an L1-Lpar.

</td>
</tr>
<tr>
<td>


0x0801

</td>
<td>


0x08

</td>
<td>


R

</td>
<td>


H

</td>
<td>


Max bytes available in the L0's Guest Management Space for an L1-Lpar

</td>
</tr>
<tr>
<td>


0x0802

</td>
<td>


0x08

</td>
<td>


R

</td>
<td>


H

</td>
<td>


Current usage in bytes of the L0's Guest Page Table Management Space for an L1-Lpar

</td>
</tr>
<tr>
<td>


0x0803

</td>
<td>


0x08

</td>
<td>


R

</td>
<td>


H

</td>
<td>


Max bytes available in the L0's Guest Page Table Management Space for an L1-Lpar

</td>
</tr>
<tr>
<td>


0x0804

</td>
<td>


0x08

</td>
<td>


R

</td>
<td>


H

</td>
<td>


Cumulative Reclaimed bytes from L0 Guest's Page Table Management Space due to overcommit

</td>
</tr>
<tr>
<td>


0x0805- 0x0BFF

</td>
<td>




</td>
<td>




</td>
<td>




</td>
<td>


Reserved

</td>
</tr>
<tr>
<td>


0x0C00

</td>
<td>


0x10

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


Run vCPU Input Buffer:

- 0x0 Addr of buffer

- 0x8 Buffer Size.

</td>
</tr>
<tr>
<td>


0x0C01

</td>
<td>


0x10

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


Run vCPU Output Buffer:

- 0x0 Addr of buffer

- 0x8 Buffer Size.

</td>
</tr>
<tr>
<td>


0x0C02

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


vCPU VPA Address

</td>
</tr>
<tr>
<td>


0x0C03- 0x0FFF

</td>
<td>




</td>
<td>




</td>
<td>




</td>
<td>


Reserved

</td>
</tr>
<tr>
<td>


0x1000- 0x101F

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


GPR 0-31

</td>
</tr>
<tr>
<td>


0x1020

</td>
<td>


0x08

</td>
<td>


T

</td>
<td>


T

</td>
<td>


HDEC expiry TB

</td>
</tr>
<tr>
<td>


0x1021

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


NIA

</td>
</tr>
<tr>
<td>


0x1022

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


MSR

</td>
</tr>
<tr>
<td>


0x1023

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


LR

</td>
</tr>
<tr>
<td>


0x1024

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


XER

</td>
</tr>
<tr>
<td>


0x1025

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


CTR

</td>
</tr>
<tr>
<td>


0x1026

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


CFAR

</td>
</tr>
<tr>
<td>


0x1027

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


SRR0

</td>
</tr>
<tr>
<td>


0x1028

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


SRR1

</td>
</tr>
<tr>
<td>


0x1029

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


DAR

</td>
</tr>
<tr>
<td>


0x102A

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


DEC expiry TB

</td>
</tr>
<tr>
<td>


0x102B

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


VTB

</td>
</tr>
<tr>
<td>


0x102C

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


LPCR

</td>
</tr>
<tr>
<td>


0x102D

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


HFSCR

</td>
</tr>
<tr>
<td>


0x102E

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


FSCR

</td>
</tr>
<tr>
<td>


0x102F

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


FPSCR

</td>
</tr>
<tr>
<td>


0x1030

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


DAWR0

</td>
</tr>
<tr>
<td>


0x1031

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


DAWR1

</td>
</tr>
<tr>
<td>


0x1032

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


CIABR

</td>
</tr>
<tr>
<td>


0x1033

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


PURR

</td>
</tr>
<tr>
<td>


0x1034

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


SPURR

</td>
</tr>
<tr>
<td>


0x1035

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


IC

</td>
</tr>
<tr>
<td>


0x1036- 0x1039

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


SPRG 0-3

</td>
</tr>
<tr>
<td>


0x103A

</td>
<td>


0x08

</td>
<td>


W

</td>
<td>


T

</td>
<td>


PPR

</td>
</tr>
<tr>
<td>


0x103B 0x103E

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


MMCR 0-3

</td>
</tr>
<tr>
<td>


0x103F

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


MMCRA

</td>
</tr>
<tr>
<td>


0x1040

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


SIER

</td>
</tr>
<tr>
<td>


0x1041

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


SIER 2

</td>
</tr>
<tr>
<td>


0x1042

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


SIER 3

</td>
</tr>
<tr>
<td>


0x1043

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


BESCR

</td>
</tr>
<tr>
<td>


0x1044

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


EBBHR

</td>
</tr>
<tr>
<td>


0x1045

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


EBBRR

</td>
</tr>
<tr>
<td>


0x1046

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


AMR

</td>
</tr>
<tr>
<td>


0x1047

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


IAMR

</td>
</tr>
<tr>
<td>


0x1048

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


AMOR

</td>
</tr>
<tr>
<td>


0x1049

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


UAMOR

</td>
</tr>
<tr>
<td>


0x104A

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


SDAR

</td>
</tr>
<tr>
<td>


0x104B

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


SIAR

</td>
</tr>
<tr>
<td>


0x104C

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


DSCR

</td>
</tr>
<tr>
<td>


0x104D

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


TAR

</td>
</tr>
<tr>
<td>


0x104E

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


DEXCR

</td>
</tr>
<tr>
<td>


0x104F

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


HDEXCR

</td>
</tr>
<tr>
<td>


0x1050

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


HASHKEYR

</td>
</tr>
<tr>
<td>


0x1051

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


HASHPKEYR

</td>
</tr>
<tr>
<td>


0x1052

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


CTRL

</td>
</tr>
<tr>
<td>


0x1053

</td>
<td>


0x08

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


DPDES

</td>
</tr>
<tr>
<td>


0x1054- 0x1FFF

</td>
<td>




</td>
<td>




</td>
<td>




</td>
<td>


Reserved

</td>
</tr>
<tr>
<td>


0x2000

</td>
<td>


0x04

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


CR

</td>
</tr>
<tr>
<td>


0x2001

</td>
<td>


0x04

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


PIDR

</td>
</tr>
<tr>
<td>


0x2002

</td>
<td>


0x04

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


DSISR

</td>
</tr>
<tr>
<td>


0x2003

</td>
<td>


0x04

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


VSCR

</td>
</tr>
<tr>
<td>


0x2004

</td>
<td>


0x04

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


VRSAVE

</td>
</tr>
<tr>
<td>


0x2005

</td>
<td>


0x04

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


DAWRX0

</td>
</tr>
<tr>
<td>


0x2006

</td>
<td>


0x04

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


DAWRX1

</td>
</tr>
<tr>
<td>


0x2007- 0x200c

</td>
<td>


0x04

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


PMC 1-6

</td>
</tr>
<tr>
<td>


0x200D

</td>
<td>


0x04

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


WORT

</td>
</tr>
<tr>
<td>


0x200E

</td>
<td>


0x04

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


PSPB

</td>
</tr>
<tr>
<td>


0x200F- 0x2FFF

</td>
<td>




</td>
<td>




</td>
<td>




</td>
<td>


Reserved

</td>
</tr>
<tr>
<td>


0x3000- 0x303F

</td>
<td>


0x10

</td>
<td>


RW

</td>
<td>


T

</td>
<td>


VSR 0-63

</td>
</tr>
<tr>
<td>


0x3040- 0xEFFF

</td>
<td>




</td>
<td>




</td>
<td>




</td>
<td>


Reserved

</td>
</tr>
<tr>
<td>


0xF000

</td>
<td>


0x08

</td>
<td>


R

</td>
<td>


T

</td>
<td>


HDAR

</td>
</tr>
<tr>
<td>


0xF001

</td>
<td>


0x04

</td>
<td>


R

</td>
<td>


T

</td>
<td>


HDSISR

</td>
</tr>
<tr>
<td>


0xF002

</td>
<td>


0x04

</td>
<td>


R

</td>
<td>


T

</td>
<td>


HEIR

</td>
</tr>
<tr>
<td>


0xF003

</td>
<td>


0x08

</td>
<td>


R

</td>
<td>


T

</td>
<td>


ASDR

</td>
</tr>
</tbody>
</table>

<a id="rst-miscellaneous-info"></a>

## Miscellaneous info

<a id="rst-state-not-in-ptregs-hvregs"></a>

### State not in ptregs/hvregs

In the v1 API, some state is not in the ptregs/hvstate. This includes the vector register and some SPRs. For the L1 to set this state for the L2, the L1 loads up these hardware registers before the h_enter_nested() call and the L0 ensures they end up as the L2 state (by not touching them).

The v2 API removes this and explicitly sets this state via the GSB.

<a id="rst-l1-implementation-details-caching-state"></a>

### L1 Implementation details: Caching state

In the v1 API, all state is sent from the L1 to the L0 and vice versa on every h_enter_nested() hcall. If the L0 is not currently running any L2s, the L0 has no state information about them. The only exception to this is the location of the partition table, registered via h_set_partition_table().

The v2 API changes this so that the L0 retains the L2 state even when it's vCPUs are no longer running. This means that the L1 only needs to communicate with the L0 about L2 state when it needs to modify the L2 state, or when it's value is out of date. This provides an opportunity for performance optimisation.

When a vCPU exits from a H_GUEST_RUN_VCPU() call, the L1 internally marks all L2 state as invalid. This means that if the L1 wants to know the L2 state (say via a kvm_get_one_reg() call), it needs call H_GUEST_GET_STATE() to get that state. Once it's read, it's marked as valid in L1 until the L2 is run again.

Also, when an L1 modifies L2 vcpu state, it doesn't need to write it to the L0 until that L2 vcpu runs again. Hence when the L1 updates state (say via a kvm_set_one_reg() call), it writes to an internal L1 copy and only flushes this copy to the L0 when the L2 runs again via the H_GUEST_VCPU_RUN() input buffer.

This lazy updating of state by the L1 avoids unnecessary H_GUEST\_\{G\|S\}ET_STATE() calls.
