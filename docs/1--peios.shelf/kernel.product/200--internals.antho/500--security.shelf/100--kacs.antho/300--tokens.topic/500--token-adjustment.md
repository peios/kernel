---
title: "Token Adjustment"
description: "What can be changed on a live token — privileges, groups, interactivity scope and object-creation defaults — and what cannot."
type: reference
---

<a id="trm-3-2-5"></a>

A live token's privileges, groups, default object-creation metadata,
and interactive session metadata can be adjusted at runtime. These are
distinct operations with separate access rights and constraint models.
All of them mutate the token object in place using atomic operations,
all become visible immediately to every thread sharing the token, and
all bump `modified_id`. <a id="cite-token.adjust.in-place-visible-bumps-modified-id"></a>

<a id="trm-3-2-5-1"></a>

## AdjustPrivileges

Requires `TOKEN_ADJUST_PRIVILEGES` on the token, and has three modes. <a id="cite-token.adjust.privs.requires-right"></a>

**Enable and disable** flips individual bits in `privileges_enabled`
for privileges present on the token. A privilege that is not present
cannot be enabled, and disabling one that is already absent is a
no-op. <a id="cite-token.adjust.privs.absent-enable-fails-disable-noop"></a> The operation activates existing privileges; it never grants
new ones.

**Reset to defaults** restores `privileges_enabled` to match
`privileges_enabled_by_default`, returning every privilege to its
creation-time state in one operation. It is encoded as a single
`kacs_priv_entry` with `luid = 0` and
`attributes = KACS_PRIV_RESET_ALL_DEFAULTS`. <a id="cite-token.adjust.privs.reset-encoding"></a> The reset touches only
`privileges_enabled`: it does not restore privileges that were removed
from `privileges_present`. <a id="cite-token.adjust.privs.reset-does-not-restore-removed"></a>

**Remove** permanently deletes a privilege, clearing its bit in
`privileges_present`, `privileges_enabled`, and
`privileges_enabled_by_default` together. Removing an already-absent
privilege is a no-op. <a id="cite-token.adjust.privs.remove-absent-noop"></a> The deletion is irreversible; nothing re-adds a
privilege to a token.

Duplicate privilege indices in one request are invalid. <a id="cite-token.adjust.privs.duplicate-indices-invalid"></a> The kernel
validates every entry before applying any change, so an invalid entry
fails the whole operation with no state change at all. <a id="cite-token.adjust.privs.all-or-nothing"></a> The caller
receives a report of each adjusted privilege's previous state. <a id="cite-token.adjust.privs.reports-previous-state"></a>

<a id="trm-3-2-5-2"></a>

## AdjustGroups

Requires `TOKEN_ADJUST_GROUPS` on the token, and has two modes. <a id="cite-token.adjust.groups.requires-right"></a>

**Enable and disable** flips `SE_GROUP_ENABLED` on individual groups,
within two constraints. A group carrying `SE_GROUP_MANDATORY`,
`SE_GROUP_USE_FOR_DENY_ONLY`, or `SE_GROUP_LOGON_ID` cannot be
adjusted **in either direction** — not enabled, not disabled, whatever
its current state; naming one in a request fails the whole call. <a id="cite-token.adjust.groups.protected-attributes-either-direction"></a> And
the user SID, when it appears in the group list, cannot be disabled,
which is the one constraint that is direction-scoped. <a id="cite-token.adjust.groups.user-sid-cannot-disable"></a>

**Reset to defaults** restores every group to its creation-time
enabled state. It restores only that state — it does not clear
`SE_GROUP_USE_FOR_DENY_ONLY` from a group that FilterToken marked
deny-only afterwards. <a id="cite-token.adjust.groups.reset-keeps-deny-only"></a>

Groups are addressed by zero-based index into the token's groups
array. A count of 0 is invalid, as is a count above 1024, as are
duplicate indices in one request. <a id="cite-token.adjust.groups.count-and-duplicate-limits"></a> Reset is encoded as a single
`kacs_group_entry` of `{ index = 0xFFFFFFFF, enable = 0 }`. <a id="cite-token.adjust.groups.reset-encoding"></a>

The caller receives the previous enabled state of every group as a
1024-bit mask encoded as sixteen 64-bit words in ascending order: word
0 covers group indices 0–63, word 1 covers 64–127, and bit `i % 64` of
word `i / 64` corresponds to group index `i`. Since group arrays cap
at 1024 entries, the mask is complete for any valid token. <a id="cite-token.adjust.groups.previous-state-mask"></a>

<a id="trm-3-2-5-3"></a>

## AdjustInteractivityScope

Requires `TOKEN_ADJUST_INTERACTIVITY_SCOPE` on the token and
`SeTcbPrivilege` on the caller's real token. <a id="cite-token.adjust.interactivity-scope.gates"></a> It changes the token's
`interactivity_scope` to a new `u32` and nothing else: the field is
metadata, and changing it grants or removes no privilege, group,
access right, label, claim, default owner, default primary group,
default DACL, or any other authorization state. <a id="cite-token.adjust.interactivity-scope.metadata-only"></a>

<a id="trm-3-2-5-4"></a>

## AdjustDefault

Requires `TOKEN_ADJUST_DEFAULT` on the token, and covers three fields. <a id="cite-token.adjust.default.requires-right"></a>

The **default DACL** applied to new objects is replaced by an RCU
pointer swap, with the old DACL freed after a grace period. The
**owner SID index** changes which SID becomes the default owner of new
objects, and has to reference the user SID or a group carrying
`SE_GROUP_OWNER`. The **primary group index** changes the default
primary group, and has to reference the user SID or any group SID on
the token. Both index updates are atomic.

All three affect future object creation only; existing objects are
untouched. <a id="cite-token.adjust.default.future-objects-only"></a> None can escalate anything, because the caller is choosing
among SIDs already on their own token.

`audit_policy` is fixed at creation, and no adjustment operation
changes it.
