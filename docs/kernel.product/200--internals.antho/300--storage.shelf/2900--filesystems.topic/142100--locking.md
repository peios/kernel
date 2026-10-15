---
title: "Locking"
type: reference
description: "The text below describes the locking rules for VFS-related methods. It is (believed to be) up-to-date. Please, if you change anything in prototypes or locking protocols - update this file. And update the relevant instances in the tree,…"
---

> **Peios:** The VFS also has Peios `validate_mountpoint` and `getlease` callbacks. See the [VFS reference](<~kernel/internals/filesystems/vfs>) for their contracts. Layered lease queries must preserve the outer `lease_file` identity when forwarding to a backing file.


<a id="rst-locking"></a>

The text below describes the locking rules for VFS-related methods. It is (believed to be) up-to-date. *Please*, if you change anything in prototypes or locking protocols - update this file. And update the relevant instances in the tree, don't leave that to maintainers of filesystems/devices/ etc. At the very least, put the list of dubious cases in the end of this file. Don't turn it into log - maintainers of out-of-the-tree code are supposed to be able to use diff(1).

Thing currently missing here: socket operations. Alexey?

<a id="rst-dentry-operations"></a>

## dentry_operations

prototypes:



```text
int (*d_revalidate)(struct inode *, const struct qstr *,
                    struct dentry *, unsigned int);
int (*d_weak_revalidate)(struct dentry *, unsigned int);
int (*d_hash)(const struct dentry *, struct qstr *);
int (*d_compare)(const struct dentry *,
                unsigned int, const char *, const struct qstr *);
int (*d_delete)(struct dentry *);
int (*d_init)(struct dentry *);
void (*d_release)(struct dentry *);
void (*d_iput)(struct dentry *, struct inode *);
char *(*d_dname)((struct dentry *dentry, char *buffer, int buflen);
struct vfsmount *(*d_automount)(struct path *path);
int (*d_manage)(const struct path *, bool);
struct dentry *(*d_real)(struct dentry *, enum d_real_type type);
bool (*d_unalias_trylock)(const struct dentry *);
void (*d_unalias_unlock)(const struct dentry *);
```

locking rules:


<table>
<thead>
<tr>
<th>


ops

</th>
<th>


rename_lock

</th>
<th>


-&gt;d_lock

</th>
<th>


may block

</th>
<th>


rcu-walk

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


d_revalidate:

</td>
<td>


no

</td>
<td>


no

</td>
<td>


yes (ref-walk)

</td>
<td>


maybe

</td>
</tr>
<tr>
<td>


d_weak_revalidate:

</td>
<td>


no

</td>
<td>


no

</td>
<td>


yes

</td>
<td>


no

</td>
</tr>
<tr>
<td>


d_hash

</td>
<td>


no

</td>
<td>


no

</td>
<td>


no

</td>
<td>


maybe

</td>
</tr>
<tr>
<td>


d_compare:

</td>
<td>


yes

</td>
<td>


no

</td>
<td>


no

</td>
<td>


maybe

</td>
</tr>
<tr>
<td>


d_delete:

</td>
<td>


no

</td>
<td>


yes

</td>
<td>


no

</td>
<td>


no

</td>
</tr>
<tr>
<td>


d_init:

</td>
<td>


no

</td>
<td>


no

</td>
<td>


yes

</td>
<td>


no

</td>
</tr>
<tr>
<td>


d_release:

</td>
<td>


no

</td>
<td>


no

</td>
<td>


yes

</td>
<td>


no

</td>
</tr>
<tr>
<td>


d_prune:

</td>
<td>


no

</td>
<td>


yes

</td>
<td>


no

</td>
<td>


no

</td>
</tr>
<tr>
<td>


d_iput:

</td>
<td>


no

</td>
<td>


no

</td>
<td>


yes

</td>
<td>


no

</td>
</tr>
<tr>
<td>


d_dname:

</td>
<td>


no

</td>
<td>


no

</td>
<td>


no

</td>
<td>


no

</td>
</tr>
<tr>
<td>


d_automount:

</td>
<td>


no

</td>
<td>


no

</td>
<td>


yes

</td>
<td>


no

</td>
</tr>
<tr>
<td>


d_manage:

</td>
<td>


no

</td>
<td>


no

</td>
<td>


yes (ref-walk)

</td>
<td>


maybe

</td>
</tr>
<tr>
<td>


d_real

</td>
<td>


no

</td>
<td>


no

</td>
<td>


yes

</td>
<td>


no

</td>
</tr>
<tr>
<td>


