---
title: "Descriptor storage and caching"
description: "Descriptor storage and caching: behaviour and implementation of the Peios kernel."
type: reference
---

<a id="trm-3-9-5"></a>

<a id="trm-3-9-5-1"></a>

## Xattr protection <a id="cite-facs.storage.xattr-protection"></a>

FACS intercepts every raw xattr operation on the canonical descriptor
xattr — `security.peios.sd`, or `system.ntfs_security` on NTFS — and
denies all three directions. An NTFS inode with no `$Secure` entry,
whose descriptor is an inline attribute the driver never reads, counts
as carrying no descriptor: the mount's missing-descriptor policy
decides for it, as it does for a file with no `security.peios.sd`.

**Writes** are denied: all modification goes through the set-security
interface. **Removal** is denied: a descriptor is never detached from
a file. And **reads** are denied, which is the least obvious of the
three and the most important. <a id="cite-facs.storage.xattr-read-denied"></a> The raw xattr holds the entire
descriptor including the SACL, so allowing a read under
`READ_CONTROL` alone would leak SACL content that properly requires
`ACCESS_SYSTEM_SECURITY`. All reads go through `kacs_get_sd`, which
distinguishes the two.

<a id="trm-3-9-5-2"></a>

## Caching

A validated, parsed descriptor object is cached in the inode's LSM
blob, holding immutable self-relative bytes together with a
prevalidated component layout — enough for AccessCheck readers never
to reparse untrusted storage bytes. <a id="cite-facs.storage.cache-parsed-in-inode-blob"></a>

**Readers** on the AccessCheck path use the RCU-published pointer.
Once a current entry exists, a reader does not take the inode mutex
merely to run AccessCheck. <a id="cite-facs.storage.readers-rcu-no-mutex"></a> It either completes the evaluation inside
an RCU read-side critical section, or pins the object with a refcount
while still under RCU and drops the RCU lock before doing anything
that can allocate, sleep or emit an audit event. A pin is acquired
with a non-zero refcount check and dropped afterwards.

**Writers** allocate a new object, swap the pointer atomically, and
free the old one after a grace period and after reader pins have
drained. <a id="cite-facs.storage.writers-rcu-swap"></a> No partial read is possible.

**Population** is lazy, on first access. The xattr is read through an
internal kernel path that bypasses the read-denial hook, and the
parsed result is installed by compare-and-swap; a thread that loses
the race frees its own copy. <a id="cite-facs.storage.population-lazy-cas"></a>

Both native and legacy open finish descriptor-cache resolution before
acquiring the central access policy (CAAP) cache mutex. Resolution can take
an inode security mutex, while set-security takes that inode mutex before
CAAP; acquiring them in the opposite order could deadlock an open against a
descriptor update. <a id="cite-facs.storage.open-resolves-before-caap"></a> Open retains a pin on the immutable descriptor
selected by that resolution, before releasing the protection used to select
it. The pin survives the subsequent CAAP wait and access check. Clearing or
replacing the inode's cache after selection cannot by itself cause a spurious
denial or change which descriptor this open evaluates; a later open resolves
again and can select the replacement. A missing or corrupt selected entry
still fails closed. <a id="cite-facs.storage.open-pins-selected-descriptor"></a>

CAAP is evaluated under its own, later cache lock; the descriptor selection
and CAAP evaluation are not an atomic snapshot of both policies. The inode
mutex is not held for the access check, and CAAP is not held across lazy
descriptor population.

**Eviction** frees the cached descriptor when the inode is evicted,
through an RCU-safe callback with the same pin draining, so in-flight
permission checks complete before the object goes away. <a id="cite-facs.storage.eviction-rcu-safe"></a>

**Invalidation** happens on write, but not atomically with it. The
set-security path deliberately releases the inode security lock across
the xattr write and re-acquires it afterwards to publish the new
parsed object, because holding it across the write would invert the
`i_rwsem` ordering the access path requires. <a id="cite-facs.storage.setsd-releases-lock-across-write"></a> Two concurrent
set-security calls on one inode are therefore last-writer-wins rather
than serialised end to end, and there is a window in which the xattr
and the cache disagree. <a id="cite-facs.storage.concurrent-setsd-last-writer-wins"></a> Readers are never blocked, and no reader sees
a partially written object — the exposure is which of two racing
writes lands, not a torn state.

