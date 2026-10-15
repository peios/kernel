---
title: "The LoongArch paravirtual interface"
type: reference
description: "KVM hypercalls use the HVCL instruction with code 0x100 and the hypercall number is put in a0. Up to five arguments may be placed in registers a1 - a5. The return value is placed in v0 (an alias of a0)."
---

<a id="rst-the-loongarch-paravirtual-interface"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

KVM hypercalls use the HVCL instruction with code 0x100 and the hypercall number is put in a0. Up to five arguments may be placed in registers a1 - a5. The return value is placed in v0 (an alias of a0).

Source code for this interface can be found in arch/loongarch/kvm\*.

<a id="rst-querying-for-existence"></a>

## Querying for existence

To determine if the host is running on KVM, we can utilize the cpucfg() function at index CPUCFG_KVM_BASE (0x40000000).

The CPUCFG_KVM_BASE range, spanning from 0x40000000 to 0x400000FF, The CPUCFG_KVM_BASE range between 0x40000000 - 0x400000FF is marked as reserved. Consequently, all current and future processors will not implement any feature within this range.

On a KVM-virtualized Linux system, a read operation on cpucfg() at index CPUCFG_KVM_BASE (0x40000000) returns the magic string 'KVM0'.

Once you have determined that your host is running on a paravirtualization- capable KVM, you may now use hypercalls as described below.

<a id="rst-kvm-hypercall-abi"></a>

## KVM hypercall ABI

The KVM hypercall ABI is simple, with one scratch register a0 (v0) and at most five generic registers (a1 - a5) used as input parameters. The FP (Floating- point) and vector registers are not utilized as input registers and must remain unmodified during a hypercall.

Hypercall functions can be inlined as it only uses one scratch register.

The parameters are as follows:

>
> <table>
> <thead>
> <tr>
> <th>
>
>
> Register
>
> </th>
> <th>
>
>
> IN
>
> </th>
> <th>
>
>
> OUT
>
> </th>
> </tr>
> </thead>
> <tbody>
> <tr>
> <td>
>
>
> a0
>
> </td>
> <td>
>
>
> function number
>
> </td>
> <td>
>
>
> Return  code
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> a1
>
> </td>
> <td>
>
>
> 1st     parameter
>
> </td>
> <td>
>
>
> - <!-- empty source list item -->
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> a2
>
> </td>
> <td>
>
>
> 2nd     parameter
>
> </td>
> <td>
>
>
> - <!-- empty source list item -->
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> a3
>
> </td>
> <td>
>
>
> 3rd     parameter
>
> </td>
> <td>
>
>
> - <!-- empty source list item -->
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> a4
>
> </td>
> <td>
>
>
> 4th     parameter
>
> </td>
> <td>
>
>
> - <!-- empty source list item -->
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> a5
>
> </td>
> <td>
>
>
> 5th     parameter
>
> </td>
> <td>
>
>
> - <!-- empty source list item -->
>
> </td>
> </tr>
> </tbody>
> </table>

The return codes may be one of the following:

>
> <table>
> <thead>
> <tr>
> <th>
>
>
> Code
>
> </th>
> <th>
>
>
> Meaning
>
> </th>
> </tr>
> </thead>
> <tbody>
> <tr>
> <td>
>
>
> 0
>
> </td>
> <td>
>
>
> Success
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> -1
>
> </td>
> <td>
>
>
> Hypercall not implemented
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> -2
>
> </td>
> <td>
>
>
> Bad Hypercall parameter
>
> </td>
> </tr>
> </tbody>
> </table>

<a id="rst-kvm-hypercalls-documentation"></a>

## KVM Hypercalls Documentation

The template for each hypercall is as follows:

1. Hypercall name

2. Purpose

<a id="rst-kvm-hcall-func-ipi"></a>

### 1. KVM_HCALL_FUNC_IPI

**Purpose:** Send IPIs to multiple vCPUs.

- a0: KVM_HCALL_FUNC_IPI

- a1: Lower part of the bitmap for destination physical CPUIDs

- a2: Higher part of the bitmap for destination physical CPUIDs

- a3: The lowest physical CPUID in the bitmap

The hypercall lets a guest send multiple IPIs (Inter-Process Interrupts) with at most 128 destinations per hypercall. The destinations are represented in a bitmap contained in the first two input registers (a1 and a2).

Bit 0 of a1 corresponds to the physical CPUID in the third input register (a3) and bit 1 corresponds to the physical CPUID in a3+1, and so on.

PV IPI on LoongArch includes both PV IPI multicast sending and PV IPI receiving, and SWI is used for PV IPI inject since there is no VM-exits accessing SWI registers.
