---
title: "Exec and library integrity"
description: "Exec and library integrity: behaviour and implementation of the Peios kernel."
type: reference
---

<a id="trm-3-6-4"></a>

## PIP determination at exec

At `execve()` the kernel looks up and verifies the signature as above.
A verified binary takes `pip_type` and `pip_trust` from the matched
key; no signature, an invalid or unstable one, a bad signature, or no
matching key all yield None/0. <a id="cite-sig.exec.tier-from-matched-key"></a>

**Exec proceeds in every case where the question could be answered.** <a id="cite-sig.exec.proceeds-regardless"></a>
PIP is additive protection, not an execution gate: it determines trust
level, not permission to run. The one exception is a signature that
could not be verified at all, described above, which refuses the exec —
because there the question was not answered, so there is no basis on
which to assign a trust level. An
attacker who replaces a signed binary's signature with garbage costs
it PIP protection but can still execute it, subject to FACS. The
asymmetry with LSV — which *does* block unsigned libraries — is
intentional. Exec is permissive; `mmap(PROT_EXEC)` is restrictive.

Determination is transactional with exec success, in three phases. The
pending value is cleared at the top of every `bprm_creds_from_file`
invocation, staged into the task's security blob, and committed to the
process state only from `bprm_committed_creds`. <a id="cite-sig.exec.stage-then-commit"></a> An exec that fails
between staging and commit leaves the process state untouched, and the
stale pending value is cleared by the next exec or at task teardown. <a id="cite-sig.exec.failed-exec-leaves-state"></a>

Because the hook fires once per binfmt iteration and each iteration
re-stages, a `#!` script's PIP comes from the **interpreter** — the
last file processed — not from the script. <a id="cite-sig.exec.shebang-takes-interpreter"></a> A TCB-signed interpreter
runs at TCB level whatever script it executes. Symlinks need no
special handling either: the LSM hooks receive the already-resolved
target file, so a symlink inherits its target's level by construction. <a id="cite-sig.exec.symlink-resolves-to-target"></a>

Once committed, the values are fixed for the lifetime of the process
image, inherited at fork, and re-derived at the child's exec. <a id="cite-sig.exec.fixed-and-inherited"></a>

<a id="trm-3-6-5"></a>

## Content pinning

A binary that verifies to a nonzero tier has its backing inode pinned
as KACS-verified executable content before the exec result is
committed, and LSV pins on success too, before allowing the mapping. <a id="cite-sig.pin.on-verified-exec-and-lsv"></a>
Pinning closes the gap between verifying one byte image and modifying
the same inode afterwards.

If pinning fails at exec, the PIP result is **downgraded to None/0**
rather than the exec being failed or the tier being kept — the process
runs unprotected. <a id="cite-sig.pin.failure-downgrades-to-none"></a> Under LSV a pin failure denies the mapping instead. <a id="cite-sig.pin.failure-denies-lsv-mapping"></a>

A pinned inode rejects in-place content mutation even when the size
would be preserved: ordinary, positioned and append writes;
`ftruncate()` and pathname `truncate()`; and every `fallocate` mode,
including allocation-only ones, because the pin check runs before and
independently of the mode-support test. <a id="cite-sig.pin.rejects-content-mutation"></a> File ioctls that mutate
content, ranges, or allocation are rejected, and so are ioctls the
kernel cannot classify — unknown ioctls fail closed on a pinned inode. <a id="cite-sig.pin.unknown-ioctl-fails-closed"></a>
Mutation or removal of the `security.peios.sig` xattr is rejected as
well. <a id="cite-sig.pin.rejects-sig-xattr-mutation"></a>

The pin is conservative and one-way. It is set once and cleared only
when the inode is allocated or freed, never while the inode is live. <a id="cite-sig.pin.cleared-only-at-inode-lifecycle"></a>
Updating verified executable content therefore means replacing the
inode — write a new file and `rename()` over it — rather than
modifying it in place.

Unsigned, invalid, unstable, bad-signature and no-match attempts never
pin. <a id="cite-sig.pin.only-on-verified"></a>

<a id="trm-3-6-6"></a>

## Library Signature Verification

With the `lsv` mitigation enabled, `mmap()` with `PROT_EXEC` on a
file-backed mapping verifies the backing file. An unsigned file, an
invalid or unstable one, a bad signature, or no matching key all deny
the mapping with `EACCES`. <a id="cite-sig.lsv.denies-unsigned-eacces"></a> On success the library's tier is compared
against the loading process's: the image has to dominate the process,
so a Protected/PeiosTcb process can load only PeiosTcb-or-above
libraries. <a id="cite-sig.lsv.image-must-dominate-process"></a> With one key in the table this reduces to "is it signed
with the TCB key?"

The hash covers the **entire file**, not the mapped region — the whole
file is read and hashed even when only part of it is being mapped, so
the signature covers code in sections this particular mapping does not
touch. <a id="cite-sig.lsv.hashes-whole-file"></a>

`mprotect()` adding `PROT_EXEC` to a mapping that was not already
executable runs the same checks in a fixed order: WXP, then TLP, then
LSV. <a id="cite-sig.lsv.mprotect-check-order"></a> Anonymous mappings have neither a path nor a signature, so TLP
and LSV skip them and only WXP applies. <a id="cite-sig.lsv.anonymous-skips-tlp-lsv"></a>

Enabling `lsv` on a running process also re-validates its existing
executable mappings before the bit is committed ([PSB Fields](<~kernel/internals/kacs/process-security/psb-fields#trm-3-3-2>)), so the
mitigation cannot be turned on over already-mapped unsigned code.

<a id="trm-3-6-9"></a>

## Interaction with other mechanisms

**WXP** is orthogonal: it prevents pages being writable and executable
at once, while LSV prevents unsigned executable pages. A process with
both can execute only signed code in read-only pages.

**FACS** runs independently. A signed binary in a directory the caller
cannot reach is still unreachable — the open is denied before signing
is consulted. <a id="cite-sig.facs.open-denied-before-signing"></a> Signing determines the PIP level of a binary that is
already being executed; it never grants access to one.

**PIP object protection** consumes the result: once a process carries
a tier from its binary's signature, trust labels on objects are
enforced through the AccessCheck pipeline against the `pip_type` and
`pip_trust` held in the PSB ([Process Integrity Protection](<~kernel/internals/kacs/executable-trust/process-integrity-protection#trm-3-7>)).
