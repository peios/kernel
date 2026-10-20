---
title: "Generated access-check and descriptor ABI"
description: "Generated access-check and descriptor ABI: behaviour and implementation of the Peios kernel."
type: reference
---

<a id="trm-3-a-2-11"></a>

## `struct kacs_access_check_args` <a id="cite-kacs-abi.struct-kacs-access-check-args"></a>

Total size 136 bytes.

| Offset | Size | Type | Field |
|---:|---:|---|---|
| 0 | 4 | `__u32` | `caller_size` |
| 4 | 4 | `__s32` | `token_fd` |
| 8 | 8 | `__u64` | `sd_ptr` |
| 16 | 4 | `__u32` | `sd_len` |
| 20 | 4 | `__u32` | `desired_access` |
| 24 | 4 | `__u32` | `mapping_read` |
| 28 | 4 | `__u32` | `mapping_write` |
| 32 | 4 | `__u32` | `mapping_execute` |
| 36 | 4 | `__u32` | `mapping_all` |
| 40 | 8 | `__u64` | `self_sid_ptr` |
| 48 | 4 | `__u32` | `self_sid_len` |
| 52 | 4 | `__u32` | `privilege_intent` |
| 56 | 8 | `__u64` | `object_tree_ptr` |
| 64 | 4 | `__u32` | `object_tree_count` |
| 68 | 4 | `__u32` | `_pad0` |
| 72 | 8 | `__u64` | `local_claims_ptr` |
| 80 | 4 | `__u32` | `local_claims_len` |
| 84 | 4 | `__u32` | `_pad1` |
| 88 | 8 | `__u64` | `granted_out_ptr` |
| 96 | 4 | `__u32` | `pip_type` |
| 100 | 4 | `__u32` | `pip_trust` |
| 104 | 8 | `__u64` | `audit_context_ptr` |
| 112 | 4 | `__u32` | `audit_context_len` |
| 116 | 4 | `__u32` | `_pad2` |
| 120 | 8 | `__u64` | `continuous_audit_out_ptr` |
| 128 | 8 | `__u64` | `staging_mismatch_out_ptr` |

<a id="trm-3-a-2-12"></a>

## `struct kacs_object_type_entry` <a id="cite-kacs-abi.struct-kacs-object-type-entry"></a>

Total size 20 bytes.

| Offset | Size | Type | Field |
|---:|---:|---|---|
| 0 | 2 | `__u16` | `level` |
| 2 | 2 | `__u16` | `_reserved` |
| 4 | 16 | `__u8``[16]` | `guid` |

<a id="trm-3-a-2-13"></a>

## `struct kacs_node_result` <a id="cite-kacs-abi.struct-kacs-node-result"></a>

Total size 8 bytes.

| Offset | Size | Type | Field |
|---:|---:|---|---|
| 0 | 4 | `__u32` | `granted` |
| 4 | 4 | `__s32` | `status` |

<a id="trm-3-a-2-16"></a>

## `struct kacs_generic_mapping` <a id="cite-kacs-abi.struct-kacs-generic-mapping"></a>

Total size 16 bytes.

| Offset | Size | Type | Field |
|---:|---:|---|---|
| 0 | 4 | `__u32` | `read` |
| 4 | 4 | `__u32` | `write` |
| 8 | 4 | `__u32` | `execute` |
| 12 | 4 | `__u32` | `all` |

<a id="trm-3-a-7"></a>

## AccessCheck constants

From `uapi/pkm/access.h`.

*Full size of kacs_access_check_args the current kernel copies.* <a id="cite-kacs-abi.access-check-args-size"></a>

| Constant | Value |
|---|---|
| `KACS_ACCESS_CHECK_ARGS_SIZE` | `136` |

*Minimum caller_size the kernel accepts (the v1 / v0.20 layout).* <a id="cite-kacs-abi.access-check-args-v1-size"></a>

| Constant | Value |
|---|---|
| `KACS_ACCESS_CHECK_ARGS_V1_SIZE` | `40` |

*Byte size of one kacs_object_type_entry in the object-type tree array.* <a id="cite-kacs-abi.object-type-entry-size"></a>

| Constant | Value |
|---|---|
| `KACS_OBJECT_TYPE_ENTRY_SIZE` | `20` |

*Largest object-audit-context buffer the kernel accepts.* <a id="cite-kacs-abi.max-audit-context-len"></a>

| Constant | Value |
|---|---|
| `KACS_ACCESS_CHECK_MAX_AUDIT_CONTEXT_LEN` | `4096` |

*Largest @Local claims blob the kernel accepts (local_claims_ptr).* <a id="cite-kacs-abi.max-local-claims-len"></a>

| Constant | Value |
|---|---|
| `KACS_ACCESS_CHECK_MAX_LOCAL_CLAIMS_LEN` | `65536` |

