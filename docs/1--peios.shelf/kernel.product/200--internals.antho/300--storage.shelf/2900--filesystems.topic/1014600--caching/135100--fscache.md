---
title: "General Filesystem Caching"
type: reference
description: "This facility is a general purpose cache for network filesystems, though it could be used for caching other things such as ISO9660 filesystems too."
---

<a id="rst-general-filesystem-caching"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-overview"></a>

## Overview

This facility is a general purpose cache for network filesystems, though it could be used for caching other things such as ISO9660 filesystems too.

FS-Cache mediates between cache backends (such as CacheFiles) and network filesystems:



```text
+---------+
|         |                                    +--------------+
|   NFS   |--+                                 |              |
|         |  |                             +-->|   CacheFS    |
+---------+  |               +----------+  |   |  /dev/hda5   |
             |               |          |  |   +--------------+
+---------+  +-------------->|          |  |
|         |      +-------+   |          |--+
|   AFS   |----->|       |   | FS-Cache |
|         |      | netfs |-->|          |--+
+---------+  +-->|  lib  |   |          |  |
             |   |       |   |          |  |   +--------------+
+---------+  |   +-------+   +----------+  |   |              |
|         |  |                             +-->|  CacheFiles  |
|   9P    |--+                                 |  /var/cache  |
|         |                                    +--------------+
+---------+
```

Or to look at it another way, FS-Cache is a module that provides a caching facility to a network filesystem such that the cache is transparent to the user:



```text
+---------+
|         |
| Server  |
|         |
+---------+
     |                  NETWORK
~~~~~|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     |
     |           +----------+
     V           |          |
+---------+      |          |
|         |      |          |
|   NFS   |----->| FS-Cache |
|         |      |          |--+
+---------+      |          |  |   +--------------+   +--------------+
     |           |          |  |   |              |   |              |
     V           +----------+  +-->|  CacheFiles  |-->|  Ext3        |
+---------+                        |  /var/cache  |   |  /dev/sda6   |
|         |                        +--------------+   +--------------+
|   VFS   |                                ^                     ^
|         |                                |                     |
+---------+                                +--------------+      |
     |                  KERNEL SPACE                      |      |
~~~~~|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|~~~~~~|~~~~
     |                  USER SPACE                        |      |
     V                                                    |      |
+---------+                                           +--------------+
|         |                                           |              |
| Process |                                           | cachefilesd  |
|         |                                           |              |
+---------+                                           +--------------+
```

FS-Cache does not follow the idea of completely loading every netfs file opened in its entirety into a cache before permitting it to be accessed and then serving the pages out of that cache rather than the netfs inode because:

> 1. It must be practical to operate without a cache.
>
> 2. The size of any accessible file must not be limited to the size of the cache.
>
> 3. The combined size of all opened files (this includes mapped libraries) must not be limited to the size of the cache.
>
> 4. The user should not be forced to download an entire file just to do a one-off access of a small portion of it (such as might be done with the "file" program).

It instead serves the cache out in chunks as and when requested by the netfs using it.

FS-Cache provides the following facilities:

