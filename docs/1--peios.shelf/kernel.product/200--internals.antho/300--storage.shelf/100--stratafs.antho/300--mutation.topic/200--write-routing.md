---
title: "Write Routing"
description: "Which single stratum a modification is performed against, when that decision is made, and what shared writable mappings do to it."
type: reference
---

<a id="trm-4-5-1"></a>

An operation that modifies an existing object is performed against
exactly one stratum. This section covers which, and when the decision
is made.

<a id="trm-4-5-1-1"></a>

## Accepting modification <a id="cite-write.accepts-modification"></a>

A stratum **accepts modification** of an object it provides when all
three of the following hold:

- the stratum does not carry `ro`;
- the provider's mount is not read-only;
- the provider's inode is not marked immutable.

<a id="trm-4-5-1-1-1"></a>

### Independence from the caller’s rights <a id="cite-write.routing-does-not-use-caller-rights"></a>

The predicate is a property of the stratum and the object alone. It
takes the superblock, the stratum index and the provider path, and
nothing else — no credentials, no security descriptor, no access
check.

That restriction is load-bearing. Were the predicate to take the
caller's rights into account, a caller *refused* write access by the
provider's descriptor could still provoke a copy-up: the write would
fail, but the copy would have been published, and from then on the
merged path would resolve to a snapshot the provider's legitimate
writer could no longer update. A caller with no write access at all
could freeze any file in the mount.

Note the third term is the immutable inode flag specifically, not
unwritability in general. A file that is unwritable by its mode bits is
routed in place and refused by the underlying filesystem.

<a id="trm-4-5-1-2"></a>

## The rule

The decision itself is `route_existing` in `stratafs-core`, which takes
the provider index, whether it accepts modification, the create index
and whether the create stratum is present, whether the object is of a
copyable type, and whether the stratafs mount itself is read-only. It
selects in-place modification, copy-up, or read-only through the following
ordered checks.

1. If the **mount** is read-only, the route is read-only. This term
   short-circuits everything else. <a id="cite-write.read-only-mount-short-circuits"></a>
2. If the provider accepts modification, the operation is performed
   against the provider's object. <a id="cite-write.in-place-when-provider-accepts"></a>
3. Otherwise, if the object is copyable, a create stratum exists, is
   present, and has **strictly higher precedence than the provider**,
   the object is copied up and the operation performed against the
   copy. <a id="cite-write.copy-up-when-create-outranks"></a>
4. Otherwise the route is read-only and the operation fails with
   `EROFS`. <a id="cite-write.erofs-when-no-writable-stratum"></a>

The strict `create_index < provider` comparison is what stops a
modification being placed where something already present would shadow
it. Where a high-precedence stratum provides a name it will not accept
a write for, there is no lower stratum that can take the write without
the result vanishing behind the provider, so `EROFS` is the honest
answer — reported at the moment of the write rather than discovered
later.

