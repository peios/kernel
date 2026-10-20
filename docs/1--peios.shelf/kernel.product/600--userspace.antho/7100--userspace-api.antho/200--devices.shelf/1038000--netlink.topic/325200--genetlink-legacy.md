---
title: "Netlink specification support for legacy Generic Netlink families"
type: reference
description: "This document describes the many additional quirks and properties required to describe older Generic Netlink families which form the genetlink-legacy protocol level."
---

<a id="rst-netlink-specification-support-for-legacy-generic-netlink-families"></a>

<!-- SPDX-License-Identifier: BSD-3-Clause -->

This document describes the many additional quirks and properties required to describe older Generic Netlink families which form the `genetlink-legacy` protocol level.

<a id="rst-specification"></a>

## Specification

<a id="rst-globals"></a>

### Globals

Attributes listed directly at the root level of the spec file.

<a id="rst-version"></a>

#### version

Generic Netlink family version, default is 1.

`version` has historically been used to introduce family changes which may break backwards compatibility. Since compatibility breaking changes are generally not allowed `version` is very rarely used.

<a id="rst-attribute-type-nests"></a>

### Attribute type nests

New Netlink families should use `multi-attr` to define arrays. Older families (e.g. `genetlink` control family) attempted to define array types reusing attribute type to carry information.

For reference the `multi-attr` array may look like this:



```text
[ARRAY-ATTR]
  [INDEX (optionally)]
  [MEMBER1]
  [MEMBER2]
[SOME-OTHER-ATTR]
[ARRAY-ATTR]
  [INDEX (optionally)]
  [MEMBER1]
  [MEMBER2]
```

where `ARRAY-ATTR` is the array entry type.

<a id="rst-indexed-array"></a>

#### indexed-array

`indexed-array` wraps the entire array in an extra attribute (hence limiting its size to 64kB). The `ENTRY` nests are special and have the index of the entry as their type instead of normal attribute type.

A `sub-type` is needed to describe what type in the `ENTRY`. A `nest` `sub-type` means there are nest arrays in the `ENTRY`, with the structure looks like:



```text
[SOME-OTHER-ATTR]
[ARRAY-ATTR]
  [ENTRY]
    [MEMBER1]
    [MEMBER2]
  [ENTRY]
    [MEMBER1]
    [MEMBER2]
```

Other `sub-type` like `u32` means there is only one member as described in `sub-type` in the `ENTRY`. The structure looks like:



```text
[SOME-OTHER-ATTR]
[ARRAY-ATTR]
  [ENTRY u32]
  [ENTRY u32]
```

<a id="rst-type-value"></a>

#### type-value

`type-value` is a construct which uses attribute types to carry information about a single object (often used when array is dumped entry-by-entry).

`type-value` can have multiple levels of nesting, for example genetlink's policy dumps create the following structures:



```text
[POLICY-IDX]
  [ATTR-IDX]
    [POLICY-INFO-ATTR1]
    [POLICY-INFO-ATTR2]
```

Where the first level of nest has the policy index as it's attribute type, it contains a single nest which has the attribute index as its type. Inside the attr-index nest are the policy attributes. Modern Netlink families should have instead defined this as a flat structure, the nesting serves no good purpose here.

<a id="rst-operations"></a>

## Operations

<a id="rst-enum-message-id-model"></a>

### Enum (message ID) model

<a id="rst-unified"></a>

#### unified

Modern families use the `unified` message ID model, which uses a single enumeration for all messages within family. Requests and responses share the same message ID. Notifications have separate IDs from the same space. For example given the following list of operations:



```yaml
-
  name: a
  value: 1
  do: ...
-
  name: b
  do: ...
-
  name: c
  value: 4
  notify: a
-
  name: d
  do: ...
```

