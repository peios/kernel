---
title: "Generated syscall index"
description: "Generated syscall index: behaviour and implementation of the Peios kernel."
type: reference
---

<a id="trm-3-a"></a>

Every name, value, offset and size in this appendix is generated
from `include/uapi/pkm/` by `tools/docs/peios-reference/generators/gen-kacs-abi.py`, with struct
layouts measured by compiling a probe against the real headers.
Regenerate it whenever the ABI changes; do not edit it by hand.

The names here are the ones a program actually compiles against. <a id="cite-kacs-abi.generated-from-source"></a>
Everything about the ABI a compiler cannot measure -- token query
payload shapes, the specification spellings that differ from these
names, what is documented elsewhere, and the kernel configuration
-- is in the notes appendix, [KACS ABI Notes](<~kernel/userspace/native/kacs/abi-status-and-naming-differences#trm-3-d>), which this generator does not
touch.

<a id="trm-3-a-1"></a>

## Syscall numbers <a id="cite-kacs-abi.syscall-numbers"></a>

Signatures are read from the `SYSCALL_DEFINE` sites in `security/pkm/kacs/`.
The PKM UAPI exports the uppercase constants in `<pkm/syscall.h>`. Peios
glibc 2.44-5 and later exports the standard lowercase `SYS_kacs_*`
aliases in `<sys/syscall.h>`; each alias has the same number as its PKM
constant.

| Number | PKM constant | glibc alias | Signature |
|---:|---|---|---|
| 1000 | `SYS_KACS_OPEN_SELF_TOKEN` | `SYS_kacs_open_self_token` | `kacs_open_self_token(unsigned int flags, u32 access_mask)` |
| 1001 | `SYS_KACS_OPEN_PROCESS_TOKEN` | `SYS_kacs_open_process_token` | `kacs_open_process_token(int pidfd, u32 access_mask)` |
| 1002 | `SYS_KACS_OPEN_THREAD_TOKEN` | `SYS_kacs_open_thread_token` | `kacs_open_thread_token(int pidfd, int tid, u32 access_mask)` |
| 1003 | `SYS_KACS_CREATE_TOKEN` | `SYS_kacs_create_token` | `kacs_create_token(const void __user *spec, size_t spec_len)` |
| 1004 | `SYS_KACS_CREATE_LOGON_SESSION` | `SYS_kacs_create_logon_session` | `kacs_create_logon_session(const void __user *spec, size_t spec_len)` |
| 1005 | `SYS_KACS_SET_PSB` | `SYS_kacs_set_psb` | `kacs_set_psb(int pidfd, u32 mitigations)` |
| 1006 | `SYS_KACS_DESTROY_EMPTY_LOGON_SESSION` | `SYS_kacs_destroy_empty_logon_session` | `kacs_destroy_empty_logon_session(u64 auth_id)` |
| 1012 | `SYS_KACS_REVERT` | `SYS_kacs_revert` | `kacs_revert(void)` |
| 1020 | `SYS_KACS_OPEN` | `SYS_kacs_open` | `kacs_open(int dirfd, const char __user *path, struct kacs_open_how __user *uhow, size_t howsize, u32 __user *status_out)` |
| 1021 | `SYS_KACS_GET_SD` | `SYS_kacs_get_sd` | `kacs_get_sd(int dirfd, const char __user *path, u32 security_info, void __user *buf, u32 buf_len, u32 flags)` |
| 1022 | `SYS_KACS_SET_SD` | `SYS_kacs_set_sd` | `kacs_set_sd(int dirfd, const char __user *path, u32 security_info, const void __user *sd_buf, u32 sd_len, u32 flags)` |
| 1023 | `SYS_KACS_ACCESS_CHECK` | `SYS_kacs_access_check` | `kacs_access_check(const void __user *uargs)` |
| 1024 | `SYS_KACS_ACCESS_CHECK_LIST` | `SYS_kacs_access_check_list` | `kacs_access_check_list(const void __user *uargs, struct kacs_node_result __user *results, u32 results_count)` |
| 1025 | `SYS_KACS_SET_CAAP` | `SYS_kacs_set_caap` | `kacs_set_caap(const void __user *policy_sid, u32 policy_sid_len, const void __user *spec, u32 spec_len)` |
| 1026 | `SYS_KACS_GET_MOUNT_POLICY` | `SYS_kacs_get_mount_policy` | `kacs_get_mount_policy(int fd, struct kacs_mount_policy_args __user *uargs, size_t argsize)` |
| 1027 | `SYS_KACS_SET_MOUNT_POLICY` | `SYS_kacs_set_mount_policy` | `kacs_set_mount_policy(int fd, struct kacs_mount_policy_args __user *uargs, size_t argsize)` |

`uapi/pkm/syscall.h` also registers the KMES and LCS numbers,
1090–1102, documented in their own chapters. <a id="cite-kacs-abi.sibling-syscall-range"></a>

<a id="trm-3-a-2"></a>

## Structure layouts

## Related explanations

- [Generated token and session ABI](<~kernel/userspace/native/kacs/generated-token-and-session-abi>)
- [Generated access-check and descriptor ABI](<~kernel/userspace/native/kacs/generated-access-check-and-descriptor-abi>)
- [Generated file and mount ABI](<~kernel/userspace/native/kacs/generated-file-and-mount-abi>)
- [Generated socket and IPC ABI](<~kernel/userspace/native/kacs/generated-socket-and-ipc-abi>)
- [Generated process and PSB ABI](<~kernel/userspace/native/kacs/generated-process-and-psb-abi>)
- [Generated diagnostic constants](<~kernel/userspace/native/kacs/generated-diagnostic-constants>)