d_unalias_trylock

</td>
<td>


yes

</td>
<td>


no

</td>
<td>


no

</td>
<td>


no

</td>
</tr>
<tr>
<td>


d_unalias_unlock

</td>
<td>


yes

</td>
<td>


no

</td>
<td>


no

</td>
<td>


no

</td>
</tr>
</tbody>
</table>

<a id="rst-inode-operations"></a>

## inode_operations

prototypes:



```text
int (*create) (struct mnt_idmap *, struct inode *,struct dentry *,umode_t, bool);
struct dentry * (*lookup) (struct inode *,struct dentry *, unsigned int);
int (*link) (struct dentry *,struct inode *,struct dentry *);
int (*unlink) (struct inode *,struct dentry *);
int (*symlink) (struct mnt_idmap *, struct inode *,struct dentry *,const char *);
struct dentry *(*mkdir) (struct mnt_idmap *, struct inode *,struct dentry *,umode_t);
int (*rmdir) (struct inode *,struct dentry *);
int (*mknod) (struct mnt_idmap *, struct inode *,struct dentry *,umode_t,dev_t);
int (*rename) (struct mnt_idmap *, struct inode *, struct dentry *,
                struct inode *, struct dentry *, unsigned int);
int (*readlink) (struct dentry *, char __user *,int);
const char *(*get_link) (struct dentry *, struct inode *, struct delayed_call *);
void (*truncate) (struct inode *);
int (*permission) (struct mnt_idmap *, struct inode *, int, unsigned int);
struct posix_acl * (*get_inode_acl)(struct inode *, int, bool);
int (*setattr) (struct mnt_idmap *, struct dentry *, struct iattr *);
int (*getattr) (struct mnt_idmap *, const struct path *, struct kstat *, u32, unsigned int);
ssize_t (*listxattr) (struct dentry *, char *, size_t);
int (*fiemap)(struct inode *, struct fiemap_extent_info *, u64 start, u64 len);
void (*update_time)(struct inode *inode, enum fs_update_time type,
                    int flags);
void (*sync_lazytime)(struct inode *inode);
int (*atomic_open)(struct inode *, struct dentry *,
                        struct file *, unsigned open_flag,
                        umode_t create_mode);
int (*tmpfile) (struct mnt_idmap *, struct inode *,
                struct file *, umode_t);
int (*fileattr_set)(struct mnt_idmap *idmap,
                    struct dentry *dentry, struct file_kattr *fa);
int (*fileattr_get)(struct dentry *dentry, struct file_kattr *fa);
struct posix_acl * (*get_acl)(struct mnt_idmap *, struct dentry *, int);
struct offset_ctx *(*get_offset_ctx)(struct inode *inode);
```

- **locking rules:**

  all may block


<table>
<thead>
<tr>
<th>


ops

</th>
<th>


i_rwsem(inode)

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


lookup:

</td>
<td>


shared

</td>
</tr>
<tr>
<td>


create:

</td>
<td>


exclusive

</td>
</tr>
<tr>
<td>


link:

</td>
<td>


exclusive (both)

</td>
</tr>
<tr>
<td>


mknod:

</td>
<td>


exclusive

</td>
</tr>
<tr>
<td>


symlink:

</td>
<td>


exclusive

</td>
</tr>
<tr>
<td>


mkdir:

</td>
<td>


exclusive

</td>
</tr>
<tr>
<td>


unlink:

</td>
<td>


exclusive (both)

</td>
</tr>
<tr>
<td>


rmdir:

</td>
<td>


exclusive (both)(see below)

</td>
</tr>
<tr>
<td>


rename:

</td>
<td>


exclusive (both parents, some children) (see below)

</td>
</tr>
<tr>
<td>


readlink:

</td>
<td>


no

</td>
</tr>
<tr>
<td>


get_link:

</td>
<td>


no

</td>
</tr>
<tr>
<td>


setattr:

</td>
<td>


exclusive

</td>
</tr>
<tr>
<td>


permission:

</td>
<td>


no (may not block if called in rcu-walk mode)

</td>
</tr>
<tr>
<td>


get_inode_acl:

</td>
<td>


no

</td>
</tr>
<tr>
<td>


get_acl:

</td>
<td>


no

</td>
</tr>
<tr>
<td>


getattr:

</td>
<td>


no

</td>
</tr>
<tr>
<td>


listxattr:

</td>
<td>


no

</td>
</tr>
<tr>
<td>


fiemap:

</td>
<td>


no

</td>
</tr>
<tr>
<td>


