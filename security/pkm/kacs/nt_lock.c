// SPDX-License-Identifier: GPL-2.0-only
/*
 * NT byte-range locks (TRM "Byte-Range Locks").
 *
 * A lock belongs to the open file description that took it. Below a
 * stacking filesystem it belongs to the backing file the outer open
 * reaches, because that is the open every read and write of the file is
 * checked through: rw_verify_area() runs again on the backing file, and
 * the outer file's own check is skipped.
 *
 * I/O is checked against the lock list when it is issued. Granting a lock
 * does not wait for I/O already admitted, so no lock is ever held across
 * I/O: the list is read under the NT state's spinlock, and a file with no
 * I/O-blocking locks costs one load.
 */

#include <linux/fs.h>
#include <linux/falloc.h>
#include <linux/kacs_stratafs.h>
#include <linux/sched/signal.h>
#include <linux/slab.h>
#include <linux/syscalls.h>
#include <linux/uaccess.h>
#include <linux/wait.h>

#include <pkm/file.h>
#include <pkm/sd.h>

#include "file_access.h"
#include "lsm_internal.h"
#include "nt_file.h"
#include "nt_lease.h"
#include "nt_lock.h"
#include "token_runtime.h"

struct pkm_kacs_nt_lock {
	struct list_head node;
	const struct file *owner;
	u64 offset;
	u64 length;
	bool exclusive;
	/* The owner could write the file, so the lock blocks I/O. */
	bool blocks_io;
};

struct pkm_kacs_nt_lock_waiter {
	struct list_head node;
	const struct file *owner;
	u64 offset;
	u64 length;
	u64 cookie;
	bool exclusive;
	bool cancelled;
};

/*
 * MS-FSA 2.1.4.10's overlap test. The range from offset zero with length
 * zero overlaps nothing; any other zero-length range is a point.
 */
static bool pkm_kacs_nt_ranges_overlap(u64 off1, u64 len1, u64 off2, u64 len2)
{
	u64 last1;
	u64 last2;

	if ((off1 == 0 && len1 == 0) || (off2 == 0 && len2 == 0))
		return false;
	last1 = off1 + len1 - 1;
	last2 = off2 + len2 - 1;
	return off1 <= last2 && last1 >= off2;
}

/*
 * Whether an access of the range conflicts with @lock (MS-FSA 2.1.4.10):
 * an exclusive lock blocks every other open, and an open's own
 * overlapping exclusive lock request; a shared lock blocks exclusive
 * intent from anyone, its holder included.
 */
static bool pkm_kacs_nt_lock_conflicts(const struct pkm_kacs_nt_lock *lock,
				       const struct file *owner, u64 offset,
				       u64 length, bool exclusive,
				       bool lock_intent)
{
	if (!pkm_kacs_nt_ranges_overlap(offset, length, lock->offset,
					lock->length))
		return false;
	if (lock->exclusive) {
		if (lock->owner != owner)
			return true;
		return exclusive && lock_intent;
	}
	return exclusive;
}

static bool
pkm_kacs_nt_lock_request_conflicts(const struct pkm_kacs_nt_state *state,
				   const struct file *owner, u64 offset,
				   u64 length, bool exclusive)
{
	const struct pkm_kacs_nt_lock *lock;

	list_for_each_entry(lock, &state->locks, node) {
		if (pkm_kacs_nt_lock_conflicts(lock, owner, offset, length,
					       exclusive, true))
			return true;
	}
	return false;
}

/* An earlier waiter whose request this one would overtake. */
static bool
pkm_kacs_nt_earlier_waiter_conflicts(const struct pkm_kacs_nt_state *state,
				     const struct pkm_kacs_nt_lock_waiter *me)
{
	const struct pkm_kacs_nt_lock_waiter *w;

	list_for_each_entry(w, &state->lock_waiters, node) {
		if (w == me)
			return false;
		if (w->cancelled)
			continue;
		if (pkm_kacs_nt_ranges_overlap(w->offset, w->length, me->offset,
					       me->length) &&
		    (w->exclusive || me->exclusive))
			return true;
	}
	return false;
}

