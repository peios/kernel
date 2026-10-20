---
title: "Token Lifecycle"
description: "How tokens follow a process through fork, clone and exec — NEW_PROCESS_MIN, self-installation, bootstrap tokens and external tokens."
type: reference
---

<a id="trm-3-2-3"></a>

<a id="trm-3-2-3-1"></a>

## Fork and clone

Every process and thread creation path goes through `clone()`, and
KACS branches on `CLONE_THREAD`.

**Without `CLONE_THREAD`** — fork or vfork — a new process is created
and the child receives an independent deep copy of the parent's
primary token. <a id="cite-token.fork.independent-copy"></a> If the parent is impersonating, the impersonation token
is not inherited: the child's effective credential is set from
`real_cred`. <a id="cite-token.fork.impersonation-not-inherited"></a> After the fork, mutations to either token are invisible
to the other. <a id="cite-token.fork.mutations-invisible-after"></a>

**With `CLONE_THREAD`** a new thread is created. Threads share the
parent's `real_cred` by reference and therefore share one primary
token object, so a privilege adjustment on it is visible to every
thread. <a id="cite-token.thread.shared-primary"></a> Each thread keeps independent impersonation state through its
own `cred`. <a id="cite-token.thread.independent-impersonation"></a> If the cloning thread is impersonating at the moment of
the clone, the impersonation token does not become the new thread's
primary or effective identity — the new thread starts with the shared
primary token as both, and may impersonate independently later. <a id="cite-token.thread.clone-starts-on-primary"></a>

<a id="trm-3-2-3-2"></a>

## Exec

The primary token survives `execve()` unchanged, with the single
exception of `NEW_PROCESS_MIN` below. <a id="cite-token.exec.primary-survives"></a> If the calling thread is
impersonating, impersonation is reverted before the new program runs;
a new program always starts with the primary token as its effective
identity. <a id="cite-token.exec.reverts-impersonation"></a>

Token assignment for services happens between fork and exec: peinit
forks, installs the service's token on the child, and the child then
execs the service binary.

<a id="trm-3-2-3-2-1"></a>

### NEW_PROCESS_MIN <a id="cite-token.new-process-min"></a>

When a token's `mandatory_policy` includes `NEW_PROCESS_MIN`, the
kernel replaces the primary token at exec time if the executable
carries an explicit, lower integrity label.

