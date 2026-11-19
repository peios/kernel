// SPDX-License-Identifier: GPL-2.0-only
/*
 * NT caching leases (TRM "Leases").
 *
 * A lease manager is a file descriptor whose reads return break notices.
 * A lease belongs to one open of a file, made under the manager's key, and
 * sits in the file's NT state with its R/H/W bits. Breaking a lease lowers
 * it to what the breaking operation can live with: at once, with a notice,
 * when only read caching goes; otherwise once the holder acknowledges, or
 * the manager's break timeout passes.
 *
 * Each lease with a state also carries one delegation-style fs/locks.c
 * entry, its proxy, on the open it belongs to. The VFS breaks delegations
 * before unlink, rename, link, setattr and setxattr, with try_break_deleg()
 * under its locks and break_deleg_wait() after dropping them. The proxy's
 * lm_breaker_owns_lease() is where KACS decides, from what its own hook
 * noted just before, whether that operation breaks the NT lease; if so the
 * VFS waits on the proxy until KACS wakes it. Everything else KACS breaks
 * directly, from places that hold no lock.
 *
 * Locking: fs/locks.c's flc_lock is taken before the NT state's lock, and
 * the NT state's lock before the manager's. A lease's mutex serializes its
 * proxy with the release of the open it belongs to, so the open is never
 * freed while KACS removes the proxy from it.
 */

#include <linux/anon_inodes.h>
#include <linux/file.h>
#include <linux/filelock.h>
#include <linux/fs.h>
#include <linux/kacs_stratafs.h>
#include <linux/kref.h>
#include <linux/mutex.h>
#include <linux/poll.h>
#include <linux/sched/signal.h>
#include <linux/slab.h>
#include <linux/syscalls.h>
#include <linux/uaccess.h>
#include <linux/wait.h>
#include <linux/workqueue.h>

#include <pkm/file.h>
#include <pkm/sd.h>

#include "lsm_internal.h"
#include "nt_file.h"
#include "nt_lease.h"

#define PKM_KACS_LEASE_ALL \
	(KACS_LEASE_READ | KACS_LEASE_HANDLE | KACS_LEASE_WRITE)
#define PKM_KACS_LEASE_MAX_TIMEOUT_MS 35000U

struct pkm_kacs_lease_manager {
	struct kref ref;
	spinlock_t lock;
	/* Leases with a notice queued, and every lease. */
	struct list_head notices;
	struct list_head leases;
	wait_queue_head_t wq;
	unsigned long timeout;
};

struct pkm_kacs_nt_lease {
	struct kref ref;
	struct mutex lock;
	/* On the NT state's leases, under its lock. */
	struct list_head inode_node;
	/* On the manager's leases and notices, under its lock. */
	struct list_head mgr_node;
	struct list_head notice_node;
	struct pkm_kacs_lease_manager *mgr;
	struct inode *inode;
	/* The open the lease belongs to; valid until released. */
	struct file *file;
	u8 key[16];
	/* Under the NT state's lock. */
	u32 state;
	u32 breaking_to;
	bool breaking;
	bool released;
	bool has_proxy;
	/* The notice to deliver, under the manager's lock. */
	struct kacs_lease_break notice;
	struct delayed_work timeout_work;
};

static const struct file_operations pkm_kacs_lease_manager_fops;

static void pkm_kacs_lease_manager_free(struct kref *ref)
{
	kfree(container_of(ref, struct pkm_kacs_lease_manager, ref));
}

static void pkm_kacs_lease_manager_put(struct pkm_kacs_lease_manager *mgr)
{
	if (mgr)
		kref_put(&mgr->ref, pkm_kacs_lease_manager_free);
}

static void pkm_kacs_lease_free(struct kref *ref)
{
	struct pkm_kacs_nt_lease *lease =
		container_of(ref, struct pkm_kacs_nt_lease, ref);

	iput(lease->inode);
	pkm_kacs_lease_manager_put(lease->mgr);
	kfree(lease);
}

static void pkm_kacs_lease_put(struct pkm_kacs_nt_lease *lease)
{
	kref_put(&lease->ref, pkm_kacs_lease_free);
}

/* A lease manager descriptor's manager, referenced, or NULL. */
static struct pkm_kacs_lease_manager *pkm_kacs_lease_manager_get(int fd)
{
	struct pkm_kacs_lease_manager *mgr = NULL;

	CLASS(fd, f)(fd);
	if (fd_empty(f) || fd_file(f)->f_op != &pkm_kacs_lease_manager_fops)
		return NULL;
	mgr = fd_file(f)->private_data;
	kref_get(&mgr->ref);
	return mgr;
}

static bool pkm_kacs_lease_key_matches(const struct pkm_kacs_nt_lease *lease,
				       const struct pkm_kacs_lease_manager *mgr,
				       const u8 *key)
{
	return mgr && lease->mgr == mgr &&
	       !memcmp(lease->key, key, sizeof(lease->key));
}