Invalidation is also driven from the **other end**, by the write
itself: any canonical descriptor xattr landing on an inode drops that
inode's cached entry, whoever wrote it and by whatever path. <a id="cite-facs.storage.xattr-write-drops-cache"></a> The
set-security path above then publishes the new parsed object as usual;
for anything else, the next reader re-reads the authoritative bytes.

This is keyed on the xattr rather than on the writer, because the
writer is not always the one holding the cache. A descriptor set
through a stacking filesystem reaches **two** inodes — the one the
caller named, and the real one beneath, which the write is re-entered
on. <a id="cite-facs.storage.stacking-two-inodes"></a> Only the first is refreshed by the set-security path. The second
is not merely cold: a stacking filesystem resolves and caches
descriptors during its own metadata work on an inode it has just
created, so it can hold an entry from the moment the object existed
and keep serving it after the xattr underneath has changed. Keying on
the xattr closes that without either side needing to know the other is
there.

<a id="trm-3-9-5-7"></a>

## Missing descriptors <a id="cite-facs.storage.deny-missing-denies"></a>

Under **`facs_deny_missing`**, no descriptor means deny. Two
exceptions keep the repair path open. `SeChangeNotifyPrivilege`
bypasses intermediate traverse checks including on directories with no
descriptor, though not explicit `chdir()`, `chroot()` or `fchdir()`
use-time checks. And `O_PATH` opens bypass the open hook entirely, so
a file with a missing descriptor can still be acquired as an `O_PATH`
reference — which is exactly the repair route: `open(path, O_PATH)`
then `kacs_set_sd` with `AT_EMPTY_PATH` under `SeRestorePrivilege`. <a id="cite-facs.storage.missing-repair-route"></a>

Under the **synthesise classes**, a missing descriptor is generated
from two sources in order. <a id="cite-facs.storage.synthesis-order"></a> First, **inheritance from the parent**: if
the parent has one, the inheritance algorithm runs as though a new
file were being created. Otherwise the **mount-level template**,
applied where there is no parent descriptor — typically only at the
mount root. With no template configured, the fallback grants
`GENERIC_ALL` to SYSTEM and `BUILTIN\Administrators` and
`GENERIC_READ | GENERIC_EXECUTE` to Everyone, owned by SYSTEM with
SYSTEM as group. <a id="cite-facs.storage.synthesis-fallback-descriptor"></a>

Because these files already exist, the accessor is not their creator.
Where inheritance needs creator inputs — owner, primary group, default
DACL — a synthetic system-policy creator supplies them: the template's
owner, group and DACL if one exists, the fallback's otherwise. **The
accessor's token never affects the synthesised descriptor**, and the
synthesis path takes no subject token at all. <a id="cite-facs.storage.synthesis-ignores-accessor"></a>

Inheritance is recursive — a parent whose own descriptor is missing is
synthesised first, walking toward the mount root where the template
terminates it. <a id="cite-facs.storage.synthesis-recursive"></a> The walk is bounded at 32 ancestor levels; a target
nested deeper than that below the nearest resolvable ancestor fails
closed with `EACCES` rather than synthesising. <a id="cite-facs.storage.synthesis-depth-limit"></a>

Resolution does not nest FACS inode locks. It releases the current inode's
lock before resolving an ancestor or calling the filesystem's descriptor
xattr handler, which may itself resolve a lower inode in a stacked
filesystem. Referenced dentries and immutable descriptor-cache entries keep
the inputs alive across that work. <a id="cite-facs.storage.resolution-no-nested-inode-locks"></a>

Before publishing the result, resolution reacquires the inode lock and
checks both the mount-policy generation and the inode's cache mutation
sequence. An explicit replacement or invalidation makes it discard the
obsolete result and retry, including when an empty cache was populated and
cleared or invalidated while still empty. Ordinary cached files also retry
a competing reader publication, then use the current entry. A failed reread
never makes an entry from an old policy generation current again.
<a id="cite-facs.storage.resolution-revalidates-unlocked-work"></a>

