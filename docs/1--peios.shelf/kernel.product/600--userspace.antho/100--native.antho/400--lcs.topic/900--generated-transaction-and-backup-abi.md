---
title: "Generated transaction and backup ABI"
description: "Generated transaction and backup ABI: behaviour and implementation of the Peios kernel."
type: reference
---

<a id="trm-5-a-3-15"></a>

## `struct reg_backup_args` <a id="cite-lcs-abi.struct-reg-backup-args"></a>

Total size 4 bytes.

| Offset | Size | Type | Field |
|---|---|---|---|
| 0 | 4 | `__s32` | `output_fd` |

<a id="trm-5-a-3-16"></a>

## `struct reg_restore_args` <a id="cite-lcs-abi.struct-reg-restore-args"></a>

Total size 4 bytes.

| Offset | Size | Type | Field |
|---|---|---|---|
| 0 | 4 | `__s32` | `input_fd` |

<a id="trm-5-a-3-17"></a>

## `struct reg_txn_status_args` <a id="cite-lcs-abi.struct-reg-txn-status-args"></a>

Total size 8 bytes.

| Offset | Size | Type | Field |
|---|---|---|---|
| 0 | 4 | `__u32` | `state` |
| 4 | 4 | `__s32` | `terminal_errno` |
