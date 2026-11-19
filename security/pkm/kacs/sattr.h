/* SPDX-License-Identifier: GPL-2.0-only */
#ifndef _SECURITY_PKM_KACS_SATTR_H
#define _SECURITY_PKM_KACS_SATTR_H

#include <linux/fs.h>
#include <linux/types.h>

/*
 * KACS special attributes (TRM "Special Attributes"): the read-only flag
 * KACS enforces for every process, and the settable Created At date, held
 * in the security.peios.sattr extended attribute.
 */

bool pkm_kacs_is_sattr_xattr(const char *name);

/* Whether a regular file is marked read-only. */
bool pkm_kacs_sattr_file_readonly(struct file *file);
bool pkm_kacs_sattr_dentry_readonly(struct dentry *dentry);

/* Validate a value written to the attribute. */
int pkm_kacs_sattr_validate(const void *value, size_t size, int flags);

/* A write or removal landed: the cached read-only state is stale. */
void pkm_kacs_sattr_invalidate(struct inode *inode);

/*
 * The attribute's writes, called from do_setxattr() and removexattr() in
 * place of the raw xattr operations: a write merges the fields it names
 * into the stored value.
 */
int pkm_kacs_sattr_vfs_set(struct mnt_idmap *idmap, struct dentry *dentry,
			   const void *value, size_t size, int flags);
int pkm_kacs_sattr_vfs_remove(struct mnt_idmap *idmap, struct dentry *dentry);

#endif /* _SECURITY_PKM_KACS_SATTR_H */
