---
title: "The stores"
description: "The three machinery stores behind NTFE's effects — flow tags on a conntrack extension, counter tables materialized from the forest's views, and REPORT emission into KMES — with their bounds and confessions."
type: reference
---

<a id="trm-6-6"></a>

Effects need somewhere to land. Three stores, each with a small C
surface the bridge calls during evaluation, each confessing what it
refuses into the engine status.

<a id="trm-6-6-1"></a>

## Identities

Tag and stream names cross into the stores as 64-bit **FNV-1a hashes**
(`pnp_core::hash::name_hash`). <a id="cite-ntfe-store.names-cross-as-fnv1a-hashes"></a> The stores never see a string on the
packet path, and never a generation: a flow's tag table holds `(hash,
value)` pairs, a counter table is keyed by its stream's hash. <a id="cite-ntfe-store.stores-hold-no-strings-or-generations"></a> Two
consequences: tags survive policy reloads by construction (the table
knows nothing to invalidate), <a id="cite-ntfe-store.tags-survive-policy-reload"></a> and a hash must be a deterministic
identity, not a probabilistic one — which ingestion guarantees by
refusing any generation whose distinct names collide ([Ingestion and generations](<~kernel/internals/ntfe/policy-ingestion-and-validation#trm-6-5>)). <a id="cite-ntfe-store.colliding-names-refuse-generation"></a> Within a
running policy a collision is impossible; across generations the
residual is a 64-bit birthday bound over a handful of names, documented
and not defended.

<a id="trm-6-6-2"></a>

## Flow tags

A tag is a named unsigned integer on a conntrack entry. The store is the
`tags` pointer of NTFE's **conntrack extension** — `NF_CT_EXT_NTFE`,
`struct peios_ntfe_ct` (`include/linux/peios_ntfe.h`), added to every flow
at creation (`init_conntrack()`, by the `ntfe-conntrack-ext.patch`), <a id="cite-ntfe-store.ct-extension-added-at-flow-creation"></a> with
the pointer NULL until the flow's first `TAG`. <a id="cite-ntfe-store.tag-table-null-until-first-tag"></a> The extension *block* of
a confirmed conntrack entry is immutable (upstream removed post-confirm
resizing as an RCU-reader race), and NTFE's egress seat runs after
confirmation, so the extension must exist before it is needed; a fixed
extension on every flow is the cheapest way to guarantee that. Since the
Flow slice the extension also holds the flow's start time and its two
sentences ([The Flow layer](<~kernel/internals/ntfe/the-flow-layer#trm-6-8>)) — 88 bytes per flow, most of it the sentences — <a id="cite-ntfe-store.ct-extension-holds-start-and-sentences"></a> while
untagged flows, nearly all of them, still pay nothing for a table.

The first `TAG` allocates (`GFP_ATOMIC`) a table of eight `(hash, value,
present)` entries; <a id="cite-ntfe-store.first-tag-allocates-eight-entries"></a> a full table is replaced by one twice the size —
copy, `rcu_assign_pointer()`, `kfree_rcu()` the old — <a id="cite-ntfe-store.full-tag-table-doubles"></a> up to the tripwire
of 64 distinct tags per flow. <a id="cite-ntfe-store.tag-tripwire-64-per-flow"></a> Readers walk the table under RCU with no
lock (the hook path already holds the read lock); <a id="cite-ntfe-store.tag-readers-lockless-under-rcu"></a> writers serialize on
the flow's own `ct->lock`. <a id="cite-ntfe-store.tag-writers-serialize-on-ct-lock"></a> `Clear` tombstones an entry (`present = 0`)
rather than compacting, so a concurrent reader never sees the table
shift under it, <a id="cite-ntfe-store.clear-tombstones-without-compacting"></a> and a later `Set` reuses the slot. <a id="cite-ntfe-store.set-reuses-tombstoned-slot"></a> `Add` saturates at
`U64_MAX`. <a id="cite-ntfe-store.tag-add-saturates"></a> The entry's identity is published before the length that
exposes it (`smp_wmb()` then `WRITE_ONCE(len)`), so a reader that sees
the new length sees a complete entry. <a id="cite-ntfe-store.tag-entry-published-before-length"></a>

When the flow dies, `nf_conntrack_free()` calls `peios_ntfe_ct_destroy()`
(the same patch), which `kfree_rcu()`s the table — a reader that found
the entry under RCU may still be walking it. <a id="cite-ntfe-store.tag-table-freed-after-grace-on-flow-death"></a>

Confessions: `tag_writes` (ops applied), <a id="cite-ntfe-store.tag-writes-counts-applied-ops"></a> `tag_untracked` (a `TAG` on a
packet with no flow — untracked traffic, or the ingress seat — is a
no-op), <a id="cite-ntfe-store.tag-without-flow-is-untracked-no-op"></a> `tag_refused` (the tripwire, an allocation failure, or a flow
whose extension could not be allocated at creation). <a id="cite-ntfe-store.tag-refused-confessions"></a> Clearing an absent
tag is a no-op, not a refusal. <a id="cite-ntfe-store.clearing-absent-tag-is-no-op"></a>

<a id="trm-6-6-3"></a>

## Counters

`COUNT(Name[, amount])` emits into a **stream**; every
`Counter.Name([window][, key])` a rule reads is a **view**. Nothing is
declared: views are compile-time constants (rules are their only
source), so at publication ([Ingestion and generations](<~kernel/internals/ntfe/policy-ingestion-and-validation#trm-6-5>)) the store receives the complete view
set of all three forests — `Packet`, `RawPacket` and `Flow` — and materializes exactly that — one **table** per
distinct `(stream hash, key-spec)`, each answering every window any
view of that pair asks for, plus the cumulative total. <a id="cite-ntfe-store.one-table-per-stream-and-key-spec"></a> A `COUNT`
increments every table of its stream; <a id="cite-ntfe-store.count-increments-every-table-of-stream"></a> the amplification is bounded by
what policy authors wrote, the trusted side of the trust asymmetry.

A table is a 1024-bucket hash of **cells** (`jhash` over the cell key)
under a per-table spinlock (`_bh`, since the publisher runs in process
context). <a id="cite-ntfe-store.table-is-1024-bucket-hash-under-bh-lock"></a> A cell key is built from the packet by the table's key-spec:
address family, source and destination address (16 bytes each, v4 in
the first four), interface index — only the facts the spec names, the
rest zero. <a id="cite-ntfe-store.cell-key-holds-only-named-facts"></a> A packet lacking a keyed fact (an ARP frame for a
`SrcAddr`-keyed table) has no cell: its `COUNT` no-ops into that table
(`count_key_absent`) <a id="cite-ntfe-store.count-without-key-fact-no-ops"></a> and its view reads absent — the absent-fact law on
both sides. <a id="cite-ntfe-store.view-without-key-fact-reads-absent"></a>

A cell holds a cumulative `total`, the seconds of its last write, and
one **ring** per table window: eight buckets, each stamped with the
*period* it belongs to (`now / bucket_secs`, where `bucket_secs =
max(1, window / 8)`). <a id="cite-ntfe-store.ring-is-eight-period-stamped-buckets"></a> A write zeroes a bucket whose stamp is stale
before adding; <a id="cite-ntfe-store.write-zeroes-stale-bucket"></a> a read sums the buckets whose stamp is within the last
eight periods. <a id="cite-ntfe-store.read-sums-last-eight-periods"></a> Advancement is lazy — there are no timers — and the
window is an approximation up to one bucket wide, by design. <a id="cite-ntfe-store.window-approximate-to-one-bucket"></a>

The keyspace of a keyed table is chosen by whoever sends packets, so
tables are hard-capped at **4096 cells**. <a id="cite-ntfe-store.table-capped-at-4096-cells"></a> At the cap the store first
reaps cells idle for longer than the table's longest window (floor
60 s); <a id="cite-ntfe-store.cap-reaps-idle-cells-first"></a> if none are idle the new key is refused and confessed
(`count_refused`). <a id="cite-ntfe-store.cap-refuses-new-key-when-none-idle"></a> Never silent eviction.

The store outlives generations. <a id="cite-ntfe-store.counter-store-outlives-generations"></a> Re-publication keeps tables whose window
set did not change, <a id="cite-ntfe-store.republish-keeps-unchanged-tables"></a> creates new ones, <a id="cite-ntfe-store.republish-creates-new-tables"></a> **migrates** tables whose windows
changed (each cell is re-allocated in the new ring layout; the total and
any window both sets share carry over, new windows start empty and
converge), <a id="cite-ntfe-store.republish-migrates-changed-tables"></a> and retires tables no forest views any more — `list_del_rcu()`
then free after grace, cells included. <a id="cite-ntfe-store.republish-retires-unviewed-tables"></a> Reads on the packet path walk the
table list and the cell lists under RCU; <a id="cite-ntfe-store.counter-reads-under-rcu"></a> the publisher holds a mutex.

`PEIOS_NTFE_IOC_COUNTERS` dumps every cell of every table for the viewer:
stream name, key-spec, the key, the total, the last-write time, and the
current value of each window. <a id="cite-ntfe-store.counters-ioctl-dumps-every-cell"></a> It is a best-effort snapshot, which is fine
for counters that are approximate by design: the cells are gathered
into a kernel batch under one RCU read section and copied out after
it, and a store with more cells than a batch holds (4096) takes
further passes, each resuming after the cells already written, so a
cell created or retired between passes may be missed or seen twice. <a id="cite-ntfe-store.counters-dump-is-best-effort"></a>

<a id="trm-6-6-4"></a>

## Reports

`REPORT(level)` at or above `CurrentReportingLevel` becomes one KMES event:
origin class `KMES_ORIGIN_NTFE` (4), event type `ntfe.verdict.reported`, <a id="cite-ntfe-store.report-becomes-one-kmes-event"></a> and a
msgpack payload laid out as the event catalogue's `ntfe` fragment
says: nested string-keyed maps, one per path segment. `rule` carries
the attribution (`name`, the path, and `hash`, the FNV-1a-64 of the
whole path), the `report-level`, and where the judgment stood
(`layer`: `raw-packet`, `packet` or `flow`; `seat`). `outcome` carries
what it said (`verdict`: `pass`, `reject` or `drop`; and `reason`,
`prohibited` or `refused`, when it was a reject). The packet is
`network` (`direction`, `interface` with its `name` and `index`,
`ether-type`, `family` as the `AF_*` number, `protocol`, `length`),
`source` and `destination` (each an `address` as text and a `port`),
and `flow` (`state`). `policy` carries the `generation`. The time is
the KMES header's; the payload does not repeat it. <a id="cite-ntfe-store.report-payload-keys"></a> A packet key whose fact can be
absent is present only when the packet has it: `network.protocol`,
`source` and `destination` when it has an address family, their ports
when it has ports, `flow` when the flow-state fact is present.
`network.direction`, `network.interface.index`, `network.ether-type`,
`network.family` and `network.length` are always emitted — an
interface index of 0 and a family of `AF_UNSPEC` (0) are the catalogue's
own values for none. `network.interface.name` is left out when no
device was there to name; no key is ever written as an empty string. <a id="cite-ntfe-store.report-omits-absent-packet-keys"></a>

The payload is built on the stack (512 bytes) <a id="cite-ntfe-store.report-payload-built-on-stack"></a> because the packet path runs in softirq and
`pkm_kmes_emit_kernel()` is a preempt-disabled per-CPU ring write with
no allocation of its own. Every map's size is known before it is
written, save `rule`'s, whose one-byte header is settled once the
name's fate is. Every value but `rule.name` is bounded, so `rule` goes
in last and `name` last within it: a path too long for the room left
is cut at a character boundary to fit, and `rule.name-truncated`
(`true`, absent when the name is whole) says so. The event is always
emitted, and `rule.hash` still names the whole path, so a reader
resolves the rule against the policy. <a id="cite-ntfe-store.report-long-rule-cut-and-said"></a> Flood control is the author's by design — the
level gate — with KMES's own ring accounting as the backstop.
`reports_emitted` counts what reached the ring. <a id="cite-ntfe-store.reports-emitted-counts-ring-arrivals"></a>
