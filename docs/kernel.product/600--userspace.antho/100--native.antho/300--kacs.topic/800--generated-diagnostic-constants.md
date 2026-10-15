---
title: "Generated diagnostic constants"
description: "Generated diagnostic constants: behaviour and implementation of the Peios kernel."
type: reference
---

<a id="trm-3-a-13"></a>

## Tracepoint diagnostic codes

From `uapi/pkm/trace.h`.

*kacs_access_decision reason — why a KACS access hook took the return path it did.* <a id="cite-kacs-abi.trace.access-decision-reasons"></a>

Emitted by the kacs:kacs_file_access / _file_open / _native_open
_inode_file_access / _inode_permission events. Verdict (allow vs deny)
is a separate signal, read from the `ret` field (0 == allow).

| Constant | Value | Notes |
|---|---|---|
| `KACS_TR_DECISION` | `0` | resolved allow/deny |
| `KACS_TR_BAD_ARGS` | `1` | NULL/zero argument guard |
| `KACS_TR_NO_ISEC` | `2` | inode has no i_security blob |
| `KACS_TR_UNMANAGED` | `3` | superblock mount policy UNMANAGED |
| `KACS_TR_PIP_CONTEXT` | `4` | current PIP context unavailable |
| `KACS_TR_NO_TOKEN` | `5` | no effective subject token |
| `KACS_TR_NO_DENTRY_ALIAS` | `6` | inode has no dentry alias yet |
| `KACS_TR_DELETE_ON_CLOSE_PENDING` | `7` | open of a delete-on-close file |
| `KACS_TR_NATIVE_STAMP` | `8` | native-open granted-access stamp |
| `KACS_TR_NATIVE_ARM` | `9` | native-open delete-on-close arm |
| `KACS_TR_STAMP` | `10` | legacy-open granted-access stamp |
| `KACS_TR_LAZY_DENTRY_RELOOKUP` | `11` | native create lazy re-lookup |
| `KACS_TR_NEGATIVE_AFTER_CREATE` | `12` | negative dentry after create |
| `KACS_TR_CHANGE_NOTIFY_PRIV` | `13` | traverse via CHANGE_NOTIFY priv |
| `KACS_TR_CHANGE_NOTIFY_PRIV_EXHAUSTED` | `14` | CHANGE_NOTIFY priv use exhausted |

*kacs_sd_cache reason — the inode security-descriptor cache outcome.* <a id="cite-kacs-abi.trace.sd-cache-reasons"></a>

The lookup miss codes disambiguate the three cache-absent paths that
were previously an indistinguishable NULL return (no cache / stale
generation missing-but-synthesis-required); the corrupt codes name why a
stored SD was rejected. Emitted by kacs:kacs_sd_cache_lookup / _corrupt.

| Constant | Value | Notes |
|---|---|---|
| `KACS_SDC_HIT` | `0` | current, valid cache present |
| `KACS_SDC_MISS_NONE` | `1` | no cache attached |
| `KACS_SDC_MISS_STALE_GEN` | `2` | cache present but stale generation |
| `KACS_SDC_MISS_NEEDS_SYNTH` | `3` | missing SD requires synthesis |
| `KACS_SDC_CORRUPT_EMPTY_OR_OVERSIZE` | `4` | stored SD zero-length or oversize |
| `KACS_SDC_CORRUPT_VALIDATE_FAIL` | `5` | stored SD failed validation |

kacs_process_access reason — the outcome of a cross-process access
decision (signal, ptrace, scheduler/attribute, prlimit). The reason
distinguishes the paths that all surface as -EACCES: an SD denial, a
PIP-based denial, a denial rescued (or not) by SeDebugPrivilege, and a
PIP-dominance failure. Emitted by kacs:kacs_process_access. <a id="cite-kacs-abi.trace.process-access-reasons"></a>

| Constant | Value | Notes |
|---|---|---|
| `KACS_PA_ALLOW` | `0` | access granted |
| `KACS_PA_BAD_ARGS` | `1` | NULL subject/target guard |
| `KACS_PA_NO_TARGET` | `2` | target has no process state/SD |
| `KACS_PA_NO_SD` | `3` | target process SD unavailable |
| `KACS_PA_SD_ERROR` | `4` | SD check failed (non-EACCES) |
| `KACS_PA_PIP_DENIED` | `5` | denied by process-integrity policy |
| `KACS_PA_DEBUG_RESCUE` | `6` | SD denial rescued by SeDebugPrivilege |
| `KACS_PA_DEBUG_DENIED` | `7` | denied; no usable SeDebugPrivilege |
| `KACS_PA_PIP_DOMINANCE` | `8` | caller PIP does not dominate target |

*kacs_exec reason — an exec/bprm credential or PIP transition.* <a id="cite-kacs-abi.trace.exec-reasons"></a>

Distinguishes the uid/gid-change gate outcomes, the exec primary-token
derivation paths and their failures, the exec file integrity-label
lookup failures, and the two commit-time transitions. Verdict is the
`ret` field. Emitted by kacs:kacs_exec.

