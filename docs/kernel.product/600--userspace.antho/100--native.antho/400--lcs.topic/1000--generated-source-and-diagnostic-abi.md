---
title: "Generated source and diagnostic ABI"
description: "Generated source and diagnostic ABI: behaviour and implementation of the Peios kernel."
type: reference
---

<a id="trm-5-a-3-18"></a>

## `struct reg_src_register_args` <a id="cite-lcs-abi.struct-reg-src-register-args"></a>

Total size 24 bytes.

| Offset | Size | Type | Field |
|---|---|---|---|
| 0 | 4 | `__u32` | `hive_count` |
| 4 | 4 | `__u32` | `_pad` |
| 8 | 8 | `__u64` | `max_sequence` |
| 16 | 8 | `__u64` | `hives_ptr` |

<a id="trm-5-a-3-19"></a>

## `struct reg_src_negotiate_args` <a id="cite-lcs-abi.struct-reg-src-negotiate-args"></a>

Total size 16 bytes.

| Offset | Size | Type | Field |
|---|---|---|---|
| 0 | 4 | `__u32` | `version` |
| 4 | 4 | `__u32` | `flags` |
| 8 | 8 | `__u64` | `session` |

<a id="trm-5-a-3-20"></a>

## `struct reg_src_request_context_args` <a id="cite-lcs-abi.struct-reg-src-request-context-args"></a>

Total size 40 bytes.

| Offset | Size | Type | Field |
|---|---|---|---|
| 0 | 8 | `__u64` | `session` |
| 8 | 8 | `__u64` | `request_id` |
| 16 | 8 | `__u64` | `request_deadline_ns` |
| 24 | 8 | `__u64` | `lifetime_deadline_ns` |
| 32 | 8 | `__u64` | `lease_deadline_ns` |

<a id="trm-5-a-3-21"></a>

## `struct reg_src_renew_args` <a id="cite-lcs-abi.struct-reg-src-renew-args"></a>

Total size 32 bytes.

| Offset | Size | Type | Field |
|---|---|---|---|
| 0 | 8 | `__u64` | `session` |
| 8 | 8 | `__u64` | `transaction_id` |
| 16 | 8 | `__u64` | `lifetime_deadline_ns` |
| 24 | 8 | `__u64` | `lease_deadline_ns` |

<a id="trm-5-a-3-22"></a>

## `struct reg_src_hive_entry` <a id="cite-lcs-abi.struct-reg-src-hive-entry"></a>

Total size 56 bytes.

| Offset | Size | Type | Field |
|---|---|---|---|
| 0 | 4 | `__u32` | `name_len` |
| 4 | 4 | `__u32` | `_pad0` |
| 8 | 8 | `__u64` | `name_ptr` |
| 16 | 16 | `__u8``[16]` | `root_guid` |
| 32 | 4 | `__u32` | `flags` |
| 36 | 4 | `__u32` | `_pad1` |
| 40 | 16 | `__u8``[16]` | `scope_guid` |

<a id="trm-5-a-5"></a>

## Tracepoint diagnostic codes

From `uapi/pkm/trace.h`. These are a diagnostic contract for
ftrace, perf and eBPF consumers, letting a tool decode an `lcs:`
event's `reason`, `op` or `state` field without recompiling
against a specific kernel. No LCS syscall accepts or returns
them, and values are append-only.

lcs_rsi_request op — which of the 18 RSI dispatch verbs a source-side
request admission record describes. Emitted by lcs:lcs_rsi_request on
successful queue admission and on the admission error rungs; the rung is
read from `ret` (0 == enqueued, -EAGAIN == in-flight at limit /
backpressure, -EIO == source gone / fd closing, -EOVERFLOW == request-id
space exhausted, other == build reject). The same op enum tags the
round-trip begin marker (lcs_rsi_roundtrip). Never records a pathname,
key name, GUID, or frame bytes — only this op code, ids, counts and ret. <a id="cite-lcs-abi.trace.rsi-request-ops"></a>

