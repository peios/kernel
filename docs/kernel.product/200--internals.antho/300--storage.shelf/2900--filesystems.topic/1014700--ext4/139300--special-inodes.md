---
title: "Special inodes"
type: reference
description: "ext4 reserves some inode for special features, as follows:"
---

<a id="rst-special-inodes"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

ext4 reserves some inode for special features, as follows:


<table>
<thead>
<tr>
<th>


inode Number

</th>
<th>


Purpose

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


0

</td>
<td>


Doesn't exist; there is no inode 0.

</td>
</tr>
<tr>
<td>


1

</td>
<td>


List of defective blocks.

</td>
</tr>
<tr>
<td>


2

</td>
<td>


Root directory.

</td>
</tr>
<tr>
<td>


3

</td>
<td>


User quota.

</td>
</tr>
<tr>
<td>


4

</td>
<td>


Group quota.

</td>
</tr>
<tr>
<td>


5

</td>
<td>


Boot loader.

</td>
</tr>
<tr>
<td>


6

</td>
<td>


Undelete directory.

</td>
</tr>
<tr>
<td>


7

</td>
<td>


Reserved group descriptors inode. (“resize inode”)

</td>
</tr>
<tr>
<td>


8

</td>
<td>


Journal inode.

</td>
</tr>
<tr>
<td>


9

</td>
<td>


The “exclude” inode, for snapshots(?)

</td>
</tr>
<tr>
<td>


10

</td>
<td>


Replica inode, used for some non-upstream feature?

</td>
</tr>
<tr>
<td>


11

</td>
<td>


Traditional first non-reserved inode. Usually this is the lost+found directory. See s_first_ino in the superblock.

</td>
</tr>
</tbody>
</table>

Note that there are also some inodes allocated from non-reserved inode numbers for other filesystem features which are not referenced from standard directory hierarchy. These are generally reference from the superblock. They are:


<table>
<thead>
<tr>
<th>


Superblock field

</th>
<th>


Description

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


s_lpf_ino

</td>
<td>


Inode number of lost+found directory.

</td>
</tr>
<tr>
<td>


s_prj_quota_inum

</td>
<td>


Inode number of quota file tracking project quotas

</td>
</tr>
<tr>
<td>


s_orphan_file_inum

</td>
<td>


Inode number of file tracking orphan inodes.

</td>
</tr>
</tbody>
</table>
