---
title: "Copy-up descriptors"
description: "Copy-up descriptors: behaviour and implementation of the Peios kernel."
type: reference
---

<a id="trm-3-9-7-6"></a>

## Exact protected-metadata cloning <a id="cite-facs.stratafs-copy-up.descriptor-cloning"></a>

KACS owns descriptor cloning rather than StrataFS raw-xattr code.
Before a create phase is armed, the provider's complete effective
descriptor is resolved and pinned using the ordinary mount-policy and
corrupt-descriptor rules ([File Descriptor Storage](<~kernel/internals/kacs/file-security/descriptor-storage-and-caching#trm-3-9-5>)). A missing, corrupt, unresolvable,
oversized or unsupported descriptor fails the phase before the
destination is created. <a id="cite-facs.stratafs-copy-up.unresolvable-descriptor-fails-phase"></a>

For a matching inode security initialisation, an exact byte-for-byte
copy of the pinned descriptor is installed instead of inheritance
running. <a id="cite-facs.stratafs-copy-up.exact-copy-not-inheritance"></a> The canonical xattr is installed as part of inode creation
and the inode's validated parsed cache is seeded from identical bytes
before the inode becomes usable. <a id="cite-facs.stratafs-copy-up.xattr-and-cache-seeded"></a> Failure to allocate, validate or
install either representation fails creation — there is no window in
which a named staging inode carries an inherited or otherwise weaker
descriptor. <a id="cite-facs.stratafs-copy-up.no-weak-window"></a>

On a stacking destination the same applies to the real inode created
below the outer dentry, with the authenticated outer transition as the
only authority to redirect installation there. The pinned bytes are
installed and cached during the real inode's creation, before the
outer object is confirmed or bound; inheriting the parent's descriptor
and repairing it afterwards would not be conforming. <a id="cite-facs.stratafs-copy-up.stacking-real-inode-install"></a>

The canonical descriptor is not copied by ordinary xattr enumeration —
it is reported as cancelled so a stacking filesystem discards it — and
raw canonical getxattr and setxattr stay denied even inside the
context, with the hook-side denial evaluated before any phase match. <a id="cite-facs.stratafs-copy-up.canonical-xattr-cancelled"></a>
The context does not override the unconditional denial of POSIX ACL
mutation either. <a id="cite-facs.stratafs-copy-up.posix-acl-still-denied"></a>

Raw setxattr, including through an internal copy-up file, remains
unable to install `security.capability`. <a id="cite-facs.stratafs-copy-up.raw-setcap-denied"></a> Where the provider has one,
StrataFS calls the dedicated clone entry point during populate, after
any operation that might clear file capabilities. That call accepts
only a kernel buffer exactly matching the pinned value, under the same
user namespace it was pinned in, for the still-bound staged inode. <a id="cite-facs.stratafs-copy-up.clone-call-preconditions"></a> It
re-reads the provider immediately before installing and fails with
`ESTALE` if the value or its presence changed. <a id="cite-facs.stratafs-copy-up.clone-estale-on-change"></a>

The call copies the caller's buffer before comparing, and installs
with `XATTR_CREATE` through the ordinary VFS path, so mount-idmap
conversion, xattr validation, filesystem permission and format checks
and other LSM checks all still apply. <a id="cite-facs.stratafs-copy-up.clone-through-vfs"></a> The otherwise-dead
`CAP_SETFCAP` gate is satisfied only synchronously inside that
validated call, and the corresponding setxattr re-entry is admitted
only after the first hook matches the exact staged inode. <a id="cite-facs.stratafs-copy-up.setfcap-synchronous-only"></a> The
capability answer targets only the pinned caller namespace or the
staged inode's filesystem namespace, and the condition is cleared on
every return. Nothing is installed when the provider had no attribute,
a different one, or an unreadable or invalid one. <a id="cite-facs.stratafs-copy-up.no-install-on-mismatch"></a> The exception does
not revive exec-time file-capability grants.

There is one asymmetry here: the removal path does not reject
`security.capability` the way the set path does, so an internal
copy-up descriptor can remove it from the staged object during
populate. <a id="cite-facs.stratafs-copy-up.removal-path-asymmetry"></a>

Other eligible provider xattrs follow StrataFS's replication rules
while KACS's caller checks on their source and staging objects are
exempted as above. An ineligible xattr that cannot be replicated
triggers StrataFS's ordinary copy-up failure rule rather than being
silently omitted.

<a id="trm-4-6-3"></a>

Copy-up produces a second instance of an existing object. Its security
descriptor is the source's — owner, group, discretionary list, system
list and integrity label alike — and it is KACS that carries it, not
stratafs. <a id="cite-security.copy-up-descriptor-preserved"></a>

<a id="trm-4-6-3-1"></a>

## How it is carried <a id="cite-security.copy-up-never-inherits-descriptor"></a>

When a copy-up context is created, the provider's complete effective
descriptor is resolved and pinned as a byte string on the context. Each
create phase copies those bytes into the phase, and the inode security
initialisation for the created object installs them verbatim instead of
running inheritance. Nothing is reconstructed field by field: it is a
copy of the source bytes, so all five components are preserved together.

The canonical descriptor attribute is deliberately excluded from
stratafs's own extended-attribute replication, precisely so that the
two mechanisms cannot disagree.

The separation inside KACS is clean and explicit. The inode security
initialisation takes the copy-up branch first, and taking it
short-circuits the inheritance builder entirely. Ordinary creation in a
create stratum inherits from its parent ([Creation](<~kernel/internals/stratafs/mutation/creation#trm-4-5-3>)); copy-up preserves.
There is no path on which a copied-up object receives an inherited
descriptor.

<a id="trm-4-6-3-1-1"></a>

### Descriptors of materialised parents <a id="cite-security.materialised-parents-use-provider-descriptor"></a>

Directories materialised in the create stratum to hold a copied-up
object are handled the same way, each carrying the descriptor of the
corresponding **provider** directory — the merged provider of that same
relative path, which is what the pre-check of [Checks on Merged Directories](<~kernel/internals/stratafs/security/checks-on-merged-directories#trm-4-6-2>) evaluated against.

<a id="trm-4-6-3-2"></a>

## Failure <a id="cite-security.copy-up-descriptor-failure-fails-operation"></a>

Where the source descriptor cannot be replicated, the copy-up fails and
the operation that required it fails. A missing, corrupt, unresolvable,
oversized or unsupported descriptor fails the phase before the
destination is created, and an absent pinned descriptor at install time
fails the create.

<a id="trm-4-6-3-2-1"></a>

### Protection precedes publication <a id="cite-security.descriptor-installed-before-publication"></a>

Nothing publishes a copied-up object carrying any
other descriptor: the descriptor is installed at inode creation, before
any content, and publication is a link or rename of an object already
stamped, so there is no window in which a differently-protected object
is reachable.

The failure errno is not the specified one. [Failure Modes](<~kernel/internals/stratafs/start-here/failure-modes#trm-4-8>)'s table pairs
descriptor failure with `EIO` alongside extended-attribute failure, and
the extended-attribute half does report `EIO`. The descriptor half is
carried by KACS, whose failures surface as `EACCES`, `EOPNOTSUPP`,
`EINVAL`, `ESTALE` or `ENOMEM`; there is no `EIO` anywhere on that
path. This is tracked as a defect.

<a id="trm-4-6-3-3"></a>

## Why preservation rather than inheritance

Copy-up is reachable by any caller with the right to modify the source
object. That right does not include the right to modify the source's
descriptor, which is a separate right.

Were a copied-up object to receive an inherited descriptor, a caller
holding only write access to a restrictively protected object could
cause a copy of it to exist carrying the create stratum directory's
inheritable entries — and that copy, having higher precedence, would
become what the merged path resolves to. The object's confinement would
have been replaced by the directory's, through an operation the caller
was entitled to perform, without their ever holding the right to alter
a descriptor.

Preserving the source descriptor closes that: a copy is exactly as
reachable as its original, and copy-up changes which stratum holds an
object without changing who may reach it.

<a id="trm-4-6-3-4"></a>

## Provenance <a id="cite-security.copy-up-descriptor-owner-is-source"></a>

Because the descriptor is preserved, the copy's descriptor-level owner
is the owner of the object it was copied from, not the caller who
caused the copy. Ownership therefore does not record who created the
copy and cannot be relied on to; the audit record of [Audit](<~kernel/internals/stratafs/security/audit#trm-4-6-5>) is where
that is available.

Setting the copying caller as the descriptor owner would have preserved
provenance, and was rejected: an owner holds implicit rights over an
object's descriptor, so making the caller the owner would reintroduce
the escalation this section exists to prevent by a slightly longer
route.

The POSIX owner is preserved separately and for a different reason —
[Copy-Up](<~kernel/internals/stratafs/mutation/copy-up#trm-4-5-2>) covers the chown and [Durability and Accounting](<~kernel/internals/stratafs/mutation/durability-and-accounting#trm-4-5-8>) what it means for accounting.

<a id="trm-4-6-3-5"></a>

## What "the source's descriptor" means <a id="cite-security.copy-up-pins-effective-descriptor"></a>

The descriptor pinned at the start of a copy-up is the provider's
**effective** descriptor rather than its raw stored attribute. On a
provider mount whose own policy class synthesises, that would be the
synthesised value. In practice that case is unreachable: reaching the
object through the stratafs mount at all requires a real descriptor,
under stratafs's own deny-missing class ([Mount Policy](<~kernel/internals/stratafs/security/mount-policy#trm-4-6-4>)). A provider on an
unmanaged mount is refused outright.
