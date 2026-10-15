---
title: "Generated key and security ABI"
description: "Generated key and security ABI: behaviour and implementation of the Peios kernel."
type: reference
---

<a id="trm-5-a-3-1"></a>

## `struct reg_create_key_args` <a id="cite-lcs-abi.struct-reg-create-key-args"></a>

Total size 48 bytes.

| Offset | Size | Type | Field |
|---|---|---|---|
| 0 | 4 | `__s32` | `parent_fd` |
| 4 | 4 | `__u32` | `_pad0` |
| 8 | 8 | `__u64` | `path_ptr` |
| 16 | 4 | `__u32` | `desired_access` |
| 20 | 4 | `__u32` | `flags` |
| 24 | 8 | `__u64` | `layer_ptr` |
| 32 | 4 | `__s32` | `txn_fd` |
| 36 | 4 | `__u32` | `_pad1` |
| 40 | 8 | `__u64` | `disposition_ptr` |

<a id="trm-5-a-3-2"></a>

## `struct reg_query_value_args` <a id="cite-lcs-abi.struct-reg-query-value-args"></a>

Total size 64 bytes.

| Offset | Size | Type | Field |
|---|---|---|---|
| 0 | 4 | `__u32` | `name_len` |
| 4 | 4 | `__u32` | `_pad0` |
| 8 | 8 | `__u64` | `name_ptr` |
| 16 | 4 | `__u32` | `type` |
| 20 | 4 | `__u32` | `data_len` |
| 24 | 4 | `__s32` | `txn_fd` |
| 28 | 4 | `__u32` | `layer_buf_len` |
| 32 | 8 | `__u64` | `data_ptr` |
| 40 | 8 | `__u64` | `sequence` |
| 48 | 4 | `__u32` | `layer_len` |
| 52 | 4 | `__u32` | `_pad1` |
| 56 | 8 | `__u64` | `layer_ptr` |

<a id="trm-5-a-3-3"></a>

## `struct reg_set_value_args` <a id="cite-lcs-abi.struct-reg-set-value-args"></a>

Total size 64 bytes.

| Offset | Size | Type | Field |
|---|---|---|---|
| 0 | 4 | `__u32` | `name_len` |
| 4 | 4 | `__u32` | `_pad0` |
| 8 | 8 | `__u64` | `name_ptr` |
| 16 | 4 | `__u32` | `type` |
| 20 | 4 | `__u32` | `data_len` |
| 24 | 8 | `__u64` | `data_ptr` |
| 32 | 4 | `__u32` | `layer_len` |
| 36 | 4 | `__u32` | `_pad1` |
| 40 | 8 | `__u64` | `layer_ptr` |
| 48 | 4 | `__s32` | `txn_fd` |
| 52 | 4 | `__u32` | `_pad2` |
| 56 | 8 | `__u64` | `expected_seq` |

<a id="trm-5-a-3-4"></a>

## `struct reg_delete_value_args` <a id="cite-lcs-abi.struct-reg-delete-value-args"></a>

Total size 40 bytes.

| Offset | Size | Type | Field |
|---|---|---|---|
| 0 | 4 | `__u32` | `name_len` |
| 4 | 4 | `__u32` | `_pad0` |
| 8 | 8 | `__u64` | `name_ptr` |
| 16 | 4 | `__u32` | `layer_len` |
| 20 | 4 | `__u32` | `_pad1` |
| 24 | 8 | `__u64` | `layer_ptr` |
| 32 | 4 | `__s32` | `txn_fd` |
| 36 | 4 | `__u32` | `_pad2` |

<a id="trm-5-a-3-5"></a>

## `struct reg_blanket_tombstone_args` <a id="cite-lcs-abi.struct-reg-blanket-tombstone-args"></a>

Total size 24 bytes.

| Offset | Size | Type | Field |
|---|---|---|---|
| 0 | 4 | `__u32` | `layer_len` |
| 4 | 4 | `__u32` | `_pad0` |
| 8 | 8 | `__u64` | `layer_ptr` |
| 16 | 1 | `__u8` | `set` |
| 17 | 3 | `__u8``[3]` | `_pad1` |
| 20 | 4 | `__s32` | `txn_fd` |

<a id="trm-5-a-3-6"></a>

## `struct reg_query_values_batch_args` <a id="cite-lcs-abi.struct-reg-query-values-batch-args"></a>

Total size 24 bytes.

| Offset | Size | Type | Field |
|---|---|---|---|
| 0 | 4 | `__u32` | `buf_len` |
| 4 | 4 | `__u32` | `count` |
| 8 | 8 | `__u64` | `buf_ptr` |
| 16 | 4 | `__s32` | `txn_fd` |
| 20 | 4 | `__u32` | `_pad` |