/* The state a lease falls to when @reason breaks it. */
static u32 pkm_kacs_lease_target(u32 state, u32 reason)
{
	switch (reason) {
	case KACS_LEASE_BREAK_OPEN:
		return state & ~KACS_LEASE_WRITE;
	case KACS_LEASE_BREAK_SHARING:
	case KACS_LEASE_BREAK_NAMESPACE:
	case KACS_LEASE_BREAK_DELETE:
	case KACS_LEASE_BREAK_SECURITY:
		return state & ~KACS_LEASE_HANDLE;
	case KACS_LEASE_BREAK_WRITE:
	case KACS_LEASE_BREAK_SIZE:
	case KACS_LEASE_BREAK_LOCK:
	case KACS_LEASE_BREAK_ATTRIBUTES:
	case KACS_LEASE_BREAK_CHILD:
		/* Handle and write caching need read caching. */
		return (state & KACS_LEASE_READ) ? 0 : state;
	default:
		/* An operation KACS did not see coming. */
		return state & ~(KACS_LEASE_WRITE | KACS_LEASE_HANDLE);
	}
}

/*
 * A break the operation waits for: one that takes handle or write caching,
 * which the holder has to act on, for an operation that waits for breaks
 * at all. Changes of contents only notify (TRM "What breaks a lease").
 */
static bool pkm_kacs_lease_break_waits(u32 from, u32 to, u32 reason)
{
	switch (reason) {
	case KACS_LEASE_BREAK_WRITE:
	case KACS_LEASE_BREAK_SIZE:
	case KACS_LEASE_BREAK_LOCK:
	case KACS_LEASE_BREAK_ATTRIBUTES:
	case KACS_LEASE_BREAK_CHILD:
		return false;
	default:
		return ((from & ~to) &
			(KACS_LEASE_HANDLE | KACS_LEASE_WRITE)) != 0;
	}
}

/* Queue a notice for @lease; called under the NT state's lock. */
static void pkm_kacs_lease_queue_notice(struct pkm_kacs_nt_lease *lease,
					u32 from, u32 to, u32 reason)
{
	struct pkm_kacs_lease_manager *mgr = lease->mgr;

	spin_lock(&mgr->lock);
	memcpy(lease->notice.lease_key, lease->key, sizeof(lease->key));
	lease->notice.dev = lease->inode->i_sb->s_dev;
	lease->notice.ino = lease->inode->i_ino;
	lease->notice.current_state = from;
	lease->notice.new_state = to;
	lease->notice.reason = reason;
	lease->notice.epoch++;
	if (list_empty(&lease->notice_node)) {
		kref_get(&lease->ref);
		list_add_tail(&lease->notice_node, &mgr->notices);
	}
	spin_unlock(&mgr->lock);
	wake_up_interruptible(&mgr->wq);
}

/*
 * Break every lease on @state that @reason affects, except those under
 * the breaker's own key. Called under the NT state's lock. Returns how
 * many were broken; *waits says whether one must be acknowledged.
 */
static int pkm_kacs_lease_break_scan(struct pkm_kacs_nt_state *state,
				     u32 reason,
				     const struct pkm_kacs_lease_manager *mgr,
				     const u8 *key, bool *waits)
{
	struct pkm_kacs_nt_lease *lease;
	int broken = 0;
	u32 from;
	u32 to;

	list_for_each_entry(lease, &state->leases, inode_node) {
		if (lease->released ||
		    pkm_kacs_lease_key_matches(lease, mgr, key))
			continue;
		from = lease->breaking ? lease->breaking_to : lease->state;
		to = pkm_kacs_lease_target(from, reason);
		if (to == from)
			continue;
		broken++;
		if (pkm_kacs_lease_break_waits(from, to, reason)) {
			lease->breaking_to = to;
			if (!lease->breaking) {
				/* The timeout holds a reference while armed. */
				lease->breaking = true;
				kref_get(&lease->ref);
				mod_delayed_work(system_wq,
						 &lease->timeout_work,
						 lease->mgr->timeout);
			}
			if (waits)
				*waits = true;
		} else {
			/* A notice: the lease falls at once. */
			lease->state = to;
			if (lease->breaking)
				lease->breaking_to &= to;
		}
		pkm_kacs_lease_queue_notice(lease, from, to, reason);
	}
	return broken;
}

/* Whether a lease the breaker waits for is still being broken. */
static bool
pkm_kacs_lease_still_breaking(struct pkm_kacs_nt_state *state,
			      const struct pkm_kacs_lease_manager *mgr,
			      const u8 *key)
{
	struct pkm_kacs_nt_lease *lease;
	bool breaking = false;

	spin_lock(&state->lock);
	list_for_each_entry(lease, &state->leases, inode_node) {
		if (!lease->released && lease->breaking &&
		    !pkm_kacs_lease_key_matches(lease, mgr, key)) {
			breaking = true;
			break;
		}
	}
	spin_unlock(&state->lock);
	return breaking;
}

/* The key of the open an operation is made through. */
static void pkm_kacs_lease_file_key(struct file *file,
				    struct pkm_kacs_lease_manager **mgr,
				    const u8 **key)
{
	struct pkm_kacs_task_security *task_sec;

	*mgr = NULL;
	*key = NULL;
	if (file && file->f_security && pkm_kacs_file(file)->lease_mgr) {
		*mgr = pkm_kacs_file(file)->lease_mgr;
		*key = pkm_kacs_file(file)->lease_key;
		return;
	}
	/* An open in progress carries its key in the task. */
	if (current && current->security) {
		task_sec = pkm_kacs_task(current);
		if (task_sec->lease_open_mgr) {
			*mgr = task_sec->lease_open_mgr;
			*key = task_sec->lease_open_key;
		}
	}
}

