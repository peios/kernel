---
title: "Generated file and mount ABI"
description: "Generated file and mount ABI: behaviour and implementation of the Peios kernel."
type: reference
---

<a id="trm-3-a-2-16"></a>

## `struct kacs_open_how` <a id="cite-kacs-abi.struct-kacs-open-how"></a>

Total size 56 bytes.

| Offset | Size | Type | Field |
|---:|---:|---|---|
| 0 | 4 | `__u32` | `desired_access` |
| 4 | 4 | `__u32` | `create_disposition` |
| 8 | 4 | `__u32` | `create_options` |
| 12 | 4 | `__u32` | `flags` |
| 16 | 8 | `__u64` | `sd_ptr` |
| 24 | 4 | `__u32` | `sd_len` |
| 28 | 4 | `__u32` | `share_access` |
| 32 | 16 | `__u8``[16]` | `lease_key` |
| 48 | 4 | `__s32` | `lease_fd` |
| 52 | 4 | `__u32` | `__pad2` |

<a id="trm-3-a-2-17"></a>

## `struct kacs_open_info` <a id="cite-kacs-abi.struct-kacs-open-info"></a>

Total size 16 bytes.

| Offset | Size | Type | Field |
|---:|---:|---|---|
| 0 | 4 | `__u32` | `granted_access` |
| 4 | 4 | `__u32` | `share_access` |
| 8 | 4 | `__u32` | `flags` |
| 12 | 4 | `__u32` | `__pad` |

<a id="trm-3-a-2-18"></a>

## `struct kacs_lock_args` <a id="cite-kacs-abi.struct-kacs-lock-args"></a>

Total size 32 bytes.

| Offset | Size | Type | Field |
|---:|---:|---|---|
| 0 | 8 | `__u64` | `offset` |
| 8 | 8 | `__u64` | `length` |
| 16 | 4 | `__u32` | `op` |
| 20 | 4 | `__u32` | `flags` |
| 24 | 8 | `__u64` | `cookie` |

<a id="trm-3-a-2-19"></a>

## `struct kacs_lease_args` <a id="cite-kacs-abi.struct-kacs-lease-args"></a>

Total size 32 bytes.

| Offset | Size | Type | Field |
|---:|---:|---|---|
| 0 | 16 | `__u8``[16]` | `lease_key` |
| 16 | 4 | `__u32` | `state` |
| 20 | 4 | `__u32` | `flags` |
| 24 | 8 | `__u64` | `__pad` |

<a id="trm-3-a-2-20"></a>

## `struct kacs_lease_break` <a id="cite-kacs-abi.struct-kacs-lease-break"></a>

Total size 48 bytes.

| Offset | Size | Type | Field |
|---:|---:|---|---|
| 0 | 16 | `__u8``[16]` | `lease_key` |
| 16 | 8 | `__u64` | `dev` |
| 24 | 8 | `__u64` | `ino` |
| 32 | 4 | `__u32` | `current_state` |
| 36 | 4 | `__u32` | `new_state` |
| 40 | 4 | `__u32` | `reason` |
| 44 | 4 | `__u32` | `epoch` |

<a id="trm-3-a-2-21"></a>

## `struct kacs_mount_policy_args` <a id="cite-kacs-abi.struct-kacs-mount-policy-args"></a>

Total size 32 bytes.

| Offset | Size | Type | Field |
|---:|---:|---|---|
| 0 | 4 | `__u32` | `policy` |
| 4 | 4 | `__u32` | `flags` |
| 8 | 4 | `__u32` | `generation` |
| 12 | 4 | `__u32` | `__pad0` |
| 16 | 8 | `__u64` | `template_sd_ptr` |
| 24 | 4 | `__u32` | `template_sd_len` |
| 28 | 4 | `__u32` | `__pad1` |

<a id="trm-3-a-2-22"></a>

## `struct kacs_sattr` <a id="cite-kacs-abi.struct-kacs-sattr"></a>

Total size 32 bytes.

