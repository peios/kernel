---
title: "ABI semantics and limits"
description: "ABI semantics and limits: behaviour and implementation of the Peios kernel."
type: reference
---

<a id="trm-2-b"></a>

[KMES ABI Reference](<~kernel/userspace/native/kmes/generated-abi-tables#trm-2-a>) is generated from `include/uapi/pkm/kmes.h` and holds only what a
compiler can measure. This appendix holds the rest.

The split is structural rather than editorial. `gen-kmes-abi.py`
overwrites [KMES ABI Reference](<~kernel/userspace/native/kmes/generated-abi-tables#trm-2-a>) wholesale on every run, so anything written there is
lost the next time the ABI changes.

Layouts that form part of the consumer contract — the event header,
the producer and consumer metadata pages, and the mapped region — are
specified normatively in the PSPK event stream specification. [KMES ABI Reference](<~kernel/userspace/native/kmes/generated-abi-tables#trm-2-a>)
gives their offsets as the header defines them; the specification
governs.

<a id="trm-2-b-1"></a>

## Syscall parameters

| Syscall | Parameter | Type | Meaning |
|---|---|---|---|
| `kmes_emit` | `event_type` | `const char *` | Event type string. |
| | `event_type_len` | `u16` | Its length in bytes. |
| | `payload` | `const void *` | MessagePack payload. |
| | `payload_len` | `u32` | Its length in bytes. |
| `kmes_emit_batch` | `entries` | `struct kmes_emit_entry *` | Array of event descriptors. |
| | `count` | `u32` | Number of entries, 1 to `KMES_BATCH_MAX_ENTRIES`. |
| | `emitted_out` | `u32 *` | Receives the number of events emitted. |
| `kmes_attach` | `cpu_id` | `unsigned int` | Ring slot index, or `KMES_ATTACH_QUERY_SLOTS` to query the slot count. |
| | `capacity` | `u64 *` | Receives the ring buffer capacity in bytes. |

`kmes_emit` and `kmes_emit_batch` return 0 on success; `kmes_attach`
returns a file descriptor. All three return -1 and set errno on
failure.

The PKM syscall range is 1090–1099; KMES uses the first three.

<a id="trm-2-b-2"></a>

## Privilege requirements <a id="cite-syscalls.privileges-by-name"></a>

`kmes.h` gives these as bit masks so it can stand alone. The names
belong to the KACS privilege catalogue, and the bit index is what the
two agree on.

| Operation | Required privilege | Bit |
|---|---|---|
| `kmes_emit`, `kmes_emit_batch` | SeAuditPrivilege | 21 |
| Rate-limit exemption on both | SeTcbPrivilege | 7 |
| `kmes_attach` | SeSecurityPrivilege | 8 |

Holding a privilege is not enough: it must be *enabled*, and KMES marks
it used before proceeding. A failure to record the used state is itself
an `EPERM`, because an unrecorded privilege use is an audit gap. <a id="cite-syscalls.privilege-enabled-and-recorded"></a>

SeTcbPrivilege is checked but not required — an emitter that holds it
enabled is exempt from the per-process rate limit, and one that does not
is throttled.

<a id="trm-2-b-3"></a>

## Implementation bounds

These are properties of the implementation rather than of the ABI, so
they are not in `kmes.h` and a program must not compile against them.
They bound what the interface will accept.

| Quantity | Value | Where |
|---|---|---|
| Maximum event size, structural | 50% of ring capacity | `security/pkm/kmes/kmes.c` |
| MessagePack validator nesting stack | 256 | `security/pkm/kmes/kmes_validate.rs` |
| Self-configuration payload buffer | 768 bytes | `security/pkm/kmes/kmes.c` |
| Self-configuration audit intents per read | 4 | `security/pkm/kmes/kmes.h` |
| Self-configuration parameter name | 64 bytes | `security/pkm/kmes/kmes.h` |

The structural 50% bound is independent of `MaxEventSize` and applies to
kernel emitters too. An event may satisfy the configured maximum and
still be refused because the ring is small.

The validator's 256-frame stack is why `MaxNestingDepth` has a maximum of
256. The two bounds are enforced independently: the configuration range
check refuses a larger value at apply time, and the validator refuses
every event outright if it is somehow handed one, rather than silently
accepting nesting it cannot track.

<a id="trm-2-b-5"></a>

## Error codes

<a id="trm-2-b-5-1"></a>

### `kmes_emit` <a id="cite-emit.errors"></a>

| Errno | Condition |
|---|---|
| `EPERM` | SeAuditPrivilege not held or not enabled, or recording its used state failed. |
| `EAGAIN` | Per-process rate limit exceeded. |
| `EINVAL` | Zero event type length, event type not valid UTF-8, declared size arithmetic overflowed, payload not valid msgpack, or nesting depth over `MaxNestingDepth`. |
| `EFAULT` | Event type or payload pointer inaccessible. |
| `ENOSPC` | Event exceeds `MaxEventSize` or 50% of ring capacity. |
| `ENOMEM` | Staging buffer allocation failed, or KMES not initialised. |

<a id="trm-2-b-5-2"></a>

### `kmes_emit_batch` <a id="cite-batch.errors"></a>

| Errno | Condition |
|---|---|
| `EPERM` | As `kmes_emit`. |
| `EAGAIN` | Fewer than `count` tokens available. |
| `EINVAL` | `count` is 0 or over `KMES_BATCH_MAX_ENTRIES`, or the failing entry hit one of `kmes_emit`'s `EINVAL` conditions. |
| `EFAULT` | `emitted_out`, the entry array, or the failing entry's type or payload pointer inaccessible. |
| `ENOSPC` | The failing entry exceeds `MaxEventSize` or 50% of ring capacity. |
| `ENOMEM` | Kernel allocation failed, or KMES not initialised. |

<a id="trm-2-b-5-3"></a>

### `kmes_attach` <a id="cite-attach.errors"></a>

| Errno | Condition |
|---|---|
| `EPERM` | SeSecurityPrivilege not held or not enabled, or recording its used state failed. |
| `EINVAL` | `cpu_id` at or beyond the ring array size, or its slot holds no live ring. |
| `EFAULT` | `capacity` pointer inaccessible. |
| `ENOMEM` | Kernel allocation failed, or KMES not initialised. |

A `KMES_ATTACH_QUERY_SLOTS` call takes the same `EPERM`, `EFAULT` and
`ENOMEM` conditions and cannot return `EINVAL`. <a id="cite-attach.query-slots-errors"></a>

The ring array is sized by `nr_cpu_ids`, not by the number of rings
allocated. On a machine with a sparse possible-CPU mask the two differ,
and a slot inside the array with no live ring returns `EINVAL` exactly
as an index beyond the array does. A consumer therefore enumerates
against the slot count from `KMES_ATTACH_QUERY_SLOTS` and skips the
`EINVAL` slots rather than stopping at the first one; see [Syscall Interface](<~kernel/userspace/native/kmes/emission-and-attachment-syscalls#trm-2-4>).
