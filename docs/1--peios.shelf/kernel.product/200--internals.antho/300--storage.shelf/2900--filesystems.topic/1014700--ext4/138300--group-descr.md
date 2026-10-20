---
title: "Block Group Descriptors"
type: reference
description: "Each block group on the filesystem has one of these descriptors associated with it. As noted in the Layout section above, the group descriptors (if present) are the second item in the block group. The standard configuration is for each…"
---

<a id="rst-block-group-descriptors"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

Each block group on the filesystem has one of these descriptors associated with it. As noted in the Layout section above, the group descriptors (if present) are the second item in the block group. The standard configuration is for each block group to contain a full copy of the block group descriptor table unless the sparse_super feature flag is set.

Notice how the group descriptor records the location of both bitmaps and the inode table (i.e. they can float). This means that within a block group, the only data structures with fixed locations are the superblock and the group descriptor table. The flex_bg mechanism uses this property to group several block groups into a flex group and lay out all of the groups' bitmaps and inode tables into one long run in the first group of the flex group.

If the meta_bg feature flag is set, then several block groups are grouped together into a meta group. Note that in the meta_bg case, however, the first and last two block groups within the larger meta group contain only group descriptors for the groups inside the meta group.

flex_bg and meta_bg do not appear to be mutually exclusive features.

In ext2, ext3, and ext4 (when the 64bit feature is not enabled), the block group descriptor was only 32 bytes long and therefore ends at bg_checksum. On an ext4 filesystem with the 64bit feature enabled, the block group descriptor expands to at least the 64 bytes described below; the size is stored in the superblock.

If gdt_csum is set and metadata_csum is not set, the block group checksum is the crc16 of the FS UUID, the group number, and the group descriptor structure. If metadata_csum is set, then the block group checksum is the lower 16 bits of the checksum of the FS UUID, the group number, and the group descriptor structure. Both block and inode bitmap checksums are calculated against the FS UUID, the group number, and the entire bitmap.

The block group descriptor is laid out in `struct ext4_group_desc`.


<table>
<thead>
<tr>
<th>


Offset

</th>
<th>


Size

</th>
<th>


Name

</th>
<th>


Description

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


0x0

</td>
<td>


\__le32

</td>
<td>


bg_block_bitmap_lo

</td>
<td>


Lower 32-bits of location of block bitmap.

</td>
</tr>
<tr>
<td>


0x4

</td>
<td>


\__le32

</td>
<td>


bg_inode_bitmap_lo

</td>
<td>


Lower 32-bits of location of inode bitmap.

</td>
</tr>
<tr>
<td>


0x8

</td>
<td>


\__le32

</td>
<td>


bg_inode_table_lo

</td>
<td>


Lower 32-bits of location of inode table.

</td>
</tr>
<tr>
<td>


0xC

</td>
<td>


\__le16

</td>
<td>


bg_free_blocks_count_lo

</td>
<td>


Lower 16-bits of free block count.

</td>
</tr>
<tr>
<td>


0xE

</td>
<td>


\__le16

</td>
<td>


bg_free_inodes_count_lo

</td>
<td>


Lower 16-bits of free inode count.

</td>
</tr>
<tr>
<td>


0x10

</td>
<td>


\__le16

</td>
<td>


bg_used_dirs_count_lo

</td>
<td>


Lower 16-bits of directory count.

</td>
</tr>
<tr>
<td>


0x12

</td>
<td>


\__le16

</td>
<td>


bg_flags

</td>
<td>


