---
title: "Operational Parameters"
description: "The nineteen parameters LCS reads from the registry, how they are validated, and what hot-swapping one does to in-flight operations."
type: reference
---

<a id="trm-5-10-3"></a>

LCS reads nineteen parameters from `Machine\System\Registry\`. <a id="cite-param.nineteen-under-registry-key"></a>

All are `REG_DWORD`. <a id="cite-param.all-are-reg-dword"></a> Each has a compiled-in default and a valid
range, and LCS runs on the defaults until the registry says otherwise.

| Value | Default | Range | Bounds |
|---|---:|---|---|
| `RequestTimeoutMs` | 30000 | 1000–600000 | A source round trip ([Request Dispatch](<~kernel/internals/lcs/sources/request-dispatch#trm-5-8-3>)). <a id="cite-param.request-timeout-ms"></a> |
| `TransactionTimeoutMs` | 30000 | 1000–600000 | The lifetime of an open transaction ([Scope and Lifetime](<~kernel/internals/lcs/transactions/scope-and-lifetime#trm-5-7-1>)). <a id="cite-param.transaction-timeout-ms"></a> |
| `NotificationQueueSize` | 256 | 16–65536 | Queued events per watcher before overflow ([Queues and Overflow](<~kernel/internals/lcs/watches/queues-and-overflow#trm-5-6-4>)). <a id="cite-param.notification-queue-size"></a> |
| `SymlinkDepthLimit` | 16 | 1–64 | Symlink resolution depth ([Symlinks](<~kernel/internals/lcs/data-model/symlinks#trm-5-2-4>)). <a id="cite-param.symlink-depth-limit"></a> |
| `MaxValueSize` | 1048576 | 4096–67108864 | One value's data, in bytes. <a id="cite-param.max-value-size"></a> |
| `MaxKeyDepth` | 512 | 32–4096 | Key hierarchy nesting. <a id="cite-param.max-key-depth"></a> |
| `MaxPathComponentLength` | 255 | 64–1024 | One key, value or layer name, in UTF-8 bytes. <a id="cite-param.max-path-component-length"></a> |
| `MaxTotalPathLength` | 16383 | 1024–65535 | A whole path, in UTF-8 bytes. <a id="cite-param.max-total-path-length"></a> |
| `MaxLayersPerValue` | 128 | 1–1024 | Layers writing to one `(key, value name)` ([The Layer Model](<~kernel/internals/lcs/layers/the-layer-model#trm-5-3-1>)). <a id="cite-param.max-layers-per-value"></a> |
| `MaxBoundTransactionsPerSource` | 16 | 1–256 | Concurrently bound transactions per source ([Scope and Lifetime](<~kernel/internals/lcs/transactions/scope-and-lifetime#trm-5-7-1>)). <a id="cite-param.max-bound-transactions-per-source"></a> |
| `MaxReadOnlyTransactionsPerSource` | 16 | 1–256 | Concurrent backup snapshots per source ([Backup](<~kernel/internals/lcs/backup-and-restore/backup#trm-5-9-2>)). <a id="cite-param.max-read-only-transactions-per-source"></a> |
| `MaxTotalLayers` | 1024 | 16–65536 | Distinct layers in the in-memory table ([The Layer Model](<~kernel/internals/lcs/layers/the-layer-model#trm-5-3-1>)). <a id="cite-param.max-total-layers"></a> |
| `MaxRegisteredSources` | 32 | 1–256 | Concurrently registered sources. <a id="cite-param.max-registered-sources"></a> |
| `MaxHivesPerSource` | 64 | 1–1024 | Hives one source may register. <a id="cite-param.max-hives-per-source"></a> |
| `MaxConcurrentRSIRequests` | 256 | 8–4096 | In-flight RSI requests per source ([Request Dispatch](<~kernel/internals/lcs/sources/request-dispatch#trm-5-8-3>)). <a id="cite-param.max-concurrent-rsi-requests"></a> |
| `MaxScopeGUIDsPerToken` | 8 | 1–256 | Private hive scope GUIDs on a token ([Private Hives](<~kernel/internals/lcs/data-model/private-hives#trm-5-2-2>)). <a id="cite-param.max-scope-guids-per-token"></a> |
| `MaxPrivateLayersPerToken` | 16 | 1–256 | Private layer names on a token ([Private Layers](<~kernel/internals/lcs/layers/private-layers#trm-5-3-5>)). <a id="cite-param.max-private-layers-per-token"></a> |
| `MaxSubtreeWatchDepth` | 0 | 0–4096 | Subtree watch depth; 0 is unlimited ([Dispatch](<~kernel/internals/lcs/watches/dispatch#trm-5-6-3>)). <a id="cite-param.max-subtree-watch-depth"></a> |
| `MaxTransactionWatchEventBurst` | 4096 | 256–65536 | Watch events per watcher from one commit ([Dispatch](<~kernel/internals/lcs/watches/dispatch#trm-5-6-3>)). <a id="cite-param.max-transaction-watch-event-burst"></a> |

Unknown values under this key are ignored. <a id="cite-param.unknown-values-ignored"></a> There are exactly
nineteen parameters and no undocumented ones; a separate set under
`Machine\System\KMES\` belongs to KMES.

Two limits are not among them. The **transaction mutation log** is
capped at 4096 entries by a compile-time constant ([Isolation and the Mutation Log](<~kernel/internals/lcs/transactions/isolation-and-the-mutation-log#trm-5-7-2>)), and hard
ceilings on total path length and key depth exist independently of
configuration — set equal to the range maxima above, so they never
conflict. <a id="cite-param.hard-ceilings-match-range-maxima"></a>

<a id="trm-5-10-3-1"></a>

## Where a configured value does not fully bind

One of the nineteen does not do everything its range suggests.

`MaxPrivateLayersPerToken` is described as an attachment-time limit but
is not enforced at attachment. KACS applies its own hard cap of 256 and
LCS applies the configured value later, at use, with `E2BIG` ([Private Layers](<~kernel/internals/lcs/layers/private-layers#trm-5-3-5>)).
`MaxScopeGUIDsPerToken` behaves the same way.

<a id="trm-5-10-3-2"></a>

## Validation

A value is checked against its range when it is read.

- **Valid** — hot-swapped into the in-memory configuration and used by
  new operations. <a id="cite-param.validation.valid-is-hot-swapped"></a>
- **Invalid** — out of range, the wrong type, or missing — the value is
  **ignored** and the previously active one is kept: the compiled-in
  default or the last known-good. <a id="cite-param.validation.invalid-is-ignored-previous-kept"></a>
  An `lcs.config.value.rejected` audit event is emitted naming the
  parameter, what was wrong, and the value being retained ([Audit](<~kernel/internals/lcs/security/audit#trm-5-4-4>)).

**Values are never clamped or silently corrected.** <a id="cite-param.validation.never-clamped"></a> There is no
`min`/`max` on any configuration path. A write to the registry
succeeds, because the source does not enforce kernel semantics, and LCS
simply refuses to use it. The registry shows what was written; the
audit log shows what LCS is running on.

Because "missing" is invalid, a first boot before seed restore emits
nineteen of these events per refresh — provided `Machine\System\Registry`
itself exists. If the key is absent there is nothing to read and
nothing is reported; the fallback watch of [The Self-Watch](<~kernel/internals/lcs/bootstrap/the-self-watch#trm-5-10-4>) waits for it.

<a id="trm-5-10-3-3"></a>

## Hot-swap and in-flight operations

Configuration is published as a whole structure under a seqlock, and a
reader takes a complete copy of it. <a id="cite-param.hot-swap.published-as-one-structure"></a>

A syscall entry point snapshots it once and threads that snapshot
through the operation, so in-flight work uses the values that were
current when it started and new work uses the updated ones. <a id="cite-param.hot-swap.syscall-snapshots-once"></a>

That is the rule, and mostly the practice. Some deeper paths take a
second snapshot part-way through, and a few call sites read a single
live value rather than a snapshot — `reg_begin_transaction`'s timeout,
the bound-transaction cap, and the in-flight request cap among them.
For those, a hot-swap can be observed mid-operation. <a id="cite-param.hot-swap.some-call-sites-read-live-values"></a>

<a id="trm-5-10-3-4"></a>

## Security

`Machine\System\Registry\` inherits the `Machine` hive root descriptor
— SYSTEM and Administrators with `KEY_ALL_ACCESS`, Authenticated Users
with `KEY_READ` — so an unprivileged process cannot change any of
this. <a id="cite-param.security.unprivileged-cannot-change"></a>

Domain policy at a higher-precedence layer defends against a
compromised local administrator, which is the reason `SeTcbPrivilege`
guards precedence above 0 ([Writing Into a Layer](<~kernel/internals/lcs/layers/writing-into-a-layer#trm-5-3-4>)).

## Operator verification

Inspect the stored configuration and installed manual before tuning LCS:

```sh
reg get Machine/System/Registry
regman 'Machine\System\Registry'
```

Keep a recovery value. A successful write confirms storage, not adoption;
inspect `lcs.config.value.rejected` events as well. Deleting a parameter does
not reset an already accepted running value. Write the intended valid value
and verify it at the documented application point.

An unavailable hive is a source problem, distinct from an absent parameter.
For loregd, inspect the output captured by Peinit before readiness and the
stored service logs after logging starts. Missing configuration alone is not
evidence that a database needs replacement or reseeding.
