// SPDX-License-Identifier: GPL-2.0-only
/*
 * Operations through an open handle (TRM "KACS-Native Open", "Sharing and
 * Deletion"): reading back what an open was granted, setting its file's
 * delete disposition, and renaming the link it names.
 *
 * Each is authorized by the handle's granted mask, which was checked when
 * the handle was opened -- including rights granted through the parent --
 * and by its share mode, which was checked then against the file's other
 * opens.
 */

#include <linux/dcache.h>
#include <linux/file.h>
#include <linux/filelock.h>
#include <linux/fs.h>
#include <linux/kacs_stratafs.h>
#include <linux/mount.h>
#include <linux/namei.h>
#include <linux/security.h>
#include <linux/syscalls.h>
#include <linux/uaccess.h>

#include <pkm/file.h>
#include <pkm/sd.h>

#include "lsm_internal.h"
#include "nt_file.h"
#include "nt_lease.h"
#include "nt_pin.h"
#include "sattr.h"
#include "token_runtime.h"

/* A managed, non-O_PATH open, or an error for the caller to return. */
static long pkm_kacs_handle_file_security(struct file *file,
					  struct pkm_kacs_file_security **out)
{
	struct pkm_kacs_file_security *sec;

	if (!file->f_security || (file->f_mode & FMODE_PATH))
		return -EOPNOTSUPP;
	sec = pkm_kacs_file(file);
	if (!sec->managed)
		return -EOPNOTSUPP;
	*out = sec;
	return 0;
}

SYSCALL_DEFINE3(kacs_query_open, int, fd, struct kacs_open_info __user *, uinfo,
		size_t, size)
{
	struct pkm_kacs_file_security *sec;
	struct kacs_open_info info = {};
	struct inode *record;
	long ret;

	if (!uinfo || size < KACS_OPEN_INFO_MIN_SIZE)
		return -EINVAL;

	CLASS(fd, f)(fd);
	if (fd_empty(f))
		return -EBADF;
	ret = pkm_kacs_handle_file_security(fd_file(f), &sec);
	if (ret)
		return ret;

	info.granted_access = sec->granted_access;
	info.share_access = sec->nt_classes ? sec->nt_share : PKM_KACS_NT_ALL;
	info.flags = KACS_OPEN_INFO_MANAGED;
	if (sec->delete_on_close)
		info.flags |= KACS_OPEN_INFO_DELETE_ON_CLOSE;
	if (pkm_kacs_pin_file_pinned(fd_file(f)))
		info.flags |= KACS_OPEN_INFO_ANCESTORS_PINNED;
	record = pkm_kacs_nt_record_inode_for_file(fd_file(f));
	if (record) {
		if (pkm_kacs_nt_delete_pending(record))
			info.flags |= KACS_OPEN_INFO_DELETE_PENDING;
		iput(record);
	}

	return copy_struct_to_user(uinfo, size, &info, sizeof(info), NULL);
}

#define PKM_KACS_DISPOSITION_FLAGS                                    \
	(KACS_DISPOSITION_DELETE | KACS_DISPOSITION_POSIX_SEMANTICS | \
	 KACS_DISPOSITION_ON_CLOSE | KACS_DISPOSITION_IGNORE_READONLY)

