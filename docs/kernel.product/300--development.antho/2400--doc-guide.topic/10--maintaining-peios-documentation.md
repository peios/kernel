---
title: "Maintaining Peios kernel documentation"
type: guide
description: "Edit the authoritative Trail documentation and reconcile changes from upstream Linux."
---

The Peios Kernel documentation is maintained in `docs/`. Edit its Trail articles
directly. The old upstream prose has been removed from `Documentation/`; Git
retains its history and the migration source map records where each document went.

## Choosing the source to edit

Ordinary prose, diagrams and images belong in `docs/`. Files included live by
Trail, such as examples, historical text and CSV tables, live in `docs/sources/`.
The configured plugin launcher keeps this directory out of article discovery
while allowing the preview to watch its inputs. Edit the
included file when changing its contents, and edit its Markdown wrapper for the
surrounding explanation. Plugin paths are relative to the kernel source root.

`Documentation/` retains files consumed by kernel tooling: device-tree and Netlink
schemas, ABI records, architecture feature tables, NFS XDR definitions, Kconfig
and build integration, and the sources needed by specific documentation tools.
RTLA/RV manual-page sources and the RST inputs parsed by checkpatch and the sysctl
checker remain there. For those retained inputs, edit the machine-consumed source
and reconcile the corresponding Trail article in the same change. YAML and other
live generated references update through their plugins. Kernel-doc comments
continue to live beside the code they describe.

The per-file decisions are recorded in
`peios/docs-migration/source-inventory.json`. Its `storage` field distinguishes
retained inputs, relocated inputs and removed originals. `source-map.json` maps
the original paths to maintained article paths and records runtime dependencies.
An old `Documentation/...` reference in a code comment can therefore be looked up
in the source map without restoring duplicate prose.

## Building and checking

Run these commands from the kernel source root, with Trail and the dependencies
listed in `tools/docs/trail-kernel-doc/README.md` installed:

```sh
make htmldocs
make linkcheckdocs
```

Set `TRAIL=/path/to/trail` to choose a binary and `BUILDDIR=/path/to/output` to
choose the output directory. The default output is `Documentation/output`.
`linkcheckdocs` checks local links, anchors and assets. `make mandocs` builds the
retained RTLA/RV manual pages using `rst2man`. The former Sphinx output formats
are no longer built by the Peios documentation targets.

For a preview:

```sh
trail serve docs --out /tmp/peios-kernel-docs --strict --addr 127.0.0.1:8724
```

## Reconciling upstream changes

Compare the recorded upstream revision with the new upstream commit:

```sh
python3 peios/docs-migration/upstream_changes.py --kernel-root . --new NEW_UPSTREAM_REVISION
```

Review the affected articles and tooling inputs. The report uses original paths,
including paths removed from this checkout, and follows relocated dependencies.
New upstream documentation requires an explicit disposition. Do not regenerate
over maintained Markdown or restore the old prose tree during an upstream merge.
Use `git show REVISION:Documentation/path` to read an upstream source version.

After reviewing an edit, refresh its current output or dependency hash in the
mapping; retain the original source and initial output hashes as provenance. Keep
inventory storage hashes aligned with reviewed input changes. Run the inventory
and authority checks, then build Trail and check its rendered links:

```sh
python3 peios/docs-migration/verify.py --kernel-root . --site docs --mapping peios/docs-migration/source-map.json
make linkcheckdocs
```

The migration tools also retain the original conversion-fidelity checks for use
with a complete historical source checkout. Those checks establish what was
preserved during import; they do not require current Peios prose to match upstream
word for word.