Where the name is held by no stratum, the operation is a creation and
[Creation](<~kernel/internals/stratafs/mutation/creation#trm-4-5-3>) applies instead.

<a id="trm-4-5-1-3"></a>

## When the decision is made

Routing happens as part of a modifying operation, not an ordinary open.
Most mutating entry points call `route_existing` afresh against their
selected provider. Shared write-capable mappings prepare the route before
the memory mapping lock is taken and recheck the selected provider in the
mapping callback. Opening a descriptor does not reserve a writable route.
<a id="cite-write.routed-per-operation"></a>

| Operation | Routes |
|---|---|
| Writing or appending | Yes <a id="cite-write.routes.write"></a> |
| Truncating, or any other `setattr` | Yes <a id="cite-write.routes.setattr"></a> |
| Changing mode, owner, timestamps, or the security descriptor | Yes <a id="cite-write.routes.metadata"></a> |
| Setting or removing an extended attribute | Yes <a id="cite-write.routes.xattr"></a> |
| `fallocate` | Yes <a id="cite-write.routes.fallocate"></a> |
| `splice` into the file | Yes <a id="cite-write.routes.splice"></a> |
| `copy_file_range` and `remap_file_range` | Yes <a id="cite-write.routes.copy-range"></a> |
| Establishing a shared writable mapping | Yes <a id="cite-write.routes.shared-mapping"></a> |
| Reading contents, attributes, or extended attributes | No <a id="cite-write.routes.read-does-not"></a> |
| Opening, for any access | No <a id="cite-write.routes.open-does-not"></a> |
| Taking or releasing a lock, or a lease | No <a id="cite-write.routes.lock-does-not"></a> |

The security descriptor and the system access control list are both
reached as extended attributes, so both route through the `setxattr`
path like any other attribute; there is no descriptor-specific code in
stratafs at all. <a id="cite-write.descriptor-routes-as-xattr"></a>

An open is not itself a routing trigger. `open` computes a route, but
uses it only to decide the flags of the backing open — a non-in-place
route downgrades the provider open to read-only and strips `O_TRUNC`,
deferring rather than deciding. <a id="cite-write.open-defers-routing"></a> The one case in which an open acts is
`O_TRUNC` on a regular file: that is a modification, so it routes, and
copies up or fails with `EROFS` there and then. The truncation itself
is applied afterwards by the VFS through `setattr`, which routes again
and lands on the copy. <a id="cite-write.o-trunc-routes-at-open"></a>

Writes to regular files use the open file description's current
`O_APPEND` setting, including changes made with `F_SETFL` after open or
copy-up. Clearing the flag restores writes at the selected offset and
allows `splice` and range-copy operations to use their explicit offsets.
The provider's append-only restrictions and flag checks still apply.

Routing at operation time rather than at open is what makes the rule
implementable. A filesystem cannot see what an open asked for in
access-mask terms — the caller's descriptor is stamped by KACS before
the filesystem's own open method runs, and its mask lives in a private
blob a filesystem cannot reach. Nor does it need to: the access check
has already happened by the time an operation reaches stratafs, so a
modifying operation arriving here is one its caller was entitled to
perform, and routing it is a decision about strata alone.

<a id="trm-4-5-1-4"></a>

## Shared writable mappings <a id="cite-write.mmap-routes-on-maywrite"></a>

Establishing a shared mapping that can become writable routes before any
bytes are written. Stores through the mapping can then modify its backing
object without another filesystem operation that could perform copy-up.

Preparation applies to regular files mapped with `MAP_SHARED` or
`MAP_SHARED_VALIDATE` through a readable, writable open file description.
This includes `PROT_READ`: the shared mapping retains `VM_MAYWRITE` and can
later gain write access through `mprotect`. Private mappings and shared
mappings that cannot gain write access do not trigger preparation.
Ordinary writable opens remain lazy; opening alone does not copy up a file.

The existing KACS mapping checks run before preparation. Preparation
follows direct StrataFS providers and the selected backing file of FUSE
passthrough mappings. It completes routing and any required copy-up for
each StrataFS layer before the VFS acquires `mmap_lock`. It grants no
additional access, and the backing file's mapping checks still apply.

The mapping callback pins the selected provider and forwards only an
in-place route. If a route change after preparation could require another
copy-up, the mapping fails with `EAGAIN`. Retry the whole `mmap`
call so that preparation runs again. Definitive read-only conditions still
fail with `EROFS`.

A completed copy-up remains published if a later mapping check or provider
callback fails. The same applies if an earlier layer completes copy-up
before preparation fails in a deeper layer. Preparation does not roll back
copies that another operation could already have observed.

<a id="trm-4-5-1-5"></a>

## What a copy-up does to an open descriptor <a id="cite-write.copying-descriptor-follows-copy"></a>

A copy-up performed for one descriptor changes which object provides
the name. That descriptor refers to the copy from then on: it keeps the
inode it was opened against while the inode's backing object becomes
the copy ([Inode Identity and Lifecycle](<~kernel/internals/stratafs/coherency/inode-identity-and-lifecycle#trm-4-4-3>)), and its backing file is replaced.

Every other descriptor already open against the original continues to
refer to the original, and any fresh resolution of the path yields a
new inode standing for the copy. The pre-copy-up file is not closed —
it is retained so that locks and leases taken before the copy-up keep
working ([Locking](<~kernel/internals/stratafs/mutation/locking#trm-4-5-7>)).

<a id="trm-4-5-1-6"></a>

## Special files <a id="cite-write.special-files-never-copied-up"></a>

A FIFO, socket, or device node is opened and written without the
filesystem object being modified: what is written passes to a pipe, a
socket, or a driver, not to the object's contents. Writing to such an
object therefore does not route, and such an object is never copied up
— every routing site gates on the object being a regular file, and the
copyable flag excludes anything that is not a regular file, directory
or symlink.

Copying up a FIFO would sever it: a reader holding the original and a
writer that arrived after the copy would hold two unrelated pipes. A
device node survives copying only by the accident that the copy names
the same device.

Opens, reads and writes are forwarded to the provider whether or not it
accepts modification, since the write-mode downgrade and the `O_TRUNC`
refusal both apply to regular files only. Operations that modify the
object itself — its mode, its descriptor, its extended attributes — do
route, and where the provider does not accept modification they fail
with `EROFS`, because the copy-up branch cannot apply to an object that
is never copied up.

<a id="trm-4-5-1-7"></a>

## `ioctl` <a id="cite-write.ioctl-regular-file-refused"></a>

`ioctl` on a regular file is refused unconditionally with `ENOTTY`, and
its compat form with `ENOIOCTLCMD`. Stored-file `ioctl`s can mutate
data and would need command-by-command routing, which is not
implemented; refusing is the conservative stand-in. `ioctl` on a
non-regular file is forwarded to the provider.
