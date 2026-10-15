---
title: "Filesystems in the Linux kernel"
type: reference
description: "This under-development manual will, some glorious day, provide comprehensive information on how the Linux virtual filesystem (VFS) layer works, along with the filesystems that sit below it. For now, what we have can be found below."
---

<a id="rst-filesystems-in-the-linux-kernel"></a>
<a id="rst-filesystems-index"></a>

This under-development manual will, some glorious day, provide comprehensive information on how the Linux virtual filesystem (VFS) layer works, along with the filesystems that sit below it.  For now, what we have can be found below.

<a id="rst-core-vfs-documentation"></a>

## Core VFS documentation

See these manuals for documentation about the VFS layer itself and how its algorithms work.

- [Overview of the Linux Virtual File System](<~kernel/internals/filesystems/vfs>)
- [Pathname lookup](<~kernel/internals/filesystems/path-lookup>)
- [Linux Filesystems API summary](<~kernel/internals/filesystems/api-summary>)
- [splice and pipes](<~kernel/internals/filesystems/splice>)
- [Locking](<~kernel/internals/filesystems/locking>)
- [Directory Locking](<~kernel/internals/filesystems/directory-locking>)
- [The Devpts Filesystem](<~kernel/internals/filesystems/devpts>)
- [Linux Directory Notification](<~kernel/internals/filesystems/dnotify>)
- [Fiemap Ioctl](<~kernel/internals/filesystems/fiemap>)
- [File management in the Linux kernel](<~kernel/internals/filesystems/files>)
- [File Locking Release Notes](<~kernel/internals/filesystems/locks>)
- [Multigrain Timestamps](<~kernel/internals/filesystems/multigrain-ts>)
- [Filesystem Mount API](<~kernel/internals/filesystems/mount-api>)
- [Quota subsystem](<~kernel/internals/filesystems/quota>)
- [The seq_file Interface](<~kernel/internals/filesystems/seq-file>)
- [Shared Subtrees](<~kernel/internals/filesystems/sharedsubtree>)
- [Idmappings](<~kernel/internals/filesystems/idmappings>)
- [VFS iomap Documentation](<~kernel/internals/filesystems/iomap/index>)
- [Automount Support](<~kernel/internals/filesystems/automount-support>)
- [Filesystem Caching](<~kernel/internals/filesystems/caching/index>)
- [Changes since 2.5.0:](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/filesystems/porting.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)

<a id="rst-filesystem-support-layers"></a>

## Filesystem support layers

Documentation for the support code within the filesystem layer for use in filesystem implementations.

- [Buffer Heads](<~kernel/internals/filesystems/buffer>)
- [The Linux Journalling API](<~kernel/internals/filesystems/journalling>)
- [Filesystem-level encryption (fscrypt)](<~kernel/internals/filesystems/fscrypt>)
- [fs-verity: read-only file-based authenticity protection](<~kernel/internals/filesystems/fsverity>)
- [Network Filesystem Services Library](<~kernel/internals/filesystems/netfs-library>)

<a id="rst-filesystems"></a>

## Filesystems

Documentation for filesystem implementations.

