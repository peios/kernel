---
title: "The Self-Watch"
description: "LCS watches its own configuration through the same machinery userspace uses — what it drives, how it is armed, and why the callback is not the atomicity boundary."
type: reference
---

<a id="trm-5-10-4"></a>

LCS watches its own configuration and layer metadata subtrees, and it
does so through the same machinery userspace uses — but not through the
same interface.

An internal watch is an entry in the same watch map, taking a reference
on the same subtree watch set, distinguished only by a kind marker. It
has **no fd, no granted access mask and no filter**. <a id="cite-self-watch.no-fd-mask-or-filter"></a>

Events reach it through a kernel callback rather than being queued for
a `read()`, and it is therefore not subject to
`NotificationQueueSize`. <a id="cite-self-watch.exempt-from-notification-queue-size"></a>

It is also not subject to `MaxSubtreeWatchDepth`, nor to the
transaction burst suppressor: internal collection happens before either
test. <a id="cite-self-watch.exempt-from-depth-and-burst-limits"></a>

Because there is no filter, deliverability is decided per target rather
than by a bitmask. Each internal target admits only the event types it
cares about: value events on the watched key itself for the
configuration subtrees, and subkey events at depth 0 or value and
descriptor events at depth 1 for the layer metadata subtree. <a id="cite-self-watch.admits-event-types-per-target"></a>

<a id="trm-5-10-4-1"></a>

## What it drives

**Self-configuration.** A change under `Machine\System\Registry\`
triggers a re-read and validation of the parameters ([Operational Parameters](<~kernel/internals/lcs/bootstrap/operational-parameters#trm-5-10-3>)). <a id="cite-self-watch.drives.parameter-re-read"></a>

**The layer table.** A change under `Machine\System\Registry\Layers\`
marks the affected layer names dirty and drives a bounded refresh of
their precedence, enabled state, owner and cached descriptor. Within
one delivery — a transaction's commit, say, whose batch creates a
layer and then writes its three values — each dirty layer is refreshed
once, however many of the batch's events named it. <a id="cite-self-watch.layer-refreshed-once-per-delivery"></a>

**Layer lifecycle.** `SUBKEY_CREATED` and `SUBKEY_DELETED` under
`Layers\` add and remove layers, except for `base`, which is ignored
([The Base Layer](<~kernel/internals/lcs/layers/the-base-layer#trm-5-3-2>)). <a id="cite-self-watch.drives.layer-lifecycle-from-subkey-events"></a>

**KMES configuration.** A third internal watch, on
`Machine\System\KMES\`, exists for KMES's own parameters. <a id="cite-self-watch.drives.kmes-configuration"></a> It is not
LCS configuration, but the registry is where it lives and this is the
mechanism that notices it change.

<a id="trm-5-10-4-2"></a>

## The callback is not the atomicity boundary

For layer metadata, internal delivery identifies which layer names are
dirty. It does not itself publish anything, and it must not: publishing
a layer means publishing its table entry, metadata key GUID and cached
descriptor together ([Layer Metadata](<~kernel/internals/lcs/layers/layer-metadata#trm-5-3-3>)), and a callback that published a partial
entry would create a window in which a layer exists and nobody can be
authorised against it. <a id="cite-self-watch.callback-does-not-publish"></a>

LCS also does not perform source round trips while holding the
watch-map or layer-table publication locks. <a id="cite-self-watch.no-source-round-trip-under-locks"></a> The refresh runs outside
them, after the mutating operation commits and before the syscall
returns.

<a id="trm-5-10-4-3"></a>

## Arming

At bootstrap, LCS resolves the GUIDs for `Machine\System\Registry\` and
`Machine\System\Registry\Layers\` through `RSI_LOOKUP` and arms
targeted subtree watches. <a id="cite-self-watch.arming.targeted-via-rsi-lookup"></a>

If either does not exist — first boot, empty database — it arms a
subtree watch on the `Machine\` hive root instead, so that seed restore
creating the subtree is noticed. <a id="cite-self-watch.arming.fallback-on-machine-root"></a>

That fallback event re-enters the whole bootstrap refresh, which
resolves the specific GUIDs and arms the targeted watches. <a id="cite-self-watch.arming.fallback-event-re-enters-refresh"></a>

In practice the kernel arms both: targeted watches for whichever roots
exist, **plus** the `Machine\` root fallback, until a refresh finds
everything present. <a id="cite-self-watch.arming.mixed-superset"></a> It is a superset of what is needed rather
than a substitute for it.

The same arming covers every key the kernel reads for itself, not only
LCS's own: KMES configuration, the port reservation table
(`Machine\System\Network\TcpIp\PortReservations\`, see the KACS
chapter on network objects), the network policy key
(`Machine\System\Network\`, whose rules and inventory the packet
engine reads — see the network policy chapter) and the event emission
policy (`Machine\Generic\Events\`, see the KMES chapter) are
discovered in the same refresh and get the same targeted-or-fallback
treatment. <a id="cite-self-watch.arming.covers-every-kernel-read-key"></a>

The two policy watches are the depth-unbounded, every-mutation ones.
For the network policy, rules are keys and exceptions are subkeys, so
anything written anywhere beneath the key may be policy. <a id="cite-self-watch.arming.policy-watch-is-depth-unbounded"></a>
The emission policy has a key per event-type segment at any depth, and
its watch passes on only changes on `Events` itself, beneath the
kernel's own roots, and to `Enabled` values (KMES [Emission Policy](<~kernel/internals/kmes/emission-policy#trm-2-8>)).

**A refresh that fails still arms the fallback.** A stage can fail
transiently — a source answering a lookup while a concurrent write has
half-created a key was the case that found this — and if the refresh
simply returned, no watch would exist and no kernel-read key would load
for the life of the boot. So when any stage before arming fails, LCS
arms the `Machine\` root fallback alone: the next subkey creation under
the hive re-enters the refresh, which then arms the targeted watches as
above. <a id="cite-self-watch.arming.failed-refresh-arms-fallback-alone"></a>

The failure and the fallback arm are both traced by
`lcs:lcs_bootstrap_refresh`. <a id="cite-self-watch.arming.failure-is-traced"></a>

<a id="trm-5-10-4-4"></a>

## Bootstrap interaction

1. A source registers. LCS reads `Machine\System\Registry\*`; the keys
   do not exist; compiled-in defaults are retained.
2. Seed restore populates them. The subtree watch fires, LCS validates
   and hot-swaps to the seed values.
3. Subsequent administrative changes fire the watch again, and LCS
   validates and hot-swaps, or rejects with an audit event.

At no point is there a state in which LCS is waiting for
configuration.
