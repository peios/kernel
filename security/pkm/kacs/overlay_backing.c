// SPDX-License-Identifier: GPL-2.0-only

#include <linux/err.h>
#include <linux/file.h>
#include <linux/fs.h>
#include <linux/magic.h>
#include <linux/mount.h>
#include <linux/string.h>

#include "overlay_backing.h"

#if IS_ENABLED(CONFIG_OVERLAY_FS)
/*
 * Keep the private layout dependency here. The unpublished staged open owns
 * of->realfile until release; no other caller can install of->upperfile.
 * Recheck these invariants when updating OverlayFS. Do not call OVL_FS():
 * its DEBUG assertion references an unexported symbol when OverlayFS=m.
 */
#include "../../../fs/overlayfs/ovl_entry.h"

struct file *pkm_kacs_copy_up_overlay_child_get(struct file *file)
{
	struct inode *inode = file_inode(file);
	const struct path *user_path;
	struct super_block *sb = inode->i_sb;
	struct ovl_fs *ofs;
	struct ovl_file *of;
	struct dentry *upper;
	struct file *child;

	if (sb->s_magic != OVERLAYFS_SUPER_MAGIC)
		return NULL;
	/* Establish filesystem and regular-file identity before private casts. */
	if (!sb->s_type || strcmp(sb->s_type->name, "overlay") ||
	    !S_ISREG(inode->i_mode) || !file->f_op ||
	    file->f_op != inode->i_fop || (file->f_mode & FMODE_PATH))
		return ERR_PTR(-ESTALE);
	ofs = sb->s_fs_info;
	of = file->private_data;
	if (!ofs || !ofs->layers || !ofs->numlayer || !of || of->upperfile)
		return ERR_PTR(-ESTALE);
	upper = ovl_upperdentry_dereference(OVL_I(inode));
	child = of->realfile;
	if (!upper || !d_inode(upper) || !child ||
	    !(child->f_mode & FMODE_BACKING) || (child->f_mode & FMODE_PATH) ||
	    !file_inode(child) || !S_ISREG(file_inode(child)->i_mode) ||
	    child->f_path.dentry != upper ||
	    child->f_path.mnt != ovl_upper_mnt(ofs) || !child->f_path.mnt ||
	    file_inode(child) != d_inode(upper))
		return ERR_PTR(-ESTALE);
	user_path = backing_file_user_path(child);
	if (!path_equal(user_path, &file->f_path) || !user_path->dentry ||
	    d_inode(user_path->dentry) != inode)
		return ERR_PTR(-ESTALE);

	/* Parent ownership pins the child while we acquire our temporary pin. */
	return get_file(child);
}
#else
struct file *pkm_kacs_copy_up_overlay_child_get(struct file *file)
{
	return NULL;
}
#endif
