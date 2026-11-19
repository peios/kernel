// SPDX-License-Identifier: GPL-2.0-only

#include <linux/atomic.h>
#include <linux/errno.h>
#include <linux/fs.h>
#include <linux/mutex.h>
#include <linux/printk.h>
#include <linux/rcupdate.h>
#include <linux/slab.h>

#include "lsm_internal.h"
#include "object_lifecycle.h"
#include "copy_up.h"
#include "nt_file.h"
#include "nt_lease.h"

#include <trace/events/kacs.h>

int pkm_kacs_inode_alloc_security(struct inode *inode)
{
	struct pkm_kacs_inode_security *sec;

	if (!inode || !inode->i_security)
		return -EINVAL;

	sec = pkm_kacs_inode(inode);
	mutex_init(&sec->lock);
	RCU_INIT_POINTER(sec->sd_cache, NULL);
	sec->sd_cache_epoch = 0;
	sec->sd_cache_invalidation = 0;
	sec->sd_cache_read_ticket = 0;
	sec->sd_cache_published_ticket = 0;
	sec->nt = NULL;
	atomic_set(&sec->sattr_cache, 0);
	atomic_set(&sec->nt_pins, 0);
	atomic_set(&sec->signed_exec_pinned, 0);
	sec->persist_work_queued = false;
#ifdef CONFIG_SECURITY_PKM_KUNIT
	sec->kunit_fake_xattr_enabled = false;
	sec->kunit_fake_xattr_bytes = NULL;
	sec->kunit_fake_xattr_len = 0;
	sec->kunit_fake_xattr_get_errno = 0;
	sec->kunit_persist_queue_calls = 0;
	sec->kunit_unlink_calls = 0;
	sec->kunit_open_cache_selected = NULL;
	sec->kunit_open_cache_context = NULL;
#endif
	return 0;
}

int pkm_kacs_file_alloc_security(struct file *file)
{
	struct pkm_kacs_file_security *sec;

	if (!file || !file->f_security)
		return 0;

	sec = pkm_kacs_file(file);
	sec->granted_access = 0;
	sec->continuous_audit_mask = 0;
	sec->copy_up_context = NULL;
	sec->copy_up_phase_generation = 0;
	sec->nt_inode = NULL;
	sec->nt_inode_held = 0;
	sec->nt_classes = 0;
	sec->nt_share = 0;
	sec->nt_intent = 0;
	sec->lease_mgr = NULL;
	sec->pins = NULL;
	sec->managed = 0;
	sec->delete_on_close = 0;
	sec->delete_on_close_token = NULL;
	return 0;
}

int pkm_kacs_backing_file_alloc(struct file *backing_file,
				const struct file *user_file)
{
	struct pkm_kacs_backing_file_security *backing_sec;
	const struct pkm_kacs_file_security *user_sec;

	if (!backing_file || !user_file || !backing_file_security(backing_file))
		return -EINVAL;

	backing_sec = pkm_kacs_backing_file(backing_file);
	backing_sec->granted_access = 0;
	backing_sec->continuous_audit_mask = 0;
	backing_sec->nt_classes = 0;
	backing_sec->nt_share = 0;
	backing_sec->nt_intent = 0;
	backing_sec->lease_mgr = NULL;
	backing_sec->managed = 0;
	backing_sec->inherited = 0;

	/*
	 * Copy-up backing files are authorized by their exact, phase-bound KACS
	 * context and explicitly adopt the outer descriptor's snapshot after the
	 * stage has been verified.  Generic backing-file inheritance here would
	 * pre-populate the backing blob and make that fail-closed handoff
	 * indistinguishable from an unrelated stackable-filesystem open.
	 */
	if (pkm_kacs_copy_up_active())
		return 0;

	if (!user_file->f_security || (user_file->f_mode & FMODE_PATH))
		return 0;
	user_sec = pkm_kacs_file(user_file);
	if (!user_sec->managed || user_sec->copy_up_context)
		return 0;

	/*
	 * A backing file is a kernel-private implementation detail of the
	 * already-authorized user file.  Capture values only: retaining the
	 * outer file would form a reference cycle.  The separate backing blob
	 * is the unforgeable association used when security_file_open() later
	 * runs on the provider path.
	 */
	backing_sec->granted_access = user_sec->granted_access;
	backing_sec->continuous_audit_mask = user_sec->continuous_audit_mask;
	backing_sec->nt_classes = user_sec->nt_classes;
	backing_sec->nt_share = user_sec->nt_share;
	backing_sec->nt_intent = user_sec->nt_intent;
	/* Borrowed: the outer open holds the manager while this one opens. */
	backing_sec->lease_mgr = user_sec->lease_mgr;
	memcpy(backing_sec->lease_key, user_sec->lease_key,
	       sizeof(backing_sec->lease_key));
	backing_sec->managed = 1;
	backing_sec->inherited = 1;
	return 0;
}

