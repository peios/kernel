// SPDX-License-Identifier: GPL-2.0-only
#define _GNU_SOURCE

#include <errno.h>
#include <fcntl.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/mman.h>
#include <sys/mount.h>
#include <sys/reboot.h>
#include <sys/stat.h>
#include <sys/syscall.h>
#include <sys/sysmacros.h>
#include <sys/uio.h>
#include <sys/wait.h>
#include <unistd.h>

#include <linux/fuse.h>

#define SYS_KACS_GET_SD 1021
#define SYS_KACS_SET_SD 1022
#define SYS_KACS_SET_MOUNT_POLICY 1027

enum mapping_mode {
	SHARED_WRITE,
	SHARED_UPGRADE,
	PRIVATE_WRITE,
	SHARED_READ,
	FILE_COUNT,
};

struct kacs_mount_policy_args {
	uint32_t policy;
	uint32_t flags;
	uint32_t generation;
	uint32_t pad0;
	uint64_t template_sd_ptr;
	uint32_t template_sd_len;
	uint32_t pad1;
};

static unsigned char descriptor[65536];
static size_t descriptor_length;
static unsigned int checks;
static const char *const names[FILE_COUNT] = { "shared", "upgrade", "private",
					       "readonly" };

static void power_off(void)
{
	fflush(NULL);
	sync();
	reboot(RB_POWER_OFF);
	_exit(0);
}

static void fail(const char *stage)
{
	int error = errno;

	printf("STRATAFS_FUSE_SMOKE_FAIL: %s: errno=%d (%s)\n", stage, error,
	       strerror(error));
	power_off();
}

static void check(bool condition, const char *what)
{
	checks++;
	if (!condition) {
		errno = 0;
		fail(what);
	}
}

static void directory(const char *path)
{
	if (mkdir(path, 0755) && errno != EEXIST)
		fail(path);
}

static void stamp_descriptor(const char *path)
{
	if (syscall(SYS_KACS_SET_SD, AT_FDCWD, path, 7, descriptor,
		    descriptor_length, 0))
		fail("stamp trusted descriptor");
}

static void seed_policy(const char *path)
{
	struct kacs_mount_policy_args args = {
		.policy = 3,
		.template_sd_ptr = (uint64_t)(uintptr_t)descriptor,
		.template_sd_len = (uint32_t)descriptor_length,
	};
	int fd = open(path, O_PATH | O_DIRECTORY | O_CLOEXEC);

	if (fd < 0)
		fail("open policy root");
	if (syscall(SYS_KACS_SET_MOUNT_POLICY, fd, &args, sizeof(args)))
		fail("set mount policy");
	stamp_descriptor(path);
	close(fd);
}

static void write_text(const char *path, const char *text)
{
	size_t length = strlen(text);
	int fd = open(path, O_WRONLY | O_CREAT | O_TRUNC | O_CLOEXEC, 0644);

	if (fd < 0 || write(fd, text, length) != (ssize_t)length)
		fail(path);
	if (close(fd))
		fail("close fixture");
}

static void expect_text(const char *path, const char *expected)
{
	char text[64] = {};
	int fd = open(path, O_RDONLY | O_CLOEXEC);
	ssize_t length;

	if (fd < 0)
		fail(path);
	length = read(fd, text, sizeof(text) - 1);
	if (length < 0 || close(fd))
		fail("read expected backing contents");
	check(!strcmp(text, expected), path);
}

static void expect_absent(const char *path)
{
	check(access(path, F_OK) == -1 && errno == ENOENT, path);
}

static void reply(int fd, uint64_t unique, int error, const void *data,
		  size_t size)
{
	struct fuse_out_header header = {
		.len = (uint32_t)(sizeof(header) + size),
		.error = -error,
		.unique = unique,
	};
	struct iovec vectors[2] = {
		{ .iov_base = &header, .iov_len = sizeof(header) },
		{ .iov_base = (void *)data, .iov_len = size },
	};
	ssize_t written = writev(fd, vectors, size ? 2 : 1);

	if (written != (ssize_t)header.len) {
		printf("FUSE_SERVER_FAIL reply errno=%d wrote=%zd expected=%u\n",
		       errno, written, header.len);
		_exit(2);
	}
}

