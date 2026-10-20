---
title: "The Base Layer"
description: "The kernel-reserved layer that exists unconditionally before any source registers — its persisted metadata and the two ways it is matched."
type: reference
---

<a id="trm-5-3-2"></a>

The base layer, named `base`, is a kernel-reserved implicit layer. It
exists unconditionally, before any source registers and whether or not
any metadata has ever been persisted for it. <a id="cite-layer.base.exists-unconditionally"></a>

It is a static constant in the kernel: precedence 0, enabled. <a id="cite-layer.base.is-precedence-zero-and-enabled"></a> It is
never stored in the dynamic layer table. <a id="cite-layer.base.not-in-the-dynamic-layer-table"></a>

It is always emitted first in every layer snapshot, and is handed out
even when the dynamic table is empty. <a id="cite-layer.base.emitted-first-in-every-snapshot"></a> A source that registers with a
completely empty database is therefore immediately usable, because the
one layer that writes need is not in the database.

Four things cannot happen to it:

- it cannot be deleted; <a id="cite-layer.base.cannot-be-deleted"></a>
- it cannot be disabled; <a id="cite-layer.base.cannot-be-disabled"></a>
- its precedence cannot be changed; <a id="cite-layer.base.precedence-cannot-be-changed"></a>
- a layer table row for it cannot be published at all. <a id="cite-layer.base.row-cannot-be-published"></a>

Each of those is enforced in more than one place. Deletion is refused by
the layer table, by the resolution core, by the `RSI_DELETE_LAYER`
dispatch path, and by the transaction layer-abort path. Publication of a
`base` row is rejected outright, and the refresh path short-circuits for
`base` **before** it would read `Precedence` or `Enabled`, so persisted
values for those are never even consulted.

<a id="trm-5-3-2-1"></a>

## Persisted metadata

`Machine\System\Registry\Layers\base\` may exist, though nothing in a
Peios system creates it, and where it does it decorates the base layer
rather than defining it. What LCS takes
from it is the metadata key's GUID and its cached Security Descriptor —
which is to say, who may write into the base layer ([Writing Into a Layer](<~kernel/internals/lcs/layers/writing-into-a-layer#trm-5-3-4>)). <a id="cite-layer.base.metadata-key-supplies-guid-and-descriptor"></a>

Its `Precedence` and `Enabled` values are ignored. <a id="cite-layer.base.persisted-precedence-and-enabled-ignored"></a>

The internal self-watch also ignores a `SUBKEY_DELETED` for `base`: if a
higher-precedence HIDDEN entry masks the base layer's metadata key, that
is not a layer deletion and is not processed as one. <a id="cite-layer.base.subkey-deleted-is-ignored"></a> The base layer's
existence is hardcoded and layer mechanics cannot reach it.

<a id="trm-5-3-2-2"></a>

## The default target

A write that names no layer targets the base layer. <a id="cite-layer.base.is-the-default-write-target"></a> That is the default
for manual administration, for system initialisation, and for what a
person keeps under their own `Users\<SID>\`.

While the base layer's metadata key does not exist, LCS uses a
compiled-in default descriptor granting SYSTEM and Administrators
`KEY_ALL_ACCESS` and Authenticated Users `KEY_SET_VALUE`, so writes into
the base layer are possible from the very beginning, by anyone who has
authenticated, to whatever the target key's own descriptor lets them
write. The compiled-in default is replaced by the key's descriptor as
soon as the key is created ([Writing Into a Layer](<~kernel/internals/lcs/layers/writing-into-a-layer#trm-5-3-4>)).

<a id="trm-5-3-2-3"></a>

## `base` is matched like every other layer name <a id="cite-layer.base.name-matched-by-case-folding"></a>

The reserved name is recognised with Unicode Simple Case Folding, the
same algorithm and the same table used for every other layer-name
comparison.

There was a second, ASCII case-insensitive comparator beside it, used on
two call sites. For the literal string `base` the two agreed — a length
pre-check made a non-ASCII case pair fail before folding could matter —
so the divergence was latent rather than absent, and would have become
live the moment anything about the reserved name changed. It is gone;
both call sites now take the folding comparator and propagate its error
rather than collapsing it into a `bool`.
