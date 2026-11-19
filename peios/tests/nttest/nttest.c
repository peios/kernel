// PEI-1720 runtime checks for the NT handle semantics kernel batch.
// Runs as SYSTEM in the Peios test VM against a directory on a managed
// mount. Prints one line per check: PASS or FAIL, and a summary.
//
// A stopgap until these checks are Provium Lua tests (PEI-1744); see
// README.md. Build from the repository root:
//   gcc -static -O2 -Wall -idirafter include/uapi
//       peios/tests/nttest/nttest.c -o nttest
#define _GNU_SOURCE
#include <errno.h>
#include <fcntl.h>
#include <poll.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/syscall.h>
#include <sys/klog.h>
#include <sys/mount.h>
#include <sys/wait.h>
#include <sys/xattr.h>
#include <unistd.h>

#include <pkm/file.h>
#include <pkm/sd.h>
#include <pkm/syscall.h>

static int failures, checks;
static const char *dir;

#define CHECK(cond, ...)                                                      \
	do {                                                                  \
		checks++;                                                     \
		if (cond) {                                                   \
			printf("PASS ");                                      \
		} else {                                                      \
			printf("FAIL ");                                      \
			failures++;                                           \
		}                                                             \
		printf(__VA_ARGS__);                                          \
		printf(" (errno %d %s)\n", errno, strerror(errno));          \
		fflush(stdout);                                               \
	} while (0)

static char *at(const char *name)
{
	static char buf[8][512];
	static int i;
	char *b = buf[i++ % 8];

	snprintf(b, 512, "%s/%s", dir, name);
	return b;
}

static int kopen(const char *path, uint32_t access, uint32_t disp,
		 uint32_t options, uint32_t flags, uint32_t share,
		 uint32_t *status)
{
	struct kacs_open_how how = {
		.desired_access = access,
		.create_disposition = disp,
		.create_options = options,
		.flags = flags,
		.share_access = share,
	};
	uint32_t st = 0;
	long fd = syscall(SYS_KACS_OPEN, AT_FDCWD, path, &how, sizeof(how), &st);

	if (status)
		*status = st;
	return (int)fd;
}

static int kopen_sd(const char *path, uint32_t access, uint32_t disp,
		    const void *sd, uint32_t sd_len)
{
	struct kacs_open_how how = {
		.desired_access = access,
		.create_disposition = disp,
		.sd_ptr = (uint64_t)(uintptr_t)sd,
		.sd_len = sd_len,
	};
	uint32_t st = 0;

	return (int)syscall(SYS_KACS_OPEN, AT_FDCWD, path, &how, sizeof(how),
			    &st);
}

static int kopen_lease(const char *path, uint32_t access, int mgr,
		       const uint8_t key[16])
{
	struct kacs_open_how how = {
		.desired_access = access,
		.create_disposition = KACS_DISPOSITION_OPEN,
		.flags = KACS_OPEN_LEASE_KEY,
		.lease_fd = mgr,
	};
	uint32_t st = 0;

	memcpy(how.lease_key, key, 16);
	return (int)syscall(SYS_KACS_OPEN, AT_FDCWD, path, &how, sizeof(how),
			    &st);
}

static int query(int fd, struct kacs_open_info *info)
{
	memset(info, 0, sizeof(*info));
	return (int)syscall(SYS_KACS_QUERY_OPEN, fd, info, sizeof(*info));
}

static int set_disposition(int fd, uint32_t flags)
{
	return (int)syscall(SYS_KACS_SET_DISPOSITION, fd, flags);
}

static int krename(int fd, const char *newpath, uint32_t flags)
{
	return (int)syscall(SYS_KACS_RENAME, fd, AT_FDCWD, newpath, flags);
}

static int klock(int fd, uint32_t op, uint64_t off, uint64_t len,
		 uint32_t flags, uint64_t cookie)
{
	struct kacs_lock_args a = {
		.offset = off, .length = len, .op = op, .flags = flags,
		.cookie = cookie,
	};

	return (int)syscall(SYS_KACS_LOCK, fd, &a, sizeof(a));
}

