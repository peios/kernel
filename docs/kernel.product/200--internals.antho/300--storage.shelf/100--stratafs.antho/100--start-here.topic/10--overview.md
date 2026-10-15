---
title: "Overview"
description: "stratafs presents an ordered set of existing directories as one tree — where it sits, the model it follows, and what it delegates."
type: reference
---

<a id="trm-4-1"></a>

stratafs presents an ordered set of existing directories — its
**strata** — as one merged directory tree. Each stratum is an ordinary
directory on an ordinary filesystem, owned and written by whatever
agent owns it, with no coordination with stratafs and no notification
to it. The merged view reflects changes to any stratum without a
remount. <a id="cite-mount.reflects-stratum-changes"></a>

It is a stacking filesystem in the strict sense: it stores no file
data, no directory entries, and no security descriptors. Every object
reachable through a stratafs mount is a real object on a real stratum,
and every data and metadata operation is performed against that object. <a id="cite-model.every-object-is-real"></a>
stratafs inodes carry no address-space operations, so there is no
second page cache to keep coherent; reads, writes, mappings and splices
are forwarded to a backing file opened on the provider.

Unlike overlayfs, stratafs has **no whiteouts and no opaque-directory
markers**. There is no mechanism anywhere in the filesystem for
recording that a name should be absent. That single omission accounts
for most of what is unusual about it: removing a name can leave the
name visible, some names cannot be removed at all, and several
operations that succeed on an ordinary filesystem are refused here
rather than faked. [Failure Modes](<~kernel/internals/stratafs/start-here/failure-modes#trm-4-8>) collects the consequences.

<a id="trm-4-1-1"></a>

## Where it sits <a id="cite-mount.superblock-identity"></a>

stratafs lives in `fs/stratafs`, alongside PKM. It is built by `CONFIG_STRATAFS_FS` — a boolean option, so it
is linked into `vmlinux` — and registered by an `fs_initcall`. The
option depends on `CONFIG_SECURITY_PKM`, because stratafs reaches KACS
for every access decision and for the whole of the copy-up context.
That reach is through `<linux/kacs_stratafs.h>`, a kernel-private
header in `include/linux` whose symbols are deliberately not exported
to modules. This is a private in-kernel integration interface, not a
userspace API.

The filesystem type registers under the name `stratafs`, with the
superblock magic `0x53545241` — ASCII `STRA` — and the flags
`FS_USERNS_MOUNT` and `FS_RENAME_DOES_D_MOVE`. It takes no device;
superblocks come from `get_tree_nodev`, so the device identifier
reported for every object in a mount is an anonymous one belonging to
the mount rather than to any stratum.

A small part of the filesystem is written in Rust. The crate
`stratafs-core` compiles the sources in `security/pkm/stratafs_core`
and holds three pure, allocation-free decisions: validating the
stack-wide flag rules, selecting the provider from a presence bitmap,
and routing one modifying operation. Everything else — the VFS glue,
resolution, enumeration, copy-up — is C.

<a id="trm-4-1-2"></a>

## The model <a id="cite-strata.identified-by-path"></a>

A mount is defined by its **stratum stack**: an ordered list of strata,
highest-precedence first, fixed for the life of the mount. A stratum is
identified by its **path**, not by the directory that path resolved to
at mount time, which is what allows a package transaction to replace a
whole stratum by renaming trees around underneath a live mount.

For a given name in a given directory, the **provider** is the
highest-precedence stratum that holds it. A name whose provider is a
directory, and which lower strata also hold as a directory, resolves to
a **merged directory** whose entries are the union of theirs. A name
whose provider is anything else masks every lower entry of that name
completely, subtree and all.

At most one stratum carries the `create` flag. That **create stratum**
receives newly created objects and is the destination of **copy-up** —
the replication of an object into the create stratum so that a
modification can be applied without touching the stratum that provides
it. A stack may have no create stratum, in which case nothing can be
created and nothing copied up.

Routing a modification is a decision about strata alone. It happens
when the modifying operation is performed, never at open, and it never
consults the caller: by the time an operation reaches stratafs, KACS
has already decided the caller was entitled to perform it. [Write Routing](<~kernel/internals/stratafs/mutation/write-routing#trm-4-5-1>) sets
out why no other formulation is implementable.

<a id="trm-4-1-3"></a>

## What it delegates

stratafs holds no security descriptors, so it makes no access
decisions of its own about the objects it presents. The descriptor
evaluated for an operation is the one on the object the operation will
be performed against, and KACS reads it through the ordinary
extended-attribute path, which the stacking layer forwards down to the
provider. A stratafs mount cannot grant access its provider stratum
would refuse.

A merged directory is the exception, because it stands for several
real directories with several descriptors and forwarding yields only
the provider's. Those checks stratafs performs itself, against every
participating directory, requiring all of them to succeed ([Checks on Merged Directories](<~kernel/internals/stratafs/security/checks-on-merged-directories#trm-4-6-2>)).

Copy-up is the other exception, in the opposite direction. It is
machinery serving an operation that was already authorised, not an
operation a caller requests, so it must introduce no new checks against
whichever task happens to execute it. KACS provides a kernel-internal
copy-up context for exactly this, described in full at [The StrataFS Copy-Up Context](<~kernel/internals/stratafs/security/kacs-admission-and-object-phases#trm-3-9-7>); [Descriptors on Copy-Up](<~kernel/internals/stratafs/security/copy-up-descriptors#trm-4-6-3>)
covers the stratafs half.

<a id="trm-4-1-4"></a>

## This chapter

[The Stratum Stack](<~kernel/internals/stratafs/strata-and-mounting/the-stratum-stack#trm-4-2-1>) covers the stack, the mount options that define it, what a
mounter must be entitled to, and absent strata. [Lookup](<~kernel/internals/stratafs/name-resolution/lookup-and-type-conflicts#trm-4-3-1>) covers resolution:
providers, merging, type conflicts, and enumeration. [The Coherency Model](<~kernel/internals/stratafs/coherency/model-and-revalidation#trm-4-4-1>) covers
coherency — how uncoordinated change is observed, and the inode
identity presented over it. [Write Routing](<~kernel/internals/stratafs/mutation/write-routing#trm-4-5-1>) covers mutation: routing, copy-up,
creation, removal, rename, links, locking and durability. [Access Check Delegation](<~kernel/internals/stratafs/security/access-check-delegation#trm-4-6-1>) covers
the security seam with KACS, and [The Origin Attribute](<~kernel/internals/stratafs/start-here/the-origin-attribute#trm-4-7>) the one interface stratafs
synthesises for userspace. [Failure Modes](<~kernel/internals/stratafs/start-here/failure-modes#trm-4-8>) collects the failure modes, including
the divergences from ordinary filesystem behaviour that follow from
having no whiteouts, and [Constants](<~kernel/internals/stratafs/start-here/generated-constants#trm-4-a>) the constants.

## Mounting and testing

See [StrataFS mount options](<~kernel/administration/stratafs/mount-options>) for operation, and [StrataFS test hooks](<~kernel/development/native-subsystems/stratafs-test-hooks>) for development.

## Topics

- [Security](<~kernel/internals/stratafs/security/overview>)
- [Mutation](<~kernel/internals/stratafs/mutation/overview>)
- [Strata and mounting](<~kernel/internals/stratafs/strata-and-mounting/overview>)
- [Name resolution](<~kernel/internals/stratafs/name-resolution/overview>)
- [Coherency](<~kernel/internals/stratafs/coherency/overview>)
