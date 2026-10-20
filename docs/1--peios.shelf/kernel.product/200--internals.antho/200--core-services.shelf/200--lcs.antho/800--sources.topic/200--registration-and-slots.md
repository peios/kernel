---
title: "Registration and Slots"
description: "Reaching LCS through /dev/pkm_registry — what registration validates, how source slots work, and resuming one that went Down."
type: reference
---

<a id="trm-5-8-2"></a>

A source reaches LCS through `/dev/pkm_registry`. The device's `open()`
handler checks the calling thread's effective token for an **enabled**
`SeTcbPrivilege` and returns `EPERM` without it, so an unprivileged
process cannot obtain an fd to the device at all. <a id="cite-source.register.open-requires-enabled-setcbprivilege"></a>

Having opened it, the source issues `REG_SRC_REGISTER`, naming the
hives it backs, the root GUID of each, the highest sequence number it
has persisted, and per-hive flags and scope GUID. On success it enters
the request loop: `read()` for requests, `write()` for responses.

<a id="trm-5-8-2-1"></a>

## What registration validates

- Every hive name is valid and is not the reserved `CurrentUser`
  ([Hives and Routing](<~kernel/internals/lcs/data-model/hives-and-routing#trm-5-2-1>)). <a id="cite-source.register.hive-name-valid-and-not-currentuser"></a>
- No route identity — the folded name paired with its scope — collides
  with one held by another **Active** source. <a id="cite-source.register.no-route-identity-collision"></a>
- Private hive collisions are scoped: the same name in different scopes
  is fine ([Private Hives](<~kernel/internals/lcs/data-model/private-hives#trm-5-2-2>)). <a id="cite-source.register.private-hive-collisions-are-scoped"></a>
- A hive's root GUID is not nil. <a id="cite-source.register.root-guid-not-nil"></a>
- The root GUIDs within one request are distinct from each other. <a id="cite-source.register.root-guids-distinct-within-request"></a>
- A hive without `RSI_HIVE_PRIVATE` carries no scope GUID. <a id="cite-source.register.scope-guid-only-for-private-hive"></a>
- No unknown flag bits are set. <a id="cite-source.register.no-unknown-flag-bits"></a>
- The hive count is within `MaxHivesPerSource` (64), and the source
  count is within `MaxRegisteredSources` (32). Either limit is `ENOSPC`;
  a zero hive count is `EINVAL`. <a id="cite-source.register.hive-and-source-counts-are-enospc"></a>
- The reported maximum sequence can be advanced past without
  overflowing 64 bits, or registration fails `EOVERFLOW` and the source
  is never made Active ([The Sequence Counter](<~kernel/internals/lcs/layers/the-sequence-counter#trm-5-3-7>)). <a id="cite-source.register.max-sequence-overflow-is-eoverflow"></a>

Root GUIDs are checked for uniqueness within one request, and against
every existing slot, Active or Down: a request whose root GUID is
already the root of a differently-named hive is refused `EEXIST`. A
same-named hive is decided by the identity rules above instead. The
already-registered state is also checked for consistency, and a table
that ever held two hives with one root would fail that check on every
later registration and path walk, which is why admission refuses it. <a id="cite-source.register.root-guids-compared-across-slots"></a>

<a id="trm-5-8-2-2"></a>

## Source slots

Successful registration creates a **source slot**: the kernel object
owning one connection and the hive set registered on it. <a id="cite-source.register.success-creates-a-slot"></a>

Each registered hive has a stable identity — its folded name, its
visibility, its scope GUID for a private hive, and its root GUID. <a id="cite-source.register.hive-identity-fields"></a>

**Down slots keep their identities reserved.** A crash or an fd close
marks the slot Down; it does not unregister anything and does not
retire any hive identity. <a id="cite-source.register.down-slot-keeps-its-identities"></a>

Slots are never freed, and collision checks see Down slots as well as
Active ones. <a id="cite-source.register.collision-checks-see-down-slots"></a>

Status is a property of the slot, not of an individual hive. A source's
hives go Down together. <a id="cite-source.register.status-is-per-slot"></a>

<a id="trm-5-8-2-3"></a>

## Resuming a Down slot

A new process may take over a Down slot if it holds `SeTcbPrivilege`
and registers **exactly the same hive set**: the same folded name,
visibility, scope GUID and root GUID for every hive, and the same
number of them. Partial resume is rejected. <a id="cite-source.register.resume-requires-exact-hive-set"></a>

The distinction between the failures matters. A request whose only
mismatch is stale identity data — a different root GUID for an
otherwise-matching hive — fails `ESTALE`. <a id="cite-source.register.stale-root-guid-is-estale"></a>

Other partial or malformed resume attempts fail `EINVAL`. <a id="cite-source.register.other-resume-mismatch-is-einval"></a>

`EEXIST` is reserved for a collision with an **Active** slot; it never
comes from a Down-slot collision. <a id="cite-source.register.eexist-only-from-active-collision"></a>

When both an Active collision and a stale Down slot apply, `EEXIST`
wins. <a id="cite-source.register.eexist-wins-over-estale"></a>

New hives cannot be added by mutating a Down slot during a resume — the
hive set has to match exactly, so a superset simply fails, and a new
hive needs a new slot. There is no implicit retirement of a Down slot;
retiring one would need an explicit administrative operation, and none
exists. <a id="cite-source.register.no-implicit-down-slot-retirement"></a>

A replacement source is authenticated by `SeTcbPrivilege`, not by
process identity. Nothing records a pid, and nothing could usefully:
process identity does not survive a crash and restart. <a id="cite-source.register.resume-authenticated-by-privilege-not-pid"></a>

<a id="trm-5-8-2-4"></a>

## Coming back

On a successful resume the slot becomes Active, its restart generation
advances, and LCS replays any layer deletions that were pending. <a id="cite-source.register.resume-activates-slot-and-replays"></a>

LCS then delivers `OVERFLOW` to every armed watch on that source
([Dispatch](<~kernel/internals/lcs/watches/dispatch#trm-5-6-3>)).

Existing key fds resume working without being reopened. Each carries
the restart generation it last saw; when it notices a change it
re-reads its key and continues. <a id="cite-source.register.key-fds-survive-a-resume"></a>

If the key's GUID no longer exists in the restarted source — the
database was restored from an older backup, say — that first operation
returns `ENOENT` and the fd is marked orphaned. <a id="cite-source.register.missing-guid-after-resume-orphans-fd"></a>
