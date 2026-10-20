---
title: "rv-mon-sched"
type: reference
description: "rv mon sched [OPTIONS]"
---

<a id="rst-rv-mon-sched"></a>

<a id="rst-scheduler-monitors-collection"></a>

## Scheduler monitors collection

<!-- SPDX-License-Identifier: GPL-2.0 -->

**Manual section:** 1

<a id="rst-synopsis"></a>

## SYNOPSIS

**rv mon sched** \[*OPTIONS*\]

**rv mon &lt;NESTED_MONITOR&gt;** \[*OPTIONS*\]

**rv mon sched:&lt;NESTED_MONITOR&gt;** \[*OPTIONS*\]

<a id="rst-description"></a>

## DESCRIPTION

The scheduler monitor collection is a container for several monitors to model the behaviour of the scheduler. Each monitor describes a specification that the scheduler should follow.

As a monitor container, it will enable all nested monitors and set them according to OPTIONS. Nevertheless nested monitors can also be activated independently both by name and by specifying sched: , e.g. to enable only monitor tss you can do any of:

> \# rv mon sched:tss
>
> \# rv mon tss

See kernel documentation for further information about this monitor: &lt;[https://docs.kernel.org/trace/rv/monitor_sched.html](<https://docs.kernel.org/trace/rv/monitor_sched.html>)&gt;

<a id="rst-options"></a>

## OPTIONS

**-h**, **--help**

> Print the monitor's options and the available reactors list.

**-r**, **--reactor** *reactor*

> Enables the *reactor*. See **-h** for a list of available reactors.

**-s**, **--self**

> When tracing (**-t**), also print the events that happened during the **rv** command itself. If the **rv** command itself generates too many events, the tool might get busy processing its own events only.

**-t**, **--trace**

> Trace monitor's events and error.

**-v**, **--verbose**

> Print debug messages.

<a id="rst-nested-monitor"></a>

## NESTED MONITOR

- **The available nested monitors are:**

  - scpd: schedule called with preemption disabled

  - snep: schedule does not enable preempt

  - sncid: schedule not called with interrupt disabled

  - snroc: set non runnable on its own context

  - sco: scheduling context operations

  - tss: task switch while scheduling

<a id="rst-see-also"></a>

## SEE ALSO

**rv**(1), **rv-mon**(1)

Linux kernel *RV* documentation: &lt;[https://www.kernel.org/doc/html/latest/trace/rv/index.html](<https://www.kernel.org/doc/html/latest/trace/rv/index.html>)&gt;

<a id="rst-author"></a>

## AUTHOR

Written by Gabriele Monaco &lt;[gmonaco@redhat.com](<mailto:gmonaco@redhat.com>)&gt;

<a id="rst-reporting-bugs"></a>

## REPORTING BUGS

Report bugs to &lt;[linux-kernel@vger.kernel.org](<mailto:linux-kernel@vger.kernel.org>)&gt; and &lt;[linux-trace-devel@vger.kernel.org](<mailto:linux-trace-devel@vger.kernel.org>)&gt;

<a id="rst-license"></a>

## LICENSE

**rv** is Free Software licensed under the GNU GPLv2

<a id="rst-copying"></a>

## COPYING

Copyright (C) 2022 Red Hat, Inc. Free use of this software is granted under the terms of the GNU Public License (GPL).
