---
title: "Peios kernel behaviour"
type: guide
description: "How Peios changes Linux authority, process access, filesystems and networking."
---

The Peios kernel retains Linux interfaces and adds native security and system
services. Read inherited Linux documentation with the distinctions below. A
documented driver, architecture or configuration option is not a promise that
the Peios build enables or qualifies it.

This guide describes the committed Peios implementation based on Linux 7.0.9.
Build configuration is defined by `peios/config/pkm.fragment`, with invariants
checked by `peios/verify-config.sh`. See [Building Peios](<~kernel/development/start-here/building-peios>)
for the supported repository entry points and the limits of development outputs.

## Authority and identity

KACS makes native access decisions using tokens, security descriptors and
enabled privileges. UID 0 is not a universal authority bypass. Unix IDs, mode
bits and Linux capability sets remain compatibility interfaces; they do not
replace KACS decisions. Code that checks a Linux capability still calls the
usual API, but KACS interprets that check as described below.

Some inherited checks still inspect IDs and modes directly. For example,
`/proc/sys` table permissions select mode bits using the current effective UID
and groups, with subsystem-specific callbacks where provided; individual
handlers can add capability checks. Keyrings and remote filesystem protocols
also retain their own permission/authentication rules. Do not infer that every
Unix field is ignored or that every interface has a native SD gate.

| Linux capability check | Peios interpretation |
| --- | --- |
| `CAP_CHOWN`, `CAP_DAC_OVERRIDE`, `CAP_DAC_READ_SEARCH`, `CAP_FOWNER`, `CAP_FSETID`, `CAP_KILL`, `CAP_SETGID`, `CAP_SETUID`, `CAP_NET_BROADCAST`, `CAP_IPC_OWNER`, `CAP_LEASE`, `CAP_NET_BIND_SERVICE` | Compatibility checks pass; native object access checks remain necessary. These bits are not authority grants. |
| `CAP_SETPCAP`, `CAP_SETFCAP`, `CAP_MAC_OVERRIDE` | Denied to ordinary callers. An internal StrataFS copy-up exception is not a userspace grant mechanism. |
| `CAP_LINUX_IMMUTABLE`, `CAP_NET_ADMIN`, `CAP_NET_RAW`, `CAP_SYS_RAWIO`, `CAP_SYS_CHROOT`, `CAP_SYS_PACCT`, `CAP_SYS_ADMIN`, `CAP_SYS_TTY_CONFIG`, `CAP_MKNOD`, `CAP_SYSLOG`, `CAP_WAKE_ALARM`, `CAP_BLOCK_SUSPEND`, `CAP_BPF`, `CAP_CHECKPOINT_RESTORE` | `SeTcbPrivilege` |
| `CAP_IPC_LOCK` | `SeLockMemoryPrivilege` |
| `CAP_SYS_MODULE` | `SeLoadDriverPrivilege` |
| `CAP_SYS_PTRACE` | `SeDebugPrivilege` |
| `CAP_SYS_BOOT` | `SeShutdownPrivilege`; remote-origin shutdown also requires `SeRemoteShutdownPrivilege`. |
| `CAP_SYS_NICE` | `SeIncreaseBasePriorityPrivilege` |
| `CAP_SYS_RESOURCE` | `SeIncreaseQuotaPrivilege` |
| `CAP_SYS_TIME` | `SeSystemtimePrivilege` |
| `CAP_AUDIT_WRITE` | `SeAuditPrivilege` |
| `CAP_AUDIT_CONTROL`, `CAP_MAC_ADMIN`, `CAP_AUDIT_READ` | `SeSecurityPrivilege` |
| `CAP_PERFMON` | Any of `SeSystemProfilePrivilege`, `SeProfileSingleProcessPrivilege` or `SeLoadDriverPrivilege` satisfies this compatibility check. Operation-specific profiling checks still apply. |

Privilege entries mean an enabled privilege in the subject token, not a bit
that an application can acquire with `capset`, `setcap` or a set-user-ID binary.
Unknown capability checks are denied. The table describes userspace subjects;
internal kernel operations have explicit handling of their own.

The `setuid`, `setgid` and supplementary-group compatibility paths ordinarily
restore the existing credential values and return success without changing
native identity. With `SeAssignPrimaryTokenPrivilege` enabled, those identity
changes return `EOPNOTSUPP` rather than installing a token. Use native token
operations for identity changes. Do not use a successful Unix-ID setter as
evidence that authority was dropped. Executing a set-user-ID file does not
mint native privileges either.

## File and device access

On managed mounts, KACS authorizes access against a security descriptor (SD).
The canonical stored attribute is `security.peios.sd`; NTFS3 uses
`system.ntfs_security`. Use the native SD operations rather than generic
`setxattr` to change these descriptors. POSIX ACL update hooks are unsupported,
and setting Linux file capabilities is not a privilege-delegation mechanism.