int pkm_kacs_lease_break_inode(struct inode *record_inode, u32 reason,
			       struct file *file)
{
	struct pkm_kacs_lease_manager *mgr;
	struct pkm_kacs_nt_state *state;
	const u8 *key;
	bool waits = false;
	int broken;
	long ret;

	state = pkm_kacs_nt_state(record_inode, false);
	if (!state || !READ_ONCE(state->nleases))
		return 0;
	pkm_kacs_lease_file_key(file, &mgr, &key);

	spin_lock(&state->lock);
	broken = pkm_kacs_lease_break_scan(state, reason, mgr, key, &waits);
	spin_unlock(&state->lock);
	if (!waits)
		return broken;
	if (file && (file->f_flags & O_NONBLOCK))
		return -EWOULDBLOCK;

	ret = wait_event_interruptible(
		state->lease_wq,
		!pkm_kacs_lease_still_breaking(state, mgr, key));
	return ret ? (int)ret : broken;
}

int pkm_kacs_lease_break_for_sharing(struct file *file,
				     struct inode *record_inode)
{
	return pkm_kacs_lease_break_inode(record_inode,
					  KACS_LEASE_BREAK_SHARING, file);
}

void pkm_kacs_lease_note_write(struct file *file)
{
	struct pkm_kacs_lease_manager *mgr;
	struct pkm_kacs_nt_state *state;
	struct inode *inode;
	const u8 *key;

	if (!file)
		return;
	inode = file_inode(file);
	if (!inode || !inode->i_security || pkm_kacs_nt_stacked(inode))
		return;
	state = pkm_kacs_nt_state(inode, false);
	if (!state || !READ_ONCE(state->nleases))
		return;
	pkm_kacs_lease_file_key(file, &mgr, &key);
	spin_lock(&state->lock);
	(void)pkm_kacs_lease_break_scan(state, KACS_LEASE_BREAK_WRITE, mgr, key,
					NULL);
	spin_unlock(&state->lock);
}

/* Wake operations waiting on a lease's proxy, so they look again. */
static void pkm_kacs_lease_wake_proxy(struct pkm_kacs_nt_lease *lease)
{
	struct file_lock_context *ctx;
	struct file_lease *fl;
	LIST_HEAD(dispose);

	ctx = locks_inode_context(lease->inode);
	if (!ctx)
		return;
	spin_lock(&ctx->flc_lock);
	list_for_each_entry(fl, &ctx->flc_lease, c.flc_list) {
		if (fl->c.flc_owner != lease)
			continue;
		fl->c.flc_flags &= ~(FL_UNLOCK_PENDING | FL_DOWNGRADE_PENDING);
		fl->fl_break_time = 0;
		fl->fl_downgrade_time = 0;
		/* Same type: no change, but blocked breakers are woken. */
		lease_modify(fl, F_RDLCK, &dispose);
	}
	spin_unlock(&ctx->flc_lock);
}

/*
 * A break completes, by acknowledgement or timeout. Returns false if it
 * had already completed. The armed timeout's reference is dropped here,
 * whether this cancels it or is it.
 */
static bool pkm_kacs_lease_complete_break(struct pkm_kacs_nt_lease *lease,
					  u32 state_value, bool timed_out)
{
	struct pkm_kacs_nt_state *state;
	bool was_breaking;

	state = pkm_kacs_nt_state(lease->inode, false);
	if (!state)
		return false;
	spin_lock(&state->lock);
	was_breaking = lease->breaking;
	if (was_breaking) {
		lease->state = state_value & lease->breaking_to;
		lease->breaking = false;
		if (timed_out)
			pkm_kacs_lease_queue_notice(lease, lease->breaking_to,
						    lease->state,
						    KACS_LEASE_BREAK_TIMEOUT);
	}
	spin_unlock(&state->lock);
	if (!was_breaking)
		return false;
	wake_up_all(&state->lease_wq);
	pkm_kacs_lease_wake_proxy(lease);
	if (timed_out || cancel_delayed_work(&lease->timeout_work))
		pkm_kacs_lease_put(lease);
	return true;
}

static void pkm_kacs_lease_timeout_workfn(struct work_struct *work)
{
	struct pkm_kacs_nt_lease *lease = container_of(
		to_delayed_work(work), struct pkm_kacs_nt_lease, timeout_work);

	/* Unacknowledged: the lease falls to the break's target. */
	if (!pkm_kacs_lease_complete_break(lease, PKM_KACS_LEASE_ALL, true))
		pkm_kacs_lease_put(lease);
}

/*
 * The proxy's view of a VFS break (fs/locks.c): whether the operation the
 * current task is performing leaves this lease alone. KACS's hook for the
 * operation noted it, and its inode, just before the VFS broke
 * delegations. A break that must wait is started here; the VFS then waits
 * on the proxy, which KACS wakes when the break completes.
 */
