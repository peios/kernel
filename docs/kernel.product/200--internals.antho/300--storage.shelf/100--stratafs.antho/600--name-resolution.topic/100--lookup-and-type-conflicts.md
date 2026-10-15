---
title: "Lookup and type conflicts"
description: "Resolving one name in one directory — the provider, ancestors, independence from the caller, and staging entries."
type: reference
---

<a id="trm-4-3-1"></a>

Resolution is defined for one name in one directory. Every path
operation is a sequence of such resolutions, each independent of the
last.

<a id="trm-4-3-1-1"></a>

## The provider <a id="cite-resolution.provider-is-highest-stratum"></a>

To resolve a name in a stratafs directory, the corresponding directory
of each stratum is examined in precedence order, and the first stratum
holding an entry of that name is its **provider**. If no stratum holds
it, the resolution produces a negative dentry and the VFS reports
`ENOENT`.

Mechanically, each stratum's path string is joined with the relative
path of the name and walked in full, once per stratum. A walk that
succeeds sets that stratum's bit in a presence bitmap; a walk that
fails with `ENOENT` or `ENOTDIR` leaves it clear and the stratum is
skipped. Selecting the provider is then the trailing-zero count of the
bitmap, computed in `stratafs-core`.

Any other error from a stratum's walk — `EACCES`, `EIO`, `ELOOP`,
`ENAMETOOLONG`, `ESTALE` — is not treated as absence. It fails the
whole resolution, so a stratum that is unreadable for a reason other
than not being there masks the name entirely rather than being passed
over.

A joined stratum path, or a child relative path, that would exceed
`PATH_MAX` fails with `ENAMETOOLONG`.

<a id="trm-4-3-1-2"></a>

## Ancestors <a id="cite-resolution.provider-chosen-per-component"></a>