/*
 * The open whose locks a handle's I/O is checked against: the file itself,
 * or the backing file below a stacking filesystem.
 */
static struct file *pkm_kacs_nt_lock_owner(struct file *file)
{
#if IS_ENABLED(CONFIG_STRATAFS_FS)
	if (file_inode(file)->i_sb->s_magic == STRATAFS_SUPER_MAGIC)
		return stratafs_kacs_real_file(file);
#endif
	return file;
}

/*
 * Whether a lock taken through @file may block others' I/O: only if its
 * opener could write the file (TRM "Who can block whom").
 */
static bool pkm_kacs_nt_lock_may_block(struct file *file)
{
	const void *subject_token;
	u32 maximum = 0;

	if (pkm_kacs_file(file)->granted_access &
	    (KACS_FILE_WRITE_DATA | KACS_FILE_APPEND_DATA))
		return true;
	subject_token = pkm_kacs_current_effective_token_ptr();
	if (!subject_token)
		return false;
	if (pkm_kacs_live_path_access_granted(subject_token, &file->f_path,
					      KACS_ACCESS_MAXIMUM_ALLOWED, 0,
					      &maximum))
		return false;
	return (maximum & (KACS_FILE_WRITE_DATA | KACS_FILE_APPEND_DATA)) != 0;
}

static long pkm_kacs_nt_lock_acquire(struct pkm_kacs_nt_state *state,
				     const struct file *owner, u64 offset,
				     u64 length, bool exclusive, bool blocks_io,
				     bool fail_immediately, u64 cookie)
{
	struct pkm_kacs_nt_lock_waiter waiter = {
		.owner = owner,
		.offset = offset,
		.length = length,
		.cookie = cookie,
		.exclusive = exclusive,
	};
	struct pkm_kacs_nt_lock *lock;
	DEFINE_WAIT(wait);
	bool queued = false;
	long ret;

	lock = kmalloc(sizeof(*lock), GFP_KERNEL);
	if (!lock)
		return -ENOMEM;
	*lock = (struct pkm_kacs_nt_lock){
		.owner = owner,
		.offset = offset,
		.length = length,
		.exclusive = exclusive,
		.blocks_io = blocks_io,
	};

	spin_lock(&state->lock);
	for (;;) {
		if (waiter.cancelled) {
			ret = -ECANCELED;
			break;
		}
		if (!pkm_kacs_nt_lock_request_conflicts(state, owner, offset,
							length, exclusive) &&
		    (!queued ||
		     !pkm_kacs_nt_earlier_waiter_conflicts(state, &waiter))) {
			list_add_tail(&lock->node, &state->locks);
			state->nlocks++;
			if (blocks_io)
				WRITE_ONCE(state->nblocking,
					   state->nblocking + 1);
			lock = NULL;
			ret = 0;
			break;
		}
		if (fail_immediately) {
			ret = -EAGAIN;
			break;
		}
		if (signal_pending(current)) {
			ret = -EINTR;
			break;
		}
		if (!queued) {
			list_add_tail(&waiter.node, &state->lock_waiters);
			queued = true;
		}
		prepare_to_wait(&state->lock_wq, &wait, TASK_INTERRUPTIBLE);
		spin_unlock(&state->lock);
		schedule();
		spin_lock(&state->lock);
	}
	if (queued) {
		list_del(&waiter.node);
		/* Others queued behind this request may now proceed. */
		wake_up_all(&state->lock_wq);
	}
	spin_unlock(&state->lock);
	finish_wait(&state->lock_wq, &wait);
	kfree(lock);
	return ret;
}