| Constant | Value | Notes |
|---|---|---|
| `KACS_EXEC_CREDS_ALLOW` | `0` | exec cred transition allowed |
| `KACS_EXEC_BAD_ARGS` | `1` | NULL cred/token guard |
| `KACS_EXEC_ID_CHANGE_NO_TOKEN` | `2` | uid/gid change, no subject token |
| `KACS_EXEC_ID_CHANGE_PRIV_UNSUPPORTED` | `3` | id change + ASSIGN_PRIMARY_TOKEN priv |
| `KACS_EXEC_TOKEN_NPM_DERIVED` | `4` | exec token derived via new-process-min |
| `KACS_EXEC_TOKEN_CLONE` | `5` | exec token via primary clone fallback |
| `KACS_EXEC_NPM_NO_FILE` | `6` | new-process-min needs file, none supplied |
| `KACS_EXEC_NPM_DERIVE_FAIL` | `7` | new_process_min_exec derivation failed |
| `KACS_EXEC_TOKEN_INSTALL_FAIL` | `8` | install token ref on new cred failed |
| `KACS_EXEC_TOKEN_CLONE_FAIL` | `9` | primary token clone returned NULL |
| `KACS_EXEC_INTEGRITY_NO_ISEC` | `10` | exec file inode has no i_security |
| `KACS_EXEC_INTEGRITY_NO_CACHE` | `11` | exec file SD cache absent |
| `KACS_EXEC_INTEGRITY_INVALID_SD` | `12` | exec file cached SD invalid/empty |
| `KACS_EXEC_IMPERSONATION_REVERT_FAIL` | `13` | bprm impersonation revert failed |
| `KACS_EXEC_PIP_COMMITTED` | `14` | pending exec PIP committed at commit |
| `KACS_EXEC_UMH_NOT_TCB` | `15` | usermodehelper exec below PeiosTcb trust |
| `KACS_EXEC_SIGNATURE_UNVERIFIABLE` | `16` | exec refused: signature could not be verified |
| `KACS_EXEC_PIP_CAPPED_UNSAFE` | `17` | exec PIP label capped at the current one: traced or no_new_privs |

kacs_signing reason — code-signature verification outcomes and the
distinct reject reasons of the signing-material probe. Only source enum,
verified flag, PIP tier codes, file length, reason, and ret are recorded
— never key, signature, xattr, or file bytes. Emitted by
kacs:kacs_signing_verify _crypto / _probe. <a id="cite-kacs-abi.trace.signing-reasons"></a>

| Constant | Value | Notes |
|---|---|---|
| `KACS_SIG_UNSIGNED` | `0` | material source NONE (unsigned) |
| `KACS_SIG_BAD_KEY_TABLE` | `1` | key table malformed / bad args |
| `KACS_SIG_NO_KEY_MATCH` | `2` | no key verified the signature |
| `KACS_SIG_VERIFIED` | `3` | a key verified; trust assigned |
| `KACS_SIG_CRYPTO_UNAVAILABLE` | `4` | mldsa65 tfm allocation failed |
| `KACS_SIG_CRYPTO_MISMATCH` | `5` | set-pubkey/verify returned nonzero |
| `KACS_SIG_PROBE_FOUND` | `6` | valid signature material committed |
| `KACS_SIG_ELF_MAGIC_READ` | `7` | failed reading ELF magic |
| `KACS_SIG_ELF_SHORT_EHDR` | `8` | file too short for Elf64_Ehdr |
| `KACS_SIG_ELF_EHDR_READ` | `9` | failed reading ELF header |
| `KACS_SIG_ELF_BAD_IDENT` | `10` | unsupported e_ident class/data/version |
| `KACS_SIG_ELF_BAD_SHTABLE` | `11` | bad shentsize/shstrndx |
| `KACS_SIG_ELF_SHDRS_RANGE` | `12` | section-header table offset/len out of range |
| `KACS_SIG_ELF_SHSTR_READ` | `13` | failed reading shstrtab section header |
| `KACS_SIG_ELF_STRTAB_RANGE` | `14` | shstrtab offset/len out of range |
| `KACS_SIG_ELF_SHDR_READ` | `15` | failed reading a section header |
| `KACS_SIG_ELF_NAME_READ` | `16` | failed reading a section name |
| `KACS_SIG_ELF_BAD_SIG_SECTION` | `17` | sig section wrong type/size/range |
| `KACS_SIG_ELF_BAD_BLOB` | `18` | sig blob read failed or invalid |
| `KACS_SIG_ELF_HASH_FAIL` | `19` | hashing failed for ELF sig |
| `KACS_SIG_XATTR_BAD_BLOB` | `20` | xattr sig blob invalid |
| `KACS_SIG_XATTR_HASH_FAIL` | `21` | hashing failed for xattr sig |
| `KACS_SIG_SIZE_CHANGED` | `22` | file size changed during probe (TOCTOU) |

kacs_firmware reason — why a kernel-initiated firmware read was allowed
or refused (kacs/firmware.c, PEI-493). Firmware is code that runs on a
device with DMA into host memory, so it is held to the PeiosTcb tier:
the same bar as a usermodehelper exec. `ret` is the verdict handed to
the loader; under log mode it is 0 whatever the reason. Emitted by
kacs:kacs_firmware_load. No path, key, or signature bytes are recorded. <a id="cite-kacs-abi.trace.firmware-reasons"></a>

| Constant | Value | Notes |
|---|---|---|
| `KACS_FW_ALLOWED` | `0` | verified at PeiosTcb |
| `KACS_FW_UNSIGNED` | `1` | no signature material on the file |
| `KACS_FW_NO_KEY_MATCH` | `2` | signed, but no built-in key verified it |
| `KACS_FW_BELOW_TCB` | `3` | verified, but the key's tier is below PeiosTcb |
| `KACS_FW_UNVERIFIABLE` | `4` | verification could not run (crypto unavailable) |
| `KACS_FW_PROBE_FAILED` | `5` | reading the signature material failed |

*kacs_socket reason — the outcome of an AF_UNIX socket SD / impersonation hook.* <a id="cite-kacs-abi.trace.socket-reasons"></a>

Distinguishes the guard, not-applicable, and verdict paths that
otherwise collapse into an indistinguishable -EACCES. Verdict is the
`ret` field. No address, pathname, or SD bytes are recorded.

