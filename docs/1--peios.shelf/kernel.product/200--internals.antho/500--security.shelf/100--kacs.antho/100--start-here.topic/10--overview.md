---
title: "Overview"
description: "KACS is the security core of Peios — an LSM inside PKM providing identity-based access control — and how it relates to MS-DTYP."
type: reference
---

<a id="trm-3-1"></a>

The Kernel Access Control Subsystem is the security core of Peios: an LSM
within PKM providing identity-based access control in the Linux
kernel. It is the sole identity-based authorization mechanism for
managed objects. Every identity-based decision — a file open, a
registry read, an IPC connection, a signal, a token operation — passes
through one evaluation function, AccessCheck.

This chapter covers tokens ([The Token Model](<~kernel/internals/kacs/tokens/the-token-model#trm-3-2-1>)), the Process Security Block ([The PSB Model](<~kernel/internals/kacs/process-security/state-and-lifetime#trm-3-3-1>)),
privileges ([The Privilege Model](<~kernel/internals/kacs/privileges/the-privilege-model#trm-3-4-1>)), impersonation ([Impersonation Levels](<~kernel/internals/kacs/impersonation/levels-and-admission#trm-3-5-1>)), binary signature verification
([Binary Signature Verification](<~kernel/internals/kacs/executable-trust/signature-verification#trm-3-6>)), Process Integrity Protection ([Process Integrity Protection](<~kernel/internals/kacs/executable-trust/process-integrity-protection#trm-3-7>)), the AccessCheck algorithm
in full ([AccessCheck Overview](<~kernel/internals/kacs/access-check/accesscheck-overview#trm-3-8-1>)), file enforcement ([The Handle Model](<~kernel/internals/kacs/file-security/the-handle-model#trm-3-9-1>)), and how Peios identity is
projected onto the Linux credential model ([Credential Projection](<~kernel/internals/security/credentials#trm-3-10-1>)).

The kernel-private storage and call-site inventory is in [LSM integration](<~kernel/internals/kacs/integration/lsm-hooks-and-object-state#trm-3-e>): the LSM
security blobs, every registered KACS hook, and the direct metadata
entry points used by patched file-descriptor operations.

Two bodies of material that KACS owns conceptually live elsewhere in
the documentation. The binary structures — SIDs, security descriptors,
ACLs, ACEs, access masks, conditional ACE bytecode — are specified in
PCDS, because userspace tooling constructs and interprets them and has
to agree with the kernel byte for byte. The signing format a third
party would use to sign a binary with a PIP level is specified in
PSPK; this chapter describes only the verification side. What remains
here is the kernel's own behaviour: how it holds identity, and how it
decides.

<a id="trm-3-1-1"></a>

## Terminology

A **token** is a per-thread identity object held in the kernel's
credential structure, carrying a user SID, group SIDs, a privilege
bitmask, an integrity level, an impersonation level, and metadata.
Identity fields — SIDs, type, integrity level — are immutable; policy
fields — enabled privileges, enabled groups, default owner, group and
DACL — are atomically adjustable. Every thread has a token, and there
is no such thing as a null token.

A **primary token** defines a process's baseline identity and is
inherited on fork, reached through `task->real_cred`. An
**impersonation token** temporarily overrides it for access decisions
on one thread only, reached through `task->cred`.

A **LogonSession** is a kernel object representing one authentication
event: a session ID, a logon type, a user SID, an authentication
package, a logon time, and a logon SID. Tokens reference their session
by ID.

A **privilege** is a system-wide right carried on a token. Some
influence AccessCheck; others gate a standalone operation.

An **impersonation level** controls how far an identity can travel:
Anonymous, Identification, Impersonation, or Delegation. It is a
ratchet carried by every token, primary or impersonation, and only
ever goes down ([Impersonation Levels](<~kernel/internals/kacs/impersonation/levels-and-admission#trm-3-5-1>)).

An **integrity level** is a vertical trust classification on tokens
and objects. Numerically it is the mandatory label SID's single
sub-authority compared as an unsigned integer, so any `S-1-16-<n>`
with exactly one sub-authority is valid. In practice five standard
levels form a strict total order — Untrusted (0), Low (4096), Medium
(8192), High (12288), System (16384) — and non-standard values such as
`S-1-16-8448` appear only in SDs authored for Windows interop.
**Mandatory Integrity Control** is the constraint evaluated before the
DACL, blocking write access, and optionally read and execute, when the
caller's level is below the object's label.

**Process Integrity Protection** is a two-dimensional trust model —
type against trust level — protecting processes and objects from
insufficiently trusted callers. Unlike MIC, it revokes rights that a
privilege would otherwise have granted.

The **Process Security Block** is a per-process structure carrying PIP
identity, process mitigations, and process restrictions. It is never
affected by impersonation, which is the point of keeping it separate
from the token.

**FACS**, the File Access Control Shim, is the part of KACS that
replaces Linux DAC with security-descriptor evaluation on files. It
enforces the handle model: AccessCheck runs at open time and the
granted mask is cached on the file description, with later operations
checked against the cached mask.

An **object type** is the category of a protected resource. Each
defines a GenericMapping table translating generic rights into
object-specific ones.

The **TCB** — the components whose correct behaviour is necessary for
system security — is the Linux kernel, PKM, and the core trusted
userspace daemons: peinit, authd, and loregd.

<a id="trm-3-1-2"></a>

## Relationship to MS-DTYP

KACS is not a port of another system's security model. Tokens,
security descriptors, AccessCheck, structured SIDs, and per-thread
impersonation were chosen because they solve what Peios needs solved:
coherent identity, rich per-object access control, scoped delegation,
and integrated audit.

Those same primitives are the ones Active Directory uses, and Peios is
built to join AD domains as a first-class member — exchanging security
data with domain controllers, authenticating through Kerberos, and
enforcing policy distributed by Group Policy. That imposes binary
format compatibility, which PCDS specifies: an SD written by a Windows
domain controller and replicated through Samba is evaluated by KACS
without translation.

Format compatibility does not imply evaluator compatibility in every
corner. Given the same token, descriptor, and desired mask, KACS
generally reaches the same decision MS-DTYP describes, which is what
makes policy authored in an AD environment behave predictably here.
Where it deliberately does not, [Departures from MS-DTYP](<~kernel/userspace/native/kacs/ms-dtyp-compatibility-and-divergences#trm-3-b>) records every departure and why.

<a id="trm-3-d-8"></a>

## Build configuration

`CONFIG_SECURITY_PKM=y` and `CONFIG_RUST=y` are required, as are
`CONFIG_STRICT_DEVMEM=y` and `CONFIG_MODULE_SIG_FORCE=y`. The last two,
and the absence of every other MAC LSM and of `CONFIG_BPF_LSM`, are
enforced at build time by `BUILD_BUG_ON` in `pkm_init` ([Process Integrity Protection](<~kernel/internals/kacs/executable-trust/process-integrity-protection#trm-3-7>)): a kernel
configured without them does not compile. They were once checked at
initialisation instead, which is no refusal at all -- the LSM framework
answers a failed init with a warning and boots with the hooks
uninstalled, the opposite of what the gate intends (PEI-487). <a id="cite-abi-notes.build.configs-enforced-at-build"></a>
`CONFIG_SECURITY_SELINUX`, `_APPARMOR`, `_SMACK` and `_TOMOYO` are
additionally refused by Kconfig dependency. `CONFIG_LSM` is never
parsed.

Two further symbols gate large bodies of code:

- `CONFIG_SECURITY_PKM_KUNIT`, which compiles in the test harness and,
  in the signing path, a different and publicly known verification key
  ([Binary Signature Verification](<~kernel/internals/kacs/executable-trust/signature-verification#trm-3-6>)). <a id="cite-abi-notes.build.kunit-test-key"></a>
- `CONFIG_STRATAFS_FS`, without which the copy-up API of [The StrataFS Copy-Up Context](<~kernel/internals/stratafs/security/kacs-admission-and-object-phases#trm-3-9-7>) is
  inert. <a id="cite-abi-notes.build.stratafs-gates-copy-up"></a>

## Related explanations

- [ABI status and naming differences](<~kernel/userspace/native/kacs/abi-status-and-naming-differences>)
- [Descriptor and ACE semantics](<~kernel/userspace/native/kacs/descriptor-and-ace-semantics>)
- [Token query semantics](<~kernel/userspace/native/kacs/token-query-semantics>)
- [Socket ABI compatibility](<~kernel/userspace/native/kacs/socket-abi-compatibility>)

## Calling the subsystem

The [native KACS interface reference](<~kernel/userspace/native/kacs/overview>) collects the caller contracts and generated ABI tables.

## Topics

- [Tokens](<~kernel/internals/kacs/tokens/overview>)
- [Process security](<~kernel/internals/kacs/process-security/overview>)
- [Privileges](<~kernel/internals/kacs/privileges/overview>)
- [Impersonation](<~kernel/internals/kacs/impersonation/overview>)
- [Executable trust](<~kernel/internals/kacs/executable-trust/overview>)
- [Access check](<~kernel/internals/kacs/access-check/overview>)
- [File security](<~kernel/internals/kacs/file-security/overview>)
- [Linux credentials](<~kernel/internals/kacs/linux-credentials/overview>)
- [System V IPC](<~kernel/internals/kacs/system-v-ipc/overview>)
- [Network objects](<~kernel/internals/kacs/network-objects/overview>)
- [Mount namespaces](<~kernel/internals/kacs/mount-namespaces/overview>)
- [Auditing](<~kernel/internals/kacs/auditing/overview>)
- [Integration](<~kernel/internals/kacs/integration/overview>)