static struct fuse_attr attributes(uint64_t node, const int *backing)
{
	struct fuse_attr attr = {
		.ino = node,
		.mode = S_IFDIR | 0755,
		.nlink = 2,
		.blksize = 4096,
	};
	struct stat st;

	if (node == FUSE_ROOT_ID)
		return attr;
	if (node < 2 || node >= 2 + FILE_COUNT ||
	    fstat(backing[node - 2], &st)) {
		printf("FUSE_SERVER_FAIL getattr node=%llu errno=%d\n",
		       (unsigned long long)node, errno);
		_exit(2);
	}
	attr.size = st.st_size;
	attr.blocks = st.st_blocks;
	attr.mode = S_IFREG | 0644;
	attr.nlink = 1;
	attr.uid = st.st_uid;
	attr.gid = st.st_gid;
	return attr;
}

static void serve(int fd, const char *label, const int *backing)
{
	static unsigned char buffer[131072] __attribute__((aligned(8)));
	int backing_ids[FILE_COUNT] = {};

	for (;;) {
		struct fuse_in_header *header = (void *)buffer;
		void *body = buffer + sizeof(*header);
		ssize_t length = read(fd, buffer, sizeof(buffer));

		if (length < 0 && errno == EINTR)
			continue;
		if (length < 0 && errno == ENODEV)
			break;
		if (length < (ssize_t)sizeof(*header) ||
		    header->len != (uint32_t)length) {
			printf("FUSE_SERVER_FAIL read label=%s length=%zd errno=%d\n",
			       label, length, errno);
			_exit(2);
		}
		switch (header->opcode) {
		case FUSE_INIT: {
			struct fuse_init_in *in = body;
			uint64_t offered = in->flags | (uint64_t)in->flags2
							       << 32;
			uint64_t wanted = FUSE_INIT_EXT | FUSE_PASSTHROUGH;
			struct fuse_init_out out = {
				.major = FUSE_KERNEL_VERSION,
				.minor = FUSE_KERNEL_MINOR_VERSION,
				.max_readahead = in->max_readahead,
				.flags = (uint32_t)wanted,
				.flags2 = (uint32_t)(wanted >> 32),
				.max_background = 16,
				.congestion_threshold = 12,
				.max_write = 65536,
				.time_gran = 1,
				.max_stack_depth = 2,
			};

			printf("OBS stage=%s_init protocol=%u.%u passthrough_offered=%u max_stack_depth=2\n",
			       label, in->major, in->minor,
			       !!(offered & FUSE_PASSTHROUGH));
			if (!(offered & FUSE_PASSTHROUGH)) {
				reply(fd, header->unique, EOPNOTSUPP, NULL, 0);
				break;
			}
			if (out.minor > in->minor)
				out.minor = in->minor;
			reply(fd, header->unique, 0, &out, sizeof(out));
			break;
		}
		case FUSE_LOOKUP: {
			struct fuse_entry_out out = {
				.generation = 1,
				.entry_valid = 60,
				.attr_valid = 60,
			};
			int index;

			for (index = 0; index < FILE_COUNT; index++)
				if (!strcmp(body, names[index]))
					break;
			if (header->nodeid != FUSE_ROOT_ID ||
			    index == FILE_COUNT) {
				reply(fd, header->unique, ENOENT, NULL, 0);
				break;
			}
			out.nodeid = 2 + index;
			out.attr = attributes(out.nodeid, backing);
			reply(fd, header->unique, 0, &out, sizeof(out));
			break;
		}
		case FUSE_GETATTR: {
			struct fuse_attr_out out = { .attr_valid = 60 };

			out.attr = attributes(header->nodeid, backing);
			reply(fd, header->unique, 0, &out, sizeof(out));
			break;
		}
		case FUSE_GETXATTR: {
			struct fuse_getxattr_in *in = body;
			const char *name = (void *)(in + 1);
			struct fuse_getxattr_out out = {
				.size = (uint32_t)descriptor_length,
			};

			if (strcmp(name, "security.peios.sd")) {
				reply(fd, header->unique, ENODATA, NULL, 0);
			} else if (!in->size) {
				reply(fd, header->unique, 0, &out, sizeof(out));
			} else if (in->size < descriptor_length) {
				reply(fd, header->unique, ERANGE, NULL, 0);
			} else {
				reply(fd, header->unique, 0, descriptor,
				      descriptor_length);
			}
			break;
		}
		case FUSE_OPEN: {
			struct fuse_open_out out = {
				.fh = header->nodeid,
				.open_flags = FOPEN_PASSTHROUGH,
			};
			unsigned int index = header->nodeid - 2;

			if (index >= FILE_COUNT) {
				reply(fd, header->unique, EINVAL, NULL, 0);
				break;
			}
			if (!backing_ids[index]) {
				struct fuse_backing_map map = {
					.fd = backing[index]
				};
				int id = ioctl(fd, FUSE_DEV_IOC_BACKING_OPEN,
					       &map);
				int error = errno;

				printf("OBS stage=%s_backing_open name=%s id=%d errno=%d\n",
				       label, names[index], id,
				       id < 0 ? error : 0);
				if (id < 0) {
					reply(fd, header->unique, error, NULL,
					      0);
					break;
				}
				backing_ids[index] = id;
			}
			out.backing_id = backing_ids[index];
			reply(fd, header->unique, 0, &out, sizeof(out));
			break;
		}
		case FUSE_ACCESS:
		case FUSE_FLUSH:
		case FUSE_RELEASE:
		case FUSE_FSYNC:
		case FUSE_SYNCFS:
		case FUSE_DESTROY:
			reply(fd, header->unique, 0, NULL, 0);
			break;
		case FUSE_FORGET:
		case FUSE_BATCH_FORGET:
			break;
		case FUSE_READ:
		case FUSE_WRITE:
			printf("FUSE_SERVER_FAIL: I/O must use passthrough, opcode=%u\n",
			       header->opcode);
			_exit(2);
		default:
			printf("OBS stage=%s_unhandled opcode=%u\n", label,
			       header->opcode);
			reply(fd, header->unique, ENOSYS, NULL, 0);
		}
	}
	close(fd);
	_exit(0);
}