| Constant | Value | Notes |
|---|---|---|
| `KACS_SOCK_BAD_ARGS` | `0` | NULL/guard argument rejected |
| `KACS_SOCK_NOT_UNIX` | `1` | not AF_UNIX / unsupported type |
| `KACS_SOCK_NO_SECURITY` | `2` | sock has no sk_security blob |
| `KACS_SOCK_NO_TOKEN` | `3` | no effective subject/client token |
| `KACS_SOCK_BAD_LEVEL` | `4` | invalid impersonation level |
| `KACS_SOCK_WRONG_STATE` | `5` | socket state forbids the op |
| `KACS_SOCK_NO_PEER_TOKEN` | `6` | no captured peer token present |
| `KACS_SOCK_PIP_CONTEXT` | `7` | caller PIP context unavailable |
| `KACS_SOCK_SD_DECISION` | `8` | socket-SD check produced verdict |
| `KACS_SOCK_NO_SD` | `9` | no socket SD; allowed without check |
| `KACS_SOCK_HAVE_SD` | `10` | socket SD present; check performed |
| `KACS_SOCK_ALREADY_BOUND` | `11` | socket SD already installed |
| `KACS_SOCK_BIND` | `12` | abstract-socket SD bind result |
| `KACS_SOCK_CONNECT` | `13` | unix_stream_connect result |
| `KACS_SOCK_LEVEL_SET` | `14` | impersonation level updated |
| `KACS_SOCK_OPEN_TOKEN` | `15` | open peer-token fd result |

*16 was KACS_SOCK_IMPERSONATE (kacs_impersonate_peer); retired, not reused.* <a id="cite-kacs-abi.trace.socket-reason-16-retired"></a>

| Constant | Value | Notes |
|---|---|---|
| `KACS_SOCK_ATTACH` | `17` | identity attached to a send |
| `KACS_SOCK_GATE` | `18` | explicit KACS_SCM_TOKEN send-gate verdict |
| `KACS_SOCK_REGISTER` | `19` | conveyed-identity register advanced |
| `KACS_SOCK_DELIVER` | `20` | KACS_SCM_TOKEN delivered to a receiver |
| `KACS_SOCK_LISTEN` | `21` | listener identity captured at listen() |
| `KACS_SOCK_RESTAMP` | `22` | listener identity replaced by KACS_SO_RESTAMP |
| `KACS_SOCK_PORT_BIND` | `23` | inet bind: port reservation SD verdict |
| `KACS_SOCK_PORT_TABLE` | `24` | port reservation table load result |
| `KACS_SOCK_OWNER` | `25` | governing identity stamped on an inet socket |

*kacs_ipc reason — a System V IPC object SD decision (ipc.c).* <a id="cite-kacs-abi.trace.ipc-reasons"></a>

| Constant | Value | Notes |
|---|---|---|
| `KACS_IPC_ALLOC` | `0` | default SD stamped at *get creation |
| `KACS_IPC_PERMISSION` | `1` | ipc_permission: read/write access to the object |
| `KACS_IPC_CTL` | `2` | *ctl command gate (RMID/SET/STAT/...) |
| `KACS_IPC_SD_QUERY` | `3` | kacs_get_sd on the object |
| `KACS_IPC_SD_SET` | `4` | kacs_set_sd on the object |
| `KACS_IPC_NO_SD` | `5` | object carries no SD; fail closed |

*kacs_namespace stage — which sub-decision of a namespace-mutation hook a record describes.* <a id="cite-kacs-abi.trace.namespace-stages"></a>

Single-decision ops report PRIMARY; multi-stage ops (link, rename,
delete fallback) tag each distinct verdict. Verdict is the `ret` field.
Never records a pathname. Emitted by the kacs:kacs_inode_* events.

| Constant | Value | Notes |
|---|---|---|
| `KACS_NS_PRIMARY` | `0` | the op's principal decision |
| `KACS_NS_PARENT_FALLBACK` | `1` | delete: parent DELETE_CHILD fallback |
| `KACS_NS_SOURCE` | `2` | link/rename source-side decision |
| `KACS_NS_DEST` | `3` | link/rename destination-parent add |
| `KACS_NS_DELETE_EXISTING` | `4` | rename: delete pre-existing dest |

kacs_psb reason — which process-security-baseline path an event marks:
mitigation activation (apply) or a W^X / LSV / PIE / prctl-lock
enforcement denial. The ok-vs-deny verdict is read from `ret`. Emitted
by kacs:kacs_psb_*. <a id="cite-kacs-abi.trace.psb-reasons"></a>

| Constant | Value | Notes |
|---|---|---|
| `KACS_PSB_APPLY_OK` | `0` | mitigations applied; result_bits set |
| `KACS_PSB_APPLY_NORMALIZE` | `1` | requested mask bad or unsupported (EINVAL/ENODEV) |
| `KACS_PSB_APPLY_MM_ACQUIRE` | `2` | could not acquire target mm (EACCES) |
| `KACS_PSB_APPLY_CFIF` | `3` | forward-CFI (IBT) activation failed |
| `KACS_PSB_APPLY_SML` | `4` | speculative-mitigation-lock activation failed |
| `KACS_PSB_APPLY_CFIB` | `5` | backward-CFI (shadow stack) activation failed |
| `KACS_PSB_WXP_MMAP` | `6` | W^X blocked a W+X mmap |
| `KACS_PSB_WXP_MPROTECT` | `7` | W^X blocked an mprotect transition |
| `KACS_PSB_WXP_EXISTING_VMA` | `8` | W^X activation blocked by an existing W+X vma |
| `KACS_PSB_LSV_PROBE` | `9` | LSV signing probe of the image failed |
| `KACS_PSB_LSV_VERIFY` | `10` | LSV signature not verified/trusted |
| `KACS_PSB_LSV_PIP_DOMINANCE` | `11` | LSV image PIP does not dominate process PIP |
| `KACS_PSB_PIE_ET_EXEC` | `12` | PIE blocked a non-PIE ET_EXEC image |
| `KACS_PSB_PRCTL_SML` | `13` | prctl blocked by SML lock |
| `KACS_PSB_PRCTL_CFIB` | `14` | prctl blocked by shadow-stack (CFIB) lock |
| `KACS_PSB_PRCTL_PIP` | `15` | prctl set-dumpable blocked by process PIP |

