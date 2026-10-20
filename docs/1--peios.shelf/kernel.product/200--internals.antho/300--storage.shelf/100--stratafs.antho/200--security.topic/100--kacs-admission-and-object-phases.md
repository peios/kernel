---
title: "KACS admission and object phases"
description: "KACS admission and object phases: behaviour and implementation of the Peios kernel."
type: reference
---

<a id="trm-3-9-7"></a>

StrataFS copy-up is the internal realisation of an operation already
authorized against a StrataFS handle — not a second caller-requested
operation. KACS therefore provides a kernel-internal context so that
the mechanics of copy-up introduce no new rights checks against the
task that happens to execute them.

The context exempts **KACS caller authorization only**. It does not
replace credentials, borrow an identity, grant a privilege, bypass
another LSM, neutralise an underlying filesystem check, make a
read-only mount writable, or suppress immutable, append-only, quota,
space, I/O or format errors. <a id="cite-facs.stratafs-copy-up.exempts-kacs-only"></a> Every exemption is a return before the
authorize call, and every mutation still goes through the ordinary
`vfs_*` path under `mnt_want_write()`. <a id="cite-facs.stratafs-copy-up.mutations-via-vfs"></a>

<a id="trm-3-9-7-1"></a>

## Admission and lifetime

Only the in-kernel StrataFS implementation can create or enter a
context. There is no userspace surface of any kind — no ABI, file
descriptor, token, ioctl, syscall or securityfs control — and the
copy-up API is declared in a kernel-private header with no exported
symbols. <a id="cite-facs.stratafs-copy-up.no-userspace-surface"></a>

A context is created only after the StrataFS operation requiring
copy-up has passed its complete outer authorization. KACS does not
verify that: the context creation call performs no check, and the
ordering is satisfied by StrataFS calling in the right order. <a id="cite-facs.stratafs-copy-up.creation-performs-no-check"></a> The
context is not itself an alternative authorization path.

