---
title: "Generated token and session ABI"
description: "Generated token and session ABI: behaviour and implementation of the Peios kernel."
type: reference
---

<a id="trm-3-a-2-1"></a>

## `struct kacs_query_args` <a id="cite-kacs-abi.struct-kacs-query-args"></a>

Total size 16 bytes.

| Offset | Size | Type | Field |
|---:|---:|---|---|
| 0 | 4 | `__u32` | `token_class` |
| 4 | 4 | `__u32` | `buf_len` |
| 8 | 8 | `__u64` | `buf_ptr` |

<a id="trm-3-a-2-2"></a>

## `struct kacs_adjust_privs_args` <a id="cite-kacs-abi.struct-kacs-adjust-privs-args"></a>

Total size 24 bytes.

| Offset | Size | Type | Field |
|---:|---:|---|---|
| 0 | 4 | `__u32` | `count` |
| 4 | 4 | `__u32` | `_pad` |
| 8 | 8 | `__u64` | `data_ptr` |
| 16 | 8 | `__u64` | `previous_enabled` |

<a id="trm-3-a-2-3"></a>

## `struct kacs_priv_entry` <a id="cite-kacs-abi.struct-kacs-priv-entry"></a>

Total size 8 bytes.

| Offset | Size | Type | Field |
|---:|---:|---|---|
| 0 | 4 | `__u32` | `luid` |
| 4 | 4 | `__u32` | `attributes` |

<a id="trm-3-a-2-4"></a>

## `struct kacs_adjust_groups_args` <a id="cite-kacs-abi.struct-kacs-adjust-groups-args"></a>

Total size 144 bytes.

| Offset | Size | Type | Field |
|---:|---:|---|---|
| 0 | 4 | `__u32` | `count` |
| 4 | 4 | `__u32` | `_pad` |
| 8 | 8 | `__u64` | `data_ptr` |
| 16 | 128 | `__u64``[16]` | `previous_state` |

<a id="trm-3-a-2-5"></a>

## `struct kacs_duplicate_args` <a id="cite-kacs-abi.struct-kacs-duplicate-args"></a>

Total size 16 bytes.

| Offset | Size | Type | Field |
|---:|---:|---|---|
| 0 | 4 | `__u32` | `access_mask` |
| 4 | 4 | `__u32` | `token_type` |
| 8 | 4 | `__u32` | `impersonation_level` |
| 12 | 4 | `__s32` | `result_fd` |

<a id="trm-3-a-2-6"></a>

## `struct kacs_group_entry` <a id="cite-kacs-abi.struct-kacs-group-entry"></a>

Total size 8 bytes.

| Offset | Size | Type | Field |
|---:|---:|---|---|
| 0 | 4 | `__u32` | `index` |
| 4 | 4 | `__u32` | `enable` |

<a id="trm-3-a-2-7"></a>

## `struct kacs_adjust_default_args` <a id="cite-kacs-abi.struct-kacs-adjust-default-args"></a>

Total size 16 bytes.

| Offset | Size | Type | Field |
|---:|---:|---|---|
| 0 | 8 | `__u64` | `dacl_ptr` |
| 8 | 4 | `__u32` | `dacl_len` |
| 12 | 2 | `__u16` | `owner_index` |
| 14 | 2 | `__u16` | `group_index` |

<a id="trm-3-a-2-8"></a>

## `struct kacs_restrict_args` <a id="cite-kacs-abi.struct-kacs-restrict-args"></a>

Total size 40 bytes.

| Offset | Size | Type | Field |
|---:|---:|---|---|
| 0 | 8 | `__u64` | `privs_to_delete` |
| 8 | 4 | `__u32` | `num_deny_indices` |
| 12 | 4 | `__u32` | `num_restrict_sids` |
| 16 | 4 | `__u32` | `data_len` |
| 20 | 4 | `__u32` | `flags` |
| 24 | 8 | `__u64` | `data_ptr` |
| 32 | 4 | `__s32` | `result_fd` |
| 36 | 4 | `__u32` | `_pad` |

<a id="trm-3-a-2-9"></a>

## `struct kacs_link_tokens_args` <a id="cite-kacs-abi.struct-kacs-link-tokens-args"></a>

Total size 16 bytes.