*kacs_token_ioctl cmd — which token-fd ioctl verb a record describes.* <a id="cite-kacs-abi.trace.token-ioctl-cmds"></a>

The verdict (allow vs deny) is read from the `ret` field (0 == allow);
the access-mask-gate rejections surface as ret == -EACCES. `token` is an
opaque numeric id (never token bytes). Emitted by kacs:kacs_token_ioctl.

| Constant | Value | Notes |
|---|---|---|
| `KACS_TOK_QUERY` | `0` | KACS_IOC_QUERY |
| `KACS_TOK_ADJUST_PRIVS` | `1` | KACS_IOC_ADJUST_PRIVS |
| `KACS_TOK_ADJUST_GROUPS` | `2` | KACS_IOC_ADJUST_GROUPS |
| `KACS_TOK_DUPLICATE` | `3` | KACS_IOC_DUPLICATE |
| `KACS_TOK_INSTALL` | `4` | KACS_IOC_INSTALL |
| `KACS_TOK_RESTRICT` | `5` | KACS_IOC_RESTRICT |
| `KACS_TOK_LINK` | `6` | KACS_IOC_LINK_TOKENS |
| `KACS_TOK_GET_LINKED` | `7` | KACS_IOC_GET_LINKED_TOKEN |
| `KACS_TOK_IMPERSONATE` | `8` | KACS_IOC_IMPERSONATE |
| `KACS_TOK_ADJUST_DEFAULT` | `9` | KACS_IOC_ADJUST_DEFAULT |
| `KACS_TOK_ADJUST_INTERACTIVITY_SCOPE` | `10` | KACS_IOC_ADJUST_INTERACTIVITY_SCOPE |
| `KACS_TOK_UNKNOWN` | `11` | unrecognised ioctl verb (-ENOTTY) |

*kacs_token_ref reason — a token-fd reference lifecycle transition.* <a id="cite-kacs-abi.trace.token-ref-reasons"></a>

TO_FD is a token installed into a fresh anon-inode handle; RELEASE is
the handle teardown that drops the token ref; BIND clones a token onto
an existing file; OPEN is the checked/fixed-access open path that clones
the target token. `token` is an opaque numeric id, never token bytes.
Emitted by kacs:kacs_token_ref.

| Constant | Value | Notes |
|---|---|---|
| `KACS_TREF_TO_FD` | `0` | token installed into a new fd (ret == fd) |
| `KACS_TREF_RELEASE` | `1` | token-fd released; ref dropped |
| `KACS_TREF_BIND` | `2` | token cloned + bound onto an existing file |
| `KACS_TREF_OPEN` | `3` | token cloned for a token-open path |

*kacs_logon_session reason — a session/token creation-surface outcome.* <a id="cite-kacs-abi.trace.logon-session-reasons"></a>

The *_DENIED codes name the privilege-gate rejections (the value); the
plain op codes mark the successful op. Verdict is also in `ret`. No
token/spec bytes are recorded. Emitted by kacs:kacs_logon_session.

| Constant | Value | Notes |
|---|---|---|
| `KACS_SES_CREATE` | `0` | create_logon_session published a session |
| `KACS_SES_CREATE_PRIV_DENIED` | `1` | create_logon_session: TCB privilege gate denied |
| `KACS_SES_DESTROY` | `2` | destroy_empty_logon_session outcome |
| `KACS_SES_DESTROY_PRIV_DENIED` | `3` | destroy: TCB privilege gate denied |
| `KACS_SES_CREATE_TOKEN` | `4` | create_token issued a token fd |
| `KACS_SES_CREATE_TOKEN_PRIV_DENIED` | `5` | create_token: CREATE_TOKEN privilege denied |

kacs_cred reason — a credential-security lifecycle transition: LSM cred
prepare/transfer/alloc/free, explicit token-ref install, the clone-time
primary-token lifecycle (CLONE_THREAD share vs fork deep-copy), and the
project-linux-cred rejection paths. old_token/new_token are opaque token
pointer ids (0 when absent); clone_flags is set only on the clone paths.
Verdict/outcome is the `ret` field. Emitted by kacs:kacs_cred. <a id="cite-kacs-abi.trace.cred-reasons"></a>

| Constant | Value | Notes |
|---|---|---|
| `KACS_CRED_PREPARE` | `0` | cred_prepare token clone |
| `KACS_CRED_TRANSFER` | `1` | cred_transfer token clone |
| `KACS_CRED_ALLOC_BLANK` | `2` | cred_alloc_blank cleared sec |
| `KACS_CRED_FREE` | `3` | cred_free released token/state |
| `KACS_CRED_INSTALL_TOKEN_REF` | `4` | install token ref on a cred |
| `KACS_CRED_CLONE_THREAD_SHARE` | `5` | CLONE_THREAD shares parent primary cred |
| `KACS_CRED_CLONE_FORK_COPY` | `6` | fork deep-copies parent primary token |
| `KACS_CRED_PROJECT_UID0_BLOCKED` | `7` | uid0 projection not allowed by token |
| `KACS_CRED_PROJECT_GROUPS_ALLOC_FAIL` | `8` | groups_alloc failed (ENOMEM) |
| `KACS_CRED_PROJECT_E2BIG` | `9` | supplementary gid count > NGROUPS_MAX |

kacs_setid reason — the KACS gate on a Linux setid projection
(task_fix_setuid / _setgid / _setgroups). Each op has two distinct
denials that otherwise collapse: NO_TOKEN (-EACCES, no effective subject
token) and PRIV_GATE (-EOPNOTSUPP, holder of ASSIGN_PRIMARY_TOKEN
privilege). `flags` is the LSM_SETID_* mask (0 for setgroups). Emitted
by kacs:kacs_setid. <a id="cite-kacs-abi.trace.setid-reasons"></a>