static long pkm_kacs_nt_lock_unlock(struct pkm_kacs_nt_state *state,
				    const struct file *owner, u64 offset,
				    u64 length)
{
	struct pkm_kacs_nt_lock *lock;
	struct pkm_kacs_nt_lock *found = NULL;

	spin_lock(&state->lock);
	list_for_each_entry(lock, &state->locks, node) {
		if (lock->owner == owner && lock->offset == offset &&
		    lock->length == length) {
			found = lock;
			break;
		}
	}
	if (found) {
		list_del(&found->node);
		state->nlocks--;
		if (found->blocks_io)
			WRITE_ONCE(state->nblocking, state->nblocking - 1);
		wake_up_all(&state->lock_wq);
	}
	spin_unlock(&state->lock);
	if (!found)
		return -ENOLCK;
	kfree(found);
	return 0;
}

static long pkm_kacs_nt_lock_cancel(struct pkm_kacs_nt_state *state,
				    const struct file *owner, u64 cookie)
{
	struct pkm_kacs_nt_lock_waiter *w;
	long ret = -ENOENT;

	spin_lock(&state->lock);
	list_for_each_entry(w, &state->lock_waiters, node) {
		if (w->owner == owner && w->cookie == cookie && !w->cancelled) {
			w->cancelled = true;
			ret = 0;
			break;
		}
	}
	if (!ret)
		wake_up_all(&state->lock_wq);
	spin_unlock(&state->lock);
	return ret;
}

void pkm_kacs_nt_locks_release(struct file *file)
{
	struct pkm_kacs_nt_state *state;
	struct pkm_kacs_nt_lock *lock;
	struct pkm_kacs_nt_lock *next;
	LIST_HEAD(dead);
	struct inode *inode;

	if (!file)
		return;
	inode = file_inode(file);
	if (!inode)
		return;
	state = pkm_kacs_nt_state(inode, false);
	if (!state || !READ_ONCE(state->nlocks))
		return;

	spin_lock(&state->lock);
	list_for_each_entry_safe(lock, next, &state->locks, node) {
		if (lock->owner != file)
			continue;
		list_move(&lock->node, &dead);
		state->nlocks--;
		if (lock->blocks_io)
			WRITE_ONCE(state->nblocking, state->nblocking - 1);
	}
	if (!list_empty(&dead))
		wake_up_all(&state->lock_wq);
	spin_unlock(&state->lock);

	list_for_each_entry_safe(lock, next, &dead, node)
		kfree(lock);
}

/*
 * Whether I/O over the range conflicts with another open's lock (MS-FSA
 * 2.1.4.10 without lock intent): a read conflicts with another open's
 * exclusive lock; a write with that, and with any shared lock.
 */
static int pkm_kacs_nt_lock_check_range(struct inode *inode,
					const struct file *owner, u64 offset,
					u64 length, bool write)
{
	struct pkm_kacs_nt_state *state;
	const struct pkm_kacs_nt_lock *lock;
	int ret = 0;

	if (!inode || !inode->i_security || !S_ISREG(inode->i_mode) ||
	    pkm_kacs_nt_stacked(inode))
		return 0;
	state = pkm_kacs_nt_state(inode, false);
	if (!state || !READ_ONCE(state->nblocking))
		return 0;

	spin_lock(&state->lock);
	list_for_each_entry(lock, &state->locks, node) {
		if (lock->blocks_io &&
		    pkm_kacs_nt_lock_conflicts(lock, owner, offset, length,
					       write, false)) {
			ret = -EAGAIN;
			break;
		}
	}
	spin_unlock(&state->lock);
	return ret;
}

int pkm_kacs_nt_lock_check_io(struct file *file, loff_t pos, size_t count,
			      bool write)
{
	struct inode *inode;
	int ret;

	if (!file || count == 0)
		return 0;
	inode = file_inode(file);
	/* An append lands at the end of the file, wherever its position. */
	if (write && (file->f_flags & O_APPEND))
		pos = i_size_read(inode);
	if (pos < 0)
		return 0;
	ret = pkm_kacs_nt_lock_check_range(inode, file, (u64)pos, count, write);
	/* Other holders lose read caching to a write (TRM "Leases"). */
	if (!ret && write)
		pkm_kacs_lease_note_write(file);
	return ret;
}