static void mkfile(const char *path, const char *text)
{
	int fd;

	unlink(path);
	fd = open(path, O_WRONLY | O_CREAT | O_TRUNC, 0600);
	if (fd >= 0) {
		if (write(fd, text, strlen(text)) < 0)
			perror("write");
		close(fd);
	}
}

static int exists(const char *path)
{
	struct stat st;

	return lstat(path, &st) == 0;
}

#define RW (KACS_FILE_READ_DATA | KACS_FILE_WRITE_DATA)
#define ALL_SHARE \
	(KACS_FILE_SHARE_READ | KACS_FILE_SHARE_WRITE | KACS_FILE_SHARE_DELETE)

static void test_control_handle(void)
{
	struct kacs_open_info info;
	char c;
	int fd;

	mkfile(at("control"), "x");
	fd = kopen(at("control"), KACS_ACCESS_READ_CONTROL,
		   KACS_DISPOSITION_OPEN, 0, 0, 0, NULL);
	CHECK(fd >= 0, "control handle: READ_CONTROL alone opens");
	if (fd < 0)
		return;
	errno = 0;
	CHECK(read(fd, &c, 1) < 0 && errno == EBADF,
	      "control handle: reading it fails with EBADF");
	CHECK(query(fd, &info) == 0 &&
		      info.granted_access == KACS_ACCESS_READ_CONTROL &&
		      (info.flags & KACS_OPEN_INFO_MANAGED),
	      "kacs_query_open reports the granted mask 0x%x", info.granted_access);
	close(fd);

	fd = kopen(at("control"), KACS_ACCESS_MAXIMUM_ALLOWED,
		   KACS_DISPOSITION_OPEN, 0, 0, 0, NULL);
	CHECK(fd >= 0, "MAXIMUM_ALLOWED alone opens");
	if (fd >= 0) {
		CHECK(query(fd, &info) == 0 &&
			      (info.granted_access & KACS_FILE_READ_DATA) &&
			      read(fd, &c, 1) == 1,
		      "MAXIMUM_ALLOWED's mode follows the maximum (0x%x)",
		      info.granted_access);
		close(fd);
	}
}

static void test_share_modes(void)
{
	uint32_t status = 0;
	int a, b;

	mkfile(at("share"), "data");
	a = kopen(at("share"), KACS_FILE_READ_DATA, KACS_DISPOSITION_OPEN, 0,
		  KACS_OPEN_SHARE_ACCESS, KACS_FILE_SHARE_READ, NULL);
	CHECK(a >= 0, "share: a reader denying write and delete opens");
	if (a < 0)
		return;
	errno = 0;
	b = open(at("share"), O_WRONLY);
	CHECK(b < 0 && errno == EBUSY,
	      "share: a legacy writer is refused with EBUSY");
	if (b >= 0)
		close(b);
	b = open(at("share"), O_RDONLY);
	CHECK(b >= 0, "share: a legacy reader is admitted");
	if (b >= 0)
		close(b);
	errno = 0;
	b = kopen(at("share"), KACS_FILE_WRITE_DATA, KACS_DISPOSITION_OPEN, 0, 0,
		  0, &status);
	CHECK(b < 0 && errno == EBUSY &&
		      status == KACS_STATUS_SHARING_VIOLATION,
	      "share: a native writer gets EBUSY and SHARING_VIOLATION (0x%x)",
	      status);
	if (b >= 0)
		close(b);
	errno = 0;
	CHECK(unlink(at("share")) < 0 && errno == EBUSY,
	      "share: unlink by name is refused while delete is not shared");
	errno = 0;
	CHECK(rename(at("share"), at("share2")) < 0 && errno == EBUSY,
	      "share: rename by name is refused too");
	close(a);
	CHECK(unlink(at("share")) == 0, "share: unlink succeeds after close");

	/* An attribute-only open never conflicts. */
	mkfile(at("share3"), "x");
	a = kopen(at("share3"), RW, KACS_DISPOSITION_OPEN, 0,
		  KACS_OPEN_SHARE_ACCESS, 0, NULL);
	b = kopen(at("share3"), KACS_FILE_READ_ATTRIBUTES,
		  KACS_DISPOSITION_OPEN, 0, 0, 0, NULL);
	CHECK(a >= 0 && b >= 0,
	      "share: an attribute-only open passes an exclusive open");
	if (a >= 0)
		close(a);
	if (b >= 0)
		close(b);
}

