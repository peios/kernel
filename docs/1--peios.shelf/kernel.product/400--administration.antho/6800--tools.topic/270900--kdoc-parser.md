---
title: "Kernel-doc parsing in Peios"
type: reference
description: "The parser, source-file handling and structured records behind live kernel-doc blocks."
---

<a id="rst-kernel-doc-parser-stage"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

Peios keeps C API documentation beside its declarations and expands it into
Trail pages with the `kernel-doc` plugin. The plugin uses the kernel's Python
parser in `tools/lib/python/kdoc/` and supplies a
[Markdown output format](<~kernel/administration/tools/kdoc-output>).

A page requests source comments with a fence such as:

````markdown
```{kernel-doc} drivers/base/core.c
:export:
```
````

Paths are relative to the configured kernel source root. The plugin resolves
the path, selects the requested declarations, and reports the files it read as
build dependencies. Its entry point is
`tools/docs/trail-kernel-doc/trail-kernel-doc`.

<a id="rst-file-handler-classes"></a>

## File handling

`kdoc.kdoc_files.KernelFiles` coordinates parsing, caching, diagnostics and output.
Peios constructs it as `KernelFiles(out_style=style, logger=logger)`, where
`style` is a `MarkdownFormat` instance and the logger writes to standard error.

| Method | Behaviour |
|---|---|
| `parse(file_list, export_file=None)` | Parses the requested sources and any additional files needed to identify exported symbols. |
| `parse_file(fname)` | Parses comments and exports together; caches the results by filename. |
| `process_export_file(fname)` | Scans only export declarations in an additional source file. |
| `msg(...)` | Applies the selection and yields `(filename, rendered_text)` pairs. |
| `warning(msg)` / `error(msg)` | Logs a diagnostic and increments the error count. |

`msg()` accepts `enable_lineno`, `export`, `internal`, `symbol`, `nosymbol`,
`no_doc_sections`, `filenames` and `export_file`. Peios passes an explicit
`filenames` list so that cached results from another block do not appear in the
current block. An empty `:identifiers:` option selects declarations without
`DOC:` sections; `:functions:` is an alias for `:identifiers:`.

The `results` dictionary holds the parsed items by filename. `files` and
`export_files` record inputs already processed; `export_table` holds the exported
names for each file. The plugin includes these inputs in its dependency response.
Use a new coordinator when the underlying source needs to be parsed afresh.

`GlobSourceFiles(srctree=None, valid_extensions=None)` supports this coordinator.
Its `parse_files(file_list, file_not_found_cb)` iterator accepts files and
directories, recursively selecting source extensions within directories. The
Trail entry point expands option globs before handing them to `KernelFiles`.

<a id="rst-parsed-item-data-class"></a>

## Parsed records

`kdoc.kdoc_item.KdocItem(name, fname, type, start_line, **other_stuff)` carries a
parsed declaration or documentation section into the output stage.

| Attribute | Content |
|---|---|
| `name`, `fname`, `type` | Identifier, source filename and declaration kind. |
| `declaration_start_line` | Source position of the declaration. |
| `sections` | Named documentation sections and their text. |
| `parameterlist` | Ordered parameter or member names. |
| `parameterdescs` | Descriptions indexed by parameter or member name. |
| `parametertypes` | Parsed types indexed by parameter or member name. |
| `parameterdesc_start_lines` | Source positions associated with parameter descriptions. |
| `other_stuff` | Additional declaration-specific values, such as purpose and prototype information. |

`set_sections(sections, start_lines)` and
`set_params(names, descs, types, starts)` populate these collections.
`get(key, default=None)` and `item[key]` read **only** `other_stuff`; they do not
look up the named attributes above. The renderer reads structured fields as
attributes and uses `get()` for optional declaration-specific fields.

<a id="rst-parser-classes-and-methods"></a>

## Parser internals

`kdoc.kdoc_parser.KernelDoc(config, fname)` handles one C source file.
`parse_kdoc()` returns the exported-symbol set and the list of parsed items.
`parse_export()` performs an export-only scan. The coordinator supplies the
configuration and diagnostic callback used by both paths.

The parser uses `state` and its `state_actions` table to move through comment
headers, bodies and declarations. `KernelEntry(config, fname, ln)` accumulates
the current comment, sections and warnings before a `KdocItem` is emitted.
The `apply_transforms()`, `trim_whitespace()` and `trim_private_members()` helpers
support declaration processing. These are internal parser machinery; a Trail
plugin should enter through `KernelFiles` rather than drive the state handlers.

## Nested documentation and updates

Some C comments contain another kernel-doc directive. Peios handles that through
a child `MarkdownFormat` and a separate `KernelFiles` coordinator, sharing the
parent's symbol registry while keeping its output buffer separate. Nested source
and export files also become dependencies.

An upstream parser change can affect every live kernel-doc page, even when its
RST wrapper has not changed. Review the parser, the record fields consumed by
the renderer, selection behaviour and generated links together. Existing
source-comment warnings are reported separately from conversion failures.
