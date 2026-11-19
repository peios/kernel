/* SPDX-License-Identifier: GPL-2.0-only */
#ifndef _SECURITY_PKM_KACS_NT_LOCK_H
#define _SECURITY_PKM_KACS_NT_LOCK_H

#include <linux/fs.h>
#include <linux/types.h>

/*
 * NT byte-range locks (TRM "Byte-Range Locks"), kept in the file's NT state
 * and enforced on every read, write, truncation and content-changing
 * fallocate when it is issued.
 */

/* Release every lock an open holds, as it closes. */
void pkm_kacs_nt_locks_release(struct file *file);

/* -EAGAIN if I/O through @file over the range conflicts with a lock. */
int pkm_kacs_nt_lock_check_io(struct file *file, loff_t pos, size_t count,
			      bool write);
/* The same, for a size change of @inode, by @file if it is known. */
int pkm_kacs_nt_lock_check_resize(struct inode *inode, struct file *file,
				  loff_t new_size);
/* The same, for fallocate. */
int pkm_kacs_nt_lock_check_fallocate(struct file *file, int mode, loff_t offset,
				     loff_t len);

#endif /* _SECURITY_PKM_KACS_NT_LOCK_H */
