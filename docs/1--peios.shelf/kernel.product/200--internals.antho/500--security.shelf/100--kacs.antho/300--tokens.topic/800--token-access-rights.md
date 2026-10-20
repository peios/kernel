---
title: "Token Access Rights"
description: "Tokens are securable objects — obtaining a token file descriptor, the token-specific rights, the generic mapping and the default descriptor."
type: reference
---

<a id="trm-3-2-8"></a>

Tokens are securable objects: each has its own security descriptor,
and reaching a token means passing an AccessCheck against it. <a id="cite-token.rights.access-checked-object"></a>

<a id="trm-3-2-8-1"></a>

## Obtaining a token file descriptor

**Opening directly.** A syscall takes a pidfd — not a raw PID — and a
desired access mask. The kernel finds the target's
primary token, evaluates the caller's token against that token's
descriptor, and returns a token fd with the granted mask cached on it. <a id="cite-token.rights.open-by-pidfd"></a>
A separate variant opens a thread's impersonation token. <a id="cite-token.rights.open-thread-token"></a> Opening
another process's token additionally requires
`PROCESS_QUERY_INFORMATION` on the target process's descriptor. <a id="cite-token.rights.open-other-needs-process-query"></a>

**Opening through `/proc`.** `/proc/<pid>/token` and
`/proc/<pid>/task/<tid>/token` open a process's primary token and a
thread's effective token as a query-only handle: the fd always carries
`TOKEN_QUERY` and nothing else. Opening another process's file makes
both of the syscall's checks — `PROCESS_QUERY_INFORMATION` on the
process's descriptor, with PIP dominance, and `TOKEN_QUERY` on the
token's own descriptor — so the path reads nothing the syscall would
refuse. A process opens its own without either check. <a id="cite-token.rights.proc-token-file"></a>

