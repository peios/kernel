// SPDX-License-Identifier: GPL-2.0-only
/*
 * NT share modes and delete-pending files (TRM "Sharing and Deletion").
 *
 * Every open of a regular file or directory on a managed mount registers
 * here: what share classes it holds and which it lets others hold. The
 * check is MS-FSA 2.1.5.1.2.1 and 2.1.5.1.2.2 over counters, so it is O(1)
 * under one spinlock however many opens there are. An open whose access
 * holds no share class takes no part, but is counted, because the last
 * close of any open is what removes a delete-pending file.
 */

#include <linux/dcache.h>
#include <linux/fs.h>
#include <linux/kacs_stratafs.h>
#include <linux/magic.h>
#include <linux/mount.h>
#include <linux/namei.h>
#include <linux/printk.h>
#include <linux/sched.h>
#include <linux/slab.h>
#include <linux/workqueue.h>

#include <pkm/file.h>
#include <pkm/sd.h>

#include "lsm_internal.h"
#include "mount_policy.h"
#include "nt_file.h"
#include "nt_lease.h"
#include "nt_lock.h"
#include "nt_pin.h"
#include "token_runtime.h"

#include <trace/events/kacs.h>

u32 pkm_kacs_nt_classes_from_access(u32 access)
{
	u32 classes = 0;

	if (access & (KACS_FILE_READ_DATA | KACS_FILE_EXECUTE))
		classes |= PKM_KACS_NT_READ;
	if (access & (KACS_FILE_WRITE_DATA | KACS_FILE_APPEND_DATA))
		classes |= PKM_KACS_NT_WRITE;
	if (access & KACS_ACCESS_DELETE)
		classes |= PKM_KACS_NT_DELETE;
	return classes;
}

u32 pkm_kacs_nt_classes_from_mode(fmode_t mode)
{
	u32 classes = 0;

	if (mode & (FMODE_READ | FMODE_EXEC))
		classes |= PKM_KACS_NT_READ;
	if (mode & FMODE_WRITE)
		classes |= PKM_KACS_NT_WRITE;
	return classes;
}

struct pkm_kacs_nt_state *pkm_kacs_nt_state(struct inode *inode, bool create)
{
	struct pkm_kacs_inode_security *sec;
	struct pkm_kacs_nt_state *state;
	struct pkm_kacs_nt_state *raced;

	if (!inode || !inode->i_security)
		return NULL;

	sec = pkm_kacs_inode(inode);
	state = READ_ONCE(sec->nt);
	if (state || !create)
		return state;

	state = kzalloc(sizeof(*state), GFP_KERNEL);
	if (!state)
		return NULL;
	spin_lock_init(&state->lock);
	INIT_LIST_HEAD(&state->locks);
	INIT_LIST_HEAD(&state->lock_waiters);
	init_waitqueue_head(&state->lock_wq);
	INIT_LIST_HEAD(&state->leases);
	init_waitqueue_head(&state->lease_wq);

	raced = cmpxchg(&sec->nt, NULL, state);
	if (raced) {
		kfree(state);
		return raced;
	}
	return state;
}

void pkm_kacs_nt_inode_free(struct pkm_kacs_nt_state *state)
{
	if (!state)
		return;
	/* An open holds its inode, and every lock belongs to an open. */
	WARN_ON_ONCE(state->opens || !list_empty(&state->locks) ||
		     !list_empty(&state->leases) || state->delete_token);
	kfree(state);
}

bool pkm_kacs_nt_stacked(const struct inode *inode)
{
	if (!inode || !inode->i_sb)
		return false;
	return inode->i_sb->s_magic == STRATAFS_SUPER_MAGIC ||
	       inode->i_sb->s_magic == OVERLAYFS_SUPER_MAGIC;
}

bool pkm_kacs_nt_applies(const struct inode *inode)
{
	if (!inode || !inode->i_security || !inode->i_sb)
		return false;
	if (!S_ISREG(inode->i_mode) && !S_ISDIR(inode->i_mode))
		return false;
	return pkm_kacs_mount_policy_is_managed(
		pkm_kacs_superblock_mount_policy(inode->i_sb));
}