> - More than one cache can be used at once.  Caches can be selected explicitly by use of tags.
>
> - Caches can be added / removed at any time, even whilst being accessed.
>
> - The netfs is provided with an interface that allows either party to withdraw caching facilities from a file (required for (2)).
>
> - The interface to the netfs returns as few errors as possible, preferring rather to let the netfs remain oblivious.
>
> - There are three types of cookie: cache, volume and data file cookies. Cache cookies represent the cache as a whole and are not normally visible to the netfs; the netfs gets a volume cookie to represent a collection of files (typically something that a netfs would get for a superblock); and data file cookies are used to cache data (something that would be got for an inode).
>
> - Volumes are matched using a key.  This is a printable string that is used to encode all the information that might be needed to distinguish one superblock, say, from another.  This would be a compound of things like cell name or server address, volume name or share path.  It must be a valid pathname.
>
> - Cookies are matched using a key.  This is a binary blob and is used to represent the object within a volume (so the volume key need not form part of the blob).  This might include things like an inode number and uniquifier or a file handle.
>
> - Cookie resources are set up and pinned by marking the cookie in-use. This prevents the backing resources from being culled.  Timed garbage collection is employed to eliminate cookies that haven't been used for a short while, thereby reducing resource overload.  This is intended to be used when a file is opened or closed.
>
>   A cookie can be marked in-use multiple times simultaneously; each mark must be unused.
>
> - Begin/end access functions are provided to delay cache withdrawal for the duration of an operation and prevent structs from being freed whilst we're looking at them.
>
> - Data I/O is done by asynchronous DIO to/from a buffer described by the netfs using an iov_iter.
>
> - An invalidation facility is available to discard data from the cache and to deal with I/O that's in progress that is accessing old data.
>
> - Cookies can be "retired" upon release, thereby causing the object to be removed from the cache.

The netfs API to FS-Cache can be found in:

> [Documentation/filesystems/caching/netfs-api.rst](~kernel/internals/filesystems/caching/netfs-api)

The cache backend API to FS-Cache can be found in:

> [Documentation/filesystems/caching/backend-api.rst](~kernel/internals/filesystems/caching/backend-api)

<a id="rst-statistical-information"></a>

## Statistical Information

If FS-Cache is compiled with the following options enabled:



```text
CONFIG_FSCACHE_STATS=y
```

then it will gather certain statistics and display them through:

> /proc/fs/fscache/stats

This shows counts of a number of events that can happen in FS-Cache:


<table>
<thead>
<tr>
<th>


CLASS

</th>
<th>


EVENT

</th>
<th>


MEANING

</th>
</tr>
</thead>
<tbody>
<tr>
<td rowspan="4">


Cookies

</td>
<td>


n=N

</td>
<td>


Number of data storage cookies allocated

</td>
</tr>
<tr>
<td>


v=N

</td>
<td>


Number of volume index cookies allocated

</td>
</tr>
<tr>
<td>


vcol=N

</td>
<td>


Number of volume index key collisions

</td>
</tr>
<tr>
<td>


voom=N

</td>
<td>


Number of OOM events when allocating volume cookies

</td>
</tr>
<tr>
<td rowspan="3">


Acquire

</td>
<td>


n=N

</td>
<td>


Number of acquire cookie requests seen

</td>
</tr>
<tr>
<td>


ok=N

</td>
<td>


Number of acq reqs succeeded

</td>
</tr>
<tr>
<td>


oom=N

</td>
<td>


Number of acq reqs failed on ENOMEM

</td>
</tr>
<tr>
<td rowspan="5">


LRU

</td>
<td>


n=N

</td>
<td>


Number of cookies currently on the LRU

</td>
</tr>
<tr>
<td>


exp=N

</td>
<td>


Number of cookies expired off of the LRU

</td>
</tr>
<tr>
<td>


rmv=N

</td>
<td>


Number of cookies removed from the LRU

</td>
</tr>
<tr>
<td>


drp=N

</td>
<td>


Number of LRU'd cookies relinquished/withdrawn

</td>
</tr>
<tr>
<td>


at=N

</td>
<td>


Time till next LRU cull (jiffies)

</td>
</tr>
<tr>
<td>


Invals

</td>
<td>


n=N

</td>
<td>


Number of invalidations

</td>
</tr>
<tr>
<td rowspan="3">


Updates

</td>
<td>


n=N

</td>
<td>


Number of update cookie requests seen

</td>
</tr>
<tr>
<td>


rsz=N

</td>
<td>


Number of resize requests

</td>
</tr>
<tr>
<td>


rsn=N

</td>
<td>


Number of skipped resize requests

</td>
</tr>
<tr>
<td rowspan="3">


Relinqs

</td>
<td>


n=N

</td>
<td>


Number of relinquish cookie requests seen

