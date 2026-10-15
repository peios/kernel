---
title: "Evaluation"
description: "The pnp-core algorithm — trigger set, abstention and speakers, collation, the backstop — and how the bridge carries a snapshot in and a verdict plus applied effects out."
type: reference
---

<a id="trm-6-4"></a>

Evaluation is `pnp_core::eval::evaluate(forest, snapshot, ctx)`: pure,
allocation-fallible, and the same code under cargo and in the kernel. <a id="cite-ntfe-eval.evaluate-is-pure-and-shared"></a>
Its steps are the ratified design's six, in order. <a id="cite-ntfe-eval.six-steps-in-order"></a>

<a id="trm-6-4-1"></a>

## 1. Matching

A rule matches iff it is enabled and every one of its conditions holds
against the snapshot. <a id="cite-ntfe-eval.rule-matches-iff-enabled-and-all-conditions-hold"></a> Conditions are a conjunction; a value written as a
list is a disjunction *within* that one field. <a id="cite-ntfe-eval.list-value-is-disjunction-within-field"></a> A disabled rule never
matches, so its subtree is unreachable. <a id="cite-ntfe-eval.disabled-rule-subtree-unreachable"></a>

Conditions are evaluated in the order ingestion stored them, which puts
live-time conditions (`Time.*`) **last**, <a id="cite-ntfe-eval.live-time-conditions-evaluated-last"></a> and the conjunction stops at
the first false one. <a id="cite-ntfe-eval.conjunction-stops-at-first-false"></a> Every live-time condition actually reached — true
or false — is *consulted*, and `Rule::matches_traced()` records into a
`MatchTrace` the moment it would next flip (`Condition::next_flip()`): <a id="cite-ntfe-eval.reached-clock-conditions-record-next-flip"></a>
for hour, minute, second and day-of-week, the value sequence is scanned
one cycle ahead with the condition's own operator, so `Time.Hour.Equal
9-17` at 10:30 flips at 18:00 and `Time.Hour.LessThan 24` never does; <a id="cite-ntfe-eval.clock-flip-scans-one-cycle-ahead"></a>
day-of-month, month and year answer "next midnight", since exact flips
need calendar arithmetic nobody has asked for. <a id="cite-ntfe-eval.calendar-fields-flip-at-next-midnight"></a> A false condition is
consulted too: a higher-priority rule that missed only on the clock may
match later. <a id="cite-ntfe-eval.false-clock-condition-is-consulted"></a> A rule whose address or port conditions fail first never
consults its clock and contributes nothing. <a id="cite-ntfe-eval.unreached-clock-condition-not-consulted"></a> The earliest consulted flip
is the evaluation's `expires_at` — the Flow layer's sentence expiry
([The Flow layer](<~kernel/internals/ntfe/the-flow-layer#trm-6-8>)); <a id="cite-ntfe-eval.expires-at-is-earliest-consulted-flip"></a> the per-packet layers compute it and ignore it. <a id="cite-ntfe-eval.per-packet-layers-ignore-expires-at"></a>

<a id="trm-6-4-2"></a>

## 2. The trigger set

The walk descends each tree from its root. A node **triggers** iff it
matches and none of its children match: a matching child shadows its
parent. <a id="cite-ntfe-eval.matching-child-shadows-its-parent"></a> Shadowing exists only within a lineage — two trees never shadow
each other, and their order in the forest carries no meaning. <a id="cite-ntfe-eval.trees-never-shadow-each-other"></a> The walk
returns "matched" to the parent so the parent knows it was shadowed. <a id="cite-ntfe-eval.walk-reports-match-to-parent"></a>

<a id="trm-6-4-3"></a>

## 3. Resolving a triggered rule

Every triggered rule's action list is resolved once. <a id="cite-ntfe-eval.triggered-rule-resolved-once"></a> Verdict actions fold
to the strictest listed; <a id="cite-ntfe-eval.verdict-actions-fold-to-strictest"></a> `TAG` and `COUNT` push effects; <a id="cite-ntfe-eval.tag-and-count-push-effects"></a> `REPORT` folds
to the highest level listed and pushes one effect if that level is at
or above `CurrentReportingLevel` (`level >= CurrentReportingLevel`; one
report per rule per evaluation); <a id="cite-ntfe-eval.report-folds-to-highest-level-and-gates"></a> `PROMPT`
pushes a prompt-issued effect and, with no handler transport in this
release, resolves its fallback in place <a id="cite-ntfe-eval.prompt-resolves-fallback-in-place"></a> (nesting bounded by
`MAX_PROMPT_CHAIN`, 4). <a id="cite-ntfe-eval.prompt-chain-bounded-at-four"></a> Side effects always execute — they are pushed
before anyone knows whether the rule's verdict will win. <a id="cite-ntfe-eval.side-effects-execute-regardless-of-verdict"></a>

<a id="trm-6-4-4"></a>

## 4. Abstention

A triggered rule that yields no verdict abstains. The walk then goes up
the rule's own parentage — the chain it descended by — to the nearest
ancestor whose actions contain a *direct* verdict (a top-level `PASS`,
`DROP` or `REJECT`; a verdict inside a `PROMPT` fallback does not count), <a id="cite-ntfe-eval.prompt-fallback-verdict-is-not-direct"></a>
and that ancestor **speaks for the region**: its full action list
resolves, once. <a id="cite-ntfe-eval.abstainer-climbs-to-nearest-verdict-ancestor"></a> A speaker reached by several abstaining descendants in
one evaluation executes only the first time (`spoken` tracks resolved
speakers by identity). <a id="cite-ntfe-eval.speaker-executes-once-per-evaluation"></a> Intermediate abstaining ancestors execute
nothing. <a id="cite-ntfe-eval.intermediate-abstainers-execute-nothing"></a> If no ancestor bears a verdict, the branch contributes nothing
and other trees or the backstop answer. <a id="cite-ntfe-eval.verdictless-branch-contributes-nothing"></a>

The attribution of a speaker's verdict is the speaker's path, not the
abstaining descendant's. <a id="cite-ntfe-eval.speaker-verdict-attributed-to-speaker"></a>

<a id="trm-6-4-5"></a>

## 5. Collation

Every yielded verdict is a candidate `(verdict, priority, path)`. <a id="cite-ntfe-eval.every-verdict-is-a-candidate"></a> The
winner has the highest priority; at equal priority the strictest
verdict: `DROP` (3) > `REJECT(Refused)` (2) > `REJECT(Prohibited)` (1) >
`PASS` (0). <a id="cite-ntfe-eval.highest-priority-then-strictest-wins"></a> The two reject ranks are a deterministic tie-break — the
quieter story wins — that exists only because candidate order is
meaningless. Priority is the rule's *effective* priority, resolved at
ingestion: a rule's own `Priority` value, else its parent's, else 0. <a id="cite-ntfe-eval.effective-priority-inherits-from-parent"></a>

<a id="trm-6-4-6"></a>

## 6. The backstop

No candidate at all: the verdict is `DROP`, attributed to `backstop`,
and the evaluation is flagged so the event can say so. <a id="cite-ntfe-eval.no-candidate-drops-via-flagged-backstop"></a> The backstop is
compiled in and un-deletable; <a id="cite-ntfe-eval.backstop-is-undeletable"></a> every permissive statement in a policy is
therefore a visible rule.

<a id="trm-6-4-7"></a>

## The evaluation as data

`Evaluation` carries the winning verdict, its attribution, the backstop
flag, every effect to apply, every candidate (winners and losers alike)
for observability, and `expires_at`. <a id="cite-ntfe-eval.evaluation-carries-every-candidate-and-effect"></a> Effects reference their stores by
name *and* hash: `Effect::Tag { hash, op }`, `Effect::Count { hash,
amount }` with the amount already resolved (`Length` becomes the packet
length, or 0 when the packet has none), <a id="cite-ntfe-eval.count-length-is-packet-length-or-zero"></a> `Effect::Report { rule, level }`,
`Effect::PromptIssued { rule, handler }`. <a id="cite-ntfe-eval.effects-carry-name-and-hash"></a>

<a id="trm-6-4-8"></a>

## The bridge

`ntfe_rust_evaluate(forest, snap, layer, reporting_level, out)` is what
`policy.c` calls under `rcu_read_lock()`. <a id="cite-ntfe-eval.bridge-runs-under-rcu-read-lock"></a> It:

1. lifts the C snapshot ([The snapshot](<~kernel/internals/ntfe/the-snapshot#trm-6-3>)) and resolves the forest's machinery facts
   through the stores — `peios_ntfe_tag_lookup()` for every tag name the
   forest mentions (`Packet` and `Flow` layers; `RawPacket` reads none), <a id="cite-ntfe-eval.rawpacket-forest-reads-no-tags"></a>
   `peios_ntfe_counter_read()` for every view — and gives a `Flow` forest
   its own facts, `Related` and `Start.*`; <a id="cite-ntfe-eval.bridge-resolves-machinery-facts-before-eval"></a>
2. evaluates with `EvalContext { reporting_level }`; <a id="cite-ntfe-eval.bridge-passes-reporting-level"></a>
3. writes the verdict, the reject kind, the backstop flag, the
   attribution (cut to 95 bytes), the FNV-1a-64 of the whole
   attributing path (`attributed_hash`) and `expires_at` (0 = never)
   into `struct peios_ntfe_outcome`; <a id="cite-ntfe-eval.bridge-writes-outcome"></a>
4. **then** applies the effects — `peios_ntfe_tag_apply()`,
   `peios_ntfe_counter_add()`, `peios_ntfe_report_emit()` with the verdict
   it just computed — counting each species into the outcome. <a id="cite-ntfe-eval.effects-applied-after-verdict"></a>

Ordering 4 after 2 is what the snapshot-immutability law requires: a
`COUNT` is applied after this packet's own view reads, so a rule cannot
trip its own threshold, <a id="cite-ntfe-eval.count-cannot-trip-own-threshold"></a> and a `REPORT` can name the verdict. <a id="cite-ntfe-eval.report-names-the-verdict"></a> Every
allocation in 1–2 is `GFP_ATOMIC` (`pnp-core`'s `pkm_alloc` in kernel
mode); <a id="cite-ntfe-eval.bridge-allocations-are-atomic"></a> a failure returns `-ENOMEM` and the hook fails closed ([Seats and dispatch](<~kernel/internals/ntfe/seats-and-dispatch#trm-6-2>)). <a id="cite-ntfe-eval.allocation-failure-fails-closed"></a> The
store calls never sleep. <a id="cite-ntfe-eval.store-calls-never-sleep"></a>
