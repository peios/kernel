---
title: "Special Attributes"
description: "The read-only flag KACS enforces for every process, and the settable Created At date, kept in the special-attributes extended attribute."
type: reference
---

<a id="trm-3-9-13"></a>

KACS keeps a file's **special attributes** in the extended attribute
`security.peios.sattr`, beside its security descriptor in
`security.peios.sd`. There are two today:

- **Read-only**, which KACS enforces for every process.
- **Created At**, a settable creation date.

<a id="trm-3-9-13-1"></a>

## Reading and writing them <a id="cite-facs.sattr.access"></a>

The attribute is read and written with the ordinary extended-attribute
calls — `getxattr`, `setxattr` and their descriptor and `*at` forms —
using `struct kacs_sattr` as the value. KACS answers these calls
itself. Reading needs `FILE_READ_ATTRIBUTES`, and writing or removing
needs `FILE_WRITE_ATTRIBUTES`, rather than the extended-attribute
rights. <a id="cite-facs.sattr.rights"></a> Through a descriptor, the right comes from the handle's
granted mask; by path, from a live check, which may grant
`FILE_READ_ATTRIBUTES` through the parent ([KACS-Native Open](<~kernel/internals/kacs/file-security/kacs-native-open#trm-3-9-2-8>)).

| Field | Meaning |
|---|---|
| `version` | `KACS_SATTR_VERSION`, currently 1. |
| `valid` | The fields a write changes. A read sets every bit. |
| `attributes` | `KACS_SATTR_READONLY` (0x1). |
| `flags` | On a read, `KACS_SATTR_CREATED_AT_SET` if Created At is set. On a write, `KACS_SATTR_CREATED_AT_CLEAR` unsets it. |
| `created_at_sec`, `created_at_nsec` | Created At, as seconds and nanoseconds since the Unix epoch. |

A write changes only the fields its `valid` mask names and leaves the
others as they are. Two programs changing different attributes at once
therefore cannot undo each other's change. <a id="cite-facs.sattr.merge"></a> A write with an unknown
version, `valid` bit, attribute or flag, a nonzero `__pad`, a value of
the wrong size, or `XATTR_CREATE` or `XATTR_REPLACE` fails with
`EINVAL`. Removing the attribute clears read-only and unsets Created
At.

The attribute is stored only while something is set, and reading a
file that has none fails with `ENODATA`: it is not read-only, and has no
Created At.
Tools that copy extended attributes copy a stored attribute with the
rest; a copy that should keep an unset Created At has to read it and
set it on the copy.

<a id="trm-3-9-13-2"></a>

## Read-only <a id="cite-facs.sattr.readonly"></a>

Read-only protects a file against accidental change, and binds its
owner too, without anyone rewriting its permissions. It is the
attribute Windows programs set and check, and source-control tools
mark checked-in files with it.

On a regular file marked read-only, for every process: <a id="cite-facs.sattr.readonly-enforced"></a>

- An open asking `FILE_WRITE_DATA` or `FILE_APPEND_DATA` fails with
  `EACCES`. A legacy open for writing fails the same way. A
  `MAXIMUM_ALLOWED` open is granted neither right, nor
  `FILE_ADD_SUBDIRECTORY` or `FILE_DELETE_CHILD`, following MS-FSA
  2.1.5.1.2.1. `FILE_OVERWRITE` and `FILE_SUPERSEDE` fail with `EACCES`.
- `truncate` by path fails with `EACCES`.
- Deleting it fails with `EPERM`: `unlink(2)`, a rename that would
  replace it, a delete disposition, and an open with delete-on-close,
  which a native open reports as `KACS_STATUS_CANNOT_DELETE`. The
  disposition and rename calls can set this aside with their
  `IGNORE_READONLY` flags ([Sharing and Deletion](<~kernel/internals/kacs/file-security/sharing-and-deletion#trm-3-9-10-4>)).

The check is made at open and at deletion, not on every write: a handle
opened for writing before the file was marked read-only keeps working,
as on Windows. Renaming a read-only file, and changing its other
attributes or its descriptor, are not affected. Anyone with
`FILE_WRITE_ATTRIBUTES` can clear the flag.

On a directory, read-only is kept and reported but not enforced.
Windows uses the flag on folders to mark them as customized, not to
protect them. <a id="cite-facs.sattr.readonly-directories"></a>

<a id="trm-3-9-13-3"></a>

## Created At <a id="cite-facs.sattr.created-at"></a>

Created At records when a file was created, in the sense a person or a
copy tool means: a copy can carry its original's creation date, and a
Windows client can set it. It is distinct from the filesystem's
**birth time**, which `statx` reports, which nobody can set, and which
records when this inode came into being. Birth time is the forensic
fact; Created At is the user-facing date.

While Created At has not been set, a file's creation date is its birth
time: a reader that finds no Created At, or finds
`KACS_SATTR_CREATED_AT_SET` clear, takes the date from `statx`. KACS
never changes Created At itself, and `statx` continues to report the
birth time.
