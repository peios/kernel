---
title: "Leases"
description: "NT caching leases kept by the kernel for a lease manager such as a file server — the read, handle and write states, what breaks them, and how breaks are delivered."
type: reference
---

<a id="trm-3-9-12"></a>

A lease lets a holder cache a file safely. Its state is any combination
of three NT caching bits:

| State | Value | The holder may cache |
|---|---|---|
| `KACS_LEASE_READ` | 0x1 | The file's contents and attributes, for reading. |
| `KACS_LEASE_HANDLE` | 0x2 | Its open handles, keeping them open after its own client has closed them. |
| `KACS_LEASE_WRITE` | 0x4 | Changes to the contents, not yet written back. |

When another open or operation would make the cached state wrong,
KACS **breaks** the lease: it tells the holder, waits for the holder to
flush and give up the state, then lets the operation proceed. A file
server holds leases on behalf of its clients and relays the breaks to
them, so a local program and a network client see a consistent file.
<a id="cite-facs.lease.purpose"></a>

Leases cover regular files and directories on FACS-managed mounts.
A directory lease can hold only read and handle caching. Below a
stacking filesystem a lease is held on the provider an open reaches
([Stacked filesystems](#trm-3-9-12-6)).

<a id="trm-3-9-12-1"></a>

## Lease managers <a id="cite-facs.lease.manager"></a>

A lease is held through a **lease manager**, created by
`kacs_create_lease_manager(flags, break_timeout_ms)`. The call returns a
descriptor; `KACS_LEASE_MANAGER_CLOEXEC` and
`KACS_LEASE_MANAGER_NONBLOCK` set close-on-exec and non-blocking
reads. Break notices for every lease the manager holds arrive on that
descriptor.

Each lease is identified by its manager and a 16-byte **key** the
manager chooses. Opens with the same key belong to one holder: an open
made with a key does not break the leases its manager holds under that
key ([KACS-Native Open](<~kernel/internals/kacs/file-security/kacs-native-open#trm-3-9-2-12>)). <a id="cite-facs.lease.key"></a> A file server gives each client lease
its own key, and each oplock its own unique key.

Closing the manager's last descriptor releases all its leases.

<a id="trm-3-9-12-2"></a>

## Requesting a lease <a id="cite-facs.lease.request"></a>

`kacs_lease(fd, manager_fd, args, size)` requests, changes or releases
the lease on the file `fd` refers to. The open has to have been made
with `KACS_OPEN_LEASE_KEY`, naming the same manager and the key given
in `args`; otherwise the call fails with `EINVAL`.

KACS grants as much of the requested state as current opens allow,
writes the granted state back into `args.state`, and may grant none.
<a id="cite-facs.lease.grant"></a>

- **Read** needs the open to hold a read right, and no open under
  another key to hold write access.
- **Write** needs the open to hold a write right, and no open of the
  file under another key.
- **Handle** is granted with read.

A state of zero releases the lease. A lease is also released when the
last open under its key closes, unless it holds handle caching.

<a id="trm-3-9-12-3"></a>

## What breaks a lease <a id="cite-facs.lease.break-points"></a>

Only operations from outside the holder break its lease: an operation
through an open under the lease's own key never does.

| Operation by another holder | Breaks | Reason |
|---|---|---|
| Opening the file | Write | `KACS_LEASE_BREAK_OPEN` |
| An open refused by a sharing conflict | Handle, then the open is checked again | `KACS_LEASE_BREAK_SHARING` |
| Writing the file | Read | `KACS_LEASE_BREAK_WRITE` |
| Changing its size | Read | `KACS_LEASE_BREAK_SIZE` |
| Taking a byte-range lock | Read | `KACS_LEASE_BREAK_LOCK` |
| Renaming or linking it, or renaming a directory above it | Handle | `KACS_LEASE_BREAK_NAMESPACE` |
| Deleting it, or setting its delete disposition | Handle | `KACS_LEASE_BREAK_DELETE` |
| Changing its security descriptor | Handle | `KACS_LEASE_BREAK_SECURITY` |
| Changing its attributes or extended attributes | Read | `KACS_LEASE_BREAK_ATTRIBUTES` |
| Adding, removing or renaming an entry of a leased directory | Read and handle | `KACS_LEASE_BREAK_CHILD` |

Breaking write also breaks whatever the new open could not share: a
writer breaks read as well. A broken lease falls to the state the
operation can live with, not necessarily to none.

The holder of a lease that loses only read caching can lose nothing it
has not already written, so such a break is a **notice**: the operation
does not wait for it. Every other break waits. <a id="cite-facs.lease.read-break-no-wait"></a>

Most of these are the points at which Linux breaks its own leases and
NFS delegations, and KACS's leases are entries in the same table, so
the existing break points reach them. KACS adds the others: writes and
size changes through descriptors that were already open, byte-range
locks, security changes, and sharing conflicts.

<a id="trm-3-9-12-4"></a>

## Break notices <a id="cite-facs.lease.notices"></a>

Reading a lease-manager descriptor returns break notices, each a
`struct kacs_lease_break`: the lease's key, the file's device and inode
number, the current and new state, the reason, and an epoch that counts
the lease's breaks. The descriptor is readable with `poll()` when a
notice is waiting.

Notices are never dropped. A lease has at most one break outstanding,
so a manager's queue is bounded by the number of leases it holds.
<a id="cite-facs.lease.lossless"></a>

The holder acknowledges a break with `kacs_lease`, setting
`KACS_LEASE_ACKNOWLEDGE` and a state no greater than the notice's new
state. The waiting operation then proceeds.

<a id="trm-3-9-12-5"></a>

## Timeouts <a id="cite-facs.lease.timeout"></a>

A break not acknowledged within the manager's break timeout is
completed by KACS: the lease is reduced to the new state, the waiting
operation proceeds, and the manager receives a notice with reason
`KACS_LEASE_BREAK_TIMEOUT`. The timeout is set when the manager is
created, in milliseconds, from 1 to 35 000; zero gives the default of
35 seconds, the time SMB allows a client to acknowledge a break.

An operation waiting on a break can be interrupted by a signal. Only
the waiting operation fails; the break goes on.

<a id="trm-3-9-12-6"></a>

## Stacked filesystems <a id="cite-facs.lease.stacked"></a>

Through StrataFS, a regular file's lease is held on the provider its
open reaches, so it covers every route to that file. A copy-up gives the
file a new provider: a lease taken before it stays with the former
provider, and changes made through the copy do not break it. Leases on
StrataFS directories, and on anything reached through overlayfs, are not
supported; `kacs_lease` fails with `EOPNOTSUPP`.
