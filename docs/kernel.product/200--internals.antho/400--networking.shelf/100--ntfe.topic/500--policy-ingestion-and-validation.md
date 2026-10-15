---
title: "Policy ingestion and validation"
description: "Policy ingestion and validation: behaviour and implementation of the Peios kernel."
type: reference
---

<a id="trm-6-5"></a>

The kernel reads its own policy. There is no daemon that compiles rules
and pushes them down; `ingest.c` walks the registry through the LCS
source interface, feeds what it finds to the `pnp-core` builder over the
bridge, and publishes the result as a generation — or keeps the previous
one, loudly. <a id="cite-ntfe-ingest.refused-walk-keeps-previous-generation"></a> The same walk reads netd's inventory beside the rules into
the network context table ([The snapshot](<~kernel/internals/ntfe/the-snapshot#trm-6-3>)), <a id="cite-ntfe-ingest.walk-reads-inventory-with-rules"></a> because to a flow the two change
together: a network being recognised on an interface is as much a
policy change as a rule being written.

<a id="trm-6-5-1"></a>

## Discovery and change notification

At LCS bootstrap, NTFE's key is discovered fifth alongside the other
kernel-owned subtrees: <a id="cite-ntfe-ingest.key-discovered-at-bootstrap"></a> `pkm_lcs_walk_absolute_components()` resolves
`Machine\System\Network` (the leading `Machine` hive component is
resolved locally against the hive root, not round-tripped), <a id="cite-ntfe-ingest.machine-component-resolved-locally"></a> and its
absence is not an error — no key, no policy and no context, generation
stays where it is. <a id="cite-ntfe-ingest.absent-network-key-is-not-an-error"></a> When the key exists one internal watch is armed on
it, depth-unbounded, for every change of content at any depth — LCS
delivers it a value set, a value deleted, a subkey created, a subkey
deleted and a key deleted; a security-descriptor change is not
delivered: <a id="cite-ntfe-ingest.one-unbounded-watch-on-network-key"></a> `Rules\`, `Interfaces\` and
`Networks\` beneath it are what NTFE reads; <a id="cite-ntfe-ingest.ntfe-reads-rules-interfaces-networks"></a> `Profiles\` and `Dns\` are
netd's and resolvd's, and a write there fires the watch and costs a
walk that publishes nothing. <a id="cite-ntfe-ingest.foreign-subtree-write-publishes-nothing"></a>

Watch events arrive per key and uncoalesced.
`peios_ntfe_network_registry_changed()` records the source and key, sets
a pending flag, and `mod_delayed_work()`s a re-walk with a 50 ms
debounce: <a id="cite-ntfe-ingest.rewalk-debounced-50ms"></a> a burst of writes (a transaction touching a rule and its
values, an autoapply seeding a whole policy, netd syncing every
interface's `Status` after a link event) yields one re-walk after the
burst goes quiet. <a id="cite-ntfe-ingest.burst-yields-one-rewalk"></a> The walk itself runs in process context on
`system_wq`, one at a time under a mutex, since the bootstrap refresh
and the deferred work may overlap. <a id="cite-ntfe-ingest.walks-serialized-under-mutex"></a>

<a id="trm-6-5-2"></a>

## The walk

`peios_ntfe_network_refresh_from_key()` snapshots the LCS runtime limits,
sequence and layer view, enumerates the Network key's children for
`Rules`, `Interfaces` and `Networks`, and runs two independent stages —
the rules, then the context; <a id="cite-ntfe-ingest.rules-stage-then-context-stage"></a> a failure in the first does not skip the
second, and the walk reports the first error. <a id="cite-ntfe-ingest.rules-failure-does-not-skip-context"></a> No `Rules` key leaves the
previous generation standing, exactly as a walk that refused would. <a id="cite-ntfe-ingest.absent-rules-key-keeps-generation"></a>

The rules stage:

1. reads the Rules key's own values for `CurrentReportingLevel`
   (`REG_DWORD`, `REG_DWORD_BIG_ENDIAN` or `REG_QWORD`; 1..6; absent =
   1; anything else refuses); <a id="cite-ntfe-ingest.reporting-level-type-and-range"></a>
2. enumerates its children for the layer keys `Packet`, `RawPacket` and
   `Flow` (`Interface` is netd's — the interface layer is built and judged
   in userspace with the same `pnp-core`, and the kernel never reads it;
   any other name is ignored); <a id="cite-ntfe-ingest.kernel-reads-three-layer-keys-only"></a>
3. for each present layer, opens a builder and walks the layer key's
   subkeys as rule roots. Each rule is one `RSI_QUERY_VALUES` round trip
   (its effective, layering-resolved values, delivered in the batch
   record format `u32 name_len | name | u32 type | u32 data_len | data`)
   followed by one `RSI_ENUM_CHILDREN` round trip for its exceptions,
   recursively, <a id="cite-ntfe-ingest.rule-read-is-two-round-trips"></a> bounded by depth 12 and 4096 rules per layer: a root rule
   is depth 0, so a chain of 13 keys is the deepest read, and a rule
   deeper than that or a 4097th rule refuses the walk. <a id="cite-ntfe-ingest.walk-bounded-depth-12-and-4096-rules"></a>

Registry types are lowered as the builder ABI expects: `REG_SZ` and
`REG_EXPAND_SZ` to strings (NUL termination stripped), `REG_DWORD` and
`REG_DWORD_BIG_ENDIAN` to integers, `REG_QWORD` to a signed 64-bit
integer, `REG_MULTI_SZ` to a list of strings. <a id="cite-ntfe-ingest.registry-type-lowering"></a> Any other type in a rule
refuses the walk: <a id="cite-ntfe-ingest.other-value-type-refuses-walk"></a> atomic transitions prefer a loud rejection over a
silently half-read rule. So does an integer of the wrong length — a
`REG_DWORD` or `REG_DWORD_BIG_ENDIAN` whose data is not 4 bytes, a
`REG_QWORD` not 8 — in a rule or in `CurrentReportingLevel`. <a id="cite-ntfe-ingest.wrong-length-integer-refuses-walk"></a>

Everything the stage feeds the builder — each layer and whether its key
exists, rule name and depth, value name, type and bytes — also goes
through an FNV-1a digest, and so does the reporting level's *value*
(not its bytes: the same level re-written as another integer type
digests the same). <a id="cite-ntfe-ingest.rules-input-digested"></a> When the digest equals the one of the last walk that
published (none before the first), the stage publishes nothing: the
built forests are freed and the generation does not move. <a id="cite-ntfe-ingest.unchanged-digest-publishes-nothing"></a> The
active generation already *is* this policy — even when that policy is
no forests at all — and republishing would only make every sentence
stale for nothing. A walk fired by an inventory write therefore
publishes no rules; it moves the generation only if the context stage
finds the table changed (below). The writes of a transaction reach the
watch together at its commit and, like any burst, coalesce into one
walk. <a id="cite-ntfe-ingest.inventory-write-changes-no-generation"></a>

<a id="trm-6-5-2-1"></a>

### The context stage

The inventory is read into one `struct peios_ntfe_context_table`, at
most 64 entries of interface name, network id, name and trust: <a id="cite-ntfe-ingest.context-table-at-most-64-entries"></a>

1. every child of `Networks\` is a record; its key name is the id (a
   UUID — a name of 40 bytes or more, which no id field can hold, is
   ignored with its record, once loudly), <a id="cite-ntfe-ingest.overlong-network-id-ignored-once-loudly"></a> and one
   `RSI_QUERY_VALUES` round trip reads its `Name` and `Trust`
   (`REG_SZ`; absent or unreadable is empty, and the id is still a
   fact), <a id="cite-ntfe-ingest.unreadable-name-or-trust-is-empty"></a> up to 256 records; <a id="cite-ntfe-ingest.network-records-up-to-256"></a>
2. every child of `Interfaces\` is an interface; its `Status` subkey is
   found by one `RSI_ENUM_CHILDREN` and read by one `RSI_QUERY_VALUES`
   for `Name` (the kernel interface name) and `Network` (the id netd
   identified on it). <a id="cite-ntfe-ingest.interface-status-read"></a> Both present make an entry, joined to the record
   of that id for its name and trust; <a id="cite-ntfe-ingest.interface-entry-joins-network-record"></a> either absent — no link, no
   offer yet, an `IGNORE`d or `DOWN` interface — makes none. <a id="cite-ntfe-ingest.incomplete-status-makes-no-entry"></a>

Nothing in the stage refuses a generation. <a id="cite-ntfe-ingest.context-stage-never-refuses"></a> A record that cannot be read is
logged and skipped — an interface key whose subkeys cannot be listed,
or whose `Status` cannot be read, carries no context; a network record
whose values cannot be read keeps its id with no name and no trust; <a id="cite-ntfe-ingest.unreadable-record-skipped"></a>
an interface beyond the 64th carries no context, <a id="cite-ntfe-ingest.interface-beyond-64th-has-no-context"></a> a value
longer than its field is truncated with one warning. <a id="cite-ntfe-ingest.overlong-context-value-truncated"></a> If the list of
`Networks\` or `Interfaces\` itself cannot be read, the stage publishes
nothing and the previous table stands: a table built from half a list
would strip every network after the failure point of its name and
trust, and with them every rule that names them. That failure is the
walk's error — it shows in `last_ingest_error` — and the rules stage's
outcome is untouched by it. <a id="cite-ntfe-ingest.unreadable-list-keeps-previous-table"></a> Otherwise the table goes to `peios_ntfe_context_publish()` ([The snapshot](<~kernel/internals/ntfe/the-snapshot#trm-6-3>)): if it equals the active
one entry for entry it is freed and nothing happens; <a id="cite-ntfe-ingest.equal-context-table-publishes-nothing"></a> otherwise it is
`rcu_assign_pointer()`ed into place, the generation counter advances,
the old table is freed after grace, and the kernel log says how many
interfaces carry a context. <a id="cite-ntfe-ingest.changed-context-table-advances-generation"></a> The generation advance is the whole
mechanism by which a context change reaches running flows: every
sentence is now stale and is re-judged on its flow's next packet
([The Flow layer](<~kernel/internals/ntfe/the-flow-layer#trm-6-8>)), the same path a rule change takes. <a id="cite-ntfe-ingest.context-change-rejudges-flows-on-next-packet"></a>

<a id="trm-6-5-3"></a>

## Building and validating

The builder (`ntfe_rust_builder_*`) accumulates `RuleInput` trees; `build`
runs `pnp_core::ingest::build_forest`, which parses every condition key
and action expression, orders each rule's conditions with the live-time
ones last ([Evaluation](<~kernel/internals/ntfe/evaluation#trm-6-4>)), <a id="cite-ntfe-ingest.build-orders-live-time-conditions-last"></a> resolves priority inheritance, <a id="cite-ntfe-ingest.build-resolves-priority-inheritance"></a> lints layer-impossible
facts (a `FlowState` or tag condition in a `RawPacket` forest; a
per-packet fact — `Length`, `TcpFlags`, `Fragment`, `Ttl`, `Dscp`,
`EtherType`, `DstMac`, `FlowState` — in a `Flow` forest; `Related` or
`Start.*` anywhere but `Flow` — all legal, and built never to hold; the kernel drops
lints, the authoring surface shows them), <a id="cite-ntfe-ingest.layer-impossible-facts-lint-not-refuse"></a> and collects the forest's
**name sets**: every tag name mentioned in a `TAG` action, a `PROMPT`
fallback, or a `Tag.<n>` condition, split into the names the forest
*writes* and the first rule reading each; every stream a `COUNT` writes;
every distinct counter view a `Counter.<n>(...)` condition reads, with
the first rule and value that mentioned it. <a id="cite-ntfe-ingest.build-collects-name-sets"></a> Views are deduplicated and
conditions refer to them by index — that index is what the bridge uses
when it fills `counter_views` ([The snapshot](<~kernel/internals/ntfe/the-snapshot#trm-6-3>)). <a id="cite-ntfe-ingest.views-deduplicated-and-indexed"></a>

Refusals, each carrying the offending rule's path (`BuildError`):
unknown fact, <a id="cite-ntfe-ingest.refuse-unknown-fact"></a> unsupported operator, <a id="cite-ntfe-ingest.refuse-unsupported-operator"></a> unparsable pattern, <a id="cite-ntfe-ingest.refuse-unparsable-pattern"></a> a counter view
that does not parse (bad duration, unknown key fact, duplicate
arguments, a window over the one-day horizon), <a id="cite-ntfe-ingest.refuse-unparsable-counter-view"></a> a non-list `Actions`, <a id="cite-ntfe-ingest.refuse-non-list-actions"></a> an
unparsable action, <a id="cite-ntfe-ingest.refuse-unparsable-action"></a> a `REJECT` kind that is not `Refused` or
`Prohibited`, <a id="cite-ntfe-ingest.refuse-unknown-reject-kind"></a> a `PROMPT` chain nested deeper than `MAX_PROMPT_CHAIN`
(4), refused as an unparsable action, <a id="cite-ntfe-ingest.refuse-prompt-chain-too-deep"></a> an action the layer does not
speak (`JOIN`, `IGNORE` or `DOWN`, the interface layer's verdicts, in
a kernel layer, directly or as a `PROMPT` fallback), <a id="cite-ntfe-ingest.refuse-action-not-at-layer"></a> a `Present`
condition on a fact that never exists at the rule's layer (every other
operator over such a fact is only linted, below; `Present` looks
through the absent-fact law, so `X.Present = 0` there would always
hold), <a id="cite-ntfe-ingest.refuse-present-never-at-layer"></a> a `Priority` that is not an integer, <a id="cite-ntfe-ingest.refuse-non-integer-priority"></a> an `Enabled` that is
not 0 or 1, <a id="cite-ntfe-ingest.refuse-enabled-not-0-or-1"></a> a rule name that is empty or contains a path separator <a id="cite-ntfe-ingest.refuse-rule-name-with-path-separator"></a>
(a backstop: LCS refuses such a key name before the walk could read
it) — and, over the name sets, two distinct tag names (or stream names)
whose 64-bit hashes collide. <a id="cite-ntfe-ingest.refuse-name-hash-collision"></a>

After all three layers build, `ntfe_rust_forests_check()` runs the checks
that span forests, because the stores are machine-wide: tag and stream
hashes must be distinct across *every* forest; <a id="cite-ntfe-ingest.hashes-distinct-across-forests"></a> every counter view must
have a writer in *some* forest — a view over a stream no rule writes is
statically dead (it can only ever read absent) and is refused with the
rule and key that read it; <a id="cite-ntfe-ingest.refuse-view-without-writer"></a> and no forest may read a tag a *higher*
forest writes (`RawPacket` < `Packet` < `Flow`) — tags flow strictly
upward, and since rules are the only source of tag names the downward
read is refused statically, with the reading rule and the name. <a id="cite-ntfe-ingest.refuse-downward-tag-read"></a>

## Related explanations

- [Generation publication and recovery](<~kernel/internals/ntfe/generation-publication-and-recovery>)
