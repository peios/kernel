---
title: "Event records and status semantics"
description: "Event records and status semantics: behaviour and implementation of the Peios kernel."
type: reference
---

<a id="trm-6-7-1"></a>

## One event

An event is the decision and enough of the snapshot to find the packet
it was about: sequence number, `CLOCK_REALTIME` nanoseconds, the seat
and layer, the verdict and — when it was a reject — its kind, flags
(`BACKSTOP`, `FAIL_CLOSED`, `REJECT_DEGRADED`, `REJUDGED` for a Flow
evaluation that replaced a stale sentence, `IDENTITY_UNRESOLVED` for
one whose endpoint could not be attributed), <a id="cite-ntfe-stream.event-flags"></a> direction, address family,
protocol, flow state, interface index, ports, ethertype, both addresses,
the stack-view length, the effect counts the evaluation yielded packed
eight bits each (tags, counts, reports, prompts, saturating), <a id="cite-ntfe-stream.event-effect-counts-packed-saturating"></a> and the
attributing rule's path — the winning rule, or `backstop`, or
`fail-closed` — in a 96-byte field (`PEIOS_NTFE_EV_ATTR_LEN`), so a
longer path is cut to 95 bytes, at a byte rather than a character
boundary, and NUL-terminated. <a id="cite-ntfe-stream.event-attributed-path-truncated-96"></a> A `Flow` event also carries both
endpoints' identities as the judgment read them ([The identity facts](<~kernel/internals/ntfe/the-identity-facts#trm-6-9>)): the kind, the
process GUID, pid and comm, the user SID and the service SID — binary
SIDs, so the viewer, not the kernel, turns them into names. <a id="cite-ntfe-stream.flow-event-carries-endpoint-identities"></a>

The path is relative to the layer key: `no-inbound/ssh`, not
`Machine\System\Network\Rules\Packet\no-inbound\ssh`. <a id="cite-ntfe-stream.path-relative-to-layer-key"></a>

<a id="trm-6-7-3"></a>

## Status

`PEIOS_NTFE_IOC_STATUS` fills `struct peios_ntfe_status`: the ABI version
(check it before trusting the rest — the ABI is experimental and
versioned, currently 5), <a id="cite-ntfe-stream.status-abi-version-5"></a> the generation, whether any layer is enforcing,
the ring's confessed drops, and the engine counters. <a id="cite-ntfe-stream.status-ioctl-contents"></a> The counters are
plain 64-bit atomics rather than per-CPU — legibility over throughput
while the engine is young, to be revisited with a compiled evaluator. <a id="cite-ntfe-stream.counters-plain-64bit-atomics"></a>

