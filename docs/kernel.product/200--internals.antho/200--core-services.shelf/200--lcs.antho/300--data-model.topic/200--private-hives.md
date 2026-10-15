---
title: "Private Hives"
description: "Hives invisible in the global namespace, reachable only through a scope GUID on the calling token — routing, lifecycle and registration rules."
type: reference
---

<a id="trm-5-2-2"></a>

A private hive is registered with the `RSI_HIVE_PRIVATE` flag and a
scope GUID. <a id="cite-private-hive.registered-with-flag-and-scope-guid"></a>

It is invisible in the global namespace and reachable only by a thread
whose token carries that scope GUID. <a id="cite-private-hive.invisible-globally-and-scope-gated"></a>

<a id="trm-5-2-2-1"></a>

## Routing

Private hives are checked **before** global ones. <a id="cite-private-hive.routing.checked-before-global"></a>

For each scope GUID on the calling thread's token, in the order the
token carries them, LCS looks for a private hive with the path's name
and that scope. The first match wins. Only if none matches is the
global table consulted. <a id="cite-private-hive.routing.token-order-first-match-wins"></a>

A private hive can therefore shadow a global one, and no name is exempt
— a thread with a private `Machine\` sees the private one. <a id="cite-private-hive.routing.shadows-any-global-name"></a> That is what
makes complete registry isolation possible for a container or a
sandbox without giving it a differently-named hive to notice.

`MaxScopeGUIDsPerToken`, default 8, bounds the per-syscall iteration
cost; a token above the cap fails every registry operation with `E2BIG`
([Private Layers](<~kernel/internals/lcs/layers/private-layers#trm-5-3-5>)). <a id="cite-private-hive.scope.max-guids-per-token"></a> Duplicate scope GUIDs on a token are rejected.

<a id="trm-5-2-2-2"></a>

## Scope GUIDs on a token

Scope GUIDs reach a thread through the KACS token's LCS credential
extension: a versioned block in the token specification carrying the
thread's scope GUIDs and its private layer names ([Private Layers](<~kernel/internals/lcs/layers/private-layers#trm-5-3-5>)). It parses at
a fixed offset, and:

- rejects a nil scope GUID; <a id="cite-private-hive.credential.rejects-nil-guid"></a>
- rejects duplicate scope GUIDs; <a id="cite-private-hive.credential.rejects-duplicate-guids"></a>
- caps the count at 256 — a hard KACS limit, above the configurable
  LCS one. <a id="cite-private-hive.credential.caps-count-at-256"></a>

The credentials propagate across fork, duplication and impersonation
like the rest of the token. <a id="cite-private-hive.credential.propagates-across-fork-and-impersonation"></a>

Attaching them is gated by `SeCreateTokenPrivilege`, because scope
GUIDs can only enter a token when the token is created. <a id="cite-private-hive.scope.attaching-gated-by-secreatetokenprivilege"></a> That is a
blanket privilege rather than a per-scope authorisation: a caller that
can create tokens at all can create one claiming any scope. Isolation
between private hives therefore rests on who may create tokens, not on
who owns a scope.

<a id="trm-5-2-2-3"></a>

## Scope lifecycle

A scope GUID is an opaque 128-bit value with no lifecycle. LCS neither
creates nor tracks one; it only compares. <a id="cite-private-hive.scope.opaque-and-untracked-by-lcs"></a> A scope exists as long as
some private hive or some token references it, and when the last
reference goes it is simply a number nobody uses.

Nothing in the kernel generates scope GUIDs. <a id="cite-private-hive.scope.not-generated-by-kernel"></a> Key GUIDs and token GUIDs
come from the kernel's UUIDv4 generator; scope GUIDs are supplied by
userspace, and choosing them unpredictably is userspace's
responsibility.

<a id="trm-5-2-2-4"></a>

## Registration rules

Registration enforces more than the route-identity uniqueness of
[Hives and Routing](<~kernel/internals/lcs/data-model/hives-and-routing#trm-5-2-1>) — the full list is [Registration and Slots](<~kernel/internals/lcs/sources/registration-and-slots#trm-5-8-2>), and the rules that exist for private
hives are these:

- A hive's root GUID may not be nil.
- The root GUIDs within one registration request must be
  distinct.
- A hive without the `RSI_HIVE_PRIVATE` flag may not carry a non-nil
  scope GUID.
- A hive **with** the flag may not carry a nil one. <a id="cite-private-hive.registration.private-hive-requires-scope-guid"></a> No token
  can carry a nil scope GUID, so such a hive would be registrable and
  then permanently unroutable — holding its name against other sources
  in that scope while every lookup returned `ENOENT`.
- Unknown flag bits are rejected.
- Opening `/dev/pkm_registry` at all requires an **enabled**
  `SeTcbPrivilege`, checked in the device's `open()` handler
  ([Registration and Slots](<~kernel/internals/lcs/sources/registration-and-slots#trm-5-8-2>)).
