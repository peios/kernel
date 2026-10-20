---
title: Process Creation and Replacement
type: reference
description: Reference process inheritance, clone flags, executable replacement, and stable process handles.
---

Choose the creation operation according to what the child must share and
what must happen before its program starts. Keep kernel behavior distinct
from C library facilities such as `posix_spawn` and `fexecve`.

## Fork inheritance

`fork()` creates a separate process with one thread: the thread that called
it. Other parent threads are absent from the child. Ordinary private memory
uses copy-on-write; mappings explicitly shared before the fork remain shared.
A multithreaded parent's child can inherit library locks whose owners do not
exist after the fork. Its pre-exec work must respect the runtime's fork
contract.

The child inherits these resources or settings:

| Resource | Child behavior |
|---|---|
| File descriptors | Separate descriptor table; entries refer to the same open file descriptions, sharing offsets and status flags |
| Open-file-description and `flock` locks | Retained through the shared open file descriptions |
| Directory streams and message-queue descriptors | Copied runtime state or descriptors; directory-stream position sharing depends on the runtime |
| Signal dispositions and mask | Copied; pending signals start empty |
| Filesystem context | Current directory, root directory, and umask copied |
| Limits and timer slack | Inherited |
| Peios primary token | Independently duplicated; the parent's active impersonation is not inherited |
| Process security state | Subject to the kernel's PSB and protection inheritance rules |

The child receives a new PID and Process GUID. Resource-usage counters start
at zero. It does not inherit memory locks, semaphore adjustments, POSIX
process-associated record locks, POSIX timers, interval timers, asynchronous
I/O operations or directory-change notifications.
On x86, the child inherits the I/O-permission bitmap when one is present.
The parent-death signal setting is reset. `MADV_DONTFORK` mappings are absent;
`MADV_WIPEONFORK` mappings are zeroed in the child.

The normal child termination signal is `SIGCHLD`. The distinction between
an independent token on fork and a shared primary token for `CLONE_THREAD`
is defined by [token lifecycle](~kernel/internals/kacs/tokens/token-lifecycle).
Later token mutations must not be inferred to affect both processes.

## Vfork and create-then-replace

`vfork()` suspends the calling thread while the child shares its address
space until exec or exit. It does not freeze every other thread in a
multithreaded parent. The child must not return from the calling function or
perform arbitrary work in that shared runtime state. Follow the C runtime's
restrictions and proceed directly to an exec operation or `_exit`.

`posix_spawn()` is a C library interface for creating a process and executing
a program, with declared file actions and attributes. Use it when those
controls express the launch operation. Its implementation and supported
attributes belong to the selected runtime, not to a separate Peios syscall.

## Clone arguments

`clone` exposes task-sharing choices. Its raw syscall argument order can be
architecture-specific; a C wrapper that takes a start function is a different
interface. `clone3` uses a size-versioned argument structure:

| Member | Purpose |
|---|---|
| `flags` | Sharing and creation choices |
| `pidfd` | Destination for a returned pidfd |
| `child_tid`, `parent_tid` | Addresses for thread-ID bookkeeping |
| `exit_signal` | Signal delivered when the child terminates |
| `stack`, `stack_size` | Child stack region |
| `tls` | Architecture-specific thread-local-storage value |
| `set_tid`, `set_tid_size` | Requested task identifiers, subject to privilege checks |
| `cgroup` | Target cgroup for `CLONE_INTO_CGROUP` |

Pass the structure size supported by the caller. Unknown trailing fields must
be zero. Requests for specific task IDs are privileged; Peios applies its
KACS capability mapping rather than granting authority from UID 0.

## Clone flags

Flags select sharing and bookkeeping:

| Flag | Effect |
|---|---|
| `CLONE_VM` | Share the address space |
| `CLONE_FS` | Share current directory, root directory, and umask |
| `CLONE_FILES` | Share the descriptor table itself |
| `CLONE_SIGHAND` | Share signal dispositions; requires `CLONE_VM` |
| `CLONE_THREAD` | Join the thread group; requires `CLONE_SIGHAND` |
| `CLONE_SETTLS` | Set the child TLS value |
| `CLONE_SYSVSEM` | Share the System V semaphore-adjustment list |
| `CLONE_IO` | Share the I/O context where the I/O scheduler uses it |
| `CLONE_PIDFD` | Return a pidfd identifying the created task |
| `CLONE_PARENT` | Use the caller's parent; prohibited for an init process |
| `CLONE_PARENT_SETTID`, `CLONE_CHILD_SETTID` | Store the new TID in the specified address space |
| `CLONE_CHILD_CLEARTID` | Arrange exit-time clearing and futex notification |
| `CLONE_UNTRACED` | Prevent a tracer from forcing `CLONE_PTRACE` on this child |
| `CLONE_VFORK` | Suspend the caller until the child releases the shared address space |

A conventional thread uses shared memory, filesystem context, descriptors,
signal dispositions, and a thread group, with TLS and TID bookkeeping.
Threads share `getpid()` and signal actions but have individual signal masks.
Ordinary `CLONE_THREAD` termination is not collected through the process wait
interface; the process's parent collects the thread group's termination.

The `CLONE_NEW*` flags select namespace separation. In Peios, private mount
namespaces have their own KACS object model; the other namespace operations
must satisfy their privilege checks. See the [namespace
contract](~kernel/internals/kacs/mount-namespaces/overview) rather than treating
all flags as available to an ordinary caller. `CLONE_INTO_CGROUP` has separate
target-cgroup rules. `CLONE_DETACHED` has no general detached-thread meaning;
incompatible combinations, including with `CLONE_PIDFD`, can be rejected.

## Replace the executable

`execve` selects a pathname. `execveat` can select relative to a directory
file descriptor or use `AT_EMPTY_PATH` with a file descriptor directly.
`AT_SYMLINK_NOFOLLOW` refuses a final symbolic link. `fexecve` is the C
library
interface for descriptor-based execution; its mechanism depends on the
runtime.

A successful exec preserves the process identity while replacing the program:

| Preserved | Replaced or reset |
|---|---|
| PID, parent PID, Process GUID, process group, session, and controlling terminal | Program mappings, stack, heap, and memory locks |
| Descriptors without close-on-exec | Descriptors marked close-on-exec |
| Current directory, root directory, umask, and resource limits | Other threads in the group |
| Signal mask, pending signals, and ignored dispositions | Caught-signal handlers and alternate signal stack |
| Primary token, subject to the Peios exec rules | Active impersonation, reverted before the new program starts |

Exec also discards attached System V shared memory, POSIX shared-memory
mappings, POSIX message-queue descriptors, named semaphore references,
POSIX timers, outstanding asynchronous I/O, registered exit handlers,
directory streams, and runtime
synchronization state. The floating-point environment is reset and the
process name follows the new executable.

`NEW_PROCESS_MIN` can lower token integrity according to the executable's
explicit label. Execution trust, process protection, and PSB rules apply
separately. Set-user-ID bits do not provide the upstream identity transition.
Read the detailed token rules before claiming identity survives unchanged.

## Stable process handles

A pidfd refers to a particular task instance, avoiding later PID reuse:

| Operation | Purpose |
|---|---|
| `pidfd_open` | Open a handle for an existing task |
| `pidfd_send_signal` | Send a signal through that stable handle |
| `pidfd_getfd` | Duplicate a target task's descriptor into the caller |

Opening by PID still requires obtaining the intended PID safely. A pidfd does
not waive signaling or cross-process descriptor access checks. KACS applies
the target process's access rules to the corresponding operation.