update_time:

</td>
<td>


no

</td>
</tr>
<tr>
<td>


sync_lazytime:

</td>
<td>


no

</td>
</tr>
<tr>
<td>


atomic_open:

</td>
<td>


shared (exclusive if O_CREAT is set in open flags)

</td>
</tr>
<tr>
<td>


tmpfile:

</td>
<td>


no

</td>
</tr>
<tr>
<td>


fileattr_get:

</td>
<td>


no or exclusive

</td>
</tr>
<tr>
<td>


fileattr_set:

</td>
<td>


exclusive

</td>
</tr>
<tr>
<td>


get_offset_ctx

</td>
<td>


no

</td>
</tr>
</tbody>
</table>

> Additionally, -&gt;rmdir(), -&gt;unlink() and -&gt;rename() have -&gt;i_rwsem exclusive on victim. cross-directory -&gt;rename() has (per-superblock) -&gt;s_vfs_rename_sem. -&gt;unlink() and -&gt;rename() have -&gt;i_rwsem exclusive on all non-directories involved. -&gt;rename() has -&gt;i_rwsem exclusive on any subdirectory that changes parent.

See [Documentation/filesystems/directory-locking.rst](~kernel/internals/filesystems/directory-locking) for more detailed discussion of the locking scheme for directory operations.

<a id="rst-xattr-handler-operations"></a>

## xattr_handler operations

prototypes:



```text
bool (*list)(struct dentry *dentry);
int (*get)(const struct xattr_handler *handler, struct dentry *dentry,
           struct inode *inode, const char *name, void *buffer,
           size_t size);
int (*set)(const struct xattr_handler *handler,
           struct mnt_idmap *idmap,
           struct dentry *dentry, struct inode *inode, const char *name,
           const void *buffer, size_t size, int flags);
```

- **locking rules:**

  all may block


<table>
<thead>
<tr>
<th>


ops

</th>
<th>


i_rwsem(inode)

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


list:

</td>
<td>


no

</td>
</tr>
<tr>
<td>


get:

</td>
<td>


no

</td>
</tr>
<tr>
<td>


set:

</td>
<td>


exclusive

</td>
</tr>
</tbody>
</table>

<a id="rst-super-operations"></a>

## super_operations

prototypes:



```text
struct inode *(*alloc_inode)(struct super_block *sb);
void (*free_inode)(struct inode *);
void (*destroy_inode)(struct inode *);
void (*dirty_inode) (struct inode *, int flags);
int (*write_inode) (struct inode *, struct writeback_control *wbc);
int (*drop_inode) (struct inode *);
void (*evict_inode) (struct inode *);
void (*put_super) (struct super_block *);
int (*sync_fs)(struct super_block *sb, int wait);
int (*freeze_fs) (struct super_block *);
int (*unfreeze_fs) (struct super_block *);
int (*statfs) (struct dentry *, struct kstatfs *);
void (*umount_begin) (struct super_block *);
int (*show_options)(struct seq_file *, struct dentry *);
ssize_t (*quota_read)(struct super_block *, int, char *, size_t, loff_t);
ssize_t (*quota_write)(struct super_block *, int, const char *, size_t, loff_t);
```

- **locking rules:**

  All may block \[not true, see below\]


<table>
<thead>
<tr>
<th>


ops

</th>
<th>


s_umount

</th>
<th>


note

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


alloc_inode:

</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


free_inode:

</td>
<td>




</td>
<td>


called from RCU callback

</td>
</tr>
<tr>
<td>


destroy_inode:

</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


dirty_inode:

</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


write_inode:

</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


drop_inode:

</td>
<td>




</td>
<td>


\!\!\!inode-&gt;i_lock\!\!\!

</td>
</tr>
<tr>
<td>


evict_inode:

</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


put_super:

</td>
<td>


write

</td>
<td>




</td>
</tr>
<tr>
<td>


sync_fs:

</td>
<td>


read

</td>
<td>




</td>
</tr>
<tr>
<td>


freeze_fs:

</td>
<td>


write

</td>
<td>




</td>
</tr>
<tr>
<td>


unfreeze_fs:

</td>
<td>


write

</td>
<td>




</td>
</tr>
<tr>
<td>


statfs:

</td>
<td>


maybe(read)

</td>
<td>


(see below)

</td>
</tr>
<tr>
<td>


umount_begin:

</td>
<td>


no

</td>
<td>




</td>
</tr>
<tr>
<td>


show_options:

</td>
<td>


no

</td>
<td>


