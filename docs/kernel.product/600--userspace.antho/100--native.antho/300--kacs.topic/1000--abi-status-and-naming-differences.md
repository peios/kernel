---
title: "ABI status and naming differences"
description: "ABI status and naming differences: behaviour and implementation of the Peios kernel."
type: reference
---

<a id="trm-3-d"></a>

[KACS ABI Reference](<~kernel/userspace/native/kacs/generated-syscall-index#trm-3-a>) is generated from `include/uapi/pkm/` and holds only what a compiler
can measure. This appendix holds the rest: the two ACE types that have
a constant and no behaviour, the payload shapes behind the token query
classes, the specification spellings a reader may arrive holding, what
is deliberately documented elsewhere, and the kernel configuration
KACS is built by.

The split is structural rather than editorial. `gen-kacs-abi.py`
overwrites [KACS ABI Reference](<~kernel/userspace/native/kacs/generated-syscall-index#trm-3-a>) wholesale on every run, so anything written there is
lost the next time the ABI changes — which is exactly what happened to
two sections of this one before they were moved here.

<a id="trm-3-d-4"></a>

## Names that differ from the specifications

This manual uses the names `include/uapi/pkm/` declares, and the generated
tables of [KACS ABI Reference](<~kernel/userspace/native/kacs/generated-syscall-index#trm-3-a>) are authoritative for them. A reader may instead arrive
holding the name PCDS uses, which is MS-DTYP's — a legitimate spelling,
not an obsolete one, and the one a third party implementing PCDS will
have. This table maps those onto the headers.

| PCDS / MS-DTYP | uapi name |
|---|---|
| `ACCESS_ALLOWED_ACE_TYPE`, `SYSTEM_AUDIT_ACE_TYPE`, ... | `KACS_ACE_TYPE_ACCESS_ALLOWED`, `KACS_ACE_TYPE_SYSTEM_AUDIT`, ... (the qualifier moves to the front) |
| `KACS_REAL_TOKEN` | `KACS_TOKEN_OPEN_REAL` |
| `KACS_LEVEL_*` | `KACS_IMLEVEL_*` |
| `KACS_FILE_SUPERSEDE`, `_OPEN`, ... | `KACS_DISPOSITION_*` |
| `OWNER_SECURITY_INFORMATION`, ... | `KACS_SECINFO_*` |
| `SE_PRIVILEGE_ENABLED` / `_REMOVED` | `KACS_PRIVILEGE_ATTR_ENABLED` / `_REMOVED` |
| `KACS_PRIV_RESET_ALL_DEFAULTS` | `KACS_PRIVILEGE_RESET_ALL_DEFAULTS` |
| `KACS_RESTRICT_WRITE_RESTRICTED` | `KACS_TOKEN_RESTRICT_WRITE_RESTRICTED` |
| `SE_GROUP_*` | `KACS_SID_GROUP_*` |
| `TOKEN_CLASS_*` | `KACS_TOKEN_CLASS_*` |

The PIP tiers have no public names at all. The Protected type (512)
and the `PeiosTcb` trust level (8192) exist only as kernel-private
constants, and nothing in `include/uapi/pkm/` defines None, Protected or
Isolated. <a id="cite-abi-notes.pip-tiers-kernel-private"></a> A program reasoning about tiers compares the numbers
([Process Integrity Protection](<~kernel/internals/kacs/executable-trust/process-integrity-protection#trm-3-7>)).

<a id="trm-3-d-6"></a>

## Open-interface documentation discrepancies

The comparison below records historical documentation differences. The
[pinned source findings](#pinned-source-findings) resolve specific creator-SD,
create-option and no-follow questions; they do **not** reconcile every group
below. No runtime behavior or historical release boundary was tested or
established. The generated ABI supplies layouts and constants; it does not
settle these behavioral questions.

Source labels and line numbers refer to the `learn` snapshot
`4b119864d7f51c569ae1ac1932e4430f06731cf2`:

- **O:** the former Security Fundamentals [Opening files source](https://github.com/peios/learn/blob/4b119864d7f51c569ae1ac1932e4430f06731cf2/peios.product/1--security-fundamentals.antho/200--access-control.shelf/500--file-access.topic/300--opening-files.md), retained in that revision's history.
- **N:** [KACS-Native Open](~kernel/internals/kacs/file-security/kacs-native-open#trm-3-9-2), TRM [KACS-Native Open](<~kernel/internals/kacs/file-security/kacs-native-open#trm-3-9-2>).
- **L:** [Legacy Open Compatibility](~kernel/internals/kacs/file-security/legacy-open-compatibility#trm-3-9-3), TRM [Legacy Open Compatibility](<~kernel/internals/kacs/file-security/legacy-open-compatibility#trm-3-9-3>).
- **D:** [Opening a file](https://learn.peios.org/peios/developing-for-peios/sdk-reference/sdk-files/opening-a-file), SDK reference.
- **G:** [Securing files](https://learn.peios.org/peios/developing-for-peios/sdk-access-control/securing-files), SDK guide.

The links reach the current references; the line numbers identify the
comparison snapshot above.

1. **Maximum allowed.** O:116–127 says `MAXIMUM_ALLOWED` returns the
   maximum mask without checking the other requested bits, which it calls
   hints; N:14–19 says the concrete data/execute bits must be granted.
   Both require a concrete bit and reject `MAXIMUM_ALLOWED` alone. The
   general [DACL walk](~kernel/internals/kacs/access-check/the-dacl-walk#trm-3-8-2-5)
   describes a separate AccessCheck layer and cannot settle open validity
   by analogy.

2. **Legacy masks.** O:135–145 maps `O_RDONLY` to
   `FILE_READ_DATA | FILE_READ_ATTRIBUTES | FILE_READ_EA | READ_CONTROL | SYNCHRONIZE`,
   `O_WRONLY` to
   `FILE_WRITE_DATA | FILE_WRITE_ATTRIBUTES | FILE_WRITE_EA | READ_CONTROL | SYNCHRONIZE`,
   and `O_RDWR` to their union. O:154–158 makes only `FILE_READ_DATA` core
   for read-only opens and allows `FILE_READ_ATTRIBUTES` to be dropped.
   L:16–37 instead makes `FILE_READ_ATTRIBUTES` core with read data, write
   data, or both according to the flag; L:39–49 lists broader compat rights.
   O:138 says `O_APPEND` adds `FILE_APPEND_DATA`; L:30–33 replaces core
   `FILE_WRITE_DATA` with it, then re-adds write data for `O_TRUNC`.
   L:44–45 also requests write data as optional compat access on append
   opens. These are different mappings, not interchangeable summaries.

3. **Creator descriptors.** O:96–97 groups open-existing branches under
   `EINVAL` and lists `SUPERSEDE` only for an absent target. N:133–144
   distinguishes `FILE_OPEN` (`EOPNOTSUPP`) from existing
   `FILE_OPEN_IF`, `FILE_OVERWRITE` and `FILE_OVERWRITE_IF` (`EINVAL`);
   N:82–89 also permits a caller-supplied SD on replacement by
   `FILE_SUPERSEDE`. D:36–46 and G:19–36 show `OPEN_IF` with a non-null
   creator SD and imply that the existing-file branch succeeds, despite
   O and N rejecting it. The SDK examples have now been changed to create-only.
   The pinned source findings below settle these existing-object rejections;
   this pass does not settle the separate `SUPERSEDE` comparison.

4. **Replacement and status.** O:71 says `SUPERSEDE` removes the inode
   and recommends it for atomic-replace patterns. N:82–89 replaces the
   pathname while preserving old hardlinks and already-open references.
   O:112 claims nonconditional dispositions predict the status; N:176–179
   says an absent-target `FILE_SUPERSEDE` reports `CREATED`, with
   `SUPERSEDED` only for actual replacement. No atomicity guarantee follows
   from this comparison.

5. **Delete-on-close.** O:80 describes deletion on the last fd referencing
   the file. N:112–129 instead specifies final close of one file-description
   lineage, preserved by `dup`, `fork` and `SCM_RIGHTS`; later opens fail
   closed, and only regular files are supported. Generic inode
   last-reference semantics and this no-share lineage boundary differ.

6. **Unverified raw details.** O:88 claims native `AT_EMPTY_PATH` opens
   an empty path against the directory referenced by `dirfd`; N:66–69
   discusses that flag for get/set-security, not native open. O:140–143
   maps `O_CREAT` to `OPEN_IF` with parent `FILE_ADD_FILE`,
   `O_CREAT | O_EXCL` to `CREATE`, and `O_NOFOLLOW` to
   `AT_SYMLINK_NOFOLLOW`. Their exact legacy translation and parent-right
   timing are not established by N/L/D. O:170 attributes legacy creation
   to umask-based defaults plus parent inheritable ACEs; [Inheritance](https://learn.peios.org/peios/security-fundamentals/security-descriptors/inheritance#the-merge-algorithm)
   describes parent, creator and token SD sources without establishing
   that umask contribution. O:183,185 also lists path-component
   `ENOTDIR` and invalid-disposition `EINVAL`. These remain earlier,
   unverified claims; omission from another reference does not prove
   rejection or support. O:180 distinguishes a failed open access check
   from an unreachable path component; [directory traversal](~kernel/internals/kacs/file-security/use-time-semantics#trm-3-9-4-3)
   is a separate authorization check.

7. **SDK destination caveats.** D:3 mentions share mode; D:28 describes
   no-follow, write-through and the rest of the `NtCreateFile` option set.
   N:111–120 instead lists two supported create-option bits, reserves all
   others, and says the ABI has no share-mode field. D:26 calls the native
   result a “granted subset,” while N:6–19 distinguishes strict requests
   from maximum-allowed requests. The SDK reference is a programming
   entry point, not evidence that every difference has been reconciled. The
   current SDK page no longer advertises share mode or unsupported create
   options; the pinned source below verifies the accepted option bits and
   their SDK field mapping. The granted-subset wording versus strict/maximum
   semantics remains part of the unresolved comparison.

<a id="trm-3-d-6-1"></a>

### Pinned source findings

A bounded source check used kernel
`8e0e22de3a59cad506bbbf8873de456e16ad272d` and libpeios 0.5.8
`de0018bdcaed14abb796aeccec9c8387fd30e452`. These are implementation findings
for those commits, not proof about a deployed kernel or the release where a
behavior began. Referenced KUnit tests are definitions; they were not executed.

- **Creator SDs (part of group 3).** [Argument validation](https://github.com/peios/pkm/blob/8e0e22de3a59cad506bbbf8873de456e16ad272d/kacs/native_open.c#L192-L202)
  rejects `OPEN` plus creator SD with `EOPNOTSUPP` and `OVERWRITE` plus creator
  SD with `EINVAL`. [Existing-path handling](https://github.com/peios/pkm/blob/8e0e22de3a59cad506bbbf8873de456e16ad272d/kacs/native_open.c#L1443-L1451)
  rejects `OPEN_IF` and `OVERWRITE_IF` plus creator SD with `EINVAL` when the
  object exists. The [OPEN_IF test](https://github.com/peios/pkm/blob/8e0e22de3a59cad506bbbf8873de456e16ad272d/kacs/kunit_file.c#L6020-L6053)
  records that expectation. [SDK marshalling](https://github.com/peios/libpeios/blob/de0018bdcaed14abb796aeccec9c8387fd30e452/src/file.rs#L131-L196)
  forwards the disposition and SD, rather than stripping the SD on an existing
  path. Use create-only with an explicit SD or open-existing with `NULL` SD;
  an `EEXIST` retry is a separate operation, not an atomic transaction.
- **Create options (part of group 7).** The [accepted-bit mask](https://github.com/peios/pkm/blob/8e0e22de3a59cad506bbbf8873de456e16ad272d/kacs/native_open.c#L165-L170)
  contains only `DIRECTORY` and `DELETE_ON_CLOSE`; unsupported bits return
  `EINVAL`. The same SDK marshalling copies `options` to `create_options` and
  `flags` to `flags`, so `AT_SYMLINK_NOFOLLOW` belongs in the latter.
- **No-follow is operation-specific.** [Native open](https://github.com/peios/pkm/blob/8e0e22de3a59cad506bbbf8873de456e16ad272d/kacs/native_open.c#L1334-L1349)
  rejects a terminal symlink with `ELOOP`. The by-path SD query instead selects
  the link itself through its [lookup flags](https://github.com/peios/pkm/blob/8e0e22de3a59cad506bbbf8873de456e16ad272d/kacs/sd_access.c#L312-L327)
  and [path resolver](https://github.com/peios/pkm/blob/8e0e22de3a59cad506bbbf8873de456e16ad272d/kacs/sd_access.c#L506-L536), as recorded by a
  [link-query test](https://github.com/peios/pkm/blob/8e0e22de3a59cad506bbbf8873de456e16ad272d/kacs/kunit_file.c#L7586-L7625).
  The [SDK query path](https://github.com/peios/libpeios/blob/de0018bdcaed14abb796aeccec9c8387fd30e452/src/file.rs#L220-L312) forwards the flags; its
  buffer-size adaptation does not impose a terminal-link rejection. This
  query finding does not verify a successful link-SD write or remove the
  set-security component and storage checks.

Groups 1, 2, 4, 5 and 6 remain unresolved by this check, as do the other
behavioral claims in groups 3 and 7. Do not treat the TRM, SDK or generated
ABI as a blanket resolution of those differences.

<a id="trm-3-d-7"></a>

## What is not here

Required rights, error codes and validation rules are properties of
the implementation rather than of the headers, so they are documented
with the operations themselves: token rights and the per-ioctl
requirements in [Token Access Rights](<~kernel/internals/kacs/tokens/token-access-rights#trm-3-2-8>), the file rights in [The Handle Model](<~kernel/internals/kacs/file-security/the-handle-model#trm-3-9-1>), the process rights
in [Process Security Descriptors](<~kernel/internals/kacs/process-security/process-security-descriptors#trm-3-3-3>), and the privileges in [Privilege Catalogue](<~kernel/internals/kacs/privileges/privilege-catalogue#trm-3-4-2>).

Two neighbouring ABIs are generated or documented separately.
`include/uapi/pkm/trace.h` is a versioned, append-only ABI of tracepoint
reason, operation and state codes intended for tooling.
`include/uapi/pkm/kmes.h` and `include/uapi/pkm/lcs.h` belong to their own chapters.
