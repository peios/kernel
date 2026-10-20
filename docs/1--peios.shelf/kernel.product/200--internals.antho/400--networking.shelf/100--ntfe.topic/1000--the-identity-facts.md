---
title: "The identity facts"
description: "The third rung — who stands at each local end of a flow, read once from the socket KACS stamped, fixed for the flow's life, and judged as the Flow layer's Local and Remote facts."
type: reference
---

<a id="trm-6-9"></a>

The identity facts (rung 3 on PEI-598) answer the question the address
facts cannot: not *where* a flow goes but *who* on this machine is
speaking or listening. They are Flow-layer facts by the same law as
`Related` and `Start.*` — a flow has one answer for its whole life — and
they are the first facts NTFE reads from somewhere other than the packet.
KACS provides them; the engine resolves them once per flow.

<a id="trm-6-9-1"></a>

## What KACS stamps on a socket

Every inet socket carries a **governing identity**, recorded by KACS in
the socket's security state ([Socket Identity](<~kernel/internals/kacs/network-objects/socket-identity#trm-3-12-2>)): the caller's *effective* token —
so a service thread impersonating a client attributes the socket to the
client, as audit does — and the process facts of that moment: the
process GUID, the thread-group id and the `comm` of the thread that
made the stamp (a thread's own name, which need not be its process's). <a id="cite-ntfe-identity.socket-stamp-effective-token-and-process-facts"></a> The stamp is
taken at every act that commits the socket to a role: creation, `bind`,
`listen`, `connect`, inheritance at `accept`, and `KACS_SO_RESTAMP`. <a id="cite-ntfe-identity.stamp-taken-at-role-acts"></a> The
last stamp governs, which is how a listener handed to another program
(socket activation, descriptor passing) is governed as that program's. <a id="cite-ntfe-identity.last-stamp-governs"></a>
A kernel socket is stamped as the kernel's, with no token. <a id="cite-ntfe-identity.kernel-socket-stamped-without-token"></a>

The engine reads the stamp through one accessor,
`pkm_kacs_socket_owner()` (`<linux/peios_ntfe.h>`), which hands it a
counted reference to the token and a copy of the process facts. <a id="cite-ntfe-identity.owner-accessor-counted-ref-and-copy"></a> The
facts outlive the process; the reference outlives the socket. <a id="cite-ntfe-identity.facts-outlive-process-and-socket"></a>

<a id="trm-6-9-2"></a>

## What stands at an end

`identity.c` classifies each local end of a flow by **whether anyone
answers**, not by whether a socket structure exists. The result is the
`Local` fact (`program`, `kernel`, `shared`, `none`) and, for a program,
the principal behind `Local.*`. <a id="cite-ntfe-identity.local-fact-kinds"></a>

**Outbound**, at `LOCAL_OUT`: the sending socket's stamp. A stamped
program socket is `program`; <a id="cite-ntfe-identity.outbound-stamped-socket-program"></a> a kernel socket, or no socket at all
(resets, ICMP errors, IGMP) is `kernel`. <a id="cite-ntfe-identity.outbound-kernel-or-no-socket-kernel"></a>

**Inbound**, at `LOCAL_IN`, a transport lookup for the receiver of this
very packet:

- UDP to a multicast or broadcast destination is `shared` before any
  lookup: the stack delivers it to every socket bound to the port — one
  flow, many endpoints — and the per-program question belongs to the
  *join*, not to the packet. `Local.*` is absent. <a id="cite-ntfe-identity.inbound-multicast-broadcast-udp-shared"></a>
- TCP, UDP and UDP-Lite are looked up by tuple, the way the netfilter
  socket match does — listeners included, and through the same hash a
  `SO_REUSEPORT` group steers by, so the sentence names the socket that
  will actually receive. <a id="cite-ntfe-identity.inbound-transport-lookup-by-tuple"></a> Early demux may already have found it, and
  its socket is used in place of the lookup — for UDP only once the
  datagram has passed the `shared` test above, since early demux also
  attaches the one socket a multicast datagram happens to match. An early
  result is used only if its socket still has a live reference that NTFE
  can pin. UDP early demux keeps the pointer valid under RCU but does not
  itself hold a reference; if the socket's last reference has gone, NTFE
  falls back to the ordinary tuple lookup without reviving the socket.
  A missing receiver then gives the same `none` result as an ordinary
  lookup miss. The temporary socket reference is released after reading
  the identity. <a id="cite-ntfe-identity.early-receiver-pin-or-lookup"></a>
  Any other protocol is looked up among raw sockets bound to it. <a id="cite-ntfe-identity.inbound-other-protocol-raw-lookup"></a>