struct inode *pkm_kacs_nt_record_inode_for_file(struct file *file)
{
	struct inode *inode;

	if (!file)
		return NULL;
	inode = file_inode(file);
	if (!inode)
		return NULL;
#if IS_ENABLED(CONFIG_STRATAFS_FS)
	if (inode->i_sb->s_magic == STRATAFS_SUPER_MAGIC) {
		if (!S_ISDIR(inode->i_mode))
			return stratafs_kacs_nt_inode_for_file(file);
		/* A directory's open holds the provider it registered on. */
		if (file->f_security && pkm_kacs_file(file)->nt_inode) {
			inode = pkm_kacs_file(file)->nt_inode;
			ihold(inode);
			return inode;
		}
		return pkm_kacs_nt_record_inode_for_dentry(file->f_path.dentry);
	}
#endif
	if (inode->i_sb->s_magic == OVERLAYFS_SUPER_MAGIC)
		inode = d_real_inode(file_dentry(file));
	if (!pkm_kacs_nt_applies(inode))
		return NULL;
	ihold(inode);
	return inode;
}

struct inode *pkm_kacs_nt_record_inode_for_dentry(struct dentry *dentry)
{
	struct inode *inode;

	if (!dentry || !d_really_is_positive(dentry))
		return NULL;
	inode = d_inode(dentry);
#if IS_ENABLED(CONFIG_STRATAFS_FS)
	if (inode->i_sb->s_magic == STRATAFS_SUPER_MAGIC)
		return stratafs_kacs_nt_inode_for_dentry(dentry);
#endif
	if (inode->i_sb->s_magic == OVERLAYFS_SUPER_MAGIC)
		inode = d_real_inode(dentry);
	if (!pkm_kacs_nt_applies(inode))
		return NULL;
	ihold(inode);
	return inode;
}

void pkm_kacs_nt_note_status(u32 status)
{
	if (current && current->security)
		pkm_kacs_task(current)->nt_open_status = status;
}

u32 pkm_kacs_nt_take_status(void)
{
	struct pkm_kacs_task_security *task_sec;
	u32 status;

	if (!current || !current->security)
		return 0;
	task_sec = pkm_kacs_task(current);
	status = task_sec->nt_open_status;
	task_sec->nt_open_status = 0;
	return status;
}

/*
 * MS-FSA 2.1.5.1.2.2: each existing participant's share mode against the
 * new open's access, and the new open's share mode against each existing
 * participant's access. Called only for a new open that takes part.
 */
static bool pkm_kacs_nt_conflicts(const struct pkm_kacs_nt_state *state,
				  u32 classes, u32 share, u32 overrides)
{
	unsigned int k;

	for (k = 0; k < 3; k++) {
		u32 bit = 1U << k;
		bool overridden =
			(k == 0 && (overrides & PKM_KACS_NT_OVERRIDE_READ)) ||
			(k != 0 &&
			 (overrides & PKM_KACS_NT_OVERRIDE_WRITE_DELETE));

		if ((classes & bit) && state->denying[k] && !overridden)
			return true;
		if (!(share & bit) && state->holding[k])
			return true;
	}
	return false;
}

int pkm_kacs_nt_register(struct file *file, struct inode *inode, u32 classes,
			 u32 share, u32 overrides)
{
	struct pkm_kacs_file_security *sec;
	struct pkm_kacs_nt_state *state;
	u32 status = 0;
	unsigned int k;
	int ret = 0;

	if (!file || !file->f_security || !inode)
		return -EACCES;
	sec = pkm_kacs_file(file);
	if (WARN_ON_ONCE(sec->nt_inode))
		return -EINVAL;

	state = pkm_kacs_nt_state(inode, true);
	if (!state)
		return -ENOMEM;

	share &= PKM_KACS_NT_ALL;
	spin_lock(&state->lock);
	if (state->delete_pending || state->deleting) {
		status = KACS_STATUS_DELETE_PENDING;
		ret = -EBUSY;
	} else if (classes &&
		   pkm_kacs_nt_conflicts(state, classes, share, overrides)) {
		status = KACS_STATUS_SHARING_VIOLATION;
		ret = -EBUSY;
	} else {
		state->opens++;
		for (k = 0; classes && k < 3; k++) {
			if (classes & (1U << k))
				state->holding[k]++;
			if (!(share & (1U << k)))
				state->denying[k]++;
		}
		sec->nt_inode = inode;
		sec->nt_classes = classes;
		sec->nt_share = share;
	}
	spin_unlock(&state->lock);

	if (ret)
		pkm_kacs_nt_note_status(status);
	return ret;
}

