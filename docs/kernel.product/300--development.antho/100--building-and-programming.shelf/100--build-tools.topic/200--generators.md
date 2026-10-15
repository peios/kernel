---
title: "Data generators"
type: guide
description: "Maintain checked-in event tables, registry seeds, Unicode folding tables and signing test fixtures."
---

Run commands from the kernel repository root. Generated outputs are reviewed
alongside their source inputs; a check command should not replace them.

## KMES event tables

Edit the kernel event catalogue in `peios/packages/data/evman/*.evman`, then run:

```sh
./peios/bazel run //:generate-kmes-events
./peios/bazel test //:kmes-event-table-test
```

The generator writes `security/pkm/kmes/event_types.h` and `event_types.rs`.
Commit the catalogue and generated tables together. It preserves matching C/Rust
IDs, event names, tiers, default enablement and the registry-policy lookup tree.
IDs are kernel-internal; event records carry names. The current enabled mask
supports at most 64 event types, and generation rejects a larger catalogue.

The test checks for stale tables without rewriting them and exercises generator
validation. CI runs it alongside the style, Cargo and ABI checks. Python 3.11 or
newer can also run `python3 peios/gen-kmes-event-table.py` directly; add `--check`
for read-only drift detection. No old PKM checkout is required.

## Port-reservation seed

`peios/gen-port-reservations-seed.py` regenerates the security descriptors in
`peios/packages/data/regim/port-reservations.reg`. It derives the `bindLowPorts`
capability SID and emits the `PORT_BIND | READ_CONTROL` grants for the existing
seed entries. The registry file must already exist; this updates its descriptors
and capability comment rather than creating a registry tree from nothing.

```sh
./peios/bazel run //:generate-port-seed
python3 peios/gen-port-reservations-seed.py --check
./peios/bazel test //:data-generator-tests
```

The Python entry point also accepts `--output PATH` for an existing seed file.
`--check` reports drift and exits unsuccessfully without rewriting it.

## Unicode case-folding tables

`peios/generate-casefold-table.py` reads a supplied Unicode `CaseFolding.txt`.
It requires `--input` and at least one of `--out` (Rust) or `--go-out` (Go).
The maintained input version is Unicode 16.0.0, with SHA-256
`6f1f9c588eb4a5c718d9e8f93b782685e5c7fec872cf05e8e6878053599e09bb`.
The generator records the input hash; it does not fetch or enforce that pin.

```sh
python3 peios/generate-casefold-table.py \
    --input /path/to/CaseFolding.txt --unicode-version 16.0.0 \
    --out security/pkm/lcs/lcs_core/casefold_table.rs \
    --go-out /path/to/loregd/internal/fold/casefold_table.go
```

Choose the Go destination in the maintained loregd checkout and update both
consumers from the same input. There is no `--check` mode: generate into temporary
files for comparison when reviewing drift. The Go path is an explicit output,
not an implicit dependency on a sibling repository.

## ML-DSA KUnit vectors

`peios/generate-kacs-kunit-mldsa-vectors.py` requires OpenSSL 3.5 or later with
ML-DSA support. It creates a fresh ML-DSA-65 test key on each invocation and
writes public key, message and signature fixtures for KACS. The temporary private
key is discarded. These are test vectors, not release signing credentials.

```sh
python3 peios/generate-kacs-kunit-mldsa-vectors.py \
    --out security/pkm/kacs/kunit_mldsa_vectors.h
./peios/bazel test //:mldsa-vector-test
```

Regeneration deliberately replaces randomized fixtures; it is not a reproducible
drift check. Review the generated header and run the affected KUnit tests.

## Build-generated trust table and configuration checks

Despite its name, `peios/generate-keys.py` does not generate a signing keypair.
It converts a supplied ML-DSA-65 public key into the built-in KACS header.
`--pubkey-hex` accepts a 1,952-byte public key encoded as hexadecimal;
`--out` selects the header. `--allow-empty` permits a terminator-only table for
test builds. The production build supplies `peios/keys/dev-tcb.hex`; the KUnit
profile explicitly selects an empty table. `peios/build.sh` performs this step
inside the build container, without modifying the checkout.

`peios/verify-config.sh PATH_TO_CONFIG` checks the resolved configuration's
security invariants, including ML-DSA, lockdown, LSM and firmware policy. The
build runs it after resolving the configuration. See
[Building Peios](<~kernel/development/start-here/building-peios>) for the public
trust inputs and the distinction between development and release outputs.

## Other generators

[ABI regeneration](<~kernel/development/native-subsystems/abi-generation>) covers
compiled Rust bindings. [Documentation maintenance](<~kernel/development/native-subsystems/documentation>)
covers generated reference tables. These have different outputs and checks.