(namespace_sem)

</td>
</tr>
<tr>
<td>


quota_read:

</td>
<td>


no

</td>
<td>


(see below)

</td>
</tr>
<tr>
<td>


quota_write:

</td>
<td>


no

</td>
<td>


(see below)

</td>
</tr>
</tbody>
</table>

-&gt;statfs() has s_umount (shared) when called by ustat(2) (native or compat), but that's an accident of bad API; s_umount is used to pin the superblock down when we only have dev_t given us by userland to identify the superblock.  Everything else (statfs(), fstatfs(), etc.) doesn't hold it when calling -&gt;statfs() - superblock is pinned down by resolving the pathname passed to syscall.

-&gt;quota_read() and -&gt;quota_write() functions are both guaranteed to be the only ones operating on the quota file by the quota code (via dqio_sem) (unless an admin really wants to screw up something and writes to quota files with quotas on). For other details about locking see also dquot_operations section.

<a id="rst-file-system-type"></a>

## file_system_type

prototypes:



```text
void (*kill_sb) (struct super_block *);
```

locking rules:


<table>
<thead>
<tr>
<th>


ops

</th>
<th>


may block

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


kill_sb

</td>
<td>


yes

</td>
</tr>
</tbody>
</table>

-&gt;kill_sb() takes a write-locked superblock, does all shutdown work on it, unlocks and drops the reference.

<a id="rst-address-space-operations"></a>

## address_space_operations

prototypes:



```text
int (*read_folio)(struct file *, struct folio *);
int (*writepages)(struct address_space *, struct writeback_control *);
bool (*dirty_folio)(struct address_space *, struct folio *folio);
void (*readahead)(struct readahead_control *);
int (*write_begin)(const struct kiocb *, struct address_space *mapping,
                        loff_t pos, unsigned len,
                        struct folio **foliop, void **fsdata);
int (*write_end)(const struct kiocb *, struct address_space *mapping,
                        loff_t pos, unsigned len, unsigned copied,
                        struct folio *folio, void *fsdata);
sector_t (*bmap)(struct address_space *, sector_t);
void (*invalidate_folio) (struct folio *, size_t start, size_t len);
bool (*release_folio)(struct folio *, gfp_t);
void (*free_folio)(struct folio *);
int (*direct_IO)(struct kiocb *, struct iov_iter *iter);
int (*migrate_folio)(struct address_space *, struct folio *dst,
                struct folio *src, enum migrate_mode);
int (*launder_folio)(struct folio *);
bool (*is_partially_uptodate)(struct folio *, size_t from, size_t count);
int (*error_remove_folio)(struct address_space *, struct folio *);
int (*swap_activate)(struct swap_info_struct *sis, struct file *f, sector_t *span)
int (*swap_deactivate)(struct file *);
int (*swap_rw)(struct kiocb *iocb, struct iov_iter *iter);
```

- **locking rules:**

  All except dirty_folio and free_folio may block


<table>
<thead>
<tr>
<th>


ops

</th>
<th>


folio locked

</th>
<th>


i_rwsem

</th>
<th>


invalidate_lock

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


read_folio:

</td>
<td>


yes, unlocks

</td>
<td>




</td>
<td>


shared

</td>
</tr>
<tr>
<td>


writepages:

</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


dirty_folio:

</td>
<td>


maybe

</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


readahead:

</td>
<td>


yes, unlocks

</td>
<td>




</td>
<td>


shared

</td>
</tr>
<tr>
<td>


write_begin:

</td>
<td>


locks the folio

</td>
<td>


exclusive

</td>
<td>




</td>
</tr>
<tr>
<td>


write_end:

</td>
<td>


yes, unlocks

</td>
<td>


exclusive

</td>
<td>




</td>
</tr>
<tr>
<td>


bmap:

</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


invalidate_folio:

</td>
<td>


yes

</td>
<td>




</td>
<td>


exclusive

</td>
</tr>
<tr>
<td>


release_folio:

</td>
<td>


yes

</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


free_folio:

</td>
<td>


yes

</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


direct_IO:

</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


migrate_folio:

</td>
<td>


yes (both)

</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


launder_folio:

</td>
<td>


yes

</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


is_partially_uptodate:

</td>
<td>


yes

</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


error_remove_folio:

</td>
<td>


yes

</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


swap_activate:

</td>
<td>


no

</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


swap_deactivate:

</td>
<td>


no

</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


swap_rw:

</td>
<td>


yes, unlocks

</td>
<td>




</td>
<td>




</td>
</tr>
</tbody>
</table>