*Largest object-type tree entry count the kernel accepts.* <a id="cite-kacs-abi.max-object-type-count"></a>

| Constant | Value |
|---|---|
| `KACS_ACCESS_CHECK_MAX_OBJECT_TYPE_COUNT` | `1024` |

Claim value types — the discriminant of one attribute in the @Local
claims array (local_claims_ptr). <a id="cite-kacs-abi.claim-value-types"></a>

| Constant | Value |
|---|---|
| `KACS_CLAIM_TYPE_INT64` | `0x0001` (1) |
| `KACS_CLAIM_TYPE_UINT64` | `0x0002` (2) |
| `KACS_CLAIM_TYPE_STRING` | `0x0003` (3) |
| `KACS_CLAIM_TYPE_SID` | `0x0005` (5) |
| `KACS_CLAIM_TYPE_BOOLEAN` | `0x0006` (6) |
| `KACS_CLAIM_TYPE_OCTET` | `0x0010` (16) |

*Claim attribute flags.* <a id="cite-kacs-abi.claim-attribute-flags"></a>

| Constant | Value |
|---|---|
| `KACS_CLAIM_ATTR_CASE_SENSITIVE` | `0x0002` (2) |
| `KACS_CLAIM_ATTR_USE_FOR_DENY_ONLY` | `0x0004` (4) |
| `KACS_CLAIM_ATTR_DISABLED` | `0x0010` (16) |

Central Access Policy (CAAP) spec wire format — the (spec, spec_len)
buffer kacs_set_caap (SYS_KACS_SET_CAAP) consumes. A non-empty spec
replaces the policy identified by the call's policy SID; a NULL/zero
spec removes it. The buffer is a fixed prefix followed by rule_count
per-rule sections, and is consumed exactly (trailing bytes are
rejected). It is not a C struct (the rule sections are variable-length);
read it as raw bytes: __u8 version must be KACS_CAAP_SPEC_VERSION __le32
rule_count number of rules that follow (<= max) rule_count * { __le32
applies_to_len [__u8 applies_to[applies_to_len]] conditional-expression
bytecode; 0 = always __le32 effective_dacl_len [__u8
effective_dacl[...]] binary ACL; length MUST be nonzero __le32
effective_sacl_len [__u8 effective_sacl[...]] (0 = none) __le32
staged_dacl_len [__u8 staged_dacl[...]] (0 = none) __le32
staged_sacl_len [__u8 staged_sacl[...]] (0 = none) } Every length-
prefixed field uses a little-endian __u32 length and is bounded by
KACS_CAAP_MAX_FIELD_BYTES; ACL payloads additionally parse under the
security-descriptor size limit (KACS_CAAP_MAX_ACL_BYTES). ACLs use the
binary ACL format from <pkm/sd.h>; applies_to is conditional-ACE
bytecode. <a id="cite-kacs-abi.caap-spec-wire-format"></a>

| Constant | Value |
|---|---|
| `KACS_CAAP_SPEC_VERSION` | `0x01` (1) |
| `KACS_CAAP_MAX_SPEC_BYTES` | `262144` |
| `KACS_CAAP_MAX_RULE_COUNT` | `256` |
| `KACS_CAAP_MAX_FIELD_BYTES` | `65536` |
| `KACS_CAAP_MAX_ACL_BYTES` | `65535` |

*Byte offsets of the fixed CAAP-spec prefix fields.* <a id="cite-kacs-abi.caap-spec-offsets"></a>

| Constant | Value |
|---|---|
| `KACS_CAAP_SPEC_OFF_VERSION` | `0` |
| `KACS_CAAP_SPEC_OFF_RULE_COUNT` | `1` |

*Byte length of the fixed CAAP-spec prefix (version + rule_count).* <a id="cite-kacs-abi.caap-spec-prefix-bytes"></a>

| Constant | Value |
|---|---|
| `KACS_CAAP_SPEC_PREFIX_BYTES` | `5` |

<a id="trm-3-a-11"></a>

## Security descriptor constants

From `uapi/pkm/sd.h`.

*Byte length of the self-relative security-descriptor header.* <a id="cite-kacs-abi.sd-header-bytes"></a>

| Constant | Value |
|---|---|
| `KACS_SD_HEADER_BYTES` | `20` |

SECURITY_INFORMATION selector bits — which components of a security
descriptor a kacs_get_sd / kacs_set_sd call reads or writes. <a id="cite-kacs-abi.security-information-bits"></a>

| Constant | Value |
|---|---|
| `KACS_SECINFO_OWNER` | `0x00000001` (1) |
| `KACS_SECINFO_GROUP` | `0x00000002` (2) |
| `KACS_SECINFO_DACL` | `0x00000004` (4) |
| `KACS_SECINFO_SACL` | `0x00000008` (8) |
| `KACS_SECINFO_LABEL` | `0x00000010` (16) |

