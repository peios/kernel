---
title: "The Origin Attribute"
description: "The one synthetic extended attribute that reveals which stratum provided a merged path — its value, constraints and access rules."
type: reference
---

<a id="trm-4-7"></a>

A merged path does not reveal which stratum provided it. stratafs
exposes that through one synthetic extended attribute,
`system.stratafs.origin`, and deliberately through nothing else — a
tool that instead re-implemented [Lookup](<~kernel/internals/stratafs/name-resolution/lookup-and-type-conflicts#trm-4-3-1>)'s resolution rules against the
strata would be a second implementation of them, and would eventually
disagree with the first.

Together with the mount table ([Mount Options](<~kernel/administration/stratafs/mount-options#trm-4-2-2>)), which gives the stratum stack,
it is enough to explain any path in a mount without privilege beyond
what reading the path itself requires.

<a id="trm-4-7-1"></a>

## The value

Reading the attribute returns the absolute path of the object that
provides it:

- For a **non-directory**, the provider's path in its stratum. <a id="cite-origin.value.non-directory"></a>
- For a **merged directory**, the paths of every participating
  directory in precedence order, separated by newlines. <a id="cite-origin.value.merged-directory"></a>

Each element is the stratum's own path, then a `/` where the relative
part is non-empty and the base does not already end in one, then the
relative path. <a id="cite-origin.value.element-format"></a> Within a path, a newline or a backslash is escaped by a
preceding backslash; those two are the whole escape set, and the `/`
stratafs itself inserts is not escaped. <a id="cite-origin.value.escaping"></a> Stratum paths are absolute
because the mount parser required them to be ([Mount Options](<~kernel/administration/stratafs/mount-options#trm-4-2-2>)).

There is no trailing newline and no trailing NUL. <a id="cite-origin.value.no-trailing-terminator"></a> A null buffer returns
the length required; an undersized one returns `ERANGE`. <a id="cite-origin.value.sizing"></a>

The value is synthesised at each read from the current resolution. It
is not stored, and it is not the value of any attribute on any stratum. <a id="cite-origin.value.synthesised-per-read"></a>
Because non-root dentries are always invalidated ([Revalidation](<~kernel/internals/stratafs/coherency/model-and-revalidation#trm-4-4-2>)), a read by
path always reflects a fresh resolution.

<a id="trm-4-7-2"></a>

## Constraints

The attribute is not settable. Any set or removal in the reserved
namespace fails with `EPERM`, before the provider is reached at all. <a id="cite-origin.not-settable"></a>

It is not reported by an attribute listing. The listing handler filters
reserved names out of both its sizing pass and its copy pass, and the
synthetic name is never added to any listing. <a id="cite-origin.hidden-from-listing"></a> Hiding it keeps
archivers, copy tools and backup software from discovering it,
attempting to preserve it, and failing.

The whole `system.stratafs.` namespace is reserved. No read, write or
removal of any name in it is forwarded to the provider: a read of any
name other than `origin` returns `ENODATA`, and a write or removal
returns `EPERM`. <a id="cite-origin.namespace-reserved"></a> Where a provider object carries a real attribute of
one of these names, it is masked — the synthesised value is returned
instead, and the provider's attribute is absent from listings through
the mount. <a id="cite-origin.masks-provider-attribute"></a>

Two details of the implementation are worth stating exactly. The
namespace test is a fixed-length prefix comparison against
`system.stratafs.` including the trailing dot, so the bare name
`system.stratafs` is *not* reserved and would be forwarded to the
provider. <a id="cite-origin.bare-name-not-reserved"></a> And the reserved set is one name wider than the namespace
suggests: the staging marker attribute,
`security.peios.stratafs_staging`, receives the same treatment —
`EPERM` to write, `ENODATA` to read, hidden from listings, masked from
providers — despite lying outside the `system.stratafs.` namespace. <a id="cite-origin.staging-marker-reserved"></a>

<a id="trm-4-7-3"></a>

## Access

Reading the attribute requires the access that reading an extended
attribute of the object requires, and is refused where that would be
refused. <a id="cite-origin.requires-read-ea"></a> The right to read the object's stat attributes is not
sufficient: the request is for the read-EA right, which KACS's
`getxattr` hook demands on the stratafs dentry before stratafs's own
handler runs.

For a merged directory the value names every participating directory,
so it discloses more than any one of them. Reading it requires that
access on **every** participating directory and is refused where any
refuses — the same intersection [Checks on Merged Directories](<~kernel/internals/stratafs/security/checks-on-merged-directories#trm-4-6-2>) applies to enumeration, and for
the same reason: a caller who may not know a restricted directory
participates must not learn it from this attribute. <a id="cite-origin.merged-requires-all-participants"></a>

Where the attribute is read **through a directory descriptor**, the
participating set is the one settled when that descriptor was opened
([Enumeration](<~kernel/internals/stratafs/name-resolution/enumeration#trm-4-3-4>)), and the value names that set rather than the current one. <a id="cite-origin.fd.settled-participant-set"></a> The
access decision was likewise made at open and is recorded on the
dentry, so the read consults a stored verdict rather than re-checking. <a id="cite-origin.fd.access-decided-at-open"></a>
A stratum that has joined since is not disclosed, because the check
that would have covered it was never run; a settled participant that
has since ceased to hold the directory is still named, for the same
reason.

Where it is read **by path**, the participating set is the current one,
resolved afresh, and the read-EA right is required against each of its
members at that moment. <a id="cite-origin.by-path.current-participant-set"></a>
