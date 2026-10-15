---
title: "LogonSessions and Revocation"
description: "The LUID-identified object every token references — how sessions are created, how they expire, and how revocation propagates."
type: reference
---

<a id="trm-3-2-7"></a>

<a id="trm-3-2-7-1"></a>

## LogonSessions

A LogonSession is a lightweight kernel object identified by a LUID,
carried on tokens as `auth_id`. Every token references one.

authd creates a LogonSession through a KACS syscall at authentication
time, before creating the token. <a id="cite-token.session.created-before-token"></a> The object holds the LogonSession ID,
the logon type (Interactive, Network, Service, and so on), the user
SID, the authentication package name such as `Kerberos` or
`Negotiate`, and a creation timestamp. <a id="cite-token.session.fields"></a> The logon SID, `S-1-5-5-X-Y`,
is derived from the LogonSession ID. Several tokens may share one
session — linked pairs, and tokens derived by duplication. <a id="cite-token.session.shared-by-many-tokens"></a>

When the last token referencing a session is freed, the kernel
destroys the session object and emits a `kacs.session.destroyed`
event through KMES. <a id="cite-token.session.destroyed-with-last-token"></a> The last
token usually goes when a credential is freed, which happens in an RCU
callback where no record can be built, so the session is queued, still
referenced, and a kernel work item writes the event moments later and
then releases it. The session is gone at once — it no longer resolves —
but its event follows the teardown rather than coming from it, and its
header names the kernel worker that wrote it. <a id="cite-token.session.destroyed-record-deferred"></a> The event is for whatever keeps per-session state
outside the kernel — an audit pipeline, an accounting tool, an authority
that caches credentials per session. authd keeps none and does not
subscribe.

The record describes the session under `object.session`: its LUID as
`id` (the `subject.token.auth-id` of every record made under it), the
user SID as `user.sid`, the logon type as `logon-type`, the
authentication package as `auth-package`, and the creation time as
`logon-time`. The logon type is written by name — `interactive`,
`network`, `batch`, `service`, `network-cleartext`, `new-credentials`
or `remote-interactive` — and the time in realtime nanoseconds, though
the kernel holds it to whole seconds.

There is one rollback path for the case where authd creates a session
but no token ever becomes live for it:
`kacs_destroy_empty_logon_session`, which requires `SeTcbPrivilege`
and succeeds only when the session exists, has zero live tokens, has
no linked-token state, and has no other in-flight kernel references. <a id="cite-token.session.destroy-empty.gates"></a>
On success it destroys the object and emits the same
`kacs.session.destroyed` event as normal cleanup. <a id="cite-token.session.destroy-empty.emits-event"></a> A nonexistent
session fails with `-ENOENT`; one with any live token, linked-token
state, or in-flight reference fails with `-EBUSY`. <a id="cite-token.session.destroy-empty.errors"></a>

A second enumeration surface exists alongside `/proc`:
`/sys/kernel/security/kacs/sessions` lists every live session, one
line each, giving the session ID, user SID, logon type, authentication
package, and creation time. <a id="cite-token.session.securityfs-listing"></a> Each
line reads

```
logon_session_id=<u64> user_sid=<hex> logon_type=<u32> auth_package=<hex> created_at=<u64>
```

with the user SID's binary form and the package name's bytes in
lowercase hexadecimal, and `created_at` in seconds since the Unix
epoch. securityfs itself is unclassified by FACS,
so its objects sit deny-missing until the mount is given a synthesising
policy ([File Descriptor Storage](<~kernel/internals/kacs/file-security/descriptor-storage-and-caching#trm-3-9-5>)); only then can the file be opened at all. On Peios,
peinit gives it one at boot that lets Authenticated Users open and
traverse. Reading it is access-checked against a
synthetic descriptor granting read to SYSTEM and Administrators, and is
PIP-checked. <a id="cite-token.session.securityfs-access-check"></a>

AccessCheck never consults `auth_id`, and the logon SID influences a
decision only because it is materialised as an ordinary group SID on
the token. <a id="cite-token.session.auth-id-not-consulted"></a> Two enforcement decisions elsewhere in the kernel do read
session state, though. Installing a primary token denies a non-TCB
caller whose target token belongs to a different
LogonSession ([Token Lifecycle](<~kernel/internals/kacs/tokens/token-lifecycle#trm-3-2-3>)). And the
`CAP_SYS_BOOT` mapping selects between `SeShutdownPrivilege` and
`SeRemoteShutdownPrivilege` by inspecting the session's logon type
([Credential Projection](<~kernel/internals/security/credentials#trm-3-10-1>)). `interactivity_scope` is metadata in the same way: the kernel
stores it and returns it on query, and no kernel security mechanism
evaluates it.

<a id="trm-3-2-7-2"></a>

## Expiration

The `expiration` field carries a timestamp, and AccessCheck does not
enforce it. It is informational.

Token lifetime is governed by reference counting instead: a token
exists as long as at least one reference — a process credential or an
open file descriptor — exists. <a id="cite-token.session.lifetime-by-refcount"></a>

<a id="trm-3-2-7-3"></a>

## Revocation

KACS has no token revocation primitive. There is no "invalidate token
X" syscall, and no syscall destroys a LogonSession while tokens still
reference it. <a id="cite-token.session.no-revocation-primitive"></a> `kacs_destroy_empty_logon_session` is only authd's
rollback for a session that never acquired live tokens.

Terminating a LogonSession is therefore userspace coordination. On
Peios authd does it, when asked over `/run/logon.sock` ([PGSS session termination](https://learn.peios.org/peios/advanced-peios/pgss/logon/ending-a-session)):

1. A caller asks authd to end the session, and authd decides whether it
   may: its own session as a person, anyone else's by an access check
   against local policy. SYSTEM's session (999), Anonymous's (998) and
   every session of logon type Service are never ended this way; a
   service is stopped through peinit.
2. authd enumerates processes whose **primary** token carries the
   target `auth_id`, by walking `/proc`, opening each process with
   `pidfd_open`, opening its primary token with
   `kacs_open_process_token` on that pidfd, and reading
   `TokenStatistics`, which includes `auth_id`. No dedicated enumeration
   syscall exists or is needed. A thread's impersonation token is not
   consulted, so a service impersonating a member of the session is not
   one of its processes.
3. authd sends each `SIGTERM` with `pidfd_send_signal`, waits up to a
   grace period (5 seconds) for them to exit, and sends `SIGKILL` to the
   survivors.
4. It walks again, since a process may have forked meanwhile, for at
   most three rounds.
5. The processes terminate, dropping their token references.
6. The last reference drops and the session object is cleaned up.

Each token handle authd opens in the walk is itself a reference to the
session, and is closed as soon as `auth_id` has been read.

Token file descriptors can be passed between processes over IPC, so a
reference held by a process outside the target session survives that
session's process termination. <a id="cite-token.session.fd-reference-survives-termination"></a> The walk finds processes running under the
session, not every process holding one of its tokens, so such a
reference keeps the session alive after authd has ended every process
in it, and authd reports nothing about it. A process that has exited
but not been reaped likewise keeps its token, and the session, until it
is reaped.

Kernel-side invalidation — a dead flag on the LogonSession object
checked during AccessCheck, so that access checks against its tokens
fail immediately — is not implemented.
