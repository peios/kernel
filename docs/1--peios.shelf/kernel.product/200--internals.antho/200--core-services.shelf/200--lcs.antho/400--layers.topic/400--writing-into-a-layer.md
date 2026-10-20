---
title: "Writing Into a Layer"
description: "Every mutation targeting a layer requires layer write access — the base layer before it exists, the precedence gate, and deleting a layer."
type: reference
---

<a id="trm-5-3-4"></a>

Every mutating operation that targets a layer — value writes, value
deletions, tombstones, key hides, blanket tombstones, key creation —
requires **layer write authorization**: `KEY_SET_VALUE` on the layer's
metadata key at `Machine\System\Registry\Layers\<LayerName>\`. <a id="cite-layer.authz.write-requires-key-set-value-on-metadata-key"></a>

This is a second AccessCheck, against a different object, and it is in
addition to the fd's granted mask on the target key. Both must pass. <a id="cite-layer.authz.is-a-second-check-additional-to-the-fd-mask"></a>

The descriptor on a layer's metadata key is therefore the answer to
"who may write into this layer". The base layer's, where the key has
been created, is the one inheritance computes from the `Machine` hive
root, like any other key's. <a id="cite-layer.authz.base-descriptor-inherits-from-the-machine-root"></a>
Group Policy layers get restrictive descriptors from the GP client at
creation; role layers get theirs from the role installer.

That closes two escalation paths at once. An unprivileged process
cannot write into a GP layer, and one role's service cannot write into
another role's.

The base layer is the one layer meant to be written by everybody. It
is where a write goes that names no layer, a person's own settings
under `Users\<SID>\` included, so its descriptor lets in anyone who has
authenticated and leaves what they may write to the descriptor of the
key they are writing. A layer check that refused them would make every
key read-only to everyone but SYSTEM and Administrators, whatever the
key's own descriptor said.

The layer metadata descriptors are cached alongside the layer table and
invalidated by the same self-watch ([Layer Metadata](<~kernel/internals/lcs/layers/layer-metadata#trm-5-3-3>)). A layer that is not in the
table is `ENOENT` for any operation naming it. <a id="cite-layer.authz.unknown-layer-is-enoent"></a>

<a id="trm-5-3-4-1"></a>

## The base layer before it exists

While `Layers\base\` does not exist, LCS falls back to a compiled-in
default descriptor, so base-layer writes work from the start. It is
owned by SYSTEM and grants `KEY_ALL_ACCESS` to SYSTEM and
Administrators and `KEY_SET_VALUE`, the one right this check asks for,
to Authenticated Users. Nobody else is granted anything: a principal
that has not authenticated cannot write into the base layer, whatever
the target key allows. <a id="cite-layer.authz.base-falls-back-to-a-compiled-in-descriptor"></a>

Nothing in a Peios system creates `Layers\base\`, so on a system as
shipped the compiled-in default is the descriptor in force for as long
as the system runs.

It is replaced by the persisted descriptor the moment the key is
created. <a id="cite-layer.authz.base-fallback-replaced-at-seed-restore"></a>

> [!WARNING]
> Creating `Layers\base\` changes who may write the registry. The new
> key inherits from the `Machine` hive root, which grants Authenticated
> Users `KEY_READ` and not `KEY_SET_VALUE`, so from that moment no
> ordinary principal can write anything, its own `Users\<SID>\`
> included. Whoever creates the key has to give it a descriptor that
> says what they mean, in the transaction that creates it.

<a id="trm-5-3-4-2"></a>

## Layer lifecycle

| Operation | Requirement |
|---|---|
| Create a layer at precedence 0 | `KEY_CREATE_SUB_KEY` on `Layers\` <a id="cite-layer.authz.create-requires-create-sub-key"></a> |
| Create a layer above precedence 0 | `KEY_CREATE_SUB_KEY` on `Layers\` **and** `SeTcbPrivilege` |
| Write into a layer | `KEY_SET_VALUE` on the layer's metadata key |
| Modify layer metadata | `KEY_SET_VALUE` on the metadata key; raising precedence above 0 additionally requires `SeTcbPrivilege` <a id="cite-layer.authz.modify-metadata-requires-key-set-value"></a> |
| Delete a layer | `DELETE` on the metadata key's fd <a id="cite-layer.authz.delete-requires-delete-on-the-metadata-fd"></a> |

Everything except the precedence rule is controlled purely by the
descriptor on the metadata key. <a id="cite-layer.authz.only-precedence-needs-a-privilege"></a>

<a id="trm-5-3-4-3"></a>

## The precedence gate

`SeTcbPrivilege` is required specifically to establish or raise a
layer's precedence above 0. <a id="cite-layer.authz.precedence-above-zero-requires-setcbprivilege"></a> It is defence in depth: compromising the
descriptor on `Layers\` is not enough to create a Group Policy-tier
layer.

The check is synchronous and inline at `REG_IOC_SET_VALUE` time, and it
happens early — before sequence allocation, before transaction
enlistment, before the source is contacted. <a id="cite-layer.authz.precedence-gate-runs-before-sequence-and-dispatch"></a>

It runs when three things hold: the target key is a layer metadata key,
the value name folds equal to `Precedence` under the same Unicode
folding used for every other value name, and the data is a positive
`REG_DWORD`. <a id="cite-layer.authz.precedence-gate-trigger-conditions"></a> A key
is a layer metadata key by its path — a direct child of
`Machine\System\Registry\Layers` — or by already being in the set of
published layer metadata keys. The path test is what covers the
recommended creation flow ([Layer Metadata](<~kernel/internals/lcs/layers/layer-metadata#trm-5-3-3>)), where `Precedence` is written inside
the transaction that creates the metadata key, before the layer has
been published at all. <a id="cite-layer.authz.precedence-gate-keys-on-the-path"></a>

Failing the privilege check is `EPERM`. <a id="cite-layer.authz.precedence-gate-denial-is-eperm"></a>

The gate tests for a four-byte `REG_DWORD` specifically. A `Precedence`
written with some other type slips past it — and then fails at the
refresh, which rejects a non-`REG_DWORD` `Precedence` as malformed
metadata. The precedence never actually rises. <a id="cite-layer.authz.non-dword-precedence-slips-the-gate-and-fails-at-refresh"></a>

`REG_IOC_RESTORE` has its own equivalent gate, applied to the backup
stream's layer manifest before anything is written ([Restore](<~kernel/internals/lcs/backup-and-restore/restore#trm-5-9-3>)).

<a id="trm-5-3-4-4"></a>

## Deleting a layer

Deleting the metadata key fires a `SUBKEY_DELETED` on the internal
self-watch. LCS removes the layer from the table and broadcasts
`RSI_DELETE_LAYER` to every registered source, each of which purges
every entry tagged with that name and reports the GUIDs that lost their
last path entry. <a id="cite-layer.authz.deleting-the-metadata-key-removes-the-layer-from-the-table"></a>

Before the broadcast, LCS aborts every bound transaction whose mutation
log touched that layer ([Deletion and Orphans](<~kernel/internals/lcs/data-model/deletion-and-orphans#trm-5-2-9>)).

A `SUBKEY_DELETED` for `base` is ignored ([The Base Layer](<~kernel/internals/lcs/layers/the-base-layer#trm-5-3-2>)).
