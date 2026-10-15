---
title: "Deletion and Orphans"
description: "Deletion works on two levels because naming and identity are separate — layer deletion, orphaned keys, and what happens to their watches."
type: reference
---

<a id="trm-5-2-9"></a>

Deletion operates on two levels, because naming and identity are
separate things.

<a id="trm-5-2-9-1"></a>

## Deleting a key

`REG_IOC_DELETE_KEY` removes **one layer's path entry**. The key's data
— its GUID, descriptor and values — is untouched; only a name is
removed. <a id="cite-orphan.delete-key.removes-one-layer-path-entry"></a>

LCS derives the parent GUID from the fd's ancestor chain and the child
name from the last component of its resolved path, and sends
`RSI_DELETE_ENTRY`. <a id="cite-orphan.delete-key.parent-and-name-derived-from-the-fd"></a>

If path entries remain in other layers, the key is still visible
through them. <a id="cite-orphan.delete-key.remaining-entries-keep-the-key-visible"></a>

If none remain anywhere, the key is orphaned. <a id="cite-orphan.delete-key.last-entry-removed-orphans-the-key"></a>

A key with **visible children** cannot be deleted:
`ENOTEMPTY`. <a id="cite-orphan.delete-key.visible-children-is-enotempty"></a>

Visibility is evaluated globally, across all enabled layers, and
deliberately ignores the caller's private layer set — so whether a
deletion succeeds does not depend on who is asking. <a id="cite-orphan.delete-key.visibility-ignores-the-callers-private-layers"></a>

Recursive deletion is a client-side tree walk, not a kernel
primitive. <a id="cite-orphan.delete-key.no-recursive-delete-primitive"></a>

Deleting a key does not delete its values. Values belong to the GUID,
not to the path entry, and go when the GUID goes. <a id="cite-orphan.delete-key.values-survive-entry-deletion"></a>