| Constant | Value | Notes |
|---|---|---|
| `KACS_SETID_SETUID_NO_TOKEN` | `0` | setuid gate: no subject token |
| `KACS_SETID_SETUID_PRIV_GATE` | `1` | setuid gate: ASSIGN_PRIMARY priv |
| `KACS_SETID_SETGID_NO_TOKEN` | `2` | setgid gate: no subject token |
| `KACS_SETID_SETGID_PRIV_GATE` | `3` | setgid gate: ASSIGN_PRIMARY priv |
| `KACS_SETID_SETGROUPS_NO_TOKEN` | `4` | setgroups gate: no subject token |
| `KACS_SETID_SETGROUPS_PRIV_GATE` | `5` | setgroups gate: ASSIGN_PRIMARY priv |

*kacs_task reason — a task-security lifecycle transition.* <a id="cite-kacs-abi.trace.task-reasons"></a>

task_alloc reports a NO_CHILD-mitigation clone block, a process-state
inherit ENOMEM, or success; task_free marks teardown. `process_state` is
an opaque process-state pointer id (0 when absent); `clone_flags` is set
on the alloc paths. Outcome is `ret`. Emitted by kacs:kacs_task.

| Constant | Value | Notes |
|---|---|---|
| `KACS_TASK_ALLOC_NO_CHILD_BLOCKED` | `0` | clone blocked by NO_CHILD mitigation |
| `KACS_TASK_ALLOC_INHERIT_ENOMEM` | `1` | process-state inherit failed (ENOMEM) |
| `KACS_TASK_ALLOC` | `2` | task_alloc completed |
| `KACS_TASK_FREE` | `3` | task_free teardown |

*kacs_primary_install reason — a primary-token / impersonation credential transition.* <a id="cite-kacs-abi.trace.primary-install-reasons"></a>

Distinguishes the install commit, the user-SID-change process-SD
reallocation and its ENOMEM, the commit_creds apply, the impersonation
override/revert, and the sibling-thread taskwork requeue/failure.
old_primary and new_primary are opaque token identity ids (never token
bytes). Verdict is the `ret` field. Emitted by
kacs:kacs_primary_install.

| Constant | Value | Notes |
|---|---|---|
| `KACS_PRIM_INSTALL_OK` | `0` | primary token install committed |
| `KACS_PRIM_SD_REALLOC` | `1` | user-SID changed; process SD reallocated |
| `KACS_PRIM_SD_ALLOC_FAIL` | `2` | process SD realloc failed (ENOMEM) |
| `KACS_PRIM_APPLY_COMMIT` | `3` | new real creds committed (commit_creds) |
| `KACS_PRIM_IMPERSONATE_INSTALL` | `4` | impersonation token installed (override_creds) |
| `KACS_PRIM_IMPERSONATE_REVERT` | `5` | impersonation reverted (revert_creds) |
| `KACS_PRIM_SIBLING_REQUEUE` | `6` | queued sibling install re-queued on ENOMEM |
| `KACS_PRIM_SIBLING_FAILED` | `7` | queued sibling install failed after apply |

kacs_process_token_open reason — the outcome of opening a process/thread
primary or effective token (kacs_open_process_token / _thread_token and
the proc inspection files). Distinguishes the bad access-mask reject,
the no-target-token path, the process access-check denial, the self vs
cross inspection verdicts, and the successful open.
subject_token/target_token are opaque token identity ids (0 when unknown
at the emit site); access_mask is the requested mask. Verdict is `ret`
(>=0 fd == allow). Emitted by kacs:kacs_process_token_open. <a id="cite-kacs-abi.trace.process-token-open-reasons"></a>

| Constant | Value | Notes |
|---|---|---|
| `KACS_PTO_OPEN_OK` | `0` | token fd opened |
| `KACS_PTO_BAD_ARGS` | `1` | NULL subject/state/task guard |
| `KACS_PTO_NO_TARGET` | `2` | target has no token |
| `KACS_PTO_BAD_ACCESS` | `3` | invalid access mask rejected |
| `KACS_PTO_ACCESS_DENIED` | `4` | process access check denied |
| `KACS_PTO_SELF` | `5` | self-target inspection allowed |
| `KACS_PTO_CROSS` | `6` | cross-process inspection authorized |

*kacs_process_state reason — a process-state / process-SD lifecycle or PIP transition.* <a id="cite-kacs-abi.trace.process-state-reasons"></a>

Covers process-state alloc/free, the CLONE_THREAD share vs fork
inheritance split, the no-child clone block, the pending-exec-PIP
stage/commit and dumpable hardening, and the process-SD
alloc/wrap/replace primitives. process_state is an opaque state-object
id (0 when none in scope, e.g. the process-SD primitives);
pip_type/pip_trust carry the PIP tier. `ret` is the outcome (0 == ok).
No token or SD bytes. Emitted by kacs:kacs_process_state.

| Constant | Value | Notes |
|---|---|---|
| `KACS_PST_ALLOC` | `0` | process state allocated |
| `KACS_PST_ALLOC_FAIL` | `1` | process state alloc failed (ENOMEM) |
| `KACS_PST_FREE` | `2` | process state freed (refcount hit 0) |
| `KACS_PST_INHERIT_SHARE` | `3` | CLONE_THREAD: parent state shared |
| `KACS_PST_INHERIT_FORK` | `4` | fork: new state allocated from parent |
| `KACS_PST_EXEC_PIP_STAGE` | `5` | pending exec PIP staged |
| `KACS_PST_EXEC_PIP_COMMIT` | `6` | pending exec PIP committed to state |
| `KACS_PST_DUMPABLE` | `7` | exec dumpable hardened by PIP |
| `KACS_PST_CLONE_BLOCKED_NOCHILD` | `8` | clone blocked by NO_CHILD mitigation |
| `KACS_PST_SD_ALLOC` | `9` | default process SD allocated |
| `KACS_PST_SD_ALLOC_FAIL` | `10` | process/socket SD alloc failed |
| `KACS_PST_SD_WRAP_FAIL` | `11` | process SD wrapper alloc failed (ENOMEM) |
| `KACS_PST_SD_REPLACE` | `12` | process SD replaced on state |
| `KACS_PST_SOCKET_SD_ALLOC` | `13` | default socket SD allocated |