int pkm_kacs_nt_lock_check_resize(struct inode *inode, struct file *file,
				  loff_t new_size)
{
	loff_t old_size;
	loff_t from;
	loff_t to;

	if (!inode || new_size < 0)
		return 0;
	old_size = i_size_read(inode);
	if (old_size == new_size)
		return 0;
	from = min(old_size, new_size);
	to = max(old_size, new_size);
	return pkm_kacs_nt_lock_check_range(inode, file, (u64)from,
					    (u64)(to - from), true);
}

int pkm_kacs_nt_lock_check_fallocate(struct file *file, int mode, loff_t offset,
				     loff_t len)
{
	struct inode *inode;
	loff_t size;

	if (!file || len <= 0 || offset < 0)
		return 0;
	inode = file_inode(file);
	switch (mode & ~FALLOC_FL_KEEP_SIZE) {
	case FALLOC_FL_PUNCH_HOLE:
	case FALLOC_FL_ZERO_RANGE:
	case FALLOC_FL_UNSHARE_RANGE:
	case FALLOC_FL_WRITE_ZEROES:
		return pkm_kacs_nt_lock_check_range(inode, file, offset, len,
						    true);
	case FALLOC_FL_COLLAPSE_RANGE:
	case FALLOC_FL_INSERT_RANGE:
		/* Everything from the offset to the end moves. */
		size = i_size_read(inode);
		if (size <= offset)
			return 0;
		return pkm_kacs_nt_lock_check_range(inode, file, offset,
						    size - offset, true);
	default:
		return 0;
	}
}

SYSCALL_DEFINE3(kacs_lock, int, fd, const struct kacs_lock_args __user *, uargs,
		size_t, size)
{
	struct pkm_kacs_file_security *sec;
	struct pkm_kacs_nt_state *state;
	struct kacs_lock_args args = {};
	struct file *owner;
	struct file *file;
	struct inode *record;
	long ret;

	if (!uargs || size < KACS_LOCK_ARGS_MIN_SIZE)
		return -EINVAL;
	ret = copy_struct_from_user(&args, sizeof(args), uargs, size);
	if (ret)
		return ret == -E2BIG ? -EINVAL : ret;
	if (args.op < KACS_LOCK_SHARED || args.op > KACS_LOCK_CANCEL ||
	    (args.flags & ~KACS_LOCK_FAIL_IMMEDIATELY))
		return -EINVAL;
	if (args.length && args.offset + args.length - 1 < args.offset)
		return -EINVAL;

	CLASS(fd, f)(fd);
	if (fd_empty(f))
		return -EBADF;
	file = fd_file(f);
	if (!file->f_security || (file->f_mode & FMODE_PATH))
		return -EOPNOTSUPP;
	sec = pkm_kacs_file(file);
	if (!sec->managed || !S_ISREG(file_inode(file)->i_mode))
		return -EOPNOTSUPP;
	if (!(sec->granted_access &
	      (KACS_FILE_READ_DATA | KACS_FILE_WRITE_DATA |
	       KACS_FILE_APPEND_DATA)))
		return -EACCES;

	owner = pkm_kacs_nt_lock_owner(file);
	if (!owner)
		return -EOPNOTSUPP;
	record = file_inode(owner);
	if (!pkm_kacs_nt_applies(record) || pkm_kacs_nt_stacked(record))
		return -EOPNOTSUPP;
	state = pkm_kacs_nt_state(record, true);
	if (!state)
		return -ENOMEM;

	switch (args.op) {
	case KACS_LOCK_SHARED:
	case KACS_LOCK_EXCLUSIVE:
		/* Other holders' read caching goes before the range is. */
		pkm_kacs_lease_break_inode(record, KACS_LEASE_BREAK_LOCK, file);
		return pkm_kacs_nt_lock_acquire(
			state, owner, args.offset, args.length,
			args.op == KACS_LOCK_EXCLUSIVE,
			pkm_kacs_nt_lock_may_block(file),
			args.flags & KACS_LOCK_FAIL_IMMEDIATELY, args.cookie);
	case KACS_LOCK_UNLOCK:
		return pkm_kacs_nt_lock_unlock(state, owner, args.offset,
					       args.length);
	default:
		return pkm_kacs_nt_lock_cancel(state, owner, args.cookie);
	}
}

