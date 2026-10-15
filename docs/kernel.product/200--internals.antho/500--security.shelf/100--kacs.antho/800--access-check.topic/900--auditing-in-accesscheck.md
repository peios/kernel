---
title: "Auditing in AccessCheck"
description: "Auditing is purely observational and never changes a decision — access, continuous and privilege-use auditing, and per-token policy."
type: reference
---

<a id="trm-3-8-9"></a>

Auditing is purely observational. No audit rule affects the access
decision, and audit ACEs are evaluated after the decision is final. <a id="cite-check.auditing.observational"></a>

Three mechanisms operate inside the pipeline, emitting two families of
KMES record: `kacs.audit.access.checked` for object-access events from the SACL
walk and from token audit-policy forcing, and `kacs.audit.privilege.used` for
privilege-use events. <a id="cite-check.auditing.event-families"></a> A third family is
emitted for the CAAP conditions of [Central Access and Auditing Policy](<~kernel/internals/kacs/access-check/central-access-and-auditing-policy#trm-3-8-8>): `kacs.caap.sacl.skipped` for
a rule SACL that would not parse or evaluate, and
`kacs.caap.staging.diverged` for a staged-versus-effective mismatch. <a id="cite-check.auditing.caap-diagnostic-family"></a> The event type strings and
payload schemas are in [Audit Event Schemas](<~kernel/internals/kacs/auditing/event-families-and-delivery#trm-3-c>).

Event delivery happens before any result is written back to the
caller, and a failure to deliver fails the call. <a id="cite-check.auditing.delivery-before-result"></a> An audit event cannot
be suppressed by handing the syscall a bad output pointer.

<a id="trm-3-8-9-1"></a>

## Access auditing

`SYSTEM_AUDIT` ACEs in the SACL define which attempts to log. Each
carries a SID, an access mask, and success and failure flags —
`SUCCESSFUL_ACCESS_ACE_FLAG` (0x40) and `FAILED_ACCESS_ACE_FLAG`
(0x80).

An event is emitted when the ACE's SID matches the caller, its mask
overlaps the requested access, and its flags match the outcome. <a id="cite-check.auditing.audit-ace-conditions"></a>

<a id="trm-3-8-9-1-1"></a>

### On the AccessCheck syscall

Through `kacs_access_check` and `kacs_access_check_list` the descriptor
is the caller's own, SACL included. So that no process can write
kernel-origin audit records at will by supplying a SACL that matches
itself, the records a SACL generates there are written only when the
calling process's effective token holds `SeAuditPrivilege`, enabled.
Without it the check runs and answers exactly as it would otherwise,
and its SACL records are withheld; the privilege is marked used when it
admits them. <a id="cite-check.auditing.syscall-sacl-needs-audit-privilege"></a> The
privilege is the caller's, not the subject's: a daemon checking a
client through `token_fd` needs it on its own token. This is Windows'
rule for `AccessCheckAndAuditAlarm`.

The records the checked token's own audit policy forces, and
privilege-use and CAAP records, are not gated: the policy belongs to
the token, not to the caller. <a id="cite-check.auditing.syscall-policy-records-ungated"></a>

Two details matter. The SID is matched with **deny polarity** — the
broadest identity view, in which deny-only groups are visible —
because auditing should capture the widest possible picture rather
than the narrowest. <a id="cite-check.auditing.deny-polarity-matching"></a> And the overlap is tested against the
generic-mapped **requested** mask, not the final granted mask, so a
failed request is still auditable for the rights it actually asked
for. <a id="cite-check.auditing.overlap-against-requested"></a>

Conditional audit ACEs gate the event on an expression, using the same
deny-side membership polarity. An expression evaluating to UNKNOWN
emits the event: when in doubt, audit. <a id="cite-check.auditing.unknown-condition-emits"></a>

<a id="trm-3-8-9-2"></a>

## Continuous auditing

Access auditing fires once, where AccessCheck runs. Continuous
auditing covers per-operation monitoring.

`SYSTEM_ALARM` ACEs configure it. When AccessCheck evaluates an alarm
ACE whose SID matches, the ACE's mask is accumulated into a
**continuous audit mask** returned to the caller, which stores it on
the open handle and enforces it per operation. <a id="cite-check.auditing.alarm-accumulates-mask"></a> Conditional alarm ACEs
use the same deny-side polarity as conditional audit ACEs. The alarm
branch deliberately performs no overlap test against the requested
mask — an alarm ACE contributes its mask on a SID match alone. <a id="cite-check.auditing.alarm-no-overlap-test"></a>

On each later operation the enforcement point emits a
`kacs.audit.handle.used` event when the operation's normalised
required-access mask overlaps the stored mask. <a id="cite-check.auditing.continuous-event-on-overlap"></a> For FACS handles that
is the same mask used by the use-time check ([Use-Time Semantics](<~kernel/internals/kacs/file-security/use-time-semantics#trm-3-9-4>)). Where an
operation's authorization accepts any one of several rights — append
or write data, say — the required mask holds the accepted set and the
event records the subset that overlapped, as `access.matched`, beside
the whole stored mask as `access.audit-mask`. <a id="cite-check.auditing.continuous-records-overlapping-subset"></a>

Events are emitted after the per-operation decision is known, for
successful and denied attempts alike. <a id="cite-check.auditing.continuous-both-outcomes"></a> The subject and process recorded
are the **operation-time** effective token and current task, not
necessarily the ones that opened the handle. <a id="cite-check.auditing.continuous-operation-time-subject"></a> That keeps attribution
correct after a handle is passed between processes, while still using
the opener-computed mask to decide whether the handle is audited at
all.

An enforcement point that cannot construct a required continuous-audit
event fails closed. <a id="cite-check.auditing.continuous-fails-closed"></a> Transport buffering and drop accounting remain
KMES's concern ([Failure Modes](<~kernel/internals/kmes/failure-modes#trm-2-7>)).

<a id="trm-3-8-9-3"></a>

## Privilege-use auditing

When a privilege is exercised to grant access the DACL would not have
granted independently, a privilege-use event may be emitted. This runs
after the complete pipeline — after integrity policy, confinement and
central access policy — so it reflects the final result rather than an
intermediate one. <a id="cite-check.auditing.privilege-use-after-pipeline"></a>

**Successful** privilege use means the privilege's contributed bits
survive into the final granted result. The privilege is marked used,
and an event is emitted when the token's `audit_policy` carries
`PRIVILEGE_USE_SUCCESS` (0x04). <a id="cite-check.auditing.privilege-use-success"></a> **Failed** privilege use means the
privilege contributed bits during evaluation that did not survive. The
privilege is *not* marked used, and an event is emitted under
`PRIVILEGE_USE_FAILURE` (0x08). <a id="cite-check.auditing.privilege-use-failure"></a> A privilege that contributed nothing
to the requested access produces no event either way. <a id="cite-check.auditing.privilege-use-no-contribution"></a>

With an object type list, the test is per-node: a privilege counts as
successfully used if its bits survive on *any* node's final mask. <a id="cite-check.auditing.privilege-use-per-node"></a>

A `MAXIMUM_ALLOWED` request short-circuits this stage entirely,
recording no used bits and emitting no privilege-use events at all. <a id="cite-check.auditing.max-allowed-skips-privilege-use"></a>

How counterfactual the accounting really is varies by privilege, as
[The Privilege Model](<~kernel/internals/kacs/privileges/the-privilege-model#trm-3-4-1>) describes: `SeSecurityPrivilege` and `SeTakeOwnershipPrivilege`
contribute only where the DACL had not already granted the right,
while backup and restore seed their bits unconditionally and so also
report use for accesses the DACL alone would have permitted. <a id="cite-check.auditing.backup-restore-overreport"></a>

<a id="trm-3-8-9-4"></a>

## Per-token audit policy

A token's `audit_policy` can force events regardless of SACL content.
This runs after the SACL walk and before result computation: if the
access succeeded and the policy carries `OBJECT_ACCESS_SUCCESS`
(0x01), a success event is emitted; if it failed and the policy
carries `OBJECT_ACCESS_FAILURE` (0x02), a failure event is. <a id="cite-check.auditing.forced-events"></a>

Success here means every requested bit was granted, or that nothing
was requested at all. <a id="cite-check.auditing.forced-success-definition"></a>

These events are additive — they fire even when no SACL ACE matched —
and they carry the object identity from the audit context the caller
supplied, exactly as a SACL-triggered record does. <a id="cite-check.auditing.forced-additive"></a> The
policy is per-token, fixed at creation, and follows impersonation,
since it is read from the effective token. <a id="cite-check.auditing.policy-from-effective-token"></a>

<a id="trm-3-8-9-5"></a>

## Event contents

An event carries the **subject**, the calling token's identity —
`subject.token.sid`, `.groups` with their parallel `.group-attributes`,
`.integrity`, the token's own LUID as `.id`, its logon session as
`.auth-id`, `.type`, `.impersonation` and the projected `.uid` — and
the PIP state as `subject.pip.type` and `subject.pip.trust`; the
**object**, as `object.kind` and the fields beneath it; the **access**,
as `access.requested` and `access.granted`, with `outcome.success`;
the **trigger**, `trigger.kind` (`sacl` or `policy`) and, for `sacl`,
the matched ACE as `trigger.ace`, or for a privilege record the
`privilege.*` fields; and the **process**, as
`emitter.process.pid`, `.name` and `.executable`. <a id="cite-check.auditing.event-contents"></a>

An access record also says what the mandatory checks withheld, since
that is often the whole reason a check the DACL would allow was denied:
`access.denied-integrity` is the requested bits the object's mandatory
label denied, and `access.denied-trust` the requested bits its
process-trust label denied — every bit each denied, for a
`MAXIMUM_ALLOWED` request — and each is absent when it denied none. <a id="cite-check.auditing.mandatory-denials-recorded"></a>

The pipeline itself produces only the object-and-access half — the
matched ACE bytes, the requested and granted masks, the outcome,
whether the event was policy-forced, the privilege, and the audit
context. The subject and process halves are attached at emission time
from the resolved call context, which is also where the effective PIP
values used for the verdict are reused for attribution.

<a id="trm-3-8-9-5-1"></a>

### The object

Where the kernel makes the check itself it knows the kind of object
and writes `object.kind`: `file`, `process`, `token`, `socket` (which
covers port-reservation binds) or `ipc`. A token check also writes the
target's `object.token.id` and `object.token.guid`. Some identity is
not yet reachable where the record is built, and is absent rather than
invented: `object.file.path` on file checks, `object.process.pid` and
`object.process.guid` on process checks. A mount-namespace check writes
`object.kind` `mount-namespace` and nothing beneath it: a namespace has
no name or identifier to carry. <a id="cite-check.auditing.mount-namespace-object-kind"></a>

A check made through `kacs_access_check` names its object through the
**audit context** (`audit_context_ptr`, `audit_context_len`), the
PGSS [The event stream](<~kernel/internals/ntfe/event-ring-and-delivery#trm-6-7>) map:

```text
{kind: "service", service: {name: "jellyfin"}}
```

The kernel validates it before running the check and fails the call
with `EINVAL` unless it is well-formed msgpack no deeper than KMES's
default nesting depth less one; its root is a map of one or two
entries with string keys; it has exactly one `kind`, a string matching
the PGSS [The snapshot](<~kernel/internals/ntfe/the-snapshot#trm-6-3>) segment grammar `[a-z][a-z0-9]*(-[a-z0-9]+)*`; and its
only other entry is keyed by that kind and holds a non-empty map whose
keys match the same grammar. The kernel copies it into the record as
`object.kind` and `object.<kind>.*` — `object.service.name` above. A
call without an audit context writes no `object`: the kernel does not
know what was checked.

These values are the caller's claim, which the kernel copied but did
not observe. So is everything else on the syscall path: the descriptor,
and with it `trigger.ace`, is the caller's, as is any PIP type or trust
it passes. Every record of `kacs_access_check` and
`kacs_access_check_list` therefore carries `fields.attestation.userspace`
set to `true`, with or without an audit context, and a record of a check
the kernel makes itself never does. <a id="cite-check.auditing.syscall-records-asserted"></a>
A context that is anything other than this map, such as the free-form
strings earlier components passed, fails with `EINVAL`.
