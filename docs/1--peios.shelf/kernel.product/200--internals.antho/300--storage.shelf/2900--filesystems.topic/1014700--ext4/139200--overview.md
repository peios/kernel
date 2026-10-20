---
title: "High Level Design"
type: reference
description: "An ext4 file system is split into a series of block groups. To reduce performance difficulties due to fragmentation, the block allocator tries very hard to keep each file's blocks within the same group, thereby reducing seek times. The…"
---

<a id="rst-high-level-design"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

An ext4 file system is split into a series of block groups. To reduce performance difficulties due to fragmentation, the block allocator tries very hard to keep each file's blocks within the same group, thereby reducing seek times. The size of a block group is specified in `sb.s_blocks_per_group` blocks, though it can also calculated as 8 \* `block_size_in_bytes`. With the default block size of 4KiB, each group will contain 32,768 blocks, for a length of 128MiB. The number of block groups is the size of the device divided by the size of a block group.

All fields in ext4 are written to disk in little-endian order. HOWEVER, all fields in jbd2 (the journal) are written to disk in big-endian order.

- [Blocks](<~kernel/internals/filesystems/ext4/blocks>)
- [Block Groups](<~kernel/internals/filesystems/ext4/blockgroup>)
- [Special inodes](<~kernel/internals/filesystems/ext4/special-inodes>)
- [Block and Inode Allocation Policy](<~kernel/internals/filesystems/ext4/allocators>)
- [Checksums](<~kernel/internals/filesystems/ext4/checksums>)
- [Bigalloc](<~kernel/internals/filesystems/ext4/bigalloc>)
- [Inline Data](<~kernel/internals/filesystems/ext4/inlinedata>)
- [Large Extended Attribute Values](<~kernel/internals/filesystems/ext4/eainode>)
- [Verity files](<~kernel/internals/filesystems/ext4/verity>)
- [Atomic Block Writes](<~kernel/internals/filesystems/ext4/atomic-writes>)