| Offset | Size | Type | Field |
|---:|---:|---|---|
| 0 | 4 | `__s32` | `elevated_fd` |
| 4 | 4 | `__s32` | `filtered_fd` |
| 8 | 8 | `__u64` | `logon_session_id` |

<a id="trm-3-a-2-10"></a>

## `struct kacs_get_linked_token_args` <a id="cite-kacs-abi.struct-kacs-get-linked-token-args"></a>

Total size 4 bytes.

| Offset | Size | Type | Field |
|---:|---:|---|---|
| 0 | 4 | `__s32` | `result_fd` |

<a id="trm-3-a-3"></a>

## Token constants

From `uapi/pkm/token.h`.

*kacs_open_self_token (SYS_KACS_OPEN_SELF_TOKEN) flags.* <a id="cite-kacs-abi.open-self-token-flags"></a>

| Constant | Value |
|---|---|
| `KACS_TOKEN_OPEN_REAL` | `0x01` (1) |

*Per-handle token rights (the low 16 bits of a token access mask).* <a id="cite-kacs-abi.token-access-rights"></a>

| Constant | Value |
|---|---|
| `KACS_TOKEN_ASSIGN_PRIMARY` | `0x0001` (1) |
| `KACS_TOKEN_DUPLICATE` | `0x0002` (2) |
| `KACS_TOKEN_IMPERSONATE` | `0x0004` (4) |
| `KACS_TOKEN_QUERY` | `0x0008` (8) |
| `KACS_TOKEN_QUERY_SOURCE` | `0x0010` (16) |
| `KACS_TOKEN_ADJUST_PRIVS` | `0x0020` (32) |
| `KACS_TOKEN_ADJUST_GROUPS` | `0x0040` (64) |
| `KACS_TOKEN_ADJUST_DEFAULT` | `0x0080` (128) |
| `KACS_TOKEN_ADJUST_INTERACTIVITY_SCOPE` | `0x0100` (256) |
| `KACS_TOKEN_ALL_ACCESS` | `0x000F01FF` |

*Token ioctl interface identifier.* <a id="cite-kacs-abi.token-ioctl-magic"></a>

| Constant | Value |
|---|---|
| `KACS_IOC_MAGIC` | `0x4B` (75) |

*kacs_priv_entry.attributes bits.* <a id="cite-kacs-abi.privilege-attributes"></a>

| Constant | Value |
|---|---|
| `KACS_PRIVILEGE_ATTR_ENABLED` | `0x00000002` (2) |
| `KACS_PRIVILEGE_ATTR_REMOVED` | `0x00000004` (4) |

*kacs_adjust_privs bulk-reset flag (not a per-entry attribute).* <a id="cite-kacs-abi.privilege-reset-all-defaults"></a>

| Constant | Value |
|---|---|
| `KACS_PRIVILEGE_RESET_ALL_DEFAULTS` | `0x80000000` |

*kacs_restrict_args.flags bits.* <a id="cite-kacs-abi.restrict-flags"></a>

| Constant | Value |
|---|---|
| `KACS_TOKEN_RESTRICT_WRITE_RESTRICTED` | `0x00000001` (1) |

*Token type (KACS_TOKEN_CLASS_TYPE).* <a id="cite-kacs-abi.token-types"></a>

| Constant | Value |
|---|---|
| `KACS_TOKEN_TYPE_PRIMARY` | `0x01` (1) |
| `KACS_TOKEN_TYPE_IMPERSONATION` | `0x02` (2) |

*Impersonation level (KACS_TOKEN_CLASS_IMPERSONATION_LEVEL).* <a id="cite-kacs-abi.impersonation-levels"></a>

| Constant | Value |
|---|---|
| `KACS_IMLEVEL_ANONYMOUS` | `0x00` (0) |
| `KACS_IMLEVEL_IDENTIFICATION` | `0x01` (1) |
| `KACS_IMLEVEL_IMPERSONATION` | `0x02` (2) |
| `KACS_IMLEVEL_DELEGATION` | `0x03` (3) |

*Elevation type (KACS_TOKEN_CLASS_ELEVATION_TYPE).* <a id="cite-kacs-abi.elevation-types"></a>

| Constant | Value |
|---|---|
| `KACS_ELEVATION_DEFAULT` | `0x01` (1) |
| `KACS_ELEVATION_FULL` | `0x02` (2) |
| `KACS_ELEVATION_LIMITED` | `0x03` (3) |