</td>
</tr>
<tr>
<td>


rtr=N

</td>
<td>


Number of rlq reqs with retire=true

</td>
</tr>
<tr>
<td>


drop=N

</td>
<td>


Number of cookies no longer blocking re-acquisition

</td>
</tr>
<tr>
<td rowspan="3">


NoSpace

</td>
<td>


nwr=N

</td>
<td>


Number of write requests refused due to lack of space

</td>
</tr>
<tr>
<td>


ncr=N

</td>
<td>


Number of create requests refused due to lack of space

</td>
</tr>
<tr>
<td>


cull=N

</td>
<td>


Number of objects culled to make space

</td>
</tr>
<tr>
<td rowspan="2">


IO

</td>
<td>


rd=N

</td>
<td>


Number of read operations in the cache

</td>
</tr>
<tr>
<td>


wr=N

</td>
<td>


Number of write operations in the cache

</td>
</tr>
</tbody>
</table>

Netfslib will also add some stats counters of its own.

<a id="rst-cache-list"></a>

## Cache List

FS-Cache provides a list of cache cookies:

> /proc/fs/fscache/cookies

This will look something like:



```text
# cat /proc/fs/fscache/caches
CACHE    REF   VOLS  OBJS  ACCES S NAME
======== ===== ===== ===== ===== = ===============
00000001     2     1  2123     1 A default
```

where the columns are:

>
> <table>
> <thead>
> <tr>
> <th>
>
>
> COLUMN
>
> </th>
> <th>
>
>
> DESCRIPTION
>
> </th>
> </tr>
> </thead>
> <tbody>
> <tr>
> <td>
>
>
> CACHE
>
> </td>
> <td>
>
>
> Cache cookie debug ID (also appears in traces)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> REF
>
> </td>
> <td>
>
>
> Number of references on the cache cookie
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> VOLS
>
> </td>
> <td>
>
>
> Number of volumes cookies in this cache
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> OBJS
>
> </td>
> <td>
>
>
> Number of cache objects in use
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> ACCES
>
> </td>
> <td>
>
>
> Number of accesses pinning the cache
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> S
>
> </td>
> <td>
>
>
> State
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> NAME
>
> </td>
> <td>
>
>
> Name of the cache.
>
> </td>
> </tr>
> </tbody>
> </table>

The state can be (-) Inactive, (P)reparing, (A)ctive, (E)rror or (W)ithdrawing.

<a id="rst-volume-list"></a>

## Volume List

FS-Cache provides a list of volume cookies:

> /proc/fs/fscache/volumes

This will look something like:



```text
VOLUME   REF   nCOOK ACC FL CACHE           KEY
======== ===== ===== === == =============== ================
00000001    55    54   1 00 default         afs,example.com,100058
```

where the columns are:

>
> <table>
> <thead>
> <tr>
> <th>
>
>
> COLUMN
>
> </th>
> <th>
>
>
> DESCRIPTION
>
> </th>
> </tr>
> </thead>
> <tbody>
> <tr>
> <td>
>
>
> VOLUME
>
> </td>
> <td>
>
>
> The volume cookie debug ID (also appears in traces)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> REF
>
> </td>
> <td>
>
>
> Number of references on the volume cookie
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> nCOOK
>
> </td>
> <td>
>
>
> Number of cookies in the volume
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> ACC
>
> </td>
> <td>
>
>
> Number of accesses pinning the cache
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> FL
>
> </td>
> <td>
>
>
> Flags on the volume cookie
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> CACHE
>
> </td>
> <td>
>
>
> Name of the cache or "-"
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> KEY
>
> </td>
> <td>
>
>
> The indexing key for the volume
>
> </td>
> </tr>
> </tbody>
> </table>

<a id="rst-cookie-list"></a>

## Cookie List

FS-Cache provides a list of cookies:

> /proc/fs/fscache/cookies

This will look something like:



