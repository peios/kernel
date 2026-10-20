---
title: Locking
type: concept
description: Find the locking primitives, usage rules, implementation details, and diagnostic tools used inside the kernel.
---

<!-- SPDX-License-Identifier: GPL-2.0 -->

Kernel code can run concurrently on multiple CPUs and in different execution
contexts. Locking primitives coordinate access to shared state. The appropriate
primitive depends on the context, whether waiting may sleep, and the guarantees
the protected operation requires.

Start with [Lock types and their rules](~kernel/internals/locking/locktypes),
which explains sleeping, spinning, and CPU-local locks, their nesting rules,
and how their behaviour changes under PREEMPT_RT.

## Locking primitives

- [Spinlocks](~kernel/internals/locking/spinlocks) and [mutexes](~kernel/internals/locking/mutex-design).
- [RT-mutexes and priority inheritance](~kernel/internals/locking/rt-mutex), with a detailed [implementation guide](~kernel/internals/locking/rt-mutex-design).
- [Wound/wait mutexes](~kernel/internals/locking/ww-mutex-design) for acquiring multiple locks when their order is not fixed.
- [Sequence counters and sequential locks](~kernel/internals/locking/seqlock).
- [Per-CPU reader/writer semaphores](~kernel/internals/locking/percpu-rw-semaphore).
- [Hardware spinlocks](~kernel/internals/locking/hwspinlock).

## Execution context and userspace coordination

[Locking and preemption](~kernel/internals/locking/preempt-locking) describes
protection for per-CPU data, processor state, and critical sections.

The futex articles cover [priority inheritance](~kernel/internals/locking/pi-futex),
[requeueing](~kernel/internals/locking/futex-requeue-pi),
[robust futexes](~kernel/internals/locking/robust-futexes), and the
[robust futex ABI](~kernel/internals/locking/robust-futex-abi).

## Validation and diagnostics

- [Lock dependency validation](~kernel/internals/locking/lockdep-design) explains lockdep and its annotations.
- [Lock statistics](~kernel/internals/locking/lockstat) covers contention and hold-time measurements.
- [Lock torture tests](~kernel/internals/locking/locktorture) describes the locking stress-test module.