The exemption covers namespace creation the outer handle authorises
without an add-entry right on the create stratum, so the context is
reachable only from a create-enabled mount established by a caller
holding `CAP_SYS_ADMIN` in the **initial** user namespace. That
closure rests on an explicit test of the mounter's user namespace at
stack establishment — the capability half contributes nothing to it,
because the KACS switchboard discards the target namespace and answers
from `SeTcbPrivilege` alone ([DAC Neutralisation](<~kernel/internals/kacs/linux-credentials/dac-neutralisation#trm-3-10-2>)). The check is made when the
immutable stack is established rather than when a copy-up runs, so
descriptor delegation cannot reintroduce acting-task authorization.
Reconfiguration cannot re-supply the strata list.

A context attaches to at most one task, and a task carries at most
one. <a id="cite-facs.stratafs-copy-up.one-context-per-task"></a> It is not inherited by `fork()`, `clone()` or `execve()` — exec
explicitly clears it. <a id="cite-facs.stratafs-copy-up.not-inherited"></a> A refcounted context can be transferred to a
kernel worker, but the originating task leaves it first. <a id="cite-facs.stratafs-copy-up.worker-transfer"></a> Leaving,
task exit, every error path, and completion all remove the attachment
and clear any armed phase. <a id="cite-facs.stratafs-copy-up.detach-clears-phase"></a>

The interface fails closed on nesting, concurrent attachment, a stale
phase, or an object mismatch. <a id="cite-facs.stratafs-copy-up.fails-closed-on-misuse"></a> A mismatched operation is evaluated
normally and neither consumes nor broadens the armed exemption. <a id="cite-facs.stratafs-copy-up.mismatch-evaluated-normally"></a>

<a id="trm-3-9-7-2"></a>

## Object and phase binding

Creation pins the exact provider path, its current inode, a complete
validated copy of its effective descriptor, and the provider-visible
`security.capability` value or its absence. <a id="cite-facs.stratafs-copy-up.creation-pins-provider"></a> Every later positive path
is paired with a pinned inode as well — retaining a dentry alone is
insufficient, because an unlink followed by recreation can
reinstantiate it over a different inode. <a id="cite-facs.stratafs-copy-up.paths-paired-with-inode"></a>

One phase is armed at a time: <a id="cite-facs.stratafs-copy-up.one-phase-armed"></a>

| Phase | Objects admitted |
|---|---|
| Source read | The pinned provider only. |
| Create | One pinned provider, one destination parent, and either one named negative dentry or one anonymous creation in that parent. Used for both parent materialisation and the staged object. |
| Populate | The pinned provider and the one staged object bound to the context. |
| Publish by link | The bound staged object, one destination parent, one absent destination dentry. |
| Publish by rename | The bound staged object and its parent, one destination parent, one absent destination dentry. |
| Cleanup | One bound staging or materialisation dentry and its exact parent. |
| Orphan cleanup | One positive provider dentry carrying an authenticated stale staging marker, and its exact parent. |
| Orphan-marker cleanup | The exact positive provider dentry whose authenticated stale marker is being removed after publication. |

Path, dentry, inode, parent, object type and operation kind are all
compared wherever the hook supplies them — and path comparison
includes the mount, so the same dentry reached through a different
mount of the same superblock does not match. <a id="cite-facs.stratafs-copy-up.match-includes-mount"></a> An inode-only hook can
match the pinned inode, but that does not authorize a pathname
operation on another dentry, and a phase never acts as a wildcard for
other objects of the same filesystem or directory. <a id="cite-facs.stratafs-copy-up.no-wildcard-matching"></a>

The staged binding stays valid only while its dentry names the pinned
inode under the pinned staging parent, and that parent still names its
own pinned inode. A rename or parent substitution invalidates the
populate, protected-metadata and publish exemptions even when the
staged dentry and inode are themselves unchanged. <a id="cite-facs.stratafs-copy-up.rename-invalidates-binding"></a>

Named creation is bound to the exact final component. <a id="cite-facs.stratafs-copy-up.named-creation-exact-component"></a> Anonymous
creation is bound to its parent, expected object type, the attached
task, and the single armed create phase — and once created, the
anonymous object has to be bound as the staged object before populate,
publish or cleanup can use it. <a id="cite-facs.stratafs-copy-up.anonymous-must-be-bound"></a>

Where the destination is a stacking filesystem creating a real inode
below the armed destination dentry, the transition is authenticated at
the exact outer dentry, and only the one subsequent real-inode
security initialisation of the expected type receives the pinned
provider descriptor. <a id="cite-facs.stratafs-copy-up.stacking-transition-authenticated"></a> The real inode is not the staged binding: the
outer inode is separately anchored, through the matching post-create
event for an anonymous object or an explicit confirmation of the exact
positive outer dentry for a named one. A missing, repeated, mismatched
or out-of-order transition fails closed, and an inner post-create
event from the real filesystem is rejected as the outer anchor by
superblock comparison. <a id="cite-facs.stratafs-copy-up.transition-out-of-order-fails"></a>

KACS retains the exact path, inode, parent path and parent inode of
every named object whose creation it admits. Cleanup can be armed only
for one of those or for the exact bound staging object; an unrelated
positive dentry fails with `ESTALE`. <a id="cite-facs.stratafs-copy-up.cleanup-victim-restricted"></a> The cleanup setup call is not
itself authority to choose a deletion victim.

After an atomic rename or link publishes the staged inode, the staging
identity can be rebound to the published path, but only while mount,
inode, parent dentry and pinned parent inode all still match. <a id="cite-facs.stratafs-copy-up.rebind-conditions"></a> The
rebind API exists and is **not called** by StrataFS: the link case is
rebound internally by the publish path, and the rename case relies on
publish preserving the dentry. <a id="cite-facs.stratafs-copy-up.rebind-unused"></a> That holds because publication always
renames within a single parent. A cross-directory publish rename would
silently invalidate the staging binding, since the rename-publish
entry point does not require the destination parent to equal the
staging parent — currently unreachable, but the guard is the caller's
discipline rather than the interface's.

Named staging entries carry `security.peios.stratafs_staging`.
Caller-originated writes and removals of it are denied. <a id="cite-facs.stratafs-copy-up.staging-marker-writes-denied"></a> A write or
removal is admitted only on the exact bound staging inode during
populate, or on the exact orphan-marker object during authenticated
recovery — where the predicate admits a *write* as well as a removal,
being shared between the setxattr and removexattr hooks. <a id="cite-facs.stratafs-copy-up.staging-marker-admission"></a> Probing the
marker for recovery is a kernel-only raw read conveying no caller
authority, and orphan deletion is bound to the exact dentry, inode,
parent dentry and parent inode supplied when the phase was armed, so
an arbitrary name sharing the staging prefix never matches. <a id="cite-facs.stratafs-copy-up.orphan-deletion-exact-binding"></a> Recovery
processes at most 128 entries per batch.

<a id="trm-3-9-7-3"></a>

## Exempt operations <a id="cite-facs.stratafs-copy-up.exempt-operations"></a>

For a matching object in a matching phase, the ordinary AccessCheck,
cached-grant check, privilege check and caller-access audit decision
are omitted at these points:

| Copy-up action | Enforcement points |
|---|---|
| Open and read provider data or a symlink target | `security_inode_permission`, `security_file_open`, `security_file_permission`, `security_inode_readlink` |
| Read provider attributes and extended attributes | the inode and file getattr, setattr-preflight, getxattr and listxattr paths as applicable |
| Create a staged file, directory or symlink, and materialise parents | `security_inode_permission`, `security_inode_create`, `security_inode_mkdir`, `security_inode_symlink`, `security_inode_init_security`; for a stacking destination also `security_dentry_create_files_as` and, for an anonymous object, `security_inode_post_create_tmpfile` |
| Populate staged data, attributes and eligible non-descriptor xattrs | `security_inode_permission`, `security_file_open`, `security_file_permission`, the inode and file setattr paths, setxattr and removexattr. `security.capability` uses only the dedicated clone call below. |
| Publish | `security_inode_permission` on the exact staged object or destination parent, then `security_inode_link` or `security_inode_rename` |
| Remove staging or roll back materialised entries | `security_inode_permission` on the exact parent, then `security_inode_unlink` or `security_inode_rmdir` |

A `security_inode_permission` or `security_file_permission` match also
matches the requested mask. <a id="cite-facs.stratafs-copy-up.mask-must-match"></a> Provider access is
read-only — write, append and non-directory execute requests never
match it. <a id="cite-facs.stratafs-copy-up.provider-read-only"></a> Staging access is limited to the read, write and append
masks population needs, plus execute and chdir for directories, and
namespace parents to the write and traverse masks the one armed action
needs, plus open and chdir. <a id="cite-facs.stratafs-copy-up.staging-mask-limits"></a> Unknown mask bits fail closed. <a id="cite-facs.stratafs-copy-up.unknown-mask-fails-closed"></a>

The list is exhaustive. The context does not exempt execution, memory
mapping, ioctl, locking, arbitrary `fcntl`, device access, process
access, socket access, mount operations, or operations on a descriptor
installed into a userspace file table — each verified by the absence
of any copy-up branch on those paths. <a id="cite-facs.stratafs-copy-up.list-exhaustive"></a> Internal copy-up files are
additionally denied `statfs`, `truncate`, `fsync` and `fallocate`. <a id="cite-facs.stratafs-copy-up.internal-file-denied-ops"></a>

A file opened internally under the exemption is marked
copy-up-internal in its blob and carries a granted mask of zero. <a id="cite-facs.stratafs-copy-up.internal-file-zero-mask"></a> It is
usable without a cached caller grant only while the same context is
attached and its phase admits that exact file. Use after phase
completion, from another task, or after transfer through `SCM_RIGHTS`
fails closed. <a id="cite-facs.stratafs-copy-up.internal-file-scope"></a> Each armed phase has a distinct monotonically increasing
generation — overflowing it fails closed — and an internal file is
sealed to the generation it was opened in, so a later phase of the
same kind after a worker transfer cannot reactivate an older file. <a id="cite-facs.stratafs-copy-up.generation-seal"></a>
Final release drops the context reference.

The one exception is the read-only provider-directory cursor used by
bounded staging recovery. StrataFS may retain that file while it
leaves the context to clean one captured batch, then resume it after
re-entering the same context and arming a new source-read phase. Only
a directory file already marked internal for that exact context, still
naming the pinned provider path and inode, opened for read without
write, execute or path-only mode, and inside that attached
source-read phase, resumes; it is then resealed to the new generation. <a id="cite-facs.stratafs-copy-up.directory-cursor-resume"></a>
Between phases it is unusable and conveys no deletion authority.

<a id="trm-3-9-7-4"></a>

## Backing-file adoption <a id="cite-facs.stratafs-copy-up.backing-adoption"></a>

Before a regular-file copy is published, one exact copy-up-internal
backing file can become the backing file for the outer StrataFS open
description. The staging binding is verified, and the backing file's
recorded user path is confirmed to be that same outer description;
the outer description's immutable granted and continuous-audit
snapshot is then copied across and the internal marker removed. <a id="cite-facs.stratafs-copy-up.adoption-copies-snapshot"></a> This
is a transfer of authority already attached to the descriptor, not a
new AccessCheck against the task that caused the copy-up, which is
what preserves descriptor delegation when that task is not the opener.
It is one-shot, and requires the backing file mode. <a id="cite-facs.stratafs-copy-up.adoption-one-shot"></a>

StrataFS performs adoption after opening the staged file and **before**
publishing the anonymous staged object. KACS verifies the still-bound
staging object while the owned context has no armed phase.
<a id="cite-facs.stratafs-copy-up.adoption-before-publish"></a>

If the staged file belongs to OverlayFS, adoption also follows its exact
private backing files. Each child must be the parent's stored real file,
name that parent's upper object on its upper mount, and record the parent
as its user path. Matching a path alone does not establish this relationship.
The child must have an ordinary managed grant, no copy-up context or phase
generation, and no inherited backing grant.

KACS pins and validates the entire bounded chain before changing any file's
snapshot. A stale association, repeated file, or excessive depth rejects the
handoff without changing those snapshots. Once validation succeeds, every
admitted file receives the original outer description's granted and
continuous-audit masks in both security blobs. This preserves delegated
authority without consulting the task's credentials or weakening phase
precedence.

<a id="trm-3-9-7-7"></a>

## Auditing <a id="cite-facs.stratafs-copy-up.auditing"></a>

The outer authorized handle operation remains subject to ordinary
audit. No second caller AccessCheck or privilege-use audit is emitted
for an exempt internal sub-operation, since that would attribute
StrataFS mechanics to a caller decision that never happened — and
internal files carry a continuous-audit mask of zero, so they generate
no per-operation events either. <a id="cite-facs.stratafs-copy-up.no-second-audit"></a> The `CAP_SETFCAP` satisfaction path
returns before the capability check that would record privilege use.

StrataFS decides when its own copy-up lifecycle and failure events —
`stratafs.file.copied-up` and `stratafs.mutation.refused` ([Audit](<~kernel/internals/stratafs/security/audit#trm-4-6-5>)) —
occur; KACS supplies the kernel-only emitter, so KMES stamps each
event with the effective token of the task whose operation caused it
([Event Model](<~kernel/internals/kmes/event-model#trm-2-2>)). Two of those emissions are best-effort: an allocation failure,
or an operation string that is empty or over 64 bytes, drops the event
silently. <a id="cite-facs.stratafs-copy-up.emission-best-effort"></a>

Denied mismatches, and operations performed with no active matching
context, follow the ordinary authorization and audit paths.

## Related explanations

- [Deferred deletion](<~kernel/internals/stratafs/mutation/deferred-deletion>)
- [Copy-up descriptors](<~kernel/internals/stratafs/security/copy-up-descriptors>)
