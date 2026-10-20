---
title: "Tombstones"
description: "An overlay that can only add is not enough — value and blanket tombstones, how they compete, and what a watcher sees."
type: reference
---

<a id="trm-5-2-7"></a>

An overlay that can only add is not enough. `registry.pol` expresses
*absence* — `**Del.ValueName` deletes a specific value,
`**DelVals` deletes every value in a key before applying new ones — and
a higher-precedence layer that can only override cannot say "this value
must not be configured". Tombstones are how absence is expressed.

Both kinds are per-layer, and both vanish with their layer, restoring
whatever they were masking. <a id="cite-tombstone.per-layer-and-vanish-with-the-layer"></a>

<a id="trm-5-2-7-1"></a>

## Value tombstones

A value tombstone is a layer entry that says the value does not exist
in this layer and lower-precedence layers are masked. <a id="cite-tombstone.value.masks-lower-precedence-layers"></a>

Resolution treats a winning tombstone as "not found" without falling
through. <a id="cite-tombstone.value.winning-tombstone-does-not-fall-through"></a>

In the source's storage it is an entry of type `REG_TOMBSTONE` with no
data. A caller who wins with one gets `ENOENT`.

Removing the tombstone's layer makes the lower-precedence value
effective again, which is the whole point.

<a id="trm-5-2-7-2"></a>

## Blanket tombstones

A blanket tombstone is a per-layer marker on a **key** that masks every
value from lower-precedence layers, whatever its name. <a id="cite-tombstone.blanket.masks-every-value-name"></a>

Where a value tombstone names one value, a blanket names none and
covers all — including values whose names were not known when the
blanket was written, which is exactly what `**DelVals`
requires. <a id="cite-tombstone.blanket.covers-names-unknown-when-written"></a>

It is stored as a flag on the `(key GUID, layer)` relationship and
occupies no per-name entry. It has its own sequence
number. <a id="cite-tombstone.blanket.stored-as-a-flag-with-its-own-sequence"></a>

<a id="trm-5-2-7-2-1"></a>

### How it competes

A blanket does not short-circuit resolution. It enters the candidate
pool as a tombstone candidate **for every value name**, at its own
`(precedence, sequence)`, <a id="cite-tombstone.blanket.enters-the-candidate-pool-for-every-name"></a> and the ordinary rule picks the winner
([Resolution](<~kernel/internals/lcs/layers/resolution#trm-5-3-6>)).

So a per-value entry that beats the blanket on the tuple overrides it,
and one that loses is masked. <a id="cite-tombstone.blanket.per-value-entry-wins-or-loses-on-the-tuple"></a>

A layer can write a blanket *and* write specific values in the same
layer: the specific values are visible because they were written
afterwards and carry higher sequence numbers, and everything else from
below is masked. <a id="cite-tombstone.blanket.same-layer-writes-after-a-blanket-stay-visible"></a> That is `**DelVals` followed by new writes,
expressed without a special case.

An exact tie — same precedence *and* same sequence — between a blanket
and a per-value entry is not resolved in the blanket's favour or
anyone's. It is malformed source data and the operation fails with
`EIO` ([Resolution](<~kernel/internals/lcs/layers/resolution#trm-5-3-6>)).

<a id="trm-5-2-7-2-2"></a>

### Enumeration

Enumerating a key with a blanket applies the same per-name rule to each
name, so what a caller sees is the set of names whose winning candidate
is not the blanket. <a id="cite-tombstone.blanket.enumeration-applies-the-per-name-rule"></a>

It is not simply "the blanket's layer and above": a different layer at
the *same* precedence with a higher sequence number surfaces, and one
with a lower sequence number does not. <a id="cite-tombstone.blanket.enumeration-surfaces-higher-sequence-at-same-precedence"></a>

<a id="trm-5-2-7-2-3"></a>

### Removal

Removing a blanket, or the layer holding it, unmasks everything it was
hiding. <a id="cite-tombstone.blanket.removal-unmasks-everything-it-hid"></a>

<a id="trm-5-2-7-3"></a>

## What a watcher sees

Nothing about tombstones. Writing a blanket produces one
`VALUE_DELETED` per name it newly masks; removing one produces one
`VALUE_SET` per name that became visible. A watcher sees per-value
effective state and never has to know the mechanism ([The Watch Model](<~kernel/internals/lcs/watches/the-watch-model#trm-5-6-1>)).
