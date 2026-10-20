---
title: "State and lifetime"
description: "The per-process structure describing what a process is, independent of the principal running it."
type: reference
---

<a id="trm-3-3-1"></a>

The Process Security Block is a per-process structure carrying
properties that describe **what the process is**, independent of the
principal running it.

Its PIP identity fields, `pip_type` and `pip_trust`, are determined by
the binary loaded at exec ([Binary Signature Verification](<~kernel/internals/kacs/executable-trust/signature-verification#trm-3-6>)). Its other fields — process
mitigations and process restrictions — are process policy, set by
whoever launches the process. Neither category is token identity, and
neither is determined by the principal.

Keeping the PSB separate from the token is the point. The token
describes identity and travels with impersonation: when a thread
impersonates a client, the effective token changes. The PSB describes
the process, and impersonation never touches it. <a id="cite-psb.impersonation-untouched"></a>

> The PSB is never affected by impersonation. Impersonation changes
> who the thread is acting as. It does not change what the process is.

The canonical PSB reference lives on the task's LSM security blob,
`task_struct->security`, separate from the credential that holds the
token pointer. <a id="cite-psb.canonical-on-task-blob"></a> A mirrored, non-authoritative reference is also kept in
credential security blobs, for the benefit of Linux hooks that receive
only a credential. For any task-attached credential that mirror refers
to the same PSB as the task blob, and it never defines a different
process identity. <a id="cite-psb.cred-mirror-same-psb"></a>

Credentials are swapped during impersonation, and that swap may change
the credential's token pointer — but the canonical PSB is untouched
and any credential-level mirror continues to refer to it. <a id="cite-psb.cred-swap-preserves-psb"></a>

<a id="trm-3-3-4"></a>

<a id="trm-3-3-4-1"></a>

## Fork

The child receives a copy of the parent's PSB with a single exception:
`process_guid` is not copied, and the child is given a new
kernel-generated one. <a id="cite-psb.fork.new-guid"></a> Everything else — the PIP fields, the
mitigations, and any active restrictions — is inherited, so a
Protected process's children start Protected and PIP propagates across
fork. <a id="cite-psb.fork.inherits-rest"></a>

The child also receives a new default process descriptor. Its owner is
the forking thread's **primary** token's user SID, not the
impersonation token's, even when the thread is impersonating at the
time. <a id="cite-psb.fork.sd-owner-primary-token"></a> The DACL follows the default template.

<a id="trm-3-3-4-2"></a>

## Exec

The PIP fields are reset at exec from the new binary's cryptographic
signature. A Protected parent that execs an unsigned binary loses PIP
protection: protection follows the binary, not the lineage. <a id="cite-psb.exec.pip-reset-from-binary"></a>

The mitigation flags — `lsv`, `wxp`, `tlp`, `cfif`, `cfib`, `pie`,
`sml`, `ui_access` — are not reset. They persist across exec
unchanged, so a mitigation set between fork and exec survives whatever
binary is subsequently loaded. <a id="cite-psb.exec.mitigations-persist"></a> `no_child_process` persists in the same
way: a process restricted from creating children stays restricted no
matter what it execs. <a id="cite-psb.exec.no-child-process-persists"></a>

`process_guid` is not reset either, because it identifies the process
— the scheduling entity — rather than the binary. <a id="cite-psb.exec.guid-preserved"></a>

The process descriptor is not reset. Exec preserves it unchanged. <a id="cite-psb.exec.sd-preserved"></a> It
was initialised at fork from the forking thread's primary token and
reflects the process creation context, or a later explicit management
context, rather than the binary being executed. Primary token
installation and the other explicit process-descriptor mutation paths
replace or modify it only under their own rules ([Token Lifecycle](<~kernel/internals/kacs/tokens/token-lifecycle#trm-3-2-3>)).

<a id="trm-3-3-4-3"></a>

## Clone with CLONE_THREAD

Threads share the process's PSB. <a id="cite-psb.clone-thread.shares-psb"></a> Thread creation is unaffected by
`no_child_process`, which blocks new processes only.

<a id="trm-3-3-4-4"></a>

## Relationship to AccessCheck

The PSB is not an input to AccessCheck in the general case. AccessCheck
takes a token and a descriptor and evaluates access; most PSB fields
are invisible to it.

PIP is the exception. The pipeline includes a PIP enforcement step
reading `pip_type` and `pip_trust`, which come from the PSB rather
than from any token: the enforcement layer extracts them and passes
them to AccessCheck as explicit parameters. <a id="cite-psb.accesscheck.pip-from-psb"></a>

The asymmetry between MIC and PIP follows from that. **MIC** uses the
effective token, so impersonation changes how it evaluates — which is
safe because the integrity ceiling on impersonation ([Impersonation Gates](<~kernel/internals/kacs/impersonation/levels-and-admission#trm-3-5-2>)) prevents
escalation. **PIP** uses the PSB, so impersonation cannot change how
it evaluates — necessary because there is no impersonation gate
constraining the PIP dimensions, making the PSB the only safe source.

The process mitigations and `no_child_process` do not interact with
AccessCheck at all. Each is enforced at its own enforcement point,
independently of the access control pipeline.
