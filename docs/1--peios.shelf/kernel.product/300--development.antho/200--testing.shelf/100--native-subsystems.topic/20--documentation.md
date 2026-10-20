---
title: "Maintaining native subsystem documentation"
description: "Keep authored subsystem explanations, generated native ABI tables and TRM provenance aligned."
type: guide
---

Native kernel documentation lives with the kernel. Internals explain the
implementation; Userspace interfaces describe caller contracts; Administration
covers operation; Development covers changing and testing the code. The combined
learn site presents these collections alongside the rest of Peios documentation.

## Authored and generated sources

Edit ordinary articles directly. `tools/docs/peios-reference/generate.py`
regenerates the native ABI tables and StrataFS constants from this source tree.
It uses a C compiler to measure ABI layouts and values; StrataFS's private
constants are extracted from the C and Rust definitions. The generator does
not need a sibling `pkm` or `learn` checkout.

Run it with `--check` to detect drift without editing pages. It refuses changes
to the expected section layout or named claims until the migration mapping is
reviewed, so a new table cannot silently disappear into an old split layout.
Handwritten interface notes are outside the generated output and are never
overwritten by regeneration.

## Provenance and claim anchors

`peios/docs-migration/trm-source-map.json` records the old book paths and hashes,
section destinations, named claims, and the pages assembled from each source.
It is separate from the upstream Linux source map. The old TRM is retained in
`learn/` during review; changes here do not regenerate or remove it.

Trail's named citation syntax is currently book-scoped. In the new topic pages,
the same claim identifiers are preserved as explicit `cite-NAME` HTML anchors.
The mapping records their new article addresses. Existing test citations still
resolve through the retained original book; these topic anchors do not silently
replace Trail's exported book citation catalogue.

Keep anchors when editing or splitting articles. Update the TRM mapping when an
article or claim moves, and update its incoming links. Numbered book references
have been converted to explicit links to their target explanation. Cross-system
specifications retain links to their own pages on learn.peios.org.

## Validation

```sh
python3 tools/docs/peios-reference/generate.py --check
make htmldocs
make linkcheckdocs
```

Keep the retained TRM unchanged until the replacement has been reviewed and its
external consumers have a deliberate migration path. Generated tables establish
header values and layouts; they do not prove the correctness of every prose
claim or qualify kernel runtime behaviour.
