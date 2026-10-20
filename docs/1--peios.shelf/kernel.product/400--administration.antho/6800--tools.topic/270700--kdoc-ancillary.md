---
title: "Kernel-doc helpers used by Peios"
type: reference
description: "Regular-expression helpers and UAPI header parsing used by Peios's documentation plugins."
---

<a id="rst-ancillary-classes"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

Peios's documentation plugins use two ancillary parts of
`tools/lib/python/kdoc/`: the regular-expression helpers used by kernel-doc,
and the C-header parser used to build UAPI symbol references.

<a id="rst-regular-expression-class-handler"></a>

## Regular-expression helpers

`kdoc.kdoc_re.KernRe(string, cache=True, flags=0)` wraps a compiled Python regular
expression and remembers the most recent `match()` or `search()` result. The
kernel-doc parser and shared output module use these objects throughout their
declaration handling.

| Method | Behaviour |
|---|---|
| `match(string)` | Matches at the start and stores the result in `last_match`. |
| `search(string)` | Searches the string and stores the result in `last_match`. |
| `group(num)` | Reads a group from the stored match; call only after a successful match or search. |
| `findall(string)` | Returns all matches using the compiled expression. |
| `split(string)` | Splits using the compiled expression. |
| `sub(sub, string, count=0)` | Replaces matches, with zero meaning no replacement-count limit. |

Adding two `KernRe` objects concatenates their patterns and combines their
flags. Because matching updates object state, consume captured groups before
reusing the same object for another match.

`NestedMatch()` supports expressions followed by paired delimiters, such as
nested parentheses in C declarations. `search(regex, line)` yields matching
substrings whose delimiters balance. `sub(regex, sub, line, count=0)` replaces
such matches; a `\1` in the replacement refers to the paired contents without
the outer delimiters. These helpers support the parser's text processing; they
do not constitute a general C parser.

<a id="rst-kernel-c-file-include-logic"></a>

## UAPI header symbols

`kdoc.parse_data_structs.ParseDataStructs(debug=False)` identifies symbols in a
header and computes their documentation references. Peios's `kernel-include`
plugin uses it when a block requests `:generate-cross-refs:` with `:toc:`.

`parse_file(file_in, exceptions=None)` reads the header and optional exception
file. The resulting `symbols` dictionary groups entries by kind. Each entry
maps a symbol name to `(reference, line)`, where the stored line index starts
at zero. `DEF_SYMBOL_TYPES` describes the groups and their default reference
roles:

| Kind | Symbols |
|---|---|
| `ioctl` | IOCTL command definitions. |
| `define` | Other macros and definitions. |
| `symbol` | Values declared within enumerations. |
| `typedef` | Typedef names. |
| `enum` | Named enumerations. |
| `struct` | Structures. |

The exception file can remove a symbol from the reference table, redirect its
documentation target, or set the C namespace:

```text
ignore <type> <symbol>
replace <type> <old_symbol> <new_reference>
namespace <namespace>
```

`new_reference` can be a plain target or an explicit inherited role such as
`:c:type:`. These role strings are parser data, not Trail syntax that article
authors need to introduce. Keep existing header exception files alongside
their source documentation and pass them through the plugin.

## Rendering and diagnostics

`tools/docs/trail-kernel-doc/uapi_markdown.py` consumes the symbol dictionary.
It resolves the parser's reference roles against Trail's anchor index and
displays source line numbers starting at one. Label references look for
`rst-…` anchors; C references look for `c-…` anchors, including tagged types.
Unresolved symbols remain visible; `:warn-broken:` reports them for review.

The include plugin records the header, exception file and parser/renderer code
as dependencies. Parser diagnostics are kept away from the JSON response on
standard output. The parser's `gen_output()`, `gen_toc()` and `write_output()`
ReST helpers are not used for Trail rendering.

## Other modules in the source tree

The retained standalone `tools/docs/parse-headers.py` command uses
`enrich_formatter.EnrichFormatter` for argument help. That formatter is outside
the Trail integration described here. `latex_fonts` and `python_version`
support the inherited Sphinx/PDF and setup tooling; Peios's Trail build does not
use them. Their source remains available, but this reference concentrates on
the modules used by the live documentation plugins.