*Mandatory-policy bits (KACS_TOKEN_CLASS_MANDATORY_POLICY).* <a id="cite-kacs-abi.mandatory-policy-bits"></a>

| Constant | Value |
|---|---|
| `KACS_TOKEN_MANDATORY_POLICY_NO_WRITE_UP` | `0x00000001` (1) |
| `KACS_TOKEN_MANDATORY_POLICY_NEW_PROCESS_MIN` | `0x00000002` (2) |

Per-token audit-policy bits — the create-token spec `audit_policy` field
(KACS_TOKEN_SPEC_OFF_AUDIT_POLICY). They select which access-check
outcomes the token's object accesses generate audit events for. <a id="cite-kacs-abi.audit-policy-bits"></a>

| Constant | Value |
|---|---|
| `KACS_AUDIT_POLICY_OBJECT_ACCESS_SUCCESS` | `0x00000001` (1) |
| `KACS_AUDIT_POLICY_OBJECT_ACCESS_FAILURE` | `0x00000002` (2) |
| `KACS_AUDIT_POLICY_PRIVILEGE_USE_SUCCESS` | `0x00000004` (4) |
| `KACS_AUDIT_POLICY_PRIVILEGE_USE_FAILURE` | `0x00000008` (8) |

*Logon type (KACS_TOKEN_CLASS_LOGON_TYPE).* <a id="cite-kacs-abi.logon-types"></a>

| Constant | Value |
|---|---|
| `KACS_LOGON_TYPE_INTERACTIVE` | `2` |
| `KACS_LOGON_TYPE_NETWORK` | `3` |
| `KACS_LOGON_TYPE_BATCH` | `4` |
| `KACS_LOGON_TYPE_SERVICE` | `5` |
| `KACS_LOGON_TYPE_NETWORK_CLEARTEXT` | `8` |
| `KACS_LOGON_TYPE_NEW_CREDENTIALS` | `9` |
| `KACS_LOGON_TYPE_REMOTE_INTERACTIVE` | `10` |

*Maximum number of groups a token may carry.* <a id="cite-kacs-abi.token-max-groups"></a>

| Constant | Value |
|---|---|
| `KACS_TOKEN_MAX_GROUPS` | `1024` |

*Number of 64-bit words in a group enabled-state bitmask (KACS_TOKEN_MAX_GROUPS / 64).* <a id="cite-kacs-abi.token-group-mask-words"></a>

| Constant | Value |
|---|---|
| `KACS_TOKEN_GROUP_MASK_WORDS` | `16` |

*kacs_create_token (SYS_KACS_CREATE_TOKEN) spec wire format.* <a id="cite-kacs-abi.token-spec-wire-format"></a>

