---
title: "Inode Table"
type: reference
description: "Inode tables are statically allocated at mkfs time. Each block group descriptor points to the start of the table, and the superblock records the number of inodes per group. See inode documentation <inodes> for more information on inode…"
---

<a id="rst-inode-table"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

Inode tables are statically allocated at mkfs time.  Each block group descriptor points to the start of the table, and the superblock records the number of inodes per group.  See [inode documentation](<~kernel/internals/filesystems/ext4/inodes>) for more information on inode table layout.
