---
title: "The Stream"
description: "The streamable binary representation of a key and everything beneath it with full layer fidelity — what the design buys, and how it is versioned."
type: reference
---

<a id="trm-5-9-1"></a>

The registry backup format is a streamable binary representation of a
key and everything beneath it, with full layer fidelity. It is used by
`REG_IOC_BACKUP` and `REG_IOC_RESTORE`, by first-boot seeding, by
disaster recovery and by offline migration.

It is an **LCS-level** format. Sources never see it: LCS serialises
from source data on the way out and deserialises into RSI operations on
the way in. <a id="cite-backup.stream.lcs-level-sources-never-see-it"></a>

Because a third party writes and reads these streams directly — that is
what migration and recovery mean — the format is a normative
specification rather than a description. It is a chapter of PSPK, and
every byte layout, record type, ordering rule and validation
requirement lives there. This section covers what LCS does with it.

<a id="trm-5-9-1-1"></a>

## What the design buys

**Streamable.** It is written to an arbitrary fd — a file, a pipe, a
socket — with no seeking, in a single pass, and read back the same way. <a id="cite-backup.stream.written-and-read-without-seeking"></a>

**Full layer fidelity.** Every path entry, value, tombstone and blanket
tombstone is stored with its layer tag, so restoring reconstructs the
layered state rather than a flattened snapshot of it. <a id="cite-backup.stream.entries-carry-their-layer-tag"></a>

**Depth-first pre-order.** A parent always appears before its children,
so a restore can create keys top-down without buffering a tree. <a id="cite-backup.stream.depth-first-pre-order"></a>

**Descriptors inline.** Each key record carries its own descriptor with
no deduplication. <a id="cite-backup.stream.descriptors-inline-without-dedup"></a> Redundancy is external compression's problem; piping
through zstd handles it.

**Self-verifying.** A trailer carries a record count and a SHA-256 over
everything before it, so truncation and corruption are detected. <a id="cite-backup.stream.trailer-carries-count-and-sha256"></a>

<a id="trm-5-9-1-2"></a>

## Versioning

The header carries a format version and a **minimum reader version**. A
writer that used only older features sets a lower minimum, letting
older readers restore the stream. <a id="cite-backup.stream.header-carries-version-and-minimum-reader"></a>

A reader that finds a minimum above its own supported version rejects
the stream outright, before touching anything. <a id="cite-backup.stream.rejects-minimum-above-supported-version"></a>

Both are 21 in the current implementation, and the reader supports 21. <a id="cite-backup.stream.current-version-is-21"></a>

Unknown record types are skipped when the minimum reader version allows
it, and they still count toward the record count and the checksum. <a id="cite-backup.stream.unknown-records-skipped-but-counted"></a> A
writer that adds a record type a restore genuinely needs must raise the
minimum reader version, so that an older reader refuses the stream
rather than restoring an incomplete one.

Extension is by new **record types** only. Existing record payloads
must be consumed exactly; trailing bytes inside a known record are an
error. <a id="cite-backup.stream.trailing-bytes-in-a-record-are-an-error"></a> This is the opposite of the RSI's request convention ([Validation](<~kernel/internals/lcs/sources/validation#trm-5-8-4>)),
and the difference is deliberate: a stream is replayed into mutations
long after it was written, and a field silently ignored there is data
silently lost.
