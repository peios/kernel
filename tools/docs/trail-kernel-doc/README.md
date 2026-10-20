# trail-kernel-doc

A [Trail](https://learn.peios.org/trail) plugin that expands kernel-doc
blocks in Markdown pages using the kernel's own kernel-doc parser
(`tools/lib/python/kdoc`). This replaces the Sphinx `kernel-doc` extension
for the Trail-based kernel docs (PEI-1505). The Trail side of the feature
is TRA-11.

The plugin lives in `tools/docs/trail-kernel-doc/` and uses the parser in
`tools/lib/python/kdoc/`. It was imported from Claude's PEI-1505 handoff.
Maintained articles live in `docs/`; `Documentation/` retains tooling inputs.

Figures embedded in kernel-doc comments can use reviewed Mermaid replacements.
`figures.py` resolves them through `docs/sources/figures/registry.json`, checks the original
DOT source hash, and returns the maintained `.mmd` content. Unknown figures or
changed upstream sources fail the build so they cannot silently render stale
diagrams. Reconcile the Mermaid and its source hash after an upstream change;
validate the rendering before accepting the new baseline. Source DOT files,
Mermaid files, the registry and renderer are included in `depends_on`.
Neither Graphviz nor pydot is required by the runtime plugin.

## Live Netlink protocol references

`trail-kernel-netlink` renders a YAML specification with the kernel's
`tools/net/ynl/pyynl/lib/doc_generator.py` (`YnlDocGenerator`, originally by
Breno Leitao). It converts the generated RST through Docutils and a bounded
Markdown writer. Protocol interpretation remains in the upstream generator;
this presents the same documentation view, not a dump of every schema key.

Install its dependencies from the kernel root into an ignored local directory:

```sh
python3 -m pip install --target tools/docs/trail-kernel-doc/.deps \
  -r tools/docs/trail-kernel-doc/requirements-netlink.txt
```

The plugin uses that directory without changing the other plugins' environments.
Docutils is pinned; PyYAML is required by the upstream generator. The site uses:

```toml
[plugins.kernel-netlink]
command = ["python3", "../tools/docs/trail-kernel-doc/trail-kernel-netlink", "--srctree", ".."]
```

Each maintained wrapper contains one block:

````markdown
```{kernel-netlink} Documentation/netlink/specs/rt-link.yaml
```
````

The block accepts one kernel-relative YAML path under `Documentation/netlink/specs/`
and no options or body. Absolute paths, missing files and symlink escapes fail.
Malformed YAML, unsupported generated RST and unresolved references are reported
against the block. Raw HTML and file-inclusion directives in generated RST are
disabled. Standard output contains only the Trail JSON response.

Source labels become `rst-` anchors, including `rst-netlink-rt-link` and the
family's operation, definition, attribute-set and sub-message labels. Headings
provide Trail's navigation, replacing the generated RST contents directive.
As Sphinx does, the adapter removes `LINENO` markers before parsing RST.

Dependency reporting covers requested YAML files, the specification directory,
the upstream generator, renderer, protocol helper and dependency requirements.
New files therefore trigger rebuilds and upstream-change reports. They still
need authored wrapper pages: run the migration Netlink inventory/content check
when updating upstream, which rejects missing or extra wrappers. Never regenerate
over maintained article prose. A new family can be named with underscores in
YAML; its Trail filename/reference uses kebab-case.

Run the tests with `KERNEL_SRCTREE=/path/to/kernel python3 test_netlink.py` from
this directory. Corpus and HTML checks live in
`peios/docs-migration/netlink_references.py` and `check_netlink.py`.

| File | |
|---|---|
| `trail-kernel-doc` | The plugin: reads Trail's request, runs kdoc, prints the response. |
| `kdoc_markdown.py` | `MarkdownFormat`, a sibling of kdoc's `RestFormat`, and the RST→Markdown conversion of comment text. |
| `test_kdoc_markdown.py` | Converter tests: `KERNEL_SRCTREE=/path/to/kernel python3 test_kdoc_markdown.py` |

## Live literal and CSV includes

The companion `trail-kernel-include` plugin renders source files at build time:

```toml
[plugins.kernel-include]
command = ["python3", "../tools/docs/trail-kernel-doc/trail-kernel-include", "--srctree", ".."]
```

````markdown
```{kernel-include} Documentation/gpu/kms-properties.csv
:csv:
:header-rows: 1
```
````

Paths are kernel-root-relative. Literal excerpts accept `language`, `tab-width`,
`encoding`, `start-line`, `end-line`, `start-after` and `end-before`. CSV inputs
accept `csv`, `encoding` and `header-rows`. UAPI symbol tables are now supported as described below. The plugin reports its input and implementation files as dependencies.

The imported include renderer preserves leading/trailing blank lines and EOF
newlines, and matches Docutils line slicing before marker selection. Regression
tests cover these preservation requirements. Trail also needs the whitespace-only
line preservation fix in `src/plugins.rs` so plugin insertion retains tabs,
spaces and form feeds inside code blocks, including lists and blockquotes.
Run `python3 -m unittest discover -s tools/docs/trail-kernel-doc -p 'test_include*.py'`.

## Configuring

In the site's root `trail.toml`, below every plain key:

```toml
[plugins.kernel-doc]
command = ["python3", "../tools/docs/trail-kernel-doc/trail-kernel-doc", "--srctree", ".."]
```

Paths are relative to the site root (`kernel/docs/`), which is also the
plugin's working directory. `--srctree` names the kernel tree, and every
block's file argument is resolved against it.

## Writing

Each `.. kernel-doc::` directive becomes a fenced block:

````markdown
```{kernel-doc} drivers/base/core.c
:export:
```

```{kernel-doc} include/linux/device.h
:identifiers: device_add device_del
```
````

The options and their meanings are the Sphinx directive's:

| Option | Outputs |
|---|---|
| `:export: [globs]` | Symbols exported with `EXPORT_SYMBOL*`, in the file or the files the globs match. |
| `:internal: [globs]` | Everything not exported. |
| `:doc: Title` | The `DOC: Title` section, without its title. |
| `:identifiers: a b` | The named symbols. Empty means everything except DOC sections. |
| `:functions: a b` | Alias of `:identifiers:`. |
| `:no-identifiers: a b` | Leaves the named symbols out. Combines with any of the above. |
| *(none)* | Everything in the file. |

- Long lists may continue on indented lines, and a trailing `\` is dropped.
- Option names are case-insensitive, as in docutils (`mm/ksm.rst` writes `:DOC:`).
- When a block gives more than one of `:export:`, `:internal:`, `:doc:` and `:identifiers:`, the first in that order wins, as in Sphinx, with a warning. `driver-api/usb/dwc3.rst` pairs `:doc:` with `:internal:`, so its `:doc:` has never had an effect.

The plugin fails the block, and so the build, on:
- an unknown option;
- a missing source file;
- an export glob that matches nothing;
- a block with body text.

A block that produces no output is a warning, not an error, because Sphinx
behaves the same way.

## What it produces

Each symbol gets an anchor and an h4 heading. An h4 keeps it out of the
page's table of contents. Then come the declaration as a C code block and
the comment's sections:

````markdown
#### <a id="c-device_add"></a>`device_add()`

```c
int device_add(struct device *dev)
```

add device to device hierarchy.

**Parameters**

- `struct device *dev`: device.

**Description**

This is part 2 of [`device_register()`](#c-device_register), …
````

**Anchors.** Anchors follow C's namespaces:
- `c-NAME` for functions, macros, variables and typedefs;
- `c-struct-NAME`, `c-union-NAME` and `c-enum-NAME` for tagged types.

The anchor is explicit because a heading's own id is Trail's slug of its
text, deduplicated per page, so the plugin can't predict it.

**Cross-references.** Trail sends every kernel-doc block on the site in a
single request. So `foo()`, `&struct foo`, `&foo` and `:c:func:` in comment
text link to wherever the site documents that symbol: `#c-foo` on the same
page, `~kernel/…#c-foo` elsewhere. A symbol the site doesn't document stays
as unlinked code. Only symbols that kernel-doc blocks document can be link
targets. Prose pages that want to link to one can use the same anchors.

**Comment text** is converted from kernel-doc's reStructuredText dialect:
- **Inline markup:** kernel-doc's highlights (`func()`, `&struct x`, `@param`, `%CONST`), ``` ``literal`` ```, roles, and hyperlinks. Relative Sphinx links such as `` `KASAN <kasan.html>`_ `` keep their words but lose the link.
- **Blocks:**
  - `::` literal blocks and `code-block` become fenced code;
  - admonitions become Trail admonitions;
  - section underlines become bold titles;
  - RST grid and simple tables become preformatted text.
- **C-domain directives** written by hand in comments (`c:macro`, `c:function`, `c:type`, `c:var`, `c:struct`, `c:union`, `c:enum`) get the same anchored heading as a parsed symbol, so they are cross-reference targets too. `pvr_drm.h`, `panthor_drm.h` and `pvr_mmu.{h,c}` document their macros this way.
- **`flat-table`** (the kernel's own table directive) becomes an HTML table whose cells hold Markdown: CommonMark ends an HTML block at a blank line, so a blank line either side of a cell's content makes it Markdown again. All of these are supported:
  - `:header-rows:`, `:stub-columns:` and `:fill-cells:`;
  - `:cspan:` and `:rspan:` roles;
  - autospanning short rows;
  - tables nested in cells (`pvr_mmu.c`).
- **`kernel-doc` inside a comment** (`security/landlock/syscalls.c`) is expanded in place, as Sphinx's nested parse does. Its files count as dependencies, and its symbols are anchors and link targets like any others.
- **Lists:** indentation is kept only where it continues a list item, because four spaces is code in Markdown.
- **Definition lists** (a term line with its definition indented beneath) become `- term: definition` items, the form parameters take. When the "term" is really a wrapped sentence, which reStructuredText also reads as a definition list, it is left as written, with the definition as its own paragraph.
- **Escaping:** `<`, `[` and `]`, and lines that Markdown would read as rules, fences or headings, are escaped.
- **Everything else:** directives with no Markdown form are kept visible as preformatted text, with a warning. Today that is only `kernel-figure`: three Graphviz diagrams in `drm_dp_mst_topology.c`.

## Dependencies and rebuilds

The response's `depends_on` lists:
- every C file parsed;
- the plugin's own files;
- kdoc's library files.

Trail reuses the last output while none of them, and none of the blocks,
change. `trail serve` rebuilds when one does. Any change reruns the whole
plugin, because cross-references span every block.

## Validation

A test site holding every kernel-doc directive in `docs-to-translate/` (1,979 blocks on 320 pages, excluding `doc-guide/kernel-doc.rst`, whose directives are examples):
- builds with `trail build --strict`, with every generated cross-reference resolving;
- runs the plugin in about 6 s, and the whole build in about 19 s.

The warnings it prints are kdoc's own, the same ones Sphinx prints.

## Feature, ABI and maintainer generators

The same directory holds `trail-kernel-feat`, `trail-kernel-abi` and
`trail-kernel-maintainers`. Configure each plugin under its fence name with
`command = ["python3", "../tools/docs/trail-kernel-doc/trail-NAME", "--srctree", ".."]`,
replacing NAME with `kernel-feat`, `kernel-abi` or `kernel-maintainers`.

- `{kernel-feat} Documentation/features`: complete matrix; `:arch: x86` selects an architecture table.
- `{kernel-abi} stable`: an ABI level (stable, testing, obsolete, removed) or README. `:no-files:` and `:no-symbols:` select a view.
- `{kernel-maintainers}`: current MAINTAINERS contents, with no argument or options.

The plugins use the kernel's parsers and report their source and implementation
files. ABI and feature plugins also report directories, allowing new files to
invalidate cached output. Keep all views present for their cross-page links.
ABI file headings use `File ...` so their automatic slug differs from the stable
`abi-file-...` anchor. Metadata includes Date, KernelVersion and Contact.

## UAPI symbol references and authored anchors

For `kernel-doc`, add `anchors = true` to its plugin table. For `kernel-include`,
add both `anchors = true` and `after = ["kernel-doc"]`. This sends authored anchors
and kernel-doc's generated anchors before header symbol links are resolved.

````markdown
```{kernel-include} include/uapi/linux/videodev2.h
:generate-cross-refs:
:exception-file: Documentation/userspace-api/media/v4l/videodev2.h.rst.exceptions
:toc:
:warn-broken:
```
````

The exception-file path is kernel-root-relative. Only symbol tables (`:toc:`)
are supported, not a source listing with embedded links. All eight migrated
headers resolve every symbol. Kernel-doc can link explicit tagged type references
to authored types; a bare `&name` only falls back to a tagged type anchor because
an untyped `c-NAME` anchor may denote an unrelated function. Ordinary function
references do not use authored fallback. Source-path mentions in generated prose
are still plain text; this integration does not add a source-to-page link protocol.

The handoff's converter fixes for nested lists and continued admonition text are
included. Reviewed hash-pinned Mermaid rendering and exact literal include
boundary/range handling are retained from the earlier installed implementation.

## Live device-tree binding references

`trail-kernel-binding` presents authored YAML schemas as readable reference pages.
It retains descriptions, property rules, required lists, conditional branches,
shared-schema links, exact DTS examples and source comments. It does not flatten
conditional rules or replace `dt_binding_check` / `dtbs_check` validation.

```sh
python3 -m pip install --target tools/docs/trail-kernel-doc/.deps \
  -r tools/docs/trail-kernel-doc/requirements-binding.txt
```

```toml
[plugins.kernel-binding]
command = ["python3", "../tools/docs/trail-kernel-doc/trail-kernel-binding", "--srctree", ".."]
```

````markdown
```{kernel-binding} Documentation/devicetree/bindings/leds/leds-gpio.yaml
```
````

The block takes one kernel-root-relative source path and no options or body.
Each referenced schema needs its own wrapper in the same build; cycles are
linked without expansion. JSON Pointer targets receive stable `dt-` anchors.
Missing references, duplicate identifiers/keys, unsupported schema keywords,
unsafe YAML and path escapes fail the build. Unknown keywords must be reviewed
and given an explicit rendering rule before an upstream update is accepted.

Shared definitions are vendored unmodified from **dtschema 2026.9** under
`schema-library/`, with licence and package/file SHA-256 provenance in
`schema-library/manifest.json`. The catalogue publishes the 16 definitions reached
by kernel bindings; all 66 library schemas participate in identifier resolution.
Runtime does not execute dt-schema or fetch the network. To refresh the library,
review a pinned dt-schema wheel, replace its schema data and licence, regenerate
the manifest hashes, then rerun the complete inventory and preservation checks.
A newly referenced shared definition needs a wrapper before the build can pass.

The displayed rules preserve their original scope. “Not listed as required here”
is not a global optionality claim. The authored view does not show every implicit
constraint added by dt-schema normalization. See the reader guide in
`docs/1--peios.shelf/kernel.product/500--hardware.antho/100--platforms.shelf/2300--devicetree.topic/10--binding-catalogue.md`.

Schema files, registry directories and renderer implementation are all runtime
cache dependencies. Source mapping stores each page's transitive source closure
and one shared dependency group for catalogue additions and implementation
changes, avoiding a quadratic dependency inventory. See
`peios/docs-migration/README.md` for independent validation and upstream review.

## Documentation source ownership

Peios maintains prose in `docs/`. Trail-only include files and reviewed figures
live under `docs/sources/`; fences name their kernel-root-relative paths.
`Documentation/` retains machine-consumed inputs, including YAML, ABI records,
feature data and NFS XDR. The figure registry is now
`docs/sources/figures/registry.json`; it retains original upstream DOT paths
alongside the current source paths. Original-to-current dependency mappings are
recorded in `peios/docs-migration/source-map.json` for upstream reconciliation.
