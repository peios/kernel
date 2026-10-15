---
title: "Signature verification"
description: "Signature verification: behaviour and implementation of the Peios kernel."
type: reference
---

<a id="trm-3-6"></a>

Binary signing is the foundation of PIP trust determination and of
Library Signature Verification. The kernel verifies cryptographic
signatures on executable files to establish their trust level, and
signing is the *only* mechanism by which a binary acquires PIP
protection — there is no runtime API that can confer it.

This section describes verification. The signature format itself, and
what a signer has to produce, are specified in PSPK's Binary Signing
and PIP chapter. The kernel only ever verifies; it holds no private
key and contains no signing primitive.

<a id="trm-3-6-1"></a>

## The key table

The kernel carries its verification keys in a dedicated data section
of the kernel image, as an array of 1960-byte entries — a raw
1952-byte ML-DSA-65 public key, then a `u32` little-endian PIP type,
then a `u32` little-endian PIP trust — terminated by an all-zero
entry. <a id="cite-sig.key-table.entry-layout"></a>

Before any cryptographic work, the whole table is walked and
validated. A table with no all-zero terminator is rejected with
`EINVAL`, and so is a table containing any entry whose tier is not
exactly Protected (512) with `PeiosTcb` trust (8192). <a id="cite-sig.key-table.validation-einval"></a> Both rejections
fail *every* verification on the system, which is what makes the
single-tier constraint absolute rather than conventional: a key at any
other tier does not merely fail to be honoured, it disables signing
entirely. <a id="cite-sig.key-table.invalid-disables-all"></a>

The consequence is that a verified binary is always Protected/8192. <a id="cite-sig.verified-always-protected-tcb"></a>
The Isolated type (1024) is reserved and unreachable, and the
multi-key, multi-tier model the table layout anticipates would need a
change to the validator, not merely an added key. <a id="cite-sig.isolated-type-unreachable"></a>

A build configured for KUnit compiles in a different, hard-coded key
at the same tier, taken from the test vector header. <a id="cite-sig.kunit-test-key"></a> Such a kernel
trusts a publicly known key.

`/sys/kernel/security/kacs/signing_keys` lists the table: one line for
each entry before the terminator, in table order, reading

```
key_sha256=<hex> pip_type=<u32> pip_trust=<u32>
```

where the key is named by the SHA-256 of its raw 1952-byte public key, in
lowercase hexadecimal, and the type and trust are the entry's own, in
decimal. <a id="cite-sig.key-table.securityfs-listing"></a> Entries are listed as they
are, whether or not the validator would accept them, so a table that
disables signing shows why. The keys are public, so reading the file is
not access-checked; whoever can open it can read it. Like every
securityfs object, it can be opened only once the mount has a
synthesising policy, which on Peios lets Authenticated Users in.
<a id="cite-sig.key-table.securityfs-unchecked"></a>

<a id="trm-3-6-2"></a>

## Finding a signature

Verification begins by recording the file's current size. Everything
that follows is bounded by that snapshot, and the size is re-read
before the attempt returns — a file that changed size mid-verification
invalidates the whole result. <a id="cite-sig.size-snapshot-revalidated"></a>

The first four bytes decide the path. A file matching `\x7fELF` takes
the ELF path; a file shorter than four bytes, or with different magic,
goes straight to the xattr. <a id="cite-sig.magic-selects-path"></a>

On the ELF path the kernel parses the header, locates the section
header table and the section-name string table, and scans sections in
index order for one named exactly `.peios.sig`. The match is over all
eleven bytes including the terminating NUL, so a longer name with that
prefix does not match. <a id="cite-sig.elf.section-name-exact-match"></a>

**Finding the section commits the ELF path.** The moment a section
header with that name is found, the xattr is no longer consulted —
whatever happens next. <a id="cite-sig.elf.section-commits-path"></a> A wrong section type, a size other than 3310, a
range outside the file, an allocation failure, a short read, a bad
version byte, or a hash failure all yield "unsigned" rather than
falling back. <a id="cite-sig.elf.section-failures-yield-unsigned"></a> This is deliberate: without it, an attacker could craft
a malformed ELF section to force fallback to whichever path they could
more easily control.

Several *structural* ELF failures commit the path too, before any
`.peios.sig` section has been seen: a file shorter than an ELF header,
a class other than `ELFCLASS64`, a byte order other than little-endian,
an unexpected ELF version, a section header entry size other than 64,
an absent or out-of-range section-name string table index, and a
section header table or string table lying outside the recorded size. <a id="cite-sig.elf.structural-failures-commit"></a>
A 32-bit or big-endian ELF therefore cannot carry an xattr signature
at all — it is committed to the ELF path and then fails on it. The one
structural case that does *not* commit is `e_shnum == 0`, so an ELF
with no section headers falls through to the xattr normally. <a id="cite-sig.elf.no-section-headers-falls-through"></a>