Block group flags. See the [bgflags](<#rst-bgflags>) table below.

</td>
</tr>
<tr>
<td>


0x14

</td>
<td>


\__le32

</td>
<td>


bg_exclude_bitmap_lo

</td>
<td>


Lower 32-bits of location of snapshot exclusion bitmap.

</td>
</tr>
<tr>
<td>


0x18

</td>
<td>


\__le16

</td>
<td>


bg_block_bitmap_csum_lo

</td>
<td>


Lower 16-bits of the block bitmap checksum.

</td>
</tr>
<tr>
<td>


0x1A

</td>
<td>


\__le16

</td>
<td>


bg_inode_bitmap_csum_lo

</td>
<td>


Lower 16-bits of the inode bitmap checksum.

</td>
</tr>
<tr>
<td>


0x1C

</td>
<td>


\__le16

</td>
<td>


bg_itable_unused_lo

</td>
<td>


Lower 16-bits of unused inode count. If set, we needn't scan past the `(sb.s_inodes_per_group - gdt.bg_itable_unused)` th entry in the inode table for this group.

</td>
</tr>
<tr>
<td>


0x1E

</td>
<td>


\__le16

</td>
<td>


bg_checksum

</td>
<td>


Group descriptor checksum; crc16(sb_uuid+group_num+bg_desc) if the RO_COMPAT_GDT_CSUM feature is set, or crc32c(sb_uuid+group_num+bg_desc) &amp; 0xFFFF if the RO_COMPAT_METADATA_CSUM feature is set.  The bg_checksum field in bg_desc is skipped when calculating crc16 checksum, and set to zero if crc32c checksum is used.

</td>
</tr>
<tr>
<td>




</td>
<td>




</td>
<td>




</td>
<td>


These fields only exist if the 64bit feature is enabled and s_desc_size &gt; 32.

</td>
</tr>
<tr>
<td>


0x20

</td>
<td>


\__le32

</td>
<td>


bg_block_bitmap_hi

</td>
<td>


Upper 32-bits of location of block bitmap.

</td>
</tr>
<tr>
<td>


0x24

</td>
<td>


\__le32

</td>
<td>


bg_inode_bitmap_hi

</td>
<td>


Upper 32-bits of location of inodes bitmap.

</td>
</tr>
<tr>
<td>


0x28

</td>
<td>


\__le32

</td>
<td>


bg_inode_table_hi

</td>
<td>


Upper 32-bits of location of inodes table.

</td>
</tr>
<tr>
<td>


0x2C

</td>
<td>


\__le16

</td>
<td>


bg_free_blocks_count_hi

</td>
<td>


Upper 16-bits of free block count.

</td>
</tr>
<tr>
<td>


0x2E

</td>
<td>


\__le16

</td>
<td>


bg_free_inodes_count_hi

</td>
<td>


Upper 16-bits of free inode count.

</td>
</tr>
<tr>
<td>


0x30

</td>
<td>


\__le16

</td>
<td>


bg_used_dirs_count_hi

</td>
<td>


Upper 16-bits of directory count.

</td>
</tr>
<tr>
<td>


0x32

</td>
<td>


\__le16

</td>
<td>


bg_itable_unused_hi

</td>
<td>


Upper 16-bits of unused inode count.

</td>
</tr>
<tr>
<td>


0x34

</td>
<td>


\__le32

</td>
<td>


bg_exclude_bitmap_hi

</td>
<td>


Upper 32-bits of location of snapshot exclusion bitmap.

</td>
</tr>
<tr>
<td>


0x38

</td>
<td>


\__le16

</td>
<td>


bg_block_bitmap_csum_hi

</td>
<td>


Upper 16-bits of the block bitmap checksum.

</td>
</tr>
<tr>
<td>


0x3A

</td>
<td>


\__le16

</td>
<td>


bg_inode_bitmap_csum_hi

</td>
<td>


Upper 16-bits of the inode bitmap checksum.

</td>
</tr>
<tr>
<td>


0x3C

</td>
<td>


\__u32

</td>
<td>


bg_reserved

</td>
<td>


Padding to 64 bytes.

</td>
</tr>
</tbody>
</table>

<a id="rst-bgflags"></a>

Block group flags can be any combination of the following:


<table>
<thead>
<tr>
<th>


Value

</th>
<th>


Description

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


0x1

</td>
<td>


inode table and bitmap are not initialized (EXT4_BG_INODE_UNINIT).

</td>
</tr>
<tr>
<td>


0x2

</td>
<td>


block bitmap is not initialized (EXT4_BG_BLOCK_UNINIT).

</td>
</tr>
<tr>
<td>


0x4

</td>
<td>


inode table is zeroed (EXT4_BG_INODE_ZEROED).

</td>
</tr>
</tbody>
</table>