| Offset | Size | Type | Field |
|---:|---:|---|---|
| 0 | 4 | `__u32` | `version` |
| 4 | 4 | `__u32` | `valid` |
| 8 | 4 | `__u32` | `attributes` |
| 12 | 4 | `__u32` | `flags` |
| 16 | 8 | `__s64` | `created_at_sec` |
| 24 | 4 | `__u32` | `created_at_nsec` |
| 28 | 4 | `__u32` | `__pad` |

<a id="trm-3-a-6"></a>

## mntns.h

From `uapi/pkm/mntns.h`.

*KACS access rights for mount namespaces.* <a id="cite-kacs-abi.mntns-access-rights"></a>

| Constant | Value | Notes |
|---|---|---|
| `KACS_MNTNS_MOUNT` | `0x00000001` (1) | change the mount table |
| `KACS_MNTNS_ENTER` | `0x00000002` (2) | join the namespace with setns(2) |
| `KACS_MNTNS_ALL_ACCESS` | `917507` |  |

<a id="trm-3-a-8"></a>

## File and open constants

From `uapi/pkm/file.h`.

*The value of the special-attributes extended attribute, as read and as written.* <a id="cite-kacs-abi.sattr-xattr-name"></a>

valid names the fields a write changes; a read sets every bit. Other
fields a write does not name are ignored, and __pad must be zero.

| Constant | Value |
|---|---|
| `KACS_SATTR_XATTR_NAME` | `109012802569580` |

*Minimum caller-supplied size accepted for each argument block.* <a id="cite-kacs-abi.arg-block-min-sizes"></a>

| Constant | Value |
|---|---|
| `KACS_OPEN_HOW_MIN_SIZE` | `16` |
| `KACS_MOUNT_POLICY_ARGS_MIN_SIZE` | `16` |
| `KACS_OPEN_INFO_MIN_SIZE` | `4` |
| `KACS_LOCK_ARGS_MIN_SIZE` | `24` |
| `KACS_LEASE_ARGS_MIN_SIZE` | `24` |

*Sizes of each published version of kacs_open_how.* <a id="cite-kacs-abi.open-how-sizes"></a>

| Constant | Value |
|---|---|
| `KACS_OPEN_HOW_SIZE_VER0` | `32` |
| `KACS_OPEN_HOW_SIZE_VER1` | `56` |

*Create dispositions (kacs_open_how.create_disposition).* <a id="cite-kacs-abi.create-dispositions"></a>

| Constant | Value |
|---|---|
| `KACS_DISPOSITION_SUPERSEDE` | `0` |
| `KACS_DISPOSITION_OPEN` | `1` |
| `KACS_DISPOSITION_CREATE` | `2` |
| `KACS_DISPOSITION_OPEN_IF` | `3` |
| `KACS_DISPOSITION_OVERWRITE` | `4` |
| `KACS_DISPOSITION_OVERWRITE_IF` | `5` |

*Create options (kacs_open_how.create_options).* <a id="cite-kacs-abi.create-options"></a>

| Constant | Value |
|---|---|
| `KACS_CREATE_OPT_DIRECTORY` | `0x0001` (1) |
| `KACS_CREATE_OPT_DELETE_ON_CLOSE` | `0x0002` (2) |

*kacs_open_how.flags bits.* <a id="cite-kacs-abi.open-how-flags"></a>

| Constant | Value |
|---|---|
| `KACS_BACKUP_INTENT` | `0x00000001` (1) |
| `KACS_RESTORE_INTENT` | `0x00000002` (2) |
| `KACS_OPEN_SHARE_ACCESS` | `0x00000004` (4) |
| `KACS_OPEN_LEASE_KEY` | `0x00000008` (8) |
| `KACS_OPEN_PIN_ANCESTORS` | `0x00000010` (16) |

*Share access (kacs_open_how.share_access, kacs_open_info.share_access).* <a id="cite-kacs-abi.share-access"></a>

| Constant | Value |
|---|---|
| `KACS_FILE_SHARE_READ` | `0x00000001` (1) |
| `KACS_FILE_SHARE_WRITE` | `0x00000002` (2) |
| `KACS_FILE_SHARE_DELETE` | `0x00000004` (4) |