*SECURITY_DESCRIPTOR_CONTROL bits — the SD header `control` field.* <a id="cite-kacs-abi.sd-control-bits"></a>

| Constant | Value |
|---|---|
| `KACS_SD_OWNER_DEFAULTED` | `0x0001` (1) |
| `KACS_SD_GROUP_DEFAULTED` | `0x0002` (2) |
| `KACS_SD_DACL_PRESENT` | `0x0004` (4) |
| `KACS_SD_DACL_DEFAULTED` | `0x0008` (8) |
| `KACS_SD_SACL_PRESENT` | `0x0010` (16) |
| `KACS_SD_SACL_DEFAULTED` | `0x0020` (32) |
| `KACS_SD_DACL_TRUSTED` | `0x0040` (64) |
| `KACS_SD_SERVER_SECURITY` | `0x0080` (128) |
| `KACS_SD_DACL_AUTO_INHERIT_REQ` | `0x0100` (256) |
| `KACS_SD_SACL_AUTO_INHERIT_REQ` | `0x0200` (512) |
| `KACS_SD_DACL_AUTO_INHERITED` | `0x0400` (1024) |
| `KACS_SD_SACL_AUTO_INHERITED` | `0x0800` (2048) |
| `KACS_SD_DACL_PROTECTED` | `0x1000` (4096) |
| `KACS_SD_SACL_PROTECTED` | `0x2000` (8192) |
| `KACS_SD_RM_CONTROL_VALID` | `0x4000` (16384) |
| `KACS_SD_SELF_RELATIVE` | `0x8000` (32768) |

*Access-mask bits — standard rights (bits 16-24) and generic rights (bits 28-31).* <a id="cite-kacs-abi.standard-and-generic-rights"></a>

The low 16 bits of a mask are object-class specific; see <pkm/file.h>
and <pkm/token.h> for those.

| Constant | Value |
|---|---|
| `KACS_ACCESS_DELETE` | `0x00010000` (65536) |
| `KACS_ACCESS_READ_CONTROL` | `0x00020000` |
| `KACS_ACCESS_WRITE_DAC` | `0x00040000` |
| `KACS_ACCESS_WRITE_OWNER` | `0x00080000` |
| `KACS_ACCESS_SYNCHRONIZE` | `0x00100000` |
| `KACS_ACCESS_ACCESS_SYSTEM_SECURITY` | `0x01000000` |
| `KACS_ACCESS_MAXIMUM_ALLOWED` | `0x02000000` |
| `KACS_ACCESS_GENERIC_ALL` | `0x10000000` |
| `KACS_ACCESS_GENERIC_EXECUTE` | `0x20000000` |
| `KACS_ACCESS_GENERIC_WRITE` | `0x40000000` |
| `KACS_ACCESS_GENERIC_READ` | `0x80000000` |

*ACE types — the `ace_type` byte of an ACE header (MS-DTYP 2.4.4.1).* <a id="cite-kacs-abi.ace-types"></a>

| Constant | Value |
|---|---|
| `KACS_ACE_TYPE_ACCESS_ALLOWED` | `0x00` (0) |
| `KACS_ACE_TYPE_ACCESS_DENIED` | `0x01` (1) |
| `KACS_ACE_TYPE_SYSTEM_AUDIT` | `0x02` (2) |
| `KACS_ACE_TYPE_SYSTEM_ALARM` | `0x03` (3) |
| `KACS_ACE_TYPE_ACCESS_ALLOWED_COMPOUND` | `0x04` (4) |
| `KACS_ACE_TYPE_ACCESS_ALLOWED_OBJECT` | `0x05` (5) |
| `KACS_ACE_TYPE_ACCESS_DENIED_OBJECT` | `0x06` (6) |
| `KACS_ACE_TYPE_SYSTEM_AUDIT_OBJECT` | `0x07` (7) |
| `KACS_ACE_TYPE_SYSTEM_ALARM_OBJECT` | `0x08` (8) |
| `KACS_ACE_TYPE_ACCESS_ALLOWED_CALLBACK` | `0x09` (9) |
| `KACS_ACE_TYPE_ACCESS_DENIED_CALLBACK` | `0x0A` (10) |
| `KACS_ACE_TYPE_ACCESS_ALLOWED_CALLBACK_OBJECT` | `0x0B` (11) |
| `KACS_ACE_TYPE_ACCESS_DENIED_CALLBACK_OBJECT` | `0x0C` (12) |
| `KACS_ACE_TYPE_SYSTEM_AUDIT_CALLBACK` | `0x0D` (13) |
| `KACS_ACE_TYPE_SYSTEM_ALARM_CALLBACK` | `0x0E` (14) |
| `KACS_ACE_TYPE_SYSTEM_AUDIT_CALLBACK_OBJECT` | `0x0F` (15) |
| `KACS_ACE_TYPE_SYSTEM_ALARM_CALLBACK_OBJECT` | `0x10` (16) |
| `KACS_ACE_TYPE_SYSTEM_MANDATORY_LABEL` | `0x11` (17) |
| `KACS_ACE_TYPE_SYSTEM_RESOURCE_ATTRIBUTE` | `0x12` (18) |
| `KACS_ACE_TYPE_SYSTEM_SCOPED_POLICY_ID` | `0x13` (19) |
| `KACS_ACE_TYPE_SYSTEM_PROCESS_TRUST_LABEL` | `0x14` (20) |
| `KACS_ACE_TYPE_SYSTEM_ACCESS_FILTER` | `0x15` (21) |

