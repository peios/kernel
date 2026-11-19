// SPDX-License-Identifier: GPL-2.0-only
/*
 * KACS special attributes (TRM "Special Attributes").
 *
 * security.peios.sattr holds a struct kacs_sattr. Reading it is an ordinary
 * getxattr under FILE_READ_ATTRIBUTES; writing goes through
 * pkm_kacs_sattr_vfs_set(), which merges the fields the caller names into
 * the stored value under the inode lock, so that two programs changing
 * different attributes cannot undo each other. Nothing is stored while
 * nothing is set.
 *
 * The read-only flag is consulted at every open for writing and every
 * deletion, so its state is cached in the inode blob: a two-bit state and a
 * generation, which every write and removal advances, so that a read racing
 * a write never installs the value it overtook.
 */

#include <linux/atomic.h>
#include <linux/dcache.h>
#include <linux/fs.h>
#include <linux/security.h>
#include <linux/string.h>
#include <linux/xattr.h>

#include <pkm/file.h>

#include "lsm_internal.h"
#include "nt_file.h"
#include "nt_lease.h"
#include "sattr.h"

#define PKM_KACS_SATTR_UNKNOWN 0
#define PKM_KACS_SATTR_CLEAR 1
#define PKM_KACS_SATTR_READONLY 2
#define PKM_KACS_SATTR_STATE_MASK 3
#define PKM_KACS_SATTR_GEN_STEP 4

#define PKM_KACS_SATTR_VALID \
	(KACS_SATTR_VALID_ATTRIBUTES | KACS_SATTR_VALID_CREATED_AT)

bool pkm_kacs_is_sattr_xattr(const char *name)
{
	return name && !strcmp(name, KACS_SATTR_XATTR_NAME);
}

/* Read the stored value, past the xattr hooks, as KACS's own read. */
static ssize_t pkm_kacs_sattr_read(struct dentry *dentry, struct inode *inode,
				   struct kacs_sattr *out)
{
	ssize_t len;

	if (current && current->security)
		pkm_kacs_task(current)->internal_sd_read_depth++;
	len = __vfs_getxattr(dentry, inode, KACS_SATTR_XATTR_NAME, out,
			     sizeof(*out));
	if (current && current->security)
		pkm_kacs_task(current)->internal_sd_read_depth--;
	if (len == -ENODATA || len == -EOPNOTSUPP) {
		memset(out, 0, sizeof(*out));
		return 0;
	}
	if (len < 0)
		return len;
	/* A damaged value is not trusted to release the flag. */
	if (len != sizeof(*out) || out->version != KACS_SATTR_VERSION)
		return -EIO;
	return len;
}

static bool pkm_kacs_sattr_readonly(struct dentry *dentry)
{
	struct pkm_kacs_inode_security *sec;
	struct kacs_sattr value;
	struct inode *inode;
	ssize_t len;
	int cached;
	int state;

	if (!dentry || !d_really_is_positive(dentry))
		return false;
	inode = d_inode(dentry);
	if (!inode->i_security || !(inode->i_opflags & IOP_XATTR))
		return false;

	sec = pkm_kacs_inode(inode);
	cached = atomic_read(&sec->sattr_cache);
	state = cached & PKM_KACS_SATTR_STATE_MASK;
	if (state != PKM_KACS_SATTR_UNKNOWN)
		return state == PKM_KACS_SATTR_READONLY;

	len = pkm_kacs_sattr_read(dentry, inode, &value);
	/* Unreadable or damaged reads as read-only: it fails closed. */
	if (len < 0)
		return true;
	state = (value.attributes & KACS_SATTR_READONLY) ?
			PKM_KACS_SATTR_READONLY :
			PKM_KACS_SATTR_CLEAR;
	(void)atomic_cmpxchg(&sec->sattr_cache, cached, cached | state);
	return state == PKM_KACS_SATTR_READONLY;
}

