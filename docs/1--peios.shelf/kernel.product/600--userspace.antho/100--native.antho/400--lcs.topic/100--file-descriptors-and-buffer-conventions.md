---
title: "File descriptors and buffer conventions"
description: "The hybrid syscall and ioctl interface — key fds, open-time checking, transaction fds, and the conventions for strings and output buffers."
type: reference
---

<a id="trm-5-5-1"></a>

LCS uses a hybrid syscall/ioctl interface, the same shape KACS uses
within PKM.

**Syscalls** create file descriptors: opening a key, creating a key,
beginning a transaction. There are three, numbered 1100 to 1102 in the
PKM range. <a id="cite-fd.three-syscalls-numbered-1100-to-1102"></a>

**Ioctls** operate on a descriptor that already exists —
eighteen of them, all under type byte `'R'`. <a id="cite-fd.eighteen-ioctls-under-type-r"></a>

**`close()`** releases
both kinds of fd through the ordinary fd lifecycle. <a id="cite-fd.close-releases-both-kinds"></a>

<a id="trm-5-5-1-1"></a>

## Key fds

A key fd is an anonymous inode created with `O_CLOEXEC`, holding: <a id="cite-fd.key-fd-is-an-anonymous-inode-with-cloexec"></a>

| Field | Description |
|---|---|
| Source and key GUID | The identity of the opened key. |
| Granted access mask | Computed once by AccessCheck at open. Immutable. |
| Resolved path | After symlink resolution and `CurrentUser\` rewriting. |
| Ancestor chain | The GUID at each path component from the hive root down. Captured during the open walk, used for subtree watch dispatch ([Dispatch](<~kernel/internals/lcs/watches/dispatch#trm-5-6-3>)). |
| Watch state | Armed or not, filter, subtree flag, pending event queue. |

Key fds behave like any other fd: `close()`, close-on-exec,
`poll`/`epoll`, and passing over Unix sockets with `SCM_RIGHTS`. <a id="cite-fd.key-fds-are-ordinary-fds"></a> That
last one is what makes them capabilities ([The Access Flow](<~kernel/internals/lcs/security/the-access-flow#trm-5-4-1>)).

<a id="trm-5-5-1-2"></a>

## Open-time checking

A caller names a desired access mask, and AccessCheck evaluates it
against the key's Security Descriptor. All of it is granted or the open
fails with `EACCES`. `MAXIMUM_ALLOWED` is the only way to ask for
whatever is available.

The granted mask lives on the fd, and every subsequent ioctl is a
bitmask test against it — not a fresh AccessCheck, and not a fresh read
of the descriptor.

Opening relative to a parent fd skips both path parsing and
AccessCheck for the parent portion. The caller already proved its
access when it obtained the parent fd, and this is the ordinary way to
walk a subtree.

<a id="trm-5-5-1-3"></a>

## Transaction fds

A transaction fd is an anonymous inode holding a transaction id and,
once bound, its source and hive. <a id="cite-fd.txn-fd-holds-id-source-and-hive"></a> Transaction lifetime is fd lifetime:
closing without committing aborts ([Scope and Lifetime](<~kernel/internals/lcs/transactions/scope-and-lifetime#trm-5-7-1>)).

<a id="trm-5-5-1-4"></a>

## Reserved fields

Every syscall and ioctl argument structure uses natural C layout with
fixed-width fields and explicit padding. Nothing is packed. <a id="cite-fd.structs-use-natural-c-layout"></a>

Fields named `_pad`, and anything else described as reserved, are ABI
extension points. **A caller must set them to zero**, and a non-zero
reserved or padding field fails the operation with `EINVAL` — before
source dispatch, before transaction enlistment, before sequence
allocation, and before any output is copied. <a id="cite-fd.non-zero-reserved-field-is-einval"></a>

In the other direction, LCS zeroes every reserved and padding byte of
an output structure or a watch event before copying it to userspace. <a id="cite-fd.output-padding-is-zeroed"></a>

Flags fields carry only the bits defined for them. An unknown or
reserved flag bit is `EINVAL` unless a specific field says otherwise. <a id="cite-fd.unknown-flag-bit-is-einval"></a>

The point of all this is that a future version can give a reserved
field meaning without an older kernel having silently accepted a value
it did not understand.

<a id="trm-5-5-1-5"></a>

## Strings

Strings in ioctl structures are **length-delimited, not
null-terminated**. Each is a `(len, ptr)` pair where `len` is a byte
count and `ptr` is a `u64` userspace address. LCS reads exactly `len`
bytes. <a id="cite-fd.string-is-a-len-ptr-pair"></a> A terminator is neither required nor expected, and one included
in the length is a null byte and therefore invalid.

Syscall paths are the exception: they arrive as null-terminated C
strings and have the terminator stripped before validation ([Names and Case](<~kernel/internals/lcs/data-model/names-and-case#trm-5-2-8>)).

<a id="trm-5-5-1-6"></a>

## Variable-size output buffers

Six ioctls return variable-size data — `REG_IOC_QUERY_VALUE`,
`QUERY_VALUES_BATCH`, `ENUM_VALUES`, `ENUM_SUBKEYS`, `QUERY_KEY_INFO`
and `GET_SECURITY` — and all six use one convention. <a id="cite-fd.six-ioctls-return-variable-size-data"></a>

For each output buffer described by `(length, pointer)`:

- **length 0 is a size probe**, whether the pointer is null or not. The
  pointer is not dereferenced. <a id="cite-fd.zero-length-is-a-size-probe"></a>
- **length greater than 0** requires a non-null pointer writable for
  that many bytes, or the ioctl returns `EFAULT`. <a id="cite-fd.non-zero-length-needs-a-writable-pointer"></a>

If any output buffer is too small the ioctl returns `ERANGE` and writes
**every required size it can determine**, not just the first one that
failed — so a caller with two undersized buffers learns both sizes from
one call. <a id="cite-fd.erange-writes-every-determinable-size"></a>

On `ERANGE`, output buffers are **not partially filled**; their
contents are unspecified. <a id="cite-fd.erange-leaves-buffers-unfilled"></a>

Output scalar metadata is meaningful only on
success, unless an ioctl explicitly documents a field as carrying a
required size or count on `ERANGE`. <a id="cite-fd.output-scalars-meaningful-only-on-success"></a>

Input pointer faults return `EFAULT`, validated before source dispatch
wherever that is possible. <a id="cite-fd.input-pointer-fault-is-efault"></a>

<a id="trm-5-b"></a>

[LCS ABI Reference](<~kernel/userspace/native/lcs/generated-syscall-and-common-abi#trm-5-a>) is generated from `include/uapi/pkm/lcs.h` and holds only what a
compiler can measure. This appendix holds the rest.

The split is structural rather than editorial. `gen-lcs-abi.py`
overwrites [LCS ABI Reference](<~kernel/userspace/native/lcs/generated-syscall-and-common-abi#trm-5-a>) wholesale on every run, so anything written there is
lost the next time the ABI changes.

<a id="trm-5-b-1"></a>

## What is not here

The header carries names, numbers and layouts. Everything else about the
interface is a property of the implementation rather than of the ABI, and
is documented with the operation it belongs to: the required access right
for each ioctl and the two-pass output buffer convention in [The Fd Model](<~kernel/userspace/native/lcs/file-descriptors-and-buffer-conventions#trm-5-5-1>), the
error vocabulary in [The Error Model](<~kernel/userspace/native/lcs/errors#trm-5-5-5>), the RSI payload shapes in the Registry Source
Interface specification, and the backup stream's record payloads in the
Registry Backup Format specification.

`REG_BACKUP_MAGIC` in [LCS ABI Reference](<~kernel/userspace/native/lcs/generated-syscall-and-common-abi#trm-5-a>) is the eight-byte header magic; <a id="cite-lcs-abi-notes.backup-magic-is-eight-byte-header"></a> the record
type codes are the framing, not the payloads.
