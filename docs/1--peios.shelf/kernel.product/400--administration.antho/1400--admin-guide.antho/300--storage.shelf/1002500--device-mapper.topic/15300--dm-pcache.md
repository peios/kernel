---
title: "dm-pcache — Persistent Cache"
type: reference
description: "Author: Dongsheng Yang <dongsheng.yang@linux.dev>"
---

<a id="rst-dm-pcache-persistent-cache"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

*Author: Dongsheng Yang &lt;dongsheng.yang@linux.dev&gt;*

This document describes *dm-pcache*, a Device-Mapper target that lets a byte-addressable *DAX* (persistent-memory, “pmem”) region act as a high-performance, crash-persistent cache in front of a slower block device.  The code lives in `drivers/md/dm-pcache/`.

<a id="rst-quick-feature-summary"></a>

## Quick feature summary

- *Write-back* caching (only mode currently supported).

- *16 MiB segments* allocated on the pmem device.

- *Data CRC32* verification (optional, per cache).

- Crash-safe: every metadata structure is duplicated (`PCACHE_META_INDEX_MAX == 2`) and protected with CRC+sequence numbers.

- *Multi-tree indexing* (indexing trees sharded by logical address) for high PMem parallelism

- Pure *DAX path* I/O – no extra BIO round-trips

- *Log-structured write-back* that preserves backend crash-consistency

<a id="rst-constructor"></a>

## Constructor



```text
pcache <cache_dev> <backing_dev> [<number_of_optional_arguments> <cache_mode writeback> <data_crc true|false>]
```


<table>
<tbody>
<tr>
<td>


`cache_dev`

</td>
<td>


Any DAX-capable block device (`/dev/pmem0`…). All metadata *and* cached blocks are stored here.

</td>
</tr>
<tr>
<td>


`backing_dev`

</td>
<td>


The slow block device to be cached.

</td>
</tr>
<tr>
<td>


`cache_mode`

</td>
<td>


Optional, Only `writeback` is accepted at the moment.

</td>
</tr>
<tr>
<td>


`data_crc`

</td>
<td>


Optional, default to `false`

- `true`  – store CRC32 for every cached entry and verify on reads

- `false` – skip CRC (faster)

</td>
</tr>
</tbody>
</table>

<a id="rst-example"></a>

### Example



```shell
dmsetup create pcache_sdb --table \
  "0 $(blockdev --getsz /dev/sdb) pcache /dev/pmem0 /dev/sdb 4 cache_mode writeback data_crc true"
```

The first time a pmem device is used, dm-pcache formats it automatically (super-block, cache_info, etc.).

<a id="rst-status-line"></a>

## Status line

`dmsetup status <device>` (`STATUSTYPE_INFO`) prints:



```text
<sb_flags> <seg_total> <cache_segs> <segs_used> \
<gc_percent> <cache_flags> \
<key_head_seg>:<key_head_off> \
<dirty_tail_seg>:<dirty_tail_off> \
<key_tail_seg>:<key_tail_off>
```

<a id="rst-field-meanings"></a>

### Field meanings


<table>
<tbody>
<tr>
<td>


`sb_flags`

</td>
<td>


Super-block flags (e.g. endian marker).

</td>
</tr>
<tr>
<td>


`seg_total`

</td>
<td>


Number of physical *pmem* segments.

</td>
</tr>
<tr>
<td>


`cache_segs`

</td>
<td>


Number of segments used for cache.

</td>
</tr>
<tr>
<td>


`segs_used`

</td>
<td>


Segments currently allocated (bitmap weight).

</td>
</tr>
<tr>
<td>


`gc_percent`

</td>
<td>


Current GC high-water mark (0-90).

</td>
</tr>
<tr>
<td>


`cache_flags`

</td>
<td>


Bit 0 – DATA_CRC enabled Bit 1 – INIT_DONE (cache initialised) Bits 2-5 – cache mode (0 == WB).

</td>
</tr>
<tr>
<td>


`key_head`

</td>
<td>


Where new key-sets are being written.

</td>
</tr>
<tr>
<td>


`dirty_tail`

</td>
<td>


First dirty key-set that still needs write-back to the backing device.

</td>
</tr>
<tr>
<td>


`key_tail`

</td>
<td>


First key-set that may be reclaimed by GC.

</td>
</tr>
</tbody>
</table>

<a id="rst-messages"></a>

## Messages

*Change GC trigger*



```text
dmsetup message <dev> 0 gc_percent <0-90>
```

<a id="rst-theory-of-operation"></a>

## Theory of operation

<a id="rst-sub-devices"></a>

### Sub-devices


<table>
<tbody>
<tr>
<td>


backing_dev

</td>
<td>


Any block device (SSD/HDD/loop/LVM, etc.).

</td>
</tr>
<tr>
<td>


cache_dev

</td>
<td>


DAX device; must expose direct-access memory.

</td>
</tr>
</tbody>
</table>

<a id="rst-segments-and-key-sets"></a>

### Segments and key-sets

- The pmem space is divided into *16 MiB segments*.

- Each write allocates space from a per-CPU *data_head* inside a segment.

- A *cache-key* records a logical range on the origin and where it lives inside pmem (segment + offset + generation).

- 128 keys form a *key-set* (kset); ksets are written sequentially in pmem and are themselves crash-safe (CRC).

- The pair *(key_tail, dirty_tail)* delimit clean/dirty and live/dead ksets.

<a id="rst-write-back"></a>

### Write-back

Dirty keys are queued into a tree; a background worker copies data back to the backing_dev and advances *dirty_tail*.  A FLUSH/FUA bio from the upper layers forces an immediate metadata commit.

<a id="rst-garbage-collection"></a>

### Garbage collection

GC starts when `segs_used >= seg_total * gc_percent / 100`.  It walks from *key_tail*, frees segments whose every key has been invalidated, and advances *key_tail*.

<a id="rst-crc-verification"></a>

### CRC verification

If `data_crc is enabled` dm-pcache computes a CRC32 over every cached data range when it is inserted and stores it in the on-media key.  Reads validate the CRC before copying to the caller.

<a id="rst-failure-handling"></a>

## Failure handling

- *pmem media errors* – all metadata copies are read with `copy_mc_to_kernel`; an uncorrectable error logs and aborts initialisation.

- *Cache full* – if no free segment can be found, writes return `-EBUSY`; dm-pcache retries internally (request deferral).

- *System crash* – on attach, the driver replays ksets from *key_tail* to rebuild the in-core trees; every segment’s generation guards against use-after-free keys.

<a id="rst-limitations-todo"></a>

## Limitations &amp; TODO

- Only *write-back* mode; other modes planned.

- Only FIFO cache invalidate; other (LRU, ARC...) planned.

- Table reload is not supported currently.

- Discard planned.

<a id="rst-example-workflow"></a>

## Example workflow



```shell
# 1.  Create devices
dmsetup create pcache_sdb --table \
  "0 $(blockdev --getsz /dev/sdb) pcache /dev/pmem0 /dev/sdb 4 cache_mode writeback data_crc true"

# 2.  Put a filesystem on top
mkfs.ext4 /dev/mapper/pcache_sdb
mount /dev/mapper/pcache_sdb /mnt

# 3.  Tune GC threshold to 80 %
dmsetup message pcache_sdb 0 gc_percent 80

# 4.  Observe status
watch -n1 'dmsetup status pcache_sdb'

# 5.  Shutdown
umount /mnt
dmsetup remove pcache_sdb
```

`dm-pcache` is under active development; feedback, bug reports and patches are very welcome\!
