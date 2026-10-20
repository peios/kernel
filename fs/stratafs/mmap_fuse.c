// SPDX-License-Identifier: GPL-2.0-only

#include <linux/file.h>
#include <linux/magic.h>

#include "stratafs.h"

/*
 * Keep the FUSE-private layout dependency in this adapter. Recheck it when
 * updating FUSE: successful open fixes passthrough/cred until final release,
 * and fuse_file_mmap chooses DAX before passthrough. No FUSE symbols are
 * called, so this also works when FUSE is a module and StrataFS is built in.
 */
#include "../fuse/fuse_i.h"

#ifdef CONFIG_STRATAFS_KUNIT_TEST
#include <kunit/test.h>
#include <linux/mman.h>
#endif

struct file *stratafs_fuse_mmap_file_get(struct file *file,
					 const struct cred **cred)
{
	struct inode *inode = file_inode(file);
	struct fuse_file *ff;
	struct file *real;

	if (inode->i_sb->s_magic != FUSE_SUPER_MAGIC ||
	    !S_ISREG(inode->i_mode) || FUSE_IS_DAX(inode))
		return NULL;
	ff = file->private_data;
	if (!ff)
		return NULL;
	real = fuse_file_passthrough(ff);
	if (!real)
		return NULL;

	/* The caller's outer-file reference excludes FUSE's final release. */
	*cred = get_cred(ff->cred);
	return get_file(real);
}

#ifdef CONFIG_STRATAFS_KUNIT_TEST
struct stratafs_fuse_mmap_fixture {
	struct super_block sb;
	struct inode inode;
	struct file file[2];
	struct fuse_file ff[2];
	struct super_block leaf_sb;
	struct inode leaf_inode;
	struct file leaf;
	struct super_block strata_sb;
	struct stratafs_sb_info sbi;
	struct inode strata_inode;
	struct file strata_file;
	struct stratafs_file_info info;
	struct cred *cred;
};

static void stratafs_fuse_mmap_cleanup(void *data)
{
	struct stratafs_fuse_mmap_fixture *f = data;

	put_cred(f->cred);
}

static struct stratafs_fuse_mmap_fixture *
stratafs_fuse_mmap_fixture(struct kunit *test)
{
	struct stratafs_fuse_mmap_fixture *f;
	unsigned int i;

	f = kunit_kzalloc(test, sizeof(*f), GFP_KERNEL);
	if (!f)
		return NULL;
	f->cred = prepare_creds();
	if (!f->cred)
		return NULL;
	if (kunit_add_action_or_reset(test, stratafs_fuse_mmap_cleanup, f))
		return NULL;
	f->sb.s_magic = FUSE_SUPER_MAGIC;
	f->inode.i_sb = &f->sb;
	f->inode.i_mode = S_IFREG | 0600;
	file_ref_init(&f->leaf.f_ref, 1);
	f->leaf_inode.i_sb = &f->leaf_sb;
	f->leaf_inode.i_mode = S_IFREG | 0600;
	f->leaf.f_inode = &f->leaf_inode;
	for (i = 0; i < ARRAY_SIZE(f->file); i++) {
		/* Synthetic files retain their fixture-owned initial reference. */
		file_ref_init(&f->file[i].f_ref, 1);
		f->file[i].f_inode = &f->inode;
		f->file[i].f_mode = FMODE_READ | FMODE_WRITE;
		f->file[i].private_data = &f->ff[i];
		f->ff[i].passthrough = &f->leaf;
		f->ff[i].cred = f->cred;
	}
	return f;
}

static void stratafs_kunit_fuse_mmap_pins_forwarding_tuple(struct kunit *test)
{
	struct stratafs_fuse_mmap_fixture *f = stratafs_fuse_mmap_fixture(test);
	const struct cred *cred = NULL;
	struct file *real;

	KUNIT_ASSERT_NOT_NULL(test, f);
	real = stratafs_fuse_mmap_file_get(&f->file[0], &cred);
	KUNIT_EXPECT_PTR_EQ(test, real, &f->leaf);
	KUNIT_EXPECT_PTR_EQ(test, cred, f->cred);
	KUNIT_EXPECT_EQ(test, file_count(&f->leaf), 2UL);
	fput(real);
	put_cred(cred);
	KUNIT_EXPECT_EQ(test, file_count(&f->leaf), 1UL);
}

