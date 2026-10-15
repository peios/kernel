---
title: "Directory Entries"
type: reference
description: "In an ext4 filesystem, a directory is more or less a flat file that maps an arbitrary byte string (usually ASCII) to an inode number on the filesystem. There can be many directory entries across the filesystem that reference the same inode…"
---

<a id="rst-directory-entries"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

In an ext4 filesystem, a directory is more or less a flat file that maps an arbitrary byte string (usually ASCII) to an inode number on the filesystem. There can be many directory entries across the filesystem that reference the same inode number--these are known as hard links, and that is why hard links cannot reference files on other filesystems. As such, directory entries are found by reading the data block(s) associated with a directory file for the particular directory entry that is desired.

<a id="rst-linear-classic-directories"></a>

## Linear (Classic) Directories

By default, each directory lists its entries in an “almost-linear” array. I write “almost” because it's not a linear array in the memory sense because directory entries are not split across filesystem blocks. Therefore, it is more accurate to say that a directory is a series of data blocks and that each block contains a linear array of directory entries. The end of each per-block array is signified by reaching the end of the block; the last entry in the block has a record length that takes it all the way to the end of the block. The end of the entire directory is of course signified by reaching the end of the file. Unused directory entries are signified by inode = 0. By default the filesystem uses `struct ext4_dir_entry_2` for directory entries unless the “filetype” feature flag is not set, in which case it uses `struct ext4_dir_entry`.

The original directory entry format is `struct ext4_dir_entry`, which is at most 263 bytes long, though on disk you'll need to reference `dirent.rec_len` to know for sure.


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


inode

</td>
<td>


Number of the inode that this directory entry points to.

</td>
</tr>
<tr>
<td>


0x4

</td>
<td>


\__le16

</td>
<td>


rec_len

</td>
<td>


Length of this directory entry. Must be a multiple of 4.

</td>
</tr>
<tr>
<td>


0x6

</td>
<td>


\__le16

</td>
<td>


name_len

</td>
<td>


Length of the file name.

</td>
</tr>
<tr>
<td>


0x8

</td>
<td>


char

</td>
<td>


name\[EXT4_NAME_LEN\]

</td>
<td>


File name.

</td>
</tr>
</tbody>
</table>

Since file names cannot be longer than 255 bytes, the new directory entry format shortens the name_len field and uses the space for a file type flag, probably to avoid having to load every inode during directory tree traversal. This format is `ext4_dir_entry_2`, which is at most 263 bytes long, though on disk you'll need to reference `dirent.rec_len` to know for sure.


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


inode

</td>
<td>


Number of the inode that this directory entry points to.

</td>
</tr>
<tr>
<td>


0x4

</td>
<td>


\__le16

</td>
<td>


rec_len

</td>
<td>


Length of this directory entry.

</td>
</tr>
<tr>
<td>


0x6

</td>
<td>


\__u8

</td>
<td>


name_len

</td>
<td>


Length of the file name.

</td>
</tr>
<tr>
<td>


0x7

</td>
<td>


\__u8

</td>
<td>


file_type

</td>
<td>


