---
title: "Mount options"
description: "The single filesystem-specific mount parameter stratafs registers, its escaping and parse failures, generic flags, and remount."
type: reference
---

<a id="trm-4-2-2"></a>

stratafs registers exactly one filesystem-specific mount parameter,
`strata`, and rejects every other name. <a id="cite-mount.only-strata-option"></a> There is no option to select a
security descriptor, an access-check behaviour, an inode-numbering
scheme, or a caching mode.

```
strata=<stratum>[:<stratum>]...
<stratum> := <path>[+<flag>]...
<flag>    := create | ro | am
```

Strata are separated by `:` and given highest-precedence first. Each
stratum is an absolute path, optionally followed by flags, each
introduced by `+`. <a id="cite-mount.strata-option-syntax"></a>

```
strata=/system/retc:/lcl/etc+create:/usr/etc+ro
```

`:` separates strata rather than `,` because a mount options string is
itself comma-separated when passed through the legacy mount interface,
which would otherwise split the value.

<a id="trm-4-2-2-1"></a>

## Escaping <a id="cite-mount.escape-set"></a>

Within a path, a literal `:`, `+`, `,` or `\` is escaped by a preceding
`\`. Those four characters are the entire escapable set; the escaped
byte is stored literally, and the backslash is consumed.

Because the legacy `mount(2)` data is one comma-separated string,
stratafs replaces the VFS's monolithic option splitter with one that
honours backslash escapes, so that an escaped comma inside a stratum
path survives the split rather than being read as an option boundary.

<a id="trm-4-2-2-2"></a>

## Parse failures

Every malformed value is refused with `EINVAL`. The parser consumes the
whole string and errors on any byte it cannot classify; there is no
skip-and-continue path, so nothing it does not understand is silently
ignored. <a id="cite-mount.parse-failure-einval"></a>

| Condition | |
|---|---|
| The `strata=` option is absent | There is no default stack <a id="cite-mount.parse.strata-absent"></a> |
| Its value is empty | <a id="cite-mount.parse.empty-value"></a> |
| An element between two separators is empty, or the value begins or ends with a separator | <a id="cite-mount.parse.empty-element"></a> |
| A path is not absolute | Tested on the raw first byte, which is exact since `/` is not escapable <a id="cite-mount.parse.path-must-be-absolute"></a> |
| A path is empty after unescaping | Defensive; the absolute-path test already guarantees one byte <a id="cite-mount.parse.empty-after-unescape"></a> |
| An unescaped `,` appears in a path, or inside a flag token | The option string is comma-separated at the outer level <a id="cite-mount.parse.unescaped-comma"></a> |
| A `\` appears at the end of the value, or before a character that is not `:`, `+`, `,` or `\` | A dangling or meaningless escape <a id="cite-mount.parse.invalid-escape"></a> |
| A `+` is followed by no flag, or by an unrecognised one | Flag names are matched by exact length and content <a id="cite-mount.parse.unknown-flag"></a> |
| The same flag appears more than once on one stratum | <a id="cite-mount.parse.duplicate-flag"></a> |
| More than 16 strata | The array bound is reached mid-parse <a id="cite-mount.parse.too-many-strata"></a> |
| `strata=` appears twice in one option string | <a id="cite-mount.parse.duplicate-strata-option"></a> |

Two paths return `ENOMEM` rather than `EINVAL`, both allocation
failures during parsing. Nothing bounds a stratum path at parse time:
an over-long one is accepted here and fails later with `ENAMETOOLONG`
when the joined path exceeds `PATH_MAX` during a resolution. <a id="cite-mount.overlong-path-enametoolong"></a>

The stack-wide conditions — an empty stack, two `create` strata, a
stratum carrying both `create` and `ro` — are checked separately, after
parsing and before any path is resolved. They depend on nothing but the
option string, so they are reported whatever the caller's access
([Mount Admission](<~kernel/internals/stratafs/strata-and-mounting/mount-admission#trm-4-2-3>)).

<a id="trm-4-2-2-3"></a>

## Generic mount flags <a id="cite-mount.read-only-refuses-all-mutation"></a>

Generic flags apply as they do to any filesystem, with one addition. A
stratafs mount may be mounted read-only, and the superblock's read-only
state is the **first** term of the routing decision, short-circuiting
before the provider or the create stratum is considered at all. It
therefore refuses every mutation with `EROFS` regardless of the stratum
stack, and is both independent of and stricter than a stack with no
create stratum.

<a id="trm-4-2-2-3-1"></a>

### Locking and synchronising a read-only mount <a id="cite-mount.locking-unaffected-by-read-only"></a>

Locking and synchronising are unaffected. Neither modifies an object,
neither consults the superblock's read-only state, and a reader of a
merged tree may need both.

<a id="trm-4-2-2-4"></a>

## Remount <a id="cite-mount.remount-rejects-a-changed-stack"></a>

A remount may alter generic mount flags. It may not alter the stack: a
remount supplying a `strata=` whose value differs from the mounted
one's is refused with `EINVAL`.

The test is on the value, not on the presence of the parameter, so a
remount that replays the current stack byte-for-byte is accepted — it
adds, removes, reorders and re-flags nothing. <a id="cite-mount.remount-accepts-an-identical-stack"></a> That is what makes
option-string replay work: a tool reconstructing the whole option
string from the mount table and handing it back is doing exactly this,
and flipping a stratafs mount read-only would otherwise fail on a
`strata=` that changed nothing.

The comparison is of the stored option string ([Mount Options](<~kernel/administration/stratafs/mount-options#trm-4-2-2>), below), which is
why that string being reported without a second escaping layer is what
lets a replayed stack compare equal at all.

<a id="trm-4-2-2-5"></a>

## The mount table <a id="cite-mount.options-reported-verbatim"></a>

The stack is reported in the filesystem options the kernel exposes for
mounts, so it is discoverable by anything that can read the mount
table, which on Linux is unprivileged. What is stored for this purpose
is the caller's own option string, kept verbatim at parse time: nothing
is abbreviated, no stratum is omitted, no path is canonicalised, and an
absent stratum is reported like any other, because the string is fixed
at mount and never filtered by what currently exists.

The filesystem type is reported as `stratafs`.

The value is emitted through the kernel's `seq_show_option`, which
applies its own escaping — octal for `,`, `\`, and whitespace — on top
of the escaping the value already carries. For a path containing none
of `: + , \` or whitespace, which is the ordinary case, the reported
value is byte-identical to what was supplied. For a path containing any
of them it is not reconstructable: a stored `\:` is re-escaped to
`\134:`, which reads back as a dangling escape. This is tracked as a
defect.
