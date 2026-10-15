# Kernel documentation migration

These are one-way import tools, initially scoped to `Documentation/locking/`
and extended with a bounded mechanical pass over the remaining RST corpus.
The maintained documentation lives in `docs/`. Never regenerate over edited
Trail articles. The source-pruning phase below supersedes the original requirement
to retain the full upstream tree.

Tracked in Acta: **PEI-1505**.


## Current authority and retained tooling inputs

Jack authorized pruning after complete translation and source accounting.
`docs/` is now authoritative for prose and illustrations. The 6,210 retained
`Documentation/` files are machine-consumed inputs: YAML schemas, ABI data,
feature tables, man-page and checker inputs, NFS XDR, build integration, and
required assets. The per-file `storage.reason` records the consuming tool.
75 live inputs moved to `docs/sources/`; the figure registry and three reviewed
Mermaid files also moved there. 4,787 replaced or excluded originals were removed.
The translation queue was subsequently verified and removed. Original files were checked byte-for-byte
against the recorded `kernel_commit` before removal and backed up before install.

The source inventory retains all 11,072 upstream records. Original `source` and
`source_sha256` remain provenance; `storage.path` and optional
`storage.current_sha256` describe current inputs. Runtime dependencies use their
current paths and retain `upstream_path` when relocated. `upstream_changes.py`
therefore still follows upstream changes to removed and moved files. The new
layout checker rejects reintroduced prose, unknown inputs and missing, duplicate
or changed live inputs. Generated `Documentation/output/` is excluded.

`verify.py` now checks current article hashes, assets and live dependencies for
this layout. Intentional prose edits require reviewing and refreshing
`current_output_sha256`, not preserving upstream wording. The original conversion
checker remains available for historical source/mapping snapshots; it requires
a complete source tree, whereas the normal authority check does not. Initial
import commands elsewhere in this file describe historical migration steps and
must be run in a full upstream checkout, never over maintained articles.

`make htmldocs` uses Trail (`TRAIL=/path/to/trail` selects a binary).
`make linkcheckdocs` additionally checks local links and assets. `make mandocs`
retains RTLA/RV manual builds. Unsupported Sphinx export targets fail explicitly.
Code comments may retain original paths: `documentation-file-ref-check` resolves
known paths to existing maintained articles and still reports unknown references.
Checkpatch searches maintained legacy device-tree bindings alongside YAML.

The public workflow is documented in the Trail article
[Maintaining Peios kernel documentation](../../docs/kernel.product/300--development.antho/400--contributing.shelf/2400--doc-guide.topic/10--maintaining-peios-documentation.md).
`pruning-report.json` records validation and recovery information for this phase.

## Initial import

Run from the kernel repository root, using a virtual environment:

```sh
python3 -m venv /tmp/kernel-docs-venv
/tmp/kernel-docs-venv/bin/pip install -r peios/docs-migration/requirements.txt
/tmp/kernel-docs-venv/bin/python peios/docs-migration/convert.py \
  --kernel-root "$PWD" --out /tmp/kernel-locking-import
```

The output directory must not exist. The converter reads `docs-to-translate/`,
parses RST with Docutils, and emits articles under the staging directory's
`docs/`, together with `source-map.json`. It writes nothing into either source
tree. Only copy reviewed output into `docs/`.

`locking-plan.json` defines titles, descriptions, order, destination identities,
and reviewed layout choices. The topic overview and the anthology/shelf/topic
configuration are authored separately. The source toctree and every RST file in
the batch must be accounted for, or conversion fails.

The parser rejects unknown directives and options, unresolved references, and
unsupported nodes. The initial Locking converter disables file includes and
raw RST. `bulk.py` extends the writer with explicitly supported constructs;
it still rejects everything it cannot preserve and verify.

## Mechanical batches

```sh
PYTHONDONTWRITEBYTECODE=1 /tmp/kernel-docs-venv/bin/python peios/docs-migration/bulk.py \
  --kernel-root "$PWD" --out /tmp/kernel-mechanical-import
```

