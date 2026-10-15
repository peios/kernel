---
title: "ABI pattern matching for optional Peios checks"
type: reference
description: "How the retained ABI checker converts documented sysfs names into grouped search patterns."
---

<a id="rst-abi-regex-search-symbol-class"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

`tools/lib/python/abi/abi_regex.py` provides `AbiRegex`, a subclass of
[`AbiParser`](<~kernel/administration/tools/kabi-parser>). The optional
`tools/docs/get_abi.py undefined` command uses it to compare sysfs paths with
documented ABI names. Peios's Trail ABI renderer uses the base parser directly;
building the documentation does not run this comparison.

## Construction and parsing

`AbiRegex(*args, **kwargs)` accepts the base parser's arguments, including the
ABI directory, logger and debug controls. It also accepts `search_string`.
When supplied and nonempty, this is compiled as a regular expression and stored
in `re_string`; an invalid expression raises `ValueError`.

`parse_abi(*args, **kwargs)` first runs the inherited ABI parser. It then
converts `What:` names beginning with `/sys` into patterns, stores the pattern
strings in each record's `regex` list, and groups the compiled expressions in
`regex_group`. File records and non-sysfs names do not generate search patterns.
Call it before requesting candidate expressions. The
[system-symbol checker](<~kernel/administration/tools/kabi-symbols>) performs
this initialisation when its check starts.

The conversion applies the ordered substitutions in `re_whats`. They handle
the numeric ranges, placeholders, alternative names and wildcard conventions
found in the inherited ABI documentation. `escape_symbols` controls escaping
within those transformations. These are documentation-matching heuristics,
not a definition of valid kernel ABI syntax.

## Searching the groups

| Method or field | Purpose |
|---|---|
| `regex_append(what, new)` | Compiles the transformed pattern and adds it to a search group. Invalid patterns produce a warning and are not added. |
| `get_regexes(what)` | Returns candidate compiled expressions for a sysfs path, using its path components and the fallback group. It does not itself decide whether the path matches. |
| `regex_group` | Dictionary from group name to compiled expression list. |
| `leave_others` | Name of the fallback group: `others`. |
| `skip_names` | Common components excluded during group selection, currently `devices` and `hwmon`. |
| `re_symbol_name` | Recognises components usable for grouping. |
| `re_has_num` | Retained compiled expression for numeric-pattern detection; the current grouping methods do not use it. |

Grouping reduces the number of patterns examined for each path. The checker
calls `get_regexes()` for the path and tests those candidates against its names
and aliases. A match suggests that an ABI description covers the name; it does
not validate the interface's values or behaviour.

## Filtering and diagnostics

`search_string` has two uses in the retained implementation. `SystemSymbols`
uses the compiled `re_string` to select paths for checking. During pattern
creation, `regex_append()` also prints a `What:` name when it contains the
original search string literally. That diagnostic is a substring test, so it
need not select the same names as the regular expression.

The inherited `debug` value accepts the
[`AbiDebug` constants](<~kernel/administration/tools/kabi-helpers>). `REGEX`
reports transformed patterns, `SUBGROUP_MAP` reports grouping decisions,
`SUBGROUP_DICT` dumps the groups, and `SUBGROUP_SIZE` prints the largest groups.
Debug log messages also require an appropriate logger level. The command-line
front end configures this when its global `--debug` option is nonzero.

## Maintaining the optional checker

If an ABI naming convention changes, review the transformation order and group
selection together. A missed match may come from an unsupported naming pattern,
an omitted candidate group, or genuinely missing documentation. Preserve the
original `What:` name when investigating; the transformed expression alone can
hide the cause. The checker is available for Peios audits, but it is not a
configured documentation-build or release gate.