<a id="trm-5-a-3-7"></a>

## `struct reg_enum_value_args` <a id="cite-lcs-abi.struct-reg-enum-value-args"></a>

Total size 40 bytes.

| Offset | Size | Type | Field |
|---|---|---|---|
| 0 | 4 | `__u32` | `index` |
| 4 | 4 | `__u32` | `name_len` |
| 8 | 8 | `__u64` | `name_ptr` |
| 16 | 4 | `__u32` | `type` |
| 20 | 4 | `__u32` | `data_len` |
| 24 | 8 | `__u64` | `data_ptr` |
| 32 | 4 | `__s32` | `txn_fd` |
| 36 | 4 | `__u32` | `_pad` |

<a id="trm-5-a-3-8"></a>

## `struct reg_enum_subkey_args` <a id="cite-lcs-abi.struct-reg-enum-subkey-args"></a>

Total size 40 bytes.

| Offset | Size | Type | Field |
|---|---|---|---|
| 0 | 4 | `__u32` | `index` |
| 4 | 4 | `__u32` | `name_len` |
| 8 | 8 | `__u64` | `name_ptr` |
| 16 | 8 | `__u64` | `last_write_time` |
| 24 | 4 | `__u32` | `subkey_count` |
| 28 | 4 | `__u32` | `value_count` |
| 32 | 4 | `__s32` | `txn_fd` |
| 36 | 4 | `__u32` | `_pad` |

<a id="trm-5-a-3-9"></a>

## `struct reg_query_key_info_args` <a id="cite-lcs-abi.struct-reg-query-key-info-args"></a>

Total size 64 bytes.

| Offset | Size | Type | Field |
|---|---|---|---|
| 0 | 4 | `__u32` | `name_len` |
| 4 | 4 | `__u32` | `_pad0` |
| 8 | 8 | `__u64` | `name_ptr` |
| 16 | 8 | `__u64` | `last_write_time` |
| 24 | 4 | `__u32` | `subkey_count` |
| 28 | 4 | `__u32` | `value_count` |
| 32 | 4 | `__u32` | `max_subkey_name_len` |
| 36 | 4 | `__u32` | `max_value_name_len` |
| 40 | 4 | `__u32` | `max_value_data_size` |
| 44 | 4 | `__u32` | `sd_size` |
| 48 | 1 | `__u8` | `volatile_key` |
| 49 | 1 | `__u8` | `symlink` |
| 50 | 6 | `__u8``[6]` | `_pad1` |
| 56 | 8 | `__u64` | `hive_generation` |

<a id="trm-5-a-3-10"></a>

## `struct reg_delete_key_args` <a id="cite-lcs-abi.struct-reg-delete-key-args"></a>

Total size 24 bytes.

| Offset | Size | Type | Field |
|---|---|---|---|
| 0 | 4 | `__u32` | `layer_len` |
| 4 | 4 | `__u32` | `_pad0` |
| 8 | 8 | `__u64` | `layer_ptr` |
| 16 | 4 | `__s32` | `txn_fd` |
| 20 | 4 | `__u32` | `_pad1` |

<a id="trm-5-a-3-11"></a>

## `struct reg_hide_key_args` <a id="cite-lcs-abi.struct-reg-hide-key-args"></a>

Total size 24 bytes.

| Offset | Size | Type | Field |
|---|---|---|---|
| 0 | 4 | `__u32` | `layer_len` |
| 4 | 4 | `__u32` | `_pad0` |
| 8 | 8 | `__u64` | `layer_ptr` |
| 16 | 4 | `__s32` | `txn_fd` |
| 20 | 4 | `__u32` | `_pad1` |

<a id="trm-5-a-3-12"></a>

## `struct reg_get_security_args` <a id="cite-lcs-abi.struct-reg-get-security-args"></a>

Total size 16 bytes.

| Offset | Size | Type | Field |
|---|---|---|---|
| 0 | 4 | `__u32` | `security_info` |
| 4 | 4 | `__u32` | `sd_len` |
| 8 | 8 | `__u64` | `sd_ptr` |

<a id="trm-5-a-3-13"></a>

## `struct reg_set_security_args` <a id="cite-lcs-abi.struct-reg-set-security-args"></a>

Total size 24 bytes.

| Offset | Size | Type | Field |
|---|---|---|---|
| 0 | 4 | `__u32` | `security_info` |
| 4 | 4 | `__u32` | `sd_len` |
| 8 | 8 | `__u64` | `sd_ptr` |
| 16 | 4 | `__s32` | `txn_fd` |
| 20 | 4 | `__u32` | `_pad` |