File type code, see [ftype](<#rst-ftype>) table below.

</td>
</tr>
<tr>
<td>


0x8

</td>
<td>


char

</td>
<td>


name\[EXT4_NAME_LEN\]

</td>
<td>


File name.

</td>
</tr>
</tbody>
</table>

<a id="rst-ftype"></a>

The directory file type is one of the following values:


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


0x0

</td>
<td>


Unknown.

</td>
</tr>
<tr>
<td>


0x1

</td>
<td>


Regular file.

</td>
</tr>
<tr>
<td>


0x2

</td>
<td>


Directory.

</td>
</tr>
<tr>
<td>


0x3

</td>
<td>


Character device file.

</td>
</tr>
<tr>
<td>


0x4

</td>
<td>


Block device file.

</td>
</tr>
<tr>
<td>


0x5

</td>
<td>


FIFO.

</td>
</tr>
<tr>
<td>


0x6

</td>
<td>


Socket.

</td>
</tr>
<tr>
<td>


0x7

</td>
<td>


Symbolic link.

</td>
</tr>
</tbody>
</table>

To support directories that are both encrypted and casefolded directories, we must also include hash information in the directory entry. We append `ext4_extended_dir_entry_2` to `ext4_dir_entry_2` except for the entries for dot and dotdot, which are kept the same. The structure follows immediately after `name` and is included in the size listed by `rec_len` If a directory entry uses this extension, it may be up to 271 bytes.


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


hash

</td>
<td>


The hash of the directory name

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


minor_hash

</td>
<td>


The minor hash of the directory name

</td>
</tr>
</tbody>
</table>

In order to add checksums to these classic directory blocks, a phony `struct ext4_dir_entry` is placed at the end of each leaf block to hold the checksum. The directory entry is 12 bytes long. The inode number and name_len fields are set to zero to fool old software into ignoring an apparently empty directory entry, and the checksum is stored in the place where the name normally goes. The structure is `struct ext4_dir_entry_tail`:


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


det_reserved_zero1

</td>
<td>


Inode number, which must be zero.

</td>
</tr>
<tr>
<td>


0x4

</td>
<td>


\__le16

</td>
<td>


det_rec_len

</td>
<td>


Length of this directory entry, which must be 12.

</td>
</tr>
<tr>
<td>


0x6

</td>
<td>


\__u8

</td>
<td>


det_reserved_zero2

</td>
<td>


Length of the file name, which must be zero.

</td>
</tr>
<tr>
<td>


0x7

</td>
<td>


\__u8

</td>
<td>


det_reserved_ft

</td>
<td>


File type, which must be 0xDE.

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


det_checksum

</td>
<td>


Directory leaf block checksum.

</td>
</tr>
</tbody>
</table>

The leaf directory block checksum is calculated against the FS UUID (or the checksum seed, if that feature is enabled for the fs), the directory's inode number, the directory's inode generation number, and the entire directory entry block up to (but not including) the fake directory entry.

<a id="rst-hash-tree-directories"></a>

## Hash Tree Directories

A linear array of directory entries isn't great for performance, so a new feature was added to ext3 to provide a faster (but peculiar) balanced tree keyed off a hash of the directory entry name. If the EXT4_INDEX_FL (0x1000) flag is set in the inode, this directory uses a hashed btree (htree) to organize and find directory entries. For backwards read-only compatibility with ext2, interior tree nodes are actually hidden inside the directory file, masquerading as “empty” directory entries spanning the whole block. It was stated previously that directory entries with the inode set to 0 are treated as unused entries; this is (ab)used to fool the old linear-scan algorithm into skipping over those blocks containing the interior tree node data.

The root of the tree always lives in the first data block of the directory. By ext2 custom, the '.' and '..' entries must appear at the beginning of this first block, so they are put here as two `struct ext4_dir_entry_2` s and not stored in the tree. The rest of the root node contains metadata about the tree and finally a hash-&gt;block map to find nodes that are lower in the htree. If `dx_root.info.indirect_levels` is non-zero then the htree has that many levels and the blocks pointed to by the root node's map are interior nodes. These interior nodes have a zeroed out `struct ext4_dir_entry_2` followed by a hash-&gt;block map to find nodes of the next level. Leaf nodes look like classic linear directory blocks, but all of its entries have a hash value equal or greater than the indicated hash of the parent node.

The actual hash value for an entry name is only 31 bits, the least-significant bit is set to 0. However, if there is a hash collision between directory entries, the least-significant bit may get set to 1 on interior nodes in the case where these two (or more) hash-colliding entries do not fit into one leaf node and must be split across multiple nodes.

To look up a name in such a htree, the code calculates the hash of the desired file name and uses it to find the leaf node with the range of hash values the calculated hash falls into (in other words, a lookup works basically the same as it would in a B-Tree keyed by the hash value), and possibly also scanning the leaf nodes that follow (in tree order) in case of hash collisions.

To traverse the directory as a linear array (such as the old code does), the code simply reads every data block in the directory. The blocks used for the htree will appear to have no entries (aside from '.' and '..') and so only the leaf nodes will appear to have any interesting content.

The root of the htree is in `struct dx_root`, which is the full length of a data block:


<table>
<thead>
<tr>
<th>


Offset

</th>
<th>


Type

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


dot.inode

</td>
<td>


inode number of this directory.

</td>
</tr>
<tr>
<td>


0x4

</td>
<td>


\__le16

</td>
<td>


dot.rec_len

</td>
<td>


Length of this record, 12.

</td>
</tr>
<tr>
<td>


0x6

</td>
<td>


u8

</td>
<td>


dot.name_len

</td>
<td>


Length of the name, 1.

</td>
</tr>
<tr>
<td>


0x7

</td>
<td>


u8

</td>
<td>


dot.file_type

</td>
<td>


File type of this entry, 0x2 (directory) (if the feature flag is set).

</td>
</tr>
<tr>
<td>


0x8

</td>
<td>


char

</td>
<td>


dot.name\[4\]

</td>
<td>


“.000”

</td>
</tr>
<tr>
<td>


0xC

</td>
<td>


\__le32

</td>
<td>


dotdot.inode

</td>
<td>


inode number of parent directory.

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


dotdot.rec_len

</td>
<td>


block_size - 12. The record length is long enough to cover all htree data.

</td>
</tr>
<tr>
<td>


0x12

</td>
<td>


u8

</td>
<td>


dotdot.name_len

</td>
<td>


Length of the name, 2.

</td>
</tr>
<tr>
<td>


0x13

</td>
<td>


u8

</td>
<td>


dotdot.file_type

</td>
<td>


File type of this entry, 0x2 (directory) (if the feature flag is set).

</td>
</tr>
<tr>
<td>


0x14

</td>
<td>


char

</td>
<td>


dotdot_name\[4\]

</td>
<td>


“..00”

</td>
</tr>
<tr>
<td>


0x18

</td>
<td>


\__le32

</td>
<td>


struct dx_root_info.reserved_zero

</td>
<td>


Zero.

</td>
</tr>
<tr>
<td>


0x1C

</td>
<td>


u8

</td>
<td>


struct dx_root_info.hash_version

</td>
<td>


Hash type, see [dirhash](<#rst-dirhash>) table below.

</td>
</tr>
<tr>
<td>


0x1D

</td>
<td>


u8

</td>
<td>


struct dx_root_info.info_length

</td>
<td>


Length of the tree information, 0x8.

</td>
</tr>
<tr>
<td>


0x1E

</td>
<td>


u8

</td>
<td>


struct dx_root_info.indirect_levels

</td>
<td>


Depth of the htree. Cannot be larger than 3 if the INCOMPAT_LARGEDIR feature is set; cannot be larger than 2 otherwise.

</td>
</tr>
<tr>
<td>


0x1F

</td>
<td>


u8

</td>
<td>


struct dx_root_info.unused_flags

</td>
<td>




</td>
</tr>
<tr>
<td>


0x20

</td>
<td>


\__le16

</td>
<td>


limit

</td>
<td>


Maximum number of dx_entries that can follow this header, plus 1 for the header itself.

</td>
</tr>
<tr>
<td>


0x22

</td>
<td>


\__le16

</td>
<td>


count

</td>
<td>


Actual number of dx_entries that follow this header, plus 1 for the header itself.

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


block

</td>
<td>


The block number (within the directory file) that lead to the left-most leaf node, i.e. the leaf containing entries with the lowest hash values.

</td>
</tr>
<tr>
<td>


0x28

</td>
<td>


struct dx_entry

</td>
<td>


entries\[0\]

</td>
<td>


As many 8-byte `struct dx_entry` as fits in the rest of the data block.

</td>
</tr>
</tbody>
</table>

<a id="rst-dirhash"></a>

The directory hash is one of the following values:


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


0x0

</td>
<td>


Legacy.

</td>
</tr>
<tr>
<td>


0x1

</td>
<td>


Half MD4.

</td>
</tr>
<tr>
<td>


0x2

</td>
<td>


Tea.

</td>
</tr>
<tr>
<td>


0x3

</td>
<td>


Legacy, unsigned.

</td>
</tr>
<tr>
<td>


0x4

</td>
<td>


Half MD4, unsigned.

</td>
</tr>
<tr>
<td>


0x5

</td>
<td>


Tea, unsigned.

</td>
</tr>
<tr>
<td>


0x6

</td>
<td>


Siphash.

</td>
</tr>
</tbody>
</table>

Interior nodes of an htree are recorded as `struct dx_node`, which is also the full length of a data block:


<table>
<thead>
<tr>
<th>


Offset

</th>
<th>


Type

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


fake.inode

</td>
<td>


Zero, to make it look like this entry is not in use.

</td>
</tr>
<tr>
<td>


0x4

</td>
<td>


\__le16

</td>
<td>


fake.rec_len

</td>
<td>


The size of the block, in order to hide all of the dx_node data.

</td>
</tr>
<tr>
<td>


0x6

</td>
<td>


u8

</td>
<td>


name_len

</td>
<td>


Zero. There is no name for this “unused” directory entry.

</td>
</tr>
<tr>
<td>


0x7

</td>
<td>


u8

</td>
<td>


file_type

</td>
<td>


Zero. There is no file type for this “unused” directory entry.

</td>
</tr>
<tr>
<td>


0x8

</td>
<td>


\__le16

</td>
<td>


limit

</td>
<td>


Maximum number of dx_entries that can follow this header, plus 1 for the header itself.

</td>
</tr>
<tr>
<td>


0xA

</td>
<td>


\__le16

</td>
<td>


count

</td>
<td>


Actual number of dx_entries that follow this header, plus 1 for the header itself.

</td>
</tr>
<tr>
<td>


0xE

</td>
<td>


\__le32

</td>
<td>


block

</td>
<td>


The block number (within the directory file) that goes with the lowest hash value of this block. This value is stored in the parent block.

</td>
</tr>
<tr>
<td>


0x12

</td>
<td>


struct dx_entry

</td>
<td>


entries\[0\]

</td>
<td>


As many 8-byte `struct dx_entry` as fits in the rest of the data block.

</td>
</tr>
</tbody>
</table>

The hash maps that exist in both `struct dx_root` and `struct dx_node` are recorded as `struct dx_entry`, which is 8 bytes long:


<table>
<thead>
<tr>
<th>


Offset

</th>
<th>


Type

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


hash

</td>
<td>


Hash code.

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


block

</td>
<td>


Block number (within the directory file, not filesystem blocks) of the next node in the htree.

</td>
</tr>
</tbody>
</table>

(If you think this is all quite clever and peculiar, so does the author.)

If metadata checksums are enabled, the last 8 bytes of the directory block (precisely the length of one dx_entry) are used to store a `struct dx_tail`, which contains the checksum. The `limit` and `count` entries in the dx_root/dx_node structures are adjusted as necessary to fit the dx_tail into the block. If there is no space for the dx_tail, the user is notified to run e2fsck -D to rebuild the directory index (which will ensure that there's space for the checksum. The dx_tail structure is 8 bytes long and looks like this:


<table>
<thead>
<tr>
<th>


Offset

</th>
<th>


Type

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


u32

</td>
<td>


dt_reserved

</td>
<td>


Unused (but still part of the checksum curiously).

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


dt_checksum

</td>
<td>


Checksum of the htree directory block.

</td>
</tr>
</tbody>
</table>

The checksum is calculated against the FS UUID, the htree index header (dx_root or dx_node), all of the htree indices (dx_entry) that are in use, and the tail block (dx_tail) with the dt_checksum initially set to 0.