*kacs_open_info.flags bits.* <a id="cite-kacs-abi.open-info-flags"></a>

| Constant | Value |
|---|---|
| `KACS_OPEN_INFO_MANAGED` | `0x00000001` (1) |
| `KACS_OPEN_INFO_DELETE_PENDING` | `0x00000002` (2) |
| `KACS_OPEN_INFO_DELETE_ON_CLOSE` | `0x00000004` (4) |
| `KACS_OPEN_INFO_ANCESTORS_PINNED` | `0x00000008` (8) |

*kacs_set_disposition flags, as FILE_DISPOSITION_INFORMATION_EX.* <a id="cite-kacs-abi.disposition-flags"></a>

| Constant | Value |
|---|---|
| `KACS_DISPOSITION_DELETE` | `0x00000001` (1) |
| `KACS_DISPOSITION_POSIX_SEMANTICS` | `0x00000002` (2) |
| `KACS_DISPOSITION_ON_CLOSE` | `0x00000008` (8) |
| `KACS_DISPOSITION_IGNORE_READONLY` | `0x00000010` (16) |

*kacs_rename flags, as FILE_RENAME_INFORMATION_EX.* <a id="cite-kacs-abi.rename-flags"></a>

| Constant | Value |
|---|---|
| `KACS_RENAME_REPLACE_IF_EXISTS` | `0x00000001` (1) |
| `KACS_RENAME_POSIX_SEMANTICS` | `0x00000002` (2) |
| `KACS_RENAME_IGNORE_READONLY` | `0x00000040` (64) |

*kacs_lock_args.op values.* <a id="cite-kacs-abi.lock-ops"></a>

| Constant | Value |
|---|---|
| `KACS_LOCK_SHARED` | `1` |
| `KACS_LOCK_EXCLUSIVE` | `2` |
| `KACS_LOCK_UNLOCK` | `3` |
| `KACS_LOCK_CANCEL` | `4` |

*kacs_lock_args.flags bits.* <a id="cite-kacs-abi.lock-flags"></a>

| Constant | Value |
|---|---|
| `KACS_LOCK_FAIL_IMMEDIATELY` | `0x00000001` (1) |

*Lease states: the NT caching bits.* <a id="cite-kacs-abi.lease-states"></a>

| Constant | Value |
|---|---|
| `KACS_LEASE_READ` | `0x00000001` (1) |
| `KACS_LEASE_HANDLE` | `0x00000002` (2) |
| `KACS_LEASE_WRITE` | `0x00000004` (4) |

*kacs_lease_args.flags bits.* <a id="cite-kacs-abi.lease-flags"></a>

| Constant | Value |
|---|---|
| `KACS_LEASE_ACKNOWLEDGE` | `0x00000001` (1) |

*kacs_lease_break.reason values: the operation that broke the lease.* <a id="cite-kacs-abi.lease-break-reasons"></a>

| Constant | Value |
|---|---|
| `KACS_LEASE_BREAK_OPEN` | `1` |
| `KACS_LEASE_BREAK_SHARING` | `2` |
| `KACS_LEASE_BREAK_WRITE` | `3` |
| `KACS_LEASE_BREAK_SIZE` | `4` |
| `KACS_LEASE_BREAK_LOCK` | `5` |
| `KACS_LEASE_BREAK_NAMESPACE` | `6` |
| `KACS_LEASE_BREAK_DELETE` | `7` |
| `KACS_LEASE_BREAK_SECURITY` | `8` |
| `KACS_LEASE_BREAK_ATTRIBUTES` | `9` |
| `KACS_LEASE_BREAK_CHILD` | `10` |
| `KACS_LEASE_BREAK_TIMEOUT` | `11` |

*kacs_create_lease_manager flags.* <a id="cite-kacs-abi.lease-manager-flags"></a>

| Constant | Value |
|---|---|
| `KACS_LEASE_MANAGER_CLOEXEC` | `0x00000001` (1) |
| `KACS_LEASE_MANAGER_NONBLOCK` | `0x00000002` (2) |

*Break timeout applied when kacs_create_lease_manager is given zero.* <a id="cite-kacs-abi.lease-default-timeout"></a>