static void test_delete_pending(void)
{
	uint32_t status = 0;
	int a, b, b2, r;
	char c;

	mkfile(at("pending"), "x");
	a = kopen(at("pending"), KACS_FILE_READ_DATA | KACS_ACCESS_DELETE,
		  KACS_DISPOSITION_OPEN, 0, 0, 0, NULL);
	b = open(at("pending"), O_RDONLY);
	CHECK(a >= 0 && b >= 0, "pending: two opens");
	if (a < 0 || b < 0)
		return;
	CHECK(set_disposition(a, KACS_DISPOSITION_DELETE) == 0,
	      "pending: kacs_set_disposition marks the file");
	CHECK(exists(at("pending")), "pending: the name stays");
	errno = 0;
	CHECK(kopen(at("pending"), KACS_FILE_READ_DATA, KACS_DISPOSITION_OPEN, 0,
		    0, 0, &status) < 0 &&
		      errno == EBUSY && status == KACS_STATUS_DELETE_PENDING,
	      "pending: a new native open gets EBUSY and DELETE_PENDING (0x%x)",
	      status);
	errno = 0;
	CHECK(open(at("pending"), O_RDONLY) < 0 && errno == EBUSY,
	      "pending: a legacy open gets EBUSY");
	errno = 0;
	CHECK(open(at("pending"), O_PATH) < 0 && errno == EBUSY,
	      "pending: an O_PATH open gets EBUSY");
	r = set_disposition(a, 0);
	b2 = open(at("pending"), O_RDONLY | O_CLOEXEC);
	CHECK(r == 0 && b2 >= 0,
	      "pending: clearing the mark admits opens again");
	if (b2 >= 0)
		close(b2);
	CHECK(set_disposition(a, KACS_DISPOSITION_DELETE) == 0,
	      "pending: marked again");
	close(a);
	CHECK(exists(at("pending")), "pending: the name stays while one open remains");
	CHECK(read(b, &c, 1) == 1, "pending: the remaining open still reads");
	close(b);
	CHECK(!exists(at("pending")), "pending: the last close removes it");

	/* Delete-on-close: pending as the open closes. */
	mkfile(at("doc"), "x");
	a = kopen(at("doc"), KACS_FILE_READ_DATA | KACS_ACCESS_DELETE,
		  KACS_DISPOSITION_OPEN, KACS_CREATE_OPT_DELETE_ON_CLOSE, 0, 0,
		  NULL);
	b = open(at("doc"), O_RDONLY);
	CHECK(a >= 0 && b >= 0,
	      "delete-on-close: another open is admitted while armed");
	if (a >= 0)
		close(a);
	errno = 0;
	CHECK(exists(at("doc")) && open(at("doc"), O_RDONLY) < 0 &&
		      errno == EBUSY,
	      "delete-on-close: closing it leaves the file delete-pending");
	if (b >= 0)
		close(b);
	CHECK(!exists(at("doc")), "delete-on-close: the last close removes it");

	/* POSIX semantics: the name goes at once. */
	mkfile(at("posix"), "y");
	a = kopen(at("posix"), KACS_FILE_READ_DATA | KACS_ACCESS_DELETE,
		  KACS_DISPOSITION_OPEN, 0, 0, 0, NULL);
	CHECK(a >= 0 &&
		      set_disposition(a, KACS_DISPOSITION_DELETE |
						 KACS_DISPOSITION_POSIX_SEMANTICS) ==
			      0 &&
		      !exists(at("posix")) && read(a, &c, 1) == 1,
	      "posix delete: the name goes at once, the handle reads on");
	if (a >= 0)
		close(a);

	/* A directory, empty at its last close. */
	rmdir(at("ddir"));
	mkdir(at("ddir"), 0700);
	a = kopen(at("ddir"), KACS_FILE_LIST_DIRECTORY | KACS_ACCESS_DELETE,
		  KACS_DISPOSITION_OPEN, KACS_CREATE_OPT_DELETE_ON_CLOSE, 0, 0,
		  NULL);
	CHECK(a >= 0, "directory delete-on-close opens");
	if (a >= 0)
		close(a);
	CHECK(!exists(at("ddir")), "directory delete-on-close removes it");
}