The xattr path reads `security.peios.sig` and requires exactly 3310
bytes; any other size is treated as unsigned. <a id="cite-sig.xattr.exact-size"></a> The read bypasses the
LSM xattr hooks, so FACS does not mediate the verifier's own read of
the signature. <a id="cite-sig.xattr.read-bypasses-lsm-hooks"></a>

<a id="trm-3-6-3"></a>

## Hashing and verification

The message signed is a 32-byte SHA-256 content hash, computed
differently depending on where the signature was found. For an ELF
section source, the hash covers the file with the section's *contents*
replaced by zeros — the `Elf64_Shdr` entry describing it is hashed
verbatim, along with everything else. <a id="cite-sig.hash.elf-section-zeroed"></a> For an xattr source the hash
covers the entire file with no exclusions, and that applies to ELF
files reaching the xattr path as well as to non-ELF ones. <a id="cite-sig.hash.xattr-covers-whole-file"></a> Hashing
proceeds in 4 KB chunks, with the zero run emitted in
`SHA256_BLOCK_SIZE` pieces.

The kernel then verifies the 3309-byte signature against each key in
the table, in order, returning on the first success. <a id="cite-sig.verify.exhaustive-trial-in-order"></a> There is no key
identifier in the blob, so key selection is exhaustive trial and the
cost is one ML-DSA verification per key. The trust tier is a property
of *which key verified*, never of anything the signer encoded. <a id="cite-sig.tier-from-key-not-blob"></a>

Verification uses the kernel crypto signature API with the `mldsa65`
algorithm. That API exposes no context parameter, so the empty FIPS
204 context is structurally guaranteed rather than checked — a
signature made under a non-empty context simply fails to verify. <a id="cite-sig.empty-fips204-context"></a>

<a id="trm-3-6-3-1"></a>

### When verification cannot be performed

"Did not verify" and "could not be verified" are different answers and
are kept apart. The per-key verifier is tri-state: verified, did not
verify, or a negative errno meaning the check could not be made — an
unavailable ML-DSA transform, or a key the transform will not accept. <a id="cite-sig.verifier.tri-state"></a>

A negative stops the search rather than trying the remaining keys: the
failure is in the machinery, and every remaining key would meet the same
one. It then propagates out of the exec path, which **refuses the exec**
with `EACCES`. <a id="cite-sig.unverifiable.exec-eacces"></a>

That asymmetry with the ordinary unsigned path is the point. An unsigned
binary runs with no integrity label, which is legitimate. Treating an
unverifiable one the same way removes PIP from every process the system
executes, and the result is indistinguishable from a correctly working
system that has no signed binaries — so nothing surfaces it until
signing is deployed, at which point it looks like the signing rollout
broke something.

On the LSV path the same condition denies the mapping, which already
fails closed. <a id="cite-sig.unverifiable.lsv-denies"></a>

<a id="trm-3-6-3-2"></a>

### The boot-time probe <a id="cite-sig.boot-probe"></a>

A `late_initcall` allocates the transform once and, if it cannot,
emits `pr_err` and a `kacs.signature.crypto.failed` KMES event
carrying `signature.crypto-stage` `boot-probe` and the error as
`outcome.errno`, negative. The condition is then visible at boot rather than
inferred from every process running without an integrity label.

It cannot refuse to start, and two things rule that out rather than one:

- At LSM init the algorithm is not yet registered, so `crypto_alloc_sig`
  returns `ENOENT` on every boot. A probe there would fire always.
- A non-zero return from an LSM's init function is only `WARN`'d
  (`security/lsm_init.c`, `lsm_init_single`). The hooks are never added,
  so "refuse to initialise" means running with no KACS at all — worse
  than the failure it would be preventing.

Enforcement therefore lives at exec, where refusing one exec is
recoverable in a way losing the integrity boundary is not.

The probe is not `IS_ENABLED(CONFIG_CRYPTO_MLDSA)`. That option is an
unconditional `select` under `SECURITY_PKM`, which is a `bool`, so a
config test would always pass and catch nothing. Only calling the
allocator sees the ordering failure.

<a id="trm-3-6-8"></a>

## Revocation <a id="cite-sig.no-revocation"></a>

There is none. A signed binary later found to be malicious cannot be
invalidated short of removing it from the filesystem or replacing the
kernel image with a different key. No hash blocklist, no per-key
revocation, and no revocation state of any kind exists.

## Related explanations

- [Exec and library integrity](<~kernel/internals/kacs/executable-trust/exec-and-library-integrity>)
- [Firmware verification](<~kernel/internals/kacs/executable-trust/firmware-verification>)