struct pkm_kacs_nt_removal {
	struct path path;
	const struct inode *dentry_inode;
	struct inode *record_inode;
	const void *token;
	/* A StrataFS directory's provider reference, dropped once done. */
	struct inode *held_inode;
};

/*
 * Take the open off its inode's counts. If it was the last open of a
 * delete-pending file, hand the caller the removal to carry out, with the
 * state left deleting so that no open slips in meanwhile.
 */
static bool pkm_kacs_nt_unregister(struct file *file,
				   struct pkm_kacs_nt_removal *removal)
{
	struct pkm_kacs_file_security *sec = pkm_kacs_file(file);
	struct pkm_kacs_nt_state *state;
	struct inode *inode = sec->nt_inode;
	bool remove = false;
	unsigned int k;

	if (!inode)
		return false;
	state = pkm_kacs_nt_state(inode, false);
	sec->nt_inode = NULL;
	if (sec->nt_inode_held) {
		removal->held_inode = inode;
		sec->nt_inode_held = 0;
	}
	if (WARN_ON_ONCE(!state))
		return false;

	spin_lock(&state->lock);
	if (!WARN_ON_ONCE(state->opens == 0))
		state->opens--;
	for (k = 0; sec->nt_classes && k < 3; k++) {
		if (sec->nt_classes & (1U << k))
			state->holding[k]--;
		if (!(sec->nt_share & (1U << k)))
			state->denying[k]--;
	}
	if (state->opens == 0 && state->delete_pending && !state->deleting) {
		removal->path = state->delete_path;
		removal->dentry_inode = state->delete_dentry_inode;
		removal->record_inode = inode;
		removal->token = state->delete_token;
		state->delete_path = (struct path){};
		state->delete_dentry_inode = NULL;
		state->delete_token = NULL;
		state->delete_pending = false;
		state->deleting = true;
		remove = true;
	}
	spin_unlock(&state->lock);
	return remove;
}

static void pkm_kacs_nt_finish_removal(struct pkm_kacs_nt_removal *removal)
{
	struct pkm_kacs_nt_state *state;
	long ret;

	ret = pkm_kacs_nt_remove_now(&removal->path, removal->dentry_inode,
				     removal->record_inode, removal->token);
	trace_kacs_object(removal->record_inode,
			  KACS_OBJ_DELETE_ON_CLOSE_UNLINK, ret);
	if (ret && ret != -ENOENT)
		pr_warn("pkm: delete-pending removal failed (%ld)\n", ret);

	state = pkm_kacs_nt_state(removal->record_inode, false);
	if (state) {
		spin_lock(&state->lock);
		state->deleting = false;
		spin_unlock(&state->lock);
	}
	path_put(&removal->path);
	if (removal->token)
		kacs_rust_token_drop(removal->token);
}

/* Carry out what unregistering left: the removal, then the held provider. */
static void pkm_kacs_nt_settle(struct pkm_kacs_nt_removal *removal, bool remove)
{
	if (remove)
		pkm_kacs_nt_finish_removal(removal);
	if (removal->held_inode)
		iput(removal->held_inode);
}