Resolution does not consult a parent's provider to find a child's. A
name's provider is chosen afresh across all strata, so if `/a` is
provided by stratum 2, `/a/b` may still be provided by stratum 1 —
provided stratum 1 also holds `/a` as a directory and the two therefore
merge ([Directory Merge](<~kernel/internals/stratafs/name-resolution/directory-merge#trm-4-3-2>)).

What resolution does consult is whether any ancestor of the path is
masked. Before resolving the final component, every proper prefix of
the relative path is resolved across all strata and its merged provider
computed; a prefix whose provider is not a directory aborts the whole
resolution with `ENOTDIR`. That is what makes masking total ([Type Conflicts](<~kernel/internals/stratafs/name-resolution/lookup-and-type-conflicts#trm-4-3-3>)),
and it is why a lookup costs one full walk per stratum for the name
itself plus one merged resolution per path component above it.

<a id="trm-4-3-1-3"></a>

## Independence from the caller <a id="cite-resolution.independent-of-caller"></a>

Resolution runs under the credentials captured at mount, against the
root captured at mount, and takes no operation argument. It does not
depend on the calling token, on what the caller is trying to do, or on
whether the operation will ultimately be permitted.

A name whose provider the caller may not access therefore resolves
normally and is then refused. It does not fall through to a lower
stratum — which would let a caller's rights change which file they
read, a considerably worse property than a denial.

<a id="trm-4-3-1-4"></a>

## Reaching the object <a id="cite-resolution.non-directory-forwarded"></a>

Once a name resolves to a non-directory provider, the object is the
provider's object and stratafs does not interpose on its contents. The
outer inode takes the provider's mode and, from it, the operations
tables for a regular file, symlink or special file; reads, writes,
mappings, splices, locks and `ioctl`s are forwarded to a backing file
opened on the provider.

Symbolic links are forwarded rather than followed. The outer inode's
`get_link` calls the provider inode's own and returns the raw target
verbatim; stratafs deliberately does not use `vfs_get_link`, which
would demand a read right the caller need not hold to traverse a link.
The VFS then interprets the target in the caller's own namespace, so an
absolute target resolves from the process's root and may re-enter this
mount, another stratafs mount, or none.

Where a mount is established at a path within a stratum, stratafs
follows it: the stratum walk is an ordinary `filename_lookup` with no
flag restricting it to one filesystem, and everything downstream
operates on the inner mount it returns.

<a id="trm-4-3-1-5"></a>

## Staging entries <a id="cite-resolution.staged-names-hidden"></a>

One class of name is invisible to resolution. While a copy-up is in
flight, its staged object may exist under a name in the create stratum;
that name is dropped from resolution for the mount that owns it, so an
incomplete copy is never reachable through the merged view ([Copy-Up](<~kernel/internals/stratafs/mutation/copy-up#trm-4-5-2>)).
The suppression applies only to the create stratum, and only within the
owning mount — a second stratafs mount sharing that directory, and any
direct reader of it, sees an ordinary entry.

<a id="trm-4-3-1-5-1"></a>

### Recovery triggered by lookup <a id="cite-resolution.staging-prefix-triggers-recovery"></a>

Staged names begin with `.stratafs-stage-`, and a lookup of any name
with that prefix triggers a recovery scan of the create-stratum parent
before resolving. A resolution can therefore have the side effect of
removing orphaned staging entries from the create stratum.

<a id="trm-4-3-1-6"></a>

## Recursion <a id="cite-resolution.reentrant-superblock-eloop"></a>

A task that is already resolving inside a superblock and re-enters the
same superblock fails immediately with `ELOOP`. The guard is a global
list of task-and-superblock pairs, not a depth counter, so a cycle
formed after mount — a stratafs mount established inside one of its own
strata, or bind-mounted into one — terminates the moment resolution
returns to a mount it is already inside.

<a id="trm-4-3-3"></a>

Two strata may hold the same name with different types — a directory in
one, a regular file in another. The provider's type is the type of the
resolved object, and the outer inode is given the provider's mode and
the operations tables that follow from it. <a id="cite-resolution.conflict-provider-type-wins"></a>

- Where the provider is a **directory**, lower-precedence strata that
  hold the name as a directory participate in a merged directory
  ([Directory Merge](<~kernel/internals/stratafs/name-resolution/directory-merge#trm-4-3-2>)). Lower-precedence strata that hold the name as anything else
  are masked. <a id="cite-resolution.conflict-directory-merges-only-directories"></a>
- Where the provider is **not** a directory, every lower-precedence
  entry of that name is masked, whatever its type. <a id="cite-resolution.non-directory-masks-lower"></a> Only the provider's
  path is retained on the dentry; the other strata's references are
  released as soon as the provider is chosen.

<a id="trm-4-3-3-1"></a>

## Masking is total <a id="cite-resolution.masking-hides-whole-subtree"></a>

A masked entry is unreachable through the mount. Where the masked entry
is a directory, its entire subtree is unreachable: no path beneath the
masked name resolves, regardless of what the masked directory contains
and regardless of whether some other stratum holds part of that
subtree.

This is enforced by the ancestor pass described in [Lookup](<~kernel/internals/stratafs/name-resolution/lookup-and-type-conflicts#trm-4-3-1>). Each proper
prefix of a relative path is resolved across every stratum and its
merged provider computed; a prefix whose merged provider is not a
directory returns `ENOTDIR` before the final component is considered.
Because the test uses the merged answer rather than a per-stratum one,
another stratum holding the subtree cannot rescue it.

A regular file at `/x` in a high-precedence stratum therefore hides a
whole `/x/…` tree in a lower one. That is severe, and deliberate: the
alternative — resolving `/x` as a file but `/x/y` through the masked
directory — would make a path's meaning depend on how far along it the
caller looked.

<a id="trm-4-3-3-1-1"></a>

### Masking leaves the strata unchanged <a id="cite-resolution.masking-does-not-modify-strata"></a>

Masking modifies nothing. Resolution and enumeration are read-only
throughout, no marker is written to any stratum, and the masked entry
remains present and unchanged in its own stratum, reachable by any path
that does not traverse the mount.

<a id="trm-4-3-3-2"></a>

## Stability <a id="cite-resolution.conflict-operation-fails-against-provider"></a>

Type conflicts resolve identically for every caller and every
operation, because provider selection is a pure function of the
presence bitmap and consults neither.

An operation that would only be valid against the masked type does not
cause the masked entry to be selected. It fails against the provider
instead, with whatever error that type produces — typically `ENOTDIR`
from the ancestor pass, or `EISDIR` raised by the generic VFS against
an outer inode carrying the provider's mode.
