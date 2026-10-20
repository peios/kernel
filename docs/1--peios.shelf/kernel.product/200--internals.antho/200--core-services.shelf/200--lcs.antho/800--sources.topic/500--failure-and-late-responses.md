---
title: "Failure and Late Responses"
description: "What happens when a source dies, and the late-response problem — a late error, a late successful read, and a late successful write."
type: reference
---

<a id="trm-5-8-5"></a>

<a id="trm-5-8-5-1"></a>

## When a source dies

The connection closes unexpectedly, and:

1. The slot is marked Down and its hives become unavailable. <a id="cite-source.failure.slot-marked-down-hives-unavailable"></a>
2. Every pending request fails `EIO`, including ones queued but not yet
   delivered. <a id="cite-source.failure.pending-requests-fail-eio"></a>
3. **Open key fds stay valid.** An fd holds a GUID and a granted mask,
   and neither depends on the source. Operations needing a round trip
   return `EIO` until the source comes back. <a id="cite-source.failure.key-fds-stay-valid-round-trips-eio"></a>
4. Bound transactions enter `REG_TXN_SOURCE_DOWN`, their poll waiters
   are woken with `POLLERR | POLLHUP`, their mutation logs are
   released, and further use of those fds returns `EIO`. <a id="cite-source.failure.bound-transactions-enter-source-down"></a>
5. **Watches stay armed.** Watch state is kernel-side and does not
   depend on the source at all. <a id="cite-source.failure.watches-stay-armed"></a> Nothing is delivered during the window,
   and `OVERFLOW` arrives on re-registration rather than on disconnect
   ([Dispatch](<~kernel/internals/lcs/watches/dispatch#trm-5-6-3>)).

Coming back is covered in [Registration and Slots](<~kernel/internals/lcs/sources/registration-and-slots#trm-5-8-2>).

<a id="trm-5-8-5-2"></a>

## The late response problem

A caller that times out after its request was dispatched is gone, but
the request is not. The source may still apply the operation and answer
minutes later, and by then there is nobody to return a value to — while
the *kernel* still has work to do, because a mutation that succeeded
has to produce its generation increment and its watch events.

This is the most intricate part of LCS and the part with the most ways
to be subtly wrong.

A late response is validated exactly like an on-time one. <a id="cite-source.late.validated-like-an-on-time-response"></a> The rules
that follow apply **only** to a request whose caller was detached after
its deadline, never to one that never had a caller ([Request Dispatch](<~kernel/internals/lcs/sources/request-dispatch#trm-5-8-3>)).

<a id="trm-5-8-5-2-1"></a>

### A late error <a id="cite-source.late.error-has-no-effects"></a>

The record is released. No watch events, no generation change, nothing.

<a id="trm-5-8-5-2-2"></a>

### A late successful read <a id="cite-source.late.read-is-validated-then-discarded"></a>

Validated, then discarded. There is nobody to give it to and nothing
about it changes kernel state.

<a id="trm-5-8-5-2-3"></a>

### A late successful mutation

The kernel-side effects that correspond to the mutation are applied
from the retained record: the hive generation increment, watch
dispatch, the layer metadata cache refresh, and — for a commit — the
transaction's batch effects and orphan tracking. <a id="cite-source.late.mutation-applies-retained-effects"></a>
The watch dispatch takes the recovery form: a watcher receives an
`OVERFLOW` ahead of the event itself ([Dispatch](<~kernel/internals/lcs/watches/dispatch#trm-5-6-3>)).

Which mutations can actually be replayed is narrower than the set of
operations that count as mutating. A replayable effect is recorded for
`RSI_SET_VALUE` and `RSI_WRITE_KEY`, and only for non-transactional
calls. <a id="cite-source.late.replayable-effects-only-for-set-value-and-write-key"></a>

For the other mutating operations — creating, hiding or deleting a path
entry, creating or dropping a key, deleting a value entry, setting a
blanket tombstone, deleting a layer — no effect was retained, so a late
success is a mutation the kernel cannot account for. LCS tears the
source down and returns `EIO` rather than silently ignoring it. <a id="cite-source.late.unreplayable-mutation-tears-source-down"></a>

That is the conservative direction, and deliberately so: the
alternative is a committed change with no watch event and a stale
generation number, which nothing downstream could detect.

<a id="trm-5-8-5-2-4"></a>

### A late successful transaction operation

A late `RSI_BEGIN_TRANSACTION` has created transaction state in the
source that nobody will ever use, so LCS enqueues an
`RSI_ABORT_TRANSACTION` for that id. <a id="cite-source.late.begin-transaction-enqueues-an-abort"></a>

A late `RSI_ABORT_TRANSACTION` or `RSI_FLUSH` releases the record with
no effects. <a id="cite-source.late.abort-or-flush-releases-the-record"></a>

A late `RSI_COMMIT_TRANSACTION` is a mutating response and applies the
retained commit effects — the same generation update and the same watch
events an on-time commit would have produced. <a id="cite-source.late.commit-applies-retained-commit-effects"></a> Watchers may therefore
observe the effects of a transaction whose caller was told it timed
out ([Commit and Failure](<~kernel/internals/lcs/transactions/commit-and-failure#trm-5-7-3>)).

<a id="trm-5-8-5-2-5"></a>

### A malformed late response

The ordinary malformed-data and malformed-protocol rules apply. But if
LCS cannot safely process the kernel-side effects of a
possibly-applied mutation because the request metadata it needs is
missing or invalid, it tears the source down and marks it Down rather
than ignoring the response. <a id="cite-source.late.unprocessable-effects-tear-source-down"></a>

A malformed late commit response takes the source down for the same
reason. <a id="cite-source.late.malformed-commit-tears-source-down"></a>

<a id="trm-5-8-5-3"></a>

## What a caller should conclude

`ETIMEDOUT` means *may or may not have completed*. A caller that needs
certainty reads state back before retrying. That applies to every
operation and, especially, to a transaction commit.

<a id="trm-5-8-5-4"></a>

## Fd lifecycle

Key fds and transaction fds are ordinary file descriptors, subject to
`RLIMIT_NOFILE`. There is no registry-specific fd accounting and no
registry-specific leak protection. <a id="cite-source.failure.no-registry-specific-fd-accounting"></a>

Process exit closes them through normal kernel cleanup: key fds
released and their watches removed, transactions aborted. <a id="cite-source.failure.process-exit-releases-fds"></a>

<a id="trm-5-8-5-5"></a>

## Memory

Registry kernel memory needs no global cap, because everything is
bounded by limits that already exist.

- **Watch queues:** `NotificationQueueSize` per queue, times
  `RLIMIT_NOFILE` queues per process.
- **Open key state:** per-fd overhead — GUID, granted mask, ancestor
  chain, watch state — times the same fd limit.
- **Layer table:** bounded by `MaxTotalLayers`, and per-value
  resolution cost by `MaxLayersPerValue`.
- **In-flight requests:** bounded per source by
  `MaxConcurrentRSIRequests`, and separately by the number of threads
  blocked on registry syscalls.