/* An open with delete-on-close marks its file as it closes. */
static void pkm_kacs_nt_close_marks(struct file *file)
{
	struct pkm_kacs_file_security *sec = pkm_kacs_file(file);
	struct inode *record;

	if (!sec->delete_on_close)
		goto out_token;
#ifdef CONFIG_SECURITY_PKM_KUNIT
	/*
	 * KUnit's file fixtures have fake mounts and dentries that a real
	 * removal cannot touch: they count it instead, as the deferred
	 * deletion they stand for would remove the name.
	 */
	if (file_inode(file) && file_inode(file)->i_security &&
	    pkm_kacs_inode(file_inode(file))->kunit_fake_xattr_enabled) {
		pkm_kacs_inode(file_inode(file))->kunit_unlink_calls++;
		sec->delete_on_close = 0;
		goto out_token;
	}
#endif
	record = pkm_kacs_nt_record_inode_for_file(file);
	if (record) {
		(void)pkm_kacs_nt_mark_delete_pending(
			record, &file->f_path, sec->delete_on_close_token);
		iput(record);
	}
	sec->delete_on_close = 0;
out_token:
	if (sec->delete_on_close_token) {
		kacs_rust_token_drop(sec->delete_on_close_token);
		sec->delete_on_close_token = NULL;
	}
}

void pkm_kacs_nt_release(struct file *file)
{
	struct pkm_kacs_nt_removal removal = {};

	if (!file || !file->f_security)
		return;
	pkm_kacs_nt_close_marks(file);
	pkm_kacs_nt_locks_release(file);
	pkm_kacs_lease_release_file(file);
	pkm_kacs_pin_release(file);
	pkm_kacs_nt_settle(&removal, pkm_kacs_nt_unregister(file, &removal));
}

void pkm_kacs_nt_open_failed(struct file *file)
{
	struct pkm_kacs_file_security *sec;
	struct pkm_kacs_nt_removal removal = {};

	if (!file || !file->f_security)
		return;
	sec = pkm_kacs_file(file);
	/* A failed open never closes, so it never marks its file. */
	sec->delete_on_close = 0;
	if (sec->delete_on_close_token) {
		kacs_rust_token_drop(sec->delete_on_close_token);
		sec->delete_on_close_token = NULL;
	}
	pkm_kacs_nt_settle(&removal, pkm_kacs_nt_unregister(file, &removal));
}

struct pkm_kacs_nt_removal_work {
	struct work_struct work;
	struct pkm_kacs_nt_removal removal;
	bool remove;
};

static void pkm_kacs_nt_removal_workfn(struct work_struct *work)
{
	struct pkm_kacs_nt_removal_work *w =
		container_of(work, struct pkm_kacs_nt_removal_work, work);

	pkm_kacs_nt_settle(&w->removal, w->remove);
	kfree(w);
}

void pkm_kacs_nt_free(struct file *file)
{
	struct pkm_kacs_nt_removal_work *w;
	struct pkm_kacs_nt_removal removal = {};
	bool remove;

	if (!file || !file->f_security || !pkm_kacs_file(file)->nt_inode)
		return;
	/*
	 * Every path that registers an open also unregisters it, at close or
	 * at the failed open's cleanup. Reaching here registered is a bug, but
	 * a leaked registration would refuse every later open of the file.
	 */
	WARN_ONCE(1, "pkm: NT registration reached file_free_security\n");
	remove = pkm_kacs_nt_unregister(file, &removal);
	if (!remove && !removal.held_inode)
		return;
	/* Neither the removal nor a final iput may run here. */
	w = kmalloc(sizeof(*w), GFP_ATOMIC);
	if (!w) {
		pr_warn("pkm: delete-pending removal lost\n");
		return;
	}
	w->removal = removal;
	w->remove = remove;
	INIT_WORK(&w->work, pkm_kacs_nt_removal_workfn);
	schedule_work(&w->work);
}

int pkm_kacs_nt_check_not_pending(struct inode *record_inode)
{
	struct pkm_kacs_nt_state *state;
	int ret = 0;

	state = pkm_kacs_nt_state(record_inode, false);
	if (!state)
		return 0;
	spin_lock(&state->lock);
	if (state->delete_pending || state->deleting)
		ret = -EBUSY;
	spin_unlock(&state->lock);
	return ret;
}

int pkm_kacs_nt_check_delete_by_name(struct inode *record_inode)
{
	struct pkm_kacs_nt_state *state;
	int ret = 0;

	state = pkm_kacs_nt_state(record_inode, false);
	if (!state)
		return 0;
	spin_lock(&state->lock);
	if (state->delete_pending || state->deleting || state->denying[2] != 0)
		ret = -EBUSY;
	spin_unlock(&state->lock);
	return ret;
}