/* Directories take part in share modes too, and refuse locks safely. */
static void test_dir_share(void)
{
	struct kacs_lease_args args = { 0 };
	uint8_t key[16] = { 9, 9 };
	int a, b, mgr;
	long r;

	rmdir(at("dshare2"));
	rmdir(at("dshare"));
	mkdir(at("dshare"), 0700);
	a = kopen(at("dshare"), KACS_FILE_LIST_DIRECTORY, KACS_DISPOSITION_OPEN,
		  0, KACS_OPEN_SHARE_ACCESS,
		  KACS_FILE_SHARE_READ | KACS_FILE_SHARE_WRITE, NULL);
	CHECK(a >= 0, "dir share: a directory opens denying delete");
	if (a < 0)
		return;
	errno = 0;
	CHECK(rmdir(at("dshare")) < 0 && errno == EBUSY,
	      "dir share: rmdir by name is refused");
	errno = 0;
	CHECK(rename(at("dshare"), at("dshare2")) < 0 && errno == EBUSY,
	      "dir share: rename by name is refused");
	b = open(at("dshare"), O_RDONLY | O_DIRECTORY);
	CHECK(b >= 0, "dir share: a legacy open of it is admitted");
	if (b >= 0)
		close(b);
	errno = 0;
	CHECK(klock(a, KACS_LOCK_EXCLUSIVE, 0, 1, 0, 0) < 0 &&
		      errno == EOPNOTSUPP,
	      "dir share: kacs_lock on a directory fails with EOPNOTSUPP");
	close(a);

	/* An exclusive open, denying what it holds, must not trip on itself. */
	a = kopen(at("dshare"), KACS_FILE_LIST_DIRECTORY | KACS_ACCESS_DELETE,
		  KACS_DISPOSITION_OPEN, 0, KACS_OPEN_SHARE_ACCESS, 0, NULL);
	CHECK(a >= 0, "dir share: an exclusive directory open succeeds");
	if (a >= 0)
		close(a);

	mgr = (int)syscall(SYS_KACS_CREATE_LEASE_MANAGER,
			   KACS_LEASE_MANAGER_CLOEXEC, 5000);
	a = mgr >= 0 ? kopen_lease(at("dshare"), KACS_FILE_LIST_DIRECTORY, mgr,
				   key) :
		       -1;
	CHECK(a >= 0, "dir share: a directory opens under a lease key");
	if (a >= 0) {
		memcpy(args.lease_key, key, 16);
		args.state = KACS_LEASE_READ | KACS_LEASE_HANDLE;
		errno = 0;
		r = syscall(SYS_KACS_LEASE, a, mgr, &args, sizeof(args));
		CHECK(r == 0 || errno == EOPNOTSUPP,
		      "dir share: a directory lease is granted or refused cleanly (%ld)",
		      r);
		close(a);
	}
	if (mgr >= 0)
		close(mgr);
	CHECK(rmdir(at("dshare")) == 0, "dir share: rmdir once closed");
}

