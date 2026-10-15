---
title: "Symlinks"
description: "The two load-bearing mechanisms behind a symlink key — the structural flag and the target value — plus resolution, depth and opening the link itself."
type: reference
---

<a id="trm-5-2-4"></a>

A symlink key uses two mechanisms, and both are load-bearing.

The **symlink flag** on the key record marks the key's structural type.
It is set at creation by `REG_OPTION_CREATE_LINK` and is immutable
afterwards. <a id="cite-symlink.flag.set-at-creation-and-immutable"></a>

`RSI_WRITE_KEY` can update only the descriptor and the last write time,
so there is no operation that could change it. <a id="cite-symlink.flag.rsi-write-key-cannot-change-it"></a>

The **default value, of type `REG_LINK`,** supplies the target
path. <a id="cite-symlink.target.is-the-reg-link-default-value"></a>

It is an ordinary layered value, which means a higher-precedence layer
can redirect a symlink by writing a different `REG_LINK` default value,
and removing that layer restores the original target. <a id="cite-symlink.target.layer-can-redirect-and-revert"></a>

The flag marks identity; the value provides the target.

<a id="trm-5-2-4-1"></a>

## Resolution

LCS follows symlinks during path resolution and the fd it returns
refers to the resolved target — its GUID, its position in the tree, its
ancestor chain — not to the link. <a id="cite-symlink.resolution.fd-refers-to-the-target"></a>

The target is resolved by issuing a separate `RSI_QUERY_VALUES` for the
key's default value (the empty name) and applying ordinary layer
resolution to the result, so the target participates in the layer
system exactly as any other value does. <a id="cite-symlink.resolution.target-read-with-layer-resolution"></a>

If the effective default value is missing, or is not of type
`REG_LINK`, resolution fails with `EINVAL`. <a id="cite-symlink.resolution.missing-or-wrong-type-is-einval"></a>

LCS does **not** validate the type at write time: a layer that writes a
`REG_SZ` default value over a symlink's target breaks resolution at the
next open, and removing that layer fixes it. <a id="cite-symlink.resolution.target-type-not-validated-at-write-time"></a>

The offending value stays in the registry; a failed resolution writes
nothing. <a id="cite-symlink.resolution.failed-resolution-writes-nothing"></a>

<a id="trm-5-2-4-2"></a>

## The target path

The `REG_LINK` payload is a length-delimited UTF-8 registry path. No
trailing null is required or permitted — the length delimits it, and a
null byte inside that length is rejected like any
other. <a id="cite-symlink.target-path.length-delimited-no-trailing-null"></a> Forward
slashes are handled as separators as everywhere else.

The target is validated with exactly the same rules as a syscall path:
UTF-8, no null bytes, per-component and total length, no empty
components, no trailing separator, maximum depth. <a id="cite-symlink.target-path.validated-like-a-syscall-path"></a> The only difference
is that a syscall path arrives null-terminated and has its terminator
stripped first.

A target is always interpreted as absolute — its first component is
routed as a hive name. <a id="cite-symlink.target-path.always-absolute"></a>

Resolution has no check that rejects a relative-looking target as
malformed. A target of `Sub\Key` is not an error; it is a request for a
hive named `Sub`, and it yields `ENOENT` unless such a hive happens to
be registered, in which case it resolves there. <a id="cite-symlink.target-path.relative-looking-target-not-rejected"></a>

Writing one is different. `REG_IOC_SET_VALUE` of a `REG_LINK` value
routes the target's first component at write time, with the writer's
scope GUIDs, and answers `EINVAL` if it names no registered hive. That
is what stops a dangling target being captured later by whoever
registers a private hive of that name: a target that cannot be written
cannot be captured, and the failure lands on whoever authored it. The
cost is that a symlink cannot forward-reference a hive registered after
it. A target that arrives in source data or a backup stream is not
gated, which is why resolution still has to treat the shape as a hive
request. <a id="cite-symlink.target-path.write-time-routing-gate"></a>

`CurrentUser\` rewriting is not applied ([Hives and Routing](<~kernel/internals/lcs/data-model/hives-and-routing#trm-5-2-1>)), so a target beginning
with `CurrentUser\` routes as a hive of that name and cannot be
registered, and therefore always fails. Ordinary hive routing does
apply, private hives included, for the resolving thread.

<a id="trm-5-2-4-3"></a>

## Depth

Symlink resolution is bounded by `SymlinkDepthLimit`, default 16,
configurable from 1 to 64. Exceeding it is `ELOOP`. <a id="cite-symlink.depth.exceeding-the-limit-is-eloop"></a>

<a id="trm-5-2-4-4"></a>

## Opening the link itself

`REG_OPEN_LINK` on `reg_open_key` opens the symlink key rather than
following it, which is how a symlink is managed at all — deleted,
retargeted, inspected. <a id="cite-symlink.open-link.opens-the-link-not-the-target"></a>

It applies to the **final path component only**. A symlink encountered
part-way along a path is followed whether or not the flag is
set. <a id="cite-symlink.open-link.final-component-only"></a>

The access check follows the same rule: with `REG_OPEN_LINK` the check
is against the link, otherwise against the target. <a id="cite-symlink.open-link.access-check-follows-the-flag"></a>

<a id="trm-5-2-4-5"></a>

## Creation

Creating a symlink needs all of:

- `KEY_CREATE_SUB_KEY` on the parent, as for any key; <a id="cite-symlink.create.requires-key-create-sub-key"></a>
- `KEY_CREATE_LINK` on the parent; <a id="cite-symlink.create.requires-key-create-link"></a>
- either an enabled `SeTcbPrivilege` or membership of Administrators. <a id="cite-symlink.create.requires-setcbprivilege-or-administrators"></a>

The last is a genuine disjunction — either satisfies it — and the
privilege branch marks the privilege used. <a id="cite-symlink.create.privilege-branch-marks-privilege-used"></a>

Failing it is `EPERM`. <a id="cite-symlink.create.failure-is-eperm"></a>
