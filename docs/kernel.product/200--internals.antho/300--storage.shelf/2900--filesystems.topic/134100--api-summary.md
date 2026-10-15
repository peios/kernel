---
title: "Linux Filesystems API summary"
type: reference
description: "This section contains API-level documentation, mostly taken from the source code itself."
---

<a id="rst-linux-filesystems-api-summary"></a>

This section contains API-level documentation, mostly taken from the source code itself.

<a id="rst-the-linux-vfs"></a>

## The Linux VFS

<a id="rst-the-filesystem-types"></a>

### The Filesystem types

```{kernel-doc} include/linux/fs.h
:internal:
```

<a id="rst-the-directory-cache"></a>

### The Directory Cache

```{kernel-doc} fs/dcache.c
:export:
```

```{kernel-doc} include/linux/dcache.h
:internal:
```

<a id="rst-inode-handling"></a>

### Inode Handling

```{kernel-doc} fs/inode.c
:export:
```

```{kernel-doc} fs/bad_inode.c
:export:
```

<a id="rst-registration-and-superblocks"></a>

### Registration and Superblocks

```{kernel-doc} fs/super.c
:export:
```

<a id="rst-file-locks"></a>

### File Locks

```{kernel-doc} fs/locks.c
:export:
```

```{kernel-doc} fs/locks.c
:internal:
```

<a id="rst-other-functions"></a>

### Other Functions

```{kernel-doc} fs/mpage.c
:export:
```

```{kernel-doc} fs/namei.c
:export:
```

```{kernel-doc} fs/open.c
:export:
```

```{kernel-doc} block/bio.c
:export:
```

```{kernel-doc} fs/seq_file.c
:export:
```

```{kernel-doc} fs/filesystems.c
:export:
```

```{kernel-doc} fs/fs-writeback.c
:export:
```

```{kernel-doc} fs/anon_inodes.c
:export:
```

```{kernel-doc} fs/attr.c
:export:
```

```{kernel-doc} fs/d_path.c
:export:
```

```{kernel-doc} fs/dax.c
:export:
```

```{kernel-doc} fs/libfs.c
:export:
```

```{kernel-doc} fs/posix_acl.c
:export:
```

```{kernel-doc} fs/stat.c
:export:
```

```{kernel-doc} fs/sync.c
:export:
```

```{kernel-doc} fs/xattr.c
:export:
```

```{kernel-doc} fs/namespace.c
:export:
```

<a id="rst-the-proc-filesystem"></a>

## The proc filesystem

<a id="rst-sysctl-interface"></a>

### sysctl interface

```{kernel-doc} kernel/sysctl.c
:export:
```

<a id="rst-proc-filesystem-interface"></a>

### proc filesystem interface

```{kernel-doc} fs/proc/base.c
:internal:
```

<a id="rst-events-based-on-file-descriptors"></a>

## Events based on file descriptors

```{kernel-doc} fs/eventfd.c
:export:
```

<a id="rst-eventpoll-epoll-interfaces"></a>

## eventpoll (epoll) interfaces

```{kernel-doc} fs/eventpoll.c
:internal:
```

<a id="rst-the-filesystem-for-exporting-kernel-objects"></a>

## The Filesystem for Exporting Kernel Objects

```{kernel-doc} fs/sysfs/file.c
:export:
```

```{kernel-doc} fs/sysfs/symlink.c
:export:
```

<a id="rst-the-debugfs-filesystem"></a>

## The debugfs filesystem

<a id="rst-debugfs-interface"></a>

### debugfs interface

```{kernel-doc} fs/debugfs/inode.c
:export:
```

```{kernel-doc} fs/debugfs/file.c
:export:
```