-&gt;write_begin(), -&gt;write_end() and -&gt;read_folio() may be called from the request handler (/dev/loop).

-&gt;read_folio() unlocks the folio, either synchronously or via I/O completion.

-&gt;readahead() unlocks the folios that I/O is attempted on like -&gt;read_folio().

-&gt;writepages() is used for periodic writeback and for syscall-initiated sync operations.  The address_space should start I/O against at least `*nr_to_write` pages.  `*nr_to_write` must be decremented for each page which is written.  The address_space implementation may write more (or less) pages than `*nr_to_write` asks for, but it should try to be reasonably close. If nr_to_write is NULL, all dirty pages must be written.

writepages should \_only\_ write pages which are present in mapping-&gt;i_pages.

-&gt;dirty_folio() is called from various places in the kernel when the target folio is marked as needing writeback.  The folio cannot be truncated because either the caller holds the folio lock, or the caller has found the folio while holding the page table lock which will block truncation.

-&gt;bmap() is currently used by legacy ioctl() (FIBMAP) provided by some filesystems and by the swapper. The latter will eventually go away.  Please, keep it that way and don't breed new callers.

-&gt;invalidate_folio() is called when the filesystem must attempt to drop some or all of the buffers from the page when it is being truncated. It returns zero on success.  The filesystem must exclusively acquire invalidate_lock before invalidating page cache in truncate / hole punch path (and thus calling into -&gt;invalidate_folio) to block races between page cache invalidation and page cache filling functions (fault, read, ...).

-&gt;release_folio() is called when the MM wants to make a change to the folio that would invalidate the filesystem's private data.  For example, it may be about to be removed from the address_space or split.  The folio is locked and not under writeback.  It may be dirty.  The gfp parameter is not usually used for allocation, but rather to indicate what the filesystem may do to attempt to free the private data.  The filesystem may return false to indicate that the folio's private data cannot be freed. If it returns true, it should have already removed the private data from the folio.  If a filesystem does not provide a -&gt;release_folio method, the pagecache will assume that private data is buffer_heads and call try_to_free_buffers().

-&gt;free_folio() is called when the kernel has dropped the folio from the page cache.

-&gt;launder_folio() may be called prior to releasing a folio if it is still found to be dirty. It returns zero if the folio was successfully cleaned, or an error value if not. Note that in order to prevent the folio getting mapped back in and redirtied, it needs to be kept locked across the entire operation.

-&gt;swap_activate() will be called to prepare the given file for swap.  It should perform any validation and preparation necessary to ensure that writes can be performed with minimal memory allocation.  It should call add_swap_extent(), or the helper iomap_swapfile_activate(), and return the number of extents added.  If IO should be submitted through -&gt;swap_rw(), it should set SWP_FS_OPS, otherwise IO will be submitted directly to the block device `sis->bdev`.

-&gt;swap_deactivate() will be called in the sys_swapoff() path after -&gt;swap_activate() returned success.

-&gt;swap_rw will be called for swap IO if SWP_FS_OPS was set by -&gt;swap_activate().

<a id="rst-file-lock-operations"></a>

## file_lock_operations

prototypes:



```text
void (*fl_copy_lock)(struct file_lock *, struct file_lock *);
void (*fl_release_private)(struct file_lock *);
```

locking rules:


<table>
<thead>
<tr>
<th>


ops

</th>
<th>


inode-&gt;i_lock

</th>
<th>


may block

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


fl_copy_lock:

</td>
<td>


yes

</td>
<td>


no

</td>
</tr>
<tr>
<td>


fl_release_private:

</td>
<td>


maybe

</td>
<td>


maybe\[1\]\_

</td>
</tr>
</tbody>
</table>

<!-- [1]:
->fl_release_private for flock or POSIX locks is currently allowed
to block. Leases however can still be freed while the i_lock is held and
so fl_release_private called on a lease should not block. -->

<a id="rst-lock-manager-operations"></a>

## lock_manager_operations

prototypes:



```text
void (*lm_notify)(struct file_lock *);  /* unblock callback */
int (*lm_grant)(struct file_lock *, struct file_lock *, int);
void (*lm_break)(struct file_lock *); /* break_lease callback */
int (*lm_change)(struct file_lock **, int);
bool (*lm_breaker_owns_lease)(struct file_lock *);
bool (*lm_lock_expirable)(struct file_lock *);
void (*lm_expire_lock)(void);
```

locking rules:


<table>
<thead>
<tr>
<th>


ops

</th>
<th>


