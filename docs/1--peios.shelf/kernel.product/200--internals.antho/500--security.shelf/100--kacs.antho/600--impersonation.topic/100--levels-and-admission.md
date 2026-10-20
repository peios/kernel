---
title: "Levels and admission"
description: "The four levels at which a server thread may assume a client's identity, and what each permits."
type: reference
---

<a id="trm-3-5-1"></a>

Impersonation lets a server thread temporarily assume a client's
identity, so that access control decisions on that thread evaluate the
client's token instead of the server's.

The client controls how far its identity can travel by setting an
impersonation level on the connection before it is established, and
the server cannot escalate beyond the level the client chose. There is
no API that bypasses that choice.

**Anonymous.** The server cannot identify the caller at all. The
connection carries no identity information: both token inspection and
impersonation yield a token whose user SID is Anonymous (`S-1-5-7`),
which carries Everyone as an enabled group and does not carry
Authenticated Users. <a id="cite-imp.anonymous.no-identity-conveyed"></a>

**Identification.** The server can identify the caller — read SIDs,
query groups, inspect privileges — but cannot act as them. An
Identification-level token is barred from AccessCheck against
resources: a server thread impersonating one and attempting to open a
file simply fails the check, with `EACCES` — the same refusal the
`kacs_access_check` syscall reports for that token. <a id="cite-imp.identification.barred-from-accesscheck"></a>

**Impersonation.** The server can act as the caller for all local
operations, including ones that cross local IPC boundaries. If service
A impersonates client B at this level and connects to local service C,
C sees B's identity — identity cascades freely across local services. <a id="cite-imp.impersonation.cascades-across-local-services"></a>
This is the default.

**Delegation.** Locally identical to Impersonation. The distinction
activates at the network boundary, where a Delegation-level token
carries authorization for the server to forward the client's identity
to services on other machines through Kerberos. <a id="cite-imp.delegation.network-boundary-only"></a> KACS enforces the
level; authd is what acts on it.

The level is set by the client through a KACS syscall on the socket
before `connect()`, and defaults to Impersonation. <a id="cite-imp.level.socket-default-impersonation"></a>

<a id="trm-3-5-1-1"></a>

## The level is a ratchet <a id="cite-imp.level.ratchet-only-down"></a>

Every token carries an impersonation level, and on every token it
means the same thing: *identity derived from this token may act at no
more than this level*. An impersonation token acts at its level. A
primary token's level is the ceiling on everything the process
carrying it can convey — what a peer captures at connect, what
`KACS_SO_PASS_TOKEN` attaches, what `KACS_IOC_DUPLICATE` produces in
either direction. <a id="cite-imp.level.primary-is-conveyance-ceiling"></a>

The level only ever goes down:

- Socket capture and `KACS_SCM_TOKEN` attach store the lower of the
  socket's level and the source token's own; <a id="cite-imp.level.capture-takes-lower"></a>
- DuplicateToken refuses a result above its source, whatever the types
  involved;
- fork, exec, `NEW_PROCESS_MIN`, FilterToken and primary installation
  copy it unchanged. <a id="cite-imp.level.derivation-copies-unchanged"></a>

The one way to a higher level is a fresh token from CreateToken, which
takes `SeCreateTokenPrivilege`. <a id="cite-imp.level.raise-only-via-create-token"></a> authd mints logon tokens at Delegation
and the bootstrap SYSTEM token is Delegation, so an identity starts at
the top and each hop can only lower it.