SYSCALL_DEFINE2(kacs_set_disposition, int, fd, u32, flags)
{
	struct pkm_kacs_file_security *sec;
	const void *subject_token;
	struct inode *record;
	struct inode *inode;
	struct file *file;
	bool deleting = (flags & KACS_DISPOSITION_DELETE) != 0;
	long ret;

	if (flags & ~PKM_KACS_DISPOSITION_FLAGS)
		return -EINVAL;
	if ((flags & KACS_DISPOSITION_POSIX_SEMANTICS) &&
	    (!deleting || (flags & KACS_DISPOSITION_ON_CLOSE)))
		return -EINVAL;

	CLASS(fd, f)(fd);
	if (fd_empty(f))
		return -EBADF;
	file = fd_file(f);
	ret = pkm_kacs_handle_file_security(file, &sec);
	if (ret)
		return ret;
	if (!(sec->granted_access & KACS_ACCESS_DELETE))
		return -EACCES;
	inode = file_inode(file);
	if (!S_ISREG(inode->i_mode) && !S_ISDIR(inode->i_mode))
		return -EOPNOTSUPP;
	subject_token = pkm_kacs_current_effective_token_ptr();
	if (!subject_token)
		return -EACCES;

	/* A read-only regular file is not deleted unless set aside. */
	if (deleting && S_ISREG(inode->i_mode) &&
	    pkm_kacs_sattr_file_readonly(file)) {
		if (!(flags & KACS_DISPOSITION_IGNORE_READONLY))
			return -EPERM;
		if (!(sec->granted_access & KACS_FILE_WRITE_ATTRIBUTES))
			return -EACCES;
	}

	if (flags & KACS_DISPOSITION_ON_CLOSE) {
		/* This open's own obligation, carried out as it closes. */
		if (deleting && !sec->delete_on_close) {
			sec->delete_on_close_token =
				kacs_rust_token_clone(subject_token);
			sec->delete_on_close = 1;
		} else if (!deleting && sec->delete_on_close) {
			sec->delete_on_close = 0;
			kacs_rust_token_drop(sec->delete_on_close_token);
			sec->delete_on_close_token = NULL;
		}
		return 0;
	}

	record = pkm_kacs_nt_record_inode_for_file(file);
	if (!record)
		return -EOPNOTSUPP;
	if (!deleting) {
		pkm_kacs_nt_clear_delete_pending(record);
		ret = 0;
		goto out;
	}

	/* Other holders' handle caching goes before the file does. */
	pkm_kacs_lease_break_inode(record, KACS_LEASE_BREAK_DELETE, file);
	if (flags & KACS_DISPOSITION_POSIX_SEMANTICS)
		ret = pkm_kacs_nt_remove_now(&file->f_path,
					     d_inode(file->f_path.dentry),
					     record, subject_token);
	else
		ret = pkm_kacs_nt_mark_delete_pending(record, &file->f_path,
						      subject_token);
out:
	iput(record);
	return ret;
}

#define PKM_KACS_RENAME_FLAGS                                          \
	(KACS_RENAME_REPLACE_IF_EXISTS | KACS_RENAME_POSIX_SEMANTICS | \
	 KACS_RENAME_IGNORE_READONLY)

/*
 * A file the rename would replace (TRM "Renaming through a handle"):
 * never a directory; not read-only unless set aside; not delete-pending;
 * and not open, unless POSIX semantics are asked and its opens all share
 * delete.
 */
static long pkm_kacs_rename_check_target(struct dentry *target, u32 flags)
{
	struct pkm_kacs_nt_state *state;
	struct inode *record;
	long ret = 0;

	if (d_is_dir(target))
		return -EISDIR;
	if (!(flags & KACS_RENAME_IGNORE_READONLY) &&
	    pkm_kacs_sattr_dentry_readonly(target))
		return -EPERM;

	record = pkm_kacs_nt_record_inode_for_dentry(target);
	if (!record)
		return 0;
	if (flags & KACS_RENAME_POSIX_SEMANTICS) {
		ret = pkm_kacs_nt_check_delete_by_name(record);
	} else {
		state = pkm_kacs_nt_state(record, false);
		if (state) {
			spin_lock(&state->lock);
			if (state->opens || state->delete_pending ||
			    state->deleting)
				ret = -EBUSY;
			spin_unlock(&state->lock);
		}
	}
	iput(record);
	return ret;
}

#if IS_ENABLED(CONFIG_STRATAFS_FS)
/*
 * Look up and lock a StrataFS handle's link for renaming (TRM "Renaming
 * through a handle"). The open's dentry is not kept current, so the name
 * comes from the provider and is looked up as rename(2) would; EAGAIN if
 * it no longer reaches that provider, as when a rename moved it meanwhile.
 * On success @old_parent holds the parent and @provider the provider's
 * inode, both referenced.
 */
static long pkm_kacs_rename_start_stratafs(struct file *file,
					   struct renamedata *rd,
					   struct qstr *new_last,
					   struct path *old_parent,
					   struct inode **provider)
{
	struct inode *record;
	struct qstr old_last;
	char *name = NULL;
	long ret;

	ret = stratafs_kacs_handle_name(file, old_parent, &name, provider);
	if (ret)
		return ret;
	rd->old_parent = old_parent->dentry;
	old_last = (struct qstr)QSTR_INIT(name, strlen(name));
	ret = start_renaming(rd, 0, &old_last, new_last);
	kfree(name);
	if (!ret) {
		record = pkm_kacs_nt_record_inode_for_dentry(rd->old_dentry);
		if (record != *provider) {
			end_renaming(rd);
			ret = -EAGAIN;
		}
		if (record)
			iput(record);
	}
	if (ret) {
		iput(*provider);
		*provider = NULL;
		path_put(old_parent);
		*old_parent = (struct path){};
	}
	return ret;
}
#endif

