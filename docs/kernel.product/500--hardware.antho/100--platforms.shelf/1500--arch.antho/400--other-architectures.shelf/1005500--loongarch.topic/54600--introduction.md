---
title: "Introduction to LoongArch"
type: reference
description: "LoongArch is a new RISC ISA, which is a bit like MIPS or RISC-V. There are currently 3 variants: a reduced 32-bit version (LA32R), a standard 32-bit version (LA32S) and a 64-bit version (LA64). There are 4 privilege levels (PLVs) defined…"
---

<a id="rst-introduction-to-loongarch"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

LoongArch is a new RISC ISA, which is a bit like MIPS or RISC-V. There are currently 3 variants: a reduced 32-bit version (LA32R), a standard 32-bit version (LA32S) and a 64-bit version (LA64). There are 4 privilege levels (PLVs) defined in LoongArch: PLV0\~PLV3, from high to low. Kernel runs at PLV0 while applications run at PLV3. This document introduces the registers, basic instruction set, virtual memory and some other topics of LoongArch.

<a id="rst-registers"></a>

## Registers

LoongArch registers include general purpose registers (GPRs), floating point registers (FPRs), vector registers (VRs) and control status registers (CSRs) used in privileged mode (PLV0).

<a id="rst-gprs"></a>

### GPRs

LoongArch has 32 GPRs ( `$r0` \~ `$r31` ); each one is 32-bit wide in LA32 and 64-bit wide in LA64. `$r0` is hard-wired to zero, and the other registers are not architecturally special. (Except `$r1`, which is hard-wired as the link register of the BL instruction.)