1. The executable's integrity label is read from the mandatory label
   ACE in its descriptor's SACL. A file with no label — no SACL, or no
   non-inherit-only mandatory label ACE — is **unlabelled**, and the
   token survives exec unchanged. <a id="cite-token.new-process-min.unlabelled-unchanged"></a> This is deliberately not the
   access-check rule, under which an unlabelled *object* counts as
   Medium ([Mandatory Integrity Control](<~kernel/internals/kacs/access-check/mandatory-integrity-control#trm-3-8-3>)): an image that labels nothing would otherwise demote
   every process on it, PID 1 first, to Medium — which is exactly what
   happened before PEI-530, leaving the TCB below every High-integrity
   user and unable to convey their identity.
2. If the file's level is lower than the token's, a new token is
   created following DuplicateToken semantics — new `token_id`, new
   `token_guid`, `modified_id` initialised to the new `token_id`,
   `elevation_type` reset to Default — with `integrity_level` set to
   the file's label. Every other field — the impersonation level
   included — is copied from the source, and the original token is
   dropped. <a id="cite-token.new-process-min.lowers-to-file-label"></a>
3. If the file's level is greater than or equal to the token's,
   nothing happens and the token survives exec unchanged. <a id="cite-token.new-process-min.higher-label-unchanged"></a>

The mechanism only ever lowers integrity, so a child's level is always
at most its parent's, and only to a level the image itself claims. The
flag itself is immutable on the token, which is what prevents a process
from opting out before exec.

<a id="trm-3-2-3-3"></a>

## Self-installing a primary token

`KACS_IOC_INSTALL` commits a new primary token on the calling process.
The operation is process-wide: the kernel replaces the primary token
for the entire thread group, not just the calling thread. <a id="cite-token.install.process-wide"></a>

The handle has to carry `TOKEN_ASSIGN_PRIMARY`, the token has to be a
primary token, and the caller's *real* token has to hold
`SeAssignPrimaryTokenPrivilege` enabled — an impersonating thread's
effective token does not satisfy the gate, and the privilege is marked
used on success. <a id="cite-token.install.gates"></a> Unless that real token also
holds `SeTcbPrivilege` enabled, the token being installed has to carry
the same user SID and the same LogonSession as the caller's, or the
call fails with `EPERM`; this is what stops a non-TCB holder of
`SeAssignPrimaryTokenPrivilege` from installing an arbitrary
higher-privilege token on itself, and `SeTcbPrivilege` bypassing it is
how peinit installs service tokens with a different user SID and
LogonSession. <a id="cite-token.install.same-user-same-session-unless-tcb"></a>

A thread that is not impersonating switches both `real_cred` and
`cred` to the new primary token. A thread that is impersonating has
only `real_cred` replaced, and its active impersonation stays in
`cred` until it reverts or execs — so reverting after an install
restores the thread to the *new* primary token, not the old one. <a id="cite-token.install.impersonating-thread-keeps-cred"></a>

The calling thread installs immediately. Sibling threads converge in
their own context through queued in-kernel credential work, with no
atomic all-threads-at-once swap: during a brief transition window some
siblings may still observe the old primary token until they run their
queued work. <a id="cite-token.install.siblings-converge-asynchronously"></a> No completion barrier is exposed to the caller.

Successful installations are ordered per process. Siblings converge to the
latest successful installation in that order; older queued work must not
restore a superseded token, including when retried after an allocation
failure. Concurrent callers need not complete their syscalls in installation
order. Once exec commits its primary token, delayed pre-exec installation
work cannot replace it. <a id="cite-token.install.latest-successful-install-wins"></a>

Installation and exec credential preparation are serialised. If a successful
installation precedes exec, an execing sibling whose queued update has not
run derives its new primary token from that latest installation, applying
`NEW_PROCESS_MIN` normally. It does not derive from the sibling's stale
primary token, and does not replay the raw installed token over the derived
result afterward. If exec has already begun preparing credentials, a new
installer waits for exec to release its credential guard; a waiting sibling
remains killable so exec can finish removing the other threads. A failed
exec releases the guard without consuming a pending installation.
<a id="cite-token.install.serialized-with-exec"></a>

Such an exec also gives the new image the installed token's Linux
credentials, projected as an installation projects them ([Credential Projection](<~kernel/internals/security/credentials#trm-3-10-1>)): uid, gid,
supplementary groups and user come from the installed token, not from the
token it replaced. A setuid or setgid binary's effective ID then applies on
top as it would to any exec. Unless the thread is impersonating, the
installed token is also the subject that decides whether that ID change is
allowed. <a id="cite-token.install.lagging-exec-takes-installed-identity"></a>

A new thread joins the same convergence rule even if it was not yet visible
when an installation selected the siblings to update. This does not change
a process fork's independent copy of the calling thread's primary token.
<a id="cite-token.install.clone-enrollment"></a>

If the installed token's user SID differs from the outgoing primary
token's, the process security descriptor is regenerated from the
default template for the new token. Otherwise the existing process
descriptor is preserved. <a id="cite-token.install.process-sd-regenerated-on-sid-change"></a>

<a id="trm-3-2-3-4"></a>

## Bootstrap tokens

Two tokens are created by PKM during kernel initialisation, before any
userspace process exists. Neither involves a syscall — the kernel
allocates the objects directly.

The **SYSTEM token** is hardcoded with user SID `S-1-5-18` (Local
System); groups `S-1-5-32-544` (BUILTIN\Administrators), `S-1-1-0`
(Everyone), `S-1-5-11` (Authenticated Users) and other well-known
SIDs; every defined privilege present and enabled; integrity level
System; token type Primary; impersonation level Delegation, the top of
the ratchet; elevation type Default; token source `PeiosKrn`;
projected UID 0; and `auth_id` set to `SYSTEM_LUID`. It is assigned to
the kernel's init task and inherited by PID 1 at exec. <a id="cite-token.bootstrap.system-token"></a>
Its `audit_policy` is `PRIVILEGE_USE_SUCCESS`, so every privilege SYSTEM
spends — at a capability gate and in an access check — is recorded as
`kacs.audit.privilege.used` ([The Privilege Model](<~kernel/internals/kacs/privileges/the-privilege-model#trm-3-4-1>)), and tokens derived from it carry the
same policy. <a id="cite-token.bootstrap.system-token-audits-privilege-use"></a> The Anonymous
token and the query-only SYSTEM token have an audit policy of 0.

The **Anonymous token** is a global singleton with user SID `S-1-5-7`;
Everyone (`S-1-1-0`) as its only group; no privileges; integrity level
Untrusted; logon type Network; token type Impersonation; impersonation
level Anonymous; elevation type Default; token source `PeiosKrn`; and
`auth_id` set to `ANONYMOUS_LOGON_LUID`. It is effectively immutable,
having no privileges and no groups to adjust. <a id="cite-token.bootstrap.anonymous-token"></a> A peer token captured
at Anonymous level references this global object, whereas
`KACS_IOC_DUPLICATE` targeting Anonymous level creates a fresh
independent token of the same shape, because the DuplicateToken
contract requires a new object. <a id="cite-token.bootstrap.anonymous-singleton-vs-duplicate"></a>

| LUID | Value | Description |
|---|---|---|
| `SYSTEM_LUID` | 999 (0x3E7) | The SYSTEM LogonSession, created at kernel init. |
| `ANONYMOUS_LOGON_LUID` | 998 (0x3E6) | The Anonymous LogonSession, created at kernel init for Anonymous impersonation tokens. |

LogonSessions created dynamically by authd receive auto-generated
LUIDs starting at 1000; 999 and 998 are never assigned dynamically. <a id="cite-token.bootstrap.reserved-luids"></a>

The SYSTEM token carries `SeBackupPrivilege` and `SeRestorePrivilege`
present and enabled at boot. <a id="cite-token.bootstrap.system-backup-restore-present"></a> FACS passes backup and restore intent
flags into AccessCheck, which grants read and write regardless of file
DACLs — subject still to PIP. <a id="cite-token.bootstrap.backup-restore-intent-bypasses-dacl"></a> Once peinit has launched the TCB
services and early boot is complete, it disables these on child
service tokens through FilterToken.

<a id="trm-3-2-3-5"></a>

## External token replacement

A privileged process being able to replace the primary token on
another running process — peinit downgrading a pre-authd service from
SYSTEM to a purpose-built token, for instance — is designed but **not
built**. Nothing in the kernel implements it today. <a id="cite-token.external-replacement-not-built"></a>

The design uses `task_work_add()` to queue a credential swap on each
task in the target thread group, each task executing the swap in its
own context to preserve RCU safety, with an impersonating thread
having only `real_cred` replaced and its impersonation left intact.
The gates would be `SeAssignPrimaryTokenPrivilege` on the caller's
real token, `TOKEN_ASSIGN_PRIMARY` (0x0001) on the token fd,
`PROCESS_SET_INFORMATION` on the target process's descriptor, and two
constraints — the new token's user SID matching the target's current
one, and the new token belonging to the same LogonSession — both
bypassed by `SeTcbPrivilege`. The process descriptor gate puts the
target's owner in control of who can change its identity, while the
SID and LogonSession constraints stop a non-TCB holder of
`SeAssignPrimaryTokenPrivilege` assigning an arbitrary token to a
process it can reach. `SeTcbPrivilege` bypassing both is how peinit
would assign tokens with different user SIDs and LogonSessions to
child services. Per-thread queuing would leave a brief window with
some threads on the new token and some on the old, which is acceptable
only because replacement is always a downgrade.

In its absence, the mitigation for pre-authd services is privilege
removal: peinit uses FilterToken to copy the SYSTEM token with the
dangerous privileges permanently deleted and assigns that filtered
token to the service at launch. The service keeps the SYSTEM SID but
permanently lacks the ability to exercise those privileges.
