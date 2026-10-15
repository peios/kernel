---
title: "Register Usage for Linux/PA-RISC"
type: reference
description: "[ an asterisk is used for planned usage which is currently unimplemented ]"
---

<a id="rst-register-usage-for-linux-pa-risc"></a>

\[ an asterisk is used for planned usage which is currently unimplemented \]

<a id="rst-general-registers-as-specified-by-abi"></a>

## General Registers as specified by ABI

<a id="rst-control-registers"></a>

### Control Registers


<table>
<tbody>
<tr>
<td>


CR 0 (Recovery Counter)

</td>
<td>


used for ptrace

</td>
</tr>
<tr>
<td>


CR 1-CR 7(undefined)

</td>
<td>


unused

</td>
</tr>
<tr>
<td>


CR 8 (Protection ID)

</td>
<td>


per-process value\*

</td>
</tr>
<tr>
<td>


CR 9, 12, 13 (PIDS)

</td>
<td>


unused

</td>
</tr>
<tr>
<td>


CR10 (CCR)

</td>
<td>


lazy FPU saving\*

</td>
</tr>
<tr>
<td>


CR11

</td>
<td>


as specified by ABI (SAR)

</td>
</tr>
<tr>
<td>


CR14 (interruption vector)

</td>
<td>


initialized to fault_vector

</td>
</tr>
<tr>
<td>


CR15 (EIEM)

</td>
<td>


initialized to all ones\*

</td>
</tr>
<tr>
<td>


CR16 (Interval Timer)

</td>
<td>


read for cycle count/write starts Interval Tmr

</td>
</tr>
<tr>
<td>


CR17-CR22

</td>
<td>


interruption parameters

</td>
</tr>
<tr>
<td>


CR19

</td>
<td>


Interrupt Instruction Register

</td>
</tr>
<tr>
<td>


CR20

</td>
<td>


Interrupt Space Register

</td>
</tr>
<tr>
<td>


CR21

</td>
<td>


Interrupt Offset Register

</td>
</tr>
<tr>
<td>


CR22

</td>
<td>


Interrupt PSW

</td>
</tr>
<tr>
<td>


CR23 (EIRR)

</td>
<td>


read for pending interrupts/write clears bits

</td>
</tr>
<tr>
<td>


CR24 (TR 0)

</td>
<td>


Kernel Space Page Directory Pointer

</td>
</tr>
<tr>
<td>


CR25 (TR 1)

</td>
<td>


User   Space Page Directory Pointer

</td>
</tr>
<tr>
<td>


CR26 (TR 2)

</td>
<td>


not used

</td>
</tr>
<tr>
<td>


CR27 (TR 3)

</td>
<td>


Thread descriptor pointer

</td>
</tr>
<tr>
<td>


CR28 (TR 4)

</td>
<td>


not used

</td>
</tr>
<tr>
<td>


CR29 (TR 5)

</td>
<td>


not used

</td>
</tr>
<tr>
<td>


CR30 (TR 6)

</td>
<td>


current / 0

</td>
</tr>
<tr>
<td>


CR31 (TR 7)

</td>
<td>


Temporary register, used in various places

</td>
</tr>
</tbody>
</table>

<a id="rst-space-registers-kernel-mode"></a>

### Space Registers (kernel mode)


<table>
<tbody>
<tr>
<td>


SR0

</td>
<td>


temporary space register

</td>
</tr>
<tr>
<td>


SR4-SR7

</td>
<td>


set to 0

</td>
</tr>
<tr>
<td>


SR1

</td>
<td>


temporary space register

</td>
</tr>
<tr>
<td>


SR2

</td>
<td>


kernel should not clobber this

</td>
</tr>
<tr>
<td>


SR3

</td>
<td>


used for userspace accesses (current process)

</td>
</tr>
</tbody>
</table>

<a id="rst-space-registers-user-mode"></a>

### Space Registers (user mode)


<table>
<tbody>
<tr>
<td>


SR0

</td>
<td>


temporary space register

</td>
</tr>
<tr>
<td>


SR1

</td>
<td>


temporary space register

</td>
</tr>
<tr>
<td>


SR2

</td>
<td>


holds space of linux gateway page

</td>
</tr>
<tr>
<td>


SR3

</td>
<td>


holds user address space value while in kernel

</td>
</tr>
<tr>
<td>


SR4-SR7

</td>
<td>


Defines short address space for user/kernel

</td>
</tr>
</tbody>
</table>

<a id="rst-processor-status-word"></a>

### Processor Status Word


