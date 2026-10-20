---
title: "unshare system call"
type: reference
description: "Unsharing process resources and namespaces in the Peios kernel."
---

<a id="rst-unshare-system-call"></a>

`unshare()` separates selected parts of the calling task's context from other
tasks that share them. It does not create a new process or grant native authority.

<a id="rst-change-log"></a>

## Document history

Adapted from Janak Desai's January 2006 design document for the implementation
in the Peios kernel. The old proposal's address-space splitting and
unimplemented-System-V-semaphore descriptions do not describe this kernel.

<a id="rst-contents"></a>
<a id="rst-overview"></a>

## Overview

`clone()` selects resources to share when creating a task. `unshare()` lets an
existing task stop sharing selected resources, subject to flag combinations,
task state, namespace configuration and authorization checks. An unshared file
descriptor table still refers to the same open file descriptions: it does not
reopen files, reset their positions or obtain new KACS handle grants.

<a id="rst-benefits"></a>
<a id="rst-per-security-context-namespaces"></a>

## Private filesystem views

A private mount namespace permits changes to a task's mount view without
necessarily changing the original namespace. Mount propagation settings can
still propagate events between namespaces. Creating the namespace and making
mounts within it are separate operations with their own authorization.

Peios has a native mount-namespace creation path. When the requested nsproxy
namespace flags select only `CLONE_NEWNS`, `kernel/nsproxy.c` does not impose
its generic `CAP_SYS_ADMIN` gate. Native mount-namespace checks still apply.
Adding another nsproxy namespace type, such as `CLONE_NEWNET` or `CLONE_NEWIPC`,
retains that gate, interpreted as enabled `SeTcbPrivilege`. A new user namespace
does not create native token privileges. See
[Peios kernel behaviour](<~kernel/introduction/peios-behaviour>).

<a id="rst-unsharing-of-virtual-memory-and-or-open-files"></a>

## File tables and address spaces

`CLONE_FILES` can copy a shared file descriptor table. `CLONE_FS` can separate
the root directory, working directory and umask context. In contrast,
`CLONE_VM`, `CLONE_SIGHAND` and `CLONE_THREAD` do not split an actively shared
address space, signal-handler table or thread group. They are accepted only
when the corresponding sharing checks establish there is nothing to split;
otherwise the call fails with `EINVAL`.

<a id="rst-cost"></a>
<a id="rst-requirements"></a>

## Allocation and lifetime

The implementation prepares replacement contexts before publishing them to
the current task. Allocation can fail. Contexts still shared with other tasks
remain alive through their references. Operations must obey the relevant task,
filesystem-context, namespace and credential locking rules.

<a id="rst-functional-specification"></a>

## Interface

```c
#define _GNU_SOURCE
#include <sched.h>

int unshare(int flags);
```

The libc interface returns zero on success, or `-1` with `errno` on failure.
Flags include:

| Flag | Effect or constraint |
| --- | --- |
| `CLONE_FILES` | Separate the file descriptor table if shared. |
| `CLONE_FS` | Separate filesystem context if needed. |
| `CLONE_NEWNS` | Create a mount namespace; implies `CLONE_FS`. |
| `CLONE_NEWUSER` | Create a user namespace; implies `CLONE_THREAD` and `CLONE_FS`, with user-namespace and single-thread checks. |
| `CLONE_NEWUTS`, `CLONE_NEWIPC`, `CLONE_NEWNET`, `CLONE_NEWCGROUP` | Request the corresponding namespace, subject to configuration and authorization. |
| `CLONE_NEWPID`, `CLONE_NEWTIME` | Change the namespace context used for subsequent children; these do not move the caller into the new PID/time namespace. |
| `CLONE_SYSVSEM` | Detach from the shared System V semaphore undo list. `CLONE_NEWIPC` also detaches it. |
| `CLONE_VM` | Implies `CLONE_SIGHAND`; requires an already single-threaded, unshared context. |
| `CLONE_SIGHAND` | Implies `CLONE_THREAD`; cannot split a shared signal-handler table. |
| `CLONE_THREAD` | Requires an empty thread group apart from the caller. |

Unknown or incompatible flags and unsupported sharing requests can return
`EINVAL`. Authorization failures can return `EPERM` or a native denial such as
`EACCES`; allocation failures can return `ENOMEM`. Namespace creation also has
its own configuration, nesting and resource limits, so this is not an exhaustive
error list. UID 0 alone is not the native authorization rule.

<a id="rst-high-level-design"></a>
<a id="rst-low-level-design"></a>
<a id="rst-reorganization-of-copy-functions"></a>

## Implementation

`ksys_unshare()` in `kernel/fork.c` normalizes implied flags, checks supported
combinations, prepares filesystem/file-table changes, then prepares the user
namespace and nsproxy. Namespace-specific creation code runs its own checks.
The function also prepares credential accounting before publishing new state.

<a id="rst-unshare-system-call-service-function"></a>

On success it detaches semaphore state when requested, handles shared-memory
state for a new IPC namespace, installs the nsproxy, swaps the filesystem and
file-table pointers under the required locks, and commits new user-namespace
credentials. It then releases old or unused references. Failure paths release
prepared state rather than leaving partially installed replacement contexts.

<a id="rst-unshare-helper-functions"></a>

`unshare_fs()`, `unshare_fd()`, `unshare_userns()` and
`unshare_nsproxy_namespaces()` prepare the relevant changes. Unlike the original
design proposal, `CLONE_SYSVSEM` is implemented. No helper clones a live shared
address space to implement `CLONE_VM` unsharing.

<a id="rst-finally"></a>

Architecture syscall tables expose the existing `unshare` syscall; adding a
new resource flag does not require a new syscall number.

<a id="rst-test-specification"></a>

## Validation considerations

Test actual resource separation, implied flags, invalid combinations, failure
cleanup and namespace limits. For file tables, distinguish an independent table
from the shared open file descriptions it contains. For Peios, include native
authorization denials and the difference between mount-only namespace requests
and combined namespace requests. These are review requirements, not a report
that this documentation change ran runtime tests.

<a id="rst-future-work"></a>

## Unsupported sharing changes

Splitting a live thread group, shared signal-handler table or shared address
space is not implemented by `unshare()`. Programs requiring a separate address
space should use an appropriate process-creation interface instead.
