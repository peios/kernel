---
title: "ABI documentation parsing in Peios"
type: reference
description: "How Peios reads ABI records and renders them through Trail."
---

<a id="rst-kernel-abi-documentation-parser-class"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

Peios's `kernel-abi` Trail plugin reads the retained `Documentation/ABI/` tree
with `abi.abi_parser.AbiParser`. It renders the resulting data through
`tools/docs/trail-kernel-doc/abi_markdown.py`. The parser lives in
`tools/lib/python/abi/abi_parser.py` and uses the
[ABI helper constants](<~kernel/administration/tools/kabi-helpers>).

These pages document the interfaces described in the source tree. The parser
does not inspect the running system or determine which interfaces a Peios
configuration enables.

## Writing an ABI view

For a symbol reference for the stable ABI records:

````markdown
```{kernel-abi} stable
:no-files:
```
````

The argument can be `stable`, `testing`, `obsolete`, `removed` or `README`.
Without flags, a level shows both its symbols and its source files.
`:no-files:` selects the symbols; `:no-symbols:` selects the files. These flags
take no value and cannot be combined. `README` renders the introduction.

## Parser interface

```python
AbiParser(directory, logger=None, enable_lineno=False, show_warnings=True, debug=0)
```

`directory` names the ABI source tree. `logger` receives diagnostics; the plugin
supplies its `kernel-abi` logger, configured for standard error. The remaining
arguments control source-line output, warnings and debugging. The Trail plugin
keeps their defaults.

The plugin constructs one parser for the request, calls `parse_abi()`, then calls
`check_issues()`. It passes the same populated parser to `AbiMarkdown` for every
requested view. `check_issues()` reports inconsistencies through the logger;
it does not produce the rendered documentation.

| Interface | Purpose |
|---|---|
| `parse_abi()` | Reads the ABI tree and populates the parser's dictionaries. |
| `parse_file(fname, path, basename)` | Parses an individual ABI source file with its ABI level and basename; used by the tree scan. |
| `parse_readme(nametag, fname)` | Populates an introduction record from a README source. |
| `check_issues()` | Reports symbols documented in more than one source file. |
| `data` | Parsed symbol records and source-file records. |
| `what_refs` | Maps a documented `What:` name to its record key for reference resolution. |
| `what_symbols` | Tracks the files and locations associated with each `What:` name. |
| `file_refs` | Maps source filenames to the parser's inherited reference labels. |

## Data consumed by Trail

Symbol records carry the `what` names, ABI level in `path`, source locations in
`file`, and fields such as `description`, `date`, `kernelversion`, `contact` and
`users` when present. A source-file record has `type` equal to `File`. The
renderer separates these records into symbol and file views and retains their
metadata.

`AbiMarkdown` registers the targets for all views before resolving links. It
creates its own deterministic `abi-…` and `abi-file-…` anchors; it does not use
the parser's ReST output as Trail page content. Mentions of documented ABI paths
and ABI source files in descriptions can then link to the corresponding view.

The parser's `doc()`, `desc_rst()` and search-oriented output methods belong to
other front ends. Peios's Trail integration consumes the dictionaries directly.

## Maintaining the integration

The plugin reports the ABI directory, parsed source files, parser modules and
renderer modules as dependencies. A newly added ABI file therefore participates
in rebuild detection as well as changes to existing records.

After an upstream parser update, check symbol and file views together: a page
can contain the right prose while its cross-references or source metadata are
wrong. Keep diagnostics on standard error so that the plugin response remains
valid JSON.