*kacs_mount_policy reason — the outcome of a mount-policy set (TCB-gated) or get.* <a id="cite-kacs-abi.trace.mount-policy-reasons"></a>

SET_OK marks a committed policy change (generation bumped); the guard
codes name the pre-commit rejects that otherwise collapse into a bare
-EINVAL/-EOPNOTSUPP/-EPERM. GET_OK/GET_NO_SECURITY are the snapshot
paths. Verdict is also in `ret`. Emitted by kacs:kacs_mount_policy_set /
_get.

| Constant | Value | Notes |
|---|---|---|
| `KACS_MP_SET_OK` | `0` | policy committed; generation bumped |
| `KACS_MP_BAD_ARGS` | `1` | NULL subject/sb/args guard (EINVAL) |
| `KACS_MP_NO_SECURITY` | `2` | superblock has no s_security (EOPNOTSUPP) |
| `KACS_MP_UNMANAGED` | `3` | magic-derived UNMANAGED; not settable (EOPNOTSUPP) |
| `KACS_MP_VALIDATE` | `4` | mount-policy args validation failed (EINVAL) |
| `KACS_MP_TEMPLATE_INVALID` | `5` | template SD bytes failed validation (EINVAL) |
| `KACS_MP_TCB_DENIED` | `6` | SeTcbPrivilege gate denied (EPERM) |
| `KACS_MP_GET_OK` | `7` | policy snapshot returned |
| `KACS_MP_GET_NO_SECURITY` | `8` | get: no s_security; magic-derived policy returned |
| `KACS_MP_FIXED_POLICY` | `9` | filesystem fixes its policy class (EOPNOTSUPP) |

kacs_sd_syscall target_kind — which SD-bearing object a query/set record
describes, resolved by the get_sd/set_sd syscall target-kind
fallthrough. ACCESS_CHECK tags the AccessCheck ingress events
(kacs_access_check*), whose other scalar fields are 0 at the ingress
boundary. <a id="cite-kacs-abi.trace.sd-syscall-target-kinds"></a>

| Constant | Value | Notes |
|---|---|---|
| `KACS_SDS_KIND_TOKEN` | `0` | token-fd target |
| `KACS_SDS_KIND_FILE` | `1` | file/inode target |
| `KACS_SDS_KIND_PROCESS` | `2` | pidfd process target |
| `KACS_SDS_KIND_PATH` | `3` | path-resolved file target |
| `KACS_SDS_KIND_ACCESS_CHECK` | `4` | AccessCheck ingress (not an SD get/set) |

*kacs_sd_syscall reason — the outcome of an SD query/set core.* <a id="cite-kacs-abi.trace.sd-syscall-reasons"></a>

QUERY_OK/SET_OK are the success paths; the remaining codes name the
guard / denial paths that otherwise surface as an indistinguishable
-EINVAL/-EACCES/-EOPNOTSUPP. Verdict is also in `ret`. Emitted by
kacs:kacs_sd_query / _set.

| Constant | Value | Notes |
|---|---|---|
| `KACS_SDS_QUERY_OK` | `0` | SD subset extracted and returned |
| `KACS_SDS_SET_OK` | `1` | SD merged/replaced |
| `KACS_SDS_BAD_ARGS` | `2` | NULL/zero argument guard (EINVAL) |
| `KACS_SDS_UNMANAGED` | `3` | superblock UNMANAGED (EOPNOTSUPP) |
| `KACS_SDS_ACCESS_DENIED` | `4` | SD access check denied (EACCES) |
| `KACS_SDS_NO_SD` | `5` | target has no usable SD (EACCES) |
| `KACS_SDS_RESTORE_BYPASS` | `6` | set via SeRestorePrivilege bypass |
| `KACS_SDS_QUERY_FAIL` | `7` | subset extraction failed after auth |

kacs_access_check reason — the AccessCheck kernel-ingress outcome, above
the closed Slice 15 ABI bridge. OK is a completed ingress; the remaining
codes name the ingress-time rejects (token-eval-context gate, token
resolution, and caap-cache lock acquisition). Verdict is also in `ret`.
Emitted by kacs:kacs_access_check / _list. <a id="cite-kacs-abi.trace.access-check-reasons"></a>

| Constant | Value | Notes |
|---|---|---|
| `KACS_ACK_OK` | `0` | ingress dispatched to the ABI bridge |
| `KACS_ACK_EVAL_CONTEXT` | `1` | token-eval-context gate denied (EACCES) |
| `KACS_ACK_TOKEN_RESOLVE` | `2` | token/args resolution failed |
| `KACS_ACK_CAAP_LOCK_FAIL` | `3` | caap-cache lock acquisition failed |

*kacs_file_snapshot op — which snapshot-grant file operation an event marks.* <a id="cite-kacs-abi.trace.file-snapshot-ops"></a>

The allow-vs-deny verdict is read from `ret`; `reason` names why a deny
path was taken. Emitted by kacs:kacs_file_snapshot (file_access.c).

| Constant | Value | Notes |
|---|---|---|
| `KACS_FSOP_ACCESS` | `0` | generic snapshot-grant access check |
| `KACS_FSOP_PERMISSION` | `1` | file_permission hook |
| `KACS_FSOP_IOCTL` | `2` | file ioctl snapshot |
| `KACS_FSOP_LOCK` | `3` | file lock snapshot |
| `KACS_FSOP_FCNTL` | `4` | file fcntl snapshot |
| `KACS_FSOP_TRUNCATE` | `5` | file truncate snapshot |
| `KACS_FSOP_FALLOCATE` | `6` | file fallocate snapshot |
| `KACS_FSOP_MMAP` | `7` | file mmap snapshot |
| `KACS_FSOP_MPROTECT` | `8` | file mprotect snapshot |
| `KACS_FSOP_WRITE_INTENT` | `9` | write-intent snapshot |
| `KACS_FSOP_SYSFS_WRITE_GATE` | `10` | unmanaged sysfs write gate |

