---
title: "Deferred deletion"
description: "Deferred deletion: behaviour and implementation of the Peios kernel."
type: reference
---

<a id="trm-3-9-7-5"></a>

## Deferred deletion <a id="cite-facs.stratafs-copy-up.deferred-deletion"></a>

Delete-on-close is authorized when armed and recorded on the open file
description ([KACS-Native Open](<~kernel/internals/kacs/file-security/kacs-native-open#trm-3-9-2>)). At final close there is no re-authorization
against the closing task. <a id="cite-facs.stratafs-copy-up.close-no-reauth"></a> Instead a synchronous, non-nesting internal
deletion scope is armed for that exact outer file, and StrataFS binds
it once to the exact provider parent, dentry and inode selected from
the descriptor's settled provider. <a id="cite-facs.stratafs-copy-up.deletion-scope-binding"></a> Only the corresponding outer and
lower unlink calls match, and the scope is cleared on every return.

The mechanism never turns an ordinary close into deletion authority,
never admits a different provider entry, and never permits unlinking
an entry that no longer names the descriptor's inode. <a id="cite-facs.stratafs-copy-up.deletion-identity-check"></a> If the original
entry has disappeared or changed identity, the deletion is already
complete and no exemption is used.

<a id="trm-4-5-3-3"></a>

## Deferred deletion <a id="cite-create.deferred-delete-targets-resolved-object"></a>

A request to delete an object when the last descriptor to it is closed
applies to the object the descriptor resolved to, not to whatever
provides that name at close time. Because removal ([Removal](<~kernel/internals/stratafs/mutation/removal#trm-4-5-4>)) is defined
over the current provider of a name, the deferred case has its own
path.

<a id="trm-4-5-3-3-1"></a>

### An entry already gone <a id="cite-create.deferred-delete-already-gone-succeeds"></a>

When the deletion is attempted, stratafs locates the entry at the path
the descriptor was opened against, in the stratum that provided it at
that time — the descriptor's private dentry carries both — and resolves
the parent in that same stratum. Four conditions end the attempt
quietly, reporting success because the deletion is already complete:
the parent is gone, the name is gone, the name now identifies a
different inode, or the unlink raced.

The merged parent can disappear or become a non-directory before the
VFS reaches stratafs’s unlink handler. An `ENOENT` or `ENOTDIR` from
that earlier check is also a successful no-op, but only after a lookup
in the descriptor’s original providing stratum confirms that its
recorded name is absent or identifies a different inode. A higher
stratum masking a still-live backing target does not satisfy that
condition: the deletion still fails and is audited. Other errors keep
their ordinary failure and audit behavior.

<a id="trm-4-5-3-3-2"></a>

### The original stratum must accept removal <a id="cite-create.deferred-delete-requires-writable-stratum"></a>

That stratum must accept modification, or the deletion fails with
`EROFS`. Then the entry is removed, and no other. In particular, where
another caller's copy-up has published a new object at that name in a
higher stratum, that object is not the one being deleted and is left
alone.

<a id="trm-4-5-3-3-3"></a>

### Failures are audited <a id="cite-create.deferred-delete-audits-failure"></a>

Because the attempt has no caller to report to, any failure is audited
— and for a deferred deletion, *every* non-zero result is audited, not
only the arrangement errors [Audit](<~kernel/internals/stratafs/security/audit#trm-4-6-5>) covers for ordinary refusals. The
object is left in place.

<a id="trm-4-5-3-3-4"></a>

### Authority at deletion time <a id="cite-create.deferred-delete-checked-against-the-providing-stratum"></a>

The right to delete the entry is checked against the directory of the
**stratum where the entry lives**, not against the merged parent, and
it is checked at deletion time rather than only at arm.

Arm time could not do it. The authorizer there holds a `struct file`,
and which stratum provides the entry is stratafs-internal — the
provider index and the parent's relative path are not visible to KACS.
stratafs computes that directory before removing anything, so the check
happens there, where the answer exists.

<a id="trm-4-5-3-3-5"></a>

### The requesting token outlives the arm <a id="cite-create.deferred-delete-token-outlives-the-arm"></a>

The token is the one that requested the deferred deletion, not the
credentials of whoever closes the descriptor. That requires it to
outlive the arm: the file's blob takes a reference when armed and
releases it in `->file_release`, on both the armed and unarmed exits.
The file is the thing that was armed, so its lifetime is the right
one — arm and close may be far apart and in different tasks.

<a id="trm-4-5-3-3-6"></a>

### Supported object types <a id="cite-create.deferred-delete-non-directories"></a>

Deferred deletion is restricted to non-directories, and at arm time to
regular files on a managed mount.

## Related explanations

- [Creation](<~kernel/internals/stratafs/mutation/creation>)
