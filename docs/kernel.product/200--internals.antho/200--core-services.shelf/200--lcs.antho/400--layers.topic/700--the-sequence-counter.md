---
title: "The Sequence Counter"
description: "The single global monotonic counter stamped on every layer-qualified entry — allocation, initialisation, and what it is not."
type: reference
---

<a id="trm-5-3-7"></a>

LCS keeps one global monotonic counter. Every mutation that creates a
layer-qualified entry — a path entry, a value write, a key hide, a
blanket tombstone — takes the next number from it. <a id="cite-layer.sequence.every-layer-qualified-mutation-takes-the-next-number"></a>

The counter is never decremented and never reset. <a id="cite-layer.sequence.never-decremented-or-reset"></a>

It provides deterministic tiebreaking within a precedence tier
([Resolution](<~kernel/internals/lcs/layers/resolution#trm-5-3-6>)). Wall-clock time is tracked separately, as each key's last
write time, for humans.

<a id="trm-5-3-7-1"></a>

## Allocation

Allocating a number increments the counter. **Allocated numbers are
never reused**, even if the operation later fails, times out, or is
part of a transaction that aborts. <a id="cite-layer.sequence.allocated-numbers-are-never-reused"></a>

Gaps in the sequence space are normal and carry no meaning. <a id="cite-layer.sequence.gaps-are-normal"></a>

A transactional mutation is assigned its number when the operation is
**accepted into the transaction**, not at commit. <a id="cite-layer.sequence.transactional-number-assigned-at-accept-not-commit"></a> That preserves the
order in which the caller performed the operations, which is what layer
tiebreaking and watch ordering need if it commits ([Isolation and the Mutation Log](<~kernel/internals/lcs/transactions/isolation-and-the-mutation-log#trm-5-7-2>)).

<a id="trm-5-3-7-2"></a>

## Initialisation

Each source reports the highest sequence number it has persisted in its
registration handshake, and LCS raises the counter to one above the
maximum reported. <a id="cite-layer.sequence.counter-raised-above-the-reported-source-maximum"></a> New writes therefore always outrank anything
already in storage, even after a restart. <a id="cite-layer.sequence.new-writes-outrank-stored-entries"></a>

A source registering later advances the counter the same way, to
`max(current, source_max + 1)`. <a id="cite-layer.sequence.late-registration-advances-the-counter"></a>

If that addition would overflow 64 bits the registration fails with
`EOVERFLOW` and the source is not made Active — the failure happens
before the slot becomes usable. <a id="cite-layer.sequence.registration-overflow-is-eoverflow"></a>

The counter itself refuses to hand out `U64_MAX`, so the value is never
allocated. <a id="cite-layer.sequence.u64-max-is-never-allocated"></a>

<a id="trm-5-3-7-3"></a>

## What a sequence number is not

A sequence number is not a hive generation number.

A **sequence number** orders layer-qualified entries for resolution and
is persisted by sources.

A **hive generation number** is a volatile, per-hive, kernel-owned
change epoch, exposed by `REG_IOC_QUERY_KEY_INFO` ([Key Ioctls](<~kernel/userspace/native/lcs/key-ioctls#trm-5-5-3>)) so that a
watcher recovering from `OVERFLOW` can tell whether it actually missed
anything. Sources never see it and never persist it. <a id="cite-layer.sequence.generation-number-never-reaches-sources"></a>

Its baseline is initialised from the source's reported maximum sequence
at registration, purely so that observed generations are monotonic
relative to persisted entries; after that the two are unrelated. <a id="cite-layer.sequence.generation-baseline-from-the-reported-source-maximum"></a>

<a id="trm-5-3-7-4"></a>

## Restore

A restore does not write the backup's sequence numbers. It reserves a
fresh range and remaps into it, so restored entries are newer than
everything that was there before while keeping their relative order
from the backup ([Restore](<~kernel/internals/lcs/backup-and-restore/restore#trm-5-9-3>)).
