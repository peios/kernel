---
title: "Sharing and Deletion"
description: "NT share modes enforced for every process, delete-pending files, deletion and renaming through an open handle, and pinning a file's ancestors."
type: reference
---

<a id="trm-3-9-10"></a>

KACS keeps NT's sharing and deletion rules in the kernel, for every
process. An open says which kinds of access it lets other opens have at
the same time. A file can be marked for deletion through any open that
holds `DELETE`, and is removed when the last open of it closes. Deletion
and renaming can be done through an open handle rather than by name.

These rules apply to regular files and directories on FACS-managed
mounts. <a id="cite-facs.share.scope"></a> They do not apply to device nodes, FIFOs, sockets or symbolic
links, to unmanaged mounts such as `/proc`, `/sys` and nullfs, or to
`O_PATH` descriptors, which take no part in share checks.

<a id="trm-3-9-10-1"></a>

## Share modes <a id="cite-facs.share.check"></a>

The rules are those of MS-FSA 2.1.5.1.2.1 and 2.1.5.1.2.2. Access falls
into three classes:

| Class | Rights | Share bit that admits it |
|---|---|---|
| Read | `FILE_READ_DATA`, `FILE_EXECUTE` | `FILE_SHARE_READ` |
| Write | `FILE_WRITE_DATA`, `FILE_APPEND_DATA` | `FILE_SHARE_WRITE` |
| Delete | `DELETE` | `FILE_SHARE_DELETE` |

An open whose granted access contains none of these rights takes no part
in share checking: it neither conflicts with other opens nor constrains
them. <a id="cite-facs.share.attribute-only-opens"></a> Opening for attributes or for the security descriptor is
always possible, whatever other opens deny.

An open that does take part conflicts with an existing open, and fails
with `EBUSY`, when either of them holds access of a class the other
does not share. <a id="cite-facs.share.conflict-both-ways"></a> A native open is judged by the access it was
**granted**, not what it asked for, so a `MAXIMUM_ALLOWED` open is
judged by what it received. A native open reports the conflict as
`KACS_STATUS_SHARING_VIOLATION`. A successful open registers its access
and share mode until it closes.

**Legacy opens take part.** A plain `open(2)` shares all three classes,
so legacy opens never conflict with each other. A legacy open is judged
by its mode instead of its granted mask, because its mask carries
optional compat rights it may never use: a readable open, file or
directory, holds the read class, and a writable one the write class.
<a id="cite-facs.share.legacy-opens"></a> A legacy open of a file another
open has denied to its class fails with `EBUSY`, as a native open does.

**A running program takes part.** Executing a file holds it as an open
with read access that shares read and delete but not write. This is the
NT form of Linux's refusal to write a running executable, which still
applies first, with `ETXTBSY`. A program can be replaced by renaming a
new file over its name while it runs. <a id="cite-facs.share.exec"></a>

An open's share registration lasts as long as its open file
description. A memory mapping holds the description, so a mapped file
keeps its registration after its descriptor is closed, until it is
unmapped.

<a id="trm-3-9-10-2"></a>

## Denying only what you could do yourself <a id="cite-facs.share.deny-limits"></a>

Share modes would let any reader lock others out of a file, such as a
system configuration file it can only read. KACS limits each denial to
what the opener could do itself. Where an open omits a share bit it is
not entitled to deny, that bit is silently set, and the open proceeds as
if it had shared it.

- **Denying read** follows MS-FSA. It takes effect only if the opener
  has `FILE_WRITE_DATA` on the parent directory (2.1.5.1.2.2). On the
  first open of a directory it also needs the generic write rights on
  the directory itself (2.1.5.1.2). <a id="cite-facs.share.deny-read"></a>
- **Denying write** takes effect only if the opener's descriptor grants
  it `FILE_WRITE_DATA` or `FILE_APPEND_DATA` on the object. <a id="cite-facs.share.deny-write"></a>
- **Denying delete** takes effect only if the opener could delete the
  object: `DELETE` on it, or `FILE_DELETE_CHILD` on its parent. <a id="cite-facs.share.deny-delete"></a>

These decide whether the opener *could* exercise the right, not
whether it asked to. Each is an AccessCheck against the current
descriptor, made only for an open that omits the corresponding share
bit. An open that shares everything, which includes every legacy open,
costs nothing extra.

<a id="trm-3-9-10-7"></a>

## Overriding share modes <a id="cite-facs.share.override"></a>

Backup and restore tools have to read and replace files that others
hold open. A native open's backup and restore intents
([Privilege-Based Grants](<~kernel/internals/kacs/privileges/the-privilege-model>)) also let it set aside other opens'
denials:

- backup intent with `SeBackupPrivilege` enabled ignores other opens'
  denial of read;
- restore intent with `SeRestorePrivilege` enabled ignores other opens'
  denial of write and delete.