bool pkm_kacs_nt_delete_pending(struct inode *record_inode)
{
	struct pkm_kacs_nt_state *state;
	bool pending;

	state = pkm_kacs_nt_state(record_inode, false);
	if (!state)
		return false;
	spin_lock(&state->lock);
	pending = state->delete_pending;
	spin_unlock(&state->lock);
	return pending;
}

int pkm_kacs_nt_mark_delete_pending(struct inode *record_inode,
				    const struct path *path,
				    const void *subject_token)
{
	struct pkm_kacs_nt_state *state;
	struct pkm_kacs_nt_removal removal = {};
	bool remove = false;

	if (!record_inode || !path || !path->dentry)
		return -EINVAL;
	state = pkm_kacs_nt_state(record_inode, true);
	if (!state)
		return -ENOMEM;

	spin_lock(&state->lock);
	if (state->deleting) {
		spin_unlock(&state->lock);
		return 0;
	}
	if (!state->delete_pending) {
		path_get(path);
		state->delete_path = *path;
		state->delete_dentry_inode = d_inode(path->dentry);
		state->delete_token =
			subject_token ? kacs_rust_token_clone(subject_token) :
					NULL;
		state->delete_pending = true;
	}
	/* No open remains to close: nothing will remove it but this. */
	if (state->opens == 0) {
		removal.path = state->delete_path;
		removal.dentry_inode = state->delete_dentry_inode;
		removal.record_inode = record_inode;
		removal.token = state->delete_token;
		state->delete_path = (struct path){};
		state->delete_dentry_inode = NULL;
		state->delete_token = NULL;
		state->delete_pending = false;
		state->deleting = true;
		remove = true;
	}
	spin_unlock(&state->lock);

	if (remove)
		pkm_kacs_nt_finish_removal(&removal);
	return 0;
}

void pkm_kacs_nt_clear_delete_pending(struct inode *record_inode)
{
	struct pkm_kacs_nt_state *state;
	struct path path = {};
	const void *token = NULL;

	state = pkm_kacs_nt_state(record_inode, false);
	if (!state)
		return;
	spin_lock(&state->lock);
	if (state->delete_pending) {
		path = state->delete_path;
		token = state->delete_token;
		state->delete_path = (struct path){};
		state->delete_dentry_inode = NULL;
		state->delete_token = NULL;
		state->delete_pending = false;
	}
	spin_unlock(&state->lock);
	if (path.dentry)
		path_put(&path);
	if (token)
		kacs_rust_token_drop(token);
}

bool pkm_kacs_nt_deferred_delete_matches(const struct inode *dir,
					 const struct dentry *dentry)
{
	struct pkm_kacs_task_security *task_sec;

	if (!dir || !dentry || !current || !current->security)
		return false;
	task_sec = pkm_kacs_task(current);
	if (!task_sec->deferred_delete_dentry)
		return false;
	/* Only from the directory the entry is in. */
	if (!dentry->d_parent || d_inode(dentry->d_parent) != dir)
		return false;
	if (dentry == task_sec->deferred_delete_dentry &&
	    d_inode(dentry) == task_sec->deferred_delete_dentry_inode)
		return true;
	/* The provider entry below a stacking filesystem's name. */
	return d_inode(dentry) &&
	       d_inode(dentry) == task_sec->deferred_delete_record_inode;
}

long pkm_kacs_nt_remove_now(const struct path *path,
			    const struct inode *dentry_inode,
			    struct inode *record_inode, const void *token)
{
	struct pkm_kacs_task_security *task_sec;
	struct path parent = {};
	struct inode *parent_inode;
	struct dentry *dentry;
	bool directory;
	int attempt;
	long ret;

	if (!path || !path->dentry || !path->mnt || !dentry_inode)
		return -EINVAL;
	if (!current || !current->security)
		return -EACCES;
	task_sec = pkm_kacs_task(current);
	if (task_sec->deferred_delete_dentry)
		return -EBUSY;