- [v9fs: Plan 9 Resource Sharing for Linux](<~kernel/internals/filesystems/9p>)
- [Acorn Disc Filing System - ADFS](<~kernel/internals/filesystems/adfs>)
- [Overview of Amiga Filesystems](<~kernel/internals/filesystems/affs>)
- [kAFS: AFS FILESYSTEM](<~kernel/internals/filesystems/afs>)
- [autofs - how it works](<~kernel/internals/filesystems/autofs>)
- [Miscellaneous Device control operations for the autofs kernel module](<~kernel/internals/filesystems/autofs-mount-control>)
- [BeOS filesystem for Linux](<~kernel/internals/filesystems/befs>)
- [BFS Filesystem for Linux](<~kernel/internals/filesystems/bfs>)
- [BTRFS](<~kernel/internals/filesystems/btrfs>)
- [Ceph Distributed File System](<~kernel/internals/filesystems/ceph>)
- [Coda Kernel-Venus Interface](<~kernel/internals/filesystems/coda>)
- [Configfs - Userspace-driven Kernel Object Configuration](<~kernel/internals/filesystems/configfs>)
- [Cramfs - cram a filesystem onto a small ROM](<~kernel/internals/filesystems/cramfs>)
- [Direct Access for files](<~kernel/internals/filesystems/dax>)
- [DebugFS](<~kernel/internals/filesystems/debugfs>)
- [DLMFS](<~kernel/internals/filesystems/dlmfs>)
- [eCryptfs: A stacked cryptographic filesystem for Linux](<~kernel/internals/filesystems/ecryptfs>)
- [efivarfs - a (U)EFI variable filesystem](<~kernel/internals/filesystems/efivarfs>)
- [EROFS - Enhanced Read-Only File System](<~kernel/internals/filesystems/erofs>)
- [The Second Extended Filesystem](<~kernel/internals/filesystems/ext2>)
- [Ext3 Filesystem](<~kernel/internals/filesystems/ext3>)
- [ext4 Data Structures and Algorithms](<~kernel/internals/filesystems/ext4/index>)
- [Flash-Friendly File System (F2FS)](<~kernel/internals/filesystems/f2fs>)
- [Global File System 2](<~kernel/internals/filesystems/gfs2/index>)
- [Macintosh HFS Filesystem for Linux](<~kernel/internals/filesystems/hfs>)
- [Macintosh HFSPlus Filesystem for Linux](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/filesystems/hfsplus.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)
- [Read/Write HPFS 2.09](<~kernel/internals/filesystems/hpfs>)
- [FUSE (Filesystem in Userspace) Technical Documentation](<~kernel/internals/filesystems/fuse/index>)
- [Inotify - A Powerful yet Simple File Change Notification System](<~kernel/internals/filesystems/inotify>)
- [ISO9660 Filesystem](<~kernel/internals/filesystems/isofs>)
- [NILFS2](<~kernel/internals/filesystems/nilfs2>)
- [NFS](<~kernel/internals/filesystems/nfs/index>)
- [NTFS3](<~kernel/internals/filesystems/ntfs3>)
- [OCFS2 filesystem](<~kernel/internals/filesystems/ocfs2>)
- [OCFS2 file system - online file check](<~kernel/internals/filesystems/ocfs2-online-filecheck>)
- [Optimized MPEG Filesystem (OMFS)](<~kernel/internals/filesystems/omfs>)
- [ORANGEFS](<~kernel/internals/filesystems/orangefs>)
- [Overlay Filesystem](<~kernel/internals/filesystems/overlayfs>)
- [The /proc Filesystem](<~kernel/internals/filesystems/proc>)
- [The QNX6 Filesystem](<~kernel/internals/filesystems/qnx6>)
- [Ramfs, rootfs and initramfs](<~kernel/internals/filesystems/ramfs-rootfs-initramfs>)
- [relay interface (formerly relayfs)](<~kernel/internals/filesystems/relay>)
- [User Interface for Resource Control feature (resctrl)](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/filesystems/resctrl.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)
- [ROMFS - ROM File System](<~kernel/internals/filesystems/romfs>)
- [CIFS](<~kernel/internals/filesystems/smb/index>)
- [SPU Filesystem](<~kernel/internals/filesystems/spufs/index>)
- [Squashfs 4.0 Filesystem](<~kernel/internals/filesystems/squashfs>)
- [sysfs - \_The\_ filesystem for exporting kernel objects](<~kernel/internals/filesystems/sysfs>)
- [Tmpfs](<~kernel/internals/filesystems/tmpfs>)
- [UBI File System](<~kernel/internals/filesystems/ubifs>)
- [UBIFS Authentication Support](<~kernel/internals/filesystems/ubifs-authentication>)
- [UDF file system](<~kernel/internals/filesystems/udf>)
- [virtiofs: virtio-fs host&lt;-&gt;guest shared file system](<~kernel/internals/filesystems/virtiofs>)
- [VFAT](<~kernel/internals/filesystems/vfat>)
- [XFS Filesystem Documentation](<~kernel/internals/filesystems/xfs/index>)
- [ZoneFS - Zone filesystem for Zoned block devices](<~kernel/internals/filesystems/zonefs>)
