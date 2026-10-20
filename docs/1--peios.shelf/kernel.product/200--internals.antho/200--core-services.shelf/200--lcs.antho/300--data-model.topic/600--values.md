---
title: "Values"
description: "A named, typed datum inside a key — one name with many layer entries, the type set, REG_TOMBSTONE, naming and size."
type: reference
---

<a id="trm-5-2-6"></a>

A value is a named, typed datum inside a key. Values hold the
configuration data; keys hold values.

| Field | Description |
|---|---|
| Key GUID | The key this value belongs to. |
| Name | The value's name; the empty string is the default value. Case-preserving, compared case-insensitively. <a id="cite-value.field.empty-name-is-the-default-value"></a> |
| Type | A registry value type. |
| Data | An opaque byte array, up to `MaxValueSize` (default 1 MB). <a id="cite-value.field.data-bounded-by-max-value-size"></a> |
| Layer | The layer this entry belongs to. Every write is tagged. <a id="cite-value.field.every-write-is-layer-tagged"></a> |
| Sequence | Assigned by LCS at write time, for tiebreaking within a precedence tier. |

A key holds many values with distinct names, and at most one unnamed
one. <a id="cite-value.at-most-one-unnamed-value-per-key"></a>

<a id="trm-5-2-6-1"></a>

## One name, many entries

A single `(key GUID, value name)` pair can have several entries in the
source — one per layer that has written to it. <a id="cite-value.one-name-many-entries.one-entry-per-writing-layer"></a>

The source stores them all and returns them all. <a id="cite-value.one-name-many-entries.source-returns-every-entry"></a>

LCS resolves the effective value at read time ([Resolution](<~kernel/internals/lcs/layers/resolution#trm-5-3-6>)).

That is the mechanism that makes layer deletion revert configuration
automatically. Delete the layer, its entries go, and the
next-highest-precedence entry becomes effective. Nothing has to be
recomputed or rewritten.

<a id="trm-5-2-6-2"></a>

## Types

The full Windows type set is supported, for `registry.pol` fidelity:
`REG_NONE`, `REG_SZ`, `REG_EXPAND_SZ`, `REG_BINARY`, `REG_DWORD`,
`REG_DWORD_BIG_ENDIAN`, `REG_LINK`, `REG_MULTI_SZ`,
`REG_RESOURCE_LIST`, `REG_FULL_RESOURCE_DESCRIPTOR`,
`REG_RESOURCE_REQUIREMENTS_LIST` and `REG_QWORD`, numbered 0 to 11. <a id="cite-value.types.full-windows-set-numbered-0-to-11"></a>
Values are in [LCS ABI Reference](<~kernel/userspace/native/lcs/generated-syscall-and-common-abi#trm-5-a>).

LCS stores the type tag and returns it on read but does not interpret
the data. <a id="cite-value.types.tag-stored-and-returned-uninterpreted"></a> The single exception is `REG_LINK` read as a symlink key's
default value, which triggers target resolution ([Symlinks](<~kernel/internals/lcs/data-model/symlinks#trm-5-2-4>)).

The three hardware-resource types, 8 to 10, describe device resource
assignments in the Windows `HKLM\HARDWARE` hive, which the Windows
kernel rebuilds at every boot. Peios has no equivalent: hardware
enumeration belongs to the Linux device model, sysfs and `/proc/iomem`,
not to the registry. LCS accepts these tags only so a value carrying
one round-trips without loss. They have no semantics, LCS never
produces one, and for every operation they behave as `REG_BINARY`. <a id="cite-value.types.hardware-resource-types-behave-as-reg-binary"></a>
Rejecting a faithfully-copied value would break the fidelity guarantee
that is the reason the registry exists.

Type tags are validated at every write boundary, before sequence
allocation, transaction enlistment or source dispatch. An unknown code
is `EINVAL`. <a id="cite-value.types.unknown-type-code-is-einval"></a>

<a id="trm-5-2-6-3"></a>

## `REG_TOMBSTONE`

One further type, `REG_TOMBSTONE` (`0xFFFF`), is internal. It is never
returned to a caller reading a value — a caller whose effective entry
is a tombstone gets `ENOENT`, which is exactly what a tombstone
means. <a id="cite-value.reg-tombstone.never-returned-to-a-caller"></a>

There is no separate tombstone flag in the `REG_IOC_SET_VALUE`
argument. Writing type `REG_TOMBSTONE` **is** the explicit tombstone
operation. <a id="cite-value.reg-tombstone.written-by-setting-the-type"></a>

It must carry zero-length data; non-empty tombstone data is `EINVAL`,
again before sequence allocation, enlistment or dispatch. <a id="cite-value.reg-tombstone.non-empty-data-is-einval"></a>

<a id="trm-5-2-6-4"></a>

## Naming

Value names use the same case rules as key names: Unicode Simple Case
Folding, case-preserving, case-insensitive. <a id="cite-value.name.same-case-rules-as-key-names"></a>

They differ in one respect. **Backslash and forward slash are permitted
in a value name.** Value names are not hierarchical, so a separator has
no meaning in one. <a id="cite-value.name.separators-are-permitted"></a>

Only the null byte is forbidden, and invalid UTF-8 is rejected. The
empty string is reserved for the default value. <a id="cite-value.name.only-the-null-byte-is-forbidden"></a>

That difference is why watch event path components are length-prefixed
rather than joined by a separator ([Event Records](<~kernel/internals/lcs/watches/event-records#trm-5-6-2>)) — a value name can contain
the separator.

<a id="trm-5-2-6-5"></a>

## Size

`MaxValueSize` defaults to 1 MB and is configurable from 4 KB to 64 MB
([Operational Parameters](<~kernel/internals/lcs/bootstrap/operational-parameters#trm-5-10-3>)).

Value data is opaque bytes and is not subject to the UTF-8 validation
that applies to every string in the interface. <a id="cite-value.data.opaque-and-not-utf8-validated"></a>

<a id="trm-5-2-6-6"></a>

## Tool value encodings

`reg`, Registry Editor and the `peios` Rust crate use these representations:

- `REG_SZ` and `REG_EXPAND_SZ`: UTF-8 ending in one null byte, rather than
  Windows' UTF-16 representation.
- `REG_LINK`: the absolute target path in UTF-8, with no null byte. Its
  length determines its end; a target containing a null is not followed.
- `REG_MULTI_SZ`: each string followed by a null byte, with one additional
  null byte ending the list.
- Integers: little-endian, except for `REG_DWORD_BIG_ENDIAN`.

These are data conventions shared by tools. LCS still treats ordinary
value payloads as opaque bytes; its special handling of a link key's
`REG_LINK` default value is described in [Symlinks](<~kernel/internals/lcs/data-model/symlinks#trm-5-2-4>). For choosing and entering
a type as an operator, see
[Keys, values, and types](https://learn.peios.org/peios/using-peios/registry/reg/).