<table>
<tbody>
<tr>
<td>


W (64-bit addresses)

</td>
<td>


0

</td>
</tr>
<tr>
<td>


E (Little-endian)

</td>
<td>


0

</td>
</tr>
<tr>
<td>


S (Secure Interval Timer)

</td>
<td>


0

</td>
</tr>
<tr>
<td>


T (Taken Branch Trap)

</td>
<td>


0

</td>
</tr>
<tr>
<td>


H (Higher-privilege trap)

</td>
<td>


0

</td>
</tr>
<tr>
<td>


L (Lower-privilege trap)

</td>
<td>


0

</td>
</tr>
<tr>
<td>


N (Nullify next instruction)

</td>
<td>


used by C code

</td>
</tr>
<tr>
<td>


X (Data memory break disable)

</td>
<td>


0

</td>
</tr>
<tr>
<td>


B (Taken Branch)

</td>
<td>


used by C code

</td>
</tr>
<tr>
<td>


C (code address translation)

</td>
<td>


1, 0 while executing real-mode code

</td>
</tr>
<tr>
<td>


V (divide step correction)

</td>
<td>


used by C code

</td>
</tr>
<tr>
<td>


M (HPMC mask)

</td>
<td>


0, 1 while executing HPMC handler\*

</td>
</tr>
<tr>
<td>


C/B (carry/borrow bits)

</td>
<td>


used by C code

</td>
</tr>
<tr>
<td>


O (ordered references)

</td>
<td>


1\*

</td>
</tr>
<tr>
<td>


F (performance monitor)

</td>
<td>


0

</td>
</tr>
<tr>
<td>


R (Recovery Counter trap)

</td>
<td>


0

</td>
</tr>
<tr>
<td>


Q (collect interruption state)

</td>
<td>


1 (0 in code directly preceding an rfi)

</td>
</tr>
<tr>
<td>


P (Protection Identifiers)

</td>
<td>


1\*

</td>
</tr>
<tr>
<td>


D (Data address translation)

</td>
<td>


1, 0 while executing real-mode code

</td>
</tr>
<tr>
<td>


I (external interrupt mask)

</td>
<td>


used by cli()/sti() macros

</td>
</tr>
</tbody>
</table>

<a id="rst-invisible-registers"></a>

### "Invisible" Registers


<table>
<tbody>
<tr>
<td>


PSW default W value

</td>
<td>


0

</td>
</tr>
<tr>
<td>


PSW default E value

</td>
<td>


0

</td>
</tr>
<tr>
<td>


Shadow Registers

</td>
<td>


used by interruption handler code

</td>
</tr>
<tr>
<td>


TOC enable bit

</td>
<td>


1

</td>
</tr>
</tbody>
</table>

---

The PA-RISC architecture defines 7 registers as "shadow registers". Those are used in RETURN FROM INTERRUPTION AND RESTORE instruction to reduce the state save and restore time by eliminating the need for general register (GR) saves and restores in interruption handlers. Shadow registers are the GRs 1, 8, 9, 16, 17, 24, and 25.

---

Register usage notes, originally from John Marvin, with some additional notes from Randolph Chung.

For the general registers:

r1,r2,r19-r26,r28,r29 &amp; r31 can be used without saving them first. And of course, you need to save them if you care about them, before calling another procedure. Some of the above registers do have special meanings that you should be aware of:

> - **r1:**
>
>   The addil instruction is hardwired to place its result in r1, so if you use that instruction be aware of that.
>
> - **r2:**
>
>   This is the return pointer. In general you don't want to use this, since you need the pointer to get back to your caller. However, it is grouped with this set of registers since the caller can't rely on the value being the same when you return, i.e. you can copy r2 to another register and return through that register after trashing r2, and that should not cause a problem for the calling routine.
>
> - **r19-r22:**
>
>   these are generally regarded as temporary registers. Note that in 64 bit they are arg7-arg4.
>
> - **r23-r26:**
>
>   these are arg3-arg0, i.e. you can use them if you don't care about the values that were passed in anymore.
>
> - **r28,r29:**
>
>   are ret0 and ret1. They are what you pass return values in. r28 is the primary return. When returning small structures r29 may also be used to pass data back to the caller.
>
> - **r30:**
>
>   stack pointer
>
> - **r31:**
>
>   the ble instruction puts the return pointer in here.
>
> r3-r18,r27,r30 need to be saved and restored. r3-r18 are just general purpose registers. r27 is the data pointer, and is used to make references to global variables easier. r30 is the stack pointer.
