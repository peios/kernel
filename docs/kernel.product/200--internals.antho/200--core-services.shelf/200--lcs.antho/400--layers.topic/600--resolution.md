---
title: "Resolution"
description: "Turning several per-layer entries into one effective answer — the rule, why unknown layers are latent rather than wrong, and enumeration."
type: reference
---

<a id="trm-5-3-6"></a>

Layer resolution turns several per-layer entries into one effective
answer. It is the mechanism that makes the registry layered, and it is
the same algorithm for path entries and for values — one resolves
existence claims, the other resolves data. <a id="cite-layer.resolution.same-algorithm-for-path-entries-and-values"></a>

<a id="trm-5-3-6-1"></a>

## The rule

Every candidate is a tuple `(precedence, sequence, entry)`. The winner
is the maximum, ordered by precedence first and sequence second. <a id="cite-layer.resolution.winner-is-highest-precedence-then-highest-sequence"></a>

Building the candidate list:

1. For each entry the source returned, look up its layer in the current
   layer table. An entry naming a layer that is not in the table is
   **skipped**, not rejected. <a id="cite-layer.resolution.entry-for-an-unknown-layer-is-skipped"></a>
2. Discard entries from layers that are not active for this thread — a
   layer is active if it is globally enabled or its name is in the
   thread's private layer set ([Private Layers](<~kernel/internals/lcs/layers/private-layers#trm-5-3-5>)). <a id="cite-layer.resolution.inactive-layers-are-discarded"></a>
3. For values, add every blanket tombstone on the key as a tombstone
   candidate for the requested name, at its own precedence and
   sequence ([Tombstones](<~kernel/internals/lcs/data-model/tombstones#trm-5-2-7>)). <a id="cite-layer.resolution.blanket-tombstones-join-the-candidate-list"></a>
4. If there are no candidates, the answer is not-found. <a id="cite-layer.resolution.no-candidates-is-not-found"></a>
5. Take the maximum. A winning HIDDEN path entry, a winning
   `REG_TOMBSTONE` value entry, and a winning blanket all mean
   not-found. <a id="cite-layer.resolution.winning-hidden-tombstone-or-blanket-is-not-found"></a>

That is the whole algorithm. Everything the layer system does —
override, revert, mask, hide, hide-and-replace — is a consequence of
it.

<a id="trm-5-3-6-2"></a>

## Unknown layers are latent, not wrong

An entry tagged with a well-formed layer name that is not currently in
the table is a valid **latent** entry. <a id="cite-layer.resolution.latent-entry-is-valid"></a>

It is ignored while the layer is absent, and if a layer with the same
folded identity is later created, that entry becomes eligible for
resolution under the new metadata. <a id="cite-layer.resolution.latent-entry-becomes-eligible-when-the-layer-appears"></a>

This is what makes restore, import and boot ordering work: source
storage can legitimately hold entries before their metadata has been
loaded. It also follows the core rule — sources persist entries, LCS
decides their meaning.

Normal operations do not create such entries. <a id="cite-layer.resolution.normal-operations-do-not-create-latent-entries"></a> A layer-targeting ioctl
naming a layer that is not in the table returns `ENOENT`. Latent
entries come from existing storage, from a restore or import, from a
previous boot, or from source behaviour. Since sources are trusted,
a well-formed latent entry is not malformed merely because its layer is
absent right now.

An entry whose layer *name* is malformed is a different matter, and is
rejected as malformed source data. <a id="cite-layer.resolution.malformed-layer-name-is-rejected"></a>

<a id="trm-5-3-6-3"></a>

## Enumeration

Enumerating values collects the unique names across all layers and
resolves each one, returning only those whose answer is not not-found. <a id="cite-layer.resolution.enum-values-returns-only-resolved-names"></a>

Enumerating subkeys collects the unique child names and resolves each,
returning those that map to a GUID rather than HIDDEN. <a id="cite-layer.resolution.enum-subkeys-skips-hidden-children"></a>

"Unique" means folded-unique. Two entries whose names differ only in
case are one name, which is the only reading consistent with names
being case-insensitive. <a id="cite-layer.resolution.enumeration-uniqueness-is-folded"></a>

A caller sees effective state only. <a id="cite-layer.resolution.callers-see-effective-state-only"></a> Tombstoned values, blanket-masked
values and hidden keys are simply absent. Per-layer raw data is never
visible through a normal operation.

<a id="trm-5-3-6-4"></a>

## Enumeration is index-based, and that has a cost

`REG_IOC_ENUM_VALUES` and `REG_IOC_ENUM_SUBKEYS` return one entry at an
index. Each call re-resolves the full set and returns the entry at that
position, so walking `0..N-1` performs N full resolutions — O(n²) work
overall. <a id="cite-layer.resolution.enumeration-re-resolves-at-every-index"></a>

For a key with a handful of values that does not matter.
`REG_IOC_QUERY_VALUES_BATCH` exists for when it does: one call, the
whole effective value set, one resolution. <a id="cite-layer.resolution.batch-query-resolves-the-whole-set-once"></a>

Enumeration order is not defined, and the index-to-entry mapping can
change between calls if the effective set changes. <a id="cite-layer.resolution.enumeration-order-is-undefined"></a> Indices must not be
cached across mutations. The batch call is also the way to get a
consistent snapshot.

<a id="trm-5-3-6-5"></a>

## Neither party can lie about ordering

Two rules stop a source manipulating the outcome.

A source-returned entry whose sequence number is greater than or equal
to the next sequence LCS would allocate is **malformed data**. <a id="cite-layer.resolution.future-sequence-number-is-malformed"></a> Sources
store the numbers LCS assigns them; they cannot legitimately hold a
future one. Without this, a compromised source could fabricate a
sequence number and win every tie in its own hive.

Every entry in a response is validated this way, whatever layer it
names. <a id="cite-layer.resolution.every-entry-in-a-response-is-sequence-checked"></a>

Duplicate sequence numbers at the same precedence, where they would
actually have to be compared to pick a winner, are also malformed. LCS
rejects the response rather than making an arbitrary choice. <a id="cite-layer.resolution.compared-duplicate-sequences-are-malformed"></a>

Duplicates that never get compared are not an error. <a id="cite-layer.resolution.uncompared-duplicate-sequences-are-not-an-error"></a>

Both produce `EIO` and an `lcs.source.response.rejected` audit event
([Audit](<~kernel/internals/lcs/security/audit#trm-5-4-4>)). <a id="cite-layer.resolution.sequence-validation-failure-is-eio"></a>