static bool pkm_kacs_lease_breaker_owns_lease(struct file_lease *fl)
{
	struct pkm_kacs_nt_lease *lease = fl->c.flc_owner;
	struct pkm_kacs_task_security *task_sec = NULL;
	struct pkm_kacs_lease_manager *mgr = NULL;
	struct pkm_kacs_nt_state *state;
	const u8 *key = NULL;
	u32 reason = 0;
	bool waits = false;
	u32 from;
	u32 to;
	int i;

	if (!lease || !lease->inode)
		return true;
	state = pkm_kacs_nt_state(lease->inode, false);
	if (!state)
		return true;

	if (current && current->security) {
		task_sec = pkm_kacs_task(current);
		for (i = 0; i < ARRAY_SIZE(task_sec->lease_vfs_inode); i++) {
			if (task_sec->lease_vfs_inode[i] == lease->inode) {
				reason = task_sec->lease_vfs_reason[i];
				break;
			}
		}
		if (task_sec->lease_breaker_mgr) {
			mgr = task_sec->lease_breaker_mgr;
			key = task_sec->lease_breaker_key;
		}
	}
	/* Opens are broken by KACS's open hook, before the VFS looks. */
	if (reason == KACS_LEASE_BREAK_OPEN)
		return true;

	spin_lock(&state->lock);
	if (lease->released || pkm_kacs_lease_key_matches(lease, mgr, key)) {
		spin_unlock(&state->lock);
		return true;
	}
	from = lease->breaking ? lease->breaking_to : lease->state;
	to = pkm_kacs_lease_target(from, reason);
	if (to != from) {
		if (pkm_kacs_lease_break_waits(from, to, reason)) {
			lease->breaking_to = to;
			if (!lease->breaking) {
				/* The timeout holds a reference while armed. */
				lease->breaking = true;
				kref_get(&lease->ref);
				mod_delayed_work(system_wq,
						 &lease->timeout_work,
						 lease->mgr->timeout);
			}
			waits = true;
		} else {
			lease->state = to;
		}
		pkm_kacs_lease_queue_notice(lease, from, to, reason);
	} else if (lease->breaking) {
		waits = true;
	}
	spin_unlock(&state->lock);
	return !waits;
}

/* The break is under way; keep the proxy and have the VFS wait on it. */
static bool pkm_kacs_lease_lm_break(struct file_lease *fl)
{
	struct pkm_kacs_nt_lease *lease = fl->c.flc_owner;

	if (lease && lease->mgr)
		fl->fl_break_time = jiffies + lease->mgr->timeout + HZ;
	return false;
}

static int pkm_kacs_lease_lm_change(struct file_lease *fl, int arg,
				    struct list_head *dispose)
{
	return lease_modify(fl, arg, dispose);
}

/* NT, not Linux, decides who may hold a lease alongside which opens. */
static int pkm_kacs_lease_lm_open_conflict(struct file *file, int arg)
{
	return 0;
}

static const struct lease_manager_operations pkm_kacs_lease_lmops = {
	.lm_break = pkm_kacs_lease_lm_break,
	.lm_change = pkm_kacs_lease_lm_change,
	.lm_breaker_owns_lease = pkm_kacs_lease_breaker_owns_lease,
	.lm_open_conflict = pkm_kacs_lease_lm_open_conflict,
};

static int pkm_kacs_lease_add_proxy(struct pkm_kacs_nt_lease *lease)
{
	struct file_lease *fl;
	int ret;

	fl = locks_alloc_lease();
	if (!fl)
		return -ENOMEM;
	fl->fl_lmops = &pkm_kacs_lease_lmops;
	fl->c.flc_flags = FL_DELEG;
	fl->c.flc_type = F_RDLCK;
	fl->c.flc_owner = lease;
	fl->c.flc_pid = current->tgid;
	fl->c.flc_file = lease->file;
	ret = kernel_setlease(lease->file, F_RDLCK, &fl, NULL);
	if (fl)
		locks_free_lease(fl);
	if (!ret)
		lease->has_proxy = true;
	return ret;
}

/* Release a lease; its mutex is held, and its open is still valid. */
static void pkm_kacs_lease_release_locked(struct pkm_kacs_nt_lease *lease)
{
	struct pkm_kacs_nt_state *state;
	void *owner = lease;
	bool listed = false;

	if (lease->released)
		return;
	if (lease->has_proxy) {
		(void)kernel_setlease(lease->file, F_UNLCK, NULL, &owner);
		lease->has_proxy = false;
	}
	state = pkm_kacs_nt_state(lease->inode, false);
	if (state) {
		spin_lock(&state->lock);
		lease->released = true;
		if (!list_empty(&lease->inode_node)) {
			list_del_init(&lease->inode_node);
			state->nleases--;
			listed = true;
		}
		spin_unlock(&state->lock);
	}
	spin_lock(&lease->mgr->lock);
	list_del_init(&lease->mgr_node);
	if (!list_empty(&lease->notice_node)) {
		list_del_init(&lease->notice_node);
		pkm_kacs_lease_put(lease);
	}
	spin_unlock(&lease->mgr->lock);
	lease->file = NULL;
	if (cancel_delayed_work(&lease->timeout_work))
		pkm_kacs_lease_put(lease);
	if (state) {
		wake_up_all(&state->lease_wq);
	}
	if (listed)
		pkm_kacs_lease_put(lease);
}

