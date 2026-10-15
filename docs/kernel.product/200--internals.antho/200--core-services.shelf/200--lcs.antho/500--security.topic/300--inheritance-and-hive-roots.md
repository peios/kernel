---
title: "Inheritance and Hive Roots"
description: "A new key's descriptor is computed from its parent by the KACS inheritance algorithm — plus hive roots and reading or writing a descriptor."
type: reference
---

<a id="trm-5-4-3"></a>

<a id="trm-5-4-3-1"></a>

## Inheritance at creation

When `reg_create_key` creates a key, its initial Security Descriptor is
computed from the parent's by the KACS inheritance algorithm. LCS
supplies the parent descriptor, the creating token, the registry
generic mapping and the valid-mask bound, and hands the result to the
source to persist. It implements no inheritance logic of its own. <a id="cite-inherit.kacs-computes-lcs-persists"></a>

Three things about registry inheritance are worth stating.

**It is static.** The computation happens once, at creation. A later
change to the parent's descriptor does not propagate to children that
already exist. <a id="cite-inherit.static-no-repropagation"></a> Re-propagating is an explicit administrative action — a
client-side tree walk — not a kernel operation, and there is no code
anywhere in LCS that walks a tree to re-propagate.

**Only `CONTAINER_INHERIT_ACE` matters.** Every registry object is a
container: keys hold subkeys and values. Values are not independent
security objects and have no descriptors of their own; they inherit
their key's access control. <a id="cite-inherit.values-have-no-descriptor-of-their-own"></a>

`OBJECT_INHERIT_ACE` is never used to
select an ACE for inheritance. <a id="cite-inherit.object-inherit-ace-never-selects"></a> The child copy clears `OBJECT_INHERIT_ACE`,
`CONTAINER_INHERIT_ACE` and `NO_PROPAGATE_INHERIT_ACE` when
`NO_PROPAGATE_INHERIT_ACE` applies. <a id="cite-inherit.no-propagate-clears-object-inherit"></a>

**A parent with no inheritable ACEs falls back to the creating token's
default DACL.** <a id="cite-inherit.no-inheritable-aces-uses-token-default-dacl"></a>

That fallback covers the DACL only; there is no default
SACL. <a id="cite-inherit.no-default-sacl"></a>

<a id="trm-5-4-3-1-1"></a>

### Creator SIDs and generic rights survive to the next generation

An inheritable ACE naming `CREATOR OWNER` or `CREATOR GROUP`, or carrying
generic rights, is resolved for each new key. When it also propagates to
further subkeys, the child receives two ACEs:

- An effective copy with the child's owner/group substituted and generic
  rights mapped to registry rights. It has `INHERITED_ACE` and no propagation
  flags.
- An inherit-only copy retaining the original SID and generic mask, with
  `INHERITED_ACE` and its propagation flags. This copy resolves afresh when
  the next subkey is created.

This applies to both DACL and SACL entries. An ordinary concrete ACE remains
one copy. `NO_PROPAGATE_INHERIT_ACE` ends the rule at the immediate child,
so it receives only the effective copy. Existing stored descriptors are not
rewritten by upgrading the kernel; an explicit propagation operation is
needed to repair an already-created subtree.

<a id="trm-5-4-3-2"></a>

## Hive roots

A hive root has no parent, so it is the top of every inheritance chain
below it and cannot inherit anything itself. <a id="cite-inherit.hive-root-inherits-nothing"></a> Its descriptor is created
by the **source**, on first boot, and LCS enforces whatever the source
stored. <a id="cite-inherit.hive-root-descriptor-comes-from-the-source"></a>

LCS holds no template. There are no hardcoded SIDs, no default hive
root descriptors, and no code that would construct one — searching for
them finds nothing. The defaults that follow are what loregd writes;
they are conventions of the source, not properties of the kernel.

