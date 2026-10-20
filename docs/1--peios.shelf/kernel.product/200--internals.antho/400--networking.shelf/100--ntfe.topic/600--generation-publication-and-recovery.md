---
title: "Generation publication and recovery"
description: "Generation publication and recovery: behaviour and implementation of the Peios kernel."
type: reference
---

<a id="trm-6-5-4"></a>

## Publication

`peios_ntfe_policy_publish(packet, raw, flow, reporting_level)` is
process context under a mutex. <a id="cite-ntfe-ingest.publish-serialized-under-mutex"></a> It runs the cross-forest check, then
materializes the counter store for the union of every forest's views
([The stores](<~kernel/internals/ntfe/the-stores#trm-6-6>)) — so a store that cannot be built (allocation, more than eight
windows on one table) refuses the generation before anything is
swapped. <a id="cite-ntfe-ingest.unbuildable-counter-store-refuses-generation"></a> Only then does it advance the generation counter, allocate the
new `struct peios_ntfe_policy` (three opaque forest pointers plus the
reporting level) and `rcu_assign_pointer()` it into place. <a id="cite-ntfe-ingest.generation-advances-only-after-checks"></a> Hook-path
readers dereference it under `rcu_read_lock()` and never block; <a id="cite-ntfe-ingest.hook-readers-never-block"></a> they see
the old generation or the new one, never a mix. <a id="cite-ntfe-ingest.readers-never-see-mixed-generation"></a> The old policy is
released by `call_rcu()`, and its forests by `ntfe_rust_forest_free()` in
the callback after grace. <a id="cite-ntfe-ingest.old-policy-freed-after-grace"></a>

Every walk records its outcome: `last_ingest_error` (0, or the positive
errno of the last failed walk) and `last_ingest_t_ns`, both in the
status. <a id="cite-ntfe-ingest.walk-outcome-in-status"></a> A refusal leaves the previous generation active and says so in
the kernel log. <a id="cite-ntfe-ingest.refusal-logged-and-previous-stays-active"></a> `contexts` in the status is the number of interfaces in
the active context table. <a id="cite-ntfe-ingest.status-contexts-counts-interfaces"></a>

<a id="trm-6-5-4-1"></a>

### In the event stream

NTFE writes its own lifecycle to KMES, origin class `KMES_ORIGIN_NTFE`
(4), beside the reports of [The stores](<~kernel/internals/ntfe/the-stores#trm-6-6>). Every publication writes one
`ntfe.policy.published`, after the swap; a refusal writes none. <a id="cite-ntfe-ingest.publish-emits-policy-published"></a>
Its payload is one `policy` map: `generation`, the generation now in
force; `generation-previous`, the generation of the policy it replaced,
0 for the first since boot; `layers`, the layers that have a forest, in
the order `raw-packet`, `packet`, `flow`, and an empty list for a policy
of no forests; and `report-threshold` and `report-threshold-previous`,
the new and the replaced `CurrentReportingLevel`, the latter 1 when
nothing was replaced. <a id="cite-ntfe-ingest.published-event-payload"></a> A walk
whose digest is unchanged publishes nothing, and so writes nothing. <a id="cite-ntfe-ingest.unchanged-walk-writes-no-published-event"></a>
A context-table change advances the generation without a policy and
writes no `ntfe.policy.published` either, so the generations between
two of these events are the earlier policy under a changed context.

A refused rules walk writes one `ntfe.policy.rejected`. <a id="cite-ntfe-ingest.refusal-emits-policy-rejected"></a>
Its `policy` map holds the `generation` still in force and
`previous-retained`, always true. Its `outcome` map holds `errno`, the
walk's negative errno, and `reason`. When the refusal is in, or names,
one rule, a `rule` map follows. It holds `layer` when the refusal arose
building one layer's forest, and `action-error` for a `bad-action`. It
holds `name`, the rule's path relative to its layer key; a path longer
than 255 bytes is cut at a character boundary, with `name-truncated`. <a id="cite-ntfe-ingest.rejected-event-payload"></a>

The errno is the walk's, unchanged. The reason is new: the bridge's
`ntfe_rust_builder_build_why()` and `ntfe_rust_forests_check_why()`
fill a `struct peios_ntfe_build_why` from pnp-core's `BuildError`. A
builder refusal keeps its own name and its rule's path, such as
`unknown-fact`, `bad-action` with its action error, `bad-priority`, or
`tag-downward-read` from the cross-forest checks, which name the rule
but no layer. <a id="cite-ntfe-ingest.build-refusal-reason-crosses-bridge"></a> The walk names the refusals it makes itself:

- `rule-too-deep` and `too-many-rules`, with `-E2BIG`;
- `bad-value-type`, `bad-value-length` and `not-utf8`, in the rule that
  holds the value;
- `bad-reporting-level`, `counter-store-refused` and `out-of-memory`;
- `registry-read-failed` for a source round trip that failed. <a id="cite-ntfe-ingest.walk-refusal-reasons"></a>

A walk that finds no `Rules` key writes the event too, with reason
`no-rules-key`, no `errno` and no rule. <a id="cite-ntfe-ingest.absent-rules-key-emits-rejected"></a>

Every walk re-reads the policy, including the walks netd's inventory
writes cause, so a broken policy is refused again and again until it
is fixed. The event is written once per distinct refusal: a walk whose
digest, errno and reason equal those of the last refusal written writes
none. A walk the rules stage accepts, published or unchanged, clears
that memory, so the next refusal is written whatever it is. A missing
`Rules` key is therefore written once each time the key goes missing. <a id="cite-ntfe-ingest.repeated-refusal-written-once"></a>
The kernel log line is written for every refusal, as before, and now
names the reason. Both events are built on the stack in process context,
under the publication mutex or the walk mutex; neither is ever written
from the packet path.

<a id="trm-6-5-4-2"></a>

### In force

A registry write that has returned is delivered, not enforced: the walk
that reads it runs after the debounce. <a id="cite-ntfe-ingest.returned-write-not-yet-enforced"></a> Two status counters say which a
writer is looking at. `changes_noted` is incremented by
`peios_ntfe_network_registry_changed()` for every watch event, <a id="cite-ntfe-ingest.changes-noted-counts-watch-events"></a> and LCS
delivers its internal watches inside the write that caused them, after
the commit and before the syscall returns, so a writer that reads the
status after its write sees its own change counted. <a id="cite-ntfe-ingest.writer-sees-own-change-noted"></a> The deferred work
reads `changes_noted` under the same lock that clears the pending flag,
before it walks, and stores that value in `changes_walked` when the walk
returns, whether it published or was refused. <a id="cite-ntfe-ingest.changes-walked-set-from-pre-walk-noted"></a>

So a writer is in force once `changes_walked` reaches the `changes_noted`
it read after writing: the walk that satisfied it started after the
write committed. <a id="cite-ntfe-ingest.in-force-when-walked-reaches-noted"></a> A change that lands mid-walk raises `changes_noted`
again and re-arms the work, so the pair stays unequal until a later walk
covers it. <a id="cite-ntfe-ingest.mid-walk-change-rearms-work"></a> A refused walk still advances `changes_walked`; <a id="cite-ntfe-ingest.refused-walk-advances-changes-walked"></a> the writer
then reads `last_ingest_error` to learn that what it wrote is not what
is enforced. The walk records its error before it stores
`changes_walked`, and the status reads them in the other order, so a
status that shows a change walked shows that walk's error or a later
one's, never an older one. The bootstrap walk is not a noted change and moves neither
counter. <a id="cite-ntfe-ingest.bootstrap-walk-moves-neither-counter"></a> `net policy wait` is this loop.

<a id="trm-6-5-5"></a>

## Generation 0

Until the first successful ingestion there is no policy at all, and
every layer is permissive: <a id="cite-ntfe-ingest.generation-zero-is-permissive"></a> `judged` stays 0, `permissive` counts
traversals, no events are emitted (there is no decision to attribute),
and the status reports `enforcing = 0`. <a id="cite-ntfe-ingest.generation-zero-status-and-no-events"></a> The init log line says it
plainly. This is the ratified loud default — the alternative, a
compiled-in policy the registry cannot see, was rejected.

A new generation does not touch the flows: every sentence written under
the old one is stale by generation and is re-judged on its flow's next
packet ([The Flow layer](<~kernel/internals/ntfe/the-flow-layer#trm-6-8>)). <a id="cite-ntfe-ingest.new-generation-stales-sentences-without-flow-walk"></a> That is how a policy change — and a context change,
which advances the same counter — reaches running connections without
a walk of the conntrack table.