*ACE header `ace_flags` byte — inheritance and audit control.* <a id="cite-kacs-abi.ace-flags"></a>

| Constant | Value |
|---|---|
| `KACS_ACE_FLAG_OBJECT_INHERIT` | `0x01` (1) |
| `KACS_ACE_FLAG_CONTAINER_INHERIT` | `0x02` (2) |
| `KACS_ACE_FLAG_NO_PROPAGATE_INHERIT` | `0x04` (4) |
| `KACS_ACE_FLAG_INHERIT_ONLY` | `0x08` (8) |
| `KACS_ACE_FLAG_INHERITED` | `0x10` (16) |
| `KACS_ACE_FLAG_SUCCESSFUL_ACCESS` | `0x40` (64) |
| `KACS_ACE_FLAG_FAILED_ACCESS` | `0x80` (128) |

Mandatory-label policy bits — the __le32 access mask of a
KACS_ACE_TYPE_SYSTEM_MANDATORY_LABEL ACE. They control which DACL-
granted rights a caller whose integrity level does not dominate the
object's label (the "up" direction) is denied. Each bit suppresses the
rights mapped from the corresponding generic class; unknown bits MUST be
ignored. <a id="cite-kacs-abi.mandatory-label-policy-bits"></a>

| Constant | Value |
|---|---|
| `KACS_SYSTEM_MANDATORY_LABEL_NO_READ_UP` | `0x00000001` (1) |
| `KACS_SYSTEM_MANDATORY_LABEL_NO_WRITE_UP` | `0x00000002` (2) |
| `KACS_SYSTEM_MANDATORY_LABEL_NO_EXECUTE_UP` | `0x00000004` (4) |

Object-ACE body `Flags` field — the __le32 at object-ACE body offset 8,
distinct from the 1-byte `ace_flags` header field above. Indicates which
optional GUIDs the object-ACE body carries. <a id="cite-kacs-abi.object-ace-flags"></a>

| Constant | Value |
|---|---|
| `KACS_ACE_OBJECT_TYPE_PRESENT` | `0x00000001` (1) |
| `KACS_ACE_INHERITED_OBJECT_TYPE_PRESENT` | `0x00000002` (2) |

<a id="trm-3-a-12"></a>

## SID constants

From `uapi/pkm/sid.h`.

*Largest sub_authority_count a valid SID may declare.* <a id="cite-kacs-abi.sid-max-sub-authorities"></a>

| Constant | Value |
|---|---|
| `KACS_SID_MAX_SUB_AUTHORITIES` | `15` |

*Encoded byte length of a SID with the given sub-authority count.* <a id="cite-kacs-abi.sid-byte-len"></a>

| Constant | Value |
|---|---|
| `KACS_SID_BYTE_LEN(count)` | `(8 + 4 * (count))` |

*SID_AND_ATTRIBUTES "Attributes" bits (MS-DTYP 2.4.4).* <a id="cite-kacs-abi.sid-attribute-bits"></a>

These describe how a group or restricted SID participates in an access
check. MS-DTYP names them for groups; they apply to any
SID_AND_ATTRIBUTES entry.

| Constant | Value |
|---|---|
| `KACS_SID_GROUP_MANDATORY` | `0x00000001` (1) |
| `KACS_SID_GROUP_ENABLED_BY_DEFAULT` | `0x00000002` (2) |
| `KACS_SID_GROUP_ENABLED` | `0x00000004` (4) |
| `KACS_SID_GROUP_OWNER` | `0x00000008` (8) |
| `KACS_SID_GROUP_USE_FOR_DENY_ONLY` | `0x00000010` (16) |
| `KACS_SID_GROUP_INTEGRITY` | `0x00000020` (32) |
| `KACS_SID_GROUP_INTEGRITY_ENABLED` | `0x00000040` (64) |
| `KACS_SID_GROUP_RESOURCE` | `0x20000000` |
| `KACS_SID_GROUP_LOGON_ID` | `0xC0000000` |