bool pkm_kacs_backing_file_inherited(const struct file *backing_file)
{
	if (!backing_file || !(backing_file->f_mode & FMODE_BACKING) ||
	    !backing_file_security(backing_file))
		return false;

	return pkm_kacs_backing_file(backing_file)->inherited;
}

int pkm_kacs_backing_file_apply(struct file *backing_file)
{
	struct pkm_kacs_backing_file_security *backing_sec;
	struct pkm_kacs_file_security *file_sec;

	if (!pkm_kacs_backing_file_inherited(backing_file))
		return -ENOENT;
	if (!backing_file->f_security)
		return -EACCES;

	backing_sec = pkm_kacs_backing_file(backing_file);
	file_sec = pkm_kacs_file(backing_file);
	file_sec->granted_access = backing_sec->granted_access;
	file_sec->continuous_audit_mask = backing_sec->continuous_audit_mask;
	file_sec->managed = backing_sec->managed;
	return 0;
}

int pkm_kacs_mmap_backing_file(struct vm_area_struct *vma,
			       struct file *backing_file,
			       struct file *user_file)
{
	struct pkm_kacs_backing_file_security *backing_sec;
	struct pkm_kacs_file_security *file_sec;
	struct pkm_kacs_file_security *user_sec;

	(void)vma;
	if (!pkm_kacs_backing_file_inherited(backing_file) || !user_file ||
	    !backing_file->f_security || !user_file->f_security)
		return -EACCES;

	backing_sec = pkm_kacs_backing_file(backing_file);
	file_sec = pkm_kacs_file(backing_file);
	user_sec = pkm_kacs_file(user_file);
	if (!backing_sec->managed || !file_sec->managed || !user_sec->managed ||
	    backing_sec->granted_access != file_sec->granted_access ||
	    backing_sec->continuous_audit_mask !=
		    file_sec->continuous_audit_mask ||
	    backing_sec->granted_access != user_sec->granted_access ||
	    backing_sec->continuous_audit_mask !=
		    user_sec->continuous_audit_mask)
		return -EACCES;
	return 0;
}

void pkm_kacs_file_release(struct file *file)
{
	if (!file || !file->f_security)
		return;

	pkm_kacs_copy_up_file_release(file);
	/*
	 * Release the open's NT share registration, marking the file
	 * delete-pending first if the open was made delete-on-close, and
	 * removing it if this was the last open of a delete-pending file.
	 */
	pkm_kacs_nt_release(file);
}

/*
 * A file whose open failed after the open hook ran never reaches
 * file_release. do_dentry_open() calls pkm_kacs_file_open_failed() for it,
 * in the opener's context; this is the backstop for anything that frees a
 * registered file otherwise, and must not sleep (PEI-1723).
 */
void pkm_kacs_file_free_security(struct file *file)
{
	pkm_kacs_nt_free(file);
	pkm_kacs_lease_file_free(file);
}

void pkm_kacs_file_open_failed(struct file *file)
{
	pkm_kacs_nt_open_failed(file);
}

int pkm_kacs_file_receive(struct file *file)
{
	/*
	 * SCM_RIGHTS transfers an already-open handle. KACS keeps the original
	 * cached grant on the file security blob rather than re-authorizing the
	 * receiver as a fresh open.
	 */
	if (file && file->f_security && pkm_kacs_file(file)->copy_up_context)
		return -EACCES;
	return 0;
}

