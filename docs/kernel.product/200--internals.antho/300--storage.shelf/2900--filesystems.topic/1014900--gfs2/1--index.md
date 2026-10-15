---
title: "Global File System 2"
type: reference
description: "GFS2 is a cluster file system. It allows a cluster of computers to simultaneously use a block device that is shared between them (with FC, iSCSI, NBD, etc). GFS2 reads and writes to the block device like a local file system, but also uses…"
---

<a id="rst-global-file-system-2"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-overview"></a>

## Overview

GFS2 is a cluster file system. It allows a cluster of computers to simultaneously use a block device that is shared between them (with FC, iSCSI, NBD, etc).  GFS2 reads and writes to the block device like a local file system, but also uses a lock module to allow the computers coordinate their I/O so file system consistency is maintained.  One of the nifty features of GFS2 is perfect consistency -- changes made to the file system on one machine show up immediately on all other machines in the cluster.

GFS2 uses interchangeable inter-node locking mechanisms, the currently supported mechanisms are:

> - **lock_nolock**
>
>   - allows GFS2 to be used as a local file system
>
> - **lock_dlm**
>
>   - uses the distributed lock manager (dlm) for inter-node locking. The dlm is found at linux/fs/dlm/

lock_dlm depends on user space cluster management systems found at the URL above.

To use GFS2 as a local file system, no external clustering systems are needed, simply:



```text
$ mkfs -t gfs2 -p lock_nolock -j 1 /dev/block_device
$ mount -t gfs2 /dev/block_device /dir
```

The gfs2-utils package is required on all cluster nodes and, for lock_dlm, you will also need the dlm and corosync user space utilities configured as per the documentation.

gfs2-utils can be found at [https://pagure.io/gfs2-utils](<https://pagure.io/gfs2-utils>)

GFS2 is not on-disk compatible with previous versions of GFS, but it is pretty close.

The following man pages are available from gfs2-utils:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> fsck.gfs2
>
> </td>
> <td>
>
>
> to repair a filesystem
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> gfs2_grow
>
> </td>
> <td>
>
>
> to expand a filesystem online
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> gfs2_jadd
>
> </td>
> <td>
>
>
> to add journals to a filesystem online
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> tunegfs2
>
> </td>
> <td>
>
>
> to manipulate, examine and tune a filesystem
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> gfs2_convert
>
> </td>
> <td>
>
>
> to convert a gfs filesystem to GFS2 in-place
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> mkfs.gfs2
>
> </td>
> <td>
>
>
> to make a filesystem
>
> </td>
> </tr>
> </tbody>
> </table>

<a id="rst-implementation-notes"></a>

## Implementation Notes

- [Glock internal locking rules](<~kernel/internals/filesystems/gfs2/glocks>)
- [uevents and GFS2](<~kernel/internals/filesystems/gfs2/uevents>)
