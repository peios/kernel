---
title: "Extended Attributes"
type: reference
description: "Extended attributes (xattrs) are typically stored in a separate data block on the disk and referenced from inodes via inode.i_file_acl*. The first use of extended attributes seems to have been for storing file ACLs and other security data…"
---

<a id="rst-extended-attributes"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

Extended attributes (xattrs) are typically stored in a separate data block on the disk and referenced from inodes via `inode.i_file_acl*`. The first use of extended attributes seems to have been for storing file ACLs and other security data (selinux). With the `user_xattr` mount option it is possible for users to store extended attributes so long as all attribute names begin with “user”; this restriction seems to have disappeared as of Linux 3.0.

There are two places where extended attributes can be found. The first place is between the end of each inode entry and the beginning of the next inode entry. For example, if inode.i_extra_isize = 28 and sb.inode_size = 256, then there are 256 - (128 + 28) = 100 bytes available for in-inode extended attribute storage. The second place where extended attributes can be found is in the block pointed to by `inode.i_file_acl`. As of Linux 3.11, it is not possible for this block to contain a pointer to a second extended attribute block (or even the remaining blocks of a cluster). In theory it is possible for each attribute's value to be stored in a separate data block, though as of Linux 3.11 the code does not permit this.

Keys are generally assumed to be ASCIIZ strings, whereas values can be strings or binary data.

Extended attributes, when stored after the inode, have a header `ext4_xattr_ibody_header` that is 4 bytes long:


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


h_magic

</td>
<td>


Magic number for identification, 0xEA020000. This value is set by the Linux driver, though e2fsprogs doesn't seem to check it(?)

</td>
</tr>
</tbody>
</table>

The beginning of an extended attribute block is in `struct ext4_xattr_header`, which is 32 bytes long:


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


h_magic

</td>
<td>


Magic number for identification, 0xEA020000.

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


h_refcount

</td>
<td>


Reference count.

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


h_blocks

</td>
<td>


Number of disk blocks used.

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


h_hash

</td>
<td>


Hash value of all attributes.

</td>
</tr>
<tr>
<td>


0x10

</td>
<td>


\__le32

</td>
<td>


h_checksum

</td>
<td>


Checksum of the extended attribute block.

</td>
</tr>
<tr>
<td>


0x14

</td>
<td>


\__u32

</td>
<td>


h_reserved\[3\]

</td>
<td>


Zero.

</td>
</tr>
</tbody>
</table>

The checksum is calculated against the FS UUID, the 64-bit block number of the extended attribute block, and the entire block (header + entries).

Following the `struct ext4_xattr_header` or `struct ext4_xattr_ibody_header` is an array of `struct ext4_xattr_entry`; each of these entries is at least 16 bytes long. When stored in an external block, the `struct ext4_xattr_entry` entries must be stored in sorted order. The sort order is `e_name_index`, then `e_name_len`, and finally `e_name`. Attributes stored inside an inode do not need be stored in sorted order.


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


\__u8

</td>
<td>


e_name_len

</td>
<td>


Length of name.

</td>
</tr>
<tr>
<td>


0x1

</td>
<td>


\__u8

</td>
<td>


e_name_index

</td>
<td>


Attribute name index. There is a discussion of this below.

</td>
</tr>
<tr>
<td>


0x2

</td>
<td>


\__le16

</td>
<td>


e_value_offs

</td>
<td>


Location of this attribute's value on the disk block where it is stored. Multiple attributes can share the same value. For an inode attribute this value is relative to the start of the first entry; for a block this value is relative to the start of the block (i.e. the header).

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


e_value_inum

</td>
<td>


The inode where the value is stored. Zero indicates the value is in the same block as this entry. This field is only used if the INCOMPAT_EA_INODE feature is enabled.

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


e_value_size

</td>
<td>


Length of attribute value.

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


e_hash

</td>
<td>


Hash value of attribute name and attribute value. The kernel doesn't update the hash for in-inode attributes, so for that case this value must be zero, because e2fsck validates any non-zero hash regardless of where the xattr lives.

</td>
</tr>
<tr>
<td>


0x10

</td>
<td>


char

</td>
<td>


e_name\[e_name_len\]

</td>
<td>


Attribute name. Does not include trailing NULL.

</td>
</tr>
</tbody>
</table>

Attribute values can follow the end of the entry table. There appears to be a requirement that they be aligned to 4-byte boundaries. The values are stored starting at the end of the block and grow towards the xattr_header/xattr_entry table. When the two collide, the overflow is put into a separate disk block. If the disk block fills up, the filesystem returns -ENOSPC.

The first four fields of the `ext4_xattr_entry` are set to zero to mark the end of the key list.

<a id="rst-attribute-name-indices"></a>

## Attribute Name Indices

Logically speaking, extended attributes are a series of key=value pairs. The keys are assumed to be NULL-terminated strings. To reduce the amount of on-disk space that the keys consume, the beginning of the key string is matched against the attribute name index. If a match is found, the attribute name index field is set, and matching string is removed from the key name. Here is a map of name index values to key prefixes:


<table>
<thead>
<tr>
<th>


Name Index

</th>
<th>


Key Prefix

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


0

</td>
<td>


(no prefix)

</td>
</tr>
<tr>
<td>


1

</td>
<td>


“user.”

</td>
</tr>
<tr>
<td>


2

</td>
<td>


“system.posix_acl_access”

</td>
</tr>
<tr>
<td>


3

</td>
<td>


“system.posix_acl_default”

</td>
</tr>
<tr>
<td>


4

</td>
<td>


“trusted.”

</td>
</tr>
<tr>
<td>


6

</td>
<td>


“security.”

</td>
</tr>
<tr>
<td>


7

</td>
<td>


“system.” (inline_data only?)

</td>
</tr>
<tr>
<td>


8

</td>
<td>


“system.richacl” (SuSE kernels only?)

</td>
</tr>
</tbody>
</table>

For example, if the attribute key is “user.fubar”, the attribute name index is set to 1 and the “fubar” name is recorded on disk.

<a id="rst-posix-acls"></a>

## POSIX ACLs

POSIX ACLs are stored in a reduced version of the Linux kernel (and libacl's) internal ACL format. The key difference is that the version number is different (1) and the `e_id` field is only stored for named user and group ACLs.