int pkm_kacs_sb_alloc_security(struct super_block *sb)
{
	struct pkm_kacs_superblock_security *sec;

	if (!sb || !sb->s_security)
		return 0;

	sec = pkm_kacs_sb(sb);
	mutex_init(&sec->lock);
	/*
	 * security_sb_alloc fires in alloc_super() BEFORE the filesystem
	 * type's fill_super/init_fs_context callback sets s_magic. We cannot
	 * resolve the magic-derived policy here - s_magic is always zero at
	 * this point. Leave mount_policy at the invalid sentinel 0 and let
	 * superblock_mount_policy() lazy-resolve + lazy-cache on the first
	 * read that observes a populated magic. Explicit kacs_set_mount_policy()
	 * syscalls still write a valid value here and short-circuit the
	 * lazy path.
	 */
	sec->mount_policy = 0;
	sec->policy_generation = 0;
	sec->template_sd_bytes = NULL;
	sec->template_sd_len = 0;
	return 0;
}

void pkm_kacs_sb_free_security(struct super_block *sb)
{
	struct pkm_kacs_superblock_security *sec;

	if (!sb || !sb->s_security)
		return;

	sec = pkm_kacs_sb(sb);
	mutex_lock(&sec->lock);
	if (sec->template_sd_bytes)
		pkm_kacs_free((void *)sec->template_sd_bytes);
	sec->template_sd_bytes = NULL;
	sec->template_sd_len = 0;
	mutex_unlock(&sec->lock);
	mutex_destroy(&sec->lock);
}

void pkm_kacs_inode_free_security_rcu(void *inode_security)
{
	struct pkm_kacs_inode_security *sec;
	struct pkm_kacs_inode_sd_cache *cache;

	if (!inode_security)
		return;

	sec = (struct pkm_kacs_inode_security *)((char *)inode_security +
						 pkm_blob_sizes.lbs_inode);
	cache = rcu_dereference_protected(sec->sd_cache, 1);
	RCU_INIT_POINTER(sec->sd_cache, NULL);
	pkm_kacs_nt_inode_free(sec->nt);
	sec->nt = NULL;
	atomic_set(&sec->signed_exec_pinned, 0);
	pkm_kacs_inode_sd_cache_free(cache);
#ifdef CONFIG_SECURITY_PKM_KUNIT
	if (sec->kunit_fake_xattr_bytes)
		kfree(sec->kunit_fake_xattr_bytes);
	sec->kunit_fake_xattr_bytes = NULL;
	sec->kunit_fake_xattr_len = 0;
	sec->kunit_fake_xattr_enabled = false;
	sec->kunit_unlink_calls = 0;
	sec->kunit_open_cache_selected = NULL;
	sec->kunit_open_cache_context = NULL;
#endif
}

bool pkm_kacs_inode_signed_exec_pinned(const struct inode *inode)
{
	struct pkm_kacs_inode_security *sec;

	if (!inode || !inode->i_security)
		return false;

	sec = pkm_kacs_inode((struct inode *)inode);
	return atomic_read(&sec->signed_exec_pinned) != 0;
}

int pkm_kacs_mark_signed_exec_pinned_file(const struct file *file)
{
	struct inode *inode;
	struct pkm_kacs_inode_security *sec;

	if (!file)
		return -EACCES;

	inode = file_inode((struct file *)file);
	if (!inode || !inode->i_security)
		return -EACCES;

	sec = pkm_kacs_inode(inode);
	atomic_set(&sec->signed_exec_pinned, 1);
	trace_kacs_object(inode, KACS_OBJ_SIGNED_EXEC_PIN, 0);
	return 0;
}

int pkm_kacs_check_signed_exec_content_mutation_inode(const struct inode *inode)
{
	if (pkm_kacs_inode_signed_exec_pinned(inode)) {
		trace_kacs_object(inode, KACS_OBJ_SIGNED_EXEC_MUTATION_BLOCKED,
				  -EACCES);
		return -EACCES;
	}

	return 0;
}

int pkm_kacs_check_signed_exec_content_mutation_file(const struct file *file)
{
	if (!file)
		return -EACCES;

	return pkm_kacs_check_signed_exec_content_mutation_inode(
		file_inode((struct file *)file));
}
