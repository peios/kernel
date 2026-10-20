---
title: "Overview"
description: "LCS is the kernel half of the Peios registry — where it sits, its semantic core, what is layered and what is not, and where the model diverges."
type: reference
---

<a id="trm-5-1"></a>

LCS — the Layered Configuration Subsystem — is the kernel half of the
Peios registry: a hierarchical, access-controlled configuration store
modelled on the Windows registry. It owns the namespace, the security
model, change observation, transactions, and the layer system that
gives the registry its name. It owns no storage at all.

Storage belongs to **sources**: userspace processes that hold registry
data and answer questions about it over the Registry Source Interface.
A source stores what it is told and returns everything it holds; it
never resolves layers, never filters by visibility, never sees the
identity of a caller, and never interprets a path beyond the parent and
child names it is given. Every decision about what a caller may see or
do is made in the kernel. loregd is the first source, and the one that
provides `Machine\` and `Users\` at boot, but nothing in LCS knows that:
hive routing is built entirely from what registers.

Userspace never talks to a source. Processes reach the registry through
three syscalls and eighteen ioctls, and the fd those syscalls return is
a capability — an open key carries the access mask it was granted, and
carries it wherever the fd goes.

<a id="trm-5-1-1"></a>

## Where it sits

LCS is a subsystem of PKM, peer to KACS and KMES, implemented in
`security/pkm/lcs` and built by `CONFIG_SECURITY_PKM` — a
boolean option, so it is linked into `vmlinux` rather than loaded. Its
three syscalls occupy 1100–1102 in the PKM range, registered in
`arch/x86/entry/syscalls/syscall_64.tbl`.

It depends on KACS and KACS does not depend on it. Every access
decision LCS makes is a call into the KACS AccessCheck function against
a Security Descriptor the source returned; LCS defines no access
control mechanism of its own. Security Descriptor inheritance at key
creation is likewise KACS's computation, not LCS's. Audit events go to
KMES.

A substantial part of LCS is Rust. The `lcs-core` implementation lives
in `security/pkm/lcs/lcs_core` and holds
the parts where correctness is a matter of pure decision rather than
kernel plumbing: layer resolution, the RSI wire codec, the backup
stream serialiser, the transaction mutation log, watch dispatch, case
folding, and configuration validation. The C half owns fds, the char
device, memory, locking, and the syscall boundary.

<a id="trm-5-1-2"></a>

## The semantic core

Six rules generate the rest of the model. Every behaviour described in
this chapter is a consequence of one of them.

1. **Names are layered.** A key's presence at a path is per-layer.
   Different layers can name different keys at the same path, and
   removing a layer removes its names.
2. **Values are layered.** Every write is tagged with a layer; the
   effective value is the highest-precedence entry. Tombstones can
   actively mask lower layers.
3. **Key identity is not layered.** A key's GUID, Security Descriptor,
   volatile flag, symlink flag and last write time belong to the key
   object, not to any layer, and are never automatically reverted.
4. **Security is key-bound, not layer-bound.** Modifying a Security
   Descriptor is a permanent change to the key. Removing a layer does
   not revert it. Security policy is operational state, not
   configuration overlay.
5. **Handles are capabilities granted at open.** An open key fd carries
   an access mask computed once, by AccessCheck, at open time. Later
   operations test the mask, not the descriptor. Changing a descriptor
   does not affect an fd that already exists.
6. **Sources persist, the kernel decides meaning.** A source stores
   path entries, key records and value entries and returns all of them.
   Everything else is the kernel's.

The consequence that surprises people most often is the fourth. A
layer is a configuration overlay and reverts cleanly; an access control
change is not configuration and does not.

<a id="trm-5-1-3"></a>

## What is layered and what is not

| Property | Layered | Resolved by | Survives layer deletion |
|---|---|---|---|
| Path existence | Yes | Highest precedence, then highest sequence | No |
| Values | Yes | Highest precedence, then highest sequence | No |
| Value tombstones | Yes | Masking lower precedence | No |
| Blanket tombstones | Yes | Masking all lower-precedence values on the key | No |
| Key hiding | Yes | Masking lower precedence | No |
| Key GUID | No | Direct on the key object | Yes |
| Security Descriptor | No | Direct on the key object | Yes |
| Volatile flag | No | Direct on the key object | Yes |
| Symlink flag | No | Direct on the key object | Yes |
| Last write time | No | Direct on the key object | Yes |

A watch is bound to the key object rather than to either, and stays on
that object whatever happens to the name ([Dispatch](<~kernel/internals/lcs/watches/dispatch#trm-5-6-3>)).

<a id="trm-5-1-4"></a>

## registry.pol

One external format constrains the design. `registry.pol` is the binary
format Active Directory Group Policy uses to deliver configuration to
domain-joined machines, and the registry exists so that Peios can
consume it without loss. Everything `registry.pol` can express, the
registry can represent.

Three consequences run all the way through:

- The **full Windows value type set** is supported, including the three
  hardware-resource types that carry no Peios semantics at all. They
  behave exactly as `REG_BINARY`; they exist so a value copied from a
  Windows hive round-trips with its type tag intact ([Values](<~kernel/internals/lcs/data-model/values#trm-5-2-6>)).
- **Paths are backslash-separated, case-preserving and
  case-insensitive.** This is not negotiable and it is the reason case
  folding appears in the kernel at all ([Names and Case](<~kernel/internals/lcs/data-model/names-and-case#trm-5-2-8>)).
- **Registry access rights occupy the Windows bit positions**, so a
  Security Descriptor containing registry ACEs is binary-compatible
  ([Access Rights](<~kernel/internals/lcs/security/access-rights#trm-5-4-2>)).

Tombstones and blanket tombstones exist for the same reason: the
`**Del.ValueName` and `**DelVals` directives express *absence*, which a
purely additive overlay cannot ([Tombstones](<~kernel/internals/lcs/data-model/tombstones#trm-5-2-7>)).

LCS does not parse `registry.pol`. Parsing is a userspace concern; LCS
provides the model that makes a faithful translation possible.

No other parity with Windows is claimed. The binary compatibility of a
Security Descriptor is a KACS guarantee, not an LCS one.

<a id="trm-5-1-5"></a>

## Where the model diverges from Windows

LCS is modelled on the Windows Configuration Manager, and departs from
it in seven places. All seven are decisions rather than gaps.

| | Windows | LCS |
|---|---|---|
| Backing store | Kernel-internal hive files | Userspace sources over the RSI, so a storage backend is not a kernel change |
| Hive routing | A fixed set of predefined hives | Any source may register any name at runtime |
| Layers | None; `registry.pol` is applied by flattening values | Precedence-ordered layers with tombstones, resolved at query time, so removal reverts rather than tattoos |
| Change observation | `RegNotifyChangeKeyValue`, single-shot | Persistent watches, closing the re-registration race |
| Key identity | Hive cell offsets | GUIDs, stable across storage reorganisation |
| Forward slash | Not accepted | Accepted on input, normalised to backslash |
| Case comparison | `RtlCompareUnicodeString` | Unicode Simple Case Folding, pinned to a version |

<a id="trm-5-1-6"></a>

## Windows features that are absent

Four have been evaluated and deliberately excluded.

**Key classes.** The `class` parameter of `RegCreateKeyEx` is
documented by Microsoft as reserved, and no consumer of it is known.

**`RegOverridePredefKey`.** Per-process key redirection, and specific
to COM. It would require unbounded per-process state in the kernel, and
private hives and private layers cover the uses that are legitimate.

**WoW64 redirection.** Splitting keys by pointer width. Peios has no
32-bit compatibility concern to split for.

**The `HKEY_CLASSES_ROOT` merged overlay.** A merge of `HKLM` and
`HKCU` `Software\Classes`, again COM-specific, with no Peios
equivalent.

<a id="trm-5-1-7"></a>

## This chapter

[Hives and Routing](<~kernel/internals/lcs/data-model/hives-and-routing#trm-5-2-1>) covers the data model — hives, keys, path entries, values,
tombstones, names, and what happens to a key that loses its last name.
[The Layer Model](<~kernel/internals/lcs/layers/the-layer-model#trm-5-3-1>) covers layers: the model, the base layer, where layer metadata
lives and the circularity that implies, who may write into a layer, and
the resolution algorithm and the sequence counter that drives it. [The Access Flow](<~kernel/internals/lcs/security/the-access-flow#trm-5-4-1>)
covers security: the access flow, the rights, inheritance, and the audit
events LCS emits. [The Fd Model](<~kernel/userspace/native/lcs/file-descriptors-and-buffer-conventions#trm-5-5-1>) covers the syscall and ioctl interface and the
error model. [The Watch Model](<~kernel/internals/lcs/watches/the-watch-model#trm-5-6-1>) covers watches, [Scope and Lifetime](<~kernel/internals/lcs/transactions/scope-and-lifetime#trm-5-7-1>) transactions, and [The Source Model](<~kernel/internals/lcs/sources/the-source-model#trm-5-8-1>) the source
model — registration, dispatch, validation, and the intricate business
of what a late response means. [The Stream](<~kernel/internals/lcs/backup-and-restore/the-stream#trm-5-9-1>) covers backup and restore, [The Bootstrap Problem](<~kernel/internals/lcs/bootstrap/dependencies-and-boot-sequence#trm-5-10-1>) how
LCS configures itself out of the registry it is serving, and [LCS ABI Reference](<~kernel/userspace/native/lcs/generated-syscall-and-common-abi#trm-5-a>) the
ABI.

Two contracts extracted from LCS are specified rather than described,
because a third party implements the other side of each: the Registry
Source Interface and the registry backup format. Both are chapters of
PSPK.

<a id="trm-5-b-2"></a>

## Build configuration

LCS is built by `CONFIG_SECURITY_PKM`, a boolean option, so it is linked
into `vmlinux` rather than loaded. <a id="cite-lcs-abi-notes.built-in-by-config-security-pkm"></a>

`CONFIG_RUST=y` is required: the resolution core, the RSI codec, the
backup serialiser and the transaction log are Rust, implemented in
`security/pkm/lcs/lcs_core`. <a id="cite-lcs-abi-notes.requires-config-rust"></a>

`CONFIG_SECURITY_PKM_KUNIT` compiles in the in-kernel test
harness. <a id="cite-lcs-abi-notes.kunit-option-compiles-test-harness"></a>

The three syscall numbers are registered in
`arch/x86/entry/syscalls/syscall_64.tbl` and the corresponding table
under `tools/perf/`. <a id="cite-lcs-abi-notes.syscall-numbers-added-by-patch"></a>

They are registered `common`, so the same row serves the x32 ABI
wherever that ABI is built in; the Peios kernel does not build it. <a id="cite-lcs-abi-notes.syscalls-registered-common"></a>

## Related explanations

- [File descriptors and buffer conventions](<~kernel/userspace/native/lcs/file-descriptors-and-buffer-conventions>)

## Calling the subsystem

The [native LCS interface reference](<~kernel/userspace/native/lcs/overview>) collects the caller contracts and generated ABI tables.

## Topics

- [Data model](<~kernel/internals/lcs/data-model/overview>)
- [Layers](<~kernel/internals/lcs/layers/overview>)
- [Security](<~kernel/internals/lcs/security/overview>)
- [Watches](<~kernel/internals/lcs/watches/overview>)
- [Transactions](<~kernel/internals/lcs/transactions/overview>)
- [Sources](<~kernel/internals/lcs/sources/overview>)
- [Backup and restore](<~kernel/internals/lcs/backup-and-restore/overview>)
- [Bootstrap](<~kernel/internals/lcs/bootstrap/overview>)
