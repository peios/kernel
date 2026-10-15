---
title: "LSM hooks and object state"
description: "The KACS security blobs, registered Linux Security Module hooks, and direct entry points at patched file-metadata call sites."
type: reference
---

<a id="trm-3-e"></a>

KACS registers as the `pkm` Linux Security Module. This appendix is an
implementation inventory for kernel developers: it describes the storage
and call sites behind the contracts in this chapter. These C structures
and callbacks are kernel-private, not userspace layouts or extension APIs.
The exported ABI remains in [KACS ABI Reference](<~kernel/userspace/native/kacs/generated-syscall-index#trm-3-a>).

The inventory comes from `security/pkm/kacs/lsm.c` (`pkm_blob_sizes` and
`pkm_hooks[]`), the structures in `security/pkm/kacs/lsm_internal.h`, and the callback
implementations listed below. When changing those declarations, update
this inventory with the same change. The hook matrix preserves registration
order; each row names an actual `LSM_HOOK_INIT` entry.

<a id="trm-3-e-1"></a>

## Security-blob inventory

`pkm_blob_sizes` requests eight sized blob families. Each `lbs_*` entry
is initialized with `sizeof` the corresponding structure; Linux's LSM
infrastructure assigns its offset in the object's security storage. Byte
sizes and offsets depend on the build and are not fixed by this manual.

| LSM size entry | KACS structure | State carried |
|---|---|---|
| `lbs_cred` | `pkm_kacs_cred_security` | Token reference, shared `process_state`, projected UID/GID, and the pending descriptor used while overlayfs creates or copies up an inode. |
| `lbs_task` | `pkm_kacs_task_security` | Shared `process_state`, usermode-helper and impersonation state, the applied primary-installation epoch and thread-enrollment callback, deferred privilege-audit work, native-open/create requests, write/metadata decisions, and narrowly scoped StrataFS creation, supersede, cleanup and delete-on-close context. |
| `lbs_sock` | `pkm_kacs_socket_security` | Socket descriptor, conveyed peer/listener identities, token-conveyance cache and impersonation limits, binder identity/reuse decision, and the committed socket-owner identity used by network policy. |
| `lbs_ipc` | `pkm_kacs_ipc_security` | Refcounted descriptor and lock for a System V message queue, shared-memory segment or semaphore array. |
| `lbs_file` | `pkm_kacs_file_security` | Cached `granted_access` and `continuous_audit_mask`, copy-up context and phase generation, `managed`, `delete_on_close`, and the referenced token that armed deferred deletion. |
| `lbs_backing_file` | `pkm_kacs_backing_file_security` | Cached `granted_access` and `continuous_audit_mask`, plus `managed` and `inherited`, for the explicit outer-to-backing-file snapshot transfer. |
| `lbs_inode` | `pkm_kacs_inode_security` | Lock and RCU descriptor-cache pointer, delete-on-close lineage and signed-exec pin counters, and the deferred descriptor-persistence state. Test-only members exist under `CONFIG_SECURITY_PKM_KUNIT`. |
| `lbs_superblock` | `pkm_kacs_superblock_security` | Mount-policy lock, template descriptor bytes/length, policy generation and mount policy. |

The additional `lbs_xattr_count = 1` reserves one xattr-initialization
slot. It is not a ninth object blob or a byte-size declaration.

The file blob uses separate `u8 managed` and `u8 delete_on_close`
fields. There is no `flags` member or `KACS_FILE_FACS_MANAGED` constant.
The backing-file blob is distinct from the ordinary file blob: its
`inherited` marker records explicit adoption of the outer description's
cached grants and continuous-audit mask ([The StrataFS Copy-Up Context](<~kernel/internals/stratafs/security/kacs-admission-and-object-phases#trm-3-9-7>)).

The task blob reaches process-wide state through its `process_state`
pointer. The refcounted `pkm_kacs_process_state` contains `process_guid`,
`pip_type`, `pip_trust`, one `u32 mitigation_bits`, the KMES rate bucket,
the `process_sd` reference and process-scoped privilege-audit bookkeeping.
It also holds `primary_lock`, `desired_primary_token` and `primary_epoch`,
which order primary-token installation across the process's threads
([Token Lifecycle](<~kernel/internals/kacs/tokens/token-lifecycle#trm-3-2-3>)).
PIP identity and the process descriptor are not inline task-blob fields;
the process mitigations are not nine independent booleans. This shared
state is separate from the effective token used during impersonation.

The credential blob's `pending_create_sd` has the lifetime of an override
credential. Overlayfs uses it to stamp the descriptor computed for the
original object or caller/parent onto the actual created inode; credential
preparation does not inherit it into a derived credential. The task blob's
internal SD read/write depth and operation contexts similarly identify
specific kernel work; they are not caller-settable authorization flags.

<a id="trm-3-e-2"></a>

## Registered hook matrix

The current `pkm_hooks[]` table contains 99 registrations. Paths in the
last column are relative to the `pkm` source repository. A callback's
presence here identifies where KACS is called; the operation's access,
privilege and lifetime rules remain specified in the relevant chapter.

| Linux LSM hook | KACS callback | Implementation |
|---|---|---|
| `cred_prepare` | `pkm_kacs_cred_prepare` | `security/pkm/kacs/cred_lifecycle.c` |
| `cred_transfer` | `pkm_kacs_cred_transfer` | `security/pkm/kacs/cred_lifecycle.c` |
| `cred_alloc_blank` | `pkm_kacs_cred_alloc_blank` | `security/pkm/kacs/cred_lifecycle.c` |
| `cred_free` | `pkm_kacs_cred_free` | `security/pkm/kacs/cred_lifecycle.c` |
| `sb_alloc_security` | `pkm_kacs_sb_alloc_security` | `security/pkm/kacs/object_lifecycle.c` |
| `sb_free_security` | `pkm_kacs_sb_free_security` | `security/pkm/kacs/object_lifecycle.c` |
| `sb_kern_mount` | `pkm_kacs_sb_kern_mount` | `security/pkm/kacs/mnt_namespace.c` |
| `inode_alloc_security` | `pkm_kacs_inode_alloc_security` | `security/pkm/kacs/object_lifecycle.c` |
| `inode_free_security_rcu` | `pkm_kacs_inode_free_security_rcu` | `security/pkm/kacs/object_lifecycle.c` |
| `inode_getattr` | `pkm_kacs_inode_getattr` | `security/pkm/kacs/file_metadata.c` |
| `path_notify` | `pkm_kacs_path_notify` | `security/pkm/kacs/namespace.c` |
| `inode_setattr` | `pkm_kacs_inode_setattr` | `security/pkm/kacs/file_metadata.c` |
| `inode_file_getattr` | `pkm_kacs_inode_file_getattr` | `security/pkm/kacs/file_metadata.c` |
| `inode_file_setattr` | `pkm_kacs_inode_file_setattr` | `security/pkm/kacs/file_metadata.c` |
| `inode_xattr_skipcap` | `pkm_kacs_inode_xattr_skipcap` | `security/pkm/kacs/file_metadata.c` |
| `inode_getxattr` | `pkm_kacs_inode_getxattr` | `security/pkm/kacs/file_metadata.c` |
| `inode_setxattr` | `pkm_kacs_inode_setxattr` | `security/pkm/kacs/file_metadata.c` |
| `inode_post_setxattr` | `pkm_kacs_inode_post_setxattr` | `security/pkm/kacs/file_metadata.c` |
| `inode_removexattr` | `pkm_kacs_inode_removexattr` | `security/pkm/kacs/file_metadata.c` |
| `inode_listxattr` | `pkm_kacs_inode_listxattr` | `security/pkm/kacs/file_metadata.c` |
| `inode_copy_up` | `pkm_kacs_inode_copy_up` | `security/pkm/kacs/file_metadata.c` |
| `inode_copy_up_xattr` | `pkm_kacs_inode_copy_up_xattr` | `security/pkm/kacs/file_metadata.c` |
| `inode_follow_link` | `pkm_kacs_inode_follow_link` | `security/pkm/kacs/file_metadata.c` |
| `inode_set_acl` | `pkm_kacs_inode_set_acl` | `security/pkm/kacs/file_metadata.c` |
| `inode_remove_acl` | `pkm_kacs_inode_remove_acl` | `security/pkm/kacs/file_metadata.c` |
| `inode_getsecurity` | `pkm_kacs_inode_getsecurity` | `security/pkm/kacs/file_metadata.c` |
| `inode_permission` | `pkm_kacs_inode_permission` | `security/pkm/kacs/namespace.c` |
| `inode_create` | `pkm_kacs_inode_create` | `security/pkm/kacs/namespace.c` |
| `inode_link` | `pkm_kacs_inode_link` | `security/pkm/kacs/namespace.c` |
| `inode_unlink` | `pkm_kacs_inode_unlink` | `security/pkm/kacs/namespace.c` |
| `inode_symlink` | `pkm_kacs_inode_symlink` | `security/pkm/kacs/namespace.c` |
| `inode_mkdir` | `pkm_kacs_inode_mkdir` | `security/pkm/kacs/namespace.c` |
| `inode_rmdir` | `pkm_kacs_inode_rmdir` | `security/pkm/kacs/namespace.c` |
| `inode_mknod` | `pkm_kacs_inode_mknod` | `security/pkm/kacs/namespace.c` |
| `inode_rename` | `pkm_kacs_inode_rename` | `security/pkm/kacs/namespace.c` |
| `inode_readlink` | `pkm_kacs_inode_readlink` | `security/pkm/kacs/namespace.c` |
| `inode_init_security` | `pkm_kacs_inode_init_security` | `security/pkm/kacs/namespace.c` |
| `inode_post_create_tmpfile` | `pkm_kacs_copy_up_post_create_tmpfile` | `security/pkm/kacs/copy_up.c` |
| `dentry_create_files_as` | `pkm_kacs_dentry_create_files_as` | `security/pkm/kacs/namespace.c` |
| `file_alloc_security` | `pkm_kacs_file_alloc_security` | `security/pkm/kacs/object_lifecycle.c` |
| `backing_file_alloc` | `pkm_kacs_backing_file_alloc` | `security/pkm/kacs/object_lifecycle.c` |
| `file_release` | `pkm_kacs_file_release` | `security/pkm/kacs/object_lifecycle.c` |
| `file_open` | `pkm_kacs_file_open` | `security/pkm/kacs/file_access.c` |
| `file_receive` | `pkm_kacs_file_receive` | `security/pkm/kacs/object_lifecycle.c` |
| `file_permission` | `pkm_kacs_file_permission` | `security/pkm/kacs/file_access.c` |
| `file_ioctl` | `pkm_kacs_file_ioctl` | `security/pkm/kacs/file_access.c` |
| `file_ioctl_compat` | `pkm_kacs_file_ioctl_compat` | `security/pkm/kacs/file_access.c` |
| `file_lock` | `pkm_kacs_file_lock` | `security/pkm/kacs/file_access.c` |
| `file_fcntl` | `pkm_kacs_file_fcntl` | `security/pkm/kacs/file_access.c` |
| `file_truncate` | `pkm_kacs_file_truncate` | `security/pkm/kacs/file_access.c` |
| `kernel_read_file` | `pkm_kacs_kernel_read_file` | `security/pkm/kacs/firmware.c` |
| `kernel_post_read_file` | `pkm_kacs_kernel_post_read_file` | `security/pkm/kacs/firmware.c` |
| `task_alloc` | `pkm_kacs_task_alloc` | `security/pkm/kacs/task_lifecycle.c` |
| `task_free` | `pkm_kacs_task_free` | `security/pkm/kacs/task_lifecycle.c` |
| `sk_alloc_security` | `pkm_kacs_sk_alloc_security` | `security/pkm/kacs/socket.c` |
| `sk_free_security` | `pkm_kacs_sk_free_security` | `security/pkm/kacs/socket.c` |
| `sk_clone_security` | `pkm_kacs_sk_clone_security` | `security/pkm/kacs/socket.c` |
| `socket_post_create` | `pkm_kacs_socket_post_create` | `security/pkm/kacs/socket.c` |
| `socket_bind` | `pkm_kacs_socket_bind` | `security/pkm/kacs/socket.c` |
| `socket_connect` | `pkm_kacs_socket_connect` | `security/pkm/kacs/socket.c` |
| `unix_stream_connect` | `pkm_kacs_unix_stream_connect` | `security/pkm/kacs/socket.c` |
| `unix_may_send` | `pkm_kacs_unix_may_send` | `security/pkm/kacs/socket.c` |
| `socket_listen` | `pkm_kacs_socket_listen` | `security/pkm/kacs/socket.c` |
| `ipc_permission` | `pkm_kacs_ipc_permission` | `security/pkm/kacs/ipc.c` |
| `msg_queue_alloc_security` | `pkm_kacs_ipc_alloc_security` | `security/pkm/kacs/ipc.c` |
| `msg_queue_free_security` | `pkm_kacs_ipc_free_security` | `security/pkm/kacs/ipc.c` |
| `msg_queue_msgctl` | `pkm_kacs_msg_queue_msgctl` | `security/pkm/kacs/ipc.c` |
| `shm_alloc_security` | `pkm_kacs_ipc_alloc_security` | `security/pkm/kacs/ipc.c` |
| `shm_free_security` | `pkm_kacs_ipc_free_security` | `security/pkm/kacs/ipc.c` |
| `shm_shmctl` | `pkm_kacs_shm_shmctl` | `security/pkm/kacs/ipc.c` |
| `sem_alloc_security` | `pkm_kacs_ipc_alloc_security` | `security/pkm/kacs/ipc.c` |
| `sem_free_security` | `pkm_kacs_ipc_free_security` | `security/pkm/kacs/ipc.c` |
| `sem_semctl` | `pkm_kacs_sem_semctl` | `security/pkm/kacs/ipc.c` |
| `task_kill` | `pkm_kacs_task_kill` | `security/pkm/kacs/process_access.c` |
| `ptrace_access_check` | `pkm_kacs_ptrace_access_check` | `security/pkm/kacs/process_access.c` |
| `ptrace_traceme` | `pkm_kacs_ptrace_traceme` | `security/pkm/kacs/process_access.c` |
| `task_setnice` | `pkm_kacs_task_setnice` | `security/pkm/kacs/process_access.c` |
| `task_setscheduler` | `pkm_kacs_task_setscheduler` | `security/pkm/kacs/process_access.c` |
| `task_setioprio` | `pkm_kacs_task_setioprio` | `security/pkm/kacs/process_access.c` |
| `task_setpgid` | `pkm_kacs_task_setpgid` | `security/pkm/kacs/process_access.c` |
| `task_getpgid` | `pkm_kacs_task_getpgid` | `security/pkm/kacs/process_access.c` |
| `task_getsid` | `pkm_kacs_task_getsid` | `security/pkm/kacs/process_access.c` |
| `task_getscheduler` | `pkm_kacs_task_getscheduler` | `security/pkm/kacs/process_access.c` |
| `task_getioprio` | `pkm_kacs_task_getioprio` | `security/pkm/kacs/process_access.c` |
| `task_movememory` | `pkm_kacs_task_movememory` | `security/pkm/kacs/process_access.c` |
| `task_fix_setuid` | `pkm_kacs_task_fix_setuid` | `security/pkm/kacs/cred_projection.c` |
| `task_fix_setgid` | `pkm_kacs_task_fix_setgid` | `security/pkm/kacs/cred_projection.c` |
| `task_fix_setgroups` | `pkm_kacs_task_fix_setgroups` | `security/pkm/kacs/cred_projection.c` |
| `task_prlimit` | `pkm_kacs_task_prlimit` | `security/pkm/kacs/process_access.c` |
| `capable` | `pkm_kacs_capable` | `security/pkm/kacs/capability.c` |
| `capset` | `pkm_kacs_capset` | `security/pkm/kacs/capability.c` |
| `task_prctl` | `pkm_kacs_task_prctl` | `security/pkm/kacs/psb.c` |
| `mmap_file` | `pkm_kacs_mmap_file` | `security/pkm/kacs/psb.c` |
| `mmap_backing_file` | `pkm_kacs_mmap_backing_file` | `security/pkm/kacs/object_lifecycle.c` |
| `file_mprotect` | `pkm_kacs_file_mprotect` | `security/pkm/kacs/psb.c` |
| `bprm_check_security` | `pkm_kacs_bprm_check_security` | `security/pkm/kacs/exec.c` |
| `bprm_creds_from_file` | `pkm_kacs_bprm_creds_from_file` | `security/pkm/kacs/exec.c` |
| `bprm_committing_creds` | `pkm_kacs_bprm_committing_creds` | `security/pkm/kacs/exec.c` |
| `bprm_committed_creds` | `pkm_kacs_bprm_committed_creds` | `security/pkm/kacs/exec.c` |

<a id="trm-3-e-3"></a>

## Direct file-metadata entry points

An LSM hook receives the arguments supplied by the Linux hook API. Some
file-descriptor operations also need the particular open file's cached
FACS grant. PKM's patch series therefore calls KACS directly at the
file-descriptor call site, before the later inode-level work. These
functions are declared and called directly under `CONFIG_SECURITY_PKM`;
they are not additional entries in `pkm_hooks[]` and are not dispatched
through another LSM's hook table.

| File-descriptor operation | Direct KACS entry point | Kernel call site |
|---|---|---|
| Change mode | `pkm_kacs_file_chmod` | `fs/open.c` |
| Change owner/group | `pkm_kacs_file_chown` | `fs/open.c` |
| Change timestamps through a file descriptor | `pkm_kacs_file_utimens` | `fs/utimes.c` |
| Read file attributes through a file descriptor | `pkm_kacs_file_getattr` | `fs/stat.c` |
| Read an xattr through a file descriptor | `pkm_kacs_file_sd_xattr_get` | `fs/xattr.c` |
| Set an xattr through a file descriptor | `pkm_kacs_file_sd_xattr_set` | `fs/xattr.c` |
| Remove an xattr through a file descriptor | `pkm_kacs_file_sd_xattr_remove` | `fs/xattr.c` |

All seven implementations are in `security/pkm/kacs/file_metadata.c`. The xattr
functions enforce the file's metadata grant as well as the separate
rules for protected SD attributes; their names do not make raw SD-xattr
access a supported security-descriptor API.

The names `security_file_setattr`, `security_file_getattr`,
`security_file_getxattr` and `security_file_setxattr` do not name hooks
provided by this kernel. In particular, do not confuse them with the
real `inode_file_getattr` and `inode_file_setattr` registrations in the
matrix: those receive a dentry and `struct file_kattr`, not the open file
whose cached grant the direct entry points consult. The metadata decision
record connects the file-level check to the later inode-level operation.
This table covers those file-metadata entry points, not every direct
KACS call in the kernel.

<a id="trm-3-e-4"></a>

## Reserved access-mask bits

`RESERVED_ACCESS_MASK_BITS` in
`security/pkm/kacs/kacs_core/access_mask.rs` is `0x0ce0_0000` (bits 21, 22, 23,
26 and 27, counting from zero). It remains a private evaluator constant,
not a new UAPI definition. [The Algorithm](<~kernel/internals/kacs/access-check/the-algorithm#trm-3-8-10>) already specifies the public behavior:
reserved bits in a desired mask or any ACE mask reject the check, rather
than being ignored. This inventory records the implementation value
without adding another exported spelling.