flc_lock

</th>
<th>


blocked_lock_lock

</th>
<th>


may block

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


lm_notify:

</td>
<td>


no

</td>
<td>


yes

</td>
<td>


no

</td>
</tr>
<tr>
<td>


lm_grant:

</td>
<td>


no

</td>
<td>


no

</td>
<td>


no

</td>
</tr>
<tr>
<td>


lm_break:

</td>
<td>


yes

</td>
<td>


no

</td>
<td>


no

</td>
</tr>
<tr>
<td>


lm_change

</td>
<td>


yes

</td>
<td>


no

</td>
<td>


no

</td>
</tr>
<tr>
<td>


lm_breaker_owns_lease:

</td>
<td>


yes

</td>
<td>


no

</td>
<td>


no

</td>
</tr>
<tr>
<td>


lm_lock_expirable

</td>
<td>


yes

</td>
<td>


no

</td>
<td>


no

</td>
</tr>
<tr>
<td>


lm_expire_lock

</td>
<td>


no

</td>
<td>


no

</td>
<td>


yes

</td>
</tr>
<tr>
<td>


lm_open_conflict

</td>
<td>


yes

</td>
<td>


no

</td>
<td>


no

</td>
</tr>
</tbody>
</table>

<a id="rst-buffer-head"></a>

## buffer_head

prototypes:



```text
void (*b_end_io)(struct buffer_head *bh, int uptodate);
```

locking rules:

called from interrupts. In other words, extreme care is needed here. bh is locked, but that's all warranties we have here. Currently only RAID1, highmem, fs/buffer.c, and fs/ntfs/aops.c are providing these. Block devices call this method upon the IO completion.

<a id="rst-block-device-operations"></a>

## block_device_operations

prototypes:



```text
int (*open) (struct block_device *, fmode_t);
int (*release) (struct gendisk *, fmode_t);
int (*ioctl) (struct block_device *, fmode_t, unsigned, unsigned long);
int (*compat_ioctl) (struct block_device *, fmode_t, unsigned, unsigned long);
int (*direct_access) (struct block_device *, sector_t, void **,
                        unsigned long *);
void (*unlock_native_capacity) (struct gendisk *);
int (*getgeo)(struct gendisk *, struct hd_geometry *);
void (*swap_slot_free_notify) (struct block_device *, unsigned long);
```

locking rules:


<table>
<thead>
<tr>
<th>


ops

</th>
<th>


open_mutex

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


open:

</td>
<td>


yes

</td>
</tr>
<tr>
<td>


release:

</td>
<td>


yes

</td>
</tr>
<tr>
<td>


ioctl:

</td>
<td>


no

</td>
</tr>
<tr>
<td>


compat_ioctl:

</td>
<td>


no

</td>
</tr>
<tr>
<td>


direct_access:

</td>
<td>


no

</td>
</tr>
<tr>
<td>


unlock_native_capacity:

</td>
<td>


no

</td>
</tr>
<tr>
<td>


getgeo:

</td>
<td>


no

</td>
</tr>
<tr>
<td>


swap_slot_free_notify:

</td>
<td>


no      (see below)

</td>
</tr>
</tbody>
</table>

swap_slot_free_notify is called with swap_lock and sometimes the page lock held.

<a id="rst-file-operations"></a>

## file_operations

prototypes:



```text
loff_t (*llseek) (struct file *, loff_t, int);
ssize_t (*read) (struct file *, char __user *, size_t, loff_t *);
ssize_t (*write) (struct file *, const char __user *, size_t, loff_t *);
ssize_t (*read_iter) (struct kiocb *, struct iov_iter *);
ssize_t (*write_iter) (struct kiocb *, struct iov_iter *);
int (*iopoll) (struct kiocb *kiocb, bool spin);
int (*iterate_shared) (struct file *, struct dir_context *);
__poll_t (*poll) (struct file *, struct poll_table_struct *);
long (*unlocked_ioctl) (struct file *, unsigned int, unsigned long);
long (*compat_ioctl) (struct file *, unsigned int, unsigned long);
int (*mmap) (struct file *, struct vm_area_struct *);
int (*open) (struct inode *, struct file *);
int (*flush) (struct file *);
int (*release) (struct inode *, struct file *);
int (*fsync) (struct file *, loff_t start, loff_t end, int datasync);
int (*fasync) (int, struct file *, int);
int (*lock) (struct file *, int, struct file_lock *);
unsigned long (*get_unmapped_area)(struct file *, unsigned long,
                unsigned long, unsigned long, unsigned long);
int (*check_flags)(int);
int (*flock) (struct file *, int, struct file_lock *);
ssize_t (*splice_write)(struct pipe_inode_info *, struct file *, loff_t *,
                size_t, unsigned int);
ssize_t (*splice_read)(struct file *, loff_t *, struct pipe_inode_info *,
                size_t, unsigned int);
int (*setlease)(struct file *, int, struct file_lease **, void **);
int (*getlease)(struct file *, struct file *lease_file, unsigned int flavor);
long (*fallocate)(struct file *, int, loff_t, loff_t);
void (*show_fdinfo)(struct seq_file *m, struct file *f);
unsigned (*mmap_capabilities)(struct file *);
ssize_t (*copy_file_range)(struct file *, loff_t, struct file *,
                loff_t, size_t, unsigned int);
loff_t (*remap_file_range)(struct file *file_in, loff_t pos_in,
                struct file *file_out, loff_t pos_out,
                loff_t len, unsigned int remap_flags);
int (*fadvise)(struct file *, loff_t, loff_t, int);
```