The output directory must be new. Already mapped sources are skipped, including
the reviewed Locking articles. The input queue is checked against the original
`Documentation/` bytes. Parsing uses the original source paths so local includes
resolve correctly, and every include is confined to the kernel tree (apart from
Docutils' standard character entities). Raw content remains disabled.

Each accepted page passes prose, heading/term, code-block, table, image, diagram,
and source-anchor preservation checks. Cross-reference captions are compared
after resolution. Unsupported pages stay in `pending.json` with their full
diagnostics, rather than being emitted with missing content. The output includes
a combined source map and a plan of the newly imported pages. `--exclude` accepts
a JSON object mapping source paths to reasons for deliberately leaving them queued.

The current navigation groups the inherited categories into Internals, Kernel
development, Administration, Hardware and drivers, and Userspace interfaces.
Scheduling and RCU share the Concurrency and synchronisation shelf with Locking.
Source indexes become linked articles; deeper source directories are represented
as a single Trail topic-folder level with descriptive paths.

Treat these as mechanically imported references awaiting editorial review.
Never copy over an existing article or shared Trail configuration. Keep the
newly migrated source queue until review authorizes its removal. During the initial translation, all original sources were kept unchanged.
The authorized pruning phase now retains only machine-consumed inputs.

### Diagrams

Graphviz figures are rewritten as Mermaid, per Jack's choice. `diagrams.py`
preserves visible nodes, connections, labels, port routing, semantic colours,
and dashed/bold edge styles. Mermaid supplies layout; invisible positioning
nodes/edges are explicitly recorded as layout-only omissions. Unsupported graph
semantics are rejected. Existing SVG/PNG and other supported raster images are
copied byte-for-byte into their article folders.

Each diagram's source path, source hash, Mermaid hash, and graph inventory are
recorded in the source map. The three figures expanded inside DRM kernel-doc
use maintained `.mmd` files and a pinned registry in the plugin directory; an
upstream change to their DOT inputs is a build error until reconciled. Runtime
rendering does not need Graphviz or pydot. Pydot is only a migration dependency.

`check_mermaid.py` optionally renders standalone `.mmd` artifacts with Trail's
bundled Mermaid and a dedicated headless Chromium profile. It requires
Playwright, separately from the normal migration requirements. Supply
`--vendor`, `--chromium`, and `--out`; it writes SVGs, screenshots, and a report.

### Combined checks

Before installation, combine the staged articles with existing docs in a
temporary tree, preserving existing configuration, then run the verifier and a
strict Trail build. Use an absolute plugin command and kernel root in that
temporary tree's configuration. Check the built site with:

```sh
/tmp/kernel-docs-venv/bin/python peios/docs-migration/check_site.py /tmp/kernel-docs-site
PYTHONDONTWRITEBYTECODE=1 /tmp/kernel-docs-venv/bin/python peios/docs-migration/check_plugins.py \
  --kernel-root "$PWD" --mapping /tmp/kernel-mechanical-import/source-map.json \
  --report /tmp/kernel-mechanical-import/plugin-report.json
```

The site checker checks local links, fragments, assets and duplicate IDs,
including print bundles. The plugin checker records actual dependencies per
article, including nested kernel-doc inputs, export scans, and generator code.
It **updates the supplied staged mapping**; do not point it at the maintained
mapping unless intentionally refreshing its dependency baseline. The full
Trail build separately validates cross-page generated symbol references.

`validation-report.json` records the installed batch's checks and counts.
`pending.json` retains the remaining RST work; `plugin-warnings.json` records
inherited C-source warnings separately from conversion failures.

### Preservation follow-up

The first 62 pages rejected by preservation checks are now converted. The
fixes preserve literal numeric paragraph prefixes and hyphens, underscore
runs, adjacent inline code, punctuation-adjacent emphasis, visible inline
target labels, title-footnote links, code-first double-digit list items, and
form-feed characters in literal excerpts. Historical `file:` references are
resolved only when their paths exist inside the kernel tree and link to the
recorded upstream revision. Missing paths still fail conversion.

`preservation-pass-report.json` records this batch separately from the original
mechanical pass. The 62 pages also passed a comparison against the actual Trail
HTML, in addition to the Markdown preservation checks. To run that comparison
on a mapping of bulk-imported pages:

```sh
PYTHONDONTWRITEBYTECODE=1 /tmp/kernel-docs-venv/bin/python \
  peios/docs-migration/check_rendered_preservation.py \
  --kernel-root "$PWD" --site /tmp/kernel-docs-site \
  --mapping /tmp/new-pages-map.json
```

The renderer check restricts text comparisons to the article body and checks
literal blocks in order, allowing generated kernel-doc examples between them.
It preserves source trailing newlines and control characters. Use it with
bulk mappings that contain `resolved_references`; the original hand-reviewed
Locking mappings use the original verifier.

The remaining implementation inventory is in [remaining-support.md](remaining-support.md).
It distinguishes Trail presentation gaps, kernel-specific generators, and
converter-only work. Keep organisation provisional until translation coverage
is complete.

### Peios Python integration references

Nine original automodule wrappers have authored replacements: six describe the
interfaces used by Peios's Trail plugins, and three describe optional build and
ABI-checking tools. This follows Jack's instructions to adapt the active
references to Peios and subsequently translate the optional tools too. These pages
are not mechanical exports of every Python member. Each has an `adaptation`
record in `source-map.json`: all source modules are classified as an adapted
active interface, optional interface or context only, and the implementations
are tracked in `source_dependencies`.

`adapted.py`, called by `verify.py`, checks source and code dependency hashes,
module dispositions, maintained article hashes, licence and retained anchors.
The rendered preservation checker compares the authored Markdown with actual
HTML for these pages, including exact literal examples. It does not claim that
unused Sphinx members were preserved. A dependency change fails the adaptation
check until the maintained prose and recorded disposition have been reviewed.
The existing upstream-diff reporter maps those same dependencies to the pages.

Keep an edited page's `initial_output_sha256`; after review, refresh only its
`current_output_sha256` and the reviewed dependency baseline. Never regenerate
over authored text. Only the outstanding Netlink RST source remains in
`pending.json`. `python-adaptation-report.json` records the first six pages;
`optional-python-adaptation-report.json` records the three optional-tool pages.

### Converter follow-up and authored symbols

The next 94 articles cover reviewed LaTeX layout omissions, web conditions,
glossaries and term links, local CSV tables, nested line blocks, option lists,
doctests, attributions, code captions, source-link repairs, provisional indexes,
and previously unsorted reference material. Seven more DOT diagrams are Mermaid;
the embedded SVG example is preserved as an extracted asset.

`constructs.py` accepts only the inspected LaTeX commands and web conditions.
Unrecognised raw content or conditions still fail. CSV reads are confined to the
kernel tree and recorded as source dependencies. Captions become adjacent prose;
the original `emphasize-lines` values are retained in `migration_decisions`, with
visual highlighting deferred. No new generator fence is emitted before its
implementation is delivered and configured.

`source-repairs.json` records exact before/after repairs and reasons for malformed
RST and obsolete links. Every repair is pinned to its original source hash and
occurrence count. An upstream change requires reconciliation rather than silently
reapplying the repair. These transformations happen in memory: neither source
tree is edited.

Authored C declarations emit `c-NAME`, `c-struct-NAME`, `c-union-NAME` or
`c-enum-NAME` anchors alongside the existing `rst-` aliases. Namespaces are
recorded in the mapping, and `noindex` declarations do not claim symbol targets.
Repeated declarations on one page share their first target; identical names on
different pages remain separate page-qualified targets. The future Trail anchor
index can expose these to generators.

`add_c_anchors.py` staged 456 anchors across 197 previously imported articles.
It checks the maintained article hash, inserts anchors before existing signature
blocks, and verifies that removing only those insertions reproduces the original
bytes. It does not regenerate prose. To stage a future anchor-only update:

```sh
PYTHONDONTWRITEBYTECODE=1 /tmp/kernel-docs-venv/bin/python \
  peios/docs-migration/add_c_anchors.py --kernel-root "$PWD" \
  --mapping peios/docs-migration/source-map.json --out /tmp/kernel-anchor-update
```

`non_article_sources` accounts for the ext4 block-map and RV option fragments
through their owning pages and source dependencies. The Sphinx subproject index
template is accounted for as navigation, supplied by Trail. The original Locking
index retains its existing separate mapping. All 3,385 English RST sources are
accounted for: 3,371 articles, 10 pending sources, three non-article sources, and
the Locking index. `converter-follow-up-report.json` records this batch and its
validation; `validation-report.json` contains the cumulative results.

## Representation choices

- Preserve source wording, code, diagrams, author credits, and licence notices.
- Use `rst-` HTML anchor aliases for source section IDs and labels so editorial
  heading changes do not invalidate imported references.
- Translate references to imported documents into Trail `~` links. References
  outside this batch point to source files at the recorded upstream commit;
  their paths are recorded for later migration.
- Keep headerless tables and cell spans as HTML tables. Do not invent headings.
- Render definition lists as nested Markdown lists, preserving their hierarchy.
- Keep Roman list labels when prose refers to them by label.
- The plan identifies source lines where indentation represented layout rather
  than a quotation, and assigns syntax highlighting to reviewed code examples.
  These are initial-import choices, not rules to apply blindly to a newer source.
- Preserve `kernel-doc` directives as `{kernel-doc}` fences, with source-root
  paths and options. Imported C-domain roles remain inline code. To add a
  link to a generated symbol, use the plugin's explicit `#c-NAME` anchors
  (or `#c-struct-NAME`, `#c-union-NAME`, `#c-enum-NAME` for tagged types).

## Live file includes

Literal files and file-backed CSV tables use `{kernel-include}` fences, following
Jack's decision recorded on PEI-1505. The initial integration covers 43 blocks
on 33 pages: 20 new articles and 13 existing articles with copied excerpts
replaced. Paths remain relative to the kernel root; options preserve the source
selection, encoding, language and CSV header rows. The same plugin now supports UAPI symbol tables, described below.

`stage_live_includes.py` replaces only exact, verified copied blocks; it refuses
changed article baselines and never regenerates maintained prose.
`check_live_includes.py` records runtime dependencies in the source map, including
the included files and plugin implementation. `upstream_changes.py` maps changes
to those dependencies back to their articles. Literal and CSV file edits were
also verified to refresh the running preview without editing its Markdown.

Preservation checks expand the live fences, compare literal content exactly,
and check raw CSV cells separately from RST paragraphs. The plugin retains EOF
newlines and Docutils line-selection semantics. Trail must include the local
`src/plugins.rs` fix preserving whitespace-only lines in generated code blocks;
the integration validated that fix on top of commit
`b8f607bbe01db04d390319c23828fdf990d5b3b9`. See `live-includes-report.json`.

## Generated references and equations

The latest handoff adds 39 articles, reaching 3,371 mapped articles with 10 RST
sources pending. `generated.py` emits only the delivered feature, ABI, maintainer
and UAPI plugin fences. It verifies each path, option and block order against the
source. Exception-file paths become kernel-root-relative. Generated references
use stable ABI file anchors and the original `rst-maintainers` label.

Display equations use `math` fences, one per source equation; inline equations
use Trail's dollar-code-span syntax. Source TeX is checked exactly, then checked
again against actual MathML annotations. The only download role links to the
pinned upstream schema file, following Jack's decision to skip downloads.

`check_generators.py` records runtime file hashes and directory inventories.
`check_generated_data.py` checks actual rendered tables, ABI metadata, maintainer
fields and UAPI header entries against their parsed sources.
`upstream_changes.py` maps changes under directory dependencies, including additions
and renames, to affected articles. Retain these records when reorganizing pages.
`generator-integration-report.json` records this pass's evidence and limitations.
Trail commit `d16453c` or later is needed for equations, directory dependencies,
ordered plugins and the anchor index, together with the locally retained plugin
whitespace fix. The installed plugin README documents configuration.

## Netlink YAML references

The Netlink integration completes the queued English RST migration: 3,381
RST-derived articles plus 30 YAML wrappers make 3,411 mapped articles. Three
non-article sources and the original Locking index account for the other English
RSTs. `pending.json` is empty; non-RST migration and editorial organization remain.
Historical counts above describe their respective batches.

`kernel-netlink` uses upstream `YnlDocGenerator` and Docutils to produce the same
reference view as Sphinx. Install its isolated runtime dependencies as described
in `tools/docs/trail-kernel-doc/README.md`. Source labels remain stable `rst-`
anchors. Each wrapper maps directly to a YAML source and records generator file
hashes and the specification directory inventory.

After an upstream update, reconcile affected sources and wrappers, build the
site, then validate a staging copy of the mapping:

```sh
cp peios/docs-migration/source-map.json /tmp/netlink-source-map.json
/tmp/kernel-docs-venv/bin/python peios/docs-migration/check_netlink.py \
  --kernel-root "$PWD" --plugin tools/docs/trail-kernel-doc \
  --docs docs --site /tmp/kernel-docs-site \
  --mapping /tmp/netlink-source-map.json --out /tmp/netlink-check
```

The check rejects changed source/wrapper baselines until deliberately reconciled,
missing or duplicate wrappers, and missing rendered text, literal blocks,
anchors or references. It refreshes generator dependencies in the supplied
mapping only after success. Review that staging result before adopting it.
Adding a YAML file invalidates caches and maps to the existing Netlink pages;
it still requires an authored wrapper. Never overwrite maintained prose with a
fresh mechanical import. `netlink-integration-report.json` records the initial
30-family checks and the final RST article's preservation evidence.

## Legacy text import

`import_legacy_text.py` stages the 732 legacy device-tree text bindings and nine
other text/README documents in a new directory. It refuses already-mapped sources
and never writes to the source tree or maintained articles:

```sh
/tmp/kernel-docs-venv/bin/python peios/docs-migration/import_legacy_text.py \
  --kernel-root "$PWD" --out /tmp/kernel-legacy-text-import
```

This batch is already integrated; the command above is for a checkout before the
import or a deliberate fresh rehearsal. Update maintained pages through review,
using `upstream_changes.py`, rather than rerunning the importer over them.

`legacy_text.py` recognizes headings and simple lists, escapes literal markup,
and keeps code, tables, nested property lists, BibTeX and ASCII figures in exact
literal blocks. Every source line has a disposition in the mapping, including
blank lines, title decorations and the LED document's editor modeline. Licence
and author text remain present. Whitespace in prose may reflow; literal bytes do
not. The source remains the upstream technical baseline, with editorial and
Peios-applicability review still pending.

The mac80211 sequence source becomes Mermaid through `legacy_sequence.py`.
All participants, messages, branches and notes are checked, and the complete
diagram was rendered and reviewed. Other ASCII drawings keep their literal form.
Links to mapped text pages become local links; redirects to unrendered YAML
schemas link to the pinned source. No YAML catalogue is added.

`verify.py` and `check_rendered_preservation.py` understand both legacy mapping
kinds. They check complete source-line coverage, visible source text in order,
exact literal content and the source/maintained-output hashes. Rendered checks
remove only known Trail navigation, title, metadata and copy/link controls.
`legacy-text-integration-report.json` records the batch checks and limitations;
`legacy-text-inventory.json` accounts for all 803 English `.txt` files and three
extensionless README files as articles, included/generated sources or metadata.

The mapped total is now 4,152: 3,381 RST-derived articles, 741 legacy text/README
articles and 30 Netlink YAML references. Historical batch counts above remain
as evidence of those earlier passes.

## Verification

```sh
/tmp/kernel-docs-venv/bin/python -m unittest discover -s peios/docs-migration -v
/tmp/kernel-docs-venv/bin/python peios/docs-migration/verify.py \
  --kernel-root "$PWD" --site docs \
  --mapping peios/docs-migration/source-map.json
```

The verifier compares prose, headings/terms, literal-block content and order,
table counts, and source/internal anchors. Five paragraphs containing Sphinx
`:ref:` substitutions need separate comparison because their visible link labels
expand to section titles. This check establishes conversion fidelity, not the
current correctness of every inherited technical claim. Later intentional prose
rewrites will require revising the verification baseline or recording the edits.

The kernel-doc plugin lives in `tools/docs/trail-kernel-doc/` and is configured
in `docs/trail.toml`. It uses the kernel's own Python parser. See its README for
directive options, symbol anchors, and dependency tracking. Use a plugin-capable
Trail binary (validated with Trail commit
`b8f607bbe01db04d390319c23828fdf990d5b3b9`):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/docs/trail-kernel-doc -v
PYTHONDONTWRITEBYTECODE=1 trail build docs --out /tmp/kernel-docs-site --strict
PYTHONDONTWRITEBYTECODE=1 trail serve docs --out /tmp/kernel-docs-site --strict --addr 127.0.0.1:8724
```

`PYTHONDONTWRITEBYTECODE=1` avoids creating Python caches in the source tree.
The integrated Locking build contains 53 generated seqlock API entries. The
27 HTML pages and all 1,834 local links/fragments passed validation, including
print bundles. No browser visual review was available. Older Trail binaries
that display plugin fences as code do not validate the generated reference.

## Upstream updates

```sh
/tmp/kernel-docs-venv/bin/python peios/docs-migration/upstream_changes.py \
  --kernel-root "$PWD" --new NEW_UPSTREAM_REVISION
```

The default old revision is the manifest's upstream commit. `--old` can be used
for a rehearsal. The report maps changed or renamed source files, includes,
image/diagram sources, and direct or recorded indirect kernel-doc inputs to
Trail pages; other changed documentation is explicitly
reported as unmapped for classification. It does not rewrite pages or advance
the baseline. It does not infer semantic effects of arbitrary kernel code
changes or yet-unrecorded generator dependencies.

Keep the mapping current when splitting or moving pages. `initial_output_sha256`
records the mechanical import; `current_output_sha256` records the reviewed
snapshot. Neither authorizes regeneration over the maintained page. The source
queue no longer contains Locking: its 17 articles and index were removed after
integration validation and user visual review. Original `Documentation/` sources remain available in Git; this mapping retains
their paths and hashes for comparison and upstream updates.
The initial-import command above requires the source batch in the queue; to
rehearse that completed import, use a temporary checkout with a copy of
`Documentation/locking/` at `docs-to-translate/locking/`. The verifier and upstream
change report do not depend on the queue.

Rehearsals used in this first batch:

- `28a0ee311960baad97bf85e1e995aed4a71e22a2^` to that commit: a seqlock prose and
  example fix maps to the Trail sequence-counter article.
- `b682b70d016f6aee20d91dcbaa319a932008a83a^` to that commit: a change to
  `include/linux/seqlock.h` maps to the same article, despite no RST change.

Neither rehearsal updates the recorded Linux 7.0.9 baseline.


## Device-tree binding catalogue

The catalogue adds 5,415 kernel binding wrappers and 16 shared dt-schema wrappers.
The 99 category topics live under Hardware / Device-tree bindings. The original
YAML remains authoritative. Existing schema links now resolve to catalogue pages.

Run the independent check after a strict Trail build (install this directory's
`requirements.txt` into the migration environment first):

```sh
python3 peios/docs-migration/check_bindings.py \
  --kernel-root . --plugin tools/docs/trail-kernel-doc --docs docs \
  --mapping peios/docs-migration/source-map.json --site /path/to/trail-output \
  --out /path/to/binding-check --complete
```

This uses an independent YAML 1.2 parser (ruamel.yaml, pure Python), checks every
source node and scalar at its own rendered anchor, checks exact example text and
all shared references, and checks wrapper coverage against the complete kernel
inventory plus its transitive shared definitions. It also verifies source and
wrapper baseline hashes. A source change deliberately requires review before
refreshing those hashes. `verify.py` checks wrappers; the rendered-preservation
checker dispatches binding pages to the same independent content checker.

For upstream updates, run `upstream_changes.py` as usual. Page dependencies track
transitive schema sources; `dependency_groups.device-tree-bindings` tracks the
registry membership and renderer once for the whole catalogue. Ordinary edits
flag the transitive dependent pages; additions, removals and renames trigger
a catalogue inventory review. This catches
added/removed/renamed schemas as well as changed sources and shared definitions.
The live plugin automatically renders reviewed schema edits. For a new binding,
add a wrapper with its exact source title and `{kernel-binding}` source fence,
record its source/output hashes, transitive dependencies and group membership,
then rerun the complete check. Preserve existing page references when moving or
renaming upstream sources. Review removed bindings and incoming links explicitly.
Do not regenerate maintained prose or remove the original YAML.

`binding-integration-report.json` records corpus, source-preservation, strict
build, local-link, existing-content and upstream-mapping validation. Vendored
library provenance is recorded with the plugin, not in the upstream baseline.


## Complete source inventory

`source-inventory.json` records every file under `Documentation/`, including
hidden files, extensionless documents and symlinks. Each record has a SHA-256,
a reviewed disposition and any owning Trail articles. Non-English translations
are explicitly excluded at Jack's request; build tooling and unused Linux
branding remain original sources with recorded reasons. Every identified prose,
history, example and useful standalone figure has a maintained representation.

```sh
python3 peios/docs-migration/check_inventory.py \
  --kernel-root . --mapping peios/docs-migration/source-map.json \
  --inventory peios/docs-migration/source-inventory.json
```

`verify.py` also checks the installed inventory by default; use `--inventory`
to select a staged inventory. Run the inventory check when updating upstream. It fails on
new files regardless of suffix, removed files, content or symlink changes, and
changed source ownership. Classify new files explicitly; reconcile changed ones
before refreshing the reviewed baseline. Never automatically classify an unknown
file merely from its extension. Historical batch inventories describe their own
passes; this whole-tree inventory is the current completion record.

`source-map.json` includes retained-source decisions for `upstream_changes.py`.
The 40 supplementary source references use whole-file `kernel-include` blocks;
`supplementary.py` verifies source/wrapper hashes,
rejects sliced excerpts and compares rendered code exactly, including whitespace.
It also verifies the standalone image and reviewed Mermaid representation.
The seven additional prose articles use the existing line-accounted verifier.
`residual-integration-report.json` records validation of the final 49-page pass.

## Organization checkpoint

The first organization pass follows migration commit `680b7136fef5`.
`reorganisation.json` records the old and new physical paths and article
addresses. Shelves group related topics without adding URL segments. Large
administration, architecture, driver and userspace collections are anthologies
of smaller topics; device-tree schemas have their own reference anthology.

When moving an article, update its destination and reference in `source-map.json`,
all inbound links, asset destinations and inventory ownership references. Preserve
upstream paths, source hashes and initial output hashes. Record changed addresses
in the article's `previous_references`; `make htmldocs-redirects` emits redirects
for these as well as upstream RST URLs. Rebuild and check links after a move.
Historical import plans and validation reports describe their original snapshots.
