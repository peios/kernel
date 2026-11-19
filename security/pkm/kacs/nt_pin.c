// SPDX-License-Identifier: GPL-2.0-only
/*
 * Ancestor pinning (TRM "Ancestor pinning").
 *
 * An open made with KACS_OPEN_PIN_ANCESTORS counts itself on every
 * directory above the file, up to the root of the mount it was opened
 * through. The namespace hooks refuse renaming or removing a directory
 * whose count is not zero. The directories are recorded on the open,
 * because the file itself may be renamed while it stays open, and the pins
 * belong to the directories it was opened beneath.
 *
 * Each directory is counted on the inode that holds its NT state, as share
 * modes are: below a stacking filesystem that is the provider's, since
 * StrataFS gives each lookup of a name an inode of its own.
 *
 * The walk reads the parents under rename_lock's sequence count, counting
 * as it goes, and repeats if a rename moved a directory meanwhile. A
 * rename that had already passed its hook's check when the walk began can
 * still complete; the pin then holds from the open onwards.
 */

#include <linux/dcache.h>
#include <linux/fs.h>
#include <linux/mount.h>
#include <linux/rcupdate.h>
#include <linux/seqlock.h>
#include <linux/slab.h>

#include <pkm/file.h>

#include "lsm_internal.h"
#include "nt_file.h"
#include "nt_pin.h"

#define PKM_KACS_PIN_MAX_DEPTH 256

struct pkm_kacs_pin_set {
	unsigned int count;
	struct inode *inodes[];
};

static void pkm_kacs_pin_set_drop(struct pkm_kacs_pin_set *set)
{
	unsigned int i;

	for (i = 0; i < set->count; i++) {
		atomic_dec(&pkm_kacs_inode(set->inodes[i])->nt_pins);
		iput(set->inodes[i]);
	}
	kfree(set);
}

/*
 * Count the open on each directory above it, holding each by reference,
 * and record them. Returns NULL with nothing held if a rename moved one of
 * them meanwhile.
 */
static struct pkm_kacs_pin_set *pkm_kacs_pin_walk(struct file *file, int *error)
{
	struct dentry *root = file->f_path.mnt->mnt_root;
	struct pkm_kacs_pin_set *set;
	struct pkm_kacs_pin_set *grown;
	struct dentry *d;
	struct dentry *parent;
	struct inode *inode;
	unsigned int capacity = 16;
	unsigned int seq;

	*error = 0;
	set = kzalloc(struct_size(set, inodes, capacity), GFP_KERNEL);
	if (!set) {
		*error = -ENOMEM;
		return NULL;
	}

	seq = read_seqbegin(&rename_lock);
	d = dget(file->f_path.dentry);
	while (d != root && !IS_ROOT(d)) {
		parent = dget_parent(d);
		dput(d);
		d = parent;
		if (set->count == capacity) {
			if (capacity >= PKM_KACS_PIN_MAX_DEPTH) {
				*error = -ELOOP;
				break;
			}
			capacity *= 2;
			grown = krealloc(set,
					 struct_size(set, inodes, capacity),
					 GFP_KERNEL);
			if (!grown) {
				*error = -ENOMEM;
				break;
			}
			set = grown;
		}
		inode = pkm_kacs_nt_record_inode_for_dentry(d);
		if (!inode) {
			inode = d_inode(d);
			ihold(inode);
		}
		atomic_inc(&pkm_kacs_inode(inode)->nt_pins);
		set->inodes[set->count++] = inode;
	}
	dput(d);

	if (*error || read_seqretry(&rename_lock, seq)) {
		pkm_kacs_pin_set_drop(set);
		return NULL;
	}
	return set;
}

int pkm_kacs_pin_ancestors_for_open(struct file *file, u32 how_flags)
{
	struct pkm_kacs_file_security *sec;
	struct pkm_kacs_pin_set *set;
	int attempt;
	int error;

	if (!(how_flags & KACS_OPEN_PIN_ANCESTORS))
		return 0;
	if (!file || !file->f_security)
		return -EINVAL;
	sec = pkm_kacs_file(file);
	if (sec->pins)
		return 0;

	for (attempt = 0; attempt < 8; attempt++) {
		set = pkm_kacs_pin_walk(file, &error);
		if (set) {
			sec->pins = set;
			return 0;
		}
		if (error)
			return error;
		/* A rename moved a directory meanwhile: walk again. */
	}
	return -EBUSY;
}

void pkm_kacs_pin_release(struct file *file)
{
	struct pkm_kacs_file_security *sec;

	if (!file || !file->f_security)
		return;
	sec = pkm_kacs_file(file);
	if (!sec->pins)
		return;
	pkm_kacs_pin_set_drop(sec->pins);
	sec->pins = NULL;
}

bool pkm_kacs_pin_file_pinned(struct file *file)
{
	return file && file->f_security && pkm_kacs_file(file)->pins;
}

bool pkm_kacs_pin_dentry_pinned(struct dentry *dentry)
{
	struct inode *record;
	bool pinned;

	if (!dentry || !d_really_is_positive(dentry) || !d_is_dir(dentry))
		return false;
	record = pkm_kacs_nt_record_inode_for_dentry(dentry);
	if (!record) {
		record = d_inode(dentry);
		ihold(record);
	}
	pinned = record->i_security &&
		 atomic_read(&pkm_kacs_inode(record)->nt_pins) != 0;
	iput(record);
	return pinned;
}
