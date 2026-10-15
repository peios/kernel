---
title: "State transitions"
description: "State transitions: behaviour and implementation of the Peios kernel."
type: reference
---

<a id="trm-3-5-3"></a>

<a id="trm-3-5-3-1"></a>

## The sequence

**The client connects.** It optionally sets the maximum impersonation
level on the socket with `setsockopt(SOL_KACS,
KACS_SO_IMPERSONATION_LEVEL)` — the default is Impersonation; the
option may be changed at any time and bounds every capture made from
then on — and calls `connect()`. <a id="cite-imp.capture.level-changeable-bounds-later-captures"></a> The kernel's LSM hook fires on the
Unix stream connection.

**Identity is captured, both ways.** The hook examines the client
thread's effective credential together with the socket's maximum
level, derives the identity at the lower of that level and the
effective token's own ([Impersonation Levels](<~kernel/internals/kacs/impersonation/levels-and-admission#trm-3-5-1>)), and stores the result on the accepted
end. It also stores, on
the connecting end, the identity the listener captured when `listen()`
was called — so a client can read `KACS_SO_PEER_TOKEN` on its own
socket immediately after `connect()` and verify who it reached, at
Identification level unless the listener set its own level. <a id="cite-imp.capture.listener-identity-to-connecting-end"></a> The
listener's identity is what `listen()` saw; a process that inherits a
listener it did not create (from a descriptor store after a restart,
or from a broker) replaces it with its own using `setsockopt(SOL_KACS,
KACS_SO_RESTAMP)`, which is self-gated and fails with `EINVAL` on a
socket that is not listening. <a id="cite-imp.restamp.listening-socket-only"></a> Clients that connect before the restamp
see the previous holder, which is honest: that is who was listening. <a id="cite-imp.restamp.not-retroactive"></a>
Squatting a name therefore buys nothing against a client that checks —
the squatter's own identity is what it conveys. At
Anonymous, a token whose user SID is `S-1-5-7`, whose enabled groups
include Everyone, and which does not carry Authenticated Users is
stored on the socket's LSM blob, and the client's real identity is
never recorded. <a id="cite-imp.capture.anonymous-records-no-real-identity"></a> At Impersonation or Delegation, the thread's effective
token is stored — and if the connecting thread is itself
impersonating, the impersonated identity is what flows through, which
is how identity cascades across local services. <a id="cite-imp.capture.stores-effective-token"></a> At Identification, the
effective token is stored but tagged at that level.

**The server reads the peer token** with `getsockopt(SOL_KACS,
KACS_SO_PEER_TOKEN)` on the accepted connection, which opens a token fd
carrying `TOKEN_QUERY | TOKEN_IMPERSONATE | TOKEN_DUPLICATE` for the
identity in that
end's conveyed-identity register — at this point, the identity captured
at connect (see *Per-message identity* below for how the register
moves). <a id="cite-imp.peer-token.fd-access-mask"></a>
**It impersonates** by installing that fd with `KACS_IOC_IMPERSONATE`:
the kernel evaluates both gates against the server thread's primary
token, computes the effective level, and constructs a new credential
carrying the impersonation token at that level. libpeios fuses the
two steps as `peios_token_impersonate_peer` for the handler that
impersonates, works and reverts on one thread.

**Access control follows the impersonation token.** Every subsequent
AccessCheck on the thread evaluates it, and MIC uses its integrity
level. PIP continues to read the PSB, unchanged.

**The server reverts** with `kacs_revert()`, restoring the thread's
credential to `real_cred` and its service identity with it. <a id="cite-imp.revert.restores-real-cred"></a>

<a id="trm-3-5-3-2"></a>

## Anonymous

Any thread may impersonate the Anonymous identity without passing
either gate. <a id="cite-imp.anonymous.no-gates"></a> Assuming Anonymous is always a downgrade — the token has
no access beyond what is explicitly granted to `S-1-5-7` or Everyone —
so no privilege is needed, no identity gate runs, and no integrity
ceiling applies.

Anonymous tokens carry the Anonymous SID as the user SID, no
privileges, and Untrusted integrity. The socket path constructs that
minimal shape rather than preserving any part of the caller's real
identity. <a id="cite-imp.anonymous.socket-constructs-minimal-shape"></a>

<a id="trm-3-5-3-3"></a>

## Double impersonation <a id="cite-imp.double.revert-then-reimpersonate"></a>