```text
# head /proc/fs/fscache/cookies
COOKIE   VOLUME   REF ACT ACC S FL DEF
======== ======== === === === = == ================
00000435 00000001   1   0  -1 - 08 0000000201d080070000000000000000, 0000000000000000
00000436 00000001   1   0  -1 - 00 0000005601d080080000000000000000, 0000000000000051
00000437 00000001   1   0  -1 - 08 00023b3001d0823f0000000000000000, 0000000000000000
00000438 00000001   1   0  -1 - 08 0000005801d0807b0000000000000000, 0000000000000000
00000439 00000001   1   0  -1 - 08 00023b3201d080a10000000000000000, 0000000000000000
0000043a 00000001   1   0  -1 - 08 00023b3401d080a30000000000000000, 0000000000000000
0000043b 00000001   1   0  -1 - 08 00023b3601d080b30000000000000000, 0000000000000000
0000043c 00000001   1   0  -1 - 08 00023b3801d080b40000000000000000, 0000000000000000
```

where the columns are:

>
> <table>
> <thead>
> <tr>
> <th>
>
>
> COLUMN
>
> </th>
> <th>
>
>
> DESCRIPTION
>
> </th>
> </tr>
> </thead>
> <tbody>
> <tr>
> <td>
>
>
> COOKIE
>
> </td>
> <td>
>
>
> The cookie debug ID (also appears in traces)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> VOLUME
>
> </td>
> <td>
>
>
> The parent volume cookie debug ID
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> REF
>
> </td>
> <td>
>
>
> Number of references on the volume cookie
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> ACT
>
> </td>
> <td>
>
>
> Number of times the cookie is marked for in use
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> ACC
>
> </td>
> <td>
>
>
> Number of access pins in the cookie
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> S
>
> </td>
> <td>
>
>
> State of the cookie
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> FL
>
> </td>
> <td>
>
>
> Flags on the cookie
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> DEF
>
> </td>
> <td>
>
>
> Key, auxiliary data
>
> </td>
> </tr>
> </tbody>
> </table>

<a id="rst-debugging"></a>

## Debugging

If CONFIG_NETFS_DEBUG is enabled, the FS-Cache facility and NETFS support can have runtime debugging enabled by adjusting the value in:



```text
/sys/module/netfs/parameters/debug
```

This is a bitmask of debugging streams to enable:

>
> <table>
> <thead>
> <tr>
> <th>
>
>
> BIT
>
> </th>
> <th>
>
>
> VALUE
>
> </th>
> <th>
>
>
> STREAM
>
> </th>
> <th>
>
>
> POINT
>
> </th>
> </tr>
> </thead>
> <tbody>
> <tr>
> <td>
>
>
> 0
>
> </td>
> <td>
>
>
> 1
>
> </td>
> <td>
>
>
> Cache management
>
> </td>
> <td>
>
>
> Function entry trace
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 1
>
> </td>
> <td>
>
>
> 2
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> Function exit trace
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 2
>
> </td>
> <td>
>
>
> 4
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> General
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 3
>
> </td>
> <td>
>
>
> 8
>
> </td>
> <td>
>
>
> Cookie management
>
> </td>
> <td>
>
>
> Function entry trace
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 4
>
> </td>
> <td>
>
>
> 16
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> Function exit trace
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 5
>
> </td>
> <td>
>
>
> 32
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> General
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 6-8
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> (Not used)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9
>
> </td>
> <td>
>
>
> 512
>
> </td>
> <td>
>
>
> I/O operation management
>
> </td>
> <td>
>
>
> Function entry trace
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 10
>
> </td>
> <td>
>
>
> 1024
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> Function exit trace
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 11
>
> </td>
> <td>
>
>
> 2048
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> General
>
> </td>
> </tr>
> </tbody>
> </table>

The appropriate set of values should be OR'd together and the result written to the control file.  For example:



```text
echo $((1|8|512)) >/sys/module/netfs/parameters/debug
```

will turn on all function entry debugging.
