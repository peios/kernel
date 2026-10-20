---
title: "Jobserver coordination for optional Peios builds"
type: reference
description: "How the retained jobserver helper shares Make's parallelism budget with a child command."
---

<a id="rst-job-server-module"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

The kernel retains `tools/lib/python/jobserver.py` and its command wrapper,
`scripts/jobserver-exec`, for commands that need to share Make's parallel-build
budget. The Clang-LTO initcall-ordering rule in `scripts/Makefile.vmlinux_o` uses
this wrapper. Peios's current `peios/config/config.x86_64.base` sets
`CONFIG_LTO_NONE=y`, so that rule is inactive in the base configuration.
Trail's documentation build does not use this helper.

## Reserving parallel work

`JobserverExec()` claims the jobserver tokens currently available and adds one
for the calling task's existing reservation. It passes that total to a child
through the `PARALLELISM` environment variable. The child must honour that
variable for the reservation to constrain its parallel work.

The helper reads jobserver information from `MAKEFLAGS`. It accepts inherited
numeric pipe descriptors and the `fifo:PATH` form. It opens a nonblocking read
handle so that it can collect the available tokens without waiting for every
other Make task to finish. The resulting budget is the capacity available at
that moment, not necessarily the original `make -j` value.

## Python interface

| Interface | Behaviour |
|---|---|
| `JobserverExec()` | Initialises token storage and connection state; it does not reserve tokens until opened. |
| `open()` | Attempts to connect and collect available tokens. Repeated calls while open do nothing. |
| `run(cmd, *args, **pwargs)` | Ensures the helper is open, sets `PARALLELISM` when a budget was obtained, and returns the result of `subprocess.call()`. Additional arguments are forwarded to that call. |
| `close()` | Returns the collected token bytes to the jobserver and clears the open-state flag. |
| Context-manager entry and exit | Calls `open()` on entry and `close()` on exit, including exceptional exits. |
| `warn(text, *args)` | Writes a warning to standard error. |

Use the context manager to return reservations after the child finishes:

```python
from jobserver import JobserverExec

with JobserverExec() as jobserver:
    status = jobserver.run(["command-that-honours-PARALLELISM"])
```

The import requires the kernel's `tools/lib/python/` on Python's module search
path; `scripts/jobserver-exec` arranges this for command-line use.

The state fields are `claim` (the child budget, including the caller's slot),
`jobs` (the reserved token bytes), `reader`, `writer` and `is_open`. Use one
instance for one reservation lifecycle. `close()` returns tokens; it does not
reset all fields or provide a fresh connection for reuse.

## Command wrapper and fallback behaviour

From the kernel source root, the wrapper's invocation is:

```text
python3 scripts/jobserver-exec COMMAND [ARGUMENT ...]
```

The wrapper runs the command inside a `JobserverExec` context. The present
wrapper does not propagate the child return code through `sys.exit()`; callers
needing that status should account for this when choosing how to invoke it.
The Python `run()` method itself returns the child status.

When no usable jobserver is found, the helper still runs the command and does
not set a new `PARALLELISM` value. It does not clear a value already inherited
from the environment. When it does set the variable, it changes the current
Python process's environment and does not restore the previous value afterward.

These details matter when embedding the helper in a longer-running process.
They do not change Peios's default build configuration or enable LTO.
