---
title: "Dependencies and boot sequence"
description: "The registry has to configure itself — the three circular dependencies, and the three rules that break them."
type: reference
---

<a id="trm-5-10-1"></a>

The registry is the configuration store for the whole system, and it
has to configure itself. Three circular dependencies have to be broken
before it can serve anyone.

**peinit needs the registry to start services, but the registry source
is a service.** Service definitions live in the registry, and the
process that would serve them has not started.

**LCS needs operational parameters from the registry, but the registry
needs LCS.** Timeouts, caps and limits live under
`Machine\System\Registry\`, in a hive LCS itself routes.

**A fresh install has no data at all.** The source's database is empty;
there is nothing to read.

Three rules break all three.

<a id="trm-5-10-1-1"></a>

## Rule 1: compiled-in defaults

Every operational parameter has a compiled-in default, and LCS runs on
those defaults from the moment PKM initialises. <a id="cite-boot.defaults-active-from-init"></a>

There is no "waiting for configuration" state, no flag, and no wait
queue: the limits structure is statically initialised at load, the
source char device is registered without consulting configuration, and
the first attempt to read configuration happens on a workqueue after a
source has already registered. <a id="cite-boot.no-waiting-for-configuration-state"></a>

Before any source registers, the routing table is empty, so every
operation that names a hive returns `ENOENT`. <a id="cite-boot.empty-routing-table-enoent"></a>
That is the only sense in which LCS is not yet useful, and it is not a
distinct state — it is just an empty table.

<a id="trm-5-10-1-2"></a>

## Rule 2: the base layer exists unconditionally

The base layer is a static constant in the kernel: name `base`,
precedence 0, enabled. It is handed out whenever the dynamic layer
table is empty and is always written first into every layer snapshot.

A source that registers with an entirely empty database is fully
functional, because the one layer that writes need is not in the
database. Persisted metadata under
`Machine\System\Registry\Layers\base\` may exist and may decorate the
base layer, but it is not required and cannot contradict it ([The Base Layer](<~kernel/internals/lcs/layers/the-base-layer#trm-5-3-2>)).

<a id="trm-5-10-1-3"></a>

## Rule 3: hot-swap, not restart <a id="cite-boot.hot-swap-not-restart"></a>

When configuration becomes available, LCS reads it, validates it, and
swaps the values in place. It does not restart, re-initialise, or
block. The whole transition from compiled-in defaults to registry-backed
configuration is driven by the internal self-watch ([The Self-Watch](<~kernel/internals/lcs/bootstrap/the-self-watch#trm-5-10-4>)).

<a id="trm-5-10-1-4"></a>

## Source dependencies are the source's problem <a id="cite-boot.source-dependencies-not-lcs-concern"></a>

LCS neither knows nor cares what a source depends on. A source that
needs the root filesystem, a SYSTEM token, or a particular kernel
feature arranges that for itself. LCS's only requirement is that the
process can open `/dev/pkm_registry` and speak RSI.

<a id="trm-5-10-2"></a>

<a id="trm-5-10-2-1"></a>

## Normal boot <a id="cite-boot.normal-sequence"></a>

```
Kernel boots
  → PKM initialises; LCS runs on compiled-in defaults
  → /dev/pkm_registry registered
  → the base layer exists in memory

A source registers — loregd, started by peinit
  → opens /dev/pkm_registry (SeTcbPrivilege checked at open)
  → REG_SRC_REGISTER: hive names, root GUIDs, max persisted sequence
  → LCS initialises or advances next_sequence to max + 1

Bootstrap refresh is queued
  → resolve Machine\System\Registry     → read and hot-swap parameters
  → resolve Machine\System\Registry\Layers → populate the layer table
  → arm internal subtree watches
```

The bootstrap refresh runs on a workqueue after `REG_SRC_REGISTER`
returns, so registration never blocks on configuration and a source
that registers can start answering immediately. <a id="cite-boot.refresh-on-workqueue-after-register"></a>

The refresh is triggered by the arrival of a **global hive named
`Machine`**. <a id="cite-boot.refresh-triggered-by-machine-hive"></a> That name is matched case-insensitively in the
kernel and is one of the two hive names LCS knows about; the other is
`Users`, the target of `CurrentUser\` rewriting ([Hives and Routing](<~kernel/internals/lcs/data-model/hives-and-routing#trm-5-2-1>)). Neither is a
routing decision — routing is entirely dynamic — but the claim that the
kernel holds no hive names at all would not be true.

<a id="trm-5-10-2-2"></a>

## First boot <a id="cite-boot.first-boot-retains-defaults"></a>

An empty source has no `Machine\System\Registry` to read.

```
Source detects an empty database on first startup
  → generates root GUIDs for the hives it backs
  → creates root key records with their default SDs
  → persists them, then registers with LCS

LCS resolves Machine\System\Registry → does not exist
  → compiled-in defaults retained
  → subtree watch armed on the Machine\ hive root instead

peinit notices the registry is empty and restores the seed backup.
That is peinit's decision, not LCS's.

Seed restore populates Machine\ through REG_IOC_RESTORE
  → the fallback subtree watch fires
  → LCS re-runs the bootstrap refresh: resolves the specific GUIDs,
    re-arms targeted watches, validates and hot-swaps the seed values,
    and re-reads layer metadata
```

Hive root Security Descriptors are set by the source, not by LCS. LCS
holds no template for them and enforces whatever the source stores
([Inheritance and Hive Roots](<~kernel/internals/lcs/security/inheritance-and-hive-roots#trm-5-4-3>)).

<a id="trm-5-10-2-3"></a>

## Watch arming in practice

The spec-level description above says the fallback watch is armed
*instead of* the targeted ones. What the kernel actually arms is a
**mixed** set: targeted watches on whichever of the two roots exist,
*plus* the `Machine\` root fallback. The fallback is a superset rather
than a substitute, and it stays armed until a refresh finds both roots
present.

A third internal watch is armed by the same sequence, on
`Machine\System\KMES`, which is not LCS configuration at all — it is
how KMES picks up its own parameters from the registry LCS serves.

<a id="trm-5-10-2-4"></a>

## The bootstrap contract

Four properties hold throughout and are relied on elsewhere:

1. **LCS is always operational with compiled-in defaults.** It accepts
   syscalls from the moment PKM initialises.
2. **The base layer requires no persisted state.**
3. **Hot-swap is the only configuration transition.** LCS never blocks,
   restarts, or re-initialises.
4. **Source dependencies are the source's concern.**
