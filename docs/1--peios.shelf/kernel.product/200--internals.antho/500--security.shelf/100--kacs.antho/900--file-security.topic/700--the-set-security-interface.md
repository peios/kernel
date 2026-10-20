---
title: "The Set-Security Interface"
description: "The single syscall all descriptor modification flows through — ownership, integrity labels, the SeRestorePrivilege bypass and mandatory attributes."
type: reference
---

<a id="trm-3-9-6"></a>

All descriptor modification flows through one syscall. The caller
provides a file descriptor or path, a bitmask naming which components
to modify, and a self-relative descriptor blob carrying the new
values.

| Flag | Component | Required right |
|---|---|---|
| `OWNER_SECURITY_INFORMATION` | Owner SID | `WRITE_OWNER` <a id="cite-facs.set-sd.owner-requires-write-owner"></a> |
| `GROUP_SECURITY_INFORMATION` | Group SID | `WRITE_OWNER` |
| `DACL_SECURITY_INFORMATION` | Discretionary ACL | `WRITE_DAC` <a id="cite-facs.set-sd.dacl-requires-write-dac"></a> |
| `SACL_SECURITY_INFORMATION` | System ACL | `ACCESS_SYSTEM_SECURITY` <a id="cite-facs.set-sd.sacl-requires-access-system-security"></a> |
| `LABEL_SECURITY_INFORMATION` | Mandatory integrity label | `WRITE_OWNER`, plus the integrity constraints below <a id="cite-facs.set-sd.label-requires-write-owner"></a> |

The blob is validated structurally — parseable, well-formed ACEs,
valid SIDs, at most 65535 bytes. With an existing valid file security descriptor,
only the indicated components are merged into it. Unindicated components
are preserved unchanged. <a id="cite-facs.set-sd.merge-preserves-unindicated"></a>

The input is always one self-relative descriptor subset, never a raw
SID or ACL fragment. `SACL_SECURITY_INFORMATION` and
`LABEL_SECURITY_INFORMATION` cannot be combined in one call, because
both target the SACL field with incompatible meanings; the pair fails
with `EINVAL`. <a id="cite-facs.set-sd.sacl-label-exclusive"></a>

A `SACL_SECURITY_INFORMATION` write replaces the object's **entire**
SACL. <a id="cite-facs.set-sd.sacl-write-replaces-all"></a> A `LABEL_SECURITY_INFORMATION` write interprets the input SACL
as the label subset only: no SACL component removes the explicit
mandatory label and returns the object to the default unlabelled
state; a present SACL contains exactly one non-inherit-only
`SYSTEM_MANDATORY_LABEL_ACE` and nothing else; and the object's
non-label SACL ACEs are preserved. <a id="cite-facs.set-sd.label-write-subset"></a>

After merging, the result still has a non-null owner — the group SID
may be null — and a merge that would leave no owner fails. <a id="cite-facs.set-sd.owner-must-remain"></a>

MIC and PIP apply to these checks. A low-integrity caller cannot
modify a high-integrity file's descriptor even where the DACL grants
`WRITE_OWNER`. <a id="cite-facs.set-sd.mic-pip-apply"></a>

A read-only mount withholds the write along that path whatever the
descriptor grants: the call fails with `EROFS`, as every modifying
operation through a read-only bind does, and the descriptor stays
writable through any writable path to the same object. The mount is
consulted after the access check, so a caller the descriptor refuses
sees the denial rather than a read-only error that would confirm the
object exists. <a id="cite-facs.set-sd.read-only-mount-erofs"></a>

<a id="trm-3-9-6-1"></a>

## Component merging and replacement

