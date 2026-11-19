/* SPDX-License-Identifier: GPL-2.0-only */
#ifndef _SECURITY_PKM_KACS_NT_FILE_H
#define _SECURITY_PKM_KACS_NT_FILE_H

#include <linux/fs.h>
#include <linux/list.h>
#include <linux/path.h>
#include <linux/spinlock.h>
#include <linux/types.h>
#include <linux/wait.h>

#include <pkm/file.h>
#include <pkm/sd.h>

/*
 * NT handle semantics for files on managed mounts (TRM "Sharing and
 * Deletion", "Byte-Range Locks"): share-mode accounting, the delete-pending
 * mark and the last-close removal it promises, and byte-range locks.
 *
 * The state hangs off the KACS inode blob of the inode an open really
 * reaches: a regular filesystem's own inode, or the provider inode below a
 * stacking filesystem, where the backing file registers on the outer
 * open's behalf. It is allocated at the first registration and freed with
 * the inode.
 */

/* Share classes; the same bits as KACS_FILE_SHARE_*. */
#define PKM_KACS_NT_READ 0x1U
#define PKM_KACS_NT_WRITE 0x2U
#define PKM_KACS_NT_DELETE 0x4U
#define PKM_KACS_NT_ALL \
	(PKM_KACS_NT_READ | PKM_KACS_NT_WRITE | PKM_KACS_NT_DELETE)

/* FILE_GENERIC_WRITE, as MS-FSA's directory first-open rule asks it. */
#define PKM_KACS_FILE_GENERIC_WRITE                                          \
	(KACS_FILE_WRITE_DATA | KACS_FILE_APPEND_DATA | KACS_FILE_WRITE_EA | \
	 KACS_FILE_WRITE_ATTRIBUTES | KACS_ACCESS_READ_CONTROL |             \
	 KACS_ACCESS_SYNCHRONIZE)

/* Share checks a registration may set aside, by backup or restore intent. */
#define PKM_KACS_NT_OVERRIDE_READ 0x1U
#define PKM_KACS_NT_OVERRIDE_WRITE_DELETE 0x2U

struct pkm_kacs_nt_state {
	spinlock_t lock;
	/* Registered opens, whether or not they take part in share checks. */
	u32 opens;
	/* Taking part: opens holding each class, and opens not sharing it. */
	u32 holding[3];
	u32 denying[3];
	/*
	 * Delete-pending: the name to remove at the last close and the token
	 * that set the mark, each held by reference. deleting covers the
	 * removal itself, during which new opens still fail.
	 */
	bool delete_pending;
	bool deleting;
	struct path delete_path;
	const struct inode *delete_dentry_inode;
	const void *delete_token;
	/* Byte-range locks (nt_lock.c), under lock. */
	struct list_head locks;
	struct list_head lock_waiters;
	wait_queue_head_t lock_wq;
	/* NT leases on the file (nt_lease.c), under lock. */
	struct list_head leases;
	u32 nleases;
	wait_queue_head_t lease_wq;
	u32 nlocks;
	/* Locks whose owner could write the file, and so block I/O. */
	u32 nblocking;
};

/* The share classes an access mask holds. */
u32 pkm_kacs_nt_classes_from_access(u32 access);
/* The share classes a legacy open's mode holds. */
u32 pkm_kacs_nt_classes_from_mode(fmode_t mode);

/* The inode's NT state, allocating it when create is set. */
struct pkm_kacs_nt_state *pkm_kacs_nt_state(struct inode *inode, bool create);

/*
 * Whether NT handle semantics apply to an inode: a regular file or a
 * directory on a managed mount.
 */
bool pkm_kacs_nt_applies(const struct inode *inode);
/* Whether a file's opens are registered by their backing file instead. */
bool pkm_kacs_nt_stacked(const struct inode *inode);

/*
 * The inode holding the NT state for an open or a name, referenced; NULL
 * where NT handle semantics do not apply. Drop it with iput().
 */
struct inode *pkm_kacs_nt_record_inode_for_file(struct file *file);
struct inode *pkm_kacs_nt_record_inode_for_dentry(struct dentry *dentry);

/*
 * Register an open on inode: fail with -EBUSY if the file is delete-pending
 * or the share check refuses it, noting the NT status for a native open.
 */
int pkm_kacs_nt_register(struct file *file, struct inode *inode, u32 classes,
			 u32 share, u32 overrides);

/* Unregister at close: may set the file delete-pending, and remove it. */
void pkm_kacs_nt_release(struct file *file);
/* Unregister an open whose opening failed after it registered. */
void pkm_kacs_nt_open_failed(struct file *file);
/* The last chance to unregister, from file_free_security; never sleeps. */
void pkm_kacs_nt_free(struct file *file);

/* -EBUSY if the file is delete-pending. */
int pkm_kacs_nt_check_not_pending(struct inode *record_inode);
/*
 * -EBUSY if deleting the file by name is refused: it is delete-pending, or
 * an open of it does not share delete.
 */
int pkm_kacs_nt_check_delete_by_name(struct inode *record_inode);

/* Set or clear the delete-pending mark. */
int pkm_kacs_nt_mark_delete_pending(struct inode *record_inode,
				    const struct path *path,
				    const void *subject_token);
void pkm_kacs_nt_clear_delete_pending(struct inode *record_inode);
bool pkm_kacs_nt_delete_pending(struct inode *record_inode);

/*
 * Remove the name path now, as the deferred deletion of record_inode, with
 * the namespace hooks letting exactly this removal through.
 */
long pkm_kacs_nt_remove_now(const struct path *path,
			    const struct inode *dentry_inode,
			    struct inode *record_inode, const void *token);

/* The NT status a native open reports when it fails. */
void pkm_kacs_nt_note_status(u32 status);
u32 pkm_kacs_nt_take_status(void);

/* Whether the current task is carrying out this deferred deletion. */
bool pkm_kacs_nt_deferred_delete_matches(const struct inode *dir,
					 const struct dentry *dentry);

/* Release the state an inode carries when it is freed. */
void pkm_kacs_nt_inode_free(struct pkm_kacs_nt_state *state);

#endif /* _SECURITY_PKM_KACS_NT_FILE_H */
