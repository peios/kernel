---
title: "Checks on Merged Directories"
description: "An operation on a merged directory is checked against every participating directory — including where the create stratum's directory does not exist."
type: reference
---

<a id="trm-4-6-2"></a>

A merged directory stands for several real directories, each with its
own security descriptor. An operation on one is checked against every
participating directory whose contents it depends on, and against the
directory it modifies. Where more than one applies, **all** must
succeed: the check walks participants in order and returns on the first
refusal, and nothing degrades an operation to the subset of strata the
caller may reach.

Two composite rights recur:

- **Search** — traverse on every participating directory, since every
  one is searched to resolve a name. The permission hook maps the
  kernel's execute intent onto it. <a id="cite-security.merged-search-right"></a>
- **Enumerate** — Search plus list on every participating directory.
  The permission hook maps the read intent onto the list right, and
  directory open demands both together. <a id="cite-security.merged-enumerate-right"></a>

| Operation | Checked against |
|---|---|
| Resolving a name | Search <a id="cite-security.rights.resolve"></a> |
| Enumerating | Enumerate, before the listing is captured <a id="cite-security.rights.enumerate"></a> |
| Reading an object's attributes | Search, plus whatever the object's own descriptor requires <a id="cite-security.rights.read-attributes"></a> |
| Reading the origin attribute on a merged directory | Search, plus read-EA on **every** participant ([The Origin Attribute](<~kernel/internals/stratafs/start-here/the-origin-attribute#trm-4-7>)) <a id="cite-security.rights.read-origin"></a> |
| Creating a name | Search, plus add-file or add-subdirectory on the **create stratum's** directory <a id="cite-security.rights.create"></a> |
| Copy-up | Nothing beyond what the operation it serves already required <a id="cite-security.rights.copy-up"></a> |
| Removing a name | Search, plus delete-child on the **provider's** directory <a id="cite-security.rights.remove"></a> |
| Removing a directory | Enumerate — emptiness is judged across every participant — plus delete-child on the provider's directory <a id="cite-security.rights.rmdir"></a> |
| Rename, source | Search, plus delete-child on the source **provider's** directory <a id="cite-security.rights.rename-source"></a> |
| Rename, destination | Search, plus add-entry on the source provider's directory, which [Rename](<~kernel/internals/stratafs/mutation/rename#trm-4-5-5>) requires to hold the destination, plus delete-child where that directory already holds the name <a id="cite-security.rights.rename-destination"></a> |
| Rename of a directory | Both of the above, plus Enumerate on the object being renamed, and Enumerate on the destination where its provider is a directory <a id="cite-security.rights.rename-directory"></a> |
| `RENAME_EXCHANGE` | Search on both, plus add-entry and delete-child on the directory of the stratum providing both names <a id="cite-security.rights.rename-exchange"></a> |
| Link | Search on both, plus add-file on the source provider's directory <a id="cite-security.rights.link"></a> |
| Creating or linking an unnamed file | Search, plus add-file on the **create stratum's** directory <a id="cite-security.rights.unnamed-file"></a> |

The mutating rights land on the directory that actually changes, which
follows from [Write Routing](<~kernel/internals/stratafs/mutation/write-routing#trm-4-5-1>): an entry appears in the create stratum's directory
and disappears from the provider's, so in each case it is that
directory's descriptor that decides. The two coincide whenever the
create stratum is also the provider. <a id="cite-security.mutating-right-on-modified-directory"></a>

One right the table does not name is required anyway: the underlying
`vfs_link` makes KACS demand write-attributes on the **source object**,
which is an object-descriptor right outside the directory scope this
section covers. <a id="cite-security.link-requires-write-attributes-on-source"></a> Linking an unnamed file is exempt, since stratafs marks
the source for that purpose. <a id="cite-security.unnamed-link-exempt-from-source-check"></a>

The effective rights on a merged directory are therefore the
intersection of the rights on its participants, with mutating rights
additionally required on the directory that is actually modified.
Requiring the intersection is fail-closed and admits no partial
results: the alternative would let the names held by a restrictively
protected directory be enumerated by a caller who could not enumerate
it directly, because a permissive directory of higher precedence
happened to provide the merged path.

One consequence is worth stating plainly. Because creation is governed
by the create stratum's directory descriptor, and a created name
shadows the same name in every lower stratum, the right to create in
the create stratum's directory is the right to determine what every
lower stratum's entry of that name resolves to.

<a id="trm-4-6-2-1"></a>

## Where the create stratum's directory does not exist <a id="cite-security.create-check-falls-back-to-provider-directory"></a>

A merged directory has a create stratum whether or not that
subdirectory exists ([Directory Merge](<~kernel/internals/stratafs/name-resolution/directory-merge#trm-4-3-2>)), so a check naming "the create stratum's
directory" has to be evaluated against a directory that is not there
yet.

Every such check is performed before any part of the operation is
carried out, and in particular before any directory is materialised:
the authorisation call strictly precedes parent materialisation in
creation, in tmpfile creation, and in the unnamed-link path. Where the
checks fail, nothing has been created, so the create stratum is left
exactly as it was.

Where the create stratum does not hold the path, the check falls back
to the **corresponding provider directory** — the merged provider of
that same relative path — which is the descriptor the directory will
carry once materialised ([Descriptors on Copy-Up](<~kernel/internals/stratafs/security/copy-up-descriptors#trm-4-6-3>)). It is never skipped, and never
substituted with an ancestor's descriptor. Where no provider exists
either, the result is `EROFS`.

Materialising the intervening directories is part of the operation, not
a separate one. No per-ancestor authorisation is taken; the mkdirs are
exempted by the copy-up context. Checking against the descriptor the
directory will have keeps the answer independent of how much of the
create stratum happens to have been materialised already: the first
caller to write into a deep path and the hundredth face the same check,
against the same descriptor.

A create that fails *after* materialisation for a reason other than a
check — `EEXIST`, `ENOSPC` — does leave the intervening directories in
place.

<a id="trm-4-6-2-2"></a>

## Copy-up carries no separate authority <a id="cite-security.copy-up-requires-no-extra-right"></a>

A copy-up requires no right beyond those the operation that provoked it
already required. In particular it does not require the caller to hold
the right to read the provider's object, nor the right to add an entry
to the create stratum's directory. Neither copy-up path takes any
authorisation at all.

Copy-up is the mechanism by which an authorised modification is
realised, not an operation a caller requests. The read of the provider
is stratafs's own, and the copy carries the source's descriptor
unchanged ([Descriptors on Copy-Up](<~kernel/internals/stratafs/security/copy-up-descriptors#trm-4-6-3>)), so the caller obtains nothing they did not already
have: the same content, under the same descriptor, at the same path.

The alternative cannot be expressed. Routing happens when a
modification is performed ([Write Routing](<~kernel/internals/stratafs/mutation/write-routing#trm-4-5-1>)), and by then the authority that
governed the open is a mask cached on the descriptor, immutable and
carrying no token — so there is nothing to evaluate a fresh right
against. Checking the *acting* token instead would break descriptor
delegation, since a descriptor passed to another process would stop
working there.

What remains is a resource consideration rather than an access one: a
caller entitled to write a file in a stratum that will not accept
modification can cause an entry to appear in the create stratum without
holding rights over that directory. They gain neither access nor space
by it: [Durability and Accounting](<~kernel/internals/stratafs/mutation/durability-and-accounting#trm-4-5-8>) records that the copy is accounted to the preserved owner
rather than to them.

That exemption is only enforceable because KACS provides a copy-up
context; without it the access-control layer would check the caller
against the create stratum's directory at exactly the point where the
authority to check no longer exists. [The StrataFS Copy-Up Context](<~kernel/internals/stratafs/security/kacs-admission-and-object-phases#trm-3-9-7>) describes the context, its
phase binding and its exhaustive list of exempt operations. What
matters here is what stratafs must hold up its end of: the context
exempts caller authorisation only, so every mutation still goes through
the ordinary VFS path under write access on the target mount, a
read-only filesystem still refuses, and filesystem errors still
propagate. Nothing is performed under a borrowed or elevated identity —
every copy-up mutation runs with the calling task's own credentials.

<a id="trm-4-6-2-2-1"></a>

### Recovery retains the mounter’s file credentials <a id="cite-security.staging-recovery-uses-mounter"></a>

The stale-staging recovery scan passes the **mounter's** credentials
to the internal directory open, which retains them as the file’s
credentials. That does not switch the calling task’s current
credentials or select a different KACS token. The scan runs in a
source-read copy-up context bound to that exact directory, so the
context admits its read before an ordinary token access check.

Consequently, neither the caller nor the mounter needs a directory-list
grant for that scoped recovery read. An ordinary open requesting list
access remains subject to the directory’s descriptor. Path resolution
separately uses the captured mounter credentials; the file-credential
argument is not itself an authority switch.
