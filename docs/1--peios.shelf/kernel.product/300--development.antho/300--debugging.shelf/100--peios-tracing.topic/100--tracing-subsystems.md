---
title: Tracing Peios Subsystems
type: how-to
description: Inspect access decisions and subsystem diagnostics through the running kernel trace interface.
---

Peios subsystems expose static Linux tracepoints for implementation
diagnostics. Use them when a result needs explanation inside the kernel.
They are separate from the KMES event catalog and its audit records.

## Choose a subsystem

The trace systems cover different questions:

| System | Typical evidence |
|---|---|
| `kacs` | Instrumented access decisions, object identifiers, masks, and return-path reasons |
| `kmes` | Event transport, validation, loss, throttling, and buffer changes |
| `lcs` | Registry source requests, responses, timeouts, and state changes |

The running kernel's `tracefs` event list is authoritative for that build.
The `format` file defines each event's fields and symbolic formatting.
Diagnostic constants are maintained in `include/uapi/pkm/trace.h`; do not
infer a reason number from a different kernel version.

On a development system with tracing available, inspect an event before
selecting it:

```sh
ls /sys/kernel/tracing/events/kacs
ls /sys/kernel/tracing/events/kmes
ls /sys/kernel/tracing/events/lcs
cat /sys/kernel/tracing/events/kacs/kacs_file_access/format
```

Missing entries can mean that tracing is unavailable, the filesystem is not
mounted at this path, or the selected kernel lacks the event. Do not treat
them as evidence that an operation did not occur.

## Capture a narrow interval

Changing trace controls requires permission. Coordinate with other tracing
users, note the existing settings, and restore them after capture. Enabling a
whole subsystem can produce substantial output; start with one event.

From the trace filesystem, a focused access-check capture uses these controls:

```sh
cd /sys/kernel/tracing
printf '%s\n' 'ret != 0' > events/kacs/kacs_file_access/filter
printf '1\n' > events/kacs/kacs_file_access/enable
printf '1\n' > tracing_on
cat trace
```

Read `trace` after reproducing the operation. This example changes global
trace settings and leaves the event enabled until you restore them. A live
stream reader and a snapshot have different consumption behavior; use the
[tracing reference](~kernel/development/trace/events) when designing a
capture tool.

Filters operate on structured fields. For an event whose format exposes
`ino`, an `ino == <number>` filter narrows the object. Use the field names
from that event's format. perf and eBPF attach to the same tracepoints where
the kernel configuration and permissions allow them.

## Interpret a KACS decision

A negative `ret` describes a refusal; zero describes success at that
instrumented return path. `reason` identifies the path taken. `access` is the
requested mask, and `mount_policy` can explain the filesystem's treatment.
`ino` and `sb_magic` provide context, not a globally unique pathname.

Trace events expose operational information even when they omit pathnames
and descriptor bytes. Limit collection and access to the resulting logs.
Disabled static tracepoints have low overhead; enabled collection has real
cost and finite buffering. A trace is not a complete audit guarantee.

## Trace early boot

For events registered early enough, the kernel command line can enable a
selection and send it to the console:

```text
trace_event=kacs:kacs_file_access tp_printk
```

A broader selection is `trace_event=kacs:*,kmes:*,lcs:*`. It can overwhelm a
slow console and alter timing. Preserve the exact command line and serial
log, and check for dropped output. Registration order and console readiness
limit what can be observed; this does not promise every early decision.

The former `kacs.trace=1` switch is not the maintained interface. Use the
trace event controls and the [kernel event model](~kernel/internals/kmes/event-model)
to distinguish trace diagnostics from records delivered through KMES.
