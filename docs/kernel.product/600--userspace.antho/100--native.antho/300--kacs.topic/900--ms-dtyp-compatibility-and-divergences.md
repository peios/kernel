---
title: "MS-DTYP compatibility and divergences"
description: "Where KACS departs from MS-DTYP despite using its binary formats, and which features are handled elsewhere rather than here."
type: reference
---

<a id="trm-3-b"></a>

KACS uses the binary formats MS-DTYP specifies, so a descriptor
authored by a Windows domain controller and replicated through Samba
is evaluated without translation. <a id="cite-dtyp.binary-formats-untranslated"></a> PCDS specifies those formats
normatively.

Evaluator behaviour is a separate question. Given the same token,
descriptor and desired mask, KACS generally reaches the same decision
MS-DTYP describes — which is what makes policy authored in an AD
environment behave predictably here — but it departs deliberately in
the following places.

| Area | Departure | Why |
|---|---|---|
| Conditional ACE `@Local.` | Resolved from an AccessCheck parameter rather than a token field | The context is per-call and varies between checks. <a id="cite-dtyp.local-from-accesscheck-parameter"></a> |
| Virtual groups in expressions | `Member_of({S-1-3-4})` returns true for the owner | Keeps the SID matcher and the expression evaluator semantically consistent. <a id="cite-dtyp.member-of-owner-virtual-group"></a> |
| INT64/UINT64 promotion | Relational operators promote between the two | Without promotion, `UINT64` claims cannot be used in conditions at all. <a id="cite-dtyp.int64-uint64-promotion"></a> |
| `Member_of` filtering | Filtered by ACE polarity, so deny-only groups do not satisfy allow-ACE conditions | Consistent with deny-only group semantics everywhere else. <a id="cite-dtyp.member-of-ace-polarity"></a> |
| `Exists` scope | Extended to all four attribute namespaces | No reason to restrict existence tests to Local and Resource. <a id="cite-dtyp.exists-all-namespaces"></a> |
| ACE mask mapping | ACE masks are mapped through GenericMapping at evaluation time | Required for `GENERIC_ALL` in central access policy recovery ACEs ([Central Access and Auditing Policy](<~kernel/internals/kacs/access-check/central-access-and-auditing-policy#trm-3-8-8>)). <a id="cite-dtyp.ace-mask-generic-mapping"></a> |
| `MAXIMUM_ALLOWED` | First-writer-wins for targeted *and* maximum-allowed requests | Eliminates disagreement between "what can I do?" and "can I do this?" on a non-canonically ordered DACL. <a id="cite-dtyp.maximum-allowed-first-writer-wins"></a> |
| Zero desired mask | Succeeds rather than returning access denied | "Asked for nothing, got nothing" is a valid answer. <a id="cite-dtyp.zero-desired-mask-succeeds"></a> |
| Alarm ACEs | Repurposed for continuous per-operation auditing, recorded as `kacs.audit.handle.used` ([Auditing in AccessCheck](<~kernel/internals/kacs/access-check/auditing-in-accesscheck#trm-3-8-9>)) | Reserved but never implemented in the reference model. <a id="cite-dtyp.alarm-ace-continuous-audit"></a> |
| Multiple scoped policy ACEs | Several permitted per SACL | AND semantics make composition safe. <a id="cite-dtyp.multiple-scoped-policy-aces"></a> |
| Mandatory policy mutability | `mandatory_policy` is immutable on the token ([Token Structure](<~kernel/internals/kacs/tokens/token-structure#trm-3-2-2>)) | A mutable policy reduces MIC to advisory. <a id="cite-dtyp.mandatory-policy-immutable"></a> |
| Impersonation integrity ceiling | Enforced unconditionally; `SeImpersonatePrivilege` does not bypass it ([Impersonation Gates](<~kernel/internals/kacs/impersonation/levels-and-admission#trm-3-5-2>)) | MIC is a real boundary precisely because the mandatory policy is immutable. <a id="cite-dtyp.impersonation-ceiling-unconditional"></a> |
| Impersonation origin check | Dropped | Eliminates hidden impersonation paths. <a id="cite-dtyp.impersonation-origin-check-dropped"></a> |
| Impersonation level on primaries | Meaningful and queryable: a ratchet every token carries, bounding everything derived from it ([Impersonation Levels](<~kernel/internals/kacs/impersonation/levels-and-admission#trm-3-5-1>)). Windows rejects `TokenImpersonationLevel` on a primary. | Delegation here is a flag authd enforces rather than a property of the credential cache, so the flag itself has to be unforgeable across duplication. <a id="cite-dtyp.impersonation-level-on-primaries"></a> |
| PIP determination | Kernel-only, from the binary signature, with no parent input ([PSB Fields](<~kernel/internals/kacs/process-security/psb-fields#trm-3-3-2>)) | One input, one answer, no ambiguity. <a id="cite-dtyp.pip-kernel-only-determination"></a> |
| Object type list validation | Duplicate GUIDs and level gaps rejected ([Object ACEs and Property-Level Access](<~kernel/internals/kacs/access-check/object-aces-and-property-level-access#trm-3-8-5>)) | Prevents node lookup returning the wrong node and propagation becoming undefined. <a id="cite-dtyp.object-type-list-validation"></a> |
| Object type list depth | No limit on levels; the tree is bounded only by the node count the access-check interface accepts. MS-DTYP limits a list to four levels. | A depth limit would reject lists the validation rules already make well-defined, and nothing in propagation depends on depth. <a id="cite-dtyp.object-type-list-no-level-limit"></a> |

<a id="trm-3-b-1"></a>

## Features handled elsewhere

Several capabilities relevant to a complete security posture are not
KACS's, and are named here so their absence is not mistaken for a gap.
Kerberos and NTLM authentication, S4U, and credential storage and
protection belong to authd, as do Resource-Based Constrained
Delegation and Authentication Policies and Silos through the KDC.
Active Directory replication is Samba's. Group Policy distribution
goes through the registry and roles. Network share permissions belong
to the Samba SMB layer. An Encrypting File System is a future service.