| Constant | Value | Notes |
|---|---|---|
| `LCS_OP_LOOKUP` | `0` | RSI_LOOKUP |
| `LCS_OP_READ_KEY` | `1` | RSI_READ_KEY |
| `LCS_OP_ENUM_CHILDREN` | `2` | RSI_ENUM_CHILDREN |
| `LCS_OP_QUERY_VALUES` | `3` | RSI_QUERY_VALUES |
| `LCS_OP_SET_VALUE` | `4` | RSI_SET_VALUE |
| `LCS_OP_DELETE_VALUE` | `5` | RSI_DELETE_VALUE_ENTRY |
| `LCS_OP_BLANKET_TOMBSTONE` | `6` | RSI_SET_BLANKET_TOMBSTONE |
| `LCS_OP_DROP_KEY` | `7` | RSI_DROP_KEY |
| `LCS_OP_CREATE_ENTRY` | `8` | RSI_CREATE_ENTRY |
| `LCS_OP_HIDE_ENTRY` | `9` | RSI_HIDE_ENTRY |
| `LCS_OP_DELETE_ENTRY` | `10` | RSI_DELETE_ENTRY |
| `LCS_OP_CREATE_KEY` | `11` | RSI_CREATE_KEY |
| `LCS_OP_WRITE_KEY` | `12` | RSI_WRITE_KEY |
| `LCS_OP_TXN_BEGIN` | `13` | RSI_BEGIN_TRANSACTION |
| `LCS_OP_TXN_COMMIT` | `14` | RSI_COMMIT_TRANSACTION |
| `LCS_OP_TXN_ABORT` | `15` | RSI_ABORT_TRANSACTION |
| `LCS_OP_FLUSH` | `16` | RSI_FLUSH |
| `LCS_OP_DELETE_LAYER` | `17` | RSI_DELETE_LAYER |

lcs_rsi_response reason — the outcome of accepting/validating a source's
RSI response frame, and the late-response effects that silently mark a
source DOWN. ACCEPTED is the clean path; DESYNC / OP_MISMATCH /
UNKNOWN_STATUS are the accept-time rejects that all surface as
-EINVAL/-EIO; MALFORMED_PAYLOAD is a per-op body validation reject; the
LATE_* codes mark a response whose deferred effect
(commit/mutation/begin bookkeeping) failed and took the source DOWN.
Verdict/outcome is also in `ret`. Never records name/GUID/frame bytes. <a id="cite-lcs-abi.trace.rsi-response-reasons"></a>

| Constant | Value | Notes |
|---|---|---|
| `LCS_RESP_ACCEPTED` | `0` | response matched an in-flight request |
| `LCS_RESP_DESYNC` | `1` | no matching delivered/unaccepted record |
| `LCS_RESP_OP_MISMATCH` | `2` | response op != request op \| RESPONSE_BIT |
| `LCS_RESP_UNKNOWN_STATUS` | `3` | rsi_status not a known status code |
| `LCS_RESP_MALFORMED_PAYLOAD` | `4` | per-op response body failed validation |
| `LCS_RESP_LATE_COMMIT_FAIL` | `5` | commit late-effect failed; source DOWN |
| `LCS_RESP_LATE_MUTATION_FAIL` | `6` | mutation late-effect failed; source DOWN |
| `LCS_RESP_LATE_BEGIN_FAIL` | `7` | begin-txn late-effect failed; source DOWN |

*lcs_source_fd reason — which source-fd lifecycle transition a record marks.* <a id="cite-lcs-abi.trace.source-fd-reasons"></a>

OPEN is a fresh /dev/pkm_registry fd; the remaining codes are the entry
points that drive a source to the DOWN/closing state. `source_down_id`
is the source id that transitioned DOWN (0 if the call was a no-op). The
semantic *cause* of a late-effect-driven DOWN is carried by
lcs_rsi_response (LCS_RESP_LATE_*); here EXPLICIT/MARK_BY_ID are the
mechanical transitions. No pathname/SD bytes.

| Constant | Value | Notes |
|---|---|---|
| `LCS_SRC_OPEN` | `0` | new source fd issued (post-TCB check) |
| `LCS_SRC_RELEASE` | `1` | fd .release() teardown |
| `LCS_SRC_MALFORMED` | `2` | malformed protocol frame -> mark down |
| `LCS_SRC_EXPLICIT` | `3` | explicit mark-down of this fd |
| `LCS_SRC_MARK_BY_ID` | `4` | mark-down requested by source id |

lcs_in_flight reason — an in-flight RSI request table transition (kept
lean; insert on admission, delivered when handed to the source's read(),
release on response completion or teardown). `in_flight_count` is the
post-transition depth. Emitted by lcs:lcs_in_flight. <a id="cite-lcs-abi.trace.in-flight-reasons"></a>

