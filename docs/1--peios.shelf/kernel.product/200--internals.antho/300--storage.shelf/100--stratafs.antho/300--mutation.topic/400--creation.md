---
title: "Creation"
description: "Creation: behaviour and implementation of the Peios kernel."
type: reference
---

<a id="trm-4-5-3"></a>

Creating a name held by no participating stratum places it in the
create stratum. <a id="cite-create.lands-in-create-stratum"></a>

1. If there is no create stratum, or it is absent, the operation fails
   with `EROFS`. <a id="cite-create.erofs-without-create-stratum"></a>
2. Any directories of the create stratum containing the name's path
   that do not exist are materialised as [Copy-Up](<~kernel/internals/stratafs/mutation/copy-up#trm-4-5-2>) requires for copy-up
   parents. Where the create stratum holds one of those components as
   something other than a directory, the operation fails with
   `ENOTDIR`; the blocking entry is not removed or replaced. <a id="cite-create.parent-conflict-enotdir"></a>
3. The name is created there.

All six kinds of creation — regular file, directory, symbolic link,
device node, FIFO, socket — go through one helper and one path.

The `ENOTDIR` case arises because creation routes positionally, into
the create stratum's subdirectory at the same path whether or not it
exists ([Directory Merge](<~kernel/internals/stratafs/name-resolution/directory-merge#trm-4-3-2>)). Where the create stratum holds that path as a file,
and a higher-precedence stratum provides it as a directory, the merged
directory exists and is reachable while its create-stratum counterpart
is blocked.

<a id="trm-4-5-3-1"></a>

## The security descriptor <a id="cite-create.descriptor-inherited-from-parent"></a>

A created object has no provider to inherit from, so its descriptor is
established by the ordinary creation semantics of the create stratum's
filesystem — by inheritance from the directory it is created in,
exactly as if it had been created there directly. The create is an
ordinary `vfs_create`, `vfs_mkdir`, `vfs_symlink` or `vfs_mknod`
against the real create-stratum parent, with the KACS creation decision
bound to that same parent.

This is cleanly separated from copy-up inside KACS: the copy-up branch
of the inode security initialisation is taken first and short-circuits
the inheritance builder entirely. Ordinary creation in a create stratum
inherits; copy-up preserves.

Where the creating interface lets the caller supply a descriptor — the
native open path does — it is honoured rather than replaced by an
inherited one. That is entirely KACS's doing; stratafs has no
descriptor parameter and cannot express it. All stratafs contributes is
re-anchoring the pending native create request onto the create-stratum
parent.

<a id="trm-4-5-3-2"></a>

## Dispositions that delete <a id="cite-create.supersede-is-removal-then-creation"></a>

A creating interface may offer a disposition that replaces an existing
object rather than opening it. In Peios that is the supersede
disposition of the native open path: KACS creates a temporary file
through the mount, opens it, and renames it onto the target, at which
point stratafs diverts the rename into a dedicated supersede path.

Such a disposition requires both removal and creation authority. This
does not prescribe their publication order. Before anything is created,
the removal is validated: the
target's provider must accept modification, or the operation fails with
`EROFS`. Before anything is removed, the replacement is checked for
reachability: if any stratum strictly above the create stratum, other
than the provider being removed, holds the name, the operation fails
with `EROFS`.

Without that guard the disposition could report success while leaving
the caller's new object invisible. The removal takes the name out of
the stratum that provided it; the creation puts the replacement in the
create stratum; and if some stratum between the two also holds the
name, it now outranks the replacement.

The creation half is treated as a creation throughout. It is never
reclassified as a modification of a newly-surfaced provider and never
copies one up: the caller asked for a new object, and its descriptor is
derived as above.

<a id="trm-4-5-3-2-1"></a>

### Implementation restrictions

Three restrictions are implementation choices rather than consequences
of the model:

1. Supersede applies to regular files only, and anything else is refused
   with `EOPNOTSUPP`. <a id="cite-create.supersede-regular-files-only"></a>
2. The source must be in the create stratum, and source and destination
   must share a parent. <a id="cite-create.supersede-source-and-parent-restrictions"></a>
3. Across distinct strata the two halves are **not** atomic. The staged
   file is renamed into place in the create stratum **before** the old
   provider is unlinked. Between those operations both backing names
   exist: ordinary precedence selects the replacement if the create
   stratum is higher, or retains the original until its removal if it is
   higher. A failure to publish leaves the original untouched, rather
   than exposing a still-lower provider. <a id="cite-create.supersede-is-not-atomic"></a>

   Write access to the original provider is probed before publication,
   then released while the replacement is published. It is reacquired
   for removal; a provider remounted read-only in between therefore fails
   with `EROFS` after publication. The two backing mounts never have
   simultaneous freeze-protection holds, even when they share a superblock.

   A later removal failure is returned to the caller and recorded as
   `supersede-removal`. Native-open cleanup then attempts to remove the
   newly published object, following its final name rather than its old
   temporary name. If the original still has its name, successful
   cleanup restores its visibility; concurrent provider changes are
   preserved. Cleanup is itself a filesystem operation and can fail;
   in that case both entries can remain, with ordinary precedence
   deciding which is visible. A crash between publication and removal
   can likewise leave both. This ordering narrows the destructive
   failure window; it does not promise a transaction or crash recovery.

   When both objects are in the create stratum, replacement uses one
   backing-filesystem rename and needs no separate provider unlink.

<a id="trm-4-5-3-4"></a>

## Exclusive creation <a id="cite-create.exclusive-eexist-from-any-stratum"></a>

Where creation is requested exclusively, the name must not exist in
**any** participating stratum, and a name provided by a lower stratum
causes `EEXIST` even though the create stratum does not hold it.

Nothing in stratafs implements this, and nothing needs to. The merged
lookup instantiates a positive dentry whenever any stratum holds the
name, and the VFS refuses `O_EXCL` on a dentry it did not create. The
`excl` argument stratafs receives is ignored. There is a race backstop
in the create path — a positive dentry appearing in the create stratum
yields `EEXIST` — but it sees only that one stratum.

Exclusive creation asks whether the name is free, and through this
mount it is not: a caller that created it anyway would find their
object shadowing a file they did not know was there, or masking a whole
subtree.

<a id="trm-4-5-3-5"></a>

## Non-exclusive creation over a shadowed name <a id="cite-create.shadowed-non-exclusive-is-open"></a>

Where creation is not exclusive and a lower stratum provides the name,
the merged dentry is positive, so the VFS never calls the create path
at all. The operation is an open, and [Write Routing](<~kernel/internals/stratafs/mutation/write-routing#trm-4-5-1>) routes it.

Where the provider is a regular file that does not accept modification
and the create stratum has higher precedence, the result is a copy-up
followed by the requested modification, including truncation where
`O_TRUNC` was requested. `O_TRUNC` is stripped from the backing open on
a non-in-place route precisely so that the copy-up source is not
destroyed before it is read.

Where the provider is a FIFO, socket, or device node, no copy-up occurs
and the open is forwarded to the provider. Such an open succeeds
whether or not the provider accepts modification: opening a special
file does not modify it.

<a id="trm-4-5-3-6"></a>

## Unnamed files <a id="cite-create.unnamed-file-in-create-stratum"></a>

A file may be created without a name, for later linking into place. In
a merged directory this is supported, and the file is created on the
create stratum's filesystem, recorded with the create stratum's index
and marked unnamed.

Where the mount has no create stratum, or it is absent, the operation
fails with `EROFS`. Parent materialisation applies as for a named
creation: the create stratum's counterpart of the directory the
operation named is materialised, and the new file's descriptor is
derived by inheritance from it, because that directory is what the
descriptor must come from. Linking such a file into the mount is
governed by [Links](<~kernel/internals/stratafs/mutation/links#trm-4-5-6>).