Hive roots cannot be deleted or hidden ([Path Entries](<~kernel/internals/lcs/data-model/path-entries#trm-5-2-5>)).

<a id="trm-5-2-9-2"></a>

## Layer deletion

Deleting a layer removes all of its path entries, value entries and
blanket tombstones, across every source. <a id="cite-orphan.layer-delete.removes-every-entry-across-all-sources"></a>

LCS broadcasts `RSI_DELETE_LAYER` and each source returns the GUIDs
that lost their last path entry as a
result. <a id="cite-orphan.layer-delete.sources-report-newly-orphaned-guids"></a>

Effects on live state follow from the model with no special cases:

- keys named only by that layer become
  orphaned; <a id="cite-orphan.layer-delete.keys-named-only-by-it-become-orphaned"></a>
- where the layer held the winning value entry, the next layer's value
  becomes effective; <a id="cite-orphan.layer-delete.next-layers-value-becomes-effective"></a>
- blanket tombstones it held are removed and unmask what they were
  hiding;
- and Security Descriptors are unchanged, because they were never
  layered. <a id="cite-orphan.layer-delete.security-descriptors-unchanged"></a>

Watchers are notified by whatever recovery mechanism applies —
per-key events for the orphaned keys, and a source-wide `OVERFLOW` for
the rest ([Dispatch](<~kernel/internals/lcs/watches/dispatch#trm-5-6-3>)).

Before sending `RSI_DELETE_LAYER`, LCS aborts every bound transaction
whose mutation log touched that layer. <a id="cite-orphan.layer-delete.aborts-transactions-touching-the-layer"></a> Otherwise a transaction could
commit writes into a layer that no longer exists.

Those transactions return `EINVAL` on their next operation or commit
attempt. <a id="cite-orphan.layer-delete.aborted-transactions-return-einval"></a>

Layer deletion is what role uninstallation and Group Policy removal
are.

<a id="trm-5-2-9-3"></a>

## Orphaned keys

An orphaned key is a GUID with no path entry in any layer. It follows
the Linux unlink model: alive but unnamed. <a id="cite-orphan.definition.guid-with-no-path-entry-anywhere"></a>

Existing fds keep working. Operations that address the key by GUID
proceed normally:

- querying, setting and deleting values; <a id="cite-orphan.allowed.value-operations"></a>
- setting and removing blanket tombstones; <a id="cite-orphan.allowed.blanket-tombstone-operations"></a>
- querying and setting the Security Descriptor; <a id="cite-orphan.allowed.security-descriptor-operations"></a>
- querying key metadata; <a id="cite-orphan.allowed.query-key-metadata"></a>
- flushing the key's hive; <a id="cite-orphan.allowed.flush-the-hive"></a>
- closing the fd. <a id="cite-orphan.allowed.close-the-fd"></a>

Namespace operations return `ENOENT`:

- creating a child key under it; <a id="cite-orphan.refused.create-a-child-key"></a>
- opening or creating anything relative to it; <a id="cite-orphan.refused.relative-open-or-create"></a>
- deleting its path entry; <a id="cite-orphan.refused.delete-its-path-entry"></a>
- hiding it; <a id="cite-orphan.refused.hide-it"></a>
- backing it up. <a id="cite-orphan.refused.back-it-up"></a>

The reason is that an orphaned key is no longer a reachable subtree
root. Allowing new names beneath an unnamed key would build a subgraph
nothing can reach.

<a id="trm-5-2-9-4"></a>

## Watches on an orphaned key

A watch armed before the key was orphaned stays armed, and the
transition delivers `KEY_DELETED`. <a id="cite-orphan.watch.stays-armed-and-delivers-key-deleted"></a>

After that the watch may still observe GUID-local changes made through
the surviving fds, though the subtree is no longer expanded through the
orphaned key. <a id="cite-orphan.watch.still-sees-guid-local-changes"></a>

Arming a *new* watch on an already-orphaned key is
`ENOENT`. <a id="cite-orphan.watch.arming-a-new-watch-is-enoent"></a>

Re-arming one that is already armed is allowed. <a id="cite-orphan.watch.re-arming-an-armed-watch-is-allowed"></a>

<a id="trm-5-2-9-5"></a>

## Dropping the GUID

When the last fd to an orphaned key closes and the source is Active,
LCS sends `RSI_DROP_KEY`, which purges the key record, every value
entry across every layer, and any remaining blanket
tombstones. <a id="cite-orphan.drop.last-close-sends-rsi-drop-key"></a>

It is dispatched **before** the in-kernel key state is
released. <a id="cite-orphan.drop.dispatched-before-state-is-released"></a>

The request is asynchronous: nothing waits for the answer, and a valid
response is processed as an ordinary response rather than as a late
one ([Failure and Late Responses](<~kernel/internals/lcs/sources/failure-and-late-responses#trm-5-8-5>)). <a id="cite-orphan.drop.request-is-asynchronous"></a> That distinction is load-bearing — `RSI_DROP_KEY` is a
mutating operation, and without it the arrival of a perfectly normal
answer to a caller-less request would look like an unaccounted
mutation and tear the source down.

If the source is Down, LCS releases its in-kernel state and does **not**
queue a deferred drop. There is no deferred-drop
queue. <a id="cite-orphan.drop.down-source-queues-no-deferred-drop"></a> Recovering the
key record then falls to the source's own startup obligation, under
the Registry Source Interface specification in PSPK, to purge records
with no path entries before it becomes Active.

`close()` never reports orphan cleanup failure to userspace, and never
can: it returns 0 unconditionally. <a id="cite-orphan.drop.close-always-returns-zero"></a>

<a id="trm-5-2-9-6"></a>

## A new key at the same path

A layer can create a new key where another layer's key already exists.
Each layer has its own path entry pointing at its own GUID, and
resolution decides which is visible.

Fds referencing the other GUID are completely isolated from it:
different identity, different data, different value entries. Nothing
observable connects two keys that merely share a name. <a id="cite-orphan.same-path.fds-to-the-other-guid-stay-isolated"></a>
