---
title: "KACS-Native Open"
description: "Opening a file by naming every right up front — handle modes, rights granted through the parent, share access, create dispositions, the creator's access and what the open reports."
type: reference
---

<a id="trm-3-9-2"></a>

> [!IMPORTANT]
> The [open-interface comparison](~kernel/userspace/native/kacs/abi-status-and-naming-differences#trm-3-d-6) records unresolved differences and the [limited pinned-source findings](~kernel/userspace/native/kacs/abi-status-and-naming-differences#trm-3-d-6-1) applied here. Creator-SD rejection, the accepted create-option bits, and native-open versus SD-query no-follow behavior were checked in source; the other differences remain unresolved. No runtime test or historical release boundary is established.

`kacs_open` takes an explicit desired access mask. The caller names
every right it will need — `FILE_READ_DATA`, `FILE_WRITE_DATA`,
`WRITE_DAC`, `READ_CONTROL`, any combination — and AccessCheck
evaluates the whole requested mask at open. If every requested right
is granted the descriptor's mask is set to the requested mask; if any
is denied, the open fails. <a id="cite-facs.open.strict-all-or-nothing"></a> This is the **strict** mode, in contrast to
the legacy path's subset behaviour ([Legacy Open Compatibility](<~kernel/internals/kacs/file-security/legacy-open-compatibility#trm-3-9-3>)).

`MAXIMUM_ALLOWED` asks for everything the caller may have. Any
concrete bits named with it have to be granted; the cached mask is
then the full computed maximum rather than the requested set. <a id="cite-facs.open.maximum-allowed-computes-max"></a>
`MAXIMUM_ALLOWED` may also be named alone. <a id="cite-facs.open.maximum-allowed-alone"></a> The maximum includes
the rights granted through the parent directory, described below, and
excludes the rights a read-only file withholds ([Special
Attributes](<~kernel/internals/kacs/file-security/special-attributes#trm-3-9-13>)).

A caller reads back what an open was granted with `kacs_query_open`,
which reports the cached mask, the open's share access, and whether the
file is delete-pending. <a id="cite-facs.open.query-open"></a> It is how a caller learns the result of a
`MAXIMUM_ALLOWED` open. The query needs no right: it reveals only what
the descriptor already carries. It fails with `EOPNOTSUPP` on an
unmanaged descriptor, including an `O_PATH` one.

<a id="trm-3-9-2-1"></a>

## Handle modes <a id="cite-facs.open.handle-modes"></a>

A Linux open file has a mode — readable, writable, or neither — which
the VFS uses for its own accounting, such as write access to an
executable and file leases. A native open derives that mode from the
rights it is granted: `FILE_READ_DATA` gives `FMODE_READ`, either
write right gives `FMODE_WRITE`, and `FILE_EXECUTE` gives `FMODE_EXEC`,
which enables `execveat(fd, "", ..., AT_EMPTY_PATH)`. <a id="cite-facs.open.execute-only-handle"></a>

An open granted none of these is a **control handle**: a managed
descriptor with no data mode, carrying only metadata, security or
delete rights. <a id="cite-facs.open.control-handle"></a> It can read attributes, read and change the
security descriptor, set a delete disposition, rename, and take part in
share checks. It cannot read or write the file's contents. No native
open needs to name a data right to obtain a descriptor. <a id="cite-facs.open.no-required-data-right"></a>

The mode is chosen **before** the file is opened, so that the VFS never
takes write access, read accounting or a lease break for an open that
does not hold the matching right. For an explicit mask the mode follows
the requested bits. For `MAXIMUM_ALLOWED`, KACS first evaluates the
maximum against the file's current descriptor and takes the mode from
the data rights that maximum contains. <a id="cite-facs.open.mode-before-open"></a>

The open hook then runs the authoritative check, as for every open. If
the descriptor changed between the two evaluations, the hook's result
stands. A strict request that is now denied fails as any denied open
does. A `MAXIMUM_ALLOWED` open is stamped with the new maximum, less
any data right its mode cannot exercise, so that `kacs_query_open`
never reports a right the descriptor cannot use. <a id="cite-facs.open.hook-authoritative"></a>

A `MAXIMUM_ALLOWED` open granted a write right takes write access like
any writer. Such an open of a file being executed fails with `ETXTBSY`,
and it breaks other holders' read leases.

<a id="trm-3-9-2-2"></a>

## Directories

Directory rights share bit positions with file data rights:
`FILE_LIST_DIRECTORY` is `FILE_READ_DATA` (0x0001), `FILE_ADD_FILE` is
`FILE_WRITE_DATA` (0x0002), and `FILE_ADD_SUBDIRECTORY` is
`FILE_APPEND_DATA` (0x0004). A directory open with `FILE_LIST_DIRECTORY`
is opened `FMODE_READ`; a directory open without it is a control
handle. <a id="cite-facs.open.dir-list-mode"></a>

The two write aliases are not cacheable directory handle rights,
though. `kacs_open` rejects a desired mask naming `FILE_ADD_FILE`,
`FILE_ADD_SUBDIRECTORY` or `FILE_DELETE_CHILD` on a directory with
`EOPNOTSUPP`. <a id="cite-facs.open.dir-write-aliases-eopnotsupp"></a> Those are parent-directory authorization rights for
namespace operations, evaluated live at the operation, not rights a
handle carries.

<a id="trm-3-9-2-3"></a>

## Special nodes and symlinks

Existing FIFOs, pathname socket nodes, and character and block device
nodes on managed mounts are ordinary filesystem file objects for
authorization: the file object type, the file right mapping, and the
file GenericMapping for metadata, standard and generic rights. <a id="cite-facs.open.special-nodes-are-file-objects"></a>

A special node still has to be opened with a data right, because its
driver decides what an open without one means; a FIFO refuses it. A
native open of a special node granted no data right fails with
`EINVAL`. <a id="cite-facs.open.special-nodes-need-data-right"></a> `FILE_EXECUTE` is not a valid data substitute for them — a
`kacs_open` naming it on such a node fails closed. <a id="cite-facs.open.execute-not-valid-on-special-nodes"></a> The Linux object
implementation may still impose its own device- or
filesystem-specific denial after KACS has authorized the file object.

Symlink objects are file objects for `kacs_get_sd`, `kacs_set_sd` and
`readlink`, but they are not opened as terminal objects by
`kacs_open`. Following is the default resolution behaviour, and
`AT_SYMLINK_NOFOLLOW` fails with `ELOOP`. <a id="cite-facs.open.symlink-nofollow-eloop"></a> This differs deliberately
from `kacs_get_sd` and `kacs_set_sd`, where the same flag resolves the
symlink object itself.

<a id="trm-3-9-2-8"></a>

## Rights granted through the parent <a id="cite-facs.open.parent-grants"></a>

Two rights may be granted by the parent directory when the file's own
descriptor withholds them, as NTFS grants them (MS-FSA 2.1.5.1.2.1):

- **`DELETE`** is granted if the parent grants `FILE_DELETE_CHILD`. <a id="cite-facs.open.delete-through-parent"></a>
- **`FILE_READ_ATTRIBUTES`** is granted if the parent grants
  `FILE_LIST_DIRECTORY`. A caller who may list a directory may already
  see what its entries' attributes would show. <a id="cite-facs.open.read-attributes-through-parent"></a>

AccessCheck runs first against the file. For each of these two rights
that it does not grant, it runs again against the parent directory for
the parent right. The parent is the directory the open resolved the
file through, so for a file with several hard links it is the parent
of the link that was opened. <a id="cite-facs.open.parent-is-opened-link"></a> A `MAXIMUM_ALLOWED` open includes
whichever of the two the parent grants.

The same pair of checks governs every other operation that deletes or
reads attributes by name: unlink, rmdir and rename by path, delete on
close, superseding a file, and `stat` by path ([Use-Time
Semantics](<~kernel/internals/kacs/file-security/use-time-semantics#trm-3-9-4-2>)). <a id="cite-facs.open.delete-fallback"></a>

<a id="trm-3-9-2-9"></a>

## Share access <a id="cite-facs.open.share-access"></a>

Every open of a regular file or directory on a managed mount takes part
in NT share-mode checking ([Sharing and Deletion](<~kernel/internals/kacs/file-security/sharing-and-deletion#trm-3-9-10>)). A native open
states the sharing it allows in `kacs_open_how.share_access`, read only
when `flags` carries `KACS_OPEN_SHARE_ACCESS`:

| Value | Name | Others may open with |
|---|---|---|
| 0x1 | `KACS_FILE_SHARE_READ` | `FILE_READ_DATA` or `FILE_EXECUTE` |
| 0x2 | `KACS_FILE_SHARE_WRITE` | `FILE_WRITE_DATA` or `FILE_APPEND_DATA` |
| 0x4 | `KACS_FILE_SHARE_DELETE` | `DELETE` |

Without the flag the open shares all three, as a legacy open does, and
`share_access` has to be zero. <a id="cite-facs.open.share-default-all"></a> An open that conflicts with
another fails with `EBUSY` and the status `KACS_STATUS_SHARING_VIOLATION`.

<a id="trm-3-9-2-4"></a>

## Create dispositions <a id="cite-facs.open.create-dispositions"></a>

| Value | Name | If it exists | If it does not |
|---|---|---|---|
| 0 | `FILE_SUPERSEDE` | Delete and recreate | Create |
| 1 | `FILE_OPEN` | Open | Fail |
| 2 | `FILE_CREATE` | Fail | Create |
| 3 | `FILE_OPEN_IF` | Open | Create |
| 4 | `FILE_OVERWRITE` | Truncate to zero | Fail |
| 5 | `FILE_OVERWRITE_IF` | Truncate to zero | Create |

`FILE_SUPERSEDE` deletes the existing name and creates a new file
under it, requiring `DELETE` on the existing file — or
`FILE_DELETE_CHILD` on the parent — together with `FILE_ADD_FILE` on
the parent. <a id="cite-facs.open.supersede-rights"></a> The existing file's other opens have to share `DELETE`,
and a read-only or delete-pending file cannot be superseded. The new
file gets a new inode and a new descriptor, inherited or
caller-supplied. The superseded pathname is broken away from the old
hardlink set and names the new inode; other pre-existing hardlinks
continue to name the old inode, and already-open descriptors still
reference it. <a id="cite-facs.open.supersede-new-inode"></a>

`FILE_OVERWRITE` truncates in place — same inode, same descriptor,
hardlinks preserved — and requires `FILE_WRITE_DATA`. <a id="cite-facs.open.overwrite-in-place"></a>

On an `unmanaged` mount, `FILE_OPEN` and `FILE_OPEN_IF` succeed and
return an unmanaged descriptor with no stamped mask rather than
failing; the creating dispositions fail with `EOPNOTSUPP`. <a id="cite-facs.open.unmanaged-create-eopnotsupp"></a>

<a id="trm-3-9-2-5"></a>

## Create options

| Value | Name | Description |
|---|---|---|
| 0x0001 | `KACS_CREATE_OPT_DIRECTORY` | The target has to be a directory. When creating, create a directory rather than a regular file; when opening an existing non-directory, fail with `ENOTDIR`. <a id="cite-facs.open.create-opt-directory"></a> |
| 0x0002 | `KACS_CREATE_OPT_DELETE_ON_CLOSE` | Mark the file for deletion when this open closes. Requires `DELETE`, which may come through the parent. |

All other bits are reserved and have to be zero; a nonzero reserved
bit fails with `EINVAL`. <a id="cite-facs.open.reserved-create-option-einval"></a>

Delete-on-close is NT's: the obligation belongs to the open, and when
the open closes the file becomes **delete-pending**. The name is removed
at the last close of any open of the file, from any process
([Sharing and Deletion](<~kernel/internals/kacs/file-security/sharing-and-deletion#trm-3-9-10-3>)). <a id="cite-facs.open.delete-on-close-nt"></a> `dup()`, `fork()` and `SCM_RIGHTS`
preserve the obligation because they preserve the open file
description; it is discharged when the description's last reference
closes. <a id="cite-facs.open.delete-on-close-lineage"></a> `kacs_set_disposition` with `KACS_DISPOSITION_ON_CLOSE` sets or
clears it on an open that has `DELETE`.

Delete-on-close applies to regular files and directories. A directory
is removed only if it is empty when it is deleted. <a id="cite-facs.open.delete-on-close-directories"></a> A read-only
regular file cannot be opened with delete-on-close: the open fails with
`EPERM` and the status `KACS_STATUS_CANNOT_DELETE`.

<a id="trm-3-9-2-6"></a>

## Caller-supplied descriptors

The descriptor format and size bound are defined in [SD Structure](https://learn.peios.org/specifications/pcds/security-descriptor/structure#binary-format).

When a disposition results in a new file the caller may supply a
descriptor. A null pointer with zero length means the new file's
descriptor is inherited from the parent directory through the
inheritance algorithm. <a id="cite-facs.open.null-descriptor-inherits"></a>

Supplying one on a branch that opens an *existing* object is invalid
input rather than something silently ignored. `FILE_OPEN_IF`
resolving to an existing object fails with `EINVAL`, and so do
`FILE_OVERWRITE` and the existing-object branch of
`FILE_OVERWRITE_IF`, since those retain the existing inode and its
descriptor. <a id="cite-facs.open.supplied-on-existing-einval"></a> `FILE_OPEN` with a descriptor supplied fails with
`EOPNOTSUPP`. <a id="cite-facs.open.supplied-with-file-open-eopnotsupp"></a>

Creator-supplied descriptors are validated at create time. An owner
SID has to be the caller's own or a token group marked
`SE_GROUP_OWNER`, unless `SeRestorePrivilege` is enabled, in which
case any owner is allowed. <a id="cite-facs.open.supplied-owner-constraint"></a> A supplied SACL is treated as a full SACL
input rather than a label-only fragment, and therefore requires
`SeSecurityPrivilege`. <a id="cite-facs.open.supplied-sacl-requires-privilege"></a> If that SACL carries an explicit mandatory
label ACE, the label also has to satisfy the ordinary label-write
constraint: at or below the caller's integrity level, unless
`SeRelabelPrivilege` is held. <a id="cite-facs.open.supplied-label-constraint"></a>

Generic rights in the descriptor's ACEs are mapped to file rights when
the descriptor is stored, whether it was supplied, inherited or taken
from the token's default DACL ([The Set-Security Interface](<~kernel/internals/kacs/file-security/the-set-security-interface#trm-3-9-6-7>)).

<a id="trm-3-9-2-10"></a>

## The creator's access <a id="cite-facs.open.creator-access"></a>

The parent's create rights authorize the creation: `FILE_ADD_FILE` or
`FILE_ADD_SUBDIRECTORY`, together with the supersede rules above. The
handle a creating open returns is then granted the access it asked
for, as in Windows, even where the new file's descriptor would not
grant it to its creator. <a id="cite-facs.open.creator-granted-requested"></a> A creator can therefore create a file with a
restrictive descriptor and still write it, in one step, and a folder
can accept files whose inherited permissions exclude the people who put
them there.

The grant replaces only the **normal discretionary pass**. The kernel
computes the new object's descriptor first, then runs the strict check
against it, with the normal DACL walk treated as granting the creator
everything. <a id="cite-facs.open.creator-normal-pass-only"></a> Every other layer still evaluates the new descriptor and
can refuse:

- the mandatory integrity label and PIP;
- the restricted-token pass;
- confinement, which stays absolute ([Application Confinement](<~kernel/internals/kacs/access-check/application-confinement#trm-3-8-6>));
- central access and auditing policy; and
- privilege-only rights, such as `ACCESS_SYSTEM_SECURITY`.

So a low-integrity creator under an inherited high-integrity label
cannot write what it created, and a confined application cannot write
outside what its confinement identity is granted. A `MAXIMUM_ALLOWED`
creating open is granted every right of the object type that those
layers allow. A refused check rolls the creation back — the newly
created file or directory is removed — and the syscall fails. <a id="cite-facs.open.failed-check-rolls-back"></a>

The grant belongs to the creating open alone. `FILE_OPEN_IF` or
`FILE_OVERWRITE_IF` that finds an existing object is an ordinary open,
and every later open of the new object is checked against its
descriptor as normal. <a id="cite-facs.open.creator-grant-only-when-creating"></a>

<a id="trm-3-9-2-11"></a>

## Ancestor pinning

`KACS_OPEN_PIN_ANCESTORS` pins the opened file's ancestor directories:
while the open lasts, none of them can be renamed or removed by anyone
([Sharing and Deletion](<~kernel/internals/kacs/file-security/sharing-and-deletion#trm-3-9-10-6>)). It requires `SeLockParentagePrivilege` enabled;
without it the open fails with `EPERM`. <a id="cite-facs.open.pin-requires-privilege"></a>

<a id="trm-3-9-2-12"></a>

## Lease keys

With `KACS_OPEN_LEASE_KEY`, `kacs_open_how.lease_key` and `lease_fd`
identify the opener to the lease manager given by `lease_fd`. Opening a
file does not break leases that the same manager holds under the same
key ([Leases](<~kernel/internals/kacs/file-security/leases#trm-3-9-12>)). <a id="cite-facs.open.lease-key-exemption"></a> `lease_fd` has to be a lease-manager
descriptor, or the open fails with `EBADF`.

<a id="trm-3-9-2-7"></a>

## Modes and status

`kacs_open_how` carries no POSIX mode field, so the raw Linux inode
mode for native creation is fixed: `0600` for regular files, `0700`
for directories. <a id="cite-facs.open.fixed-create-modes"></a> These are compatibility metadata only — and if Linux
DAC ever denies an operation KACS would have authorized, the operation
fails closed.

Native creation does not create FIFOs, socket nodes, device nodes or
symlinks. <a id="cite-facs.open.no-native-special-creation"></a> Those stay on the Linux namespace APIs — `mknod()`,
`mkfifo()`, Unix `bind()` to a path — governed by the namespace hooks.
NTFS is excluded from native creation entirely. <a id="cite-facs.open.ntfs-excluded"></a>

`kacs_open_how` is size-versioned. A caller passes the size it was
built with — 32 bytes for the original layout, 56 bytes with the lease
fields — and fields beyond that size read as zero. A size below 16
bytes fails with `EINVAL`. <a id="cite-facs.open.how-size-versioned"></a> New fields are added at the end, behind a
flag, so that an existing caller's meaning never changes.

The syscall reports what happened through `status_out`: created,
opened, overwritten, or superseded. `KACS_STATUS_SUPERSEDED` is used
only when an existing object was actually replaced — a
`FILE_SUPERSEDE` that finds no target and simply creates one reports
`KACS_STATUS_CREATED`. <a id="cite-facs.open.status-superseded-only-if-replaced"></a>

When the open fails for a reason one errno cannot tell apart,
`status_out` also names the NT condition: <a id="cite-facs.open.failure-status"></a>

| Status | Errno | Condition |
|---|---|---|
| `KACS_STATUS_SHARING_VIOLATION` | `EBUSY` | Another open's share access conflicts with this one. |
| `KACS_STATUS_DELETE_PENDING` | `EBUSY` | The file is delete-pending. |
| `KACS_STATUS_CANNOT_DELETE` | `EPERM` | Delete-on-close on a read-only file. |

On any other failure `status_out` is left unwritten.
