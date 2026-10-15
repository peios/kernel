---
title: "The DACL Walk"
description: "Walking the ACEs in order under first-writer-wins — SID matching, absent and empty DACLs, owner implicit rights and MAXIMUM_ALLOWED."
type: reference
---

<a id="trm-3-8-2"></a>

The DACL is an ordered list of ACEs, walked from first to last,
comparing each ACE's SID against the calling token's identity. The
governing principle is **first-writer-wins**: once a bit has been
resolved, granted or denied, no later ACE changes the outcome for that
bit. <a id="cite-check.dacl.first-writer-wins"></a>

An **allow** ACE whose SID matches the token grants the rights it
carries that have not yet been decided, leaving already-decided bits
untouched. <a id="cite-check.dacl.allow-grants-undecided"></a> A **deny** ACE whose SID matches denies its
not-yet-decided rights — marking them decided but not granted — and
likewise leaves decided bits alone. <a id="cite-check.dacl.deny-marks-decided"></a>

<a id="trm-3-8-2-1"></a>

## SID matching

An ACE's SID matches the token when it equals the user SID or a group
SID on the token, subject to attribute filtering.

For **allow** ACEs, only groups that are enabled and not deny-only
match. <a id="cite-check.dacl.allow-enabled-groups-only"></a> For **deny** ACEs, both enabled groups and deny-only groups
match: a deny-only group always participates in deny matching whatever
its enabled state. <a id="cite-check.dacl.deny-matches-deny-only"></a> A group with neither `SE_GROUP_ENABLED` nor
`SE_GROUP_USE_FOR_DENY_ONLY` participates in no matching at all. <a id="cite-check.dacl.inert-group"></a>

The user SID follows the same rule — when `user_deny_only` is set on
the token, it matches deny ACEs and not allow ACEs. <a id="cite-check.dacl.user-deny-only"></a>

<a id="trm-3-8-2-2"></a>

## Skipping and mapping

ACEs carrying `INHERIT_ONLY` exist purely to propagate to child
objects and are skipped by the walk. <a id="cite-check.dacl.inherit-only-skipped"></a>

At the top of the walk each ACE's access mask is mapped through
`MapGenericBits` using the same GenericMapping applied to the caller's
request. <a id="cite-check.dacl.ace-mask-mapped"></a> The mapping works on a local copy — the ACE itself is never
mutated. Mapping ACE masks at evaluation time is a deliberate
departure from MS-DTYP, and it is what makes `GENERIC_ALL` work in
central access policy recovery ACEs ([Central Access and Auditing Policy](<~kernel/internals/kacs/access-check/central-access-and-auditing-policy#trm-3-8-8>)).

<a id="trm-3-8-2-3"></a>

## Absent and empty DACLs

If the descriptor has no DACL — `SE_DACL_PRESENT` unset — every valid
right not already decided by an earlier pipeline stage is granted. <a id="cite-check.dacl.absent-grants-valid-rights"></a> The
valid rights are bounded by `MapGenericBits(GENERIC_ALL, mapping)`
rather than by a raw `0xFFFFFFFF`. <a id="cite-check.dacl.absent-bounded-by-generic-all"></a>

If the DACL is present but holds zero ACEs, the walk grants nothing. <a id="cite-check.dacl.empty-grants-nothing"></a>
The only access an owner gets in that case comes from the implicit
rights mechanism below.

<a id="trm-3-8-2-4"></a>

## Owner implicit rights

By default the owner of an object receives `READ_CONTROL` and
`WRITE_DAC` whatever the DACL says. <a id="cite-check.dacl.owner-implicit-rights"></a> These are granted **before** the
walk begins, as the first action inside `EvaluateDACL`, and because
first-writer-wins governs the walk, no deny ACE encountered later can
override them. <a id="cite-check.dacl.owner-implicit-before-walk"></a>

`EvaluateDACL` takes a `skip_owner_implicit` parameter. The
confinement pass sets it, because confinement is an absolute
intersection with no owner bypass.

The grant is suppressed entirely if any non-inherit-only
access-control ACE in the DACL targets the `OWNER RIGHTS` SID
(`S-1-3-4`). <a id="cite-check.dacl.owner-rights-suppresses-implicit"></a> This is a pre-scan performed at the start of
`EvaluateDACL`, before the main loop, and it checks only for the SID's
presence — it does not evaluate any conditional expression on the ACE. <a id="cite-check.dacl.owner-rights-prescan-presence-only"></a>

During the walk proper, `S-1-3-4` is treated as an ordinary SID
matching the owner, at both allow and deny polarity. <a id="cite-check.dacl.owner-rights-ordinary-sid"></a> It obeys the same
rules as any other SID: an allow ACE matches only through an enabled,
non-deny-only group, and not through the user SID of a
`user_deny_only` token; a deny ACE matches through a group that is
enabled or deny-only, and through the user SID unconditionally.

Note that the *implicit* grant above is a separate rule and remains
presence-based. It is bounded by the pre-scan rather than by polarity.

The implicit grant is also bounded twice over: by the object type's
valid rights, and by what has already been decided. A pre-decision
from MIC, PIP or a privilege therefore suppresses it — a non-dominant
owner does not receive `WRITE_DAC` through this route. <a id="cite-check.dacl.owner-implicit-bounded-by-decided"></a>

<a id="trm-3-8-2-5"></a>

## MAXIMUM_ALLOWED

When the caller includes `MAXIMUM_ALLOWED` (bit 25), AccessCheck runs
the full pipeline and returns the complete set of rights that would be
granted. The bit is stripped from the desired mask before evaluation
begins. <a id="cite-check.dacl.max-allowed-stripped"></a>

Two things change. The walk runs to completion with no short-circuit,
and the returned mask is whatever the pipeline accumulated rather than
being filtered to the requested bits. <a id="cite-check.dacl.max-allowed-returns-accumulated"></a>

`MAXIMUM_ALLOWED` can be combined with specific rights:
`MAXIMUM_ALLOWED | READ_CONTROL` asks both "can I read the
descriptor?" as a success or failure and "what else could I get?" as a
mask. A pure `MAXIMUM_ALLOWED` request carrying no specific bits
always succeeds. <a id="cite-check.dacl.max-allowed-alone-succeeds"></a>

Otherwise — when the desired mask is fully decided — the walk may stop
early.

First-writer-wins applies to `MAXIMUM_ALLOWED` requests exactly as it
does to targeted ones. <a id="cite-check.dacl.max-allowed-first-writer-wins"></a> MS-DTYP treats the two differently; KACS does
not, which is what stops "what can I do?" and "can I do this?"
disagreeing on a DACL that is not in canonical order.