| Constant | Value | Notes |
|---|---|---|
| `LCS_IF_INSERT` | `0` | request inserted into in-flight table |
| `LCS_IF_DELIVERED` | `1` | request delivered to source read() |
| `LCS_IF_RELEASE` | `2` | request released from in-flight table |

*lcs_route op — which resolution the lcs:lcs_route event describes.* <a id="cite-lcs-abi.trace.route-ops"></a>

| Constant | Value | Notes |
|---|---|---|
| `LCS_ROUTE_HIVE_NAME` | `0` | hive-name -> source/root resolution |
| `LCS_ROUTE_ABSOLUTE_PATH` | `1` | absolute-path -> source/root resolution |
| `LCS_ROUTE_SYMLINK_TARGET` | `2` | symlink-target -> source/root resolution |

*lcs_registration decision — the source registration path.* <a id="cite-lcs-abi.trace.registration-decisions"></a>

NEW/RESUME_DOWN are publish verdicts; COPY is the input-copy stage;
REPLAY_FAIL/OVERFLOW_FAIL are resume post-publish -EIO paths that mark
the resumed source down. Emitted by lcs:lcs_source_register /
_registration_publish / _registration_copy.

| Constant | Value | Notes |
|---|---|---|
| `LCS_REG_NEW` | `0` | new source slot admitted |
| `LCS_REG_RESUME_DOWN` | `1` | down source slot resumed |
| `LCS_REG_COPY` | `2` | registration input copied from user |
| `LCS_REG_REPLAY_FAIL` | `3` | resume pending-delete replay failed (EIO) |
| `LCS_REG_OVERFLOW_FAIL` | `4` | resume overflow dispatch failed (EIO) |

*lcs_bootstrap stage — the phase of a bootstrap / self-config refresh.* <a id="cite-lcs-abi.trace.bootstrap-stages"></a>

Emitted by lcs:lcs_bootstrap_refresh / _self_config_refresh /
_self_config_publish.

| Constant | Value | Notes |
|---|---|---|
| `LCS_BOOT_REGISTRY` | `0` | registry root discover phase |
| `LCS_BOOT_KMES` | `1` | kmes config root discover phase |
| `LCS_BOOT_LAYERS` | `2` | layer metadata root discover phase |
| `LCS_BOOT_SELF_WATCH` | `3` | self-watch arm phase |
| `LCS_BOOT_COMPLETE` | `4` | bootstrap refresh completed |
| `LCS_BOOT_SELF_CONFIG_REFRESH` | `5` | self-config refresh-from-key outcome |
| `LCS_BOOT_SELF_CONFIG_PARAM_INVALID` | `6` | self-config publish rejected a parameter |

lcs_runtime_limits field_id — which runtime-limit field a validate
reject names, or LCS_LIM_ALL for a successful whole-struct publish.
Emitted by lcs:lcs_limits_validate (-EINVAL, `value` offending) and
lcs:lcs_limits_publish. <a id="cite-lcs-abi.trace.runtime-limit-fields"></a>

| Constant | Value | Notes |
|---|---|---|
| `LCS_LIM_REQUEST_TIMEOUT_MS` | `0` |  |
| `LCS_LIM_TRANSACTION_TIMEOUT_MS` | `1` |  |
| `LCS_LIM_NOTIFICATION_QUEUE_SIZE` | `2` |  |
| `LCS_LIM_SYMLINK_DEPTH_LIMIT` | `3` |  |
| `LCS_LIM_MAX_VALUE_SIZE` | `4` |  |
| `LCS_LIM_MAX_KEY_DEPTH` | `5` |  |
| `LCS_LIM_MAX_PATH_COMPONENT_LENGTH` | `6` |  |
| `LCS_LIM_MAX_TOTAL_PATH_LENGTH` | `7` |  |
| `LCS_LIM_MAX_LAYERS_PER_VALUE` | `8` |  |
| `LCS_LIM_MAX_BOUND_TRANSACTIONS_PER_SOURCE` | `9` |  |
| `LCS_LIM_MAX_READ_ONLY_TRANSACTIONS_PER_SOURCE` | `10` |  |
| `LCS_LIM_MAX_TOTAL_LAYERS` | `11` |  |
| `LCS_LIM_MAX_REGISTERED_SOURCES` | `12` |  |
| `LCS_LIM_MAX_HIVES_PER_SOURCE` | `13` |  |
| `LCS_LIM_MAX_CONCURRENT_RSI_REQUESTS` | `14` |  |
| `LCS_LIM_MAX_SCOPE_GUIDS_PER_TOKEN` | `15` |  |
| `LCS_LIM_MAX_PRIVATE_LAYERS_PER_TOKEN` | `16` |  |
| `LCS_LIM_MAX_SUBTREE_WATCH_DEPTH` | `17` |  |
| `LCS_LIM_MAX_TRANSACTION_WATCH_EVENT_BURST` | `18` |  |
| `LCS_LIM_ALL` | `19` | whole-struct publish (success) |