A thread already impersonating that installs another token with
`KACS_IOC_IMPERSONATE` causes the kernel to revert internally and then
re-impersonate.
Because the gates are evaluated against the primary token, the
previous impersonation has no bearing on the new one.

<a id="trm-3-5-3-4"></a>

## Interaction with MIC and PIP

**MIC reads the effective token** for tokens permitted to act, which
is safe precisely because the integrity ceiling makes acting
impersonation safe. <a id="cite-imp.mic.reads-effective-token"></a> A thread cannot act at Impersonation or Delegation
level with a client token whose integrity exceeds the server primary
token's. When the ceiling caps the level to Identification, the
installed token may still preserve the client's literal label as
metadata, but it authorizes no resource access because
Identification-level tokens are barred from AccessCheck. An acting
impersonation token therefore preserves or lowers the server's
integrity, and a higher literal label can only ever exist on a
non-acting Identification-level token.

**PIP reads the PSB**, because there is no equivalent ceiling for it. <a id="cite-imp.pip.reads-psb-not-effective-token"></a>
PIP operates on `pip_type` and `pip_trust`, which are orthogonal to
integrity level. Reading them from the effective token would let a
process impersonate a token carrying higher PIP values and acquire
protection it has not earned.

<a id="trm-3-5-3-5"></a>

## SeImpersonatePrivilege

The privilege permits a service to impersonate arbitrary clients —
those with different user SIDs. Without it a process can impersonate
only tokens matching its own user SID and restriction status.

It is checked against the server's primary token, so a thread already
impersonating one client is judged on its real service identity. It
has to be enabled at the moment of the call. And it bypasses the
identity gate only, never the integrity ceiling.

<a id="trm-3-5-3-9"></a>

## Audit records

Every `KACS_IOC_IMPERSONATE` writes a `kacs.impersonation.started`
record through KMES ([Audit Event Schemas](<~kernel/internals/kacs/auditing/event-families-and-delivery#trm-3-c>)). Its subject is the server's token, the one
that acted, and its object is the client token: `object.token.sid`,
`.type`, `.integrity`, `.auth-id` and `.restricted`, with the level the
client token offered as `object.token.impersonation` and the level the
gate allowed as `object.token.impersonation-permitted`. The thread that
took the identity on is `emitter.thread.tid`, since impersonation is per
thread. Where the gate needed `SeImpersonatePrivilege` and used it, the
record carries `privilege.name` and `privilege.held`. <a id="cite-imp.audit.started-record"></a>

A level the gate lowered is not a failure: the record says
`outcome.success` with `impersonation-permitted` below
`impersonation`. A lowered level installs a new token, and the record's
`object.token.guid` and `object.token.id` are always the installed
token's — the client's own when the level was not lowered, the new one
when it was — so they match the header of the records the thread writes
next. <a id="cite-imp.audit.started-permitted-level"></a>

A refused impersonation is recorded too, with `outcome.errno` and, where
the kernel knows why, `outcome.reason`: `primary-token` for a primary
token (`EINVAL`), `restriction-escape` for a restricted server reaching
for an unrestricted token of its own user (`EPERM`),
`no-impersonate-access` for a handle without `TOKEN_IMPERSONATE`
(`EACCES`), and `projection-failed` when the identity could not be
projected onto the thread's credentials. A refusal before the gate
answered carries no `impersonation-permitted`. <a id="cite-imp.audit.started-records-refusals"></a>

Ending an impersonation writes `kacs.impersonation.reverted`, a
`verbose` type, so only where the emission policy ([Emission Policy](<~kernel/internals/kmes/emission-policy#trm-2-8>)) switches it on.
The record names the
token given up in `object.token.guid` and `object.token.sid`, with the
thread's token after the revert as subject. `operation.name` says why:
`revert` for `kacs_revert`, `exec` for the revert every exec performs,
and `replaced` when a second impersonation ends the first. A revert with
no impersonation in force writes nothing, nor does the revert and
re-apply around a primary-token install, which leaves the impersonation
in place, nor does a thread that exits while impersonating. <a id="cite-imp.audit.reverted-record"></a>
Both records are best effort: a record that cannot be built does not
change the outcome of the impersonation or the revert.

## Related explanations

- [Transport and per-message identity](<~kernel/internals/kacs/impersonation/transport-and-per-message-identity>)
