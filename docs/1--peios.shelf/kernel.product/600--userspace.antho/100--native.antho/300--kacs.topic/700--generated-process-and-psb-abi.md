---
title: "Generated process and PSB ABI"
description: "Generated process and PSB ABI: behaviour and implementation of the Peios kernel."
type: reference
---

<a id="trm-3-a-9"></a>

## Process access rights

From `uapi/pkm/process.h`.

*KACS process object-specific access rights (the low 16 bits of a process access mask).* <a id="cite-kacs-abi.process-access-rights"></a>

Named for the Windows process rights; an access check folds the generic
bits (<pkm/sd.h>) into these via the process generic mapping.

| Constant | Value |
|---|---|
| `KACS_PROCESS_TERMINATE` | `0x00000001` (1) |
| `KACS_PROCESS_SIGNAL` | `0x00000002` (2) |
| `KACS_PROCESS_VM_READ` | `0x00000010` (16) |
| `KACS_PROCESS_VM_WRITE` | `0x00000020` (32) |
| `KACS_PROCESS_DUP_HANDLE` | `0x00000040` (64) |
| `KACS_PROCESS_SET_INFORMATION` | `0x00000200` (512) |
| `KACS_PROCESS_QUERY_INFORMATION` | `0x00000400` (1024) |
| `KACS_PROCESS_SUSPEND_RESUME` | `0x00000800` (2048) |
| `KACS_PROCESS_QUERY_LIMITED` | `0x00001000` (4096) |

<a id="trm-3-a-10"></a>

## Process mitigation bits

From `uapi/pkm/psb.h`.

*Process Security Block (PSB) process-mitigation bits.* <a id="cite-kacs-abi.mitigation-bits"></a>

The `mitigations` argument of kacs_set_psb (SYS_KACS_SET_PSB) is a
bitmask of these flags. Setting a bit is activation-backed: KACS either
places the target process in the protected state (or verifies it already
satisfies the invariant) before committing, and rejects later operations
that would disable the protection. Each mitigation is enforced at its
own enforcement point and persists across exec. See Kernel TRM section
3.3 (Process Security Block). Only the bits in KACS_MIT_ALL are valid;
any other bit set in the request is rejected. KACS_MIT_CFI is a legacy
alias: requesting it sets both KACS_MIT_CFIF and KACS_MIT_CFIB, and the
alias bit itself is not retained.

| Constant | Value | Notes |
|---|---|---|
| `KACS_MIT_WXP` | `0x001` (1) | Write-XOR-Execute protection |
| `KACS_MIT_TLP` | `0x002` (2) | Trusted Library Paths |
| `KACS_MIT_LSV` | `0x004` (4) | Library Signature Verification |
| `KACS_MIT_CFI` | `0x008` (8) | legacy alias: CFIF \| CFIB |
| `KACS_MIT_UI_ACCESS` | `0x010` (16) | UI interaction (reserved) |
| `KACS_MIT_NO_CHILD` | `0x020` (32) | cannot fork (one-way) |
| `KACS_MIT_CFIF` | `0x040` (64) | forward-edge CFI (Intel IBT) |
| `KACS_MIT_CFIB` | `0x080` (128) | backward-edge CFI (shadow stack) |
| `KACS_MIT_PIE` | `0x100` (256) | reject non-PIE binaries at exec |
| `KACS_MIT_SML` | `0x200` (512) | speculation mitigation lock |

*All valid mitigation bits OR'd together — the accepted-request mask.* <a id="cite-kacs-abi.mitigation-all-mask"></a>

| Constant | Value |
|---|---|
| `KACS_MIT_ALL` | `0x3FF` (1023) |
