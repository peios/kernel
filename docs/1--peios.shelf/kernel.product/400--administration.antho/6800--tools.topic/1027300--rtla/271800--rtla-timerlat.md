---
title: "rtla-timerlat"
type: reference
description: "rtla timerlat [MODE] ..."
---

<a id="rst-rtla-timerlat"></a>

<a id="rst-measures-the-operating-system-timer-latency"></a>

## Measures the operating system timer latency

**Manual section:** 1

<a id="rst-synopsis"></a>

## SYNOPSIS

**rtla timerlat** \[*MODE*\] ...

<a id="rst-description"></a>

## DESCRIPTION

The **rtla timerlat** tool is an interface for the *timerlat* tracer. The *timerlat* tracer dispatches a kernel thread per-cpu. These threads set a periodic timer to wake themselves up and go back to sleep. After the wakeup, they collect and generate useful information for the debugging of operating system timer latency.

The *timerlat* tracer outputs information in two ways. It periodically prints the timer latency at the timer *IRQ* handler and the *Thread* handler. It also enables the trace of the most relevant information via **osnoise:** tracepoints.

The **rtla timerlat** tool sets the options of the *timerlat* tracer and collects and displays a summary of the results. By default, the collection is done synchronously in kernel space using a dedicated BPF program attached to the *timerlat* tracer. If either BPF or the **osnoise:timerlat_sample** tracepoint it attaches to is unavailable, the **rtla timerlat** tool falls back to using tracefs to process the data asynchronously in user space.

The **rtla timerlat top** mode displays a summary of the periodic output from the *timerlat* tracer. The **rtla timerlat hist** mode displays a histogram of each tracer event occurrence. For further details, please refer to the respective man page.

<a id="rst-modes"></a>

## MODES

**top**

> Prints the summary from *timerlat* tracer.

**hist**

> Prints a histogram of timerlat samples.

If no *MODE* is given, the top mode is called, passing the arguments.

<a id="rst-options"></a>

## OPTIONS

**-h**, **--help**

> Display the help text.

For other options, see the man page for the corresponding mode.

<a id="rst-see-also"></a>

## SEE ALSO

**rtla-timerlat-top**(1), **rtla-timerlat-hist**(1)

*timerlat* tracer documentation: &lt;[https://www.kernel.org/doc/html/latest/trace/timerlat-tracer.html](<https://www.kernel.org/doc/html/latest/trace/timerlat-tracer.html>)&gt;

<a id="rst-author"></a>

## AUTHOR

Written by Daniel Bristot de Oliveira &lt;[bristot@kernel.org](<mailto:bristot@kernel.org>)&gt;

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-exit-status"></a>

## EXIT STATUS



```text
0  Passed: the test did not hit the stop tracing condition
1  Error: invalid argument
2  Failed: the test hit the stop tracing condition
```

<a id="rst-reporting-bugs"></a>

## REPORTING BUGS

Report bugs to &lt;[linux-kernel@vger.kernel.org](<mailto:linux-kernel@vger.kernel.org>)&gt; and &lt;[linux-trace-devel@vger.kernel.org](<mailto:linux-trace-devel@vger.kernel.org>)&gt;

<a id="rst-license"></a>

## LICENSE

**rtla** is Free Software licensed under the GNU GPLv2

<a id="rst-copying"></a>

## COPYING

Copyright (C) 2021 Red Hat, Inc. Free use of this software is granted under the terms of the GNU Public License (GPL).
