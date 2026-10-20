---
title: "Backup"
description: "Writing a subtree to a stream under SeBackupPrivilege with no per-key access check — the snapshot, the audit, and what is written."
type: reference
---

<a id="trm-5-9-2"></a>

`REG_IOC_BACKUP` exports the key on the fd and its entire subtree to
another fd, preserving parent/child relationships even when traversal
must grow its internal storage. <a id="cite-backup.exports-the-key-and-its-subtree"></a>

It requires `SeBackupPrivilege` and performs **no per-key AccessCheck**
whatsoever. <a id="cite-backup.requires-sebackupprivilege-and-checks-no-key"></a> The privilege is the whole authorisation, which is
why the operation is audited unconditionally ([Audit](<~kernel/internals/lcs/security/audit#trm-5-4-4>)).

The output fd must be writable, or `EBADF`. <a id="cite-backup.output-fd-must-be-writable"></a>

<a id="trm-5-9-2-1"></a>

## The snapshot

Before reading anything, LCS opens a **read-only** source transaction —
`RSI_BEGIN_TRANSACTION` with mode `RSI_TXN_READ_ONLY` — so that the
whole export is a point-in-time snapshot. Concurrent mutations do not
appear part-way through the stream. <a id="cite-backup.opens-a-read-only-snapshot-transaction"></a>

That transaction is **released with `RSI_ABORT_TRANSACTION` and never
committed**. There is no commit call anywhere in the backup path; a
read-only transaction has nothing to commit. <a id="cite-backup.snapshot-released-with-abort-never-committed"></a>

A source that does not support read-only snapshots answers
`RSI_TXN_NOT_SUPPORTED` and the backup fails `ENOTSUP`. <a id="cite-backup.unsupported-snapshot-is-enotsup"></a>

A source already holding `MaxReadOnlyTransactionsPerSource` snapshots
(default 16) yields `EBUSY` — which bounds snapshot-holding without
treating backups as write-lock holders, since they are not. <a id="cite-backup.snapshot-limit-is-ebusy"></a>

Backing up an orphaned key is `ENOENT`: it is no longer a reachable
subtree root ([Deletion and Orphans](<~kernel/internals/lcs/data-model/deletion-and-orphans#trm-5-2-9>)). <a id="cite-backup.orphaned-key-is-enoent"></a>

<a id="trm-5-9-2-2"></a>

## Audit

`lcs.audit.backup.started` is emitted **before any subtree data is read**, and
if it cannot be emitted the backup returns `EIO` and does not start. <a id="cite-backup.start-event-precedes-any-data-or-eio"></a>

After privilege, output-fd and key validation, START precedes the request for
the read-only snapshot. A refused or failed snapshot therefore emits both
START and END, with END carrying the failure errno; no subtree is exported
and no unopened snapshot is released. A START emission failure prevents the
snapshot request itself. <a id="cite-backup.snapshot-refusal-is-audited"></a>

`lcs.audit.backup.ended` is emitted afterwards, carrying the result, and a
failure to emit it cannot change a result that has already happened. <a id="cite-backup.complete-event-cannot-change-the-result"></a>

<a id="trm-5-9-2-3"></a>

## What is written

The stream is a header, the layer manifest, then each key in
depth-first pre-order with its path entries, values and blanket
tombstones, then the trailer. The exact shapes are in the PSPK chapter.

Two things about the exporter are worth stating here, because they
constrain a reader more tightly than the format does.

The exporter writes **no GUID-bearing path entries for the backup
root**. The root's section contains only its hidden entries. <a id="cite-backup.root-section-has-no-guid-path-entries"></a>

A reader tolerates and skips them if some other writer produces them,
but this one does not emit them, because on restore the target key's
existing name is authoritative and they would be discarded anyway. <a id="cite-backup.reader-skips-root-path-entries"></a>

Hidden entries belong to the **parent's** section, not to a section of
their own — a hidden entry has no key to have a section for. <a id="cite-backup.hidden-entries-live-in-the-parent-section"></a>

A hidden entry masking a name where no key exists in any layer is still
valid; it expresses "this layer hides this name" whether or not
anything is there to hide. <a id="cite-backup.hidden-entry-without-a-key-is-valid"></a>

The layer manifest is written from the live layer table, and it is a
manifest: it records what the layers looked like at backup time so that
a restore can validate the stream against them. It is not a backup of
the layer definitions. <a id="cite-backup.manifest-is-written-from-the-live-layer-table"></a>

A layer definition is backed up only when
`Machine\System\Registry\Layers\<Name>\` is itself inside the subtree
being exported, in which case it is ordinary key and value data like
anything else. <a id="cite-backup.layer-definition-backed-up-only-if-inside-the-subtree"></a>

This includes definitions for unused layers in a whole-hive export.
Their metadata remains ordinary registry data; an unused definition
does not by itself require an entry in the layer manifest.
