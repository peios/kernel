---
title: "Model and revalidation"
description: "Strata change underneath stratafs without telling it — what can change a resolution, and the guarantee that survives it."
type: reference
---

<a id="trm-4-4-1"></a>

Every stratum of a mount may be modified at any time by an agent that
does not know stratafs exists. stratafs observes such changes without
being told of them.

<a id="trm-4-4-1-1"></a>

## No coordination <a id="cite-coherency.no-notification-protocol"></a>

There is no notification machinery anywhere in the filesystem — no
`fsnotify` registration, no `inotify`, nothing a stratum's filesystem
is expected to report. No writer announces a change, quiesces, or
participates in any protocol. Every resolution is performed from
scratch by re-walking the stratum path string, so nothing has to be
told anything.

<a id="trm-4-4-1-2"></a>

## What can change a resolution <a id="cite-coherency.resolution-depends-on-names-not-contents"></a>

A resolution depends only on which names each participating stratum
directory holds and what type each entry has. It does not depend on the
contents of any file.

A change to an object's **contents** therefore requires no action at
all. stratafs inodes carry no address-space operations; there is no
second page cache, and every data operation is forwarded to a backing
file opened on the provider. A change to that object is observed
through the mount immediately and by construction, because there is
nothing to invalidate.

A change to the **structure** of a participating stratum directory — an
entry created, removed, renamed, or replaced by one of another type —
may change which stratum provides a name. [Revalidation](<~kernel/internals/stratafs/coherency/model-and-revalidation#trm-4-4-2>) covers how that is
handled, which is by not caching anything.

<a id="trm-4-4-1-3"></a>

## The guarantee <a id="cite-coherency.structural-change-visible-to-next-resolution"></a>

A structural change in a stratum becomes visible to any resolution
begun after the stratum's own filesystem exposes that change to an
ordinary lookup. stratafs adds no delay of its own: there is no
timeout, no jiffies comparison, no generation counter, and no
resolution cache to serve a stale answer from.

It cannot anticipate a change the underlying filesystem is not yet
reporting. A network filesystem holding an attribute cache does not
show a change to stratafs any sooner than to any other caller, and
nothing claims otherwise.

Resolutions already completed are not revisited. Every regular-file
open is detached onto a descriptor-private dentry and inode holding
their own reference to the provider, and I/O runs against the file
opened at that time, so later masking or removal in any stratum cannot
reach that descriptor. It is not re-pointed and it does not fail. A
process holding a configuration file open across a package upgrade
continues to read the file it opened.

The one exception is copy-up, which [Inode Identity and Lifecycle](<~kernel/internals/stratafs/coherency/inode-identity-and-lifecycle#trm-4-4-3>) covers: a descriptor whose
own write caused a copy-up keeps its inode while that inode's backing
object becomes the copy.

<a id="trm-4-4-1-4"></a>

## Live strata <a id="cite-coherency.stratum-replaceable-while-mounted"></a>

Because resolutions are made against current state, and because a
stratum is a path rather than a directory object ([The Stratum Stack](<~kernel/internals/stratafs/strata-and-mounting/the-stratum-stack#trm-4-2-1>)), a stratum's
directory may be replaced wholesale — by a package transaction, by a
reconciler, by an administrator — while the mount is live, with no
remount and no interruption to callers. That is the requirement the
filesystem exists to satisfy, and [Revalidation](<~kernel/internals/stratafs/coherency/model-and-revalidation#trm-4-4-2>) is the whole of its cost.

<a id="trm-4-4-2"></a>

The specification permits an implementation to cache resolutions,
subject to a version tuple recorded per stratum and an identity
comparison on reuse. This implementation caches nothing, and so
implements neither.

<a id="trm-4-4-2-1"></a>

## Always invalidate <a id="cite-coherency.revalidate.always-invalidates"></a>

`d_revalidate` returns 0 for every dentry except the mount root. The
VFS therefore discards the dentry and re-enters `lookup` on every path
walk, and the lookup re-resolves the parent and the child from their
relative path strings across every stratum.

Nothing is memoised. No version value is recorded, no directory
identity is retained for comparison, no nearest-existing-ancestor walk
happens, and no `i_version` is read anywhere in the filesystem. The
per-dentry provider path that is retained is not a cache of a
resolution: it is dropped when the dentry is released, and the dentry
is released on the next walk.

The specification's machinery exists to know when a cached resolution
has gone stale. With no cached resolution, the questions it answers do
not arise:

| What the tuple would detect | Why it is unnecessary here |
|---|---|
| A stratum gaining or losing a name | The next walk resolves the name afresh |
| A stratum's directory appearing | The next walk finds it |
| A stratum's directory removed, renamed away, or renamed over | The next walk finds nothing, or finds the replacement |

The result is strictly stronger than the specification requires, in the
safe direction. The internal filesystem-domain, fallback-inode and
staging-name counters do not validate cached resolutions.

<a id="trm-4-4-2-2"></a>

## What it costs <a id="cite-coherency.revalidate.rcu-walk-refused"></a>

The cost is real and lands on the hottest path in the kernel.

`d_revalidate` refuses RCU-walk unconditionally: a lookup in RCU mode
returns `ECHILD` and the walk is retried in ref-walk mode, and the
directory permission check does the same. RCU-walk is therefore never
used on a stratafs mount, and the fallback is taken always rather than
only where it genuinely cannot proceed.

The refusal, invisible to the caller by design, is visible at two
tracepoints. `stratafs:stratafs_rcu_walk_refused` marks the directory
permission check turning a walk back under `MAY_NOT_BLOCK` — in
practice the first stratafs directory a walk must traverse does this,
so it is the point that actually takes every walk out of RCU mode.
`stratafs:stratafs_d_revalidate` records each revalidation verdict —
mount cookie, merged inode number (zero for a negative entry), whether
the call was in RCU mode, and the return value — and because the
permission check fires first, every recorded call arrives already in
ref-walk mode; its `-ECHILD` branch is the backstop. Like every PKM
tracepoint, neither records a pathname.

What replaces it, per path component, is one full `filename_lookup` per
stratum — up to sixteen — plus one merged resolution per proper prefix
of the path, for the ancestor-masking test of [Type Conflicts](<~kernel/internals/stratafs/name-resolution/lookup-and-type-conflicts#trm-4-3-3>). Where a mount is
established over a directory of executables, that lies on the path of
every program execution, and there is no dentry cache hit to avoid it.

This is the one part of the filesystem whose cost is worth measuring
rather than assuming, and closing the gap — recording enough per
resolution to reuse one safely, and making the comparison RCU-safe — is
tracked as work in its own right.