static void test_rename(void)
{
	int fd;

	mkfile(at("ren-a"), "r");
	unlink(at("ren-b"));
	unlink(at("ren-c"));
	fd = kopen(at("ren-a"), KACS_FILE_READ_DATA | KACS_ACCESS_DELETE,
		   KACS_DISPOSITION_OPEN, 0, 0, 0, NULL);
	CHECK(fd >= 0 && krename(fd, at("ren-b"), 0) == 0 &&
		      !exists(at("ren-a")) && exists(at("ren-b")),
	      "kacs_rename moves the handle's link");
	/* Someone renames it by name; the handle follows. */
	CHECK(rename(at("ren-b"), at("ren-x")) == 0, "rename by name");
	CHECK(krename(fd, at("ren-c"), 0) == 0 && exists(at("ren-c")) &&
		      !exists(at("ren-x")),
	      "kacs_rename follows the handle's current name");
	mkfile(at("ren-d"), "d");
	errno = 0;
	CHECK(krename(fd, at("ren-d"), 0) < 0 && errno == EEXIST,
	      "kacs_rename refuses an existing name without REPLACE");
	CHECK(krename(fd, at("ren-d"), KACS_RENAME_REPLACE_IF_EXISTS) == 0,
	      "kacs_rename replaces with REPLACE_IF_EXISTS");
	if (fd >= 0)
		close(fd);

	/* The handle's own share mode does not stand in its way. */
	mkfile(at("ren-e"), "e");
	unlink(at("ren-f"));
	fd = kopen(at("ren-e"), KACS_FILE_READ_DATA | KACS_ACCESS_DELETE,
		   KACS_DISPOSITION_OPEN, 0, KACS_OPEN_SHARE_ACCESS,
		   KACS_FILE_SHARE_READ, NULL);
	CHECK(fd >= 0 && krename(fd, at("ren-f"), 0) == 0 &&
		      exists(at("ren-f")),
	      "kacs_rename works through a handle denying delete to others");
	if (fd >= 0)
		close(fd);

	/* A directory's handle renames it too. */
	rmdir(at("ren-dir2"));
	rmdir(at("ren-dir"));
	mkdir(at("ren-dir"), 0700);
	fd = kopen(at("ren-dir"), KACS_FILE_LIST_DIRECTORY | KACS_ACCESS_DELETE,
		   KACS_DISPOSITION_OPEN, 0, 0, 0, NULL);
	CHECK(fd >= 0 && krename(fd, at("ren-dir2"), 0) == 0 &&
		      exists(at("ren-dir2")) && !exists(at("ren-dir")),
	      "kacs_rename moves a directory through its handle");
	if (fd >= 0)
		close(fd);
}

static void test_locks(void)
{
	char buf[8];
	int a, b;

	mkfile(at("lock"), "0123456789abcdefghijklmnopqrstuvwxyz");
	a = kopen(at("lock"), RW, KACS_DISPOSITION_OPEN, 0, 0, 0, NULL);
	b = open(at("lock"), O_RDWR);
	CHECK(a >= 0 && b >= 0, "locks: two opens");
	if (a < 0 || b < 0)
		return;
	CHECK(klock(a, KACS_LOCK_EXCLUSIVE, 0, 10, 0, 0) == 0,
	      "locks: an exclusive lock on 0-9");
	errno = 0;
	CHECK(pread(b, buf, 4, 2) < 0 && errno == EAGAIN,
	      "locks: another open's read in the range fails with EAGAIN");
	CHECK(pread(b, buf, 4, 20) == 4, "locks: a read outside it works");
	CHECK(pread(a, buf, 4, 2) == 4, "locks: the holder's own read works");
	errno = 0;
	CHECK(klock(b, KACS_LOCK_SHARED, 5, 2, KACS_LOCK_FAIL_IMMEDIATELY, 0) <
			      0 &&
		      errno == EAGAIN,
	      "locks: a conflicting lock with FAIL_IMMEDIATELY fails");
	CHECK(klock(a, KACS_LOCK_UNLOCK, 0, 10, 0, 0) == 0 &&
		      pread(b, buf, 4, 2) == 4,
	      "locks: unlocking admits the read");
	errno = 0;
	CHECK(klock(a, KACS_LOCK_UNLOCK, 0, 10, 0, 0) < 0 && errno == ENOLCK,
	      "locks: unlocking an unheld range fails with ENOLCK");
	CHECK(klock(a, KACS_LOCK_SHARED, 0, 10, 0, 0) == 0, "locks: a shared lock");
	errno = 0;
	CHECK(pwrite(a, "Z", 1, 1) < 0 && errno == EAGAIN,
	      "locks: a shared lock blocks its holder's write");
	CHECK(pread(b, buf, 4, 2) == 4, "locks: but not others' reads");
	errno = 0;
	CHECK(ftruncate(b, 4) < 0 && errno == EAGAIN,
	      "locks: truncating into the range is a write, refused");
	close(a);
	CHECK(pwrite(b, "Z", 1, 1) == 1, "locks: closing the holder releases them");
	close(b);
}