void pkm_kacs_lease_release_file(struct file *file)
{
	struct pkm_kacs_nt_lease *lease;
	struct pkm_kacs_nt_lease *found;
	struct pkm_kacs_nt_state *state;
	struct inode *inode;

	if (!file)
		return;
	inode = file_inode(file);
	state = pkm_kacs_nt_state(inode, false);
	if (!state || !READ_ONCE(state->nleases))
		return;
	for (;;) {
		found = NULL;
		spin_lock(&state->lock);
		list_for_each_entry(lease, &state->leases, inode_node) {
			if (lease->file == file && !lease->released) {
				found = lease;
				kref_get(&found->ref);
				break;
			}
		}
		spin_unlock(&state->lock);
		if (!found)
			return;
		mutex_lock(&found->lock);
		/* The open's proxy is gone already: locks_remove_file(). */
		found->has_proxy = false;
		pkm_kacs_lease_release_locked(found);
		mutex_unlock(&found->lock);
		pkm_kacs_lease_put(found);
	}
}

void pkm_kacs_lease_file_free(struct file *file)
{
	struct pkm_kacs_file_security *sec;

	if (!file || !file->f_security)
		return;
	sec = pkm_kacs_file(file);
	pkm_kacs_lease_manager_put(sec->lease_mgr);
	sec->lease_mgr = NULL;
}

int pkm_kacs_lease_prepare_open(const struct kacs_open_how *how)
{
	struct pkm_kacs_task_security *task_sec;
	struct pkm_kacs_lease_manager *mgr;

	if (!(how->flags & KACS_OPEN_LEASE_KEY))
		return 0;
	if (!current->security)
		return -EACCES;
	mgr = pkm_kacs_lease_manager_get(how->lease_fd);
	if (!mgr)
		return -EBADF;
	task_sec = pkm_kacs_task(current);
	pkm_kacs_lease_manager_put(task_sec->lease_open_mgr);
	task_sec->lease_open_mgr = mgr;
	memcpy(task_sec->lease_open_key, how->lease_key,
	       sizeof(task_sec->lease_open_key));
	return 0;
}

void pkm_kacs_lease_finish_open(void)
{
	struct pkm_kacs_task_security *task_sec;

	if (!current || !current->security)
		return;
	task_sec = pkm_kacs_task(current);
	pkm_kacs_lease_manager_put(task_sec->lease_open_mgr);
	task_sec->lease_open_mgr = NULL;
	memset(task_sec->lease_open_key, 0, sizeof(task_sec->lease_open_key));
}

void pkm_kacs_lease_bind_open(struct file *file)
{
	struct pkm_kacs_task_security *task_sec;
	struct pkm_kacs_file_security *sec;

	if (!file || !file->f_security || !current->security)
		return;
	task_sec = pkm_kacs_task(current);
	sec = pkm_kacs_file(file);
	if (!task_sec->lease_open_mgr || sec->lease_mgr)
		return;
	kref_get(&task_sec->lease_open_mgr->ref);
	sec->lease_mgr = task_sec->lease_open_mgr;
	memcpy(sec->lease_key, task_sec->lease_open_key,
	       sizeof(sec->lease_key));
}

void pkm_kacs_lease_note_vfs_break(struct inode *inode, u32 reason)
{
	struct pkm_kacs_task_security *task_sec;
	int i;

	if (!inode || !current || !current->security)
		return;
	task_sec = pkm_kacs_task(current);
	for (i = 0; i < ARRAY_SIZE(task_sec->lease_vfs_inode); i++) {
		if (task_sec->lease_vfs_inode[i] == inode ||
		    !task_sec->lease_vfs_inode[i]) {
			task_sec->lease_vfs_inode[i] = inode;
			task_sec->lease_vfs_reason[i] = reason;
			return;
		}
	}
	/* Full: the oldest note gives way. */
	memmove(&task_sec->lease_vfs_inode[0], &task_sec->lease_vfs_inode[1],
		sizeof(task_sec->lease_vfs_inode) -
			sizeof(task_sec->lease_vfs_inode[0]));
	memmove(&task_sec->lease_vfs_reason[0], &task_sec->lease_vfs_reason[1],
		sizeof(task_sec->lease_vfs_reason) -
			sizeof(task_sec->lease_vfs_reason[0]));
	task_sec->lease_vfs_inode[ARRAY_SIZE(task_sec->lease_vfs_inode) - 1] =
		inode;
	task_sec->lease_vfs_reason[ARRAY_SIZE(task_sec->lease_vfs_reason) - 1] =
		reason;
}

void pkm_kacs_lease_clear_vfs_breaks(void)
{
	struct pkm_kacs_task_security *task_sec;

	if (!current || !current->security)
		return;
	task_sec = pkm_kacs_task(current);
	memset(task_sec->lease_vfs_inode, 0, sizeof(task_sec->lease_vfs_inode));
	memset(task_sec->lease_vfs_reason, 0,
	       sizeof(task_sec->lease_vfs_reason));
}

