---
title: "Validation"
description: "LCS validates every response before using it — malformed data against malformed protocol, and the asymmetric extensibility between them."
type: reference
---

<a id="trm-5-8-4"></a>

LCS validates every response before using it, and the failures split
into two categories with very different consequences. <a id="cite-source.validate.every-response-is-validated"></a>

<a id="trm-5-8-4-1"></a>

## Malformed data

The RSI message is structurally valid but its content is not: a
descriptor that will not parse, a value type that does not exist, a
sequence number that cannot be real, a metadata block that does not
cover the GUIDs it should.

- The request returns `EIO` to its caller. <a id="cite-source.validate.malformed-data-returns-eio"></a>
- An `lcs.source.response.rejected` audit event is emitted, naming the
  source slot and — where known — the hive, the request id, the
  operation code, the key GUID, and which of the twelve validation
  classes applies ([Audit](<~kernel/internals/lcs/security/audit#trm-5-4-4>)). <a id="cite-source.validate.malformed-data-emits-an-audit-event"></a>
- **The source stays alive.** Corruption may be localised, and one bad
  key is not a reason to take a hive offline. <a id="cite-source.validate.malformed-data-keeps-the-source-alive"></a>

What is checked, by category:

- **Security Descriptors**, from lookups and from layer metadata
  refreshes, must parse and must satisfy the ACE mask rules of [Access Rights](<~kernel/internals/lcs/security/access-rights#trm-5-4-2>). <a id="cite-source.validate.descriptors-must-parse"></a>
  A malformed layer metadata descriptor additionally leaves the
  previous known-good one cached ([Layer Metadata](<~kernel/internals/lcs/layers/layer-metadata#trm-5-3-3>)).
- **Names** — layer names, key and child names, value names — must be
  valid under the ordinary rules for their kind. <a id="cite-source.validate.names-must-be-valid"></a>
- **Sequence numbers** must be below the next number LCS would
  allocate, and must not duplicate at the same precedence in a way that
  would decide a winner ([Resolution](<~kernel/internals/lcs/layers/resolution#trm-5-3-6>)). <a id="cite-source.validate.sequence-number-checks"></a>
- **Payload shape** — an otherwise-matched response whose
  operation-specific payload is the wrong shape, carries trailing
  bytes, or encodes a path target invalidly. <a id="cite-source.validate.payload-shape-checks"></a>
- **Metadata closure** — a lookup or enumeration whose per-GUID
  metadata block has missing, duplicate, unreferenced or nil entries. <a id="cite-source.validate.metadata-closure-checks"></a>
  A HIDDEN entry must carry an all-zero GUID and contributes no
  metadata. <a id="cite-source.validate.hidden-entry-carries-a-zero-guid"></a>
- **Value payloads** — invalid types, a tombstone carrying data, data
  above `MaxValueSize`. <a id="cite-source.validate.value-payload-checks"></a>
- **Orphan lists** — a nil or duplicated GUID in an `RSI_DELETE_LAYER`
  response. <a id="cite-source.validate.orphan-list-checks"></a>
- **Status codes** outside the defined vocabulary. <a id="cite-source.validate.unknown-status-code"></a>

<a id="trm-5-8-4-2"></a>

## Malformed protocol

The message itself is structurally invalid: bad framing, a truncated
response, an unknown request id, a duplicate response, an operation
code that does not match the request.

This is treated as a source crash. The connection is torn down, the
in-flight table is destroyed with every waiter completed `EIO`, the
slot is marked Down, its hives become unavailable, and bound
transactions enter `SOURCE_DOWN`. <a id="cite-source.validate.malformed-protocol-is-treated-as-a-crash"></a>

There is one case where malformed *data* also takes the source down:
when the caller had already timed out and the operation was a commit or
a replayable mutation. At that point LCS cannot establish whether a
mutation was applied, and it cannot account for one it cannot describe
([Failure and Late Responses](<~kernel/internals/lcs/sources/failure-and-late-responses#trm-5-8-5>)).

<a id="trm-5-8-4-3"></a>

## Asymmetric extensibility

Requests and responses do not extend the same way.

A **request** may carry trailing fields a source does not recognise; a
source skips them using `total_len`. <a id="cite-source.validate.requests-may-carry-trailing-fields"></a> That is how a new optional field
is added without an RSI version bump.

A **response** may not. LCS rejects any trailing bytes in a response
payload as malformed data. Forward compatibility on the response side
comes from new operations, not from extending existing payloads.
