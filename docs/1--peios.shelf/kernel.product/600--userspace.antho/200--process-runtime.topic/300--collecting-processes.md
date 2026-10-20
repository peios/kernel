---
title: Process Termination and Collection
type: reference
description: Distinguish runtime cleanup, task exit, wait status, and orphan adoption.
---

Process termination and collection are separate operations. A supervisor
must collect the child's result even after all its threads have stopped.

## Termination interfaces

The C runtime and raw syscalls expose different levels of cleanup:

| Interface | Behavior |
|---|---|
| C `exit()` or return from `main` | Run registered exit handlers, flush standard I/O, and perform the runtime's normal termination cleanup |
| C `_exit()` or `_Exit()` | Skip those handlers and standard-I/O flushing; modern Linux runtimes terminate the thread group |
| Raw `exit` syscall | End the calling thread |
| Raw `exit_group` syscall | End the whole thread group |

File-descriptor closure and kernel resource cleanup still occur. An immediate
termination interface is not a promise that kernel cleanup takes no time.
The C runtime's cleanup of its own temporary streams does not remove arbitrary
temporary files an application created.

An external fatal signal can also terminate the process. A fatal default
signal action affects the thread group even when delivery targets a thread.

## Decode the result

Normal termination reports the low 8 bits of the supplied exit code. Signal
termination reports the signal and, where supported, a core-dump flag. Use
status macros instead of decoding a packed `waitpid` result by hand:

| Macro | Meaning |
|---|---|
| `WIFEXITED`, `WEXITSTATUS` | Normal termination and its exit code |
| `WIFSIGNALED`, `WTERMSIG` | Signal termination and the terminating signal |
| `WCOREDUMP` | Core-dump flag where the runtime exposes this macro |
| `WIFSTOPPED`, `WSTOPSIG` | Stop notification and its signal |
| `WIFCONTINUED` | Continue notification |

Check the corresponding predicate before reading the value. A core-dump flag
does not locate a retained core file or prove that a collector saved it.
Stop and continue notifications are not termination.

## Wait interfaces

The wait family chooses a child and the result information:

| Interface | Selection and result |
|---|---|
| `wait` | Any eligible child; PID and packed status |
| `waitpid` | PID or process-group selection, with packed status |
| `waitid` | Explicit ID kind, including `P_PIDFD`, and structured signal information |
| `wait4` | Selection and packed status with resource-usage information |

For `waitpid`, a positive ID selects that child; `-1` selects any child;
zero selects the caller's process group; and a value below `-1` selects the
process group with the corresponding absolute ID. `WNOHANG` avoids blocking.
`WUNTRACED` and `WCONTINUED` request stop and continue observations.

For `waitid`, choose `WEXITED`, `WSTOPPED`, or `WCONTINUED` explicitly.
`WNOWAIT` observes a result without consuming it, leaving it collectable.
A pidfd stabilizes the identifier but does not make a non-child waitable.
Handle interruption and the no-ready-result case according to the interface.

`__WCLONE` selects children whose termination signal differs from `SIGCHLD`;
`__WALL` selects both categories. These do not make ordinary threads created
with `CLONE_THREAD` individually waitable as process children. When children
are automatically reaped because of signal configuration, do not assume a
later wait can recover their status.

## Orphans and subreapers

`prctl(PR_SET_CHILD_SUBREAPER)` marks a process as a subreaper for descendant
orphans. Reparenting selects the nearest eligible living ancestor subreaper;
otherwise the PID namespace's init process adopts the child. It is not
necessarily the first subreaper that originally launched the work.

Adoption changes who must collect the result; it does not itself stop or
restart the child. Preserve separate records of launch, termination,
collection, and any runtime or service-manager restart decision.