bool pkm_kacs_sattr_file_readonly(struct file *file)
{
	if (!file)
		return false;
	return pkm_kacs_sattr_readonly(file->f_path.dentry);
}

bool pkm_kacs_sattr_dentry_readonly(struct dentry *dentry)
{
	return pkm_kacs_sattr_readonly(dentry);
}

void pkm_kacs_sattr_invalidate(struct inode *inode)
{
	struct pkm_kacs_inode_security *sec;
	int old;

	if (!inode || !inode->i_security)
		return;
	sec = pkm_kacs_inode(inode);
	do {
		old = atomic_read(&sec->sattr_cache);
	} while (atomic_cmpxchg(&sec->sattr_cache, old,
				(old & ~PKM_KACS_SATTR_STATE_MASK) +
					PKM_KACS_SATTR_GEN_STEP) != old);
}

int pkm_kacs_sattr_validate(const void *value, size_t size, int flags)
{
	const struct kacs_sattr *in = value;

	if (flags || !value || size != sizeof(*in))
		return -EINVAL;
	if (in->version != KACS_SATTR_VERSION ||
	    (in->valid & ~PKM_KACS_SATTR_VALID) || in->__pad ||
	    (in->attributes & ~KACS_SATTR_READONLY) ||
	    (in->flags & ~KACS_SATTR_CREATED_AT_CLEAR))
		return -EINVAL;
	if ((in->valid & KACS_SATTR_VALID_CREATED_AT) &&
	    !(in->flags & KACS_SATTR_CREATED_AT_CLEAR) &&
	    in->created_at_nsec >= NSEC_PER_SEC)
		return -EINVAL;
	if ((in->flags & KACS_SATTR_CREATED_AT_CLEAR) &&
	    !(in->valid & KACS_SATTR_VALID_CREATED_AT))
		return -EINVAL;
	return 0;
}

/* Write @value, or remove the attribute if nothing remains set. */
static int pkm_kacs_sattr_store(struct mnt_idmap *idmap, struct dentry *dentry,
				const struct kacs_sattr *value)
{
	struct kacs_sattr stored = *value;
	int ret;

	stored.version = KACS_SATTR_VERSION;
	stored.valid = PKM_KACS_SATTR_VALID;
	if (current && current->security)
		pkm_kacs_task(current)->internal_sd_write_depth++;
	if (!stored.attributes && !(stored.flags & KACS_SATTR_CREATED_AT_SET)) {
		ret = __vfs_removexattr(idmap, dentry, KACS_SATTR_XATTR_NAME);
		if (ret == -ENODATA)
			ret = 0;
	} else {
		ret = __vfs_setxattr_noperm(idmap, dentry,
					    KACS_SATTR_XATTR_NAME, &stored,
					    sizeof(stored), 0);
	}
	if (current && current->security)
		pkm_kacs_task(current)->internal_sd_write_depth--;
	pkm_kacs_sattr_invalidate(d_inode(dentry));
	return ret;
}

/* Other holders lose read caching to an attribute change. */
static void pkm_kacs_sattr_break_leases(struct dentry *dentry)
{
	struct inode *record = pkm_kacs_nt_record_inode_for_dentry(dentry);

	if (record) {
		(void)pkm_kacs_lease_break_inode(
			record, KACS_LEASE_BREAK_ATTRIBUTES, NULL);
		iput(record);
	}
}

