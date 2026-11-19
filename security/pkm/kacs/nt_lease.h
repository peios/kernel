/* SPDX-License-Identifier: GPL-2.0-only */
#ifndef _SECURITY_PKM_KACS_NT_LEASE_H
#define _SECURITY_PKM_KACS_NT_LEASE_H

#include <linux/fs.h>
#include <linux/types.h>

/*
 * NT caching leases for lease managers (TRM "Leases").
 *
 * A lease belongs to one open, made under its manager's key, and lives in
 * the file's NT state. Operations KACS sees with no lock held -- opens, a
 * sharing conflict, delete dispositions, byte-range locks, security
 * changes, writes -- break leases directly. Operations the VFS performs
 * under inode locks -- unlink, rename, link, setattr, setxattr -- reach a
 * delegation-style fs/locks.c entry each lease carries, so that the VFS
 * drops its locks and waits for the break as it does for NFS delegations;
 * the KACS hook that ran just before notes what the operation is.
 */

struct kacs_open_how;
struct pkm_kacs_lease_manager;

/* kacs_open: take the opener's lease key for this open's breaks. */
int pkm_kacs_lease_prepare_open(const struct kacs_open_how *how);
void pkm_kacs_lease_finish_open(void);
/* The open hook: record the opener's key on the new open. */
void pkm_kacs_lease_bind_open(struct file *file);

/*
 * Break other holders' leases on record_inode for an operation through
 * @file (whose own key is exempt; NULL for none). Waits for breaks that
 * must be acknowledged, unless the open is non-blocking. Returns the
 * number of leases broken, or a negative errno.
 */
int pkm_kacs_lease_break_inode(struct inode *record_inode, u32 reason,
			       struct file *file);
/* A sharing conflict: break handle caching and report whether any went. */
int pkm_kacs_lease_break_for_sharing(struct file *file,
				     struct inode *record_inode);
/* A write through @file: other holders lose read caching (no wait). */
void pkm_kacs_lease_note_write(struct file *file);

/*
 * Note the operation the VFS is about to break delegations for, so that a
 * lease's fs/locks.c entry can tell whether it must break.
 */
void pkm_kacs_lease_note_vfs_break(struct inode *inode, u32 reason);
void pkm_kacs_lease_clear_vfs_breaks(void);
/* The open a VFS operation is made through, whose key is exempt. */
void pkm_kacs_lease_set_breaker_file(struct file *file);

/* Release the leases an open holds, as it closes. */
void pkm_kacs_lease_release_file(struct file *file);
/* Drop an open's reference to its manager. */
void pkm_kacs_lease_file_free(struct file *file);

#endif /* _SECURITY_PKM_KACS_NT_LEASE_H */