void pkm_kacs_lease_set_breaker_file(struct file *file)
{
	struct pkm_kacs_task_security *task_sec;
	struct pkm_kacs_file_security *sec;

	if (!current || !current->security)
		return;
	task_sec = pkm_kacs_task(current);
	task_sec->lease_breaker_mgr = NULL;
	memset(task_sec->lease_breaker_key, 0,
	       sizeof(task_sec->lease_breaker_key));
	if (!file || !file->f_security)
		return;
	sec = pkm_kacs_file(file);
	if (!sec->lease_mgr)
		return;
	/* The open holds its manager for as long as the operation runs. */
	task_sec->lease_breaker_mgr = sec->lease_mgr;
	memcpy(task_sec->lease_breaker_key, sec->lease_key,
	       sizeof(task_sec->lease_breaker_key));
}

/* What an open may be granted now (TRM "Requesting a lease"). */
static u32 pkm_kacs_lease_grantable(struct file *file, struct file *record,
				    struct pkm_kacs_nt_state *state,
				    u32 requested)
{
	struct pkm_kacs_file_security *sec = pkm_kacs_file(file);
	struct pkm_kacs_file_security *record_sec = pkm_kacs_file(record);
	struct inode *inode = file_inode(record);
	u32 granted = 0;
	u32 own_writers;

	/* The open's own registration, on the record file. */
	own_writers = (record_sec->nt_inode &&
		       (record_sec->nt_classes & PKM_KACS_NT_WRITE)) ?
			      1 :
			      0;
	if ((requested & KACS_LEASE_READ) &&
	    (sec->granted_access & KACS_FILE_READ_DATA) &&
	    state->holding[1] <= own_writers)
		granted |= KACS_LEASE_READ;
	if ((granted & KACS_LEASE_READ) && (requested & KACS_LEASE_HANDLE))
		granted |= KACS_LEASE_HANDLE;
	if ((granted & KACS_LEASE_READ) && (requested & KACS_LEASE_WRITE) &&
	    S_ISREG(inode->i_mode) &&
	    (sec->granted_access &
	     (KACS_FILE_WRITE_DATA | KACS_FILE_APPEND_DATA)) &&
	    state->opens <= 1)
		granted |= KACS_LEASE_WRITE;
	return granted;
}

static long pkm_kacs_lease_request(struct file *outer, struct file *file,
				   struct pkm_kacs_lease_manager *mgr,
				   struct kacs_lease_args *args)
{
	struct pkm_kacs_nt_lease *lease = NULL;
	struct pkm_kacs_nt_lease *existing;
	struct pkm_kacs_nt_state *state;
	struct inode *inode = file_inode(file);
	bool acknowledge = args->flags & KACS_LEASE_ACKNOWLEDGE;
	u32 granted;
	long ret = 0;

	state = pkm_kacs_nt_state(inode, true);
	if (!state)
		return -ENOMEM;

	spin_lock(&state->lock);
	list_for_each_entry(existing, &state->leases, inode_node) {
		if (existing->file == file && !existing->released &&
		    pkm_kacs_lease_key_matches(existing, mgr,
					       args->lease_key)) {
			lease = existing;
			kref_get(&lease->ref);
			break;
		}
	}
	spin_unlock(&state->lock);

	if (acknowledge) {
		if (!lease)
			return -ENOENT;
		pkm_kacs_lease_complete_break(lease, args->state, false);
		spin_lock(&state->lock);
		args->state = lease->state;
		spin_unlock(&state->lock);
		goto out_put;
	}

	if (!lease) {
		if (!args->state)
			return 0;
		lease = kzalloc(sizeof(*lease), GFP_KERNEL);
		if (!lease)
			return -ENOMEM;
		kref_init(&lease->ref);
		mutex_init(&lease->lock);
		INIT_LIST_HEAD(&lease->inode_node);
		INIT_LIST_HEAD(&lease->mgr_node);
		INIT_LIST_HEAD(&lease->notice_node);
		INIT_DELAYED_WORK(&lease->timeout_work,
				  pkm_kacs_lease_timeout_workfn);
		kref_get(&mgr->ref);
		lease->mgr = mgr;
		ihold(inode);
		lease->inode = inode;
		lease->file = file;
		memcpy(lease->key, args->lease_key, sizeof(lease->key));

		mutex_lock(&lease->lock);
		spin_lock(&state->lock);
		granted = pkm_kacs_lease_grantable(outer, file, state,
						   args->state);
		if (granted) {
			lease->state = granted;
			kref_get(&lease->ref);
			list_add_tail(&lease->inode_node, &state->leases);
			WRITE_ONCE(state->nleases, state->nleases + 1);
		}
		spin_unlock(&state->lock);
		if (granted) {
			spin_lock(&mgr->lock);
			list_add_tail(&lease->mgr_node, &mgr->leases);
			spin_unlock(&mgr->lock);
			ret = pkm_kacs_lease_add_proxy(lease);
			if (ret) {
				/* No proxy, no lease: the VFS could not
				 * be made to wait for it. */
				pkm_kacs_lease_release_locked(lease);
				granted = 0;
				ret = 0;
			}
		}
		mutex_unlock(&lease->lock);
		args->state = granted;
		goto out_put;
	}