*kacs_file_snapshot reason — why a snapshot-grant op took its return path.* <a id="cite-kacs-abi.trace.file-snapshot-reasons"></a>

DECISION is the resolved allow/deny (verdict in `ret`); the remaining
codes name the distinct deny causes. Emitted by kacs:kacs_file_snapshot.

| Constant | Value | Notes |
|---|---|---|
| `KACS_FSR_DECISION` | `0` | resolved allow/deny (grant compare) |
| `KACS_FSR_SIGNED_EXEC` | `1` | signed-exec content mutation denied |
| `KACS_FSR_GRANT_DENY` | `2` | granted access lacked required right |
| `KACS_FSR_APPEND_DENY` | `3` | append/write intent lacked write grant |
| `KACS_FSR_UNMANAGED_SYSFS` | `4` | unmanaged fd: sysfs write gate applied |
| `KACS_FSR_AUDIT_EMIT_FAIL` | `5` | kacs.audit.handle.used emit failed |

*kacs_metadata reason — the file-metadata (getattr/setattr/xattr/getsecurity) decision path.* <a id="cite-kacs-abi.trace.metadata-reasons"></a>

DECISION/CONSUME_HIT/BEGIN_BUSY mark the begin/consume decision
lifecycle; the remaining codes name the distinct deny reasons of the
xattr setattr hooks. `op_class` carries the internal
PKM_KACS_METADATA_OP_* value; `matched` is the consume match flag.
Emitted by kacs:kacs_metadata (file_metadata.c).

| Constant | Value | Notes |
|---|---|---|
| `KACS_META_DECISION` | `0` | generic metadata decision |
| `KACS_META_CONSUME_HIT` | `1` | consumed a pre-staged decision |
| `KACS_META_BEGIN_BUSY` | `2` | begin failed: a decision already active |
| `KACS_META_CANONICAL_SD` | `3` | canonical SD xattr access denied |
| `KACS_META_CAPS_XATTR` | `4` | capability xattr mutation denied (EPERM) |
| `KACS_META_ACL` | `5` | POSIX ACL xattr denied |
| `KACS_META_SIGNED_EXEC` | `6` | signed-exec xattr/size mutation denied |
| `KACS_META_BAD_ARGS` | `7` | NULL name / dentry guard |
| `KACS_META_INTERNAL_SD` | `8` | internal SD read/write re-entry allowed |
| `KACS_META_GETSECURITY` | `9` | inode_getsecurity outcome |

kacs_native_open_ext reason — a widening decision inside the native
(kacs_open) create/open machinery. The PREPARE_* codes name the arg-
validation reject buckets of pkm_kacs_prepare_native_open; RESOLVE /
BUILD_CREATED_SD DELETE_ON_CLOSE_ARM name the later stage outcomes
(verdict in `ret`). Emitted by kacs:kacs_native_open_ext
(native_open.c). <a id="cite-kacs-abi.trace.native-open-ext-reasons"></a>

| Constant | Value | Notes |
|---|---|---|
| `KACS_NOX_PREPARE_OK` | `0` | prepare accepted the request |
| `KACS_NOX_PREPARE_BAD_FLAGS` | `1` | flags/create_options/__pad rejected |
| `KACS_NOX_PREPARE_BAD_SD_ARGS` | `2` | sd_ptr/sd_len/disposition-sd combo bad |
| `KACS_NOX_PREPARE_BAD_DISPOSITION` | `3` | create_disposition out of range |
| `KACS_NOX_PREPARE_BAD_ACCESS` | `4` | desired-access mask invalid/empty |
| `KACS_NOX_PREPARE_UNSUPPORTED` | `5` | valid but unsupported combination |
| `KACS_NOX_RESOLVE` | `6` | resolve-existing-path outcome |
| `KACS_NOX_BUILD_CREATED_SD` | `7` | build-created-file-SD outcome |
| `KACS_NOX_DELETE_ON_CLOSE_ARM` | `8` | delete-on-close arm outcome |

*kacs_object reason — which object-lifecycle verdict a record marks.* <a id="cite-kacs-abi.trace.object-reasons"></a>

Only the high-value transitions are traced (pure inode/file/sb
alloc/free are not). `ret` is the outcome (0 == ok). Emitted by
kacs:kacs_object.

| Constant | Value | Notes |
|---|---|---|
| `KACS_OBJ_DELETE_ON_CLOSE_UNLINK` | `0` | file_release delete-on-close unlink attempt |
| `KACS_OBJ_SIGNED_EXEC_PIN` | `1` | inode pinned as signed-exec (immutable) |
| `KACS_OBJ_SIGNED_EXEC_MUTATION_BLOCKED` | `2` | content mutation of a signed-exec-pinned inode denied |

*kacs_securityfs reason — which securityfs endpoint path a record marks.* <a id="cite-kacs-abi.trace.securityfs-reasons"></a>

The sessions_read codes disambiguate the deny rungs that otherwise
collapse into an errno; open_self / init report the endpoint outcome.
Verdict is `ret`. Emitted by kacs:kacs_securityfs.

| Constant | Value | Notes |
|---|---|---|
| `KACS_SFS_LOGON_SESSIONS_NO_TOKEN` | `0` | sessions read: no effective subject token |
| `KACS_SFS_LOGON_SESSIONS_PIP_CONTEXT` | `1` | sessions read: caller PIP context unavailable |
| `KACS_SFS_LOGON_SESSIONS_ACCESS_CHECK` | `2` | sessions read: rust access check denied |
| `KACS_SFS_OPEN_SELF` | `3` | open of kacs/self self-token file outcome |
| `KACS_SFS_INIT` | `4` | securityfs kacs/ endpoint init outcome |