SYSCALL_DEFINE4(kacs_rename, int, fd, int, newdirfd, const char __user *,
		newpath, u32, flags)
{
	struct pkm_kacs_task_security *task_sec;
	struct pkm_kacs_file_security *sec;
	struct delegated_inode delegated = {};
	struct renamedata rd = {};
	struct path new_parent = {};
	struct path old_parent = {};
	struct inode *provider = NULL;
	struct qstr last;
	struct file *file;
	bool stratafs;
	int attempt = 0;
	int type;
	long ret;

	if (flags & ~PKM_KACS_RENAME_FLAGS)
		return -EINVAL;
	if (!current->security)
		return -EACCES;

	CLASS(fd, f)(fd);
	if (fd_empty(f))
		return -EBADF;
	file = fd_file(f);
	ret = pkm_kacs_handle_file_security(file, &sec);
	if (ret)
		return ret;
	if (!(sec->granted_access & KACS_ACCESS_DELETE))
		return -EACCES;

	CLASS(filename, name)(newpath);
	ret = pkm_filename_parentat(newdirfd, name, 0, &new_parent, &last,
				    &type);
	if (ret)
		return ret;
	if (type != LAST_NORM) {
		ret = -EINVAL;
		goto out_parent;
	}
	if (new_parent.mnt != file->f_path.mnt) {
		ret = -EXDEV;
		goto out_parent;
	}
	ret = mnt_want_write(new_parent.mnt);
	if (ret)
		goto out_parent;

	stratafs = file->f_path.dentry->d_sb->s_magic == STRATAFS_SUPER_MAGIC;
	task_sec = pkm_kacs_task(current);
retry:
	rd = (struct renamedata){
		.mnt_idmap = mnt_idmap(new_parent.mnt),
		.new_parent = new_parent.dentry,
		.delegated_inode = &delegated,
		.flags = (flags & KACS_RENAME_REPLACE_IF_EXISTS) ?
				 0 :
				 RENAME_NOREPLACE,
	};
	if (stratafs) {
#if IS_ENABLED(CONFIG_STRATAFS_FS)
		ret = pkm_kacs_rename_start_stratafs(file, &rd, &last,
						     &old_parent, &provider);
		if (ret == -EAGAIN && ++attempt < 8)
			goto retry;
		/* Still not the handle's: its name is masked or gone. */
		if (ret == -EAGAIN)
			ret = -ENOENT;
#else
		ret = -EOPNOTSUPP;
#endif
	} else if (d_unhashed(file->f_path.dentry)) {
		/* The link this handle names has been removed. */
		ret = -ENOENT;
	} else {
		ret = start_renaming_dentry(&rd, 0, file->f_path.dentry, &last);
		if (!ret)
			old_parent = (struct path){ .mnt = file->f_path.mnt,
						    .dentry = rd.old_parent };
	}
	if (ret)
		goto out_write;
	if (d_is_positive(rd.new_dentry) && rd.new_dentry != rd.old_dentry) {
		ret = (flags & KACS_RENAME_REPLACE_IF_EXISTS) ?
			      pkm_kacs_rename_check_target(rd.new_dentry,
							   flags) :
			      -EEXIST;
		if (ret)
			goto out_end;
	}
	ret = security_path_rename(&old_parent, rd.old_dentry, &new_parent,
				   rd.new_dentry, rd.flags);
	if (ret)
		goto out_end;

	/*
	 * Below StrataFS the rename the hooks judge is the provider's, on a
	 * dentry of StrataFS's choosing: the handle is named by inode alone.
	 */
	task_sec->handle_rename_dentry = stratafs ? NULL : rd.old_dentry;
	task_sec->handle_rename_inode = stratafs ? provider :
						   d_inode(rd.old_dentry);
	pkm_kacs_lease_set_breaker_file(file);
	ret = vfs_rename(&rd);
	pkm_kacs_lease_set_breaker_file(NULL);
	task_sec->handle_rename_dentry = NULL;
	task_sec->handle_rename_inode = NULL;
out_end:
	end_renaming(&rd);
	if (stratafs) {
		iput(provider);
		provider = NULL;
		path_put(&old_parent);
	}
	old_parent = (struct path){};
	if (is_delegated(&delegated)) {
		ret = break_deleg_wait(&delegated);
		if (!ret)
			goto retry;
	}
out_write:
	mnt_drop_write(new_parent.mnt);
out_parent:
	path_put(&new_parent);
	return ret;
}
