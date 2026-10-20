---
title: "Path Entries"
description: "Key existence and naming are layer-qualified while key identity is not — the per-layer path entry that separates them, and hiding."
type: reference
---

<a id="trm-5-2-5"></a>

Key existence and naming are layer-qualified; key identity is not. The
source stores a **path entry** per layer, which separates the two. <a id="cite-path-entry.existence-and-naming-are-layer-qualified"></a> The
overlay-filesystem analogy is exact: directory entries are per-layer,
inodes are shared.

| Field | Description |
|---|---|
| Parent GUID | The parent key. |
| Child name | The key's name under that parent — one component, not a path. <a id="cite-path-entry.field.child-name-is-one-component"></a> |
| Layer | The layer this entry belongs to. |
| Target | The GUID of the key at this path in this layer, or HIDDEN. <a id="cite-path-entry.field.target-is-a-guid-or-hidden"></a> |
| Sequence | A monotonic number assigned by LCS at creation, used for tiebreaking within a precedence tier. |

On the wire a HIDDEN entry is a target type of 1 with an all-zero GUID
([LCS ABI Reference](<~kernel/userspace/native/lcs/generated-syscall-and-common-abi#trm-5-a>)). <a id="cite-path-entry.hidden.wire-form-is-type-1-and-zero-guid"></a>

A source returning a non-zero GUID on a HIDDEN entry is returning
malformed data. <a id="cite-path-entry.hidden.non-zero-guid-is-malformed"></a>

<a id="trm-5-2-5-1"></a>

## Creating a key

Creating a key in a layer always assigns a fresh GUID and produces two
records: a path entry `(parent, name, layer) → GUID` with a new
sequence number, and a key record carrying that GUID. <a id="cite-path-entry.create.fresh-guid-and-two-records"></a>

LCS sends `RSI_CREATE_ENTRY` first and `RSI_CREATE_KEY`
second. <a id="cite-path-entry.create.entry-before-key"></a>

That order matters for the race: if another caller got there first, the
entry creation returns `RSI_ALREADY_EXISTS` and LCS retries the whole
thing as an open, reporting `REG_OPENED_EXISTING`. <a id="cite-path-entry.create.entry-already-exists-retries-as-open"></a> Failure on the
*second* call, for a GUID LCS just minted, is not a race and fails
closed ([Keys](<~kernel/internals/lcs/data-model/keys#trm-5-2-3>)).

If a different layer already has a key at that path, the new layer gets
its own distinct GUID. Each layer has its own key object, and
resolution decides which is visible. <a id="cite-path-entry.create.other-layer-gets-a-distinct-guid"></a>

**No operation creates a path entry pointing at an existing GUID.**
`reg_create_key` always mints a new one. The namespace is a tree, never
a graph. <a id="cite-path-entry.create.never-points-at-an-existing-guid"></a>

<a id="trm-5-2-5-2"></a>

## No GUID sharing across layers

The path table's shape would technically permit two entries referencing
one GUID, which would be a hard link. No API exposes it. <a id="cite-path-entry.no-hard-links.no-api-exposes-guid-sharing"></a>

Every key has exactly one canonical parent and name, and LCS validates
that a source is not reporting otherwise: the key record's parent must
be the parent the key was reached through, and its name must fold to the
component the key was reached by. A record that says otherwise is
malformed key metadata — `REG_IOC_QUERY_KEY_INFO` answers
`EIO` and the source-data validation failure is audited. <a id="cite-path-entry.no-hard-links.one-canonical-parent-and-name"></a>

Aliasing has an explicit, visible mechanism, and it is symlinks. Hard
links would make parent-GUID semantics, descriptor inheritance, subtree
enumeration and watch dispatch all ambiguous at once.

<a id="trm-5-2-5-3"></a>

## Hiding

A layer can create a HIDDEN entry at a path, making the key invisible
regardless of what lower-precedence layers say. <a id="cite-path-entry.hiding.hidden-entry-makes-a-key-invisible"></a>

It is the path-level equivalent of a value tombstone, and when the
hiding layer is removed the lower key reappears. <a id="cite-path-entry.hiding.removing-the-layer-restores-the-lower-key"></a>

A HIDDEN entry gets a sequence number like any other entry, so a
conflict between a GUID entry in one layer and a HIDDEN entry in
another at the same precedence resolves deterministically: the higher
sequence number wins. <a id="cite-path-entry.hiding.hidden-entry-carries-a-sequence-number"></a>

<a id="trm-5-2-5-4"></a>

## Hide and replace

A single layer can hide an existing key and put a new one at the same
path, and no special mechanism is needed for it. The layer creates its
own path entry pointing at its own new GUID; lower-precedence entries
for the same `(parent, name)` are masked because this layer's entry
wins on precedence. <a id="cite-path-entry.hide-and-replace.layer-entry-masks-lower-entries"></a>

Removing the layer removes both the new key and its masking effect, and
the lower key comes back. <a id="cite-path-entry.hide-and-replace.removing-the-layer-restores-the-lower-key"></a>

This falls out of per-layer path entries and precedence ordering
without a line of code that knows about it.

<a id="trm-5-2-5-5"></a>

## Hive roots

A hive root has no parent GUID and no child name, so there is no
`(parent, name, layer)` tuple to remove or mask. <a id="cite-path-entry.hive-root.has-no-parent-or-child-name"></a>

Deleting or hiding a hive root fd is `EINVAL`, rejected before source
dispatch, before transaction enlistment, before sequence allocation and
before any watch event is generated. <a id="cite-path-entry.hive-root.delete-or-hide-is-einval"></a>
