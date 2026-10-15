---
title: "Hives and Routing"
description: "A hive is the first component of every path — the routing table that maps hive names to sources, and the two names the kernel knows itself."
type: reference
---

<a id="trm-5-2-1"></a>

A hive is a top-level namespace — the first component of every registry
path. LCS keeps a routing table mapping hive names to registered
sources, and that table is built entirely from what registers. There is
no static configuration. <a id="cite-hive.routing-table.built-from-registrations"></a>

| Field | Description |
|---|---|
| Name | The hive name, e.g. `Machine`, `Users`. Case-preserving, compared case-insensitively. <a id="cite-hive.field.name-case-insensitive"></a> |
| Root GUID | The GUID of the hive's root key, supplied by the source at registration. <a id="cite-hive.field.root-guid-supplied-by-source"></a> |
| Source | The source slot backing this hive. |
| Status | Active or Unavailable, tracking source connectivity. <a id="cite-hive.field.status-active-or-unavailable"></a> |

Status is a property of the source slot rather than of the individual
hive, which amounts to the same thing: a slot's hives are exactly one
source's, and they go Down together. <a id="cite-hive.status-is-per-source-slot"></a>

<a id="trm-5-2-1-1"></a>

## Route identity

A hive route is identified by the pair **(case-folded name, scope)**,
where the scope is either the global namespace or one private scope
GUID. <a id="cite-hive.route-identity.name-and-scope"></a>

That pair must be unique across every registered source; a source
claiming one another source already holds is rejected. <a id="cite-hive.route-identity.must-be-unique"></a>

The same name may appear in different scopes, which is precisely how a
private hive shadows a global one without colliding with it. <a id="cite-hive.route-identity.same-name-in-different-scopes"></a>

A hive is backed by exactly one source. A source may back many. <a id="cite-hive.one-source-per-hive"></a>

<a id="trm-5-2-1-2"></a>

## Routing a path

LCS takes the first component of a path — everything before the first
separator — and looks it up. <a id="cite-hive.routing.uses-first-component"></a>

- Registered and active routes to the backing source. <a id="cite-hive.routing.active-routes-to-source"></a>
- Not registered is `ENOENT`. <a id="cite-hive.routing.unregistered-is-enoent"></a>
- Registered but Down is `EIO`. <a id="cite-hive.routing.down-is-eio"></a>

Before any source registers, the table is empty and every path yields
`ENOENT` ([The Bootstrap Problem](<~kernel/internals/lcs/bootstrap/dependencies-and-boot-sequence#trm-5-10-1>)).

<a id="trm-5-2-1-3"></a>

## `CurrentUser` is not a hive

`CurrentUser\` is a kernel-level alias. When a caller-supplied absolute
path starts with it, LCS reads the user SID from the calling thread's
effective token and rewrites the path to `Users\<SID>\...` before
routing. <a id="cite-hive.currentuser.rewrites-to-users-sid"></a>

The rewritten path is re-checked against the total-length limit, since
a textual SID is longer than the alias it replaced. <a id="cite-hive.currentuser.rewritten-path-rechecked-for-length"></a>

Three constraints keep this safe.

It applies **only to the first component** of a path, and only to a
caller-supplied absolute one. <a id="cite-hive.currentuser.first-component-of-caller-path-only"></a>

It does **not** apply to symlink targets: a target beginning with
`CurrentUser\` is followed literally, routes as a hive of that name,
and finds nothing. <a id="cite-hive.currentuser.not-applied-to-symlink-targets"></a> Without that rule, a symlink
containing `CurrentUser\` would redirect a privileged service into the
service's own user hive — a confused deputy.

And `CurrentUser` cannot be registered as a hive name. LCS rejects the
registration with `EINVAL`, so the alias can never collide with a real
hive. <a id="cite-hive.currentuser.cannot-be-registered-einval"></a>

Symlink targets *are* subject to ordinary hive routing, private hives
included. <a id="cite-hive.symlink-targets-use-ordinary-routing"></a> A sandboxed process resolving a symlink sees the same
registry through it that it sees directly, which is the point of
sandboxing it.

<a id="trm-5-2-1-4"></a>

## Two names the kernel knows

LCS is source-agnostic about routing but not entirely ignorant of
names. `Users` is compiled in as the target of `CurrentUser\`
rewriting. `Machine` is matched, case-insensitively and only for a
global hive, to decide when to run the bootstrap refresh that reads
LCS's own configuration ([The Boot Sequence](<~kernel/internals/lcs/bootstrap/dependencies-and-boot-sequence#trm-5-10-2>)).

Neither is a routing decision — an unregistered `Machine` routes
nowhere like any other name — but the two names do exist in the kernel. <a id="cite-hive.known-names.get-no-routing-privilege"></a>

In practice loregd registers `Machine` and `Users` at boot. Other
sources may register other hives at any time.

<a id="trm-5-2-1-5"></a>

## Names

Hive names follow the same rules as key name components: no backslash,
no forward slash, no null byte, valid UTF-8, non-empty, and no longer
than `MaxPathComponentLength`. <a id="cite-hive.name.follows-key-component-rules"></a> They are case-preserving and compared
case-insensitively ([Names and Case](<~kernel/internals/lcs/data-model/names-and-case#trm-5-2-8>)).