StrataFS re-reads the current provider descriptor on every check, including
when an earlier result was missing or corrupt. Concurrent reader publication
does not restart these reads: without an explicit invalidation or policy
change, N checks perform N descriptor reads (each may query size and then
bytes). A reader may reuse a result published by another reader whose read
began later than its own; an older read cannot overwrite that later result,
including a missing or corrupt result. Its own read error is still returned.
Explicit writes and policy changes continue to trigger revalidation and may
require another read. This does not alter the fixed deny-missing policy or a
handle's frozen grant. <a id="cite-facs.storage.stratafs-read-contention"></a>

An **ephemeral** synthesis is cached in the inode blob only and never
written back, leaving the original filesystem unmodified. <a id="cite-facs.storage.ephemeral-not-written-back"></a> A
**persistent** one is additionally written to the xattr so the medium
acquires durable descriptors — but never inline. <a id="cite-facs.storage.persistent-written-back"></a>

<a id="trm-3-9-5-8"></a>

## Deferred write-back <a id="cite-facs.storage.write-back-deferred"></a>

Writing the xattr takes the inode's `i_rwsem`. Synthesis may be reached
from a metadata operation whose VFS caller already holds that lock, so
inline write-back would self-deadlock even though resolution releases its
FACS inode lock around parent resolution and xattr reads. Write-back
therefore runs with no FACS or VFS lock held.

Synthesis caches the descriptor immediately and marks the entry
pending. <a id="cite-facs.storage.synthesis-marks-pending"></a> The access decision is correct from that cached value the
instant synthesis completes — correctness never depends on the xattr
reaching disk. The write-back runs later from a task-work callback
firing as the triggering syscall returns to userspace, so a persistent
descriptor is normally on disk by the time the operation that first
observed it missing returns. <a id="cite-facs.storage.write-back-task-work"></a>

A pending entry is generation-tagged exactly like an ephemeral one, so
a policy or template change before the write-back discards it and
re-synthesises; a stale pre-change descriptor is never pinned to disk.

Write-back is best-effort, and can be because the synthesised
descriptor is a deterministic function of the parent or the template —
the on-disk xattr is a cache of a recomputable value, not unique
state. If it does not happen, because the entry was evicted or the
task exited first, the identical descriptor is re-synthesised on next
access and retried. A failed or skipped write-back never fails the
operation that triggered synthesis. <a id="cite-facs.storage.write-back-best-effort"></a> Kernel threads, and a failure to
queue the callback, fall back to re-synthesis the same way.

Once written, the cached entry becomes an ordinary xattr-backed
descriptor: durable, no longer generation-tagged, never synthesised
again, and owed no further write-back. <a id="cite-facs.storage.written-back-becomes-ordinary"></a>

An ancestor synthesised only to supply inheritance inputs for a
descendant is itself pending, and persists under the same rules when
it is next accessed in its own right. <a id="cite-facs.storage.ancestor-also-persists"></a>

<a id="trm-3-9-5-9"></a>

## Corrupt descriptors <a id="cite-facs.storage.corrupt-fails-closed"></a>

A descriptor xattr that exists but fails structural validation is
corrupt, and the policy is fail-closed: deny all access, do not call
AccessCheck, and never treat a truncated DACL as an empty one.

Every encounter emits an audit event, fired exactly once per inode per
cache population rather than per access, so a hot corrupt inode does
not flood the log. <a id="cite-facs.storage.corrupt-audit-once-per-population"></a>

Recovery is a process holding `SeRestorePrivilege` calling
set-security to overwrite it. Offline repair tools can also rewrite
xattrs directly on an unmounted filesystem.

<a id="trm-3-9-5-10"></a>

## NFS client mounts <a id="cite-facs.storage.nfs-dual-authority"></a>

NFS is the one managed class where the sole-authority guarantee does
not hold. The server enforces its own access control independently:
FACS evaluates locally against a synthesised descriptor, and the
server may deny I/O that FACS allowed. A locally authorized `open()`
can therefore produce a descriptor whose `read()` calls fail. This is
inherent to network filesystems with server-side enforcement, and
nothing suppresses the server's denial.

## Related explanations

- [Mount classes and bootstrap descriptors](<~kernel/internals/kacs/file-security/mount-classes-and-bootstrap-descriptors>)