	mutex_lock(&lease->lock);
	if (!args->state) {
		pkm_kacs_lease_release_locked(lease);
	} else {
		spin_lock(&state->lock);
		if (lease->breaking) {
			ret = -EBUSY;
		} else {
			/* An upgrade is judged as a request; a
			 * downgrade always succeeds. */
			granted = pkm_kacs_lease_grantable(outer, file, state,
							   args->state);
			lease->state = granted;
			args->state = granted;
		}
		spin_unlock(&state->lock);
	}
	mutex_unlock(&lease->lock);
out_put:
	pkm_kacs_lease_put(lease);
	return ret;
}

SYSCALL_DEFINE4(kacs_lease, int, fd, int, manager_fd,
		struct kacs_lease_args __user *, uargs, size_t, size)
{
	struct pkm_kacs_lease_manager *mgr;
	struct pkm_kacs_file_security *sec;
	struct kacs_lease_args args = {};
	struct file *record_file;
	struct file *file;
	long ret;

	if (!uargs || size < KACS_LEASE_ARGS_MIN_SIZE)
		return -EINVAL;
	ret = copy_struct_from_user(&args, sizeof(args), uargs, size);
	if (ret)
		return ret == -E2BIG ? -EINVAL : ret;
	if ((args.state & ~PKM_KACS_LEASE_ALL) ||
	    (args.flags & ~KACS_LEASE_ACKNOWLEDGE) || args.__pad)
		return -EINVAL;

	CLASS(fd, f)(fd);
	if (fd_empty(f))
		return -EBADF;
	file = fd_file(f);
	if (!file->f_security || (file->f_mode & FMODE_PATH))
		return -EOPNOTSUPP;
	sec = pkm_kacs_file(file);
	if (!sec->managed || !pkm_kacs_nt_applies(file_inode(file)))
		return -EOPNOTSUPP;

	mgr = pkm_kacs_lease_manager_get(manager_fd);
	if (!mgr)
		return -EBADF;
	/* The open has to have been made under this manager and key. */
	if (sec->lease_mgr != mgr ||
	    memcmp(sec->lease_key, args.lease_key, sizeof(args.lease_key))) {
		ret = -EINVAL;
		goto out;
	}
	record_file = file;
#if IS_ENABLED(CONFIG_STRATAFS_FS)
	if (file_inode(file)->i_sb->s_magic == STRATAFS_SUPER_MAGIC)
		record_file = stratafs_kacs_real_file(file);
#endif
	if (!record_file || pkm_kacs_nt_stacked(file_inode(record_file))) {
		ret = -EOPNOTSUPP;
		goto out;
	}

	ret = pkm_kacs_lease_request(file, record_file, mgr, &args);
	if (!ret &&
	    copy_to_user(&uargs->state, &args.state, sizeof(args.state)))
		ret = -EFAULT;
out:
	pkm_kacs_lease_manager_put(mgr);
	return ret;
}

static ssize_t pkm_kacs_lease_manager_read(struct file *file, char __user *buf,
					   size_t count, loff_t *ppos)
{
	struct pkm_kacs_lease_manager *mgr = file->private_data;
	struct pkm_kacs_nt_lease *lease;
	struct kacs_lease_break notice;
	size_t done = 0;
	long ret;

	if (count < sizeof(notice))
		return -EINVAL;
	for (;;) {
		spin_lock(&mgr->lock);
		lease = list_first_entry_or_null(
			&mgr->notices, struct pkm_kacs_nt_lease, notice_node);
		if (lease) {
			notice = lease->notice;
			list_del_init(&lease->notice_node);
		}
		spin_unlock(&mgr->lock);
		if (!lease) {
			if (done)
				return done;
			if (file->f_flags & O_NONBLOCK)
				return -EAGAIN;
			ret = wait_event_interruptible(
				mgr->wq, !list_empty_careful(&mgr->notices));
			if (ret)
				return ret;
			continue;
		}
		pkm_kacs_lease_put(lease);
		if (copy_to_user(buf + done, &notice, sizeof(notice)))
			return done ? done : -EFAULT;
		done += sizeof(notice);
		if (count - done < sizeof(notice))
			return done;
	}
}

static __poll_t pkm_kacs_lease_manager_poll(struct file *file,
					    struct poll_table_struct *wait)
{
	struct pkm_kacs_lease_manager *mgr = file->private_data;

	poll_wait(file, &mgr->wq, wait);
	return list_empty_careful(&mgr->notices) ? 0 : EPOLLIN | EPOLLRDNORM;
}

static int pkm_kacs_lease_manager_release(struct inode *inode,
					  struct file *file)
{
	struct pkm_kacs_lease_manager *mgr = file->private_data;
	struct pkm_kacs_nt_lease *lease;

