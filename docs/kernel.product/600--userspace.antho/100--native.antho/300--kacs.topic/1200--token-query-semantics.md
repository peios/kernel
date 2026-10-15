---
title: "Token query semantics"
description: "Token query semantics: behaviour and implementation of the Peios kernel."
type: reference
---

<a id="trm-3-d-2"></a>

## Querying a token handle

The ioctl is straightforward in shape:

```
ioctl(token_fd, KACS_IOC_QUERY, &args)
```

Where `args` is a `kacs_query_args` struct:

| Field | Meaning |
|---|---|
| `token_class` | The numeric class identifying what to return (1–24 in v0.20). |
| `buf_len` | Input: the size of the output buffer in bytes. Output: the actual number of bytes the query needed. |
| `buf_ptr` | Userspace pointer to the output buffer. |

The kernel:

1. Validates the class against the catalog. Unknown classes return `-EINVAL`.
2. Checks that the fd grants `TOKEN_QUERY`. If not, returns `-EACCES`.
3. Computes the size the response needs.
4. If `buf_ptr` is zero or `buf_len` is zero — this is a **size query** — writes the required size to `buf_len` and returns 0.
5. If `buf_ptr` is non-zero but `buf_len` is smaller than required, returns `-ERANGE` with the required size still written to `buf_len`.
6. Otherwise writes the response to the buffer and returns 0.

The "two-call pattern" — size query then fetch — is the standard way to handle variable-length output:

1. Call once with `buf_ptr = NULL` (or `buf_len = 0`). The kernel writes the required size into `buf_len` and returns 0.
2. Allocate a buffer of the indicated size.
3. Call again with `buf_ptr` set to the buffer and `buf_len` set to its size. The kernel writes the response.

For classes with a fixed-size response, a single call with a buffer of the known size works in one go. The two-call pattern is needed only for classes whose response size depends on the token's contents (the groups class, the restricted-SIDs class, the default-DACL class, the claims classes).

The ioctl is idempotent — multiple queries for the same class produce the same result as long as the token has not been modified. Tokens carry a `modified_id` counter that increments on adjustment; if a query is part of a pipeline that depends on consistency across multiple queries, the `modified_id` can be queried first to detect mid-pipeline changes.

<a id="trm-3-d-3"></a>

## Token query payloads <a id="cite-abi-notes.token-query-payloads"></a>

The class numbers come from the header and are tabulated in [KACS ABI Reference](<~kernel/userspace/native/kacs/generated-syscall-index#trm-3-a>);
these are the payloads each one returns. Sizes are in bytes; a variable-length payload uses
the shapes below. An invalid class returns `EINVAL`. <a id="cite-abi-notes.token-query-invalid-class"></a>

Two repeating shapes appear throughout. A **SID array** is
`[count:u32le]` followed by `count` entries of
`[sid_len:u32le][sid_bytes][attributes:u32le]`, and reports a count of
zero when the array is empty rather than an empty payload. <a id="cite-abi-notes.sid-array-shape"></a> A **claims
array** is `[count:u32le]` followed by `count` entries of
`[entry_len:u32le][entry_bytes]`. <a id="cite-abi-notes.claims-array-shape"></a> A bare SID is the SID bytes alone,
and an absent optional SID or ACL is zero bytes. <a id="cite-abi-notes.absent-optional-is-zero-bytes"></a>

| Class | Payload |
|---|---|
| `USER` | Bare SID. |
| `GROUPS` | SID array. |
| `PRIVILEGES` | 32 bytes: present, enabled, enabled-by-default and used, four `u64` in that order. |
| `TYPE` | `u32`, 4 bytes. |
| `INTEGRITY_LEVEL` | The mandatory-label SID `S-1-16-<level>`, 12 bytes. |
| `OWNER` | Bare SID, resolved through the owner index: 0 is the user SID, N is `groups[N-1]`. <a id="cite-abi-notes.owner-index-resolution"></a> |
| `PRIMARY_GROUP` | Bare SID, resolved the same way. |
| `INTERACTIVITY_SCOPE` | `u32`, 4 bytes. |
| `RESTRICTED_SIDS` | SID array; count 0 on an unrestricted token. |
| `SOURCE` | 16 bytes: an 8-byte name followed by a `u64` LUID. |
| `STATISTICS` | 40 bytes: token id, LogonSession id, modified id, token type, a reserved zero, and expiration. |
| `ORIGIN` | `u64`, 8 bytes. |
| `ELEVATION_TYPE` | `u32`, 4 bytes. |
| `DEVICE_GROUPS` | SID array. |
| `APPCONTAINER_SID` | Bare SID; empty when the token is unconfined. |
| `CAPABILITIES` | SID array. |
| `MANDATORY_POLICY` | `u32`, 4 bytes. |
| `LOGON_TYPE` | `u32`, 4 bytes, read from the LogonSession. |
| `LOGON_SID` | Bare SID, derived from the LogonSession id. |
| `DEFAULT_DACL` | Binary ACL; empty when none is set. |
| `IMPERSONATION_LEVEL` | `u32`, 4 bytes. |
| `USER_CLAIMS` | Claims array. |
| `DEVICE_CLAIMS` | Claims array. |
| `PROJECTED_SUPPLEMENTARY_GIDS` | `[count:u32le]` followed by `count` `u32` GIDs. |
| `GUID` | 16 raw bytes: the immutable token instance GUID, in the same byte order as KMES headers. |

`KACS_TOKEN_CLASS_GUID` (`0x19`) uses the standard query contract: a size probe reports 16, a non-probe buffer smaller than 16 returns `ERANGE` without a partial payload, and every query requires `TOKEN_QUERY`. `TOKEN_QUERY_SOURCE` alone does not grant it. <a id="cite-token.query.guid-size-and-right"></a>

Adjusting a token preserves its GUID; duplicating or restricting it creates a distinct token with a new GUID. Reopening the same token returns the same GUID. The `STATISTICS` payload remains 40 bytes and its token id is a LUID, not this GUID. <a id="cite-token.query.guid-immutable-instance"></a>

Querying the effective token returns the bytes stamped as KMES `effective_token_guid`; querying the real primary token returns `true_token_guid`. Impersonation changes which token the effective open selects, not either token's identity. <a id="cite-token.query.guid-matches-kmes"></a>

Several token fields have no query class at all: `created_at`,
`audit_policy`, `write_restricted`, `user_deny_only`,
`isolation_boundary`, `confinement_exempt`, the projected UID and GID
— only the supplementary GIDs are reportable —
`restricted_device_groups`, and the LCS registry credentials. <a id="cite-abi-notes.fields-without-query-class"></a>
