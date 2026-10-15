---
title: "Overview"
description: "NTFE is the Peios packet engine — where it stands in the kernel, what it replaced, how its C glue and Rust core divide the work, and the terms this chapter uses."
type: reference
---

<a id="trm-6-1"></a>

NTFE — the Network Traffic Filtering Engine — is the kernel's packet
filter. It executes the packet layers of PNP, the Peios Network Policy:
PNP is the policy language and its registry layout under
`Machine\System\Network`, and NTFE is one of the components that carry
it out (netd is another, for the interface layer). It stands at
the netfilter seats, judges every traversal against the policy it reads
from the LCS registry itself, and applies the result: a verdict on the
packet, side effects on the flow and machine, and an event for whoever
is watching. <a id="cite-ntfe-engine.judges-from-registry-policy-itself"></a> No userspace process is in the enforcement path; the
viewer daemon (pnpd) observes and authors, it never decides. <a id="cite-ntfe-engine.no-userspace-in-enforcement-path"></a>

<a id="trm-6-1-1"></a>

## What it replaced

Peios ships a clean slate below NTFE. The netfilter **hook framework**
and **conntrack** (built in, with events, zones and timeouts; helpers
off) are kept, as are `nf_defrag` and the `nf_reject` machinery NTFE uses
to phrase refusals. <a id="cite-ntfe-engine.keeps-hooks-conntrack-defrag-reject"></a> With helpers off nothing assigns a
helper to a flow (only a conntrack entry a privileged process creates
over ctnetlink, naming one, could carry it), so no flow is *expected*
by another: `ct->master` stays NULL, and the Flow layer's `Related`
fact ([The snapshot](<~kernel/internals/ntfe/the-snapshot#trm-6-3>)) is false on every flow the stack tracks. <a id="cite-ntfe-engine.helpers-off-related-never-true"></a> Everything that was a policy *frontend* is
configured out: nf_tables, the xtables family (`iptables`, `ip6tables`,
`ebtables`, `arptables`), ipset, NFQUEUE, NFLOG, the flow table offload,
bridge netfilter, the netfilter BPF link and IPVS. <a id="cite-ntfe-engine.policy-frontends-configured-out"></a> `NF_NAT` is built but
dormant. <a id="cite-ntfe-engine.nf-nat-built-but-dormant"></a> The kernel config gate (`peios/verify-config.sh`)
asserts both halves so a merge cannot quietly bring a frontend back. <a id="cite-ntfe-engine.config-gate-asserts-both-halves"></a>

One consequence is worth knowing: conntrack's hooks are demand-activated,
historically by a ct-using iptables rule. With no frontend left, NTFE pins
them itself at init (`nf_ct_netns_get(&init_net, NFPROTO_INET)`); without
that pin `nf_ct_get()` is NULL on every packet and the `FlowState` fact
reads `untracked` forever. <a id="cite-ntfe-engine.pins-conntrack-hooks-at-init"></a>

<a id="trm-6-1-2"></a>

## Two halves

The engine is split along the line that kernels are good at and pure
code is good at.

**`net/ntfe/` (C)** owns everything that touches the kernel: the hook
registrations and the dispatch law (`seats.c`), building the fact
snapshot from an `sk_buff` (`snapshot.c`), RCU publication of policy
generations (`policy.c`), walking the registry into the builder
(`ingest.c`), the three machinery stores — flow tags on a conntrack
extension (`tags.c`), counter tables (`counters.c`), report emission into
KMES (`report.c`) — the Flow layer's sentence cache and dispatch
(`flow.c`), the refusals a `REJECT` sends (`refuse.c`), and the verdict
event ring behind `/dev/peios-ntfe` (`events.c`). <a id="cite-ntfe-engine.c-glue-owns-kernel-facing-work"></a>

**`pnp-core` (Rust, `security/pkm/pnp_core`)** owns everything the policy
*means*: the action language, the fact vocabulary and operators,
registry-shaped ingestion and validation, the forest, and the evaluation
algorithm. <a id="cite-ntfe-engine.core-owns-policy-meaning"></a> It is `no_std`, allocates only through the fallible PKM
wrappers, and has no I/O. <a id="cite-ntfe-engine.core-no-std-fallible-alloc-no-io"></a> The same source compiles twice: under cargo,
where a test suite encodes every ratified law by name, and into the
kernel, compiled from `security/pkm/pnp_core` as modules of the
`security/pkm` Rust crate and reached over a C ABI (`security/pkm/kacs/ntfe_runtime.rs`,
the bridge). <a id="cite-ntfe-engine.core-compiles-for-cargo-and-kernel"></a> Nothing about a rule's semantics exists in C. <a id="cite-ntfe-engine.no-rule-semantics-in-c"></a>

The bridge is the only place the two meet. <a id="cite-ntfe-engine.bridge-is-only-meeting-point"></a> C hands it a snapshot and a
forest; it resolves the forest's machinery facts against the packet by
calling back into the stores, evaluates, and applies the effects — after
collation, so a `COUNT` lands after this packet's own reads and a
`REPORT` can carry the verdict. <a id="cite-ntfe-engine.effects-applied-after-collation"></a>

<a id="trm-6-1-3"></a>

## Terms

- **Traversal** — one packet passing one direction through the machine.
- **Seat** — a netfilter hook NTFE stands at: the device *ingress* and
  *egress* seats (per interface) and the two IP seats, *inbound*
  (`LOCAL_IN`) and *outbound* (`LOCAL_OUT`).
- **Layer** — one of the three rule forests, `RawPacket`, `Packet` and
  `Flow`, each a registry key under `Machine\System\Network\Rules`.
- **Flow** — what conntrack tracks: a tuple-identified, bidirectional
  exchange. The unit the Flow layer judges.
- **Sentence** — the Flow layer's cached verdict on a flow: verdict,
  generation, expiry, on the flow's conntrack extension.
- **Snapshot** — the immutable set of facts one traversal is judged
  against at its seat.
- **Generation** — one published policy. Advances on every successful
  ingestion; <a id="cite-ntfe-engine.generation-advances-per-ingestion"></a> 0 means nothing was ever ingested and every layer is
  permissive, loudly. <a id="cite-ntfe-engine.generation-zero-is-permissive"></a>
- **Forest** — a layer's rule trees plus the machinery names it mentions:
  the tags it reads or writes, the counter streams it writes, and the
  counter views it reads.
- **Effect** — a side effect an evaluation yields (`TAG`, `COUNT`,
  `REPORT`, a prompt), applied by the glue.
- **Confession** — a counter in the engine status for something the
  engine refused or could not do. Nothing in NTFE fails silently. <a id="cite-ntfe-engine.nothing-fails-silently"></a>
- **Owner** — the identity KACS stamps on an inet socket ([Socket Identity](<~kernel/internals/kacs/network-objects/socket-identity#trm-3-12-2>)): the
  effective token and process facts at the last act that committed the
  socket to a role. What the Flow layer's `Local.*` facts are read from.
- **Endpoint kind** — what stands at a local end of a flow: `program`,
  `kernel`, `shared` or `none` ([The identity facts](<~kernel/internals/ntfe/the-identity-facts#trm-6-9>)).

The chapter follows a packet: the seats it meets ([Seats and dispatch](<~kernel/internals/ntfe/seats-and-dispatch#trm-6-2>)), the snapshot
taken of it ([The snapshot](<~kernel/internals/ntfe/the-snapshot#trm-6-3>)), how the forest judges it ([Evaluation](<~kernel/internals/ntfe/evaluation#trm-6-4>)), where that forest
came from ([Ingestion and generations](<~kernel/internals/ntfe/policy-ingestion-and-validation#trm-6-5>)), the stores its effects land in ([The stores](<~kernel/internals/ntfe/the-stores#trm-6-6>)), the event that
records it ([The event stream](<~kernel/internals/ntfe/event-ring-and-delivery#trm-6-7>)), what happens when it is the first packet of a flow
([The Flow layer](<~kernel/internals/ntfe/the-flow-layer#trm-6-8>)), and who stands at its local end ([The identity facts](<~kernel/internals/ntfe/the-identity-facts#trm-6-9>)). [NTFE ABI Reference](<~kernel/userspace/native/ntfe/generated-device-abi#trm-6-a>) is the generated
ABI of `/dev/peios-ntfe`; [NTFE ABI Notes](<~kernel/userspace/native/ntfe/device-operations-and-errors#trm-6-b>) is what the ABI tables cannot say.

<a id="trm-6-b-8"></a>

## Build configuration

`CONFIG_PEIOS_NTFE` (bool) depends on `SECURITY_PKM`, `NETFILTER`,
`NETFILTER_INGRESS`, `NETFILTER_EGRESS` and `NF_CONNTRACK=y` — NTFE is built in and reads flow
facts on the packet path, so conntrack must be too. <a id="cite-ntfe-abi-notes.config-ntfe-dependencies"></a> `CONFIG_PEIOS_NTFE_KUNIT`
builds the kernel-resident tests (`pkm_kunit_ntfe`), defaulting to
`SECURITY_PKM_KUNIT`. <a id="cite-ntfe-abi-notes.config-kunit-default"></a> The production fragment (`build/config/pkm.fragment`)
enables NTFE and configures the nf_tables/xtables family out; <a id="cite-ntfe-abi-notes.production-fragment-ntfe-on-nftables-off"></a>
`peios/verify-config.sh` asserts both. <a id="cite-ntfe-abi-notes.verify-kernel-config-asserts-fragment"></a>

## Related explanations

- [Event records and status semantics](<~kernel/userspace/native/ntfe/event-records-and-status-semantics>)
- [Device operations and errors](<~kernel/userspace/native/ntfe/device-operations-and-errors>)

## Calling the subsystem

The [native NTFE interface reference](<~kernel/userspace/native/ntfe/overview>) collects the caller contracts and generated ABI tables.