The kernel uses a variant of the LoongArch register convention, as described in the LoongArch ELF psABI spec, in [References](<#rst-loongarch-references>):


<table>
<thead>
<tr>
<th>


Name

</th>
<th>


Alias

</th>
<th>


Usage

</th>
<th>


Preserved across calls

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


`$r0`

</td>
<td>


`$zero`

</td>
<td>


Constant zero

</td>
<td>


Unused

</td>
</tr>
<tr>
<td>


`$r1`

</td>
<td>


`$ra`

</td>
<td>


Return address

</td>
<td>


No

</td>
</tr>
<tr>
<td>


`$r2`

</td>
<td>


`$tp`

</td>
<td>


TLS/Thread pointer

</td>
<td>


Unused

</td>
</tr>
<tr>
<td>


`$r3`

</td>
<td>


`$sp`

</td>
<td>


Stack pointer

</td>
<td>


Yes

</td>
</tr>
<tr>
<td>


`$r4`-`$r11`

</td>
<td>


`$a0`-`$a7`

</td>
<td>


Argument registers

</td>
<td>


No

</td>
</tr>
<tr>
<td>


`$r4`-`$r5`

</td>
<td>


`$v0`-`$v1`

</td>
<td>


Return value

</td>
<td>


No

</td>
</tr>
<tr>
<td>


`$r12`-`$r20`

</td>
<td>


`$t0`-`$t8`

</td>
<td>


Temp registers

</td>
<td>


No

</td>
</tr>
<tr>
<td>


`$r21`

</td>
<td>


`$u0`

</td>
<td>


Percpu base address

</td>
<td>


Unused

</td>
</tr>
<tr>
<td>


`$r22`

</td>
<td>


`$fp`

</td>
<td>


Frame pointer

</td>
<td>


Yes

</td>
</tr>
<tr>
<td>


`$r23`-`$r31`

</td>
<td>


`$s0`-`$s8`

</td>
<td>


Static registers

</td>
<td>


Yes

</td>
</tr>
</tbody>
</table>

> [!NOTE]
>
> The register `$r21` is reserved in the ELF psABI, but used by the Linux kernel for storing the percpu base address. It normally has no ABI name, but is called `$u0` in the kernel. You may also see `$v0` or `$v1` in some old code,however they are deprecated aliases of `$a0` and `$a1` respectively.

<a id="rst-fprs"></a>

### FPRs

LoongArch has 32 FPRs ( `$f0` \~ `$f31` ) when FPU is present. Each one is 64-bit wide on the LA64 cores.

The floating-point register convention is the same as described in the LoongArch ELF psABI spec:


<table>
<thead>
<tr>
<th>


Name

</th>
<th>


Alias

</th>
<th>


Usage

</th>
<th>


Preserved across calls

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


`$f0`-`$f7`

</td>
<td>


`$fa0`-`$fa7`

</td>
<td>


Argument registers

</td>
<td>


No

</td>
</tr>
<tr>
<td>


`$f0`-`$f1`

</td>
<td>


`$fv0`-`$fv1`

</td>
<td>


Return value

</td>
<td>


No

</td>
</tr>
<tr>
<td>


`$f8`-`$f23`

</td>
<td>


`$ft0`-`$ft15`

</td>
<td>


Temp registers

</td>
<td>


No

</td>
</tr>
<tr>
<td>


`$f24`-`$f31`

</td>
<td>


`$fs0`-`$fs7`

</td>
<td>


Static registers

</td>
<td>


Yes

</td>
</tr>
</tbody>
</table>

> [!NOTE]
>
> You may see `$fv0` or `$fv1` in some old code, however they are deprecated aliases of `$fa0` and `$fa1` respectively.

<a id="rst-vrs"></a>

### VRs

There are currently 2 vector extensions to LoongArch:

- LSX (Loongson SIMD eXtension) with 128-bit vectors,

- LASX (Loongson Advanced SIMD eXtension) with 256-bit vectors.

LSX brings `$v0` \~ `$v31` while LASX brings `$x0` \~ `$x31` as the vector registers.

The VRs overlap with FPRs: for example, on a core implementing LSX and LASX, the lower 128 bits of `$x0` is shared with `$v0`, and the lower 64 bits of `$v0` is shared with `$f0`; same with all other VRs.

<a id="rst-csrs"></a>

### CSRs

CSRs can only be accessed from privileged mode (PLV0):


<table>
<thead>
<tr>
<th>


Address

</th>
<th>


Full Name

</th>
<th>


Abbrev Name

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


0x0

</td>
<td>


Current Mode Information

</td>
<td>


CRMD

</td>
</tr>
<tr>
<td>


0x1

</td>
<td>


Pre-exception Mode Information

</td>
<td>


PRMD

</td>
</tr>
<tr>
<td>


0x2

</td>
<td>


Extension Unit Enable

</td>
<td>


EUEN

</td>
</tr>
<tr>
<td>


0x3

</td>
<td>


Miscellaneous Control

</td>
<td>


MISC

</td>
</tr>
<tr>
<td>


0x4

</td>
<td>


Exception Configuration

</td>
<td>


ECFG

</td>
</tr>
<tr>
<td>


0x5

</td>
<td>


Exception Status

</td>
<td>


ESTAT

</td>
</tr>
<tr>
<td>


0x6

</td>
<td>


Exception Return Address

</td>
<td>


ERA

</td>
</tr>
<tr>
<td>


0x7

</td>
<td>


Bad (Faulting) Virtual Address

</td>
<td>


BADV

</td>
</tr>
<tr>
<td>


0x8

</td>
<td>


Bad (Faulting) Instruction Word

</td>
<td>


BADI

</td>
</tr>
<tr>
<td>


0xC

</td>
<td>


Exception Entrypoint Address

</td>
<td>


EENTRY

</td>
</tr>
<tr>
<td>


0x10

</td>
<td>


TLB Index

</td>
<td>


TLBIDX

</td>
</tr>
<tr>
<td>


0x11

</td>
<td>


TLB Entry High-order Bits

</td>
<td>


TLBEHI

</td>
</tr>
<tr>
<td>


0x12

</td>
<td>


TLB Entry Low-order Bits 0

</td>
<td>


TLBELO0

</td>
</tr>
<tr>
<td>


0x13

</td>
<td>


TLB Entry Low-order Bits 1

</td>
<td>


TLBELO1

</td>
</tr>
<tr>
<td>


0x18

</td>
<td>


Address Space Identifier

</td>
<td>


ASID

</td>
</tr>
<tr>
<td>


0x19

</td>
<td>


Page Global Directory Address for Lower-half Address Space

</td>
<td>


PGDL

</td>
</tr>
<tr>
<td>


0x1A

</td>
<td>


Page Global Directory Address for Higher-half Address Space

</td>
<td>


PGDH

</td>
</tr>
<tr>
<td>


0x1B

</td>
<td>


Page Global Directory Address

</td>
<td>


PGD

</td>
</tr>
<tr>
<td>


0x1C

</td>
<td>


Page Walk Control for Lower- half Address Space

</td>
<td>


PWCL

</td>
</tr>
<tr>
<td>


0x1D

</td>
<td>


Page Walk Control for Higher- half Address Space

</td>
<td>


PWCH

</td>
</tr>
<tr>
<td>


0x1E

</td>
<td>


STLB Page Size

</td>
<td>


STLBPS

</td>
</tr>
<tr>
<td>


0x1F

</td>
<td>


Reduced Virtual Address Configuration

</td>
<td>


RVACFG

</td>
</tr>
<tr>
<td>


0x20

</td>
<td>


CPU Identifier

</td>
<td>


CPUID

</td>
</tr>
<tr>
<td>


0x21

</td>
<td>


Privileged Resource Configuration 1

</td>
<td>


PRCFG1

</td>
</tr>
<tr>
<td>


0x22

</td>
<td>


Privileged Resource Configuration 2

</td>
<td>


PRCFG2

</td>
</tr>
<tr>
<td>


0x23

</td>
<td>


Privileged Resource Configuration 3

</td>
<td>


PRCFG3

</td>
</tr>
<tr>
<td>


0x30+n (0≤n≤15)

</td>
<td>


Saved Data register

</td>
<td>


SAVEn

</td>
</tr>
<tr>
<td>


0x40

</td>
<td>


Timer Identifier

</td>
<td>


TID

</td>
</tr>
<tr>
<td>


0x41

</td>
<td>


Timer Configuration

</td>
<td>


TCFG

</td>
</tr>
<tr>
<td>


0x42

</td>
<td>


Timer Value

</td>
<td>


TVAL

</td>
</tr>
<tr>
<td>


0x43

</td>
<td>


Compensation of Timer Count

</td>
<td>


CNTC

</td>
</tr>
<tr>
<td>


0x44

</td>
<td>


Timer Interrupt Clearing

</td>
<td>


TICLR

</td>
</tr>
<tr>
<td>


0x60

</td>
<td>


LLBit Control

</td>
<td>


LLBCTL

</td>
</tr>
<tr>
<td>


0x80

</td>
<td>


Implementation-specific Control 1

</td>
<td>


IMPCTL1

</td>
</tr>
<tr>
<td>


0x81

</td>
<td>


Implementation-specific Control 2

</td>
<td>


IMPCTL2

</td>
</tr>
<tr>
<td>


0x88

</td>
<td>


TLB Refill Exception Entrypoint Address

</td>
<td>


TLBRENTRY

</td>
</tr>
<tr>
<td>


0x89

</td>
<td>


TLB Refill Exception BAD (Faulting) Virtual Address

</td>
<td>


TLBRBADV

</td>
</tr>
<tr>
<td>


0x8A

</td>
<td>


TLB Refill Exception Return Address

</td>
<td>


TLBRERA

</td>
</tr>
<tr>
<td>


0x8B

</td>
<td>


TLB Refill Exception Saved Data Register

</td>
<td>


TLBRSAVE

</td>
</tr>
<tr>
<td>


0x8C

</td>
<td>


TLB Refill Exception Entry Low-order Bits 0

</td>
<td>


TLBRELO0

</td>
</tr>
<tr>
<td>


0x8D

</td>
<td>


TLB Refill Exception Entry Low-order Bits 1

</td>
<td>


TLBRELO1

</td>
</tr>
<tr>
<td>


0x8E

</td>
<td>


TLB Refill Exception Entry High-order Bits

</td>
<td>


TLBEHI

</td>
</tr>
<tr>
<td>


0x8F

</td>
<td>


TLB Refill Exception Pre-exception Mode Information

</td>
<td>


TLBRPRMD

</td>
</tr>
<tr>
<td>


0x90

</td>
<td>


Machine Error Control

</td>
<td>


MERRCTL

</td>
</tr>
<tr>
<td>


0x91

</td>
<td>


Machine Error Information 1

</td>
<td>


MERRINFO1

</td>
</tr>
<tr>
<td>


0x92

</td>
<td>


Machine Error Information 2

</td>
<td>


MERRINFO2

</td>
</tr>
<tr>
<td>


0x93

</td>
<td>


Machine Error Exception Entrypoint Address

</td>
<td>


MERRENTRY

</td>
</tr>
<tr>
<td>


0x94

</td>
<td>


Machine Error Exception Return Address

</td>
<td>


MERRERA

</td>
</tr>
<tr>
<td>


0x95

</td>
<td>


Machine Error Exception Saved Data Register

</td>
<td>


MERRSAVE

</td>
</tr>
<tr>
<td>


0x98

</td>
<td>


Cache TAGs

</td>
<td>


CTAG

</td>
</tr>
<tr>
<td>


0x180+n (0≤n≤3)

</td>
<td>


Direct Mapping Configuration Window n

</td>
<td>


DMWn

</td>
</tr>
<tr>
<td>


0x200+2n (0≤n≤31)

</td>
<td>


Performance Monitor Configuration n

</td>
<td>


PMCFGn

</td>
</tr>
<tr>
<td>


0x201+2n (0≤n≤31)

</td>
<td>


Performance Monitor Overall Counter n

</td>
<td>


PMCNTn

</td>
</tr>
<tr>
<td>


0x300

</td>
<td>


Memory Load/Store WatchPoint Overall Control

</td>
<td>


MWPC

</td>
</tr>
<tr>
<td>


0x301

</td>
<td>


Memory Load/Store WatchPoint Overall Status

</td>
<td>


MWPS

</td>
</tr>
<tr>
<td>


0x310+8n (0≤n≤7)

</td>
<td>


Memory Load/Store WatchPoint n Configuration 1

</td>
<td>


MWPnCFG1

</td>
</tr>
<tr>
<td>


0x311+8n (0≤n≤7)

</td>
<td>


Memory Load/Store WatchPoint n Configuration 2

</td>
<td>


MWPnCFG2

</td>
</tr>
<tr>
<td>


0x312+8n (0≤n≤7)

</td>
<td>


Memory Load/Store WatchPoint n Configuration 3

</td>
<td>


MWPnCFG3

</td>
</tr>
<tr>
<td>


0x313+8n (0≤n≤7)

</td>
<td>


Memory Load/Store WatchPoint n Configuration 4

</td>
<td>


MWPnCFG4

</td>
</tr>
<tr>
<td>


0x380

</td>
<td>


Instruction Fetch WatchPoint Overall Control

</td>
<td>


FWPC

</td>
</tr>
<tr>
<td>


0x381

</td>
<td>


Instruction Fetch WatchPoint Overall Status

</td>
<td>


FWPS

</td>
</tr>
<tr>
<td>


0x390+8n (0≤n≤7)

</td>
<td>


Instruction Fetch WatchPoint n Configuration 1

</td>
<td>


FWPnCFG1

</td>
</tr>
<tr>
<td>


0x391+8n (0≤n≤7)

</td>
<td>


Instruction Fetch WatchPoint n Configuration 2

</td>
<td>


FWPnCFG2

</td>
</tr>
<tr>
<td>


0x392+8n (0≤n≤7)

</td>
<td>


Instruction Fetch WatchPoint n Configuration 3

</td>
<td>


FWPnCFG3

</td>
</tr>
<tr>
<td>


0x393+8n (0≤n≤7)

</td>
<td>


Instruction Fetch WatchPoint n Configuration 4

</td>
<td>


FWPnCFG4

</td>
</tr>
<tr>
<td>


0x500

</td>
<td>


Debug Register

</td>
<td>


DBG

</td>
</tr>
<tr>
<td>


0x501

</td>
<td>


Debug Exception Return Address

</td>
<td>


DERA

</td>
</tr>
<tr>
<td>


0x502

</td>
<td>


Debug Exception Saved Data Register

</td>
<td>


DSAVE

</td>
</tr>
</tbody>
</table>

ERA, TLBRERA, MERRERA and DERA are sometimes also known as EPC, TLBREPC, MERREPC and DEPC respectively.

<a id="rst-basic-instruction-set"></a>

## Basic Instruction Set

<a id="rst-instruction-formats"></a>

### Instruction formats

LoongArch instructions are 32 bits wide, belonging to 9 basic instruction formats (and variants of them):


<table>
<thead>
<tr>
<th>


Format name

</th>
<th>


Composition

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


2R

</td>
<td>


Opcode + Rj + Rd

</td>
</tr>
<tr>
<td>


3R

</td>
<td>


Opcode + Rk + Rj + Rd

</td>
</tr>
<tr>
<td>


4R

</td>
<td>


Opcode + Ra + Rk + Rj + Rd

</td>
</tr>
<tr>
<td>


2RI8

</td>
<td>


Opcode + I8 + Rj + Rd

</td>
</tr>
<tr>
<td>


2RI12

</td>
<td>


Opcode + I12 + Rj + Rd

</td>
</tr>
<tr>
<td>


2RI14

</td>
<td>


Opcode + I14 + Rj + Rd

</td>
</tr>
<tr>
<td>


2RI16

</td>
<td>


Opcode + I16 + Rj + Rd

</td>
</tr>
<tr>
<td>


1RI21

</td>
<td>


Opcode + I21L + Rj + I21H

</td>
</tr>
<tr>
<td>


I26

</td>
<td>


Opcode + I26L + I26H

</td>
</tr>
</tbody>
</table>

Rd is the destination register operand, while Rj, Rk and Ra ("a" stands for "additional") are the source register operands. I8/I12/I14/I16/I21/I26 are immediate operands of respective width. The longer I21 and I26 are stored in separate higher and lower parts in the instruction word, denoted by the "L" and "H" suffixes.

<a id="rst-list-of-instructions"></a>

### List of Instructions

For brevity, only instruction names (mnemonics) are listed here; please see the [References](<#rst-loongarch-references>) for details.

1. Arithmetic Instructions:



   ```text
   ADD.W SUB.W ADDI.W ADD.D SUB.D ADDI.D
   SLT SLTU SLTI SLTUI
   AND OR NOR XOR ANDN ORN ANDI ORI XORI
   MUL.W MULH.W MULH.WU DIV.W DIV.WU MOD.W MOD.WU
   MUL.D MULH.D MULH.DU DIV.D DIV.DU MOD.D MOD.DU
   PCADDI PCADDU12I PCADDU18I
   LU12I.W LU32I.D LU52I.D ADDU16I.D
   ```

2. Bit-shift Instructions:



   ```text
   SLL.W SRL.W SRA.W ROTR.W SLLI.W SRLI.W SRAI.W ROTRI.W
   SLL.D SRL.D SRA.D ROTR.D SLLI.D SRLI.D SRAI.D ROTRI.D
   ```

3. Bit-manipulation Instructions:



   ```text
   EXT.W.B EXT.W.H CLO.W CLO.D SLZ.W CLZ.D CTO.W CTO.D CTZ.W CTZ.D
   BYTEPICK.W BYTEPICK.D BSTRINS.W BSTRINS.D BSTRPICK.W BSTRPICK.D
   REVB.2H REVB.4H REVB.2W REVB.D REVH.2W REVH.D BITREV.4B BITREV.8B BITREV.W BITREV.D
   MASKEQZ MASKNEZ
   ```

4. Branch Instructions:



   ```text
   BEQ BNE BLT BGE BLTU BGEU BEQZ BNEZ B BL JIRL
   ```

5. Load/Store Instructions:



   ```text
   LD.B LD.BU LD.H LD.HU LD.W LD.WU LD.D ST.B ST.H ST.W ST.D
   LDX.B LDX.BU LDX.H LDX.HU LDX.W LDX.WU LDX.D STX.B STX.H STX.W STX.D
   LDPTR.W LDPTR.D STPTR.W STPTR.D
   PRELD PRELDX
   ```

6. Atomic Operation Instructions:



   ```text
   LL.W SC.W LL.D SC.D
   AMSWAP.W AMSWAP.D AMADD.W AMADD.D AMAND.W AMAND.D AMOR.W AMOR.D AMXOR.W AMXOR.D
   AMMAX.W AMMAX.D AMMIN.W AMMIN.D
   ```

7. Barrier Instructions:



   ```text
   IBAR DBAR
   ```

8. Special Instructions:



   ```text
   SYSCALL BREAK CPUCFG NOP IDLE ERTN(ERET) DBCL(DBGCALL) RDTIMEL.W RDTIMEH.W RDTIME.D
   ASRTLE.D ASRTGT.D
   ```

9. Privileged Instructions:



   ```text
   CSRRD CSRWR CSRXCHG
   IOCSRRD.B IOCSRRD.H IOCSRRD.W IOCSRRD.D IOCSRWR.B IOCSRWR.H IOCSRWR.W IOCSRWR.D
   CACOP TLBP(TLBSRCH) TLBRD TLBWR TLBFILL TLBCLR TLBFLUSH INVTLB LDDIR LDPTE
   ```

<a id="rst-virtual-memory"></a>

## Virtual Memory

LoongArch supports direct-mapped virtual memory and page-mapped virtual memory.

Direct-mapped virtual memory is configured by CSR.DMWn (n=0\~3), it has a simple relationship between virtual address (VA) and physical address (PA):



```text
VA = PA + FixedOffset
```

Page-mapped virtual memory has arbitrary relationship between VA and PA, which is recorded in TLB and page tables. LoongArch's TLB includes a fully-associative MTLB (Multiple Page Size TLB) and set-associative STLB (Single Page Size TLB).

By default, the whole virtual address space of LA32 is configured like this:


<table>
<thead>
<tr>
<th>


Name

</th>
<th>


Address Range

</th>
<th>


Attributes

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


`UVRANGE`

</td>
<td>


`0x00000000 - 0x7FFFFFFF`

</td>
<td>


Page-mapped, Cached, PLV0\~3

</td>
</tr>
<tr>
<td>


`KPRANGE0`

</td>
<td>


`0x80000000 - 0x9FFFFFFF`

</td>
<td>


Direct-mapped, Uncached, PLV0

</td>
</tr>
<tr>
<td>


`KPRANGE1`

</td>
<td>


`0xA0000000 - 0xBFFFFFFF`

</td>
<td>


Direct-mapped, Cached, PLV0

</td>
</tr>
<tr>
<td>


`KVRANGE`

</td>
<td>


`0xC0000000 - 0xFFFFFFFF`

</td>
<td>


Page-mapped, Cached, PLV0

</td>
</tr>
</tbody>
</table>

User mode (PLV3) can only access UVRANGE. For direct-mapped KPRANGE0 and KPRANGE1, PA is equal to VA with bit30\~31 cleared. For example, the uncached direct-mapped VA of 0x00001000 is 0x80001000, and the cached direct-mapped VA of 0x00001000 is 0xA0001000.

By default, the whole virtual address space of LA64 is configured like this:


<table>
<thead>
<tr>
<th>


Name

</th>
<th>


Address Range

</th>
<th>


Attributes

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


`XUVRANGE`

</td>
<td>


`0x0000000000000000 - 0x3FFFFFFFFFFFFFFF`

</td>
<td>


Page-mapped, Cached, PLV0\~3

</td>
</tr>
<tr>
<td>


`XSPRANGE`

</td>
<td>


`0x4000000000000000 - 0x7FFFFFFFFFFFFFFF`

</td>
<td>


Direct-mapped, Cached / Uncached, PLV0

</td>
</tr>
<tr>
<td>


`XKPRANGE`

</td>
<td>


`0x8000000000000000 - 0xBFFFFFFFFFFFFFFF`

</td>
<td>


Direct-mapped, Cached / Uncached, PLV0

</td>
</tr>
<tr>
<td>


`XKVRANGE`

</td>
<td>


`0xC000000000000000 - 0xFFFFFFFFFFFFFFFF`

</td>
<td>


Page-mapped, Cached, PLV0

</td>
</tr>
</tbody>
</table>

User mode (PLV3) can only access XUVRANGE. For direct-mapped XSPRANGE and XKPRANGE, PA is equal to VA with bits 60\~63 cleared, and the cache attribute is configured by bits 60\~61 in VA: 0 is for strongly-ordered uncached, 1 is for coherent cached, and 2 is for weakly-ordered uncached.

Currently we only use XKPRANGE for direct mapping and XSPRANGE is reserved.

To put this in action: the strongly-ordered uncached direct-mapped VA (in XKPRANGE) of 0x00000000_00001000 is 0x80000000_00001000, the coherent cached direct-mapped VA (in XKPRANGE) of 0x00000000_00001000 is 0x90000000_00001000, and the weakly-ordered uncached direct-mapped VA (in XKPRANGE) of 0x00000000 \_00001000 is 0xA0000000_00001000.

<a id="rst-relationship-of-loongson-and-loongarch"></a>

## Relationship of Loongson and LoongArch

LoongArch is a RISC ISA which is different from any other existing ones, while Loongson is a family of processors. Loongson includes 3 series: Loongson-1 is the 32-bit processor series, Loongson-2 is the low-end 64-bit processor series, and Loongson-3 is the high-end 64-bit processor series. Old Loongson is based on MIPS, while New Loongson is based on LoongArch. Take Loongson-3 as an example: Loongson-3A1000/3B1500/3A2000/3A3000/3A4000 are MIPS-compatible, while Loongson- 3A5000 (and future revisions) are all based on LoongArch.

<a id="rst-references"></a>
<a id="rst-loongarch-references"></a>

## References

Official web site of Loongson Technology Corp. Ltd.:

> [http://www.loongson.cn/](<http://www.loongson.cn/>)

Developer web site of Loongson and LoongArch (Software and Documentation):

> [http://www.loongnix.cn/](<http://www.loongnix.cn/>)
>
> [https://github.com/loongson/](<https://github.com/loongson/>)
>
> [https://loongson.github.io/LoongArch-Documentation/](<https://loongson.github.io/LoongArch-Documentation/>)

Documentation of LoongArch ISA:

> [https://github.com/loongson/LoongArch-Documentation/releases/latest/download/LoongArch-Vol1-v1.10-CN.pdf](<https://github.com/loongson/LoongArch-Documentation/releases/latest/download/LoongArch-Vol1-v1.10-CN.pdf>) (in Chinese)
>
> [https://github.com/loongson/LoongArch-Documentation/releases/latest/download/LoongArch-Vol1-v1.10-EN.pdf](<https://github.com/loongson/LoongArch-Documentation/releases/latest/download/LoongArch-Vol1-v1.10-EN.pdf>) (in English)

Documentation of LoongArch ELF psABI:

> [https://github.com/loongson/LoongArch-Documentation/releases/latest/download/LoongArch-ELF-ABI-v2.01-CN.pdf](<https://github.com/loongson/LoongArch-Documentation/releases/latest/download/LoongArch-ELF-ABI-v2.01-CN.pdf>) (in Chinese)
>
> [https://github.com/loongson/LoongArch-Documentation/releases/latest/download/LoongArch-ELF-ABI-v2.01-EN.pdf](<https://github.com/loongson/LoongArch-Documentation/releases/latest/download/LoongArch-ELF-ABI-v2.01-EN.pdf>) (in English)

Linux kernel repository of Loongson and LoongArch:

> [https://git.kernel.org/pub/scm/linux/kernel/git/chenhuacai/linux-loongson.git](<https://git.kernel.org/pub/scm/linux/kernel/git/chenhuacai/linux-loongson.git>)