static void test_leases(void)
{
	struct kacs_lease_args args = { 0 };
	struct kacs_lease_break notice;
	uint8_t key[16] = { 1, 7, 2, 0 };
	struct pollfd p;
	pid_t child;
	int mgr, fd, status;

	mkfile(at("lease"), "leased");
	mgr = (int)syscall(SYS_KACS_CREATE_LEASE_MANAGER,
			   KACS_LEASE_MANAGER_CLOEXEC, 5000);
	CHECK(mgr >= 0, "leases: a lease manager");
	if (mgr < 0)
		return;
	fd = kopen_lease(at("lease"), RW, mgr, key);
	CHECK(fd >= 0, "leases: an open under the manager's key");
	if (fd < 0)
		return;
	memcpy(args.lease_key, key, 16);
	args.state = KACS_LEASE_READ | KACS_LEASE_HANDLE | KACS_LEASE_WRITE;
	CHECK(syscall(SYS_KACS_LEASE, fd, mgr, &args, sizeof(args)) == 0 &&
		      args.state == (KACS_LEASE_READ | KACS_LEASE_HANDLE |
				     KACS_LEASE_WRITE),
	      "leases: the sole open is granted RWH (0x%x)", args.state);

	child = fork();
	if (child == 0) {
		/* Another opener: breaks write caching, and waits for it. */
		int o = open(at("lease"), O_RDONLY);

		_exit(o >= 0 ? 0 : 1);
	}
	p.fd = mgr;
	p.events = POLLIN;
	CHECK(poll(&p, 1, 3000) == 1 &&
		      read(mgr, &notice, sizeof(notice)) == sizeof(notice) &&
		      notice.reason == KACS_LEASE_BREAK_OPEN &&
		      notice.new_state ==
			      (KACS_LEASE_READ | KACS_LEASE_HANDLE),
	      "leases: another open raises a break notice to RH (reason %u)",
	      notice.reason);
	CHECK(waitpid(child, &status, WNOHANG) == 0,
	      "leases: the opener waits for the acknowledgement");
	args.flags = KACS_LEASE_ACKNOWLEDGE;
	args.state = KACS_LEASE_READ | KACS_LEASE_HANDLE;
	CHECK(syscall(SYS_KACS_LEASE, fd, mgr, &args, sizeof(args)) == 0,
	      "leases: acknowledging the break");
	CHECK(waitpid(child, &status, 0) == child && WIFEXITED(status) &&
		      WEXITSTATUS(status) == 0,
	      "leases: then the opener proceeds");
	close(fd);
	close(mgr);
}

static void test_readonly(void)
{
	struct kacs_sattr v = {
		.version = KACS_SATTR_VERSION,
		.valid = KACS_SATTR_VALID_ATTRIBUTES,
		.attributes = KACS_SATTR_READONLY,
	};
	struct kacs_sattr got;
	int fd;

	mkfile(at("ro"), "readonly");
	CHECK(setxattr(at("ro"), KACS_SATTR_XATTR_NAME, &v, sizeof(v), 0) == 0,
	      "read-only: set through the xattr");
	memset(&got, 0, sizeof(got));
	CHECK(getxattr(at("ro"), KACS_SATTR_XATTR_NAME, &got, sizeof(got)) ==
			      sizeof(got) &&
		      (got.attributes & KACS_SATTR_READONLY),
	      "read-only: read back");
	errno = 0;
	CHECK(open(at("ro"), O_WRONLY) < 0 && errno == EACCES,
	      "read-only: an open for writing fails with EACCES");
	fd = open(at("ro"), O_RDONLY);
	CHECK(fd >= 0, "read-only: reading still opens");
	if (fd >= 0)
		close(fd);
	errno = 0;
	CHECK(unlink(at("ro")) < 0 && errno == EPERM,
	      "read-only: unlink fails with EPERM");
	/* Created At, a different field, leaves read-only alone. */
	v.valid = KACS_SATTR_VALID_CREATED_AT;
	v.attributes = 0;
	v.created_at_sec = 1000000000;
	CHECK(setxattr(at("ro"), KACS_SATTR_XATTR_NAME, &v, sizeof(v), 0) == 0 &&
		      getxattr(at("ro"), KACS_SATTR_XATTR_NAME, &got,
			       sizeof(got)) == sizeof(got) &&
		      (got.attributes & KACS_SATTR_READONLY) &&
		      (got.flags & KACS_SATTR_CREATED_AT_SET) &&
		      got.created_at_sec == 1000000000,
	      "sattr: writing Created At merges, keeping read-only");
	v.valid = KACS_SATTR_VALID_ATTRIBUTES;
	v.attributes = 0;
	CHECK(setxattr(at("ro"), KACS_SATTR_XATTR_NAME, &v, sizeof(v), 0) == 0 &&
		      unlink(at("ro")) == 0,
	      "read-only: cleared, the file can be deleted");
}