Changing ownership or mode bits does not replace a descriptor update.
`fchmod` requires `WRITE_DAC` and `fchown` requires `WRITE_OWNER` on a managed
handle. Consequently, inherited recipes using `chmod 666`, `chown`, Unix groups
or `setcap` alone do not establish access for a Peios principal. This includes
device nodes. A driver's own capability and ioctl checks still apply after
the device has been opened.

An open managed file carries a granted-access snapshot. Later operations check
the relevant rights on that handle; changing its pathname's SD is not a
general revocation of existing handles. Metadata operations also have rights:
for example, file statistics require `FILE_READ_ATTRIBUTES`. Append-only grants
do not permit positioned overwrites, clearing `O_APPEND`, truncation or other
operations that require `FILE_WRITE_DATA`.

Opening by filesystem handle additionally requires enabled
`SeChangeNotifyPrivilege`; it is not authorized by the compatibility
`CAP_DAC_READ_SEARCH` bit alone.

Ordinary filesystem types default to denying access when an SD is missing.
NFS, FAT, exFAT, ISO9660, ramfs and cgroup2 default to synthesizing ephemeral
descriptors from a mount template. Procfs and sysfs are unmanaged by this
file-descriptor policy and have separate checks. In particular, sysfs writes
have a KACS gate; “unmanaged” does not mean unrestricted. StrataFS requires
stored descriptors. System tmpfs and SquashFS also default to deny-missing;
their contents must be seeded or stamped appropriately.

With PKM and tmpfs enabled, initramfs rootfs is always tmpfs, including when
`root=` or `rootfstype=ramfs` is supplied. Peios seeds its root descriptor, and
also seeds devtmpfs. This is necessary for descriptor storage and inheritance.

## Mount namespaces

Mount operations have a privilege path through `SeManageVolumePrivilege` or
`SeTcbPrivilege`. There is also a mount-namespace descriptor path for callers
without those privileges. It admits bind mounts, unmounts, `pivot_root` and new
mounts of `tmpfs`, `proc` and `stratafs`, subject to the namespace's mount right
and the filesystem's own checks. Other filesystem types, remounts, moves and
propagation changes do not gain this descriptor-only authorization.

A tmpfs admitted through the unprivileged descriptor path receives an
ephemeral descriptor template. Privileged system tmpfs mounts keep their
deny-missing default and must be seeded. StrataFS stratum creation still needs
initial-user-namespace TCB authority; the descriptor path does not confer it.
Creating a mount namespace alone can use native authorization; combining it
with other namespace creation flags does not remove their privilege gates.
Creating a user namespace does not manufacture native token privileges.

## System V IPC

Message queues, shared-memory segments and semaphore arrays receive a native
descriptor from the creator's token. Their read and write checks use native
IPC rights. `CAP_IPC_OWNER` is a compatibility pass that lets the request reach
the KACS hook; it does not bypass that hook. The nine Unix permission bits are
not the native authority boundary.

`IPC_RMID` requires delete access, `IPC_SET` requires write-DAC and write-owner
access, and `IPC_STAT` requires query-information access. Object-specific
commands have their own rights, including read/write for semaphore values and
set-information for shared-memory lock changes. Commands that query global
IPC information have no individual object descriptor to check.

## Process access and inspection

Cross-process access uses the target process descriptor and process integrity
protection (PIP). The caller must dominate the target's protected integrity
type and trust. `SeDebugPrivilege` can rescue an eligible descriptor denial;
it does not bypass PIP dominance. Same-process and kernel-origin operations
have explicit exceptions. Equal Unix IDs are not the authorization rule.

| Operation | Native process right or additional gate |
| --- | --- |
| Read another process's memory, including `process_vm_readv` and read-only `/proc/PID/mem` | `PROCESS_VM_READ` |
| Ptrace attachment, `process_vm_writev`, writable `/proc/PID/mem` | `PROCESS_VM_WRITE` |
| `pidfd_open` | `PROCESS_QUERY_LIMITED_INFORMATION` |
| `pidfd_getfd` | `PROCESS_DUP_HANDLE` |
| Basic proc metadata such as `stat`, `statm`, `comm`, `cgroup` | `PROCESS_QUERY_LIMITED_INFORMATION` |
| Proc metadata such as `status`, `cmdline`, `io`, `limits`, `sched` | `PROCESS_QUERY_INFORMATION` |
| Process-setting operations | `PROCESS_SET_INFORMATION`, with operation-specific checks |
| Change another process's CPU affinity | `SeIncreaseBasePriorityPrivilege`, process set-information access and PIP dominance |
| Profile another process | `SeProfileSingleProcessPrivilege`, process query-information access and PIP dominance |
| System-wide `perf_event_open` with `pid == -1` outside cgroup mode | `SeSystemProfilePrivilege` |