	/*
	 * Hold the dentry as a pathname unlink's lookup does. The caller's
	 * reference may be the only other one -- an open file's, still in
	 * use for a POSIX-semantics delete -- and d_delete() turns a dentry
	 * nobody else holds negative under it, rather than unhashing it.
	 */
	dentry = dget(path->dentry);
	directory = S_ISDIR(dentry_inode->i_mode);
	ret = mnt_want_write(path->mnt);
	if (ret) {
		dput(dentry);
		return ret;
	}

	for (attempt = 0; attempt < 8; attempt++) {
		parent.mnt = path->mnt;
		parent.dentry = dget_parent(dentry);
		parent_inode = d_inode(parent.dentry);
		inode_lock_nested(parent_inode, I_MUTEX_PARENT);
		if (dentry->d_parent == parent.dentry)
			break;
		/* Renamed between finding the parent and locking it. */
		inode_unlock(parent_inode);
		dput(parent.dentry);
		parent.dentry = NULL;
	}
	if (!parent.dentry) {
		ret = -EBUSY;
		goto out_write;
	}

	/*
	 * The name may already be gone. An unlink by someone else while the
	 * file was open leaves this dentry unhashed (and negative once the
	 * last reference goes), and a name re-created since names another
	 * inode. Either way the deletion promised has happened or been
	 * overtaken, so the last close is a no-op rather than a second unlink
	 * of the same entry -- which on tmpfs drops the pin shmem_link took a
	 * second time and frees the dentry under us (PEI-694).
	 *
	 * StrataFS is the exception to the unhashed test: it drops a merged
	 * entry on copy-up by design, so its dentries are routinely unhashed
	 * while very much alive, and its own unlink looks the provider entry
	 * up afresh and tolerates ENOENT for a deferred deletion.
	 */
	if (!d_is_positive(dentry) || d_inode(dentry) != dentry_inode ||
	    (d_unhashed(dentry) &&
	     dentry->d_sb->s_magic != STRATAFS_SUPER_MAGIC)) {
		ret = 0;
		goto out_unlock;
	}

	task_sec->deferred_delete_dentry = dentry;
	task_sec->deferred_delete_dentry_inode = dentry_inode;
	task_sec->deferred_delete_record_inode = record_inode;
	task_sec->deferred_delete_token = token;
	task_sec->delete_on_close_stratafs_entered = false;
	pkm_kacs_lease_note_vfs_break(parent_inode, KACS_LEASE_BREAK_CHILD);
	pkm_kacs_lease_note_vfs_break((struct inode *)dentry_inode,
				      KACS_LEASE_BREAK_DELETE);
	if (directory)
		ret = vfs_rmdir(mnt_idmap(parent.mnt), parent_inode, dentry,
				NULL);
	else
		ret = vfs_unlink(mnt_idmap(parent.mnt), parent_inode, dentry,
				 NULL);
#if IS_ENABLED(CONFIG_STRATAFS_FS)
	/*
	 * A refused deferred deletion is audited on any non-zero result.
	 * StrataFS audits every refusal its own unlink raises, but
	 * may_delete() checks the merged parent before ->unlink is entered,
	 * and a refusal there would otherwise leave no record (PEI-588).
	 */
	if (ret && dentry->d_sb->s_magic == STRATAFS_SUPER_MAGIC &&
	    !task_sec->delete_on_close_stratafs_entered) {
		if ((ret == -ENOENT || ret == -ENOTDIR) &&
		    stratafs_kacs_deferred_target_gone(dentry))
			ret = 0;
		if (ret)
			stratafs_kacs_audit_deferred_refusal(dentry, (int)ret);
	}
#endif
	task_sec->deferred_delete_dentry = NULL;
	task_sec->deferred_delete_dentry_inode = NULL;
	task_sec->deferred_delete_record_inode = NULL;
	task_sec->deferred_delete_token = NULL;
out_unlock:
	inode_unlock(parent_inode);
	dput(parent.dentry);
out_write:
	mnt_drop_write(path->mnt);
	dput(dentry);
	return ret;
}

#ifdef CONFIG_SECURITY_PKM_KUNIT
#include <kunit/test.h>

#include "object_lifecycle.h"

/* A bare inode and files with just the KACS blobs registration uses. */
struct pkm_kunit_nt_fixture {
	struct inode inode;
	struct file files[3];
};