The (spec, len) buffer the syscall consumes is a fixed
KACS_TOKEN_SPEC_HEADER_BYTES-byte header followed by variable-length
sections at header-specified byte offsets. An offset/length (or
offset/count) pair that is both zero means the section is absent.
Sections may appear in any order; every offset+length is validated to
fall within the buffer. The header is not a C struct (it carries packed
mixed-width fields and crosses the syscall boundary as raw bytes); read
each field at its KACS_TOKEN_SPEC_OFF_* offset. Its fields, in order:
__u32 version must be KACS_TOKEN_SPEC_VERSION __u8 token_type
KACS_TOKEN_TYPE_ __u8 impersonation_level KACS_IMLEVEL_ __u8
_reserved0[2] must be 0 __u32 integrity_rid integrity-level RID __u32
mandatory_policy KACS_TOKEN_MANDATORY_POLICY_* bits __u64 privs_present
privilege bitmask (KACS_SE_*_PRIVILEGE) __u64 privs_enabled initially
enabled privileges (subset) __u32 _reserved1 must be 0 (elevation set
only by LINK_TOKENS) __u32 projected_uid Linux UID for credential
projection __u32 projected_gid Linux GID for credential projection __u32
audit_policy per-token audit flags __u64 expiration expiry timestamp (0
= none) __u64 logon_session_id logon session ID (auth_id) __u32
owner_sid_index 0 = user SID, 1..N = caller group __u32
primary_group_index 0 = user SID, 1..N = caller group __u8
source_name[8] token source name __u64 source_id token source LUID __u32
user_sid_offset byte offset to the user SID __u32 groups_offset byte
offset to the groups array __u32 groups_count number of group entries
__u32 default_dacl_offset byte offset to the default DACL (0 = none)
__u32 default_dacl_len default DACL byte length (0 = none) __u32
user_claims_offset byte offset to user claims (0 = none) __u32
user_claims_len user claims byte length (0 = none) __u32
device_claims_offset byte offset to device claims (0 = none) __u32
device_claims_len device claims byte length (0 = none) __u32
device_groups_offset byte offset to device groups (0 = none) __u32
device_groups_count number of device-group entries (0 = none) __u32
restricted_sids_offset byte offset to restricted SIDs (0 = none) __u32
restricted_sids_count number of restricted-SID entries (0 = none) __u32
confinement_sid_offset byte offset to confinement SID (0 = none) __u32
confinement_sid_len confinement SID byte length (0 = none) __u32
confinement_caps_offset byte offset to confinement caps (0 = none) __u32
confinement_caps_count number of confinement-cap entries (0 = none) __u8
confinement_exempt 1 = exempt from confinement __u8 write_restricted 1 =
write-restricted mode __u8 user_deny_only 1 = user SID matches deny ACEs
only __u8 isolation_boundary 1 = enable namespace filtering __u32
supp_gids_offset byte offset to supplementary GIDs (0 = none) __u32
supp_gids_count number of supplementary-GID entries (0 = none) __u32
restricted_device_groups_offset byte offset (0 = none) __u32
restricted_device_groups_count entry count (0 = none) __u64 origin
originating logon-session LUID (0 = none) __u32 interactivity_scope
interactive session number __u32 lcs_credentials_offset byte offset to
the LCS extension (0 = none) A group/device-group/restricted-
SID/confinement-cap/restricted-device-group entry is [__u32
sid_len][__u8 sid[sid_len]][__u32 attributes]. A supplementary-GIDs
section is supp_gids_count little-endian __u32 GIDs. All multi-byte
header and section scalars are little-endian.

| Constant | Value |
|---|---|
| `KACS_TOKEN_SPEC_VERSION` | `2` |
| `KACS_TOKEN_SPEC_HEADER_BYTES` | `192` |
| `KACS_TOKEN_SPEC_MIN_BYTES` | `192` |
| `KACS_TOKEN_SPEC_MAX_BYTES` | `65536` |

*Byte offsets of the fixed token-spec header fields.* <a id="cite-kacs-abi.token-spec-offsets"></a>