The override skips only the share check. Lease breaks still happen, so
a client caching the file flushes first. The overriding open's own
share mode still binds later opens, and every override is audited. <a id="cite-facs.share.override-audited"></a>

<a id="trm-3-9-10-3"></a>

## Delete-pending files <a id="cite-facs.delete.pending"></a>

A file is **delete-pending** when it has been marked to be deleted at
its last close. Any open of the file that holds `DELETE` can set or
clear the mark with `kacs_set_disposition`. An open created with
`KACS_CREATE_OPT_DELETE_ON_CLOSE` sets it when it closes. <a id="cite-facs.delete.set-clear"></a>

While a file is delete-pending:

- its name stays in place: `stat` and directory listings still show it;
- every new open of it fails with `EBUSY`, whatever the access asked,
  including attribute-only and `O_PATH` opens; a native open reports
  `KACS_STATUS_DELETE_PENDING`; <a id="cite-facs.delete.pending-opens-fail"></a>
- unlinking or renaming it by name fails with `EBUSY`;
- a delete-pending directory accepts no new entries: creating, linking
  or renaming into it fails with `EBUSY`; and
- creating a file of the same name fails, because the name still
  exists.

When the last open of the file closes, from whichever process, the
name is removed. <a id="cite-facs.delete.last-close"></a> The removal is authorized by the token of the open
that set the mark, captured when it was set, not by whoever happens to
close last; the closing task needs no right. A removal that fails at
close, for example because a directory gained an entry, is audited,
and the file is left in place and no longer delete-pending. <a id="cite-facs.delete.close-failure-audited"></a>

The name removed is the link the marking open was opened through,
followed across any renames since. Other hard links to the file remain.
If that name is already gone by the last close, nothing more is done.

