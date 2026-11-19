---
title: "Byte-Range Locks"
description: "NT byte-range locks, kept by the kernel and enforced on every read and write — when they are checked, what they block, and the limit on who can block whom."
type: reference
---

<a id="trm-3-9-11"></a>

An NT byte-range lock reserves part of a file for one open. An
exclusive lock keeps every other open from reading or writing the range;
a shared lock keeps everyone, its holder included, from writing it.
Unlike Linux's advisory `fcntl` and `flock` locks, these are
**enforced**: a read or write that conflicts with another open's lock
fails, whichever program issued it. <a id="cite-facs.lock.enforced"></a> KACS keeps them for regular files
on FACS-managed mounts; `kacs_lock` on anything else fails with
`EOPNOTSUPP`.

Linux's own locks are unchanged and independent. A program that takes
`fcntl` locks neither sees nor conflicts with byte-range locks, except
that its reads and writes are checked against them like everyone
else's.

<a id="trm-3-9-11-1"></a>

## Taking and releasing locks <a id="cite-facs.lock.call"></a>

`kacs_lock(fd, args, size)` takes or releases a lock through an open
handle. `struct kacs_lock_args` gives the range as `offset` and
`length`, the operation, and flags:

| Operation | Value | Meaning |
|---|---|---|
| `KACS_LOCK_SHARED` | 1 | Take a shared lock. |
| `KACS_LOCK_EXCLUSIVE` | 2 | Take an exclusive lock. |
| `KACS_LOCK_UNLOCK` | 3 | Release a lock this open holds over exactly this range. |
| `KACS_LOCK_CANCEL` | 4 | Cancel this open's waiting request named by `cookie`. |

The open has to hold a data right — `FILE_READ_DATA`, `FILE_WRITE_DATA`
or `FILE_APPEND_DATA` — or the call fails with `EACCES`. <a id="cite-facs.lock.needs-data-right"></a> A lock
belongs to the open file description that took it, so descriptors
duplicated from it share its locks. When the description closes, its
locks are released and its waiting requests cancelled. <a id="cite-facs.lock.owner-and-release"></a>

Lock conflicts follow MS-FSA 2.1.4.10. Two locks of different opens
conflict where their ranges overlap and either is exclusive. An open's
exclusive lock also conflicts with its own overlapping exclusive lock.
A zero-length lock is a point at its offset, and the range from offset
zero with length zero conflicts with nothing. <a id="cite-facs.lock.conflicts"></a>

A request that conflicts waits until it can be granted, unless it
carries `KACS_LOCK_FAIL_IMMEDIATELY`, in which case it fails with
`EAGAIN`. A waiting request can be interrupted by a signal (`EINTR`),
or cancelled by another thread with `KACS_LOCK_CANCEL` and the same
`cookie`, in which case it fails with `ECANCELED`. Waiting requests are
granted in the order they arrived as the conflicting locks go.
<a id="cite-facs.lock.waiting"></a> Unlocking a range this open does not hold exactly fails with `ENOLCK`.

<a id="trm-3-9-11-2"></a>

## What locks block <a id="cite-facs.lock.io-checks"></a>

Each operation that reads or changes a file's contents is checked
against the locks of **other** opens:

| Operation | Checked as |
|---|---|
| Read | A read of its range |
| Write, including append | A write of its range |
| `truncate`, `ftruncate` | A write of the range between the old and new size |
| `fallocate` that changes contents | A write of the range it changes, to end of file for collapse and insert |

An exclusive lock blocks reads and writes; a shared lock blocks writes.
A shared lock also blocks its own holder's writes. A conflicting
operation fails with `EAGAIN`; it does not wait. <a id="cite-facs.lock.io-eagain"></a>

The check covers every way of issuing these operations: `read`,
`write` and their vectored and positioned forms, `sendfile`, `splice`
and `copy_file_range`, direct I/O, AIO and io_uring.

<a id="trm-3-9-11-3"></a>

## When a lock takes effect <a id="cite-facs.lock.at-issue"></a>

An I/O is checked against the lock list when it is **issued**. Granting
a lock does not wait for I/O already admitted: an I/O that passed its
check before a conflicting lock was granted may finish after it, and
counts as having happened before the lock. This is the guarantee
Windows gives. No lock is held across the I/O itself, so asynchronous
I/O completing elsewhere needs no special treatment, and an I/O cannot
deadlock against a lock request.

A file with no byte-range locks costs one check that its lock list is
empty.

<a id="trm-3-9-11-4"></a>

## Memory mappings are not covered <a id="cite-facs.lock.mmap-excluded"></a>

Loads and stores through a memory mapping are not checked against
locks, as on Windows, where mapped views bypass byte-range locks.
Mapping a file, and changing a mapping's protection, are checked only
by the handle's rights ([Use-Time Semantics](<~kernel/internals/kacs/file-security/use-time-semantics#trm-3-9-4-1>)).

<a id="trm-3-9-11-5"></a>

## Who can block whom <a id="cite-facs.lock.dos-limit"></a>

Enforced locks would let any reader stop others using a file. KACS
limits their reach as it limits share modes: a lock blocks other opens'
reads and writes only if the open that took it could write the file
itself, that is, if the file's descriptor grants its opener
`FILE_WRITE_DATA` or `FILE_APPEND_DATA`. A lock taken by an opener who
could not write the file still conflicts with other locks, so
cooperating readers can coordinate with it, but it blocks no I/O.

<a id="trm-3-9-11-6"></a>

## Stacked filesystems <a id="cite-facs.lock.stacked"></a>

Through StrataFS, a lock belongs to the backing file its open reaches
and is held on the provider, so it covers every route to that file. A
copy-up gives the file a new provider: locks taken before it stay with
the former provider, and I/O through the copy is not checked against
them. Locks through overlayfs are not supported, and `kacs_lock` fails
with `EOPNOTSUPP`.