This is what makes the client's choice hold across any number of
hops and process boundaries. A client that connects at Impersonation
is captured at Impersonation; a server that converts that token to a
primary and launches a process with it ([Token Creation](<~kernel/internals/kacs/tokens/token-creation#trm-3-2-4>)) produces a process
capped at Impersonation; and nothing that process captures, conveys
or duplicates can ever be Delegation — so authd, which reads the
level to decide whether to forward the client's credentials, is never
shown a Delegation flag the client did not grant. <a id="cite-imp.level.holds-across-hops"></a>

<a id="trm-3-5-2"></a>

When a server thread attempts to impersonate a client's token, two
independent checks decide whether it proceeds at the requested level.
Both have to pass. If either fails the effective level is reduced to
Identification — the movement is only ever downward.

Both gates are evaluated against the server's **primary token**
(`real_cred`), never its effective token. <a id="cite-imp.gate.evaluated-against-primary-token"></a> A server already
impersonating another client has its gates judged against its own
service identity, so a previous impersonation cannot influence the
next one.

<a id="trm-3-5-2-1"></a>

## The identity gate

The identity gate asks whether this server may impersonate this
particular user's identity. Impersonation at Impersonation or
Delegation level is permitted if either of two conditions holds.

**Same user, same restriction status** — the server's primary token
and the client's token carry the same user SID, and both are
restricted or both unrestricted. <a id="cite-imp.gate.same-user-same-restriction"></a>

**`SeImpersonatePrivilege`** — the server's primary token holds it,
enabled. <a id="cite-imp.gate.impersonate-privilege-enabled"></a>

If neither holds, the level is **silently capped to Identification**. <a id="cite-imp.gate.identity-failure-caps-silently"></a>
No error is returned: the call succeeds, and the resulting token is
merely at Identification level.

There is one hard denial. A **restricted** server impersonating an
**unrestricted** client of the same user is rejected outright with
`-EPERM` rather than capped, because that is precisely how a sandboxed
process would escape by impersonating its parent's unrestricted token. <a id="cite-imp.gate.restricted-to-unrestricted-eperm"></a>
The reverse direction, unrestricted server to restricted client, is a
harmless downgrade and takes the ordinary cap-to-Identification path. <a id="cite-imp.gate.unrestricted-to-restricted-caps"></a>

MS-DTYP includes a third condition — an origin LogonSession check
letting the session that created a token impersonate it without the
privilege. KACS drops it. A service needing to impersonate a different
user holds `SeImpersonatePrivilege`, and there are no hidden paths.

<a id="trm-3-5-2-2"></a>

## The integrity ceiling <a id="cite-imp.gate.integrity-ceiling"></a>

The integrity ceiling asks whether the client's token sits at an
integrity level the server is allowed to assume. To act at
Impersonation or Delegation level, the client token's integrity level
has to be less than or equal to the server primary token's. A
Medium-integrity server can impersonate Low or Medium clients; against
a High-integrity client the level caps to Identification.

The installed token may keep the client's literal integrity label as
identity metadata after the cap, but that preserved label authorizes
nothing, because Identification-level tokens are barred from
AccessCheck entirely. <a id="cite-imp.gate.capped-token-keeps-label"></a>

The ceiling exists because MIC evaluates the *effective* token's
integrity level for tokens that can act. Without it, a server could
impersonate a higher-integrity token and gain write access to
higher-integrity objects — integrity escalation through impersonation.

The ceiling is enforced unconditionally, regardless of privilege.
`SeImpersonatePrivilege` bypasses the identity gate and never the
ceiling. <a id="cite-imp.gate.privilege-never-bypasses-ceiling"></a> MS-DTYP allows the privilege to bypass every check including
this one; KACS does not, because `mandatory_policy` is immutable here
([Token Structure](<~kernel/internals/kacs/tokens/token-structure#trm-3-2-2>)) and MIC is consequently a real boundary. Letting a privilege
punch through would give back exactly what that immutability buys.

<a id="trm-3-5-2-3"></a>

## Composition <a id="cite-imp.gate.composition-minimum"></a>

The two gates are independent, both are evaluated, and the effective
level is the minimum any constraint permits: start from the level the
client set on the socket, cap to Identification if the identity gate
fails, cap to Identification if the integrity ceiling fails, and the
result is the effective impersonation level.
