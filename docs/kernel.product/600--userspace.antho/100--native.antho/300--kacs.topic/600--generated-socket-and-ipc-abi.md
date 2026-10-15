---
title: "Generated socket and IPC ABI"
description: "Generated socket and IPC ABI: behaviour and implementation of the Peios kernel."
type: reference
---

<a id="trm-3-a-4"></a>

## socket.h

From `uapi/pkm/socket.h`.

*KACS socket options — peer identity on local sockets.* <a id="cite-kacs-abi.sol-kacs"></a>

KACS captures a connecting client's identity onto the accepted end of an
AF_UNIX SOCK_STREAM / SOCK_SEQPACKET connection at connect(). This
header is the setsockopt(2)/getsockopt(2) surface through which that
identity is bounded and read back. Every option lives under one option
level, SOL_KACS, which the kernel dispatches ahead of the protocol's own
setsockopt/getsockopt (net/socket.c), so the options behave identically
on every socket family that supports them. SOL_KACS is 4096: far above
the upstream SOL_* range, which grows by one per new protocol, so it
cannot collide with a future Linux level. Errors: -ENOPROTOOPT for an
option this level does not define (or a get-only option passed to
setsockopt); -EOPNOTSUPP on a socket family KACS does not carry identity
on (and, for the register, on a socket type that has none); -EINVAL for
a short optlen or an out-of-range value; -EFAULT for an
unreadable/unwritable optval.

| Constant | Value |
|---|---|
| `SOL_KACS` | `4096` |

*getsockopt only.* <a id="cite-kacs-abi.so-peer-token"></a>

optval: int — a new token fd, carrying fixed TOKEN_QUERY |
TOKEN_IMPERSONATE | TOKEN_DUPLICATE access and opened O_CLOEXEC, for
this end's conveyed-identity register: the peer identity associated with
the data this end has consumed so far. The register is initialised at
connect() — on the accepted end with the client's identity, on the
connecting end with the listener's identity as captured at listen() (at
KACS_IMLEVEL_IDENTIFICATION unless the listener set its own level) — and
advanced by each KACS_SCM_TOKEN the reader's position passes (a token
still queued but unread is not yet visible). Every call returns a fresh
fd to an immutable snapshot; two calls may name different tokens, but no
token ever changes. -ENOTCONN if the socket is not connected; -ENODATA
if nothing has been conveyed yet.

| Constant | Value |
|---|---|
| `KACS_SO_PEER_TOKEN` | `1` |

*getsockopt / setsockopt.* <a id="cite-kacs-abi.so-impersonation-level"></a>

optval: __u32 KACS_IMLEVEL_* — the maximum impersonation level at which
identity leaving this end may be captured: at connect(), and at each
send that conveys identity. The default is KACS_IMLEVEL_IMPERSONATION.
May be changed at any time; a change bounds captures from then on and
never rewrites one already made.

| Constant | Value |
|---|---|
| `KACS_SO_IMPERSONATION_LEVEL` | `2` |

*getsockopt / setsockopt.* <a id="cite-kacs-abi.so-pass-token"></a>

optval: int (0/1) — sender-side automation: while set, every send from
this end carries the sender's effective identity as a KACS_SCM_TOKEN,
derived at this end's impersonation level. Costs nothing at the trust
level: the sender can always attest to what it is. Default 0.

| Constant | Value |
|---|---|
| `KACS_SO_PASS_TOKEN` | `3` |

*setsockopt only.* <a id="cite-kacs-abi.so-restamp"></a>

optval: int, ignored. Self-gated: a process can always attest to what it
is. On a listening AF_UNIX socket: replaces the identity the listener
conveys to connecting clients — captured when listen() was called — with
the caller's current effective identity, at the listener's level. For a
process that receives a listener it did not create (from a descriptor
store after a restart, or from a broker), so that clients see the
process actually accepting. -EINVAL if the socket is not listening. On
an AF_INET / AF_INET6 socket, in any state: replaces the identity that
governs the socket's traffic for network policy — stamped at creation,
bind, listen, connect and accept — with the caller's current effective
identity, so a socket handed to another program (socket activation,
descriptor passing) is governed as that program's. The identity is read
by the network policy engine at the first judgment of each flow and
fixed for that flow's life.

| Constant | Value |
|---|---|
| `KACS_SO_RESTAMP` | `4` |

*Ancillary message type, at cmsg_level SOL_KACS.* <a id="cite-kacs-abi.scm-token"></a>

Data: one int. Received: a token fd (TOKEN_QUERY | TOKEN_IMPERSONATE |
TOKEN_DUPLICATE, O_CLOEXEC) for the identity the kernel attests sent the
accompanying data. Delivered when the receive buffer has room for it and
the conveyed identity differs from the reader's register; a receiver
that reads no ancillary data still has the register
(KACS_SO_PEER_TOKEN). Sent: a token fd the sender wishes to attach to
the data. The kernel gates the send as if the sender were impersonating
that token: the two-gate model runs with the sender as installer, and an
attach that would lower the token's level fails with -EPERM rather than
downgrading. A primary token is derived to an impersonation token at
this end's level. The fd must carry TOKEN_IMPERSONATE (-EACCES
otherwise); at most one per message (-EINVAL). Attaching is exactly
equivalent to impersonating the token for the duration of the send.

| Constant | Value |
|---|---|
| `KACS_SCM_TOKEN` | `1` |

<a id="trm-3-a-5"></a>

## ipc.h

From `uapi/pkm/ipc.h`.

KACS access rights for System V IPC objects — message queues, shared
memory segments and semaphore arrays. Every SysV object carries a
security descriptor, created from the creator's token at *get time and
enforced through the LSM IPC hooks; the nine-bit ipc_perm mode is never
consulted (CAP_IPC_OWNER is in KACS's always-allow set). The key
namespace is claim-on-create: the descriptor protects the object,
nothing protects the name. Object-specific rights (low 16 bits); the
standard rights (DELETE, READ_CONTROL, WRITE_DAC, WRITE_OWNER —
<pkm/access.h>) apply as on every KACS object. <a id="cite-kacs-abi.ipc-access-rights"></a>

| Constant | Value | Notes |
|---|---|---|
| `KACS_IPC_READ` | `0x00000001` (1) | msgrcv, shmat read-only, semop without alter, GETVAL/GETALL |
| `KACS_IPC_WRITE` | `0x00000002` (2) | msgsnd, shmat read-write, semop with alter, SETVAL/SETALL |
| `KACS_IPC_QUERY_INFORMATION` | `0x00000004` (4) | IPC_STAT and the *_STAT variants |
| `KACS_IPC_SET_INFORMATION` | `0x00000008` (8) | SHM_LOCK / SHM_UNLOCK |
| `KACS_IPC_ALL_ACCESS` | `983055` |  |

ipcctl gates: IPC_RMID needs DELETE; IPC_SET needs WRITE_DAC and
WRITE_OWNER (one command carries mode, uid and gid); the mode, uid and
gid it writes are informational (ipcs, IPC_STAT) and never decide
access. Addressing a SysV object's descriptor with kacs_get_sd /
kacs_set_sd: pass one of these in `flags`, the object id in `dirfd`, and
a NULL path. The object is looked up in the caller's IPC namespace. <a id="cite-kacs-abi.sysv-sd-selectors"></a>

| Constant | Value |
|---|---|
| `KACS_SD_AT_SYSV_SHM` | `0x01000000` |
| `KACS_SD_AT_SYSV_MSG` | `0x02000000` |
| `KACS_SD_AT_SYSV_SEM` | `0x04000000` |
| `KACS_SD_AT_SYSV_MASK` | `117440512` |