static void test_pins(void)
{
	char sub[512], file[512], moved[512];
	int fd;

	snprintf(sub, sizeof(sub), "%s/pindir", dir);
	snprintf(moved, sizeof(moved), "%s/pindir-moved", dir);
	snprintf(file, sizeof(file), "%s/pindir/f", dir);
	rmdir(moved);
	mkdir(sub, 0700);
	mkfile(file, "p");
	fd = kopen(file, KACS_FILE_READ_DATA, KACS_DISPOSITION_OPEN, 0,
		   KACS_OPEN_PIN_ANCESTORS, 0, NULL);
	CHECK(fd >= 0, "pins: an open pinning its ancestors (needs "
		       "SeLockParentagePrivilege)");
	if (fd < 0)
		return;
	errno = 0;
	CHECK(rename(sub, moved) < 0 && errno == EBUSY,
	      "pins: the pinned folder cannot be renamed");
	close(fd);
	CHECK(rename(sub, moved) == 0, "pins: closing the open releases it");
	unlink(at("pindir-moved/f"));
	rmdir(moved);
}

/*
 * StrataFS only: "cu" and "cu2" exist in a lower stratum alone. Share
 * state must follow a file through copy-up, and delete-pending must
 * remove a lower-only name.
 */
static void test_copy_up(void)
{
	uint32_t status = 0;
	int a, b, c;

	if (!exists(at("cu")))
		return;
	a = kopen(at("cu"), KACS_FILE_READ_DATA, KACS_DISPOSITION_OPEN, 0,
		  KACS_OPEN_SHARE_ACCESS,
		  KACS_FILE_SHARE_READ | KACS_FILE_SHARE_WRITE, NULL);
	CHECK(a >= 0, "copy-up: a lower file opens denying delete");
	if (a < 0)
		return;
	b = open(at("cu"), O_WRONLY);
	CHECK(b >= 0 && write(b, "y", 1) == 1,
	      "copy-up: a legacy writer copies it up and writes");
	errno = 0;
	CHECK(unlink(at("cu")) < 0 && errno == EBUSY,
	      "copy-up: the reader's deny-delete survives copy-up");
	errno = 0;
	c = kopen(at("cu"), KACS_FILE_WRITE_DATA, KACS_DISPOSITION_OPEN, 0,
		  KACS_OPEN_SHARE_ACCESS, KACS_FILE_SHARE_READ, &status);
	CHECK(c < 0 && errno == EBUSY &&
		      status == KACS_STATUS_SHARING_VIOLATION,
	      "copy-up: a writer denying write conflicts with the copied-up writer");
	if (c >= 0)
		close(c);
	if (b >= 0)
		close(b);
	close(a);
	CHECK(unlink(at("cu")) == 0 && !exists(at("cu")),
	      "copy-up: unlink succeeds once closed");

	a = kopen(at("cu2"), KACS_FILE_READ_DATA | KACS_ACCESS_DELETE,
		  KACS_DISPOSITION_OPEN, 0, 0, 0, NULL);
	CHECK(a >= 0 && set_disposition(a, KACS_DISPOSITION_DELETE) == 0,
	      "copy-up: a lower-only file is marked delete-pending");
	if (a < 0)
		return;
	CHECK(exists(at("cu2")), "copy-up: its name stays while open");
	close(a);
	CHECK(!exists(at("cu2")), "copy-up: closing removes the lower-only name");

	/* A handle renames the copy its file was copied up to. */
	a = kopen(at("cu3"), KACS_FILE_READ_DATA | KACS_ACCESS_DELETE,
		  KACS_DISPOSITION_OPEN, 0, 0, 0, NULL);
	b = open(at("cu3"), O_WRONLY);
	CHECK(a >= 0 && b >= 0 && write(b, "z", 1) == 1,
	      "copy-up: a lower file is opened, then copied up by a writer");
	if (b >= 0)
		close(b);
	CHECK(a >= 0 && krename(a, at("cu3-moved"), 0) == 0 &&
		      exists(at("cu3-moved")) && !exists(at("cu3")),
	      "copy-up: kacs_rename moves the copied-up file");
	if (a >= 0)
		close(a);

	/* A name a higher stratum masks is not the handle's to move. */
	if (getenv("NTTEST_UPPER")) {
		char upper[512];

		a = kopen(at("cu4"), KACS_FILE_READ_DATA | KACS_ACCESS_DELETE,
			  KACS_DISPOSITION_OPEN, 0, 0, 0, NULL);
		snprintf(upper, sizeof(upper), "%s/cu4", getenv("NTTEST_UPPER"));
		mkfile(upper, "mask");
		errno = 0;
		CHECK(a >= 0 && krename(a, at("cu4-moved"), 0) < 0 &&
			      errno == ENOENT && exists(at("cu4")),
		      "copy-up: kacs_rename of a masked lower file fails with ENOENT");
		if (a >= 0)
			close(a);
	}
}

