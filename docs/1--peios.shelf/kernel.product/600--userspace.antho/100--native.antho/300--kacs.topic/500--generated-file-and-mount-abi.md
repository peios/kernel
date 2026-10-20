---
title: "Generated file and mount ABI"
description: "Generated file and mount ABI: behaviour and implementation of the Peios kernel."
type: reference
---

<a id="trm-3-a-2-14"></a>

## `struct kacs_open_how` <a id="cite-kacs-abi.struct-kacs-open-how"></a>

Total size 32 bytes.

| Offset | Size | Type | Field |
|---:|---:|---|---|
| 0 | 4 | `__u32` | `desired_access` |
| 4 | 4 | `__u32` | `create_disposition` |
| 8 | 4 | `__u32` | `create_options` |
| 12 | 4 | `__u32` | `flags` |
| 16 | 8 | `__u64` | `sd_ptr` |
| 24 | 4 | `__u32` | `sd_len` |
| 28 | 4 | `__u32` | `__pad` |

<a id="trm-3-a-2-15"></a>

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

*Minimum caller-supplied size accepted for each argument block.* <a id="cite-kacs-abi.arg-block-min-sizes"></a>

| Constant | Value |
|---|---|
| `KACS_OPEN_HOW_MIN_SIZE` | `16` |
| `KACS_MOUNT_POLICY_ARGS_MIN_SIZE` | `16` |

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