static void stratafs_kunit_fuse_mmap_ignores_other_paths(struct kunit *test)
{
	struct stratafs_fuse_mmap_fixture *f = stratafs_fuse_mmap_fixture(test);
	const struct cred *cred = NULL;

	KUNIT_ASSERT_NOT_NULL(test, f);
	f->sb.s_magic = 0;
	KUNIT_EXPECT_PTR_EQ(
		test, stratafs_fuse_mmap_file_get(&f->file[0], &cred), NULL);
	f->sb.s_magic = FUSE_SUPER_MAGIC;
	f->inode.i_mode = S_IFDIR | 0700;
	KUNIT_EXPECT_PTR_EQ(
		test, stratafs_fuse_mmap_file_get(&f->file[0], &cred), NULL);
	f->inode.i_mode = S_IFREG | 0600;
	f->file[0].f_mode = FMODE_READ;
	KUNIT_EXPECT_EQ(test, stratafs_prepare_mmap(&f->file[0], MAP_SHARED),
			0);
	f->file[0].f_mode = FMODE_READ | FMODE_WRITE;
	if (IS_ENABLED(CONFIG_FUSE_DAX)) {
		f->inode.i_flags |= S_DAX;
		KUNIT_EXPECT_PTR_EQ(
			test, stratafs_fuse_mmap_file_get(&f->file[0], &cred),
			NULL);
		f->inode.i_flags &= ~S_DAX;
	}
	f->ff[0].passthrough = NULL;
	KUNIT_EXPECT_PTR_EQ(
		test, stratafs_fuse_mmap_file_get(&f->file[0], &cred), NULL);
	KUNIT_EXPECT_PTR_EQ(test, cred, NULL);
	KUNIT_EXPECT_EQ(test, file_count(&f->leaf), 1UL);
}

static void
stratafs_kunit_fuse_mmap_prepares_selected_strata(struct kunit *test)
{
	struct stratafs_fuse_mmap_fixture *f = stratafs_fuse_mmap_fixture(test);
	const struct cred *cred = current_cred();

	KUNIT_ASSERT_NOT_NULL(test, f);
	f->strata_sb.s_fs_info = &f->sbi;
	f->strata_sb.s_flags = SB_RDONLY;
	f->sbi.create_index = -1;
	f->strata_inode.i_sb = &f->strata_sb;
	f->strata_inode.i_mode = S_IFREG | 0600;
	file_ref_init(&f->strata_file.f_ref, 1);
	f->strata_file.f_inode = &f->strata_inode;
	f->strata_file.f_op = &stratafs_file_operations;
	f->strata_file.private_data = &f->info;
	mutex_init(&f->info.mutation_lock);
	f->ff[0].passthrough = &f->strata_file;
	/* The inner refusal must be reached before the outer mmap callback. */
	KUNIT_EXPECT_EQ(test,
			stratafs_prepare_mmap(&f->file[0], MAP_SHARED_VALIDATE),
			-EROFS);
	KUNIT_EXPECT_PTR_EQ(test, current_cred(), cred);
	KUNIT_EXPECT_EQ(test, file_count(&f->strata_file), 1UL);
	KUNIT_EXPECT_FALSE(test, mutex_is_locked(&f->info.mutation_lock));
}

static void stratafs_kunit_fuse_mmap_bounds_wrapper_cycles(struct kunit *test)
{
	struct stratafs_fuse_mmap_fixture *f = stratafs_fuse_mmap_fixture(test);
	const struct cred *cred = current_cred();

	KUNIT_ASSERT_NOT_NULL(test, f);
	f->ff[0].passthrough = &f->file[1];
	/* Two wrappers may finish at a plain leaf at the depth limit. */
	KUNIT_EXPECT_EQ(test, stratafs_prepare_mmap(&f->file[0], MAP_SHARED),
			0);
	KUNIT_EXPECT_PTR_EQ(test, current_cred(), cred);
	KUNIT_EXPECT_EQ(test, file_count(&f->leaf), 1UL);
	f->ff[1].passthrough = &f->file[0];
	KUNIT_EXPECT_EQ(test, stratafs_prepare_mmap(&f->file[0], MAP_SHARED),
			-ELOOP);
	KUNIT_EXPECT_PTR_EQ(test, current_cred(), cred);
	KUNIT_EXPECT_EQ(test, file_count(&f->file[0]), 1UL);
	KUNIT_EXPECT_EQ(test, file_count(&f->file[1]), 1UL);
}

static struct kunit_case stratafs_fuse_mmap_cases[] = {
	KUNIT_CASE(stratafs_kunit_fuse_mmap_pins_forwarding_tuple),
	KUNIT_CASE(stratafs_kunit_fuse_mmap_ignores_other_paths),
	KUNIT_CASE(stratafs_kunit_fuse_mmap_prepares_selected_strata),
	KUNIT_CASE(stratafs_kunit_fuse_mmap_bounds_wrapper_cycles),
	{}
};

static struct kunit_suite stratafs_fuse_mmap_suite = {
	.name = "stratafs_fuse_mmap",
	.test_cases = stratafs_fuse_mmap_cases,
};

kunit_test_suite(stratafs_fuse_mmap_suite);
#endif