static struct pkm_kunit_nt_fixture *pkm_kunit_nt_fixture(struct kunit *test)
{
	struct pkm_kunit_nt_fixture *f;
	int i;

	f = kunit_kzalloc(test, sizeof(*f), GFP_KERNEL);
	KUNIT_ASSERT_NOT_NULL(test, f);
	f->inode.i_mode = S_IFREG | 0600;
	f->inode.i_security =
		kunit_kzalloc(test,
			      pkm_blob_sizes.lbs_inode +
				      sizeof(struct pkm_kacs_inode_security),
			      GFP_KERNEL);
	KUNIT_ASSERT_NOT_NULL(test, f->inode.i_security);
	KUNIT_ASSERT_EQ(test, pkm_kacs_inode_alloc_security(&f->inode), 0);
	for (i = 0; i < ARRAY_SIZE(f->files); i++) {
		f->files[i].f_security = kunit_kzalloc(
			test,
			pkm_blob_sizes.lbs_file +
				sizeof(struct pkm_kacs_file_security),
			GFP_KERNEL);
		KUNIT_ASSERT_NOT_NULL(test, f->files[i].f_security);
	}
	return f;
}

static void pkm_kunit_nt_fixture_exit(struct pkm_kunit_nt_fixture *f)
{
	int i;

	for (i = 0; i < ARRAY_SIZE(f->files); i++)
		pkm_kacs_nt_open_failed(&f->files[i]);
	pkm_kacs_nt_inode_free(pkm_kacs_inode(&f->inode)->nt);
	pkm_kacs_inode(&f->inode)->nt = NULL;
}

/* MS-FSA 2.1.5.1.2.2: each open's share mode against the other's access. */
static void pkm_kunit_nt_share_conflicts_both_ways(struct kunit *test)
{
	struct pkm_kunit_nt_fixture *f = pkm_kunit_nt_fixture(test);

	/* A reader that denies writing. */
	KUNIT_ASSERT_EQ(
		test,
		pkm_kacs_nt_register(&f->files[0], &f->inode, PKM_KACS_NT_READ,
				     PKM_KACS_NT_READ | PKM_KACS_NT_DELETE, 0),
		0);
	/* A writer is refused, with the sharing-violation status. */
	KUNIT_EXPECT_EQ(test,
			pkm_kacs_nt_register(&f->files[1], &f->inode,
					     PKM_KACS_NT_WRITE, PKM_KACS_NT_ALL,
					     0),
			-EBUSY);
	KUNIT_EXPECT_EQ(test, pkm_kacs_nt_take_status(),
			KACS_STATUS_SHARING_VIOLATION);
	/* Another reader sharing everything is admitted. */
	KUNIT_EXPECT_EQ(test,
			pkm_kacs_nt_register(&f->files[1], &f->inode,
					     PKM_KACS_NT_READ, PKM_KACS_NT_ALL,
					     0),
			0);
	/* A reader that denies reading conflicts with the readers present. */
	KUNIT_EXPECT_EQ(
		test,
		pkm_kacs_nt_register(&f->files[2], &f->inode, PKM_KACS_NT_READ,
				     PKM_KACS_NT_WRITE | PKM_KACS_NT_DELETE, 0),
		-EBUSY);
	pkm_kunit_nt_fixture_exit(f);
}

/* An open holding no share class takes no part (MS-FSA 2.1.5.1.2.2). */
static void pkm_kunit_nt_attribute_only_open_never_conflicts(struct kunit *test)
{
	struct pkm_kunit_nt_fixture *f = pkm_kunit_nt_fixture(test);

	KUNIT_ASSERT_EQ(test,
			pkm_kacs_nt_register(
				&f->files[0], &f->inode,
				PKM_KACS_NT_READ | PKM_KACS_NT_WRITE, 0, 0),
			0);
	KUNIT_EXPECT_EQ(test,
			pkm_kacs_nt_register(&f->files[1], &f->inode, 0, 0, 0),
			0);
	KUNIT_EXPECT_EQ(test, pkm_kacs_nt_state(&f->inode, false)->opens, 2U);
	pkm_kunit_nt_fixture_exit(f);
}