static void test_creator_access(void)
{
	/* Owner SYSTEM, group SYSTEM, a present but empty DACL. */
	static const uint8_t empty_dacl_sd[] = {
		1, 0, 4, 0x80, 20, 0, 0, 0, 32, 0, 0, 0, 0, 0, 0, 0, 44,
		0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 5, 18, 0, 0, 0, 1, 1, 0,
		0, 0, 0, 0, 5, 18, 0, 0, 0, 2, 0, 8, 0, 0, 0, 0, 0,
	};
	int fd;

	unlink(at("creator"));
	fd = kopen_sd(at("creator"), RW, KACS_DISPOSITION_CREATE, empty_dacl_sd,
		      sizeof(empty_dacl_sd));
	CHECK(fd >= 0 && write(fd, "c", 1) == 1,
	      "creator: a new file with an empty DACL gives its creator a "
	      "write handle");
	if (fd >= 0)
		close(fd);
	errno = 0;
	fd = kopen(at("creator"), RW, KACS_DISPOSITION_OPEN, 0, 0, 0, NULL);
	CHECK(fd < 0 && errno == EACCES,
	      "creator: a later open is checked against the descriptor");
	if (fd >= 0)
		close(fd);
}

/* The guest has no dmesg: print the kernel log's warnings and KACS lines. */
static int print_kmsg(void)
{
	static char buf[1 << 20];
	char *line, *save;
	int n = klogctl(3, buf, sizeof(buf) - 1);

	if (n < 0) {
		perror("klogctl");
		return 1;
	}
	buf[n] = '\0';
	for (line = strtok_r(buf, "\n", &save); line;
	     line = strtok_r(NULL, "\n", &save))
		if (strstr(line, "WARNING") || strstr(line, "BUG") ||
		    strstr(line, "Oops") || strstr(line, "pkm") ||
		    strstr(line, "kacs") || strstr(line, "Call Trace"))
			puts(line);
	return 0;
}

int main(int argc, char **argv)
{
	if (argc > 1 && !strcmp(argv[1], "--kmsg"))
		return print_kmsg();
	/* The guest has no mount either: --mount <target> <strata>. */
	if (argc > 3 && !strcmp(argv[1], "--mount")) {
		char opts[1024];

		snprintf(opts, sizeof(opts), "strata=%s", argv[3]);
		if (mount("stratafs", argv[2], "stratafs", 0, opts)) {
			perror("mount");
			return 1;
		}
		return 0;
	}
	dir = argc > 1 ? argv[1] : "/srv/nt";
	printf("nttest in %s\n", dir);
	test_control_handle();
	test_share_modes();
	test_delete_pending();
	test_dir_share();
	test_rename();
	test_locks();
	test_leases();
	test_readonly();
	test_pins();
	test_copy_up();
	test_creator_access();
	printf("NTTEST %d/%d passed\n", checks - failures, checks);
	return failures != 0;
}
