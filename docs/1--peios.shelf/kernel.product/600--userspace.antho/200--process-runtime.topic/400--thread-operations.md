---
title: Thread Operations
type: reference
description: Reference thread IDs, clear-TID notification, and architecture-specific TLS setup.
---

Thread operations act on one task inside a process. A task ID is a kernel
identifier, not the security identity under which the thread acts.

## Identify a thread

`gettid()` returns the calling thread's TID. `getpid()` returns its thread
group ID, shared by all threads in that process. The leader's TID equals the
thread group ID. IDs are reported in the caller's PID namespace and can be
reused after the task's lifetime.

A threading library's opaque thread handle is not interchangeable with a
kernel TID. Thread-targeted signals, affinity operations, and task directories
use their own kernel interfaces. Peios impersonation belongs to the thread's
effective credentials, not to its numeric TID.

## Clear-TID notification

`set_tid_address()` records the calling thread's clear-TID address and returns
its TID. `CLONE_CHILD_CLEARTID` arranges the same exit-time mechanism during
creation. On the applicable exit path, the kernel attempts to write zero to
the address and wake one futex waiter when another user of the address space
remains.

Keep that memory valid until the protocol completes. A waiter must check the
value and use the futex comparison protocol so an exit between checking and
sleeping does not become a lost wakeup. Account for spurious wakeups and the
possibility that the task has already exited. The kernel wake is one part of
a thread library's join implementation, not a complete ownership or memory
reclamation protocol by itself.

## Thread-local storage

The compiler and runtime define the TLS layout and access convention. The
kernel maintains architecture-specific per-thread state used to locate that
layout. `CLONE_SETTLS` supplies it at task creation.

On x86-64, `arch_prctl` with `ARCH_SET_FS` sets the FS base used by common
runtimes. The older x86 `set_thread_area` interface uses a descriptor rather
than the same raw-pointer contract. Do not rewrite the runtime's TLS base
while continuing to call code that expects the old layout.

The [creation reference](~kernel/userspace/process-runtime/creating-processes)
connects TLS and TID bookkeeping to the clone flags. The runtime owns thread
startup, language TLS initialization, destructors, and joining above that ABI.