| Constant | Value |
|---|---|
| `KACS_LEASE_DEFAULT_BREAK_TIMEOUT_MS` | `35000` |

*kacs_sattr.version.* <a id="cite-kacs-abi.sattr-version"></a>

| Constant | Value |
|---|---|
| `KACS_SATTR_VERSION` | `1` |

*kacs_sattr.valid bits.* <a id="cite-kacs-abi.sattr-valid-bits"></a>

| Constant | Value |
|---|---|
| `KACS_SATTR_VALID_ATTRIBUTES` | `0x00000001` (1) |
| `KACS_SATTR_VALID_CREATED_AT` | `0x00000002` (2) |

*kacs_sattr.attributes bits.* <a id="cite-kacs-abi.sattr-attribute-bits"></a>

| Constant | Value |
|---|---|
| `KACS_SATTR_READONLY` | `0x00000001` (1) |

*kacs_sattr.flags bits.* <a id="cite-kacs-abi.sattr-flags"></a>

On a read, CREATED_AT_SET says Created At was set explicitly rather than
taken from the birth time. On a write naming
KACS_SATTR_VALID_CREATED_AT, CREATED_AT_CLEAR unsets it.

| Constant | Value |
|---|---|
| `KACS_SATTR_CREATED_AT_SET` | `0x00000001` (1) |
| `KACS_SATTR_CREATED_AT_CLEAR` | `0x00000002` (2) |

*File and directory object-specific access rights (the low 16 bits of a file access mask).* <a id="cite-kacs-abi.file-access-rights"></a>

The directory aliases name the same bit as the file right it acts as for
a directory object.

| Constant | Value |
|---|---|
| `KACS_FILE_READ_DATA` | `0x00000001` (1) |
| `KACS_FILE_WRITE_DATA` | `0x00000002` (2) |
| `KACS_FILE_APPEND_DATA` | `0x00000004` (4) |
| `KACS_FILE_READ_EA` | `0x00000008` (8) |
| `KACS_FILE_WRITE_EA` | `0x00000010` (16) |
| `KACS_FILE_EXECUTE` | `0x00000020` (32) |
| `KACS_FILE_DELETE_CHILD` | `0x00000040` (64) |
| `KACS_FILE_READ_ATTRIBUTES` | `0x00000080` (128) |
| `KACS_FILE_WRITE_ATTRIBUTES` | `0x00000100` (256) |
| `KACS_FILE_LIST_DIRECTORY` | `1` |
| `KACS_FILE_TRAVERSE` | `32` |
| `KACS_FILE_ADD_FILE` | `2` |
| `KACS_FILE_ADD_SUBDIRECTORY` | `4` |

*Mount-policy values (kacs_mount_policy_args.policy).* <a id="cite-kacs-abi.mount-policy-values"></a>

| Constant | Value |
|---|---|
| `KACS_MOUNT_POLICY_UNMANAGED` | `1` |
| `KACS_MOUNT_POLICY_DENY_MISSING` | `2` |
| `KACS_MOUNT_POLICY_SYNTHESIZE_EPHEMERAL` | `3` |
| `KACS_MOUNT_POLICY_SYNTHESIZE_PERSISTENT` | `4` |

*Status word kacs_open writes back, describing what happened to the file.* <a id="cite-kacs-abi.open-status-values"></a>

| Constant | Value |
|---|---|
| `KACS_STATUS_OPENED` | `1` |
| `KACS_STATUS_CREATED` | `2` |
| `KACS_STATUS_OVERWRITTEN` | `3` |
| `KACS_STATUS_SUPERSEDED` | `4` |

Status word kacs_open writes back when it fails, naming the NT condition
behind the errno where one errno covers several. <a id="cite-kacs-abi.open-failure-status-values"></a>

| Constant | Value |
|---|---|
| `KACS_STATUS_SHARING_VIOLATION` | `0x10` (16) |
| `KACS_STATUS_DELETE_PENDING` | `0x11` (17) |
| `KACS_STATUS_CANNOT_DELETE` | `0x12` (18) |
