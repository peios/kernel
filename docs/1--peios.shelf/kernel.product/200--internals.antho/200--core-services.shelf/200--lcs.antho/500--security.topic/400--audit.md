---
title: "Audit"
description: "The fifteen audit events LCS emits, which are unconditional, how registry writes are audited through a key handle's alarm mask, and what happens when emission itself fails."
type: reference
---

<a id="trm-5-4-4"></a>

LCS emits audit events through KMES. Fifteen events exist. <a id="cite-lcs-audit.events-through-kmes"></a>

| Event | Emitted when |
|---|---|
| `lcs.audit.key.opened` | A key open matched a SACL audit ACE. <a id="cite-lcs-audit.key-open.on-sacl-match"></a> |
| `lcs.audit.value.set` | A value write through a handle whose audit mask covers `KEY_SET_VALUE`. |
| `lcs.audit.value.deleted` | A value delete through a handle whose audit mask covers `KEY_SET_VALUE`. |
| `lcs.audit.key.tombstoned` | A blanket tombstone set or cleared through a handle whose audit mask covers `KEY_SET_VALUE`. |
| `lcs.audit.key.deleted` | A key deleted through a handle whose audit mask covers `DELETE`. |
| `lcs.audit.key.hidden` | A key hidden through a handle whose audit mask covers `DELETE`. |
| `lcs.audit.key.created` | A key create that made a key matched a SACL audit ACE on the parent. |
| `lcs.audit.key.descriptor.changed` | A descriptor change included the SACL, or its right is covered by the handle's audit mask. |
| `lcs.audit.transaction.committed` | A transaction that staged an audited write ended. |
| `lcs.audit.backup.started` | After admission checks and before `REG_IOC_BACKUP` requests its read-only snapshot or reads any subtree data. <a id="cite-lcs-audit.backup-start.before-any-read"></a> |
| `lcs.audit.backup.ended` | After a backup completes or fails after starting. <a id="cite-lcs-audit.backup-complete.after-finish-or-failure"></a> |
| `lcs.audit.restore.started` | Before `REG_IOC_RESTORE` modifies any source state. <a id="cite-lcs-audit.restore-start.before-any-mutation"></a> |
| `lcs.audit.restore.ended` | After a restore completes or fails after starting. <a id="cite-lcs-audit.restore-complete.after-finish-or-failure"></a> |
| `lcs.source.response.rejected` | LCS rejected malformed source data. <a id="cite-lcs-audit.validation-failure.on-malformed-source-data"></a> |
| `lcs.config.value.rejected` | LCS rejected an invalid self-configuration value. <a id="cite-lcs-audit.self-config-invalid.on-invalid-value"></a> |