static pid_t start_fuse(const char *label, const char *target,
			const char *backing_root)
{
	char path[128];
	char options[128];
	int backing[FILE_COUNT];
	int fd;
	pid_t daemon;
	int index;

	for (index = 0; index < FILE_COUNT; index++) {
		snprintf(path, sizeof(path), "%s/%s", backing_root,
			 names[index]);
		backing[index] = open(path, O_RDWR | O_CLOEXEC);
		if (backing[index] < 0)
			fail("open passthrough backing");
	}
	fd = open("/dev/fuse", O_RDWR | O_CLOEXEC);
	if (fd < 0)
		fail("open fuse device");
	if (ioctl(fd, FUSE_DEV_IOC_SYNC_INIT))
		fail("enable synchronous fuse initialization");
	daemon = fork();
	if (daemon < 0)
		fail("fork fuse server");
	if (!daemon)
		serve(fd, label, backing);
	snprintf(
		options, sizeof(options),
		"fd=%d,rootmode=40000,user_id=0,group_id=0,default_permissions",
		fd);
	if (mount(label, target, "fuse", 0, options))
		fail("mount fuse");
	printf("OBS stage=%s_mount result=0\n", label);
	close(fd);
	for (index = 0; index < FILE_COUNT; index++)
		close(backing[index]);
	return daemon;
}