A directory is removed at its last close only if it is empty then; one
that is not stays, and the failed removal is audited. A delete-pending
directory accepts no new entries meanwhile, so it can only empty. A
read-only regular file cannot be marked unless the caller sets it aside ([Special
Attributes](<~kernel/internals/kacs/file-security/special-attributes#trm-3-9-13>)).

<a id="trm-3-9-10-4"></a>

## The disposition call <a id="cite-facs.delete.disposition-call"></a>

`kacs_set_disposition(fd, flags)` sets a file's delete disposition
through an open handle. Its flags are those of NT's
`FILE_DISPOSITION_INFORMATION_EX`:

| Flag | Value | Meaning |
|---|---|---|
| `KACS_DISPOSITION_DELETE` | 0x01 | Mark the file for deletion. Without it, clear the mark. |
| `KACS_DISPOSITION_POSIX_SEMANTICS` | 0x02 | With `DELETE`: remove the name now. |
| `KACS_DISPOSITION_ON_CLOSE` | 0x08 | Set or clear this open's delete-on-close obligation instead of the file's mark. |
| `KACS_DISPOSITION_IGNORE_READONLY` | 0x10 | Delete a read-only file. Requires `FILE_WRITE_ATTRIBUTES` as well. |

The open has to hold `DELETE`, or the call fails with `EACCES`. <a id="cite-facs.delete.disposition-needs-delete"></a> The
right was checked when the handle was opened, including through the
parent; the call checks the handle's mask, not the descriptor.

**POSIX semantics** remove the name at once, as `unlink(2)` does, and
open handles carry on with the unnamed file. <a id="cite-facs.delete.posix-now"></a> This is how a
Windows client's POSIX-semantics delete, and a Peios program's "delete
this file I hold open", are carried out. A directory has to be empty,
or the call fails with `ENOTEMPTY`.

Other opens of the file were checked against this open's `DELETE` when
each was opened, so the call does not repeat the share check. A read-only
regular file without `IGNORE_READONLY` fails with `EPERM`. Calling it on
an unmanaged descriptor fails with `EOPNOTSUPP`.

<a id="trm-3-9-10-5"></a>

## Renaming through a handle <a id="cite-facs.rename.handle"></a>

`kacs_rename(fd, newdirfd, newpath, flags)` moves the link an open
handle names to `newpath`, resolved relative to `newdirfd` as by
`renameat2()`. Its flags are those of NT's `FILE_RENAME_INFORMATION_EX`:

| Flag | Value | Meaning |
|---|---|---|
| `KACS_RENAME_REPLACE_IF_EXISTS` | 0x01 | Replace an existing file at the destination. |
| `KACS_RENAME_POSIX_SEMANTICS` | 0x02 | Replace a destination file that is open, if its opens share delete. |
| `KACS_RENAME_IGNORE_READONLY` | 0x40 | Replace a read-only destination file. |

An open file's name follows renames, so the handle always names its
current link; renaming by handle cannot hit a different file that has
since taken the old name. On StrataFS the link is found from the file's
provider instead ([Stacked filesystems](#trm-3-9-10-9)). Authorization is:

- `DELETE` in the handle's granted mask, for removing the source link; <a id="cite-facs.rename.needs-delete"></a>
- a live check for `FILE_ADD_FILE`, or `FILE_ADD_SUBDIRECTORY` for a
  directory, on the destination directory; and
- where a file is replaced, a live check for `DELETE` on it or
  `FILE_DELETE_CHILD` on its parent. <a id="cite-facs.rename.replace-checks"></a>

A replaced file that is open fails the rename with `EBUSY`, unless
`POSIX_SEMANTICS` is given and all its opens share delete. A replaced
file that is delete-pending, or read-only without `IGNORE_READONLY`,
also fails. A directory is never replaced. A destination that exists
without `REPLACE_IF_EXISTS` fails with `EEXIST`. If the handle's link
has already been removed, the call fails with `ENOENT`.

<a id="trm-3-9-10-8"></a>

## Deleting and renaming by name <a id="cite-facs.share.unlink-rename-by-name"></a>

NT treats deleting a file by name as an open with `DELETE`, so the
Linux calls obey the same rules. `unlink(2)`, `rmdir(2)` and `rename(2)`
fail with `EBUSY` when the source, or a file the rename would replace:

- is held by an open that does not share delete; or
- is delete-pending.

This covers `rm`, `mv`, and editors that save by renaming a new file
over the old one. The limit on denials means that only someone who
could delete a file can stop others deleting it. Their access checks
are unchanged ([Use-Time Semantics](<~kernel/internals/kacs/file-security/use-time-semantics#trm-3-9-4>)). Plain deletion by name is still
immediate: the name goes at once, and open handles carry on.

<a id="trm-3-9-10-6"></a>

## Ancestor pinning <a id="cite-facs.pin.ancestors"></a>

Windows will not rename or remove a folder while a file beneath it is
open. Linux has no such rule, and Peios keeps Linux's for its own
programs. An open made with `KACS_OPEN_PIN_ANCESTORS` asks for the
Windows rule for that one file: while it is open, each directory above
it, up to the root of the mount it was opened through, is **pinned**.
A pinned directory cannot be renamed, removed, or replaced by a rename,
by any process; those calls fail with `EBUSY`. <a id="cite-facs.pin.refuses-rename-rmdir"></a>

The pin follows the link the file was opened through, and the
directories it pins are those above that link when the open was made.
It is held as a count on each directory, so many pinned files beneath
one directory pin it once each. The counts are taken in a single walk
that is repeated if a rename moves one of the directories while the
walk is in progress, and dropped when the open's description closes.
<a id="cite-facs.pin.counts"></a> The pinned file itself is not pinned: renaming or deleting it is
governed by share modes.

Pinning blocks other people's work, so it requires
`SeLockParentagePrivilege`. File servers hold it, to give the Windows
clients they serve the folder protection those clients expect from each
other. <a id="cite-facs.pin.privilege"></a>

<a id="trm-3-9-10-9"></a>

## Stacked filesystems <a id="cite-facs.share.stacked"></a>

A stacking filesystem shows files that live on another filesystem
beneath it, the **provider**. StrataFS gives every lookup of a name a
new inode of its own, so KACS keeps a file's share registrations,
delete-pending mark and pin counts on the provider's inode instead. All
routes to a file therefore see the same state: the merged view, another
StrataFS mount over the same stratum, and the stratum itself. A regular
file's open registers through the backing file that StrataFS opens on
the provider. A directory's open has no backing file, so it registers on
its provider itself. <a id="cite-facs.share.stratafs-provider"></a>

**Copy-up.** When StrataFS copies a regular file up to its writable
stratum, the file's opens move their registrations to the copy. A
directory copied up while it is open keeps its registrations and pins
on the former provider, so opens and removals made after the copy-up do
not see them. A directory present in more than one stratum cannot be
renamed in any case. <a id="cite-facs.share.stratafs-copy-up"></a>

**Renaming through a handle.** A StrataFS open's own name is the one it
was looked up by, which goes out of date when the file is renamed. The
provider is renamed in its own filesystem, which keeps its name current,
so `kacs_rename` finds the handle's link there:

1. it takes the provider's path within its stratum;
2. it looks that path up again through the mount the handle was opened
   through, and locks it as `rename(2)` would;
3. it checks that the name still reaches the same provider, retrying if
   a rename moved it meanwhile.

After a copy-up the handle names the copy. A name that a higher stratum
masks is not the handle's file, and the call fails with `ENOENT`, as it
does when the link has been removed. A file whose provider is a
read-only stratum fails with `EROFS`, as `rename(2)` does. <a id="cite-facs.rename.stratafs"></a>

**Overlayfs.** A file's opens register on its real inode through their
backing files. A directory opened through overlayfs opens its real
directory as a plain open, so the real directory sees a legacy open that
shares everything, and the native open's share mode is not enforced. <a id="cite-facs.share.overlayfs"></a>