int pkm_kacs_sattr_vfs_set(struct mnt_idmap *idmap, struct dentry *dentry,
			   const void *value, size_t size, int flags)
{
	const struct kacs_sattr *in = value;
	struct inode *inode = d_inode(dentry);
	struct kacs_sattr current_value;
	ssize_t len;
	int ret;

	inode_lock(inode);
	/* The rights and the value's shape, through every LSM's hook. */
	ret = security_inode_setxattr(idmap, dentry, KACS_SATTR_XATTR_NAME,
				      value, size, flags);
	if (ret)
		goto out;
	len = pkm_kacs_sattr_read(dentry, inode, &current_value);
	if (len < 0 && len != -EIO) {
		ret = len;
		goto out;
	}
	/* A damaged value is replaced, not merged. */
	if (len == -EIO)
		memset(&current_value, 0, sizeof(current_value));

	if (in->valid & KACS_SATTR_VALID_ATTRIBUTES)
		current_value.attributes = in->attributes;
	if (in->valid & KACS_SATTR_VALID_CREATED_AT) {
		if (in->flags & KACS_SATTR_CREATED_AT_CLEAR) {
			current_value.flags &= ~KACS_SATTR_CREATED_AT_SET;
			current_value.created_at_sec = 0;
			current_value.created_at_nsec = 0;
		} else {
			current_value.flags |= KACS_SATTR_CREATED_AT_SET;
			current_value.created_at_sec = in->created_at_sec;
			current_value.created_at_nsec = in->created_at_nsec;
		}
	}
	current_value.flags &= KACS_SATTR_CREATED_AT_SET;
	current_value.__pad = 0;
	ret = pkm_kacs_sattr_store(idmap, dentry, &current_value);
out:
	inode_unlock(inode);
	if (!ret)
		pkm_kacs_sattr_break_leases(dentry);
	return ret;
}

int pkm_kacs_sattr_vfs_remove(struct mnt_idmap *idmap, struct dentry *dentry)
{
	struct inode *inode = d_inode(dentry);
	struct kacs_sattr cleared = {};
	int ret;

	inode_lock(inode);
	ret = security_inode_removexattr(idmap, dentry, KACS_SATTR_XATTR_NAME);
	if (!ret)
		ret = pkm_kacs_sattr_store(idmap, dentry, &cleared);
	inode_unlock(inode);
	if (!ret)
		pkm_kacs_sattr_break_leases(dentry);
	return ret;
}

#ifdef CONFIG_SECURITY_PKM_KUNIT
#include <kunit/test.h>

/* TRM "Reading and writing them": the shapes a write may take. */
static void pkm_kunit_sattr_validate(struct kunit *test)
{
	struct kacs_sattr value = {
		.version = KACS_SATTR_VERSION,
		.valid = KACS_SATTR_VALID_ATTRIBUTES,
		.attributes = KACS_SATTR_READONLY,
	};

	KUNIT_EXPECT_EQ(test, pkm_kacs_sattr_validate(&value, sizeof(value), 0),
			0);
	/* XATTR_CREATE and XATTR_REPLACE mean nothing for a merge. */
	KUNIT_EXPECT_EQ(test,
			pkm_kacs_sattr_validate(&value, sizeof(value),
						XATTR_CREATE),
			-EINVAL);
	KUNIT_EXPECT_EQ(test,
			pkm_kacs_sattr_validate(&value, sizeof(value) - 1, 0),
			-EINVAL);
	value.attributes = 0x2;
	KUNIT_EXPECT_EQ(test, pkm_kacs_sattr_validate(&value, sizeof(value), 0),
			-EINVAL);
	value.attributes = 0;
	value.valid = KACS_SATTR_VALID_CREATED_AT;
	value.created_at_nsec = NSEC_PER_SEC;
	KUNIT_EXPECT_EQ(test, pkm_kacs_sattr_validate(&value, sizeof(value), 0),
			-EINVAL);
	value.created_at_nsec = 0;
	value.valid = KACS_SATTR_VALID_ATTRIBUTES;
	value.flags = KACS_SATTR_CREATED_AT_CLEAR;
	KUNIT_EXPECT_EQ(test, pkm_kacs_sattr_validate(&value, sizeof(value), 0),
			-EINVAL);
}

static struct kunit_case pkm_kunit_sattr_cases[] = {
	KUNIT_CASE(pkm_kunit_sattr_validate),
	{}
};

static struct kunit_suite pkm_kunit_sattr_suite = {
	.name = "pkm_kunit_sattr",
	.test_cases = pkm_kunit_sattr_cases,
};

kunit_test_suite(pkm_kunit_sattr_suite);
#endif