| Constant | Value |
|---|---|
| `KACS_TOKEN_SPEC_OFF_VERSION` | `0` |
| `KACS_TOKEN_SPEC_OFF_TOKEN_TYPE` | `4` |
| `KACS_TOKEN_SPEC_OFF_IMPERSONATION_LEVEL` | `5` |
| `KACS_TOKEN_SPEC_OFF_RESERVED0` | `6` |
| `KACS_TOKEN_SPEC_OFF_INTEGRITY_RID` | `8` |
| `KACS_TOKEN_SPEC_OFF_MANDATORY_POLICY` | `12` |
| `KACS_TOKEN_SPEC_OFF_PRIVS_PRESENT` | `16` |
| `KACS_TOKEN_SPEC_OFF_PRIVS_ENABLED` | `24` |
| `KACS_TOKEN_SPEC_OFF_RESERVED1` | `32` |
| `KACS_TOKEN_SPEC_OFF_PROJECTED_UID` | `36` |
| `KACS_TOKEN_SPEC_OFF_PROJECTED_GID` | `40` |
| `KACS_TOKEN_SPEC_OFF_AUDIT_POLICY` | `44` |
| `KACS_TOKEN_SPEC_OFF_EXPIRATION` | `48` |
| `KACS_TOKEN_SPEC_OFF_LOGON_SESSION_ID` | `56` |
| `KACS_TOKEN_SPEC_OFF_OWNER_SID_INDEX` | `64` |
| `KACS_TOKEN_SPEC_OFF_PRIMARY_GROUP_INDEX` | `68` |
| `KACS_TOKEN_SPEC_OFF_SOURCE_NAME` | `72` |
| `KACS_TOKEN_SPEC_OFF_SOURCE_ID` | `80` |
| `KACS_TOKEN_SPEC_OFF_USER_SID_OFFSET` | `88` |
| `KACS_TOKEN_SPEC_OFF_GROUPS_OFFSET` | `92` |
| `KACS_TOKEN_SPEC_OFF_GROUPS_COUNT` | `96` |
| `KACS_TOKEN_SPEC_OFF_DEFAULT_DACL_OFFSET` | `100` |
| `KACS_TOKEN_SPEC_OFF_DEFAULT_DACL_LEN` | `104` |
| `KACS_TOKEN_SPEC_OFF_USER_CLAIMS_OFFSET` | `108` |
| `KACS_TOKEN_SPEC_OFF_USER_CLAIMS_LEN` | `112` |
| `KACS_TOKEN_SPEC_OFF_DEVICE_CLAIMS_OFFSET` | `116` |
| `KACS_TOKEN_SPEC_OFF_DEVICE_CLAIMS_LEN` | `120` |
| `KACS_TOKEN_SPEC_OFF_DEVICE_GROUPS_OFFSET` | `124` |
| `KACS_TOKEN_SPEC_OFF_DEVICE_GROUPS_COUNT` | `128` |
| `KACS_TOKEN_SPEC_OFF_RESTRICTED_SIDS_OFFSET` | `132` |
| `KACS_TOKEN_SPEC_OFF_RESTRICTED_SIDS_COUNT` | `136` |
| `KACS_TOKEN_SPEC_OFF_CONFINEMENT_SID_OFFSET` | `140` |
| `KACS_TOKEN_SPEC_OFF_CONFINEMENT_SID_LEN` | `144` |
| `KACS_TOKEN_SPEC_OFF_CONFINEMENT_CAPS_OFFSET` | `148` |
| `KACS_TOKEN_SPEC_OFF_CONFINEMENT_CAPS_COUNT` | `152` |
| `KACS_TOKEN_SPEC_OFF_CONFINEMENT_EXEMPT` | `156` |
| `KACS_TOKEN_SPEC_OFF_WRITE_RESTRICTED` | `157` |
| `KACS_TOKEN_SPEC_OFF_USER_DENY_ONLY` | `158` |
| `KACS_TOKEN_SPEC_OFF_ISOLATION_BOUNDARY` | `159` |
| `KACS_TOKEN_SPEC_OFF_SUPP_GIDS_OFFSET` | `160` |
| `KACS_TOKEN_SPEC_OFF_SUPP_GIDS_COUNT` | `164` |
| `KACS_TOKEN_SPEC_OFF_RESTRICTED_DEVICE_GROUPS_OFFSET` | `168` |
| `KACS_TOKEN_SPEC_OFF_RESTRICTED_DEVICE_GROUPS_COUNT` | `172` |
| `KACS_TOKEN_SPEC_OFF_ORIGIN` | `176` |
| `KACS_TOKEN_SPEC_OFF_INTERACTIVITY_SCOPE` | `184` |
| `KACS_TOKEN_SPEC_OFF_LCS_CREDENTIALS_OFFSET` | `188` |

*Byte length of the fixed token-source-name field.* <a id="cite-kacs-abi.token-source-name-bytes"></a>

| Constant | Value |
|---|---|
| `KACS_TOKEN_SPEC_SOURCE_NAME_BYTES` | `8` |

Optional LCS registry-credentials extension, located at the token-spec
header's lcs_credentials_offset. The section is a fixed
KACS_TOKEN_LCS_EXT_HEADER_BYTES-byte header bounded by the next active
variable-section offset or the end of the spec; it is consumed exactly
(trailing bytes are malformed). Header fields, in order: __u32 version
must be KACS_TOKEN_LCS_EXT_VERSION __u32 _reserved must be 0 __u32
scope_count private hive scope GUIDs (<= max) __u32 private_layer_count
private layer names (<= max) Payload: scope_count raw 16-byte GUIDs,
then private_layer_count little-endian __u32 name byte lengths, then the
concatenated UTF-8 layer names. Scope GUIDs must be non-nil and unique;
layer names must be 1.. KACS_TOKEN_LCS_MAX_LAYER_NAME_BYTES bytes, must
not contain '\\', '/', or NUL, and must be unique under case-insensitive
matching. <a id="cite-kacs-abi.token-lcs-extension"></a>

