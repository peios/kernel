---
title: "Event families and delivery"
description: "The audit records KACS emits through KMES — the event families, their shared payload records, and how they are delivered."
type: reference
---

<a id="trm-3-c"></a>

KACS emits its audit records through KMES with origin class 2 ([Event Model](<~kernel/internals/kmes/event-model#trm-2-2>)). <a id="cite-audit-events.origin-class-two"></a>
Each event's payload is a msgpack map whose field paths follow PGSS
[Evaluation](<~kernel/internals/ntfe/evaluation#trm-6-4>): `access.requested` is the key `requested` inside the map under
`access`, never a key containing a dot, and a value the emitter does
not have is absent rather than nil. The shared `subject` group — the
effective token's `subject.token.*`, the PIP state in `subject.pip.*`,
and the calling process as `emitter.process.{pid,name,executable}` — is
attached at emission time from the resolved call context rather than by
the evaluation pipeline ([Auditing in AccessCheck](<~kernel/internals/kacs/access-check/auditing-in-accesscheck#trm-3-8-9>)). A process with no executable, such as a
kernel thread, has `executable` left out; the record is still written.

This appendix covers which events KACS emits and from where. The
field-by-field payload schemas are in the
[Peios Events Index](https://learn.peios.org/peios/using-peios/events/all-event-types), which is
canonical for them, and `evman <event-type>` prints each one.

<a id="trm-3-c-1"></a>

## Event families

| Event type | Emitted by |
|---|---|
| `kacs.audit.access.checked` | The SACL walk, and token audit-policy forcing. <a id="cite-audit-events.access-audit-record"></a> |
| `kacs.audit.handle.used` | Enforcement points, per operation, against a handle's continuous audit mask. <a id="cite-audit-events.continuous-audit-record"></a> |
| `kacs.audit.privilege.used` | Privilege-use auditing, for the five AccessCheck-influencing privileges in an access check, and at a Linux capability or volume gate ([The Privilege Model](<~kernel/internals/kacs/privileges/the-privilege-model#trm-3-4-1>)). <a id="cite-audit-events.privilege-use-record"></a> |
| `kacs.audit.descriptor.changed` | A change to the descriptor of a file, token, process or System V IPC object (below). |
| `kacs.impersonation.started`, `kacs.impersonation.reverted` | An impersonation attempt, and the end of an impersonation ([Impersonation Lifecycle](<~kernel/internals/kacs/impersonation/state-transitions#trm-3-5-3>)). |
| `kacs.caap.sacl.skipped`, `kacs.caap.staging.diverged` | A CAAP rule SACL that could not be parsed or evaluated; a staged result that differs from the effective one. <a id="cite-audit-events.caap-policy-diagnostic-record"></a> |
| `kacs.session.destroyed` | LogonSession teardown ([LogonSessions and Revocation](<~kernel/internals/kacs/tokens/logonsessions-and-revocation#trm-3-2-7>)). <a id="cite-audit-events.logon-session-destroyed-record"></a> |
| `kacs.descriptor.rejected` | A descriptor xattr that exists but fails structural validation ([File Descriptor Storage](<~kernel/internals/kacs/file-security/descriptor-storage-and-caching#trm-3-9-5>)). <a id="cite-audit-events.corrupt-sd-record"></a> |
| `kacs.caap.policy.changed` | `kacs_set_caap` installing, replacing or removing a central access policy ([Central Access and Auditing Policy](<~kernel/internals/kacs/access-check/central-access-and-auditing-policy#trm-3-8-8>)). |
| `kacs.mount.policy.changed` | `kacs_set_mount_policy` ([File Descriptor Storage](<~kernel/internals/kacs/file-security/descriptor-storage-and-caching#trm-3-9-5>)). |
| `kacs.config.value.rejected` | A port reservation table refused whole ([Port Reservations](<~kernel/internals/kacs/network-objects/port-reservations#trm-3-12-1>)). |
| `stratafs.file.copied-up` | StrataFS copy-up lifecycle and failure ([The StrataFS Copy-Up Context](<~kernel/internals/stratafs/security/kacs-admission-and-object-phases#trm-3-9-7>)). <a id="cite-audit-events.stratafs-copy-up-record"></a> |
| `stratafs.mutation.refused` | A StrataFS arrangement refusal. <a id="cite-audit-events.stratafs-mutation-refused-record"></a> |

`kacs.descriptor.rejected` carries `object.kind` `file` and
`outcome.reason` `corrupt`. It does not name the file by path: the
descriptor is read through internal path anchors whose mount cannot
always be resolved to an absolute path, so `object.file.path` is absent.
It names the file by `object.file.inode` and `object.file.device` (the
filesystem's `st_dev`) instead, carries the stored attribute's length as
`object.sd.length`, and carries the `subject` whose access made KACS read
the descriptor. <a id="cite-audit-events.corrupt-sd-identifies-file"></a>

KACS also writes `kacs.signature.crypto.failed` once at boot when the
signature transform is unavailable ([Binary Signature Verification](<~kernel/internals/kacs/executable-trust/signature-verification#trm-3-6>)), carrying
`signature.crypto-stage` `boot-probe` and the negative `outcome.errno`.

The `privilege.name` field of a `kacs.audit.privilege.used` event carries a canonical
name. A record of an access check (`operation.name` `access-check`)
names one of five — `SeSecurityPrivilege`, `SeTakeOwnershipPrivilege`,
`SeBackupPrivilege`, `SeRestorePrivilege` and `SeRelabelPrivilege` —
the only privileges an access check consults. <a id="cite-audit-events.privilege-five-canonical-names"></a>
A record of a capability or volume gate (`linux-cap`, `volume-mount`)
names whichever privilege the gate spent ([The Privilege Model](<~kernel/internals/kacs/privileges/the-privilege-model#trm-3-4-1>)). The encoder names
every defined privilege, and a bit with no name fails it closed rather
than emitting an unnamed privilege; a token holding only privileges an
access check does not consult produces no access-check record at all. <a id="cite-audit-events.privilege-encoder-fails-closed"></a>

`kacs.audit.handle.used` carries an `operation.name` naming the enforcement
point: `file.access`, `file.mmap`, `file.mprotect`, `file.permission`,
`file.write`, `file.ioctl`, `file.lock`, `file.fcntl`, `file.truncate`
and `file.fallocate`. <a id="cite-audit-events.continuous-operation-names"></a> It never carries a caller-supplied audit context: its
`object.kind` is always `file`, with the handle's absolute path in
`object.file.path` (absent only if the path cannot be resolved), and it
never sets `fields.attestation.userspace`. <a id="cite-audit-events.continuous-object-context-nil"></a>

<a id="trm-3-c-2"></a>

## Descriptor changes

`kacs.audit.descriptor.changed` records a change to the descriptor of a
file, a token, a process or a System V IPC object by a caller authorised
to make it, whether or not the change then applied. A change that
includes the SACL is always recorded, whatever either descriptor says —
so removing a file's SACL, which leaves nothing to audit the removal
itself, is still recorded. <a id="cite-audit-events.descriptor-changed-sacl-always"></a>
Any other change is recorded when the rights it needed overlap the alarm
mask on the handle it was made through. Only a file handle opened
through FACS carries such a mask, so a change made through a path, or to
a token, a process or an IPC object, is recorded only when it includes
the SACL. <a id="cite-audit-events.descriptor-changed-dacl-by-handle-mask"></a>

The record names the object by `object.kind` and its identity —
`object.file.path` where it can be resolved, `object.token.id` and
`.guid`, `object.process.guid`, or `object.ipc.type` and `.id` — and
describes the change in `object.sd`: the parts set as `components`, and
the length, SHA-256 digest and owner of the descriptor written
(`length`, `digest`, `owner`) and of the one replaced (`length-previous`,
`digest-previous`, `owner-previous`; absent where there was no stored
descriptor). `access.requested` is the rights the change needed, with the
handle's `access.granted`, `access.audit-mask` and the overlap as
`access.matched` — zero when only the SACL made the record exist — for a
change made through one. <a id="cite-audit-events.descriptor-changed-object-kinds"></a>
Registry keys have the same record as `lcs.audit.key.descriptor.changed`.

<a id="trm-3-c-3"></a>

## Delivery

Audit and privilege-use events are delivered **before** any result is
written back to the caller, and a delivery failure fails the syscall
with `EIO` or `EOPNOTSUPP`. <a id="cite-audit-events.delivered-before-result"></a> An audit event cannot be suppressed by
handing the call a bad output pointer.

Three emissions are best-effort by contrast, and drop silently rather
than failing the operation that caused them:

- `kacs.session.destroyed` where the authentication package name is
  not valid UTF-8. <a id="cite-audit-events.best-effort-logon-session-utf8"></a>
- The two StrataFS events on an over-long operation string or path. <a id="cite-audit-events.best-effort-stratafs"></a>
- Any self-emitted payload that would exceed its encoding buffer. <a id="cite-audit-events.best-effort-oversize-payload"></a>

A StrataFS record is not lost for want of memory. When the allocation
for the full record fails, a reduced record is written from a fixed
buffer instead: the same type with the stratum indices, the operation
and the outcome, and without the paths — `object.file.path-relative` and
each `stratum.path` — whose absence marks it as reduced. <a id="cite-audit-events.stratafs-reduced-record"></a>

The transport itself — ring buffer delivery, buffering and drop
accounting — is KMES's ([Ring Buffers](<~kernel/internals/kmes/ring-buffers#trm-2-5>), [Failure Modes](<~kernel/internals/kmes/failure-modes#trm-2-7>)).