- **locking rules:**

  All may block.

-&gt;llseek() locking has moved from llseek to the individual llseek implementations.  If your fs is not using generic_file_llseek, you need to acquire and release the appropriate locks in your -&gt;llseek(). For many filesystems, it is probably safe to acquire the inode mutex or just to use i_size_read() instead. Note: this does not protect the file-&gt;f_pos against concurrent modifications since this is something the userspace has to take care about.

-&gt;iterate_shared() is called with i_rwsem held for reading, and with the file f_pos_lock held exclusively

-&gt;fasync() is responsible for maintaining the FASYNC bit in filp-&gt;f_flags. Most instances call fasync_helper(), which does that maintenance, so it's not normally something one needs to worry about.  Return values &gt; 0 will be mapped to zero in the VFS layer.

-&gt;readdir() and -&gt;ioctl() on directories must be changed. Ideally we would move -&gt;readdir() to inode_operations and use a separate method for directory -&gt;ioctl() or kill the latter completely. One of the problems is that for anything that resembles union-mount we won't have a struct file for all components. And there are other reasons why the current interface is a mess...

-&gt;read on directories probably must go away - we should just enforce -EISDIR in sys_read() and friends.

-&gt;setlease operations should call generic_setlease() before or after setting the lease within the individual filesystem to record the result of the operation

-&gt;fallocate implementation must be really careful to maintain page cache consistency when punching holes or performing other operations that invalidate page cache contents. Usually the filesystem needs to call truncate_inode_pages_range() to invalidate relevant range of the page cache. However the filesystem usually also needs to update its internal (and on disk) view of file offset -&gt; disk block mapping. Until this update is finished, the filesystem needs to block page faults and reads from reloading now-stale page cache contents from the disk. Since VFS acquires mapping-&gt;invalidate_lock in shared mode when loading pages from disk (filemap_fault(), filemap_read(), readahead paths), the fallocate implementation must take the invalidate_lock to prevent reloading.

-&gt;copy_file_range and -&gt;remap_file_range implementations need to serialize against modifications of file data while the operation is running. For blocking changes through write(2) and similar operations inode-&gt;i_rwsem can be used. To block changes to file contents via a memory mapping during the operation, the filesystem must take mapping-&gt;invalidate_lock to coordinate with -&gt;page_mkwrite.

<a id="rst-dquot-operations"></a>

## dquot_operations

prototypes:



```text
int (*write_dquot) (struct dquot *);
int (*acquire_dquot) (struct dquot *);
int (*release_dquot) (struct dquot *);
int (*mark_dirty) (struct dquot *);
int (*write_info) (struct super_block *, int);
```

These operations are intended to be more or less wrapping functions that ensure a proper locking wrt the filesystem and call the generic quota operations.

What filesystem should expect from the generic quota functions:


<table>
<thead>
<tr>
<th>


ops

</th>
<th>


FS recursion

</th>
<th>


Held locks when called

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


write_dquot:

</td>
<td>


yes

</td>
<td>


dqonoff_sem or dqptr_sem

</td>
</tr>
<tr>
<td>


acquire_dquot:

</td>
<td>


yes

</td>
<td>


dqonoff_sem or dqptr_sem

</td>
</tr>
<tr>
<td>


release_dquot:

</td>
<td>


yes

</td>
<td>


dqonoff_sem or dqptr_sem

</td>
</tr>
<tr>
<td>


mark_dirty:

</td>
<td>


no

</td>
<td>