/* Restore intent sets other opens' denial of write and delete aside. */
static void pkm_kunit_nt_restore_override(struct kunit *test)
{
	struct pkm_kunit_nt_fixture *f = pkm_kunit_nt_fixture(test);

	KUNIT_ASSERT_EQ(test,
			pkm_kacs_nt_register(&f->files[0], &f->inode,
					     PKM_KACS_NT_READ, PKM_KACS_NT_READ,
					     0),
			0);
	KUNIT_EXPECT_EQ(test,
			pkm_kacs_nt_register(&f->files[1], &f->inode,
					     PKM_KACS_NT_WRITE |
						     PKM_KACS_NT_DELETE,
					     PKM_KACS_NT_ALL,
					     PKM_KACS_NT_OVERRIDE_WRITE_DELETE),
			0);
	/* Backup's override does not cover writing. */
	KUNIT_EXPECT_EQ(test,
			pkm_kacs_nt_register(&f->files[2], &f->inode,
					     PKM_KACS_NT_WRITE, PKM_KACS_NT_ALL,
					     PKM_KACS_NT_OVERRIDE_READ),
			-EBUSY);
	pkm_kunit_nt_fixture_exit(f);
}

/* Deleting by name is refused while an open does not share delete. */
static void pkm_kunit_nt_delete_by_name_needs_share_delete(struct kunit *test)
{
	struct pkm_kunit_nt_fixture *f = pkm_kunit_nt_fixture(test);

	KUNIT_ASSERT_EQ(
		test,
		pkm_kacs_nt_register(&f->files[0], &f->inode, PKM_KACS_NT_READ,
				     PKM_KACS_NT_READ | PKM_KACS_NT_WRITE, 0),
		0);
	KUNIT_EXPECT_EQ(test, pkm_kacs_nt_check_delete_by_name(&f->inode),
			-EBUSY);
	pkm_kacs_nt_open_failed(&f->files[0]);
	KUNIT_EXPECT_EQ(test, pkm_kacs_nt_check_delete_by_name(&f->inode), 0);
	pkm_kunit_nt_fixture_exit(f);
}

/* A delete-pending file admits no open, whatever it asks. */
static void pkm_kunit_nt_delete_pending_refuses_opens(struct kunit *test)
{
	struct pkm_kunit_nt_fixture *f = pkm_kunit_nt_fixture(test);
	struct pkm_kacs_nt_state *state;

	KUNIT_ASSERT_EQ(test,
			pkm_kacs_nt_register(&f->files[0], &f->inode,
					     PKM_KACS_NT_DELETE,
					     PKM_KACS_NT_ALL, 0),
			0);
	state = pkm_kacs_nt_state(&f->inode, false);
	state->delete_pending = true;
	KUNIT_EXPECT_EQ(test,
			pkm_kacs_nt_register(&f->files[1], &f->inode, 0, 0, 0),
			-EBUSY);
	KUNIT_EXPECT_EQ(test, pkm_kacs_nt_take_status(),
			KACS_STATUS_DELETE_PENDING);
	KUNIT_EXPECT_EQ(test, pkm_kacs_nt_check_delete_by_name(&f->inode),
			-EBUSY);
	/* Cleared without a path, so the last close removes nothing. */
	state->delete_pending = false;
	pkm_kunit_nt_fixture_exit(f);
}

static struct kunit_case pkm_kunit_nt_share_cases[] = {
	KUNIT_CASE(pkm_kunit_nt_share_conflicts_both_ways),
	KUNIT_CASE(pkm_kunit_nt_attribute_only_open_never_conflicts),
	KUNIT_CASE(pkm_kunit_nt_restore_override),
	KUNIT_CASE(pkm_kunit_nt_delete_by_name_needs_share_delete),
	KUNIT_CASE(pkm_kunit_nt_delete_pending_refuses_opens),
	{}
};

static struct kunit_suite pkm_kunit_nt_share_suite = {
	.name = "pkm_kunit_nt_share",
	.test_cases = pkm_kunit_nt_share_cases,
};

kunit_test_suite(pkm_kunit_nt_share_suite);
#endif
