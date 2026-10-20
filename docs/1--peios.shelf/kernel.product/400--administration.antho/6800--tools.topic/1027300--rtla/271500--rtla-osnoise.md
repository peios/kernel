---
title: "rtla-osnoise"
type: reference
description: "rtla osnoise [MODE] ..."
---

<a id="rst-rtla-osnoise"></a>

<a id="rst-measure-the-operating-system-noise"></a>

## Measure the operating system noise

**Manual section:** 1

<a id="rst-synopsis"></a>

## SYNOPSIS

**rtla osnoise** \[*MODE*\] ...

<a id="rst-description"></a>

## DESCRIPTION

The **rtla osnoise** tool is an interface for the *osnoise* tracer. The *osnoise* tracer dispatches a kernel thread per-cpu. These threads read the time in a loop while with preemption, softirq and IRQs enabled, thus allowing all the sources of operating system noise during its execution. The *osnoise*'s tracer threads take note of the delta between each time read, along with an interference counter of all sources of interference. At the end of each period, the *osnoise* tracer displays a summary of the results.

The *osnoise* tracer outputs information in two ways. It periodically prints a summary of the noise of the operating system, including the counters of the occurrence of the source of interference. It also provides information for each noise via the **osnoise:** tracepoints. The **rtla osnoise top** mode displays information about the periodic summary from the *osnoise* tracer. The **rtla osnoise hist** mode displays information about the noise using the **osnoise:** tracepoints. For further details, please refer to the respective man page.

<a id="rst-modes"></a>

## MODES

**top**

> Prints the summary from osnoise tracer.

**hist**

> Prints a histogram of osnoise samples.

If no MODE is given, the top mode is called, passing the arguments.

<a id="rst-options"></a>

## OPTIONS

**-h**, **--help**

> Display the help text.

For other options, see the man page for the corresponding mode.

<a id="rst-see-also"></a>

## SEE ALSO

**rtla-osnoise-top**(1), **rtla-osnoise-hist**(1)

Osnoise tracer documentation: &lt;[https://www.kernel.org/doc/html/latest/trace/osnoise-tracer.html](<https://www.kernel.org/doc/html/latest/trace/osnoise-tracer.html>)&gt;

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
