---
title: "membarrier() System Call"
type: reference
description: "The commands MEMBARRIER_CMD_PRIVATE_EXPEDITED and MEMBARRIER_CMD_GLOBAL_EXPEDITED require each architecture to have a full memory barrier after coming from user-space, before updating rq->curr. This barrier is implied by the sequence…"
---

<a id="rst-membarrier-system-call"></a>

<a id="rst-membarrier-cmd-private-global-expedited-architecture-requirements"></a>

## MEMBARRIER_CMD\_\{PRIVATE,GLOBAL\}\_EXPEDITED - Architecture requirements

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-memory-barriers-before-updating-rq-curr"></a>

## Memory barriers before updating rq-&gt;curr

The commands MEMBARRIER_CMD_PRIVATE_EXPEDITED and MEMBARRIER_CMD_GLOBAL_EXPEDITED require each architecture to have a full memory barrier after coming from user-space, before updating rq-&gt;curr.  This barrier is implied by the sequence rq_lock(); smp_mb__after_spinlock() in \__schedule().  The barrier matches a full barrier in the proximity of the membarrier system call exit, cf. membarrier\_\{private,global\}\_expedited().

<a id="rst-memory-barriers-after-updating-rq-curr"></a>

## Memory barriers after updating rq-&gt;curr

The commands MEMBARRIER_CMD_PRIVATE_EXPEDITED and MEMBARRIER_CMD_GLOBAL_EXPEDITED require each architecture to have a full memory barrier after updating rq-&gt;curr, before returning to user-space.  The schemes providing this barrier on the various architectures are as follows.

> - alpha, arc, arm, hexagon, mips rely on the full barrier implied by spin_unlock() in finish_lock_switch().
>
> - arm64 relies on the full barrier implied by switch_to().
>
> - powerpc, riscv, s390, sparc, x86 rely on the full barrier implied by switch_mm(), if mm is not NULL; they rely on the full barrier implied by mmdrop(), otherwise.  On powerpc and riscv, switch_mm() relies on membarrier_arch_switch_mm().

The barrier matches a full barrier in the proximity of the membarrier system call entry, cf. membarrier\_\{private,global\}\_expedited().
