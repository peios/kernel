---
title: "Dispatch"
description: "Given a mutation, which armed watches hear about it — computed from object identity and ancestry, with depth, batching and recovery."
type: reference
---

<a id="trm-5-6-3"></a>

Dispatch answers one question: given a mutation on a key, which armed
watches hear about it? The answer is computed from object identity and
from ancestry captured at open time, never from a path string resolved
at the moment of the event. <a id="cite-watch.dispatch.computed-from-identity-and-captured-ancestry"></a>

<a id="trm-5-6-3-1"></a>

## A watch is bound to an object

A watch is registered against the GUID on the fd it was armed through.
It fires for changes to *that object*. <a id="cite-watch.dispatch.registered-against-the-fd-guid"></a>

If a layer change causes a different key to become visible at the same
path, the watch does not move: the new key is a different object with a
different GUID, and nothing about the old watch refers to a name. <a id="cite-watch.dispatch.watch-does-not-follow-the-path"></a>

To follow the path rather than the object, a process detects the change
— through `KEY_DELETED` on the old object, or a subtree watch on the
parent — re-opens the path, and arms a new watch. This is the fd model
applied consistently: an fd is a capability bound to one identity.

The converse also holds. If a watched key is hidden, `KEY_DELETED` is
delivered, but the watch is not removed. <a id="cite-watch.dispatch.hiding-keeps-the-watch-armed"></a>

Should the hiding layer later be deleted, the key reappears at its
original path with the same GUID, and events resume. <a id="cite-watch.dispatch.events-resume-when-the-key-reappears"></a>
There is no re-emergence event; the watcher simply observes the key
being active again. <a id="cite-watch.dispatch.no-re-emergence-event"></a>

<a id="trm-5-6-3-2"></a>

## The ancestor chain

Subtree dispatch needs to know where a key sits in the tree, and it
learns that once, at open.

Resolving a path walks it component by component, and the GUID at each
level is retained on the resulting fd as the **ancestor chain** —
root GUID through parent GUID to the key itself. <a id="cite-watch.dispatch.ancestor-chain-captured-at-open"></a>
It costs nothing extra: the walk had to resolve those components
anyway.

A relative open copies the parent fd's chain and extends it with the
components the relative walk resolved. <a id="cite-watch.dispatch.relative-open-extends-the-parent-chain"></a>

An open that followed a symlink records the chain of the *resolved*
path, so the fd's ancestry reflects the target's real position in the
tree, not the link's. <a id="cite-watch.dispatch.symlink-open-records-the-resolved-chain"></a>

Dispatch uses that captured chain and never re-resolves it. If an
ancestor in the chain is later hidden, deleted, orphaned, or replaced
at the same path by a different key, watches on the original ancestor
GUID still receive subtree events from descendants mutated through fds
opened through that chain. <a id="cite-watch.dispatch.stale-ancestor-still-receives-subtree-events"></a>

Watches on a new key that later appears at the same path receive
nothing from the old one. <a id="cite-watch.dispatch.new-key-at-the-same-path-receives-nothing"></a>

<a id="trm-5-6-3-3"></a>

## The algorithm

Two structures back dispatch. The **watch map** is a hash map from GUID
to the watchers armed on it. The **subtree watch set** is a refcounted
hash set of the GUIDs that have at least one subtree watch, maintained
as watches are armed, re-armed, disarmed and closed.

For a mutation on key *B*, with *B*'s ancestor chain in hand:

1. Look up *B*'s GUID in the watch map and queue the event, with
   `path_depth` 0, to every watcher whose filter admits it. <a id="cite-watch.dispatch.direct-watchers-receive-depth-zero"></a>
2. Walk the ancestor chain outward from *B*'s parent. At each ancestor,
   skip it unless it is in the subtree watch set — that test is what
   makes the walk cheap. For an ancestor that is, queue the event to
   each of its watchers that armed with the subtree flag and whose
   filter admits it, with the path from that ancestor down to *B*. <a id="cite-watch.dispatch.subtree-watchers-receive-the-relative-path"></a>

The cost is O(depth) hash lookups, with no RSI round trips, no trie and
no string comparison. <a id="cite-watch.dispatch.costs-o-depth-hash-lookups-and-no-source-io"></a>
The path components handed to a subtree watcher are sliced out of the
resolved path already stored on the mutating fd.

Dispatch runs under a single global registry lock, so it is serialised
across the whole system rather than per hive or per source.

<a id="trm-5-6-3-4"></a>

## Depth

`MaxSubtreeWatchDepth` bounds how far below a watched key a subtree
watch is told about. The default is 0, meaning unlimited. <a id="cite-watch.dispatch.depth-zero-means-unlimited"></a>