**`Machine\`:** <a id="cite-inherit.machine-root-default-descriptor"></a>

| Principal | Rights | Inheritance |
|---|---|---|
| SYSTEM | `KEY_ALL_ACCESS` | Container-inherit |
| Administrators | `KEY_ALL_ACCESS` | Container-inherit |
| Authenticated Users | `KEY_READ` | Container-inherit |

**`Users\<SID>\`:** <a id="cite-inherit.user-root-default-descriptor"></a>

| Principal | Rights | Inheritance |
|---|---|---|
| the user's SID | `KEY_ALL_ACCESS` | Container-inherit |
| SYSTEM | `KEY_ALL_ACCESS` | Container-inherit |
| Administrators | `KEY_ALL_ACCESS` | Container-inherit |

These mirror Windows HKLM and HKU. A subsystem needing something
tighter — `Machine\Security\`, say — sets an explicit descriptor on its
own subtree root at creation, overriding what it inherited.

Because there is no traverse checking ([The Access Flow](<~kernel/internals/lcs/security/the-access-flow#trm-5-4-1>)), a restrictive
descriptor high in the tree protects only the key it is on. Protection
of a subtree comes from the descriptors its keys inherited at creation,
which is exactly why an administrator changing a parent's descriptor
and expecting the subtree to follow will be disappointed.

<a id="trm-5-4-3-3"></a>

## Reading and writing descriptors

`REG_IOC_GET_SECURITY` and `REG_IOC_SET_SECURITY` take a
`security_info` bitmask naming which components to act on: owner,
group, DACL, SACL, or mandatory integrity label (`LABEL_SECURITY_INFORMATION`). <a id="cite-inherit.security-info-selects-components"></a>

Zero is `EINVAL`, and so is any unknown flag; both
are rejected before the source is contacted, before transaction
enlistment and before any mutation. <a id="cite-inherit.security-info-zero-or-unknown-is-einval"></a>

The rights required are computed from every component named. Reading
owner, group, the DACL or the label needs `READ_CONTROL`; reading the SACL needs
`ACCESS_SYSTEM_SECURITY`. Setting owner **or group** needs
`WRITE_OWNER`, as does setting the label; setting the DACL needs `WRITE_DAC`; setting the SACL
needs `ACCESS_SYSTEM_SECURITY`. A request naming several components
must hold all the corresponding rights.

A set is a merge, not a replacement. LCS reads only the components
`security_info` names from the supplied self-relative descriptor and
preserves the existing ones. <a id="cite-inherit.set-security-is-a-merge"></a>

Component selection includes its control flags even when the component
has no bytes. A null ACL remains `PRESENT` clear, but its defaulted,
inheritance and protection flags survive a query or an update to another
component. Replacing a selected DACL or SACL takes that ACL's flags from
the input descriptor, including for a null ACL; unselected component
flags are preserved. An empty ACL remains present with zero ACEs and is
not converted to null. The same preservation rule applies to a defaulted
null group. <a id="cite-inherit.null-acl-control-flags"></a>

`LABEL_SECURITY_INFORMATION` reads only the first effective mandatory-label
ACE from the SACL, omitting inherit-only labels and every non-label ACE.
If there is no effective label, the returned subset has no SACL. Reading
this subset needs `READ_CONTROL`; writing it needs `WRITE_OWNER`. Neither
operation needs `ACCESS_SYSTEM_SECURITY` or `SeSecurityPrivilege`.
<a id="cite-inherit.label-access-and-projection"></a>

A label update removes the existing mandatory-label ACEs and inserts the
supplied label before the remaining SACL entries. An input descriptor
with no SACL clears the explicit label. Non-label SACL entries, SACL
inheritance and protection flags, and all unselected descriptor components
are preserved, including flags on a null DACL. Clearing the last SACL
entry clears `SE_SACL_PRESENT` while retaining the other SACL flags.
<a id="cite-inherit.label-merge-preserves-other-security"></a>

For a label-only subset, a supplied SACL must contain exactly one
mandatory-label ACE with an `S-1-16-<level>` SID and without
`INHERIT_ONLY_ACE`; an empty ACL, an audit ACE, or multiple labels is
`EINVAL`. `SACL_SECURITY_INFORMATION` and `LABEL_SECURITY_INFORMATION`
cannot be combined. These input errors are rejected before source contact
or transaction enlistment. <a id="cite-inherit.label-input-validation"></a>

An explicit label above the current caller's integrity level requires
enabled `SeRelabelPrivilege`, checked before source contact or transaction
enlistment; otherwise the update fails with `EACCES`. Labels at or below
the caller's level do not require that privilege. The same rule applies
to an explicit label inside a whole-SACL write: `SeSecurityPrivilege`
does not substitute for `SeRelabelPrivilege`. Existing fd rights remain
cached, but this privilege check uses the caller performing the update.
<a id="cite-inherit.label-level-constraint"></a>

The result must still have an owner; a
merge that would leave the descriptor ownerless is `EINVAL`. <a id="cite-inherit.merge-must-leave-an-owner"></a>

A null
group SID stays valid. <a id="cite-inherit.null-group-sid-is-valid"></a>

Enlisting a descriptor change in a transaction gives it atomicity with
the rest of the transaction's operations. It does not make it
layer-qualified: the change is still a direct mutation on the key, is
still not reverted by deleting a layer, and is simply not applied at
all if the transaction aborts. <a id="cite-inherit.descriptor-change-in-a-transaction"></a>