*lcs_audit event_type_id — which LCS audit event a record describes.* <a id="cite-lcs-abi.trace.audit-event-types"></a>

Emitted by lcs:lcs_audit_emit and lcs:lcs_audit_emit_failed.
`result_errno` carries the op-specific numeric. No SD or raw GUID bytes;
key GUID is a u64 hash.

| Constant | Value | Notes |
|---|---|---|
| `LCS_AUDIT_KEY_OPEN` | `0` | key-open SACL audit |
| `LCS_AUDIT_BACKUP_START` | `1` |  |
| `LCS_AUDIT_BACKUP_COMPLETE` | `2` |  |
| `LCS_AUDIT_RESTORE_START` | `3` |  |
| `LCS_AUDIT_RESTORE_COMPLETE` | `4` |  |
| `LCS_AUDIT_VALIDATION_FAILURE` | `5` | source validation-failure audit |
| `LCS_AUDIT_SELF_CONFIG_INVALID` | `6` | self-config-invalid audit |

*lcs_txn state — the transaction-fd state machine state carried in old_state new_state.* <a id="cite-lcs-abi.trace.txn-states"></a>

Emitted by lcs:lcs_txn_begin / _first_bind / _bind_mutation _commit /
_abort / _timeout / _source_down.

| Constant | Value | Notes |
|---|---|---|
| `LCS_TXN_ST_ACTIVE_UNBOUND` | `0` | allocated, not yet source-bound |
| `LCS_TXN_ST_ACTIVE_BOUND` | `1` | bound to a source + root guid |
| `LCS_TXN_ST_COMMITTED` | `2` | commit round-trip succeeded |
| `LCS_TXN_ST_ABORTED` | `3` | aborted (close / layer writer abort) |
| `LCS_TXN_ST_TIMED_OUT` | `4` | deadline timer or commit timeout |
| `LCS_TXN_ST_SOURCE_DOWN` | `5` | bound source marked down |

*lcs_key_fd cmd — the key-fd ioctl verb (also stamped on lcs_key_mutation).* <a id="cite-lcs-abi.trace.key-fd-cmds"></a>

LCS_KCMD_NONE is used by publish/release/read. Never records key/name/SD
bytes. Emitted by lcs:lcs_key_ioctl / _mutation.

| Constant | Value | Notes |
|---|---|---|
| `LCS_KCMD_NONE` | `0` | no ioctl verb (publish/release/read) |
| `LCS_KCMD_SET_VALUE` | `1` |  |
| `LCS_KCMD_DELETE_VALUE` | `2` |  |
| `LCS_KCMD_BLANKET_TOMBSTONE` | `3` |  |
| `LCS_KCMD_DELETE_KEY` | `4` |  |
| `LCS_KCMD_HIDE_KEY` | `5` |  |
| `LCS_KCMD_QUERY_VALUE` | `6` |  |
| `LCS_KCMD_QUERY_VALUES_BATCH` | `7` |  |
| `LCS_KCMD_ENUM_VALUES` | `8` |  |
| `LCS_KCMD_ENUM_SUBKEYS` | `9` |  |
| `LCS_KCMD_QUERY_KEY_INFO` | `10` |  |
| `LCS_KCMD_GET_SECURITY` | `11` |  |
| `LCS_KCMD_SET_SECURITY` | `12` |  |
| `LCS_KCMD_FLUSH` | `13` |  |
| `LCS_KCMD_BACKUP` | `14` |  |
| `LCS_KCMD_RESTORE` | `15` |  |
| `LCS_KCMD_NOTIFY` | `16` |  |