A non-zero value suppresses events whose path is longer than it,
limiting both noise and dispatch cost for a watch armed high in a
tree. <a id="cite-watch.dispatch.depth-limit-suppresses-deeper-events"></a>

The limit applies to watches held by userspace. LCS's own internal
watches are collected before the depth test and are not subject to it
([The Self-Watch](<~kernel/internals/lcs/bootstrap/the-self-watch#trm-5-10-4>)).

<a id="trm-5-6-3-5"></a>

## Transaction batches

Nothing inside an uncommitted transaction dispatches. <a id="cite-watch.dispatch.uncommitted-transaction-dispatches-nothing"></a>

At commit, and only when the source reports success, the transaction's
mutation log is walked in operation order and the whole set of events
is queued as one batch, under a single hold of the registry lock, so no
other operation interleaves with it. <a id="cite-watch.dispatch.commit-batch-queued-in-operation-order-without-interleaving"></a>

An aborted or failed transaction dispatches nothing and its log is
released. A transaction that timed out after its commit was dispatched
keeps its log, and a late `RSI_OK` still emits the batch ([Commit and Failure](<~kernel/internals/lcs/transactions/commit-and-failure#trm-5-7-3>)).

A large transaction — a role installation writing thousands of values —
could otherwise fill a watcher's queue atomically. So the batch is
counted per watcher first: any watcher whose share exceeds
`MaxTransactionWatchEventBurst`, default 4096, receives exactly one
`OVERFLOW` and none of its individual events. <a id="cite-watch.dispatch.burst-cap-replaces-a-watchers-batch-with-one-overflow"></a>

That `OVERFLOW` is queued ahead of the batch, so it arrives before
whatever else that watcher is still owed. <a id="cite-watch.dispatch.burst-overflow-queued-ahead-of-the-batch"></a>

<a id="trm-5-6-3-6"></a>

## Recovery dispatch

Some changes alter effective state for keys whose fds nobody holds and
whose descendants the kernel is retaining no context for. Deleting a
layer, changing its precedence, enabling or disabling it, and restoring
a subtree from a stream are all of this kind. <a id="cite-watch.dispatch.recovery-triggering-operations"></a>
Computing an exact diff would mean walking arbitrary parts of the tree
through the source.

LCS does not attempt it. It increments the generation number of every
hive the affected source backs and then queues a no-name `OVERFLOW` to
every armed watch on that source, which is the notification for those
changes. <a id="cite-watch.dispatch.recovery-bumps-generation-and-queues-overflow"></a>
The watcher re-reads, and can compare the generation number it last saw
against the current one ([Key Ioctls](<~kernel/userspace/native/lcs/key-ioctls#trm-5-5-3>)) to tell whether an *ordinary* write
happened in between; after a recovery it cannot, because the bump is
deliberately conservative. The kernel does not know which hives a layer
operation touched — the source's delete-layer answer names only the
keys it orphaned, and a layer holding hiding or masked entries changes
effective state without orphaning anything — so it bumps every hive
rather than risk a watcher skipping a re-read its hive needed. The
consequence is always a spurious re-read, never a missed change.
<a id="cite-watch.dispatch.recovery-generation-bump-is-source-wide"></a>

Two properties of this delivery are worth stating. It is object-
semantic like every other dispatch — it walks the watch map, resolves
no paths — and it bypasses the filter, because `OVERFLOW` always does.
It does not disarm anything. <a id="cite-watch.dispatch.recovery-does-not-disarm"></a>

The scope is the **source**, not the hive. A source backing several
hives delivers `OVERFLOW` to watches on all of them, including hives
the operation did not touch, and bumps all of their generation
counters. <a id="cite-watch.dispatch.recovery-scope-is-the-source-not-the-hive"></a>
The generation counters are maintained per hive for ordinary writes;
recovery treats the source as the unit.

For a restore, recovery is published only after the source commit
succeeds. A restore that fails or aborts before commit emits nothing. <a id="cite-watch.dispatch.restore-recovery-published-only-after-commit"></a>

<a id="trm-5-6-3-7"></a>

## Source restart

When a source disconnects, watches stay armed and nothing is delivered;
operations needing the source return `EIO`. <a id="cite-watch.dispatch.disconnect-keeps-watches-armed-and-silent"></a>

`OVERFLOW` arrives on **re-registration**, not on disconnect, which is
the only ordering that works: a watcher told to re-read needs the
source to be there when it does. <a id="cite-watch.dispatch.overflow-arrives-on-re-registration"></a>

Existing fds resume without re-opening, and no watcher has to
re-arm. <a id="cite-watch.dispatch.fds-resume-without-re-arming"></a>