	/* Closing the manager releases every lease it holds. */
	for (;;) {
		spin_lock(&mgr->lock);
		lease = list_first_entry_or_null(
			&mgr->leases, struct pkm_kacs_nt_lease, mgr_node);
		if (lease)
			kref_get(&lease->ref);
		spin_unlock(&mgr->lock);
		if (!lease)
			break;
		mutex_lock(&lease->lock);
		pkm_kacs_lease_release_locked(lease);
		mutex_unlock(&lease->lock);
		pkm_kacs_lease_put(lease);
	}
	spin_lock(&mgr->lock);
	while ((lease = list_first_entry_or_null(&mgr->notices,
						 struct pkm_kacs_nt_lease,
						 notice_node))) {
		list_del_init(&lease->notice_node);
		spin_unlock(&mgr->lock);
		pkm_kacs_lease_put(lease);
		spin_lock(&mgr->lock);
	}
	spin_unlock(&mgr->lock);
	pkm_kacs_lease_manager_put(mgr);
	return 0;
}

static const struct file_operations pkm_kacs_lease_manager_fops = {
	.owner = THIS_MODULE,
	.read = pkm_kacs_lease_manager_read,
	.poll = pkm_kacs_lease_manager_poll,
	.release = pkm_kacs_lease_manager_release,
	.llseek = noop_llseek,
};

SYSCALL_DEFINE2(kacs_create_lease_manager, u32, flags, u32, timeout_ms)
{
	struct pkm_kacs_lease_manager *mgr;
	int fd_flags = O_RDONLY;
	int fd;

	if (flags & ~(KACS_LEASE_MANAGER_CLOEXEC | KACS_LEASE_MANAGER_NONBLOCK))
		return -EINVAL;
	if (timeout_ms > PKM_KACS_LEASE_MAX_TIMEOUT_MS)
		return -EINVAL;
	if (!timeout_ms)
		timeout_ms = KACS_LEASE_DEFAULT_BREAK_TIMEOUT_MS;

	mgr = kzalloc(sizeof(*mgr), GFP_KERNEL);
	if (!mgr)
		return -ENOMEM;
	kref_init(&mgr->ref);
	spin_lock_init(&mgr->lock);
	INIT_LIST_HEAD(&mgr->notices);
	INIT_LIST_HEAD(&mgr->leases);
	init_waitqueue_head(&mgr->wq);
	mgr->timeout = msecs_to_jiffies(timeout_ms);

	if (flags & KACS_LEASE_MANAGER_CLOEXEC)
		fd_flags |= O_CLOEXEC;
	if (flags & KACS_LEASE_MANAGER_NONBLOCK)
		fd_flags |= O_NONBLOCK;
	fd = anon_inode_getfd("[kacs_lease]", &pkm_kacs_lease_manager_fops, mgr,
			      fd_flags);
	if (fd < 0)
		pkm_kacs_lease_manager_put(mgr);
	return fd;
}

#ifdef CONFIG_SECURITY_PKM_KUNIT
#include <kunit/test.h>

#define PKM_KUNIT_RWH (KACS_LEASE_READ | KACS_LEASE_WRITE | KACS_LEASE_HANDLE)
#define PKM_KUNIT_RH (KACS_LEASE_READ | KACS_LEASE_HANDLE)

/* TRM "What breaks a lease". */
static void pkm_kunit_nt_lease_targets(struct kunit *test)
{
	KUNIT_EXPECT_EQ(test,
			pkm_kacs_lease_target(PKM_KUNIT_RWH,
					      KACS_LEASE_BREAK_OPEN),
			(u32)PKM_KUNIT_RH);
	KUNIT_EXPECT_EQ(test,
			pkm_kacs_lease_target(PKM_KUNIT_RH,
					      KACS_LEASE_BREAK_SHARING),
			(u32)KACS_LEASE_READ);
	KUNIT_EXPECT_EQ(test,
			pkm_kacs_lease_target(PKM_KUNIT_RH,
					      KACS_LEASE_BREAK_WRITE),
			0U);
	KUNIT_EXPECT_EQ(test,
			pkm_kacs_lease_target(KACS_LEASE_READ,
					      KACS_LEASE_BREAK_DELETE),
			(u32)KACS_LEASE_READ);
}

static void pkm_kunit_nt_lease_waits(struct kunit *test)
{
	/* Losing write or handle caching waits for the holder... */
	KUNIT_EXPECT_TRUE(
		test, pkm_kacs_lease_break_waits(PKM_KUNIT_RWH, PKM_KUNIT_RH,
						 KACS_LEASE_BREAK_OPEN));
	KUNIT_EXPECT_TRUE(
		test, pkm_kacs_lease_break_waits(PKM_KUNIT_RH, KACS_LEASE_READ,
						 KACS_LEASE_BREAK_NAMESPACE));
	/* ...a write only notifies, even when handle caching goes. */
	KUNIT_EXPECT_FALSE(test,
			   pkm_kacs_lease_break_waits(PKM_KUNIT_RH, 0,
						      KACS_LEASE_BREAK_WRITE));
}

static struct kunit_case pkm_kunit_nt_lease_cases[] = {
	KUNIT_CASE(pkm_kunit_nt_lease_targets),
	KUNIT_CASE(pkm_kunit_nt_lease_waits),
	{}
};

static struct kunit_suite pkm_kunit_nt_lease_suite = {
	.name = "pkm_kunit_nt_lease",
	.test_cases = pkm_kunit_nt_lease_cases,
};

kunit_test_suite(pkm_kunit_nt_lease_suite);
#endif