Requests and responses for operation `a` will have the ID of 1, the requests and responses of `b` - 2 (since there is no explicit `value` it's previous operation `+ 1`). Notification `c` will use the ID of 4, operation `d` 5 etc.

<a id="rst-directional"></a>

#### directional

The `directional` model splits the ID assignment by the direction of the message. Messages from and to the kernel can't be confused with each other so this conserves the ID space (at the cost of making the programming more cumbersome).

In this case `value` attribute should be specified in the `request` `reply` sections of the operations (if an operation has both `do` and `dump` the IDs are shared, `value` should be set in `do`). For notifications the `value` is provided at the op level but it only allocates a `reply` (i.e. a "from-kernel" ID). Let's look at an example:



```yaml
-
  name: a
  do:
    request:
      value: 2
      attributes: ...
    reply:
      value: 1
      attributes: ...
-
  name: b
  notify: a
-
  name: c
  notify: a
  value: 7
-
  name: d
  do: ...
```

In this case `a` will use 2 when sending the message to the kernel and expects message with ID 1 in response. Notification `b` allocates a "from-kernel" ID which is 2. `c` allocates "from-kernel" ID of 7. If operation `d` does not set `values` explicitly in the spec it will be allocated 3 for the request (`a` is the previous operation with a request section and the value of 2) and 8 for response (`c` is the previous operation in the "from-kernel" direction).

<a id="rst-other-quirks"></a>

## Other quirks

<a id="rst-structures"></a>

### Structures

Legacy families can define C structures both to be used as the contents of an attribute and as a fixed message header. Structures are defined in `definitions`  and referenced in operations or attributes.

<a id="rst-members"></a>

#### members

> - `name` - The attribute name of the struct member
>
> - `type` - One of the scalar types `u8`, `u16`, `u32`, `u64`, `s8`, `s16`, `s32`, `s64`, `string`, `binary` or `bitfield32`.
>
> - `byte-order` - `big-endian` or `little-endian`
>
> - `doc`, `enum`, `enum-as-flags`, `display-hint` - Same as for [attribute definitions](<~kernel/userspace/userspace-api/netlink/specs#rst-attribute-properties>)

Note that structures defined in YAML are implicitly packed according to C conventions. For example, the following struct is 4 bytes, not 6 bytes:



```c
struct {
        u8 a;
        u16 b;
        u8 c;
}
```

Any padding must be explicitly added and C-like languages should infer the need for explicit padding from whether the members are naturally aligned.

Here is the struct definition from above, declared in YAML:



```yaml
definitions:
  -
    name: message-header
    type: struct
    members:
      -
        name: a
        type: u8
      -
        name: b
        type: u16
      -
        name: c
        type: u8
```

<a id="rst-fixed-headers"></a>

#### Fixed Headers

Fixed message headers can be added to operations using `fixed-header`. The default `fixed-header` can be set in `operations` and it can be set or overridden for each operation.



```yaml
operations:
  fixed-header: message-header
  list:
    -
      name: get
      fixed-header: custom-header
      attribute-set: message-attrs
```

<a id="rst-attributes"></a>

#### Attributes

A `binary` attribute can be interpreted as a C structure using a `struct` property with the name of the structure definition. The `struct` property implies `sub-type: struct` so it is not necessary to specify a sub-type.



```yaml
attribute-sets:
  -
    name: stats-attrs
    attributes:
      -
        name: stats
        type: binary
        struct: vport-stats
```

<a id="rst-c-arrays"></a>

### C Arrays

Legacy families also use `binary` attributes to encapsulate C arrays. The `sub-type` is used to identify the type of scalar to extract.



```yaml
attributes:
  -
    name: ports
    type: binary
    sub-type: u32
```

<a id="rst-multi-message-do"></a>

### Multi-message DO

New Netlink families should never respond to a DO operation with multiple replies, with `NLM_F_MULTI` set. Use a filtered dump instead.

At the spec level we can define a `dumps` property for the `do`, perhaps with values of `combine` and `multi-object` depending on how the parsing should be implemented (parse into a single reply vs list of objects i.e. pretty much a dump).