| Constant | Value |
|---|---|
| `KACS_TOKEN_LCS_EXT_VERSION` | `1` |
| `KACS_TOKEN_LCS_EXT_HEADER_BYTES` | `16` |
| `KACS_TOKEN_LCS_SCOPE_GUID_BYTES` | `16` |
| `KACS_TOKEN_LCS_MAX_SCOPE_GUIDS` | `256` |
| `KACS_TOKEN_LCS_MAX_PRIVATE_LAYERS` | `256` |
| `KACS_TOKEN_LCS_MAX_LAYER_NAME_BYTES` | `255` |

*Byte offsets of the fixed LCS-extension header fields.* <a id="cite-kacs-abi.token-lcs-extension-offsets"></a>

| Constant | Value |
|---|---|
| `KACS_TOKEN_LCS_EXT_OFF_VERSION` | `0` |
| `KACS_TOKEN_LCS_EXT_OFF_RESERVED` | `4` |
| `KACS_TOKEN_LCS_EXT_OFF_SCOPE_COUNT` | `8` |
| `KACS_TOKEN_LCS_EXT_OFF_PRIVATE_LAYER_COUNT` | `12` |

*kacs_create_logon_session (SYS_KACS_CREATE_LOGON_SESSION) spec wire format.* <a id="cite-kacs-abi.logon-session-spec-wire-format"></a>

The (spec, len) buffer the syscall consumes is, in order: __u8
logon_type one of KACS_LOGON_TYPE_* above __le16 auth_pkg_len byte
length of the auth-package name __u8 auth_pkg[auth_pkg_len] auth-package
name (valid UTF-8) __le32 user_sid_len byte length of the user SID __u8
user_sid[user_sid_len] binary SID of the authenticated user The buffer
is consumed exactly: 7 + auth_pkg_len + user_sid_len must equal len. The
kernel assigns the session ID and derives the logon SID from it.

| Constant | Value |
|---|---|
| `KACS_LOGON_SESSION_SPEC_MIN_BYTES` | `15` |
| `KACS_LOGON_SESSION_SPEC_MAX_BYTES` | `4096` |

*Byte offsets of the fixed-position session-spec fields.* <a id="cite-kacs-abi.logon-session-spec-offsets"></a>

| Constant | Value |
|---|---|
| `KACS_LOGON_SESSION_SPEC_OFF_LOGON_TYPE` | `0` |
| `KACS_LOGON_SESSION_SPEC_OFF_AUTH_PKG_LEN` | `1` |
| `KACS_LOGON_SESSION_SPEC_OFF_AUTH_PKG` | `3` |

*Token-handle ioctls.* <a id="cite-kacs-abi.token-ioctls"></a>

| Constant | Value |
|---|---|
| `KACS_IOC_QUERY` | `0xC0104B00` |
| `KACS_IOC_ADJUST_PRIVS` | `0x40184B01` |
| `KACS_IOC_DUPLICATE` | `0xC0104B02` |
| `KACS_IOC_INSTALL` | `0x00004B03` |
| `KACS_IOC_RESTRICT` | `0xC0284B04` |
| `KACS_IOC_LINK_TOKENS` | `0x40104B05` |
| `KACS_IOC_GET_LINKED_TOKEN` | `0xC0044B06` |
| `KACS_IOC_ADJUST_GROUPS` | `0x40904B07` |
| `KACS_IOC_IMPERSONATE` | `0x00004B08` |
| `KACS_IOC_ADJUST_DEFAULT` | `0x40104B09` |
| `KACS_IOC_ADJUST_INTERACTIVITY_SCOPE` | `0x40044B0A` |

*Token information classes (kacs_query_args.token_class).* <a id="cite-kacs-abi.token-information-classes"></a>

GUID returns 16 immutable raw bytes in the same order as KMES headers.