The peer-token socket option (`getsockopt(SOL_KACS,
KACS_SO_PEER_TOKEN)`) is the exception: it takes no desired-access
mask, and the fd it returns always carries the fixed rights
`TOKEN_QUERY | TOKEN_IMPERSONATE | TOKEN_DUPLICATE`. <a id="cite-token.rights.peer-token-fixed-rights"></a> A token delivered
in a `KACS_SCM_TOKEN` control message carries the same three. <a id="cite-token.rights.scm-token-fixed-rights"></a>
`TOKEN_DUPLICATE` is what lets a server turn a client's identity into a
primary token for a process it launches on the client's behalf
([Token Creation](<~kernel/internals/kacs/tokens/token-creation#trm-3-2-4>)); it is safe to hand out because the level ratchet means the
copy can never act above the level the client chose ([Impersonation Levels](<~kernel/internals/kacs/impersonation/levels-and-admission#trm-3-5-1>)).

**Receiving over IPC.** A token fd can be passed over a Unix socket
with `SCM_RIGHTS`. What the recipient may do is bounded by the mask
cached on the fd when it was originally opened, not by the recipient's
own identity. <a id="cite-token.rights.passed-fd-keeps-cached-mask"></a>

**Implicit self-access.** A thread has implicit access to its own
effective token for query operations, but this is not a kernel bypass.
It follows from the default token descriptor, which grants
`TOKEN_QUERY` and the adjustment rights to the token's own user SID.
The AccessCheck still runs; it simply succeeds while the descriptor
continues to grant the right. Explicitly mutating a token's own
descriptor later can revoke self-query by removing that grant. <a id="cite-token.rights.self-query-revocable"></a>

<a id="trm-3-2-8-2"></a>

## Token-specific rights

| Right | Value | Grants |
|---|---|---|
| `TOKEN_ASSIGN_PRIMARY` | 0x0001 | Install as a process's primary token. Also requires `SeAssignPrimaryTokenPrivilege` on the caller's token. <a id="cite-token.rights.assign-primary-needs-privilege"></a> |
| `TOKEN_DUPLICATE` | 0x0002 | Duplicate the token, or create a restricted copy with FilterToken. |
| `TOKEN_IMPERSONATE` | 0x0004 | Install as a thread's impersonation token. |
| `TOKEN_QUERY` | 0x0008 | Read token information: SIDs, groups, privileges, integrity, claims, source, statistics, GUID, elevation type. |
| `TOKEN_ADJUST_PRIVILEGES` | 0x0020 | Enable, disable, or permanently remove privileges. |
| `TOKEN_ADJUST_GROUPS` | 0x0040 | Enable or disable groups. |
| `TOKEN_ADJUST_DEFAULT` | 0x0080 | Change the default DACL, owner SID, and primary group SID. |
| `TOKEN_ADJUST_INTERACTIVITY_SCOPE` | 0x0100 | Change the interactivity scope. Also requires `SeTcbPrivilege`. |

Bit 0x0010, `TOKEN_QUERY_SOURCE`, is subsumed by `TOKEN_QUERY`: a
holder of 0x0008 can query source information too. <a id="cite-token.rights.query-source-subsumed"></a> The bit is not
reused for anything else, for format compatibility with MS-DTYP.

`TOKEN_ALL_ACCESS` is 0x000F01FF — the union of the token-specific
rights with `STANDARD_RIGHTS_REQUIRED`
(`DELETE | READ_CONTROL | WRITE_DAC | WRITE_OWNER`, 0x000F0000). The
named rights alone OR to 0x01EF; the reserved `TOKEN_QUERY_SOURCE` bit
adds 0x0010 to reach 0x01FF. <a id="cite-token.rights.all-access-value"></a>

<a id="trm-3-2-8-3"></a>

## Generic mapping <a id="cite-token.rights.generic-mapping"></a>

| Generic right | Maps to |
|---|---|
| `GENERIC_READ` | `TOKEN_QUERY \| READ_CONTROL` |
| `GENERIC_WRITE` | `TOKEN_ADJUST_PRIVILEGES \| TOKEN_ADJUST_GROUPS \| TOKEN_ADJUST_DEFAULT \| WRITE_DAC` |
| `GENERIC_EXECUTE` | `TOKEN_IMPERSONATE` |
| `GENERIC_ALL` | `TOKEN_ALL_ACCESS` (0x000F01FF) |

<a id="trm-3-2-8-4"></a>

## Standard rights

`READ_CONTROL` reads the token's own descriptor, `WRITE_DAC` modifies
its DACL, and `WRITE_OWNER` changes its owner. `DELETE` has no
practical effect on a token and is present only for uniformity across
standard rights. <a id="cite-token.rights.delete-inert"></a>

<a id="trm-3-2-8-5"></a>

## The default token descriptor <a id="cite-token.rights.default-descriptor"></a>

A newly created token receives a descriptor owned by the creating
process's user SID, with a DACL granting:

- the token's own user SID `TOKEN_QUERY | TOKEN_ADJUST_PRIVILEGES |
  TOKEN_ADJUST_GROUPS | TOKEN_ADJUST_DEFAULT`;
- the creator `TOKEN_ALL_ACCESS`;
- SYSTEM (`S-1-5-18`) `TOKEN_ALL_ACCESS`;
- Administrators (`S-1-5-32-544`) `TOKEN_QUERY`.

The Administrators grant is read-only: it lets an administrator see who
any process runs as, its groups and privileges, and which logon session
it belongs to, which is what a machine-wide process listing needs.
Duplicating, impersonating, adjusting or rewriting the token still
needs the token's own grants. <a id="cite-token.rights.default-sd-administrators-query"></a>

Self-access is deliberately limited to the adjustment operations that
cannot escalate. `TOKEN_DUPLICATE`, `TOKEN_IMPERSONATE`, and
`WRITE_DAC` are not granted to the token's own subject. <a id="cite-token.rights.default-sd-no-self-escalation"></a>

That limit needs protecting in the case where the creator and the
token's own user SID are the same, which would otherwise hand the
subject `TOKEN_ALL_ACCESS` through the creator ACE. When the two SIDs
are identical the creator ACE is omitted — and the descriptor also
gains a non-inherit-only `OWNER RIGHTS` ACE suppressing the owner's
implicit `READ_CONTROL | WRITE_DAC` grant while preserving
`READ_CONTROL`. <a id="cite-token.rights.default-sd-self-created-owner-rights"></a> Without it, owner-implicit `WRITE_DAC` would let the
subject rewrite its own DACL and reintroduce exactly the escalation
that omitting the creator ACE was meant to close.

<a id="trm-3-2-8-6"></a>

## Check-at-open

The check-at-open model applies to tokens exactly as it does to files,
for the token-specific rights. AccessCheck runs once, when the token
fd is obtained; the granted mask is cached on the fd; and each of the
token ioctls verifies against that cached mask with no re-evaluation. <a id="cite-token.rights.check-at-open"></a>

The standard rights are the exception. Reading and writing a token's
own descriptor passes no cached mask at all and runs a **live**
AccessCheck on every call, so `READ_CONTROL`, `WRITE_DAC` and
`WRITE_OWNER` are re-evaluated per operation rather than snapshotted
at open. <a id="cite-token.rights.standard-rights-live-check"></a> A descriptor change therefore takes effect immediately for
those three rights, while already-opened handles keep their cached
token-specific rights.