static void test_mapping(const char *mountpoint, const char *provider,
			 const char *create, enum mapping_mode mode)
{
	char path[128];
	char source[128];
	char copy[128];
	char initial[32];
	char expected[32];
	bool shared_write = mode == SHARED_WRITE || mode == SHARED_UPGRADE;
	int protection = mode == SHARED_WRITE || mode == PRIVATE_WRITE ?
				 PROT_READ | PROT_WRITE :
				 PROT_READ;
	char *mapping;
	int fd;

	snprintf(path, sizeof(path), "%s/%s", mountpoint, names[mode]);
	snprintf(source, sizeof(source), "%s/%s", provider, names[mode]);
	snprintf(initial, sizeof(initial), "%s-old", names[mode]);
	snprintf(expected, sizeof(expected), "%s", initial);
	fd = open(path, (mode == SHARED_READ ? O_RDONLY : O_RDWR) | O_CLOEXEC);
	if (fd < 0)
		fail(path);
	if (create) {
		snprintf(copy, sizeof(copy), "%s/%s", create, names[mode]);
		expect_absent(copy);
	}
	mapping = mmap(NULL, 4096, protection,
		       mode == PRIVATE_WRITE ? MAP_PRIVATE : MAP_SHARED, fd, 0);
	if (mapping == MAP_FAILED)
		fail("map passthrough file");
	check(!memcmp(mapping, initial, strlen(initial)),
	      "passthrough mapping must expose original contents");
	if (create) {
		if (shared_write)
			expect_text(copy, initial);
		else
			expect_absent(copy);
	}
	/* The VMA must retain its provider after the FUSE description closes. */
	if (close(fd))
		fail("close mapped passthrough description");
	if (mode == SHARED_UPGRADE &&
	    mprotect(mapping, 4096, PROT_READ | PROT_WRITE))
		fail("upgrade shared passthrough mapping");
	if (mode == SHARED_READ) {
		check(mprotect(mapping, 4096, PROT_READ | PROT_WRITE) == -1 &&
			      errno == EACCES,
		      "read-only passthrough description must not gain write access");
	} else {
		mapping[0] = 'X';
		if (shared_write)
			expected[0] = 'X';
	}
	if (msync(mapping, 4096, MS_SYNC) || munmap(mapping, 4096))
		fail("synchronize and unmap passthrough mapping");
	if (create) {
		if (shared_write)
			expect_text(copy, expected);
		else
			expect_absent(copy);
		expect_text(source, initial);
	} else {
		expect_text(source, expected);
	}
}

static void stop_fuse(const char *label, const char *target, pid_t daemon)
{
	int status;

	if (umount(target))
		fail("unmount fuse");
	if (waitpid(daemon, &status, 0) != daemon)
		fail("wait fuse server");
	check(WIFEXITED(status) && WEXITSTATUS(status) == 0, label);
}

int main(void)
{
	pid_t daemon;
	long length;
	unsigned int index;
	char path[128];
	char text[32];

	setvbuf(stdout, NULL, _IONBF, 0);
	length = syscall(SYS_KACS_GET_SD, AT_FDCWD, "/", 7, descriptor,
			 sizeof(descriptor), 0);
	if (length <= 0 || length > (long)sizeof(descriptor))
		fail("get trusted root descriptor");
	descriptor_length = length;
	directory("/proc");
	if (mount("proc", "/proc", "proc", 0, NULL))
		fail("mount proc");
	directory("/dev");
	if (mknod("/dev/fuse", S_IFCHR | 0600, makedev(10, 229)) &&
	    errno != EEXIST)
		fail("create fuse device");
	stamp_descriptor("/dev/fuse");
	directory("/storage");
	directory("/strata");
	directory("/control");
	directory("/candidate");
	if (mount("tmpfs", "/storage", "tmpfs", 0, "mode=0755"))
		fail("mount storage");
	seed_policy("/storage");
	directory("/storage/control");
	directory("/storage/base");
	directory("/storage/create");
	for (index = 0; index < FILE_COUNT; index++) {
		snprintf(text, sizeof(text), "%s-old", names[index]);
		snprintf(path, sizeof(path), "/storage/control/%s",
			 names[index]);
		write_text(path, text);
		snprintf(path, sizeof(path), "/storage/base/%s", names[index]);
		write_text(path, text);
	}
	if (mount("none", "/strata", "stratafs", 0,
		  "strata=/storage/create+create:/storage/base+ro"))
		fail("mount backing stratafs");

	daemon = start_fuse("control", "/control", "/storage/control");
	for (index = 0; index < FILE_COUNT; index++)
		test_mapping("/control", "/storage/control", NULL, index);
	stop_fuse("control", "/control", daemon);

	daemon = start_fuse("candidate", "/candidate", "/strata");
	for (index = 0; index < FILE_COUNT; index++)
		test_mapping("/candidate", "/storage/base", "/storage/create",
			     index);
	stop_fuse("candidate", "/candidate", daemon);
	printf("STRATAFS_FUSE_SMOKE_PASS: %u checks\n", checks);
	power_off();
}
