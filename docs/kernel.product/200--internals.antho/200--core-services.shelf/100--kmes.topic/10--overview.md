---
title: "Overview"
description: "KMES is the sole event emission path in Peios, used by kernel subsystems and userspace alike, and the terms this chapter uses for it."
type: reference
---

<a id="trm-2-1"></a>

The Kernel Mediated Event Subsystem is the sole event emission path in
Peios. Kernel subsystems and userspace processes alike emit events
exclusively through KMES — there is no alternative path. KMES stamps
each event with trusted metadata at emission time, buffers it in
per-CPU shared memory ring buffers, and delivers it to userspace
consumers that map those buffers directly. It does not persist, index,
or query events, and it imposes no schema or naming convention on them;
those are consumer concerns, handled by eventd.

KMES serves a similar role to ETW in the Windows kernel and auditd in
Linux, but is compatible with neither at the wire, format, or API
level. The design — structured events with a fixed binary header and a
msgpack payload, shared memory delivery, one emission path for kernel
and userspace — was chosen for unified observability with
kernel-trusted metadata.

The consumer-facing contract — the event header layout, the mapped
ring buffer regions, and the protocols a consumer follows to drain,
sleep, and survive buffer swaps — is specified in PSPK's KMES event
stream chapter. This chapter describes the kernel side: how events are
constructed and stamped ([Event Model](<~kernel/internals/kmes/event-model#trm-2-2>)), the in-kernel emission API ([Emission API](<~kernel/internals/kmes/emission-api#trm-2-3>)), the
syscall surface ([Syscall Interface](<~kernel/userspace/native/kmes/emission-and-attachment-syscalls#trm-2-4>)), how the ring buffers are organised and written
([Ring Buffers](<~kernel/internals/kmes/ring-buffers#trm-2-5>)), self-configuration through the registry ([Self-Configuration](<~kernel/internals/kmes/self-configuration#trm-2-6>)), behaviour
under failure ([Failure Modes](<~kernel/internals/kmes/failure-modes#trm-2-7>)), and the emission policy that decides which of
the kernel's own event types are written ([Emission Policy](<~kernel/internals/kmes/emission-policy#trm-2-8>)).

<a id="trm-2-1-1"></a>

## Terminology

An **event** is an indivisible record: a packed binary **header**
carrying KMES-intrinsic metadata, followed by a msgpack-encoded
**payload** whose structure is defined by the emitter. Header and
payload are produced, stored, and consumed together as one contiguous
byte sequence; neither is meaningful alone. KMES treats the payload as
opaque.

The **stamp** fields are the header fields KMES populates itself at
emission time: the timestamp, sequence number, CPU identifier, and
origin class, plus three identity GUIDs captured from KACS — the
**effective token GUID** (the token governing the emitting thread's
access rights, which is the impersonation token when the thread is
impersonating), the **true token GUID** (the process's primary token,
regardless of impersonation), and the **process GUID** (assigned by
KACS at fork and unchanged across exec). The **null GUID** — sixteen
zero bytes — stamps an identity field whose value is unavailable. <a id="cite-event.null-guid-means-unavailable"></a>

The **sequence number** is a per-CPU, per-boot monotonic 64-bit
counter. Each CPU counts independently; the counter starts at zero
when PKM loads and is incremented before its value is taken, so the
first event on each CPU carries sequence number 1 and sequence 0 is
never assigned. <a id="cite-event.sequence-starts-at-one"></a> A gap in one CPU's sequence indicates lost events. The
pair (`cpu_id`, `sequence`) uniquely identifies an event within a
boot; there is no global sequence. <a id="cite-event.sequence-scoped-per-cpu"></a>

The **origin class** is a header byte identifying the emission path:
userspace (0), KMES itself (1), KACS (2), or LCS (3). Values 4–255 are
unassigned. <a id="cite-event.origin-classes-assigned"></a>

The **event type** is a length-prefixed UTF-8 string in the header
identifying the kind of event. KMES imposes no structure on it and
compares nothing against it; types are consumer vocabulary. <a id="cite-event.type-opaque"></a>

A **ring buffer** is a per-CPU shared memory region — producer
metadata page, consumer metadata page, and a data region — created
and managed by KMES and mapped by consumers. A **consumer** is a
userspace process that maps one or more ring buffers and drains events
from them, typically with one thread per CPU. **Boot-time ring
buffers** are the ordinary per-CPU buffers created at module load
using compiled-in defaults; they are the live consumer-facing buffers
from the first instant, not a separate class. <a id="cite-ring.boot-buffers-ordinary"></a>

<a id="trm-2-b-6"></a>

## Build configuration <a id="cite-build.config-security-pkm"></a>

KMES is built by `CONFIG_SECURITY_PKM`, a boolean option, so it is
linked into `vmlinux` rather than loaded. `CONFIG_RUST=y` is required:
the MessagePack validator is Rust. The subsystem lives in
`security/pkm/kmes`, with tracepoint declarations in
`include/trace/events/kmes.h`.

The three syscall numbers are registered in
`arch/x86/entry/syscalls/syscall_64.tbl` and the corresponding table
under `tools/perf/`. They are registered `common` in the table, but the
kernel is built without `CONFIG_X86_X32_ABI`, so the only entry point
that exists is x86-64: an x32 invocation (the number with bit 30 set)
fails `ENOSYS` like any other x32 syscall on this
kernel. <a id="cite-build.syscalls-registered-common"></a>

`CONFIG_SECURITY_PKM_KUNIT` compiles in the in-kernel test harness.

## Related explanations

- [Self-configuration](<~kernel/internals/kmes/self-configuration>)
- [ABI semantics and limits](<~kernel/userspace/native/kmes/abi-semantics-and-limits>)

## Calling the subsystem

The [native KMES interface reference](<~kernel/userspace/native/kmes/overview>) collects the caller contracts and generated ABI tables.
