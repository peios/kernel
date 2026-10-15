---
title: "Socket ABI compatibility"
description: "Socket ABI compatibility: behaviour and implementation of the Peios kernel."
type: reference
---

<a id="trm-3-d-5"></a>

## Socket options and retired syscall numbers

Peer identity on AF_UNIX sockets is read and bounded through socket
options rather than syscalls. `include/uapi/pkm/socket.h` defines the option
level `SOL_KACS` (4096), its options `KACS_SO_PEER_TOKEN`,
`KACS_SO_IMPERSONATION_LEVEL`, `KACS_SO_PASS_TOKEN` and
`KACS_SO_RESTAMP`, and the ancillary message type `KACS_SCM_TOKEN`,
which travels at
`cmsg_level SOL_KACS` ([KACS ABI Reference](<~kernel/userspace/native/kacs/generated-syscall-index#trm-3-a>)). <a id="cite-abi-notes.scm-token-cmsg-level"></a> The kernel dispatches the option level
in `net/socket.c` ahead of the protocol's own handlers (patch
`net/socket.c`), so the options reach KACS on
every socket family and KACS decides which it supports. <a id="cite-abi-notes.sol-kacs-dispatch-all-families"></a> The ancillary
message is carried per skb on AF_UNIX: `net/core/scm.c`
gives `struct scm_cookie` a counted token reference and parses
`SOL_KACS` control messages; `net/unix/af_unix.c` carries
the reference on `struct unix_skb_parms`, stops a stream read at an
identity boundary, and advances the register at the point of
consumption. Everything KACS-specific behind those hooks lives in
`security/pkm/kacs/socket.c`. The semantics and error codes are in [Impersonation Lifecycle](<~kernel/internals/kacs/impersonation/state-transitions#trm-3-5-3>).

System V IPC objects carry descriptors of their own ([Objects and Their Descriptors](<~kernel/internals/kacs/system-v-ipc/objects-and-their-descriptors#trm-3-11-1>)); their
rights are `include/uapi/pkm/ipc.h`, and the same header defines the
`KACS_SD_AT_SYSV_*` flags that let `kacs_get_sd` and `kacs_set_sd`
address such an object by kind and id (`dirfd` carries the id, the
path is NULL). <a id="cite-abi-notes.sysv-sd-at-addressing"></a> The lookup is `ipc_lsm_with_object`, exported from
`ipc/util.c` by `ipc/util-lsm-with-object.patch`; the hooks themselves
are the LSM's own IPC hooks and need no patch.

Three syscall numbers are retired and left as permanent holes:
1010 (`kacs_open_peer_token`), 1011 (`kacs_impersonate_peer`) and
1013 (`kacs_set_impersonation_level`). A binary built against them
gets `ENOSYS`. <a id="cite-abi-notes.retired-syscalls-enosys"></a> The first became `getsockopt(SOL_KACS,
KACS_SO_PEER_TOKEN)`, the third `setsockopt(SOL_KACS,
KACS_SO_IMPERSONATION_LEVEL)`, and the second was a fusion of the
first with `KACS_IOC_IMPERSONATE` that now lives in libpeios as
`peios_token_impersonate_peer`.
