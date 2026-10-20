---
title: "Kernel-doc rendering in Peios"
type: reference
description: "How Peios adapts the shared kernel-doc output interface to Trail Markdown."
---

<a id="rst-kernel-doc-output-stage"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

Peios renders parsed kernel-doc records with
`tools/docs/trail-kernel-doc/kdoc_markdown.py`. Its `MarkdownFormat` class
inherits `OutputFormat` from `tools/lib/python/kdoc/kdoc_output.py`, reusing
selection and dispatch while providing Markdown-specific output handlers.
The upstream module remains an active dependency even though its man-page and
ReST renderers are not used to build the Trail site.

<a id="rst-output-handler-for-man-pages-and-rest"></a>

## Shared output interface

The [parser coordinator](<~kernel/administration/tools/kdoc-parser>) calls the
following `OutputFormat` methods:

| Method | Role |
|---|---|
| `set_config(config)` | Supplies the shared parser configuration and warning callback. |
| `set_filter(export, internal, symbol, nosymbol, function_table, enable_lineno, no_doc_sections)` | Sets declaration selection for the current source. |
| `set_symbols(symbols)` | Makes a file's parsed item list available to an output implementation. |
| `msg(fname, name, args)` | Clears the item output buffer, applies selection, dispatches by declaration kind and returns rendered text. |
| `check_doc(name, args)` | Selects a `DOC:` section and emits its applicable warnings. |
| `check_declaration(dtype, name, args)` | Selects a declaration and emits its applicable warnings. |

The modes are `OUTPUT_ALL` (0), `OUTPUT_INCLUDE` (1), `OUTPUT_EXPORTED` (2) and
`OUTPUT_INTERNAL` (3). Exclusions in `nosymbol` apply alongside the selection.
The coordinator prepares `function_table` from explicit identifiers or export
scans. The Trail entry point resolves fence options before calling this interface.

The base class's output hooks are empty. A renderer implements `out_doc()`,
`out_function()`, `out_enum()`, `out_var()`, `out_typedef()` and `out_struct()`;
the last handles both structures and unions. Each receives
`(fname, name, args)` and appends text to `self.data`.

## Markdown rendering

`MarkdownFormat(parent=None)` supplies these hooks. `begin(reference)` sets the
current Trail page and prepares its anchor set. The renderer emits declarations,
parameter or member descriptions, and named sections from the parsed `KdocItem`.

`heading_markdown(kind, name, title)` registers a target and emits its explicit
anchor only once per page. Functions, macros, variables and typedefs use
`c-NAME`; tagged types use `c-struct-NAME`, `c-union-NAME` or `c-enum-NAME`.
The symbol registry allows a mention in one block to link to a declaration
documented by another block. References are resolved after the blocks have
registered their targets.

The inherited `function_pointer` expression is also used when rendering
function-pointer parameters. This is a separate dependency on `kdoc_output.py`,
in addition to `OutputFormat` itself.

`text()`, `sections()` and `items()` convert comment prose and assemble the
Markdown body. `purpose()` emits the short description. The parser's
`KernelDoc.undescribed` marker is interpreted when deciding how to display
missing parameter or member descriptions.

## Embedded content

A child `MarkdownFormat(parent=parent)` shares symbol and page-anchor registries
with its parent but owns a separate output buffer. This is needed when a comment
expands another kernel-doc block while the parent is still being rendered.
The plugin supplies the nested-expansion callbacks and the reviewed Mermaid
figure integration.

Other Peios documentation renderers reuse the comment-to-Markdown converter for
inherited ReST prose. For example, the ABI renderer disables kernel-doc-specific
highlighting when interpreting ordinary ABI descriptions.

## Maintaining the renderer

When updating `OutputFormat`, check method signatures, filter behaviour and the
`KdocItem` fields consumed by all Markdown hooks. Changes to `RestFormat` or
`ManFormat` need review only if they also affect shared code; neither class
supplies Peios's Trail output. Keep generated anchors stable when changing
presentation so that existing documentation links continue to work.