| Group | Counters |
|---|---|
| Seats | `seen_ingress`, `seen_egress`, `seen_local_in`, `seen_local_out`, `deferred` (ingress traversals left for the IP seat), `fallback_judged` (ingress traversals the Packet layer judged there) <a id="cite-ntfe-stream.counters-seats"></a> |
| Evaluation | `judged`, `permissive`, `parse_errors`, `fail_closed` <a id="cite-ntfe-stream.counters-evaluation"></a> |
| Verdicts | `verdict_pass`, `verdict_drop`, `verdict_reject`, `reject_degraded` <a id="cite-ntfe-stream.counters-verdicts"></a> |
| Effects yielded | `fx_tags`, `fx_counts`, `fx_reports`, `fx_prompts` <a id="cite-ntfe-stream.counters-effects-yielded"></a> |
| Ingestion | `last_ingest_error`, `last_ingest_t_ns`, `reporting_level`, `changes_noted` and `changes_walked` ([Ingestion and generations](<~kernel/internals/ntfe/policy-ingestion-and-validation#trm-6-5>), in force), `contexts` (interfaces in the network context table) <a id="cite-ntfe-stream.counters-ingestion"></a> |
| The stores | `tag_writes`, `tag_untracked`, `tag_refused`, `count_writes`, `count_key_absent`, `count_refused`, `reports_emitted`, `counter_cells` <a id="cite-ntfe-stream.counters-stores"></a> |
| The Flow layer | `flow_judged` (evaluations, sentences written), `flow_cached` (packets answered by a current sentence), `flow_rejudged` (stale by generation), `flow_expired` (stale by time edge), `flow_uncached` (flows with no extension to hold a sentence, evaluated per packet) <a id="cite-ntfe-stream.counters-flow-layer"></a> |
| Refusals | `refusals_emitted` (answers built and sent), `refusals_bypassed` (own refusals waved through a seat), `teardowns_emitted` (far-end resets for refused established TCP flows) <a id="cite-ntfe-stream.counters-refusals"></a> |
| The identity facts | `identity_unresolved` (endpoints that could not be attributed at resolution: a socket with no KACS state, an inet socket nobody stamped, a loopback sender the inbound seat could not see) <a id="cite-ntfe-stream.counters-identity"></a> |

Two invariants a reader can check: `judged` equals the number of
evaluations against a live forest at any layer (Flow evaluations
included, so `judged − flow_judged` is the per-packet count), <a id="cite-ntfe-stream.judged-counts-live-forest-evaluations"></a> and
`permissive` counts layer evaluations that found no forest — at
generation 0, every one. <a id="cite-ntfe-stream.permissive-counts-forestless-evaluations"></a>

`PEIOS_NTFE_IOC_COUNTERS` is the counter dump described in [The stores](<~kernel/internals/ntfe/the-stores#trm-6-6>): the
caller supplies a buffer of `struct peios_ntfe_counter_rec`, the kernel
fills as many as fit and reports both how many it wrote and how many
cells exist, so a short buffer is visible. <a id="cite-ntfe-stream.counters-ioctl-short-buffer-visible"></a> `PEIOS_NTFE_IOC_FLOWS` is the
flows dump described in [The Flow layer](<~kernel/internals/ntfe/the-flow-layer#trm-6-8>), with the same short-buffer contract over
`struct peios_ntfe_flow_rec`. <a id="cite-ntfe-stream.flows-ioctl-short-buffer-visible"></a>

<a id="trm-6-7-4"></a>

## Confessions, collected

Everything NTFE declines to do is counted somewhere in the status, and
the viewer shows every one of them. <a id="cite-ntfe-stream.every-refusal-counted"></a> A reader should never have to infer
a refusal from a missing effect:

- a `REJECT` it could not send → `reject_degraded`, and the event's flag; <a id="cite-ntfe-stream.confess-reject-degraded"></a>
- an evaluation it could not finish → `fail_closed`, and an event; <a id="cite-ntfe-stream.confess-fail-closed"></a>
- a frame it could not describe → `parse_errors`; <a id="cite-ntfe-stream.confess-parse-errors"></a>
- a tag it could not write → `tag_untracked` or `tag_refused`; <a id="cite-ntfe-stream.confess-tag-not-written"></a>
- a count it could not land → `count_key_absent` or `count_refused`; <a id="cite-ntfe-stream.confess-count-not-landed"></a>
- a sentence it could not keep → `flow_uncached`; <a id="cite-ntfe-stream.confess-flow-uncached"></a>
- an endpoint it could not attribute → `identity_unresolved`, and the
  event's flag; <a id="cite-ntfe-stream.confess-identity-unresolved"></a>
- a packet it did not judge because a sentence answered → `flow_cached`; <a id="cite-ntfe-stream.confess-flow-cached"></a>
- a refusal it did not judge because it was its own → `refusals_bypassed`; <a id="cite-ntfe-stream.confess-refusals-bypassed"></a>
- a generation it could not accept → `last_ingest_error`, and the log; <a id="cite-ntfe-stream.confess-ingest-error"></a>
- an event it could not keep → `events_dropped`. <a id="cite-ntfe-stream.confess-events-dropped"></a>

<a id="trm-6-b-3"></a>

## Event fields

- `attributed` is the winning rule's path relative to its layer key,
  UTF-8, NUL-terminated, truncated to `PEIOS_NTFE_EV_ATTR_LEN` − 1 bytes
  (95), which may split a multi-byte character. <a id="cite-ntfe-abi-notes.event-attributed-relative-nul-truncated"></a>
  Two reserved values: `backstop` (nothing yielded) and `fail-closed`
  (evaluation failed). <a id="cite-ntfe-abi-notes.event-attributed-reserved-values"></a>
- `effects` packs the effect counts the evaluation *yielded* — `tags |
  counts << 8 | reports << 16 | prompts << 24`, each saturating at 255. <a id="cite-ntfe-abi-notes.event-effects-packing-saturating"></a>
  What the stores then *applied* is in the status confessions, not in
  the event. <a id="cite-ntfe-abi-notes.event-effects-yielded-not-applied"></a>
- `reject_kind` is meaningful only when `verdict` is
  `PEIOS_NTFE_EV_VERDICT_REJECT`; <a id="cite-ntfe-abi-notes.event-reject-kind-only-on-reject"></a> a degraded reject (`flags &
  PEIOS_NTFE_EV_F_REJECT_DEGRADED`) still carries the kind the rule
  chose. <a id="cite-ntfe-abi-notes.event-degraded-reject-keeps-kind"></a>
- `PEIOS_NTFE_EV_F_REJUDGED` marks a `Flow`-layer evaluation that
  replaced a stale sentence (policy change or time edge). <a id="cite-ntfe-abi-notes.event-rejudged-flag"></a> A packet
  answered by a current sentence produces no event at all. <a id="cite-ntfe-abi-notes.cached-sentence-packet-no-event"></a>
- `layer` 2 is `Flow`; `seat` 4 is `LOCAL_OUT`. <a id="cite-ntfe-abi-notes.layer-2-flow-seat-4-local-out"></a> A `Flow` event's
  `direction` is the endpoint judged: the originator's side for a normal
  flow, each seat's own for a loopback flow's two judgments. <a id="cite-ntfe-abi-notes.flow-event-direction-is-endpoint-judged"></a>
- Addresses: the first 4 bytes when `addr_family` is 4, all 16 when 6,
  undefined when 0. <a id="cite-ntfe-abi-notes.event-address-bytes-by-family"></a> Ports are 0 when the fact was absent — check
  `protocol`. <a id="cite-ntfe-abi-notes.event-ports-zero-when-absent"></a>
- `flow_state` 0 means the fact was absent (the ingress seat), not that
  the flow was untracked; untracked is 5. <a id="cite-ntfe-abi-notes.event-flow-state-0-absent-5-untracked"></a>
- The identity fields (ABI 4) are set on `Flow` events only and zero
  elsewhere. <a id="cite-ntfe-abi-notes.event-identity-fields-flow-only"></a> `local_kind` / `remote_kind` are `PEIOS_NTFE_EV_LOCAL_*`:
  `ABSENT` (0) for a non-Flow event, and for `remote` whenever the
  other end is not local; <a id="cite-ntfe-abi-notes.event-kind-absent-cases"></a> `remote` is filled only on a loopback flow. <a id="cite-ntfe-abi-notes.event-remote-loopback-only"></a>
  For a `PROGRAM` end, `*_guid`, `*_pid` and `*_comm` are the process
  facts at the socket's stamp, `*_user` the token's user SID and
  `*_service` its per-service SID, both binary and self-sized (byte 1
  is the sub-authority count; all zero = absent — a user program has no
  service SID). <a id="cite-ntfe-abi-notes.event-program-end-fields"></a> `*_unresolved` says the end could not be attributed and
  was reported as the kernel's or as absent. <a id="cite-ntfe-abi-notes.event-unresolved-flag"></a>

<a id="trm-6-b-4"></a>

## Counter records

- `name` is the stream name (a rule's `COUNT(Name)`), NUL-terminated;
  `hash` is its FNV-1a identity as the kernel keys tables. <a id="cite-ntfe-abi-notes.counter-rec-name-and-hash"></a>
- `keyspec` says which of `src_addr`, `dst_addr`, `ifindex` are
  meaningful for this cell's key; the others are zero. <a id="cite-ntfe-abi-notes.counter-rec-keyspec-unkeyed-zero"></a> `family` is 4, 6,
  or 0 when no address fact is keyed. <a id="cite-ntfe-abi-notes.counter-rec-family"></a>
- `window_secs[i]` / `window_value[i]` for `i < n_windows` are the
  table's windows and this cell's current value in each; <a id="cite-ntfe-abi-notes.counter-rec-window-values"></a> `total` is
  cumulative since the cell was created (or migrated — see [The stores](<~kernel/internals/ntfe/the-stores#trm-6-6>)); <a id="cite-ntfe-abi-notes.counter-rec-total-cumulative"></a>
  `last_secs` is `CLOCK_REALTIME` seconds of the last write, for
  staleness. <a id="cite-ntfe-abi-notes.counter-rec-last-secs"></a>
- The dump lists every table's cells consecutively; group by `(name,
  keyspec)` to reconstruct tables. <a id="cite-ntfe-abi-notes.counter-dump-tables-consecutive"></a>

<a id="trm-6-b-5"></a>

## Flow records

- `id` is conntrack's own id for the entry (`nf_ct_get_id()`), stable
  for the flow's life and the key to use across dumps. <a id="cite-ntfe-abi-notes.flow-rec-id-stable"></a>
- `src_addr`/`dst_addr`, the ports and the ICMP fields are the
  *original-direction* tuple — the originator first. <a id="cite-ntfe-abi-notes.flow-rec-original-direction-tuple"></a> For ICMP, `src_port`
  carries the echo id and `icmp_type`/`icmp_code` the type and code;
  `dst_port` is 0. <a id="cite-ntfe-abi-notes.flow-rec-icmp-fields"></a>
- `direction`, `ifindex` and `loopback` are meaningful only when `judged`
  is 1: they were recorded at the Flow layer's first judgment. <a id="cite-ntfe-abi-notes.flow-rec-judged-gates-first-judgment-fields"></a> A flow
  with `judged == 0` has had no Flow judgment recorded: every packet of
  it that reached the flow dispatch ([The Flow layer](<~kernel/internals/ntfe/the-flow-layer#trm-6-8>)) found no Flow forest (a
  permissive generation) or failed closed, or none did — or it has no
  extension at all, and so nowhere to record one (`flow_uncached`; its
  sentences and identities read empty too). <a id="cite-ntfe-abi-notes.flow-rec-unjudged-began-permissive"></a>
- The sentences are parallel arrays indexed by slot (UAPI records hold
  scalars only): slot 0 is the flow's sentence; slot 1 is only ever
  filled for a loopback flow (its inbound endpoint). <a id="cite-ntfe-abi-notes.flow-rec-sentence-slots"></a> A slot with
  `sentence_generation == 0` is empty. <a id="cite-ntfe-abi-notes.flow-rec-generation-0-empty"></a> `sentence_expires_at` 0 means
  never. <a id="cite-ntfe-abi-notes.flow-rec-expires-0-never"></a> `sentence_rule_hash` is FNV-1a-64 (offset
  `0xcbf29ce484222325`, prime `0x100000001b3`) of the whole attributing
  path relative to the layer key, however long — not of the event's
  truncated `attributed`. `backstop` hashes like any other path; <a id="cite-ntfe-abi-notes.flow-rec-rule-hash-fnv1a-64"></a>
  `fail-closed` is never a sentence's, since a failed evaluation is
  not cached. <a id="cite-ntfe-abi-notes.flow-rec-fail-closed-never-cached"></a>
- `packets`/`bytes` are conntrack's accounting, original then reply; <a id="cite-ntfe-abi-notes.flow-rec-accounting-original-then-reply"></a>
  NTFE turns conntrack accounting on at init
  (`net.netfilter.nf_conntrack_acct`). <a id="cite-ntfe-abi-notes.init-enables-conntrack-acct"></a>
- `timeout_secs` is the entry's remaining lifetime as conntrack sees it; <a id="cite-ntfe-abi-notes.flow-rec-timeout-remaining"></a>
  `start_secs` is `CLOCK_REALTIME` seconds when conntrack created it. <a id="cite-ntfe-abi-notes.flow-rec-start-secs"></a>
- `tag_hash`/`tag_value` hold up to `PEIOS_NTFE_FLOW_MAX_TAGS` (8)
  present tags by name hash and value; <a id="cite-ntfe-abi-notes.flow-rec-up-to-8-tags"></a> `n_tags` is the flow's *total*,
  so a value above 8 means some are not listed. <a id="cite-ntfe-abi-notes.flow-rec-n-tags-is-total"></a>
- The identities (ABI 4) are per sentence slot, recorded at the flow's
  first judgment and fixed: `owner_kind[slot]` is `PEIOS_NTFE_EV_LOCAL_*`
  (`ABSENT` = not resolved; `ABSENT` with `owner_unresolved[slot]` set
  = judged but unattributed, such as a loopback sender the outbound seat
  never recorded); <a id="cite-ntfe-abi-notes.flow-rec-owner-kind-per-slot"></a> the per-slot arrays are flattened at a
  fixed stride — `owner_guid` 16 bytes per slot, `owner_comm` 16,
  `owner_user` 68, `owner_service` 32 — so slot 1's user SID starts at
  byte 68. <a id="cite-ntfe-abi-notes.flow-rec-owner-array-strides"></a> Slot 1 is filled only for a loopback flow. <a id="cite-ntfe-abi-notes.flow-rec-owner-slot-1-loopback-only"></a>

<a id="trm-6-b-6"></a>

## Listener records

- One record per socket prepared to receive: TCP in `LISTEN`, and UDP /
  UDP-Lite bound to a port (`connected` when it also has a peer and so
  receives from one address only). <a id="cite-ntfe-abi-notes.listener-rec-one-per-receiving-socket"></a> `addr` all zero is the wildcard; <a id="cite-ntfe-abi-notes.listener-rec-zero-addr-wildcard"></a>
  `ifindex` is `SO_BINDTODEVICE`, 0 for any; <a id="cite-ntfe-abi-notes.listener-rec-ifindex-bindtodevice"></a> `reuseport` marks a member
  of a `SO_REUSEPORT` group, of which each member is listed. <a id="cite-ntfe-abi-notes.listener-rec-reuseport-each-member-listed"></a> `v6only`
  says an `AF_INET6` socket refuses v4-mapped traffic — a v6 socket
  without it answers on both families. <a id="cite-ntfe-abi-notes.listener-rec-v6only"></a>
- The owner fields are those of the flow record's slot, for the socket's
  current stamp: `owner_kind` is `PROGRAM` or `KERNEL` (a socket nobody
  stamped reads `KERNEL` with `owner_unresolved` set). <a id="cite-ntfe-abi-notes.listener-rec-owner-current-stamp"></a>
- The walk is the root namespace's tables only, copied out between hash
  buckets: a best-effort list of a set that changes under it. <a id="cite-ntfe-abi-notes.listener-dump-root-ns-best-effort"></a>