- A socket found is `program` (a request minisock stands for its
  listener; a `TIME_WAIT` minisock is nobody's: `kernel`). <a id="cite-ntfe-identity.inbound-found-socket-program"></a>
- Nothing found: `kernel` if the stack has a handler registered for the
  protocol — ICMP and ICMPv6 (neighbour discovery, router advertisements,
  MLD), IGMP, the tunnel and IPsec outers that are decapsulated and
  re-enter the ingress seat as their inner packet — else `none`, which
  the stack will answer with a reset or an unreachable. <a id="cite-ntfe-identity.inbound-nothing-found-kernel-or-none"></a>

The classification is a rule, not a list of protocols. Two consequences
are documented rather than special-cased: SCTP, a socket transport whose
table lives inside its module, reads `kernel` while the module is
loaded; <a id="cite-ntfe-identity.sctp-reads-kernel"></a> and a ping socket's echo reply pairs with the outbound request in
conntrack and inherits the outbound `program` sentence, so the direct
lookup is deferred. <a id="cite-ntfe-identity.ping-reply-inherits-outbound-sentence"></a>

The lookup runs **once per flow**, on the first judgment, and only when
a `Flow` forest is published: a permissive machine pays nothing. <a id="cite-ntfe-identity.lookup-once-per-flow-only-with-flow-forest"></a>

<a id="trm-6-9-3"></a>

## Loopback: both ends

A loopback flow has two local ends and two sentences ([The Flow layer](<~kernel/internals/ntfe/the-flow-layer#trm-6-8>)). The
outbound seat resolves both on the first packet — its own end from the
socket, the other by running the receiver lookup early on the
loopback-destined packet — and records them on the flow's extension. <a id="cite-ntfe-identity.loopback-outbound-seat-resolves-both-ends"></a>
The inbound seat's judgment, on the same packet, reads both from there:
`Local.*` is its own end and `Remote.*` the sender's. <a id="cite-ntfe-identity.loopback-inbound-local-own-remote-sender"></a> The inbound seat
cannot see a loopback packet's sender itself (loopback transmission
orphans the buffer), so a flow whose extension could not be allocated
reads `Remote` as absent there, confessed. <a id="cite-ntfe-identity.loopback-no-extension-remote-absent-confessed"></a> Off loopback `Remote` is
always absent: nothing is provable about a peer yet. <a id="cite-ntfe-identity.remote-absent-off-loopback"></a>

<a id="trm-6-9-4"></a>

## Fixed for the flow's life

The identities are recorded on the conntrack extension at the first
judgment, per slot, beside the direction and the interface, and never
replaced: a re-judgment after a policy change or a time edge sees the
same principal, and a later restamp of the socket, a fork after
`accept`, or a `SO_REUSEPORT` sibling taking over the port changes
nothing for flows already judged. <a id="cite-ntfe-identity.fixed-at-first-judgment"></a> The extension holds one counted token
reference per slot and releases it when conntrack frees the flow. <a id="cite-ntfe-identity.token-ref-per-slot-released-on-free"></a> Two
CPUs racing on a new flow's first packets may both resolve; the first
record stands — unlike the sentence, where the second write wins
([The Flow layer](<~kernel/internals/ntfe/the-flow-layer#trm-6-8>)) — and the loser releases its reference and judges the recorded
identity instead of its own. <a id="cite-ntfe-identity.resolve-race-first-record-stands"></a>

<a id="trm-6-9-5"></a>

## Across the bridge

The flow view carries, per end, the kind, the process facts and a
borrowed token pointer. <a id="cite-ntfe-identity.flow-view-carries-borrowed-token"></a> The bridge (`security/pkm/kacs/ntfe_runtime.rs`) implements
pnp-core's `Principal` trait over the token — user SID, enabled-group
membership (deny-only groups are invisible to policy), <a id="cite-ntfe-identity.deny-only-groups-invisible"></a> integrity level,
confinement SID and capabilities, the per-service SID found among the
enabled groups, the process GUID as text (PCDS's string form —
`Data1`, `Data2` and `Data3` read as little-endian numbers and written
most significant digit first, `Data4` bytes in order — lowercase and unbraced, `8-4-4-4-12`; ingestion lowercases a
`Local.Process` or `Remote.Process` pattern and strips braces from a
braced one to match) — without copying the group
list: a token may carry a thousand groups and the judgment runs in
softirq context, so the snapshot borrows a view and asks membership
questions of it. <a id="cite-ntfe-identity.principal-view-without-copying-groups"></a> The view is lock-free: group SIDs are fixed at token
creation and each group's attributes are an atomic. <a id="cite-ntfe-identity.principal-view-lock-free"></a>

The judgment compares SIDs and nothing else; what NTFE knows of a SID's
meaning is only what pnp-core compiles into it — the service-SID
derivation and a table of well-known names — used once, at ingestion,
to turn a name a rule wrote into a SID. The engine holds no directory
of principals and resolves no SID back to a name. <a id="cite-ntfe-identity.no-sid-meaning-in-kernel"></a> `Local.Service.Equal
= resolvd` is turned into the service's SID at ingestion by pnp-core,
with the same derivation peinit and authd use to mint it (the SHA-1 of
the uppercased UTF-16LE name under `S-1-5-80`); <a id="cite-ntfe-identity.service-name-to-sid-at-ingestion"></a> `Local.User.Equal =
LocalService` by a table of well-known names. <a id="cite-ntfe-identity.well-known-user-names-by-table"></a> The viewer resolves the
other way, from the service definitions in the registry. <a id="cite-ntfe-identity.viewer-resolves-sids-from-registry"></a>

<a id="trm-6-9-6"></a>

## What the stream says

A `Flow` event and a flow record carry both ends: the kind, the process
GUID, pid and comm, the user SID and the service SID (ABI 4, [NTFE ABI Reference](<~kernel/userspace/native/ntfe/generated-device-abi#trm-6-a>),
[NTFE ABI Notes](<~kernel/userspace/native/ntfe/device-operations-and-errors#trm-6-b>)). <a id="cite-ntfe-identity.event-and-record-carry-both-ends"></a> An end that could not be attributed — a socket with no KACS
state, an inet socket nobody stamped, a loopback sender the inbound
seat could not see — is confessed: `identity_unresolved` in the status,
`PEIOS_NTFE_EV_F_IDENTITY_UNRESOLVED` on the event, and the flag on the
flow record's slot. <a id="cite-ntfe-identity.unattributed-end-confessed"></a>

<a id="trm-6-9-7"></a>

## At rest: the listeners dump

The same stamp, read without a packet: `PEIOS_NTFE_IOC_LISTENERS`
(`listeners.c`) walks the listening TCP hash and the bound UDP and
UDP-Lite tables of the root namespace the way `/proc/net/tcp` and
`/proc/net/udp` do — each bucket under its lock, records copied out
between buckets — and reports every socket prepared to receive with the
identity that governs it. <a id="cite-ntfe-identity.listeners-dump-reports-receivers-with-identity"></a> It is the attack surface as a list, by whom,
and it exercises the stamp before a single flow is judged.

<a id="trm-6-9-8"></a>

## What was decided against

- **Identity in the per-packet layers.** A packet carries no owner; the
  socket does. `Local.*` in a `Packet` rule is linted as never present, <a id="cite-ntfe-identity.local-in-packet-rule-linted-never-present"></a>
  and `Present` on it refuses the generation. <a id="cite-ntfe-identity.present-local-in-packet-rule-refuses-generation"></a>
- **Many sentences for a shared receiver.** Inbound multicast is one
  flow with many endpoints; modelling N judgments would have made the
  join-time question a per-packet one. `shared` and a later gate on
  `IP_ADD_MEMBERSHIP` (C11) instead.
- **Copying the group list into the snapshot.** Up to 1024 SIDs per
  token, in softirq: the `Principal` view answers membership instead.
- **`Program.Trust` and the image hash.** PIP is under review, and
  unsigned binaries are not hashed at exec today; both wait.