For a file whose cached descriptor is valid, [the C dispatcher](https://github.com/peios/pkm/blob/8e0e22de3a59cad506bbbf8873de456e16ad272d/kacs/sd_access.c#L197-L255) selects the merge path. The [control-bit merge](https://github.com/peios/pkm/blob/8e0e22de3a59cad506bbbf8873de456e16ad272d/kacs/token_runtime.rs#L4232-L4264) starts from the destination control value and replaces these bits from the input when their component is selected:

| Selected component | Replaced control bits |
|---|---|
| Owner | `OWNER_DEFAULTED` |
| Group | `GROUP_DEFAULTED` |
| DACL | `DACL_DEFAULTED`, `DACL_TRUSTED`, `DACL_AUTO_INHERIT_REQ`, `DACL_AUTO_INHERITED`, `DACL_PROTECTED` |
| Full SACL | `SACL_DEFAULTED`, `SACL_AUTO_INHERIT_REQ`, `SACL_AUTO_INHERITED`, `SACL_PROTECTED` |

This copies more than ACE lists, but is not byte-identical descriptor replacement. If group is not selected, [the destination group remains](https://github.com/peios/pkm/blob/8e0e22de3a59cad506bbbf8873de456e16ad272d/kacs/token_runtime.rs#L4347-L4351). The [resource-manager control byte remains the destination's](https://github.com/peios/pkm/blob/8e0e22de3a59cad506bbbf8873de456e16ad272d/kacs/token_runtime.rs#L4410-L4416), as does its `RM_CONTROL_VALID` state. A label-only merge does not replace the full-SACL control-bit set in the table.

A missing or invalid cached file security descriptor does **not** take that merge path. The dispatcher requires enabled `SeRestorePrivilege` and calls the [replacement builder](https://github.com/peios/pkm/blob/8e0e22de3a59cad506bbbf8873de456e16ad272d/kacs/token_runtime.rs#L4420-L4468), which requires owner, group and DACL selections and validates the supplied owner and label. Do not apply valid-descriptor field-retention guarantees to that repair case.

These details are source-checked against kernel commit [`8e0e22de`](https://github.com/peios/pkm/tree/8e0e22de3a59cad506bbbf8873de456e16ad272d), not a runtime-validated restore procedure.

<a id="trm-3-9-6-2"></a>

## Ownership <a id="cite-facs.set-sd.ownership"></a>

A new owner may be set only to the caller's own SID, or to a group SID
on the token carrying `SE_GROUP_OWNER`. `SeTakeOwnershipPrivilege`
allows setting ownership to the caller's own SID regardless of what
the current descriptor says, and `SeRestorePrivilege` allows any
arbitrary SID. <a id="cite-facs.set-sd.take-ownership-and-restore"></a>

<a id="trm-3-9-6-3"></a>

## Integrity labels <a id="cite-facs.set-sd.label-level-constraint"></a>

Without enabled `SeRelabelPrivilege` a caller may set a label only at or below
its own integrity level; with it, the label-level check permits any level.
Other access and validation checks still apply.

The constraint applies through **both** paths — the dedicated label
subset, and a label ACE embedded in a full SACL write. A SACL write
whose ACL contains a mandatory label ACE raising integrity above the
caller's level requires `SeRelabelPrivilege` exactly as the label path
does, even though the SACL component itself is gated only by
`ACCESS_SYSTEM_SECURITY`. <a id="cite-facs.set-sd.label-constraint-via-sacl"></a>
`SeSecurityPrivilege` or `SeRestorePrivilege` alone is not sufficient for
a label above the caller's integrity: the [label-assignment check](https://github.com/peios/pkm/blob/8e0e22de3a59cad506bbbf8873de456e16ad272d/kacs/token_runtime.rs#L4180-L4197) independently requires enabled
`SeRelabelPrivilege`.

<a id="trm-3-9-6-4"></a>

## The SeRestorePrivilege bypass

`SeRestorePrivilege` fires inside the AccessCheck pipeline, so it
bypasses the check only where `kacs_set_sd` runs a **live** one: an
`O_PATH` descriptor with `AT_EMPTY_PATH`, a pidfd, a token descriptor
with `AT_EMPTY_PATH`, or a path. <a id="cite-facs.set-sd.restore-bypass-live-only"></a> On those paths it grants every
requested right, `WRITE_OWNER`, `WRITE_DAC` and
`ACCESS_SYSTEM_SECURITY` included.

Called on an ordinary file descriptor the required rights are checked
against the cached mask instead, no AccessCheck runs, and the
privilege has no effect at all. <a id="cite-facs.set-sd.restore-no-effect-on-fd"></a> A caller needing the bypass has to use
the `O_PATH` route — which is the mechanism behind backup restoration,
administrative repair, and the missing-descriptor repair path
([File Descriptor Storage](<~kernel/internals/kacs/file-security/descriptor-storage-and-caching#trm-3-9-5>)).

<a id="trm-3-9-6-5"></a>

## Mandatory resource attributes <a id="cite-facs.set-sd.mandatory-attribute-requires-tcb"></a>

When a caller modifies the SACL, the existing and new SACLs are
compared for changes to `SYSTEM_RESOURCE_ATTRIBUTE_ACE` entries. An
existing attribute carrying `CLAIM_SECURITY_ATTRIBUTE_MANDATORY`
(0x0020) cannot be removed, nor its values modified, without
`SeTcbPrivilege` — and an attempt without it fails the entire call
rather than silently dropping the change.

<a id="trm-3-9-6-6"></a>

## Write mechanics

The updated descriptor is serialised to self-relative binary form and
written to the xattr through an internal kernel path bypassing the
denial hook, and the in-memory cache is updated. <a id="cite-facs.set-sd.write-bypasses-denial-hook"></a> An audit event is
emitted if the file's SACL carries a matching audit ACE. <a id="cite-facs.set-sd.audit-on-matching-ace"></a>

The cache update is not atomic with the xattr write; [File Descriptor Storage](<~kernel/internals/kacs/file-security/descriptor-storage-and-caching#trm-3-9-5>) describes
the lock ordering that forces this and the last-writer-wins window it
produces.
