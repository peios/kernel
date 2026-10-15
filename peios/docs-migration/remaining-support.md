# Remaining kernel documentation support

Work: PEI-1505. There are now **9,632 mapped articles**: 3,381 RST-derived
articles, 748 legacy prose/text articles, 30 live Netlink protocol references,
5,415 device-tree binding references, 16 shared schema references, 40 live
supporting-source references and two standalone figures. No RST or identified
human-readable source remains unaccounted for. `source-inventory.json` covers
all 11,072 Documentation files, including the 549 excluded translations.

This completes source translation and disposition accounting. Final organization
and technical/editorial review remain. Selected-line highlighting remains a
presentation enhancement; its original metadata is preserved. Downloads remain
deliberately excluded at Jack's request.

## Whole-tree completion audit

The final pass adds the four extensionless device-tree bindings missed by the
.txt/README scan, the architecture feature-table legend and two licence notices.
Eight SCSI changelogs, twelve litmus tests, four Netlink schema definitions and
sixteen other scripts/examples/data files now have live source-reference pages.
Their source is displayed verbatim through `kernel-include`; they are not
rewritten as executable instructions or presented as current release notes.
The MultiSound script also contains a README, now extracted into readable prose
above its unchanged live source archive. The standalone DRBD connection diagram is reviewed Mermaid, and the AMD display
SVG is preserved as an image. Neither original source tree was changed.

The inventory also records original Sphinx/build tooling, redirect notices and
Linux logo artwork as retained non-article material. These are explicit,
hash-pinned decisions. The checker rejects added, removed or changed files,
changed symlink targets and stale ownership, without relying on filename suffixes.
`upstream_changes.py` reports both affected pages and retained-source decisions.

## RST and Netlink completion

The `kernel-netlink` plugin now renders all 30 protocol specifications through
upstream `YnlDocGenerator`, Docutils and a bounded Markdown writer. The previously
blocked `netlink-raw.rst` article links to the generated `rt-link` and `tc` pages.
`pending.json` is empty. `netlink-integration-report.json` records validation.

Generated source text, code, anchors and references are checked against actual
HTML. Runtime dependencies cover YAML files, the specification directory and
generator implementation. The complete inventory check rejects missing wrappers
when upstream adds a family. See `check_netlink.py` and the plugin README.

Six automodule wrappers now have authored Peios integration references: `feat`,
`kabi_helpers`, `kabi_parser`, `kdoc_parser`, `kdoc_output`, and `kdoc_ancillary`.
They describe the APIs and data actually consumed by the current Trail plugins,
with source-code dependency hashes and an explicit disposition for every source
module. They are selected references, not complete exports of all Python members.
ReST/man renderers, standalone CLI-only details and Sphinx/PDF setup helpers are
scoped out explicitly. No Python documentation plugin is needed for these pages;
source changes flag the maintained prose for review through the existing map.

At Jack's subsequent request, the three optional-tooling wrappers (`jobserver`,
`kabi_regex`, `kabi_symbols`) also have authored Peios references. Their mappings
use `adapted-optional-interface`, distinguishing available tools from active
Trail dependencies. The references cover public interfaces, command usage,
configuration applicability and result interpretation. No tool was enabled or
removed. `optional-python-adaptation-report.json` records this follow-up.

## Latest delivered features

Feature tables (17 pages), ABI views (9), maintainer references (1), UAPI symbol
tables (8 headers on 5 pages), equations (4), the schema example (1), and two
references into generated content added 39 articles. The runtime expands 35 new
generator blocks. All 72 equations preserve canonical source TeX, including
`align*`, and render to annotated MathML. A `math` fence is a display equation;
inline equations use a code span with a dollar sign immediately on both sides.
Ordinary dollar-delimited prose is not math.

Jack declined downloads on PEI-1505. The schema example's download sentence now
links to the upstream file at the recorded revision; its full current contents
remain a live include. No attachment publishing feature is required.

The Trail anchor index and plugin ordering connect header symbols to both
hand-written and kernel-doc documentation. ABI and feature directory dependencies
also participate in upstream-change mapping, including newly added files. Existing
reviewed Mermaid and literal whitespace/range behavior remain in place.

## Structured collections and scope

- **Netlink:** all 30 YAML protocol specifications under
  `Documentation/netlink/specs/` have maintained wrappers and live rendering.
  The earlier count of 31 included `index.rst`. The four other YAML files in
  the wider directory are schema definitions; the final pass gives them live
  source-reference pages. The upstream generator
  defines the documentation view; this does not expose every raw schema key.
- **Device tree:** all 5,415 YAML bindings have live Trail references, together
  with 16 shared definitions from pinned dt-schema 2026.9. Conditions and source
  values remain scoped as authored; this catalogue does not replace binding
  validation. All 732 legacy text bindings also have maintained Trail articles.
  The YAML and legacy text remain outside the RST conversion count.

## Legacy text completion

All 732 device-tree text bindings, seven other `.txt` documents and two README
articles are migrated. The other text/README sources are already represented by
includes or generators, apart from `.renames.txt` and the two Sphinx dependency
requirement files, which are metadata. `legacy-text-inventory.json` accounts for
all 806 English `.txt`/extensionless README sources.

The pass preserves every source line and exact literal blocks, including DTS
examples, tables, pseudocode, BibTeX and ASCII figures. The mac80211 sequence
source is now a reviewed Mermaid diagram. Source mapping flags upstream changes
for every new article. Existing pages received link-only updates where they
previously pointed to these documents on the upstream source browser.

Final organization and technical/editorial review remain. The final residual audit now accounts for every source/data format under Documentation. The originals and source queue remain unchanged.

## Converter capabilities now implemented

Live literal and file-backed CSV includes now use `kernel-include`: 43 blocks on
33 pages. This added 20 articles and replaced 15 copied blocks on 13 maintained
articles without regenerating their prose. Plugin dependencies participate in
upstream change reports and live preview refresh. Parsed RST fragments retain
their existing source mapping rather than becoming literal file excerpts.

The follow-up handles inspected LaTeX layout commands, explicit web conditions,
local CSV files, glossaries and term links, nested line blocks, option lists,
doctests, attributions, generated section numbers, C namespaces, code captions,
embedded SVG, source-link repairs, and provisional index placement. Seven new
DOT figures are Mermaid, following Jack's existing decision.

Authored C declarations expose the agreed `c-…` anchors; the existing articles
received anchor-only additions with byte-for-byte prose preservation. Exact,
hash-pinned RST repairs are in `source-repairs.json`. Source mapping records
dependencies and conversion decisions. Unrecognised content still fails.

Selected-line highlighting is deferred, with each original `emphasize-lines`
value retained in the mapping. Downloads were explicitly declined by Jack. Final organisation and editorial review remain later work. Neither
`Documentation/` nor the source queue was changed by this follow-up.