A registry open that a privilege contributed to is also recorded, as KACS's
`kacs.audit.privilege.used`; see [Privilege use on opens](#privilege-use-on-opens).

Backup and restore are audited **unconditionally**, whatever the SACL
on the target key says. <a id="cite-lcs-audit.backup-and-restore-unconditional"></a> They are privilege-gated bulk operations that
bypass per-key access checks entirely, so the audit trail is the only
record that they happened.

Every payload is a single MessagePack map with string keys. <a id="cite-lcs-audit.payload-is-a-msgpack-map"></a>
Each field path is written as nested maps, one per segment, so
`object.key.guid` is `{object: {key: {guid: …}}}`. A value LCS does not
have is left out rather than written as nil, and every map counts only
the keys actually written (PGSS [Evaluation](<~kernel/internals/ntfe/evaluation#trm-6-4>)).

The key GUID, `object.key.guid`, is a 16-byte binary value, and the
caller's SID is a binary KACS encoding. The token and process GUIDs
are not payload fields at all: they ride in the KMES event header, so
the payload never repeats them. <a id="cite-lcs-audit.payload-guid-and-sid-encoding"></a>

<a id="trm-5-4-4-1"></a>

## The caller summary

Every event except `lcs.source.response.rejected` and
`lcs.config.value.rejected` describes the effective token used for the
operation under `subject.token`. It has six fields and no more: `sid`,
`integrity`, `id` (the token's LUID), `auth-id` (its logon session's
LUID), `type` (`primary` or `impersonation`) and `impersonation`, the
impersonation level. <a id="cite-lcs-audit.caller-summary-nine-fields"></a>

The bound is deliberate. Group lists, privilege arrays, claims and
default DACLs are unbounded and are never included. The summary carries
enough to correlate an event with a caller, and nothing that could make
one event arbitrarily large. `lcs.source.response.rejected` and
`lcs.config.value.rejected` carry no caller: neither is a principal
acting.

A primary token reports an impersonation
level of 0. <a id="cite-lcs-audit.primary-token-impersonation-level-zero"></a> An Anonymous impersonation token also
reports 0, which is why `subject.token.type` is recorded beside it.

<a id="trm-5-4-4-2"></a>

## Key opens

`lcs.audit.key.opened` carries the caller summary, then
`object.kind` (always `key`, which names the table the masks decode
against), `object.key.guid`, the requested and granted masks as
`access.requested` and `access.granted`, `outcome.success` (`true`
when the open was allowed), and `trigger.sacl-match` — bit 0 for a
success-audit match, bit 1 for a failure-audit match, no other
bits. <a id="cite-lcs-audit.key-open.payload-fields"></a>

`access.granted` is forced to zero on a denial, and that is enforced
rather than merely intended: a denied event carrying a non-zero granted
mask is rejected as a malformed payload. <a id="cite-lcs-audit.key-open.denied-event-has-zero-granted"></a>

`access.requested` is the mask
after registry generic mapping, with `MAXIMUM_ALLOWED` re-added if the
caller asked for it. <a id="cite-lcs-audit.key-open.requested-access-is-post-mapping"></a>

SACL evaluation follows the KACS AccessCheck algorithm — the SACL is
evaluated alongside the DACL, not separately. <a id="cite-lcs-audit.sacl-evaluated-with-the-dacl"></a>

Reading or modifying a
SACL requires `ACCESS_SYSTEM_SECURITY`, which is itself gated by
`SeSecurityPrivilege`. <a id="cite-lcs-audit.sacl-access-gated-by-sesecurityprivilege"></a>

A request of `MAXIMUM_ALLOWED` **alone** maps to a desired mask of zero,
so AccessCheck's SACL walk matches each audit ACE against the *granted*
mask instead. <a id="cite-lcs-audit.key-open.maximum-allowed-matches-granted-mask"></a> An audit ACE says "audit when someone gets this right",
and with `MAXIMUM_ALLOWED` they did get it.

Such an open therefore
always audits as a success, which is correct: `MAXIMUM_ALLOWED` returns
whatever is available and never fails, so a failure ACE has nothing to
record. <a id="cite-lcs-audit.key-open.maximum-allowed-always-audits-success"></a>

An ACE naming a right the caller did not receive still does not
match. <a id="cite-lcs-audit.key-open.ace-for-ungranted-right-does-not-match"></a>

<a id="trm-5-4-4-3"></a>

## Registry writes

Writes are audited through the key handle, as file operations are
through a file handle. When a key is opened, the access check evaluates
the key's `SYSTEM_ALARM*` ACEs against the caller, and the union of the
masks of the ones that match becomes the handle's **continuous-audit
mask**. <a id="cite-lcs-audit.write.alarm-mask-cached-at-open"></a> Success and failure
`SYSTEM_AUDIT` ACEs do not contribute; they govern the open itself. This
is the continuous auditing of [Auditing in AccessCheck](<~kernel/internals/kacs/access-check/auditing-in-accesscheck#trm-3-8-9>) with LCS as the enforcement point,
except in two respects: LCS writes records named for the operation
rather than `kacs.audit.handle.used`, and a record it cannot write does
not fail the operation (see below).

The mask is fixed for the life of the handle. A later change to the
key's SACL neither adds to it nor takes from it, so a handle that removes
the alarm ACE is still audited for the change it makes, and handles
opened before an alarm ACE was added are not. <a id="cite-lcs-audit.write.mask-fixed-for-handle-life"></a>

A write through the handle is recorded when the right it needs overlaps
the mask, and not otherwise. <a id="cite-lcs-audit.write.recorded-when-right-overlaps-mask"></a>
The right is the one the handle's own gate checks:

| Event | Operation | Right |
|---|---|---|
| `lcs.audit.value.set` | `REG_IOC_SET_VALUE` | `KEY_SET_VALUE` |
| `lcs.audit.value.deleted` | `REG_IOC_DELETE_VALUE` | `KEY_SET_VALUE` |
| `lcs.audit.key.tombstoned` | `REG_IOC_BLANKET_TOMBSTONE` | `KEY_SET_VALUE` |
| `lcs.audit.key.deleted` | `REG_IOC_DELETE_KEY` | `DELETE` |
| `lcs.audit.key.hidden` | `REG_IOC_HIDE_KEY` | `DELETE` |

<a id="cite-lcs-audit.write.rights-per-event"></a>

A write that fails is recorded too, with `outcome.success` false and
`outcome.errno` the negative errno the caller received. That includes a
write the handle's own gate refuses because the handle lacks the right:
the mask comes from the SACL, not the grant, so it can cover rights the
handle was not given. <a id="cite-lcs-audit.write.failures-recorded"></a>

Every write record carries the caller summary; `object.kind` (`key`),
`object.key.guid` and `object.key.path`, the handle's key and its
resolved path; `object.key.layer.name`, the layer written; the masks
`access.requested` (the right above), `access.granted` (the handle's
grant), `access.matched` and `access.audit-mask`; `transaction.id` when
the write was staged in a transaction; and `outcome.success`, with
`outcome.errno` on a failure. A failure also carries `request.timed-out`.
Value records add `object.key.value.name`; a value write adds the value's
type and length and a digest of its data, and `mutation.sequence`, with
`mutation.sequence-expected` on a compare-and-swap; a tombstone change
adds `operation.name` (`set` or `clear`); a hide adds `mutation.sequence`.
A field the operation had not reached when it failed is left out. <a id="cite-lcs-audit.write.payload-fields"></a>

A value's data is never recorded. In its place a record carries the data's
type, its length and its SHA-256 digest, so two records can be compared
without either holding the data. Every digest LCS records, of a value or
of a security descriptor, is SHA-256. <a id="cite-lcs-audit.write.data-recorded-as-sha256-digest"></a>

A value write outside a transaction also records the value it replaced, as
`object.key.value.type-previous`, `.length-previous` and
`.digest-previous`: the effective value before the write, across every
layer. A value delete records the value it removed the same way. <a id="cite-lcs-audit.write.previous-value-recorded"></a>

A write whose source does not answer before the request timeout fails
with `ETIMEDOUT`, and its record carries `request.timed-out` true. The
source is not told to cancel, so the change may still land; for a value
write or descriptor change outside a transaction, LCS also applies the
write's kernel-side effects when the late reply arrives, and nothing
records who made the write then. Read a timed-out record as "may have
been applied later". <a id="cite-lcs-audit.write.timed-out-may-apply-later"></a>

A write made in a transaction is recorded when it is staged, with
`transaction.id`. Its `outcome.success` then says the source accepted it
into the transaction, not that it took effect. <a id="cite-lcs-audit.write.transacted-recorded-when-staged"></a>

<a id="trm-5-4-4-3-1"></a>

### Transaction ends

A transaction that staged at least one recorded write — a write or a key
creation whose record was emitted — writes one
`lcs.audit.transaction.committed` when it ends, and only one: at a
`REG_IOC_COMMIT` that leaves it committed or otherwise finished, at its
timeout, or when its fd is closed without a commit. A commit that fails
and leaves the transaction open writes nothing yet. <a id="cite-lcs-audit.txn-committed.once-per-recorded-transaction"></a>

It carries the caller summary, `transaction.id` and `transaction.state`,
the state it ended in, and `outcome.success`, true only for `committed`.
A failure adds `transaction.commit-outstanding` and `outcome.reason`:
`aborted` (closed without a commit, or a layer it wrote was deleted),
`timed-out` or `source-error`; and `outcome.errno` when a
`REG_IOC_COMMIT` call failed. <a id="cite-lcs-audit.txn-committed.payload-fields"></a>

On `REG_IOC_COMMIT` the subject is the caller who committed, not the one
who staged the writes. A transaction that ended by timeout or by its fd
closing has nobody acting, and names the subject that staged its first
recorded write. The timer that ends a transaction runs in softirq context,
which cannot build a record; the record is written from the work item
that aborts the transaction at the source. <a id="cite-lcs-audit.txn-committed.subject"></a>

A commit whose reply does not arrive in time reports `timed-out` with
`transaction.commit-outstanding` true: the source may have committed it
before the reply was lost.

<a id="trm-5-4-4-4"></a>

## Key creation

`lcs.audit.key.created` records a key a create made. Creating a key
checks only `KEY_CREATE_SUB_KEY` on its parent, so the parent's SACL
decides, by the rule that decides `lcs.audit.key.opened`: a success audit
ACE on the parent that matches the caller. <a id="cite-lcs-audit.key-created.on-parent-sacl-match"></a>

Only a key that was made is recorded. A create that found the key already
present and opened it instead writes nothing here. The record is written
once the key exists, or is staged in a transaction, so a create whose
handle then fails to reach the caller is still recorded. <a id="cite-lcs-audit.key-created.only-made-keys"></a>

It carries the caller summary; `object.kind`; the new key's
`object.key.guid`, `object.key.path` and `object.key.layer.name`;
`object.key.created` (true), `object.key.volatile`,
`object.key.volatile-requested` and `object.key.symlink`; the new key's
descriptor as `object.sd.length` and `object.sd.owner`; `access.requested`
(`KEY_CREATE_SUB_KEY`) and `access.granted`, from the parent check;
`transaction.id` when staged; and `outcome.success`. <a id="cite-lcs-audit.key-created.payload-fields"></a>

<a id="trm-5-4-4-5"></a>

## Descriptor changes

`lcs.audit.key.descriptor.changed` records `REG_IOC_SET_SECURITY` through
a key handle.

A change that includes the SACL is recorded whatever the handle's mask
says. It is recorded once the handle's own gate has admitted it, which
takes `ACCESS_SYSTEM_SECURITY`: a handle without that right is refused
first, and asking for a SACL change writes no record. <a id="cite-lcs-audit.descriptor-changed.sacl-change-always-recorded"></a>

Any other change is recorded when the right it needs — `WRITE_OWNER` for
the owner or group, `WRITE_DAC` for the DACL — overlaps the handle's
mask, and then failures are recorded as writes' are. <a id="cite-lcs-audit.descriptor-changed.other-changes-follow-mask"></a>

The record carries what a write record does, without a layer, and the
descriptors: `object.sd.components`, the `security_info` bits asked for;
and for the descriptor written and the one it replaced, `object.sd.length`
and `object.sd.length-previous`, their SHA-256 digests `object.sd.digest`
and `object.sd.digest-previous`, and their owners `object.sd.owner` and
`object.sd.owner-previous`. `access.requested` is every right the change
needs, and `access.matched` is zero when only the SACL made the record
exist. <a id="cite-lcs-audit.descriptor-changed.payload-fields"></a>

<a id="trm-5-4-4-6"></a>

## Privilege use on opens

A registry open whose access check used a privilege — `SeSecurityPrivilege`
for `ACCESS_SYSTEM_SECURITY`, `SeTakeOwnershipPrivilege` for
`WRITE_OWNER` — writes KACS's `kacs.audit.privilege.used` when the
caller's token audit policy asks for privilege use, in the shape KACS
uses for its own access checks, with `object.kind` `key`. The key's
identity is not carried. The checks LCS makes for layer writes and on a
create's parent record none. <a id="cite-lcs-audit.open.privilege-use-recorded"></a>

<a id="trm-5-4-4-7"></a>

## Backup and restore

`lcs.audit.backup.started` and `lcs.audit.restore.started` carry the
caller summary, `object.key.guid` for the subtree root, and
`operation.fd`, the descriptor the stream is written to or read from.

`lcs.audit.backup.ended` and `lcs.audit.restore.ended` carry the
caller summary, `object.key.guid` and `outcome.success`. When the
operation failed they also carry `outcome.errno`, the error as a
negative errno; on success it is absent.

<a id="trm-5-4-4-8"></a>

## Source validation failures

`lcs.source.response.rejected` carries the source slot as
`source.rsi.slot` and then, where each is known, the hive name as
`source.rsi.hive`, the RSI request id and operation code as
`request.id` and `request.op-code`, and the key GUID as
`object.key.guid`. <a id="cite-lcs-audit.validation-failure.payload-fields"></a> `outcome.reason` names what was wrong.
There are twelve:

`malformed-security-descriptor`, `malformed-layer-name`,
`unknown-rsi-status-code`, `future-sequence-number`,
`duplicate-winning-sequence-tie`,
`malformed-layer-metadata-security-descriptor`,
`malformed-key-name`, `malformed-value-name`,
`malformed-response-payload`, `malformed-key-metadata`,
`malformed-value-payload`, `malformed-delete-layer-orphan-list`. <a id="cite-lcs-audit.validation-failure.twelve-classes"></a>

The three name classes are field-specific: layer-name fields, key
component or child-name fields, and value-name fields respectively. <a id="cite-lcs-audit.validation-failure.name-classes"></a>

The structural classes cover a response whose operation-specific
payload has the wrong shape or trailing bytes; a lookup or
enumeration whose metadata block is incomplete, duplicated,
unreferenced or nil; a value payload with an invalid type, a
tombstone/data mismatch or oversized data; and an invalid orphan GUID
array from `RSI_DELETE_LAYER`. <a id="cite-lcs-audit.validation-failure.structural-classes"></a>

<a id="trm-5-4-4-9"></a>

## Configuration

`lcs.config.value.rejected` has the same shape as KMES's
`kmes.config.value.rejected`, with every field under one `config`
map. It carries the offending parameter's key and name as
`config.key.path` and `config.name`; the expected type and numeric
range as `config.expected.type`, `config.expected.min` and
`config.expected.max`; what was actually received as
`config.received.kind` — one of `missing`, `wrong-type` or
`out-of-range` — with `config.received.type` for a value of the wrong
type or `config.received.value` for one out of range; and, as
`config.value`, the value LCS retained instead. <a id="cite-lcs-audit.self-config.payload-fields"></a>

Because `missing` counts as invalid, a first boot before seed restore
emits one of these per parameter on each refresh: nineteen events
against an empty `Registry\` key. <a id="cite-lcs-audit.self-config.missing-counts-as-invalid"></a> That is correct and expected, but it
is a noticeable share of the boot audit stream.

<a id="trm-5-4-4-10"></a>

## What happens when emission fails

The policy differs per event, and the differences are the point.

- **`lcs.audit.key.opened`.** If LCS cannot *construct* a valid payload —
  corrupt internal state, allocation failure, anything on the LCS side
  — the open fails with `EIO` and no key fd is published. <a id="cite-lcs-audit.emit-failure.key-open-construct-failure-fails-the-open"></a> If the
  payload is valid but KMES cannot *retain* the event — unavailable,
  ring drops, capacity pressure, no consumer — the access decision and
  the fd publication are unaffected. Loss accounting is KMES's problem. <a id="cite-lcs-audit.emit-failure.key-open-retain-failure-is-harmless"></a>
- **`lcs.audit.backup.started`, `lcs.audit.restore.started`.** Emission
  failure returns `EIO` and the operation does not start. Nothing is
  read and nothing is written. <a id="cite-lcs-audit.emit-failure.start-events-block-the-operation"></a>
- **`lcs.audit.backup.ended`, `lcs.audit.restore.ended`.** The operation
  has already finished. Emission is attempted; failure does not change
  the result. <a id="cite-lcs-audit.emit-failure.complete-events-are-best-effort"></a>
- **`lcs.source.response.rejected`.** The triggering operation is
  already failing with `EIO`. Emission is attempted; failure does not
  change that. <a id="cite-lcs-audit.emit-failure.validation-failure-is-best-effort"></a>
- **`lcs.config.value.rejected`.** The invalid value has already been
  ignored and the previous known-good value retained. Emission is
  attempted; failure leaves the retained configuration in force. <a id="cite-lcs-audit.emit-failure.self-config-is-best-effort"></a>
- **The write, creation, descriptor-change and transaction records.**
  Each is written after the source has applied or refused the operation,
  or after the transaction's state is final. Emission is attempted; a
  record that cannot be built or retained leaves the caller's result as
  it was. <a id="cite-lcs-audit.emit-failure.write-records-preserve-result"></a>
  These records fire no `lcs:lcs_audit_emit` or `lcs:lcs_audit_emit_failed`
  tracepoint; the tracepoints' event-type codes cover the other seven.

The rule underneath them all: an audit failure blocks an operation only
where the audit record is the *point* of the operation being permitted.
A privileged bulk export whose start could not be recorded does not
happen. A key open whose decision could not be recorded does not
happen. Everything downstream of an already-determined outcome records
what it can.

LCS constructs the payload and attempts to enqueue it before
continuing past the audit point. It never waits for a userspace
consumer to observe or retain the event. <a id="cite-lcs-audit.enqueue-without-awaiting-a-consumer"></a>