*kacs_caap reason — which CAAP policy-cache path a record marks.* <a id="cite-kacs-abi.trace.caap-reasons"></a>

SET carries the post-set cache_len (an insert grows it; an evict/replace
may shrink it); INIT/DESTROY are cache lifecycle; TCB_GATE is the
SeTcbPrivilege gate deny. Emitted by kacs:kacs_caap. No SID or spec
bytes — lengths only.

| Constant | Value | Notes |
|---|---|---|
| `KACS_CAAP_TCB_GATE` | `0` | SeTcbPrivilege gate denied the caller |
| `KACS_CAAP_SET` | `1` | cache set (insert/evict); cache_len is post-set count |
| `KACS_CAAP_INIT` | `2` | CAAP cache created |
| `KACS_CAAP_DESTROY` | `3` | CAAP cache destroyed |

kacs_capability reason — the capability->privilege gate verdicts and the
capability LSM-hook outcomes. ALLOW_GRANT is an auto-granted allow-cap;
HARD_DENY is the SETPCAP/SETFCAP/MAC_OVERRIDE hard block;
PRIV_NOT_ENABLED USE_MARK_FAIL are the mapped-privilege gate failures;
CAPSET / PRCTL_GUARD CAPABLE / CAPGET report the corresponding hook
outcome. Emitted by kacs:kacs_capability. Verdict is `ret`. <a id="cite-kacs-abi.trace.capability-reasons"></a>

| Constant | Value | Notes |
|---|---|---|
| `KACS_CAP_ALLOW_GRANT` | `0` | allow-cap auto-granted (no privilege needed) |
| `KACS_CAP_HARD_DENY` | `1` | SETPCAP/SETFCAP/MAC_OVERRIDE hard-denied |
| `KACS_CAP_PRIV_NOT_ENABLED` | `2` | mapped privilege not enabled on token |
| `KACS_CAP_USE_MARK_FAIL` | `3` | privilege use-mark failed |
| `KACS_CAP_CAPSET` | `4` | capset core outcome |
| `KACS_CAP_PRCTL_GUARD` | `5` | prctl capability-guard outcome |
| `KACS_CAP_CAPABLE` | `6` | capable() hook guard-deny outcome |
| `KACS_CAP_CAPGET` | `7` | capget for-task outcome |

kacs_privilege reason — the require_enabled_privilege gate rungs plus
two standalone privilege-path markers. NULL_OR_ZERO is a null-
token/zero-mask guard; NOT_ENABLED / USE_MARK_FAIL are the gate
failures; CHANGE_NOTIFY marks the open_by_handle_at
SeChangeNotifyPrivilege check outcome; RCU_ENOMEM_ FALLBACK marks the
deferred-free ENOMEM synchronize_rcu fallback. Emitted by
kacs:kacs_privilege. Verdict is `ret`. <a id="cite-kacs-abi.trace.privilege-reasons"></a>

| Constant | Value | Notes |
|---|---|---|
| `KACS_PRIV_NULL_OR_ZERO` | `0` | null token or zero privilege mask |
| `KACS_PRIV_NOT_ENABLED` | `1` | privilege not enabled on token |
| `KACS_PRIV_USE_MARK_FAIL` | `2` | privilege use-mark failed |
| `KACS_PRIV_CHANGE_NOTIFY` | `3` | open_by_handle_at CHANGE_NOTIFY gate outcome |
| `KACS_PRIV_RCU_ENOMEM_FALLBACK` | `4` | deferred-free kmalloc failed; sync-rcu fallback |

*kacs_tlp reason — the trusted-launch-path decisions.* <a id="cite-kacs-abi.trace.tlp-reasons"></a>

CHECK_PATH marks a no-prefix-match executable-transition deny (path_len
+ prefix_count only, NEVER path or prefix bytes); REPLACE marks a
prefix-table replacement. Emitted by kacs:kacs_tlp. Verdict is `ret`.

| Constant | Value | Notes |
|---|---|---|
| `KACS_TLP_CHECK_PATH` | `0` | executable transition denied: no prefix match |
| `KACS_TLP_REPLACE` | `1` | TLP prefix table replaced |

*kacs_mntns reason — mount-namespace object lifecycle and the mount gate.*

SD_ALLOC / SD_ALLOC_FAIL mark a namespace minted with (or without) its
creator descriptor; the gate reasons say which rung admitted or refused
a mount-table change: PRIVILEGE is SeManageVolume / SeTcb, NO_SD is a
namespace with no descriptor (the initial one), OP_NOT_ADMITTED is an
operation the descriptor can never grant, SD_DECISION is the access
check against the namespace descriptor, PIP_CONTEXT a failure to read
the caller's PIP state. Emitted by kacs:kacs_mntns. Verdict is `ret`.

| Constant | Value | Notes |
|---|---|---|
| `KACS_MNTNS_SD_ALLOC` | `0` | namespace minted with a creator descriptor |
| `KACS_MNTNS_SD_ALLOC_FAIL` | `1` | descriptor could not be built |
| `KACS_MNTNS_GATE_PRIVILEGE` | `2` | admitted by SeManageVolume / SeTcb |
| `KACS_MNTNS_GATE_NO_SD` | `3` | namespace has no descriptor; refused |
| `KACS_MNTNS_GATE_OP_NOT_ADMITTED` | `4` | op needs the privilege whatever the SD says |
| `KACS_MNTNS_GATE_SD_DECISION` | `5` | access check against the namespace SD |
| `KACS_MNTNS_GATE_PIP_CONTEXT` | `6` | caller PIP context unavailable |
| `KACS_MNTNS_GATE_FS_NOT_ADMITTED` | `7` | filesystem type not on the unprivileged allowlist |
| `KACS_MNTNS_SB_STAMP` | `8` | unprivileged tmpfs stamped synth-ephemeral, creator template |
| `KACS_MNTNS_SB_STAMP_FAIL` | `9` | creator template could not be built |
