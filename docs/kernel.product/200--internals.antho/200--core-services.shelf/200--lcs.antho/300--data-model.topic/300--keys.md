---
title: "Keys"
description: "A key is a container of subkeys and values — its identity, its properties, volatile keys, and the rules for naming one."
type: reference
---

<a id="trm-5-2-3"></a>

A key is a node in the hierarchy: a container holding subkeys and
values. The filesystem analogy is an inode. A key carries identity and
properties; naming lives in path entries ([Path Entries](<~kernel/internals/lcs/data-model/path-entries#trm-5-2-5>)).

| Field | Mutable | Layered | Description |
|---|---|---|---|
| GUID | No | No | Identity, assigned by LCS at creation, persisted by the source. |
| Name | No | No | The key's own name component. Informational; the path entry resolves the identity. `QUERY_KEY_INFO` preserves this spelling only when it folds to that resolved leaf, and audits and refuses a mismatch with `EIO`. <a id="cite-key.field.name-is-informational"></a> |
| Parent GUID | No | No | The parent key. Nil for a hive root. <a id="cite-key.field.parent-guid-nil-for-hive-root"></a> |
| Security Descriptor | Yes | No | Computed from the parent at creation; changed at runtime with `WRITE_DAC` / `WRITE_OWNER`. <a id="cite-key.field.security-descriptor-computed-from-parent"></a> |
| Last write time | Yes | No | Updated when a value is written or deleted or the descriptor changes. <a id="cite-key.field.last-write-time-updates"></a> |
| Volatile | No | No | The source stores this key in non-persistent storage only. |
| Symlink | No | No | This key is a symbolic link ([Symlinks](<~kernel/internals/lcs/data-model/symlinks#trm-5-2-4>)). |

**No key property is layer-qualified.** Properties belong to the object. <a id="cite-key.no-property-is-layer-qualified"></a>
Changing a key's structural type through a layer is not a matter of
setting a flag; the layer hides the original key and creates a new one
at the same path, which is the ordinary overlay pattern.

<a id="trm-5-2-3-1"></a>

## Identity

A key's identity is its GUID, not its path. Two keys occupying the same
path at different times are different objects with different GUIDs. <a id="cite-key.identity.is-guid-not-path"></a> A
path is a name that maps to an identity; the identity outlives the
name.

GUIDs are assigned by LCS — never by a source — and pushed to the
source at creation, where they become the primary key of its
storage. <a id="cite-key.identity.guid-assigned-by-lcs-not-source"></a>

Once a path has been resolved to a GUID at open time, every subsequent
RSI operation uses the GUID directly. <a id="cite-key.identity.rsi-uses-guid-after-open"></a>

The generator is the kernel's version-4 GUID generator: random bytes
from the kernel CSPRNG with the version and variant bits set in the
PCDS layout — the version nibble in the high nibble of byte 7, because
`Data3` is little-endian in bytes 6–7, and the variant bits in byte 8. <a id="cite-key.identity.guid-generator-is-uuidv4"></a>

Freshness is the collision resistance of UUIDv4 plus a check against
the keys LCS currently tracks, with a bounded retry. <a id="cite-key.identity.freshness-checked-against-tracked-keys"></a>

There is **no persistent retired-GUID catalogue**, and no code anywhere
that would maintain one. A GUID dropped by orphan cleanup is not
remembered. <a id="cite-key.identity.no-retired-guid-catalogue"></a>

If a source answers `RSI_CREATE_KEY` for a freshly generated GUID with
`RSI_ALREADY_EXISTS`, that is not a race to retry — the kernel believes
the GUID is unused and the source disagrees. LCS treats it as source
inconsistency and fails closed with `EIO`. <a id="cite-key.identity.create-key-already-exists-is-eio"></a>

It is never retried as an open and `EEXIST` never reaches userspace
from `reg_create_key`. <a id="cite-key.identity.no-eexist-from-reg-create-key"></a>

A GUID appears at exactly one canonical location. LCS validates that
and rejects a source that reports otherwise.

<a id="trm-5-2-3-2"></a>

## Volatile keys

Volatile is a flag LCS carries and forwards. Storing a volatile key in
non-persistent storage is the source's obligation; nothing in the
kernel enforces it. <a id="cite-key.volatile.storage-is-the-source-obligation"></a>

What the kernel does enforce is the containment rule: **a non-volatile
key may not be created under a volatile parent** (`EINVAL`). <a id="cite-key.volatile.non-volatile-under-volatile-parent-is-einval"></a>

The converse is allowed — a volatile key under a persistent parent is
ordinary. <a id="cite-key.volatile.volatile-under-persistent-parent-allowed"></a>

<a id="trm-5-2-3-3"></a>

## Naming

Three bytes are forbidden in a key name component: backslash and
forward slash, both of which are separators, and the null
byte. <a id="cite-key.name.three-forbidden-bytes"></a>

Every other valid UTF-8 sequence is permitted, spaces and arbitrary
Unicode included. <a id="cite-key.name.any-other-utf8-permitted"></a>

Empty components are forbidden, which rules out a leading separator and
consecutive separators (`Machine\\System`). <a id="cite-key.name.empty-components-forbidden"></a>

A trailing separator (`Machine\System\`) is likewise
invalid. <a id="cite-key.name.trailing-separator-invalid"></a>

Length limits are byte counts: `MaxPathComponentLength` per component,
`MaxTotalPathLength` for the whole path, `MaxKeyDepth` for nesting.

Forward slash normalisation is achieved by treating `/` as a separator
wherever a separator is recognised, rather than by rewriting the string
— so a materialised component never contains either separator, and the
canonical form is per-component rather than a canonicalised string.