- <!-- empty source list item -->

</td>
</tr>
<tr>
<td>


write_info:

</td>
<td>


yes

</td>
<td>


dqonoff_sem

</td>
</tr>
</tbody>
</table>

FS recursion means calling -&gt;quota_read() and -&gt;quota_write() from superblock operations.

More details about quota locking can be found in fs/dquot.c.

<a id="rst-vm-operations-struct"></a>

## vm_operations_struct

prototypes:



```text
void (*open)(struct vm_area_struct *);
void (*close)(struct vm_area_struct *);
vm_fault_t (*fault)(struct vm_fault *);
vm_fault_t (*huge_fault)(struct vm_fault *, unsigned int order);
vm_fault_t (*map_pages)(struct vm_fault *, pgoff_t start, pgoff_t end);
vm_fault_t (*page_mkwrite)(struct vm_area_struct *, struct vm_fault *);
vm_fault_t (*pfn_mkwrite)(struct vm_area_struct *, struct vm_fault *);
int (*access)(struct vm_area_struct *, unsigned long, void*, int, int);
```

locking rules:


<table>
<thead>
<tr>
<th>


ops

</th>
<th>


mmap_lock

</th>
<th>


PageLocked(page)

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


open:

</td>
<td>


write

</td>
<td>




</td>
</tr>
<tr>
<td>


close:

</td>
<td>


read/write

</td>
<td>




</td>
</tr>
<tr>
<td>


fault:

</td>
<td>


read

</td>
<td>


can return with page locked

</td>
</tr>
<tr>
<td>


huge_fault:

</td>
<td>


maybe-read

</td>
<td>




</td>
</tr>
<tr>
<td>


map_pages:

</td>
<td>


maybe-read

</td>
<td>




</td>
</tr>
<tr>
<td>


page_mkwrite:

</td>
<td>


read

</td>
<td>


can return with page locked

</td>
</tr>
<tr>
<td>


pfn_mkwrite:

</td>
<td>


read

</td>
<td>




</td>
</tr>
<tr>
<td>


access:

</td>
<td>


read

</td>
<td>




</td>
</tr>
</tbody>
</table>

-&gt;fault() is called when a previously not present pte is about to be faulted in. The filesystem must find and return the page associated with the passed in "pgoff" in the vm_fault structure. If it is possible that the page may be truncated and/or invalidated, then the filesystem must lock invalidate_lock, then ensure the page is not already truncated (invalidate_lock will block subsequent truncate), and then return with VM_FAULT_LOCKED, and the page locked. The VM will unlock the page.

-&gt;huge_fault() is called when there is no PUD or PMD entry present.  This gives the filesystem the opportunity to install a PUD or PMD sized page. Filesystems can also use the -&gt;fault method to return a PMD sized page, so implementing this function may not be necessary.  In particular, filesystems should not call filemap_fault() from -&gt;huge_fault(). The mmap_lock may not be held when this method is called.

-&gt;map_pages() is called when VM asks to map easy accessible pages. Filesystem should find and map pages associated with offsets from "start_pgoff" till "end_pgoff". -&gt;map_pages() is called with the RCU lock held and must not block.  If it's not possible to reach a page without blocking, filesystem should skip it. Filesystem should use set_pte_range() to setup page table entry. Pointer to entry associated with the page is passed in "pte" field in vm_fault structure. Pointers to entries for other offsets should be calculated relative to "pte".

-&gt;page_mkwrite() is called when a previously read-only pte is about to become writeable. The filesystem again must ensure that there are no truncate/invalidate races or races with operations such as -&gt;remap_file_range or -&gt;copy_file_range, and then return with the page locked. Usually mapping-&gt;invalidate_lock is suitable for proper serialization. If the page has been truncated, the filesystem should not look up a new page like the -&gt;fault() handler, but simply return with VM_FAULT_NOPAGE, which will cause the VM to retry the fault.

-&gt;pfn_mkwrite() is the same as page_mkwrite but when the pte is VM_PFNMAP or VM_MIXEDMAP with a page-less entry. Expected return is VM_FAULT_NOPAGE. Or one of the VM_FAULT_ERROR types. The default behavior after this call is to make the pte read-write, unless pfn_mkwrite returns an error.

-&gt;access() is called when get_user_pages() fails in access_process_vm(), typically used to debug a process through /proc/pid/mem or ptrace.  This function is needed only for VM_IO \| VM_PFNMAP VMAs.

---

> Dubious stuff

(if you break something or notice that it is broken and do not fix it yourself - at least put it here)
