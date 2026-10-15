---
title: "Device operations and errors"
description: "Device operations and errors: behaviour and implementation of the Peios kernel."
type: reference
---

<a id="trm-6-b"></a>

[NTFE ABI Reference](<~kernel/userspace/native/ntfe/generated-device-abi#trm-6-a>) is generated from `include/uapi/pkm/ntfe.h` and holds only what a
compiler can measure. This appendix holds the rest.

<a id="trm-6-b-1"></a>

## Stability

The ABI is **experimental** while NTFE grows (PEI-598): no stability
promise until the design ships. `peios_ntfe_status.abi` carries
`PEIOS_NTFE_ABI_VERSION`; <a id="cite-ntfe-abi-notes.status-abi-carries-version"></a> a consumer checks it before trusting any other
field or record layout. <a id="cite-ntfe-abi-notes.consumer-checks-abi-first"></a> Version 2 (the machinery slice) added the
event's `reject_kind`, the store confessions and `counter_cells` and
`reporting_level` in the status, and the counters ioctl. Version 3 (the
Flow layer) added the `LOCAL_OUT` seat and `Flow` layer ids, the
`REJUDGED` event flag, the Flow and refusal counters in the status, and
the flows ioctl. Version 4 (the identity facts) added the endpoints'
identities to the event and the flow record, the `IDENTITY_UNRESOLVED`
event flag and the `identity_unresolved` counter (in a reserved slot,
so the status kept its size). Version 5 renamed the device and every
symbol from `pnp` to `ntfe`, let more than one file hold the device open,
and added `changes_noted`, `changes_walked` and `contexts` to the status:
the first took one of the two reserved words version 4 left, the other
two are new, so the status grew by two words and keeps one reserved. <a id="cite-ntfe-abi-notes.abi-v5-changes"></a> pnpd and the kernel ship together on the
experimental edition, so the check is a guard, not a negotiation.

<a id="trm-6-b-2"></a>

## `/dev/peios-ntfe`

A misc device, created mode 0600 and owned by uid 0. Those Unix fields
do not grant native access: KACS checks an `open()` using the opener's
token and the node's security descriptor
([File Descriptor Storage](<~kernel/internals/kacs/file-security/descriptor-storage-and-caching#trm-3-9-5>)). On devtmpfs that descriptor is inherited from the seeded
root's, which grants `GENERIC_ALL` to SYSTEM alone, so the device is
SYSTEM's unless trusted userspace sets another. <a id="cite-ntfe-abi-notes.device-misc-0600-root-only"></a>

| Operation | Semantics | Errors |
|---|---|---|
| `open()` | Any number of openers. | — <a id="cite-ntfe-abi-notes.open-any-number-of-openers"></a> |
| `read(buf, len)` | Returns whole `struct peios_ntfe_event` records only — never a partial one — up to 64 per call, oldest first, consuming them. Blocks on an empty ring unless `O_NONBLOCK`. | `EINVAL` — `len` smaller than one record; `EBUSY` — another open file is the stream's reader; `EAGAIN` — empty and non-blocking; `EINTR`; `ENOMEM`; `EFAULT` — the records it took are lost (below) <a id="cite-ntfe-abi-notes.read-whole-records-oldest-first"></a> <a id="cite-ntfe-abi-notes.read-einval-len-below-one-record"></a> <a id="cite-ntfe-abi-notes.read-ebusy-other-file-is-reader"></a> <a id="cite-ntfe-abi-notes.read-eagain-empty-nonblocking"></a> <a id="cite-ntfe-abi-notes.read-eintr"></a> <a id="cite-ntfe-abi-notes.read-enomem"></a> <a id="cite-ntfe-abi-notes.read-efault"></a> |
| `poll()` | `POLLIN \| POLLRDNORM` when at least one event waits. | — <a id="cite-ntfe-abi-notes.poll-readable-when-event-waits"></a> |
| `ioctl(PEIOS_NTFE_IOC_STATUS, struct peios_ntfe_status *)` | Fills the status snapshot. Cumulative counters since boot. | `EFAULT` <a id="cite-ntfe-abi-notes.status-ioctl-fills-snapshot"></a> |
| `ioctl(PEIOS_NTFE_IOC_COUNTERS, struct peios_ntfe_counters_query *)` | `buf`/`buf_len` describe a user buffer of `struct peios_ntfe_counter_rec`; on return `count` is how many were written and `total` how many cells exist. A short buffer is not an error — the two numbers disagree. Best-effort snapshot: cells may change between records. | `EFAULT`; `ENOMEM` <a id="cite-ntfe-abi-notes.counters-ioctl-count-and-total"></a> <a id="cite-ntfe-abi-notes.counters-ioctl-efault"></a> <a id="cite-ntfe-abi-notes.counters-ioctl-enomem"></a> |
| `ioctl(PEIOS_NTFE_IOC_FLOWS, struct peios_ntfe_flows_query *)` | Same contract over `struct peios_ntfe_flow_rec`: `count` written, `total` live flows the walk saw. Records are copied out between hash buckets, so the dump is a best-effort picture of a table that changes under it. | `EFAULT`; `ENOMEM` <a id="cite-ntfe-abi-notes.flows-ioctl-count-and-total"></a> <a id="cite-ntfe-abi-notes.flows-ioctl-efault"></a> <a id="cite-ntfe-abi-notes.flows-ioctl-enomem"></a> |
| `ioctl(PEIOS_NTFE_IOC_LISTENERS, struct peios_ntfe_listeners_query *)` | Same contract over `struct peios_ntfe_listener_rec`: every TCP socket in the listening state and every bound UDP / UDP-Lite socket of the root network namespace, with the identity KACS stamped on it ([The identity facts](<~kernel/internals/ntfe/the-identity-facts#trm-6-9>)). `total` is how many the walk saw. A hash bucket holding more sockets than one copy-out batch is walked again from where the batch filled, so with room for every record `count` equals `total`. | `EFAULT`; `ENOMEM` <a id="cite-ntfe-abi-notes.listeners-ioctl-count-and-total"></a> <a id="cite-ntfe-abi-notes.listeners-ioctl-efault"></a> <a id="cite-ntfe-abi-notes.listeners-ioctl-enomem"></a> |
| other ioctls | — | `ENOTTY` <a id="cite-ntfe-abi-notes.unknown-ioctl-enotty"></a> |

Sequence numbers are monotonic per boot. <a id="cite-ntfe-abi-notes.sequence-monotonic-per-boot"></a> A gap between consecutive
records read is the number of events the ring overwrote while the
reader was away, plus any a faulting `read()` consumed; <a id="cite-ntfe-abi-notes.sequence-gap-equals-overwritten"></a> `events_dropped` in the status is the running
total of the overwrites. <a id="cite-ntfe-abi-notes.events-dropped-running-total"></a> A `read()` that fails with `EFAULT` has
already taken its records off the ring: they are lost, and counted
nowhere but in that gap. <a id="cite-ntfe-abi-notes.read-efault-consumes-records"></a>

<a id="trm-6-b-7"></a>

## Bounds not in the header

| Bound | Value |
|---|---|
| Event ring | 4096 records, overwrite-oldest <a id="cite-ntfe-abi-notes.bound-event-ring-4096"></a> |
| Records per `read()` | 64 <a id="cite-ntfe-abi-notes.bound-read-64-records"></a> |
| Counter cells per table | 4096 (`PEIOS_NTFE_COUNTER_MAX_KEYS`, kernel-internal) <a id="cite-ntfe-abi-notes.bound-counter-cells-per-table-4096"></a> |
| Distinct tags per flow | 64 (`PEIOS_NTFE_TAG_MAX_PER_FLOW`, kernel-internal) <a id="cite-ntfe-abi-notes.bound-tags-per-flow-64"></a> |
| Rule depth / rules per layer | 12 (roots are depth 0: 13 levels) / 4096 (ingestion) <a id="cite-ntfe-abi-notes.bound-rule-depth-12-rules-4096"></a> |
| Longest counter window | 86 400 s <a id="cite-ntfe-abi-notes.bound-counter-window-86400s"></a> |
| Sentences per flow | 2 (slot 1 only for loopback flows) <a id="cite-ntfe-abi-notes.bound-sentences-per-flow-2"></a> |
| Flow records batched per copy-out | 32 (kernel-internal) <a id="cite-ntfe-abi-notes.bound-flow-batch-32"></a> |
| Listener records batched per copy-out | 32 (kernel-internal) <a id="cite-ntfe-abi-notes.bound-listener-batch-32"></a> |
