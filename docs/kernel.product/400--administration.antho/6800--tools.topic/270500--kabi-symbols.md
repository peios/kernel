---
title: "Checking Peios sysfs documentation coverage"
type: reference
description: "Using the optional system-symbol checker and interpreting its ABI coverage results."
---

<a id="rst-system-abi-documentation-validation-class"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

`tools/lib/python/abi/system_symbols.py` provides `SystemSymbols`, the optional
checker behind `tools/docs/get_abi.py undefined`. It compares names found in a
sysfs tree with patterns derived from `Documentation/ABI/`. Peios retains the
tool for manual audits; Trail does not run it when rendering ABI documentation.

For an audit of a running Peios system, use that system's sysfs tree and the
matching Peios source revision. Running against a build workstation's `/sys`
describes the workstation, not a Peios image being built there. The results also
depend on the devices and modules present at the time of the scan.

## Command-line use

From the matching kernel source root on the system being examined:

```sh
python3 tools/docs/get_abi.py -D Documentation/ABI undefined --jobs 1
```

To restrict the check to paths matching a pattern, add `--search-string` after
`undefined`. To inspect the selected names without performing the matching
work, add `--dry-run` there instead.

| Option after `undefined` | Purpose |
|---|---|
| `--sysfs-dir PATH` / `-S PATH` | Selects the sysfs root; the default is `/sys`. |
| `--search-string REGEX` / `-s REGEX` | Selects paths through a regular-expression search. |
| `--show-hints` / `-H` | Shows the candidate expressions tried for an unmatched path. |
| `--jobs N` / `-j N` / `--max-workers N` | Selects the worker count; the CLI defaults to one. |
| `--max-chunk-size N` / `-c N` | Sets the maximum work-batch size; the CLI defaults to 50. |
| `--found` / `-f` | Enables additional diagnostics for matched entries. |
| `--dry-run` / `-d` | Lists selected path references instead of scheduling match checks. Sysfs scanning and ABI parsing still occur. |

The global `-D`/`--dir` selects the ABI documentation directory and precedes
the subcommand. Global `-d` means `--debug`; after `undefined`, `-d` means
`--dry-run`. Prefer the long names when writing audit instructions.

## Python interface

`SystemSymbols(abi, sysfs="/sys", hints=False)` receives an
[`AbiRegex`](<~kernel/administration/tools/kabi-regex>) instance. Construction
immediately scans sysfs and builds the path graph; it is not a lazy operation.

| Method | Behaviour |
|---|---|
| `graph_add_file(path, link=None)` | Adds a path and an optional alias to the graph, avoiding an already-recorded path. |
| `print_graph(root_prefix="", root=None, level=0)` | Prints a diagnostic tree, with a recursion-depth limit. |
| `check_file(refs, found)` | Tests batches of related names against candidate ABI patterns and returns result dictionaries containing `found`, `fname` and `msg`. |
| `get_fileref(all_refs, chunk_size)` | Yields batches of path-reference lists for scheduling. |
| `check_undefined_symbols(max_workers=None, chunk_size=50, found=None, dry_run=None)` | Parses the ABI documentation, selects path references, runs the comparisons and prints unmatched paths. |

The collected state includes `root` (the nested path graph), `files` (recorded
paths), `aliases`, `abi`, `log`, `sysfs`, `hints` and `re_ignore`. Graph nodes
store their associated names in `__name`. The walker handles symlinks before
directories to avoid recursively traversing directory links. An alternate
sysfs root is normalised toward `/sys` names for matching documentation.

The scan deliberately excludes categories such as module information,
parameters, firmware, cgroups and debugging/tracing trees. It inventories names
and filesystem relationships; it does not validate the contents returned by
sysfs attributes. Treat the inventory and exclusion rules as part of the tool's
scope, especially when supplying an alternate root.

## Work scheduling and results

The Python method defaults to the detected CPU count when no worker count is
supplied; the CLI explicitly supplies its default of one. Multiple workers use
a process pool and shuffled batches. A single worker uses a thread executor.
The batch size is bounded by the selected chunk size and available work.

An unmatched path is printed as `PATH not found.`. This is a prompt to inspect
the source documentation and the pattern conversion, not proof of a broken
kernel interface. Conversely, a matching name does not establish that an
interface behaves as documented. The command reports findings as text; it
does not turn the number of unmatched paths into a failing process exit status.
Any future automated Peios audit needs to define how it interprets those results.

For debugging, start with a narrow search and `--show-hints`. The `GRAPH` and
`UNDEFINED` flags from `AbiDebug` expose the path graph and individual pattern
comparisons. The associated [pattern reference](<~kernel/administration/tools/kabi-regex>)
explains grouping and the limitations of the inherited name transformations.
