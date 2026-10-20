---
title: "Process integrity protection"
description: "PIP protects objects through trust label ACEs and processes through a dominance test — where it is enforced, and the limits of what it can do."
type: reference
---

<a id="trm-3-7"></a>

PIP protects **objects** from insufficiently trusted processes through
trust label ACEs evaluated inside AccessCheck ([PIP in AccessCheck](<~kernel/internals/kacs/access-check/pip-in-accesscheck#trm-3-8-7>)). It also
protects **processes** — their memory, their execution, their metadata
— from other processes, which is what this section covers.

Every process-to-process operation passes two independent checks, and
both have to succeed. <a id="cite-pip.two-checks-both-required"></a>

The **process descriptor check** is an ordinary AccessCheck of the
caller's token against the target's process descriptor ([Process Security Descriptors](<~kernel/internals/kacs/process-security/process-security-descriptors#trm-3-3-3>)). It
answers *who* may operate on the process, and it is where per-operation
granularity lives — different rights for signals, memory, and
metadata.

The **PIP dominance check** is a direct comparison of the two
processes' PSB fields. It answers *what trust level is required*. It
does not use AccessCheck, does not read a descriptor, and does not
involve the DACL pipeline at all: it is a standalone arithmetic test. <a id="cite-pip.dominance-independent-of-descriptor"></a>

The two are complementary. Object PIP protection stops a non-dominant
process opening authd's private key file; process PIP protection stops
the same process reading the key straight out of authd's memory with
ptrace, or killing authd with a signal.

<a id="trm-3-7-1"></a>

## The dominance test <a id="cite-pip.dominance-both-axes"></a>

```
pip_dominates(caller_psb, target_psb) -> bool:
    if target_psb.pip_type == None:
        return true   // Unprotected target — any caller dominates.
    return caller_psb.pip_type  >= target_psb.pip_type
       AND caller_psb.pip_trust >= target_psb.pip_trust
```

Both axes are plain unsigned integers compared numerically, not closed
enumerations — the dominance layer would happily order tiers the
signing layer cannot currently produce ([PSB Fields](<~kernel/internals/kacs/process-security/psb-fields#trm-3-3-2>)). The early return for
an unprotected target is what keeps ordinary processes universally
accessible whatever trust values a caller happens to carry. <a id="cite-pip.unprotected-target-always-dominated"></a>

Dominance is binary. A caller that does not dominate has no process
access at all, whichever operation was attempted; the descriptor
provides the granularity and PIP is the all-or-nothing gate above it. <a id="cite-pip.dominance-is-all-or-nothing"></a>

That asymmetry with the object model is deliberate. Object access has
natural categories — read, write, execute. Process access does not: a
caller that can ptrace a process can read its memory, inject code, and
effectively become it. Partial process access is not a meaningful
boundary.

<a id="trm-3-7-2"></a>

## SeDebugPrivilege <a id="cite-pip.sedebug-bypasses-descriptor-only"></a>

`SeDebugPrivilege` bypasses the descriptor check and never the
dominance check. This holds at every enforcement point, and it is
enforced structurally in two independent places: inside the descriptor
evaluation a PIP-label denial short-circuits *before* the debug
rescue is reached, and the standalone dominance test runs afterwards
with no privilege escape of any kind.

<a id="trm-3-7-3"></a>

## Where dominance is enforced

**ptrace**, in every mode. A single successful attach is equivalent to
full compromise of the target — read and write memory and registers,
single-step, inject signals, redirect execution — so a non-dominant
caller is refused whatever the mode. <a id="cite-pip.ptrace.all-modes"></a> The Linux `__ptrace_may_access`
path is patched to return the LSM's answer directly, so native UID and
capability rules no longer grant where KACS denies. <a id="cite-pip.ptrace.lsm-answer-final"></a> Direct memory
access through `/proc/<pid>/mem`, `process_vm_readv` and
`process_vm_writev` routes through the same check, so one hook covers
every memory-access vector. <a id="cite-pip.ptrace.covers-memory-vectors"></a> This is what makes in-memory secrets
genuinely unreachable: a compromised administrator cannot read an
HSM daemon's key material out of its address space.

`PTRACE_TRACEME` inverts the roles — the nominated tracer is the
subject and the caller is the target — and requires `PROCESS_VM_WRITE`
on the caller's own descriptor plus dominance by the nominated tracer. <a id="cite-pip.ptrace.traceme-inverted"></a>

Mode combinations are validated: the mutually exclusive
`PIDFD_OPEN`, `GETFD` and `PROC_QUERY` flags cannot be combined, and a
request that is neither a read nor an attach, or claims to be both, is
rejected as malformed. <a id="cite-pip.ptrace.mode-combinations-rejected"></a>

**Signal delivery**, uniformly regardless of signal type. <a id="cite-pip.signal.uniform-all-types"></a> Lifecycle
management of PIP-protected processes therefore has to go through a
process that dominates them — in practice peinit, which runs at the
highest tier.

Signalling within the same process security state is not a boundary
operation, and the exemption is **structural**: it is a pointer
comparison of the two processes' security state, tested before any
descriptor or dominance evaluation. <a id="cite-pip.signal.same-security-state-exempt"></a> It does not depend on the default
descriptor's self ACE, which is what makes `raise()`, `abort()` and
`pthread_kill()` work for restricted and confined tokens whose
AccessCheck against their own descriptor would fail. <a id="cite-pip.signal.self-signals-work-for-restricted"></a>

Multi-target sends are evaluated per target by Linux's own iteration,
so the signal reaches the permitted subset and the call succeeds if at
least one delivery happened. <a id="cite-pip.signal.multi-target-partial-success"></a> POSIX's same-session `SIGCONT` exception
is deliberately absent — the patched `check_kill_permission` returns
the KACS answer before reaching the switch that carried it — so
`SIGCONT` needs `PROCESS_SUSPEND_RESUME` plus dominance like every
other job-control signal, whatever the session. <a id="cite-pip.signal.sigcont-no-session-exception"></a>

Kernel-originated signals bypass the whole check, as described in
[Process Security Descriptors](<~kernel/internals/kacs/process-security/process-security-descriptors#trm-3-3-3>).

**`pidfd_open()`**, a boundary information query rather than a memory
or attach operation, needs `PROCESS_QUERY_LIMITED` plus dominance. <a id="cite-pip.pidfd-open.query-limited"></a>
**`pidfd_getfd()`** maps to `PROCESS_DUP_HANDLE` plus dominance —
extracting a descriptor from another process is a boundary crossing in
its own right. <a id="cite-pip.pidfd-getfd.dup-handle"></a>

**`/proc` metadata.** Entries that are already ptrace-gated or
memory-open-gated are covered automatically by the ptrace hook. The
rest would leak information about a protected process, so the
non-ptrace-gated entries carry their own descriptor requirement plus
dominance; [Process Security Descriptors](<~kernel/internals/kacs/process-security/process-security-descriptors#trm-3-3-3>) gives the mapping. <a id="cite-pip.proc.metadata-needs-descriptor-and-dominance"></a> The one exception is
`/proc/<pid>/psb`, which needs `PROCESS_QUERY_LIMITED` and no
dominance: a protected process's PIP type, trust and mitigations are
readable to whoever its descriptor lets query it ([PSB Fields](<~kernel/internals/kacs/process-security/psb-fields#trm-3-3-2>)). <a id="cite-pip.proc.psb-exempt-from-dominance"></a> Entries stricter than a metadata
query, such as `/proc/<pid>/stack`, keep their native hardening and
are not brought under the metadata rule. <a id="cite-pip.proc.stricter-entries-keep-native"></a>

Denying access prevents reading inside `/proc/<pid>/` but does not
hide the PID: the directory name is still visible through `getdents`. <a id="cite-pip.proc.pid-visible-not-hidden"></a>
Visible-but-inaccessible is the accepted position.

`/proc` is not FACS-managed — it is a virtual filesystem with no
backing store and no xattrs — so enforcement there happens through
direct kernel checks rather than an object-backed FACS path.

**Capability metadata.** `capget()` on the current process, or on a
thread sharing its security state, is not a boundary operation. <a id="cite-pip.capget.self-and-sibling-exempt"></a>
Against another process it is a detailed information query needing
`PROCESS_QUERY_INFORMATION` plus dominance. <a id="cite-pip.capget.cross-process-query-information"></a>

**Resource limits, scheduler and placement.** Read-only `prlimit`
needs `PROCESS_QUERY_INFORMATION` plus dominance; a limit change needs
`PROCESS_SET_INFORMATION` plus dominance. <a id="cite-pip.prlimit.read-and-change"></a>

- `setpgid()` needs `PROCESS_SET_INFORMATION`; <a id="cite-pip.setpgid.set-information"></a>
- `getpgid()` and `getsid()` need `PROCESS_QUERY_LIMITED`; <a id="cite-pip.getpgid-getsid.query-limited"></a>
- the scheduler, affinity and I/O priority queries need
  `PROCESS_QUERY_INFORMATION`; <a id="cite-pip.sched-queries.query-information"></a>
- and the memory-placement mutations Linux routes through
  `task_movememory` need `PROCESS_SET_INFORMATION`. <a id="cite-pip.movememory.set-information"></a>

Setting nice, scheduler parameters and I/O priority all need
`PROCESS_SET_INFORMATION` too. <a id="cite-pip.sched-set.set-information"></a> Self-directed
versions of all of these are not boundary operations and skip both
checks. <a id="cite-pip.self-directed-skips-checks"></a>

**CPU affinity** is per-thread, so changing the caller's own thread or
a sibling in the same process is not a boundary operation. <a id="cite-pip.affinity.same-process-not-boundary"></a> Changing a
thread in a *different* process needs `PROCESS_SET_INFORMATION` plus
dominance plus `SeIncreaseBasePriorityPrivilege` — and the privilege
is checked and marked used *before* the descriptor and dominance call,
so the `SeDebugPrivilege` rescue cannot substitute for it. <a id="cite-pip.affinity.cross-process-privilege-first"></a> KACS does
not relax the kernel's native affinity validity rules: an invalid or
disallowed mask still fails. <a id="cite-pip.affinity.native-validity-preserved"></a>

**Token opens.** `kacs_open_process_token` and
`kacs_open_thread_token` need `PROCESS_QUERY_INFORMATION` plus
dominance. <a id="cite-pip.token-open.query-information"></a> Reading a process's security identity is as sensitive as
reading its memory.

**Performance monitoring.** Target-specific `perf_event_open()` on
another process can leak execution timing, branch prediction
behaviour, cache access patterns and instruction traces — side
channels that reveal cryptographic keys. It needs
`SeProfileSingleProcessPrivilege` plus `PROCESS_QUERY_INFORMATION`
plus dominance, with the privilege again checked first so the debug
rescue cannot stand in for it. <a id="cite-pip.perf.target-specific-requirements"></a> Own-task profiling is not a boundary
operation and needs no privilege. <a id="cite-pip.perf.own-task-exempt"></a> System-wide profiling, `pid == -1`,
samples every task on a CPU including protected ones, so it needs the
operator-class `SeSystemProfilePrivilege`. <a id="cite-pip.perf.system-wide-privilege"></a> Cgroup perf mode stays
under Linux's native model. <a id="cite-pip.perf.cgroup-native"></a> Because the target task is resolved after
the stock `security_perf_event_open` hook fires, this rule is enforced
through a target-resolved syscall patch rather than that hook — there
is no `security_perf_event_open` registration at all.

<a id="trm-3-7-4"></a>

## The PeiosTcb floor on kernel-initiated execs

One place PIP gates execution rather than merely labelling it. It is
not a dominance test — there is no caller to compare against — but a
threshold: a binary the kernel execs *on its own behalf* must carry at
least PeiosTcb trust, or the exec fails with `EACCES`. <a id="cite-pip.umh.peiostcb-floor"></a>

The case that motivates it is `request_module()`. When the kernel needs
a module it does not have — `get_fs_type()` on a mount, `socket()` for
an unknown protocol family, the crypto API resolving a name — it spawns
`CONFIG_MODPROBE_PATH` as a usermode helper and runs it at the kernel's
own authority. That path is a writable sysctl, which makes redirecting
`/proc/sys/kernel/modprobe` a classic escalation: point it somewhere
attacker-controlled and the next module request executes it with the
kernel behind it. The floor makes the redirection worthless on its own,
because the attacker would also have to produce a TCB-signed binary.

This is the only exec KACS refuses on integrity grounds. Everywhere
else an unsigned binary runs and simply carries no tier, because a
requesting process's own authority bounds what it can do. A
kernel-initiated exec has no such process behind it, so there is no
lesser authority to fall back to.

The floor also refuses when no tier could be derived at all, not only
when one was derived and graded too low. <a id="cite-pip.umh.refuses-underivable-tier"></a> Treating "could not establish
trust" differently from "is not trusted" would leave the check
bypassable by whatever prevented the derivation from running.

Nothing upstream identifies such an exec by the time the LSM sees it.
The helper child is created by `user_mode_thread()`, so it never
carries `PF_KTHREAD` — `kernel_execve()` rejects kernel threads
outright — and `security_kernel_module_request()` fires in the
*requesting* task, before the child exists. So `kernel/umh.c` is
patched to mark the child after `commit_creds()` and before
`kernel_execve()`, and the mark is read in the `bprm_creds_from_file`
hook. It lives in the KACS task blob rather than costing a
`task_struct` flag.

The mark is never cleared. A helper that re-execs — an interpreter for
a `#!` helper — stays under the floor rather than escaping it on the
second exec; the task exists only to be that helper. <a id="cite-pip.umh.mark-never-cleared"></a>

A refusal emits `kacs_exec` with reason `umh-not-tcb`, so it is
visible rather than presenting as an unexplained module-load failure. <a id="cite-pip.umh.audit-reason"></a>

<a id="trm-3-7-5"></a>

## Trust raising under a tracer or supervisor

Dominance is tested when a tracer attaches and when a seccomp filter is
installed, and not again. <a id="cite-pip.unsafe.dominance-tested-at-attach-only"></a> That leaves one way to end up controlling a
process one does not dominate: be attached to it, or supervising its
syscalls through seccomp user notification, when it execs a binary
whose signature would raise its label. Linux marks exactly these execs
— `LSM_UNSAFE_PTRACE` when the task is traced, `LSM_UNSAFE_NO_NEW_PRIVS`
under `no_new_privs`, which every unprivileged seccomp filter requires
— and uses them to withhold setuid gains. KACS applies the same rule to
the label: the exec goes ahead, but the staged label is **capped at
the process's current one** whenever the new label would not be
dominated by it. <a id="cite-pip.unsafe.label-capped"></a> The binary runs with the protection it can be given,
as a setuid binary runs without its setuid under `strace`.

There is no privilege exception. `SeDebugPrivilege` never bypasses
dominance, and a TCB tracer already dominates every label, so nothing
is lost by capping. An exec that does not raise the label — the common
case, and every unsigned binary — is untouched. <a id="cite-pip.unsafe.non-raising-exec-untouched"></a> A cap emits
`kacs_exec` with reason `pip-capped-unsafe` carrying the label that
was kept. <a id="cite-pip.unsafe.audit-reason"></a>

<a id="trm-3-7-6"></a>

## Raw physical memory

A process able to read `/dev/mem` could map any process's physical
pages and bypass virtual memory protections entirely, PIP included.

The defence is `CONFIG_STRICT_DEVMEM`, which restricts `/dev/mem` to
I/O regions and denies RAM access. It is not merely a recommended
build option: the LSM **refuses to initialise** unless both
`CONFIG_STRICT_DEVMEM` and `CONFIG_MODULE_SIG_FORCE` are enabled, so a
kernel configured without them does not boot with KACS at all. <a id="cite-pip.devmem.required-configs"></a> The
same initialisation gate refuses to coexist with SELinux, AppArmor,
Smack, TOMOYO or the BPF LSM. <a id="cite-pip.init.refuses-other-lsms"></a>

Placing a restrictive descriptor on `/dev/mem` and `/dev/kmem` as a
secondary defence is not implemented; nothing in the kernel handles
those paths specially. <a id="cite-pip.devmem.no-descriptor-protection"></a>

<a id="trm-3-7-7"></a>

## Limits of the guarantee

PIP operates inside the kernel's trust boundary, and three things sit
outside it.

**Kernel compromise.** A loaded module runs with unrestricted access
to all memory and kernel structures. PIP is enforced by the kernel, so
a compromised kernel voids it, and `SeLoadDriverPrivilege` is the
ceiling of every guarantee here. `CONFIG_MODULE_SIG_FORCE` is
hard-required as noted above, and module signing is itself ML-DSA-65.
Stripping `SeLoadDriverPrivilege` from every token but peinit's and the
device manager's is the other half of that defence, and is policy
rather than kernel behaviour — nothing in the kernel strips it. The
device manager holds it because loading drivers for the hardware that
appears is its job; module signature enforcement is what keeps the
privilege from meaning more than "load a module Peios built".

**Hardware access.** DMA-capable devices read and write physical
memory directly, bypassing the CPU's virtual memory system. An IOMMU
mitigates this, and configuring one is a kernel responsibility outside
KACS.

**Hypervisor-level isolation.** PIP does not offer guarantees
equivalent to hypervisor-based memory isolation. The threat model
ceiling is a non-compromised kernel.

<a id="trm-3-7-8"></a>

## Impersonation

PIP reads the PSB, never the effective token. A Protected service
impersonating a client still evaluates its own PSB for every process
boundary check, so the client's identity has no bearing on it. <a id="cite-pip.impersonation.reads-psb-not-token"></a> In the
other direction, an unprotected process impersonating a token created
for a protected one gains nothing — its PSB is still None. Since
nothing constrains the PIP dimensions the way the integrity ceiling
constrains impersonation ([Impersonation Lifecycle](<~kernel/internals/kacs/impersonation/state-transitions#trm-3-5-3>)), the PSB is the only safe source.

<a id="trm-3-7-9"></a>

## Coredumps

A crashing PIP-protected process is a potential secret leak, so its
dumps must not be readable by non-dominant processes.

The implemented strategy is to disable them: a process with a nonzero
`pip_type` has its dumpable flag cleared at exec, and
`prctl(PR_SET_DUMPABLE, 1)` is refused for as long as the process
remains protected. <a id="cite-pip.coredump.disabled-for-protected"></a> Requests that keep or make it non-dumpable are
allowed, and no alternative dumpable-setting path is left ungated. <a id="cite-pip.coredump.non-dumpable-requests-allowed"></a> If
a later exec assigns None/0, normal Linux exec-time dumpability rules
apply to the new image. <a id="cite-pip.coredump.unprotected-exec-restores-rules"></a>

The alternative — a signed, high-trust crash handler receiving dump
data from the kernel and writing it under a restrictive descriptor, so
that diagnostics survive without bypassing isolation — is not
implemented. <a id="cite-pip.coredump.no-crash-handler"></a> The two are not mutually exclusive; disabling dumps is
the minimum viable position.