Proc entries are checked individually; their Unix modes are not the complete
policy. `/proc/PID/fd` access also checks process-read access. There is no
`CAP_PERFMON` fallback that bypasses a KACS refusal to read another process's
memory. See [Perf security](<~kernel/administration/admin-guide/resources/perf-security>)
for the additional Linux perf controls. Cgroup-scoped perf events skip the
two native profiling gates listed above; they retain cgroup-handle and Linux
perf checks, not per-target process-query/PIP authorization. Do not infer
that the ordinary system-wide gate covers this mode.

Signal authorization is native too. Signal 0 queries limited information;
stop/continue signals require suspend/resume access; `SIGCHLD`, `SIGURG` and
`SIGWINCH` use signal access; termination-class signals, including user and
real-time signals, use terminate access. Matching UIDs or sessions alone do
not authorize these operations. `/proc/PID/token`, per-thread `token` and
`/proc/PID/psb` expose native token or process-security information subject to
their access checks.

## Execution and system integrity

Execution checks file-execute access and the process security baseline (PSB).
PSB restrictions can additionally constrain executable mappings, library trust,
child creation and architecture controls. Hardware and runtime support matter:
a declared mitigation bit does not establish that activation is available.
In this implementation, live-task CFIF activation returns `ENODEV` even when
the CPU has IBT; it is not an available userspace enforcement path. CFIB uses
the shadow-stack support and prevents subsequent disable/unlock operations.

Unsigned ordinary executables can run without a PIP integrity label, subject
to access and mitigation checks. Their token still determines their authority.
Kernel-initiated usermode helpers have a stronger rule: the executed image must
have at least `PeiosTcb` trust. Redirecting `modprobe` to an arbitrary script
does not satisfy this rule. The configured helper path is `/bin/modprobe`.
Tracing and `no_new_privs` prevent exec from raising the process's PIP label
above its current label.

The configured LSM list is `landlock,lockdown,integrity,pkm`. SELinux, AppArmor,
Smack, TOMOYO and BPF LSM are incompatible with this PKM configuration; other
inherited LSM guides describe optional upstream mechanisms, not active Peios
policy. Landlock can add restrictions; it cannot grant access KACS denies.

The build enforces module signatures and integrity lockdown. Enabling a native
privilege does not turn those checks off. Raw build outputs still contain
unsigned modules; they require the separate signing stage before use.
Lockdown restricts debugfs interfaces and unsigned kernel replacement and
disables hibernation. Read-only debugfs files meeting its safety checks can
remain accessible; signed `kexec_file` verification has its own path.

File-based firmware loading has a Peios signature policy. The development
configuration defaults to `kacs_fwsig=log`; `kacs_fwsig=enforce` requests
enforcement for reads through the firmware file hooks. It does not cover
built-in or platform-supplied blobs, sysfs request fallback, or the separate
`FW_UPLOAD` interface. The configured build disables the request fallback,
while device upload support remains enabled. These paths can have other checks;
module signing does not establish blanket firmware signature enforcement.

## Networking

NTFE is the configured network policy engine. The profile disables nftables,
xtables/iptables, NFQUEUE/NFLOG, IPVS, flow tables, bridge netfilter and BPF
netfilter hook attachment. Conntrack, defragmentation and rejection support
remain enabled for NTFE. NAT machinery remains present but has no enabled
legacy policy configurator. Inherited nftables and iptables command examples
are not Peios policy-installation instructions.

Before the first policy is ingested, NTFE generation zero is deliberately
permissive and logs that condition. Building or booting NTFE does not by itself
install a restrictive policy. A layer without a published policy forest also
permits traffic at that layer, including when another layer has a policy.
Native policy and socket identity checks must
be considered alongside the inherited transport and driver reference.

`ping_group_range` does not authorize Peios datagram ping sockets; they follow
the ordinary native network policy path. Raw sockets retain their privilege
check. `CAP_NET_BIND_SERVICE` is a compatibility pass, so the Linux privileged
port distinction is not the Peios authority boundary. Port reservations and
native socket checks remain relevant. Socket reuse and AF_UNIX identity
handling also use native KACS checks; matching Unix ownership is insufficient.

## Implementation references

The authority mapping and integration rules are implemented in
`security/pkm/kacs/{capability,cred_projection,file_access,file_metadata,`
`mount_policy,mnt_namespace,process_access,exec,psb}.c`, with syscall integration
in `fs/`, `kernel/` and `mm/`. Network policy is under `net/ntfe/`, and the
native layered filesystem is under `fs/stratafs/`. These source paths, the
UAPI headers and the configured build are the basis for this guide; inherited
Linux examples do not override them.