#ifdef CONFIG_SECURITY_PKM_KUNIT
#include <kunit/test.h>

static const struct file pkm_kunit_lock_owner_a;
static const struct file pkm_kunit_lock_owner_b;

/* MS-FSA 2.1.4.10's overlap, including the {0, 0} range and points. */
static void pkm_kunit_nt_lock_overlap(struct kunit *test)
{
	KUNIT_EXPECT_TRUE(test, pkm_kacs_nt_ranges_overlap(0, 10, 9, 5));
	KUNIT_EXPECT_FALSE(test, pkm_kacs_nt_ranges_overlap(0, 10, 10, 5));
	KUNIT_EXPECT_FALSE(test, pkm_kacs_nt_ranges_overlap(0, 0, 0, 10));
	KUNIT_EXPECT_FALSE(test, pkm_kacs_nt_ranges_overlap(0, 10, 0, 0));
	/* A zero-length lock at 6 meets I/O that spans it. */
	KUNIT_EXPECT_TRUE(test, pkm_kacs_nt_ranges_overlap(0, 10, 6, 0));
}

static void pkm_kunit_nt_lock_conflict_rules(struct kunit *test)
{
	struct pkm_kacs_nt_lock exclusive = {
		.owner = &pkm_kunit_lock_owner_a,
		.offset = 0,
		.length = 10,
		.exclusive = true,
		.blocks_io = true,
	};
	struct pkm_kacs_nt_lock shared = {
		.owner = &pkm_kunit_lock_owner_a,
		.offset = 0,
		.length = 10,
		.exclusive = false,
		.blocks_io = true,
	};

	/* An exclusive lock blocks other opens' reads and writes. */
	KUNIT_EXPECT_TRUE(test, pkm_kacs_nt_lock_conflicts(
					&exclusive, &pkm_kunit_lock_owner_b, 2,
					2, false, false));
	/* Not its own open's I/O. */
	KUNIT_EXPECT_FALSE(test, pkm_kacs_nt_lock_conflicts(
					 &exclusive, &pkm_kunit_lock_owner_a, 2,
					 2, true, false));
	/* Its own open's overlapping exclusive lock request conflicts. */
	KUNIT_EXPECT_TRUE(test, pkm_kacs_nt_lock_conflicts(
					&exclusive, &pkm_kunit_lock_owner_a, 2,
					2, true, true));
	/* A shared lock blocks writes, its holder's included... */
	KUNIT_EXPECT_TRUE(test, pkm_kacs_nt_lock_conflicts(
					&shared, &pkm_kunit_lock_owner_a, 2, 2,
					true, false));
	/* ...but not reads. */
	KUNIT_EXPECT_FALSE(test, pkm_kacs_nt_lock_conflicts(
					 &shared, &pkm_kunit_lock_owner_b, 2, 2,
					 false, false));
}

static struct kunit_case pkm_kunit_nt_lock_cases[] = {
	KUNIT_CASE(pkm_kunit_nt_lock_overlap),
	KUNIT_CASE(pkm_kunit_nt_lock_conflict_rules),
	{}
};

static struct kunit_suite pkm_kunit_nt_lock_suite = {
	.name = "pkm_kunit_nt_lock",
	.test_cases = pkm_kunit_nt_lock_cases,
};

kunit_test_suite(pkm_kunit_nt_lock_suite);
#endif
