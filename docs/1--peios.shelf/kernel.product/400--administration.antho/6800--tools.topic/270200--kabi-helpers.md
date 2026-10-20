---
title: "ABI parser helpers in Peios"
type: reference
description: "The ABI source path and diagnostic controls used by the documentation parser."
---

<a id="rst-ancillary-classes"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

`tools/lib/python/abi/helpers.py` supplies constants used by the
[ABI parser](<~kernel/administration/tools/kabi-parser>). Peios retains this
module because the `kernel-abi` Trail plugin uses that parser to read
`Documentation/ABI/`.

## Source directory

`ABI_DIR` is the string `Documentation/ABI/`. The parser uses it when interpreting
source paths. It is not the Trail site's output directory. The plugin constructs
an absolute input path from its configured kernel source root and passes that
path to `AbiParser`.

## Diagnostic controls

`AbiDebug` is a class containing integer constants. The parser accepts their
values through its `debug` constructor argument; the Trail plugin uses the
default value, zero.

| Constant | Value | Parser use |
|---|---:|---|
| `WHAT_PARSING` | 1 | Detailed parsing diagnostics for a `What:` entry. |
| `WHAT_OPEN` | 2 | File-opening diagnostics. |
| `DUMP_ABI_STRUCTS` | 4 | Dumps the collected ABI data after parsing. |

The implementation checks `WHAT_PARSING` using equality. The other two checks
use bit masks. For the detailed `What:` trace, set `debug=AbiDebug.WHAT_PARSING`
alone; combining it with another value does not enable that trace.
The logger must also be configured to emit debug messages to display it.

The module also defines flags for the optional undefined-ABI checker and its
regular-expression grouping diagnostics, plus the CLI help string `DEBUG_HELP`.
Those controls are used by separate tooling and are not exposed as Trail fence
options. Peios's documentation build does not run that checker.

## Keeping plugin output valid

The plugin writes its JSON response to standard output and configures the ABI
logger to use standard error. Keep diagnostics separate from the response when
changing the integration. These helpers describe documentation tooling; an ABI
entry appearing in the generated reference is not evidence that its interface
is enabled in a running Peios kernel.