| Constant | Value |
|---|---|
| `KACS_TOKEN_CLASS_USER` | `0x01` (1) |
| `KACS_TOKEN_CLASS_GROUPS` | `0x02` (2) |
| `KACS_TOKEN_CLASS_PRIVILEGES` | `0x03` (3) |
| `KACS_TOKEN_CLASS_TYPE` | `0x04` (4) |
| `KACS_TOKEN_CLASS_INTEGRITY_LEVEL` | `0x05` (5) |
| `KACS_TOKEN_CLASS_OWNER` | `0x06` (6) |
| `KACS_TOKEN_CLASS_PRIMARY_GROUP` | `0x07` (7) |
| `KACS_TOKEN_CLASS_INTERACTIVITY_SCOPE` | `0x08` (8) |
| `KACS_TOKEN_CLASS_RESTRICTED_SIDS` | `0x09` (9) |
| `KACS_TOKEN_CLASS_SOURCE` | `0x0A` (10) |
| `KACS_TOKEN_CLASS_STATISTICS` | `0x0B` (11) |
| `KACS_TOKEN_CLASS_ORIGIN` | `0x0C` (12) |
| `KACS_TOKEN_CLASS_ELEVATION_TYPE` | `0x0D` (13) |
| `KACS_TOKEN_CLASS_DEVICE_GROUPS` | `0x0E` (14) |
| `KACS_TOKEN_CLASS_APPCONTAINER_SID` | `0x0F` (15) |
| `KACS_TOKEN_CLASS_CAPABILITIES` | `0x10` (16) |
| `KACS_TOKEN_CLASS_MANDATORY_POLICY` | `0x11` (17) |
| `KACS_TOKEN_CLASS_LOGON_TYPE` | `0x12` (18) |
| `KACS_TOKEN_CLASS_LOGON_SID` | `0x13` (19) |
| `KACS_TOKEN_CLASS_DEFAULT_DACL` | `0x14` (20) |
| `KACS_TOKEN_CLASS_IMPERSONATION_LEVEL` | `0x15` (21) |
| `KACS_TOKEN_CLASS_USER_CLAIMS` | `0x16` (22) |
| `KACS_TOKEN_CLASS_DEVICE_CLAIMS` | `0x17` (23) |
| `KACS_TOKEN_CLASS_PROJECTED_SUPPLEMENTARY_GIDS` | `0x18` (24) |
| `KACS_TOKEN_CLASS_GUID` | `0x19` (25) |

Privileges, as single-bit masks within a token's 64-bit privilege word
(present / enabled / enabled-by-default / used are each one such word).
Named for the Windows privilege identifiers (SeTcbPrivilege, …). <a id="cite-kacs-abi.privilege-bits"></a>

| Constant | Value |
|---|---|
| `KACS_SE_CREATE_TOKEN_PRIVILEGE` | `4` |
| `KACS_SE_ASSIGN_PRIMARY_TOKEN_PRIVILEGE` | `8` |
| `KACS_SE_LOCK_MEMORY_PRIVILEGE` | `16` |
| `KACS_SE_INCREASE_QUOTA_PRIVILEGE` | `32` |
| `KACS_SE_TCB_PRIVILEGE` | `128` |
| `KACS_SE_SECURITY_PRIVILEGE` | `256` |
| `KACS_SE_TAKE_OWNERSHIP_PRIVILEGE` | `512` |
| `KACS_SE_LOAD_DRIVER_PRIVILEGE` | `1024` |
| `KACS_SE_SYSTEM_PROFILE_PRIVILEGE` | `2048` |
| `KACS_SE_SYSTEMTIME_PRIVILEGE` | `4096` |
| `KACS_SE_PROFILE_SINGLE_PROCESS_PRIVILEGE` | `8192` |
| `KACS_SE_INCREASE_BASE_PRIORITY_PRIVILEGE` | `16384` |
| `KACS_SE_BACKUP_PRIVILEGE` | `131072` |
| `KACS_SE_RESTORE_PRIVILEGE` | `262144` |
| `KACS_SE_SHUTDOWN_PRIVILEGE` | `524288` |
| `KACS_SE_DEBUG_PRIVILEGE` | `0x100000` (1048576) |
| `KACS_SE_AUDIT_PRIVILEGE` | `0x200000` (2097152) |
| `KACS_SE_CHANGE_NOTIFY_PRIVILEGE` | `0x800000` (8388608) |
| `KACS_SE_REMOTE_SHUTDOWN_PRIVILEGE` | `0x1000000` (16777216) |
| `KACS_SE_MANAGE_VOLUME_PRIVILEGE` | `0x10000000` (268435456) |
| `KACS_SE_IMPERSONATE_PRIVILEGE` | `0x20000000` (536870912) |
| `KACS_SE_RELABEL_PRIVILEGE` | `0x100000000` (4294967296) |
| `KACS_SE_CREATE_SYMBOLIC_LINK_PRIVILEGE` | `0x800000000` (34359738368) |
