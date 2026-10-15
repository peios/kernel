---
title: "rv-mon-wwnr"
type: reference
description: "rv mon wip [OPTIONS]"
---

<a id="rst-rv-mon-wwnr"></a>

<a id="rst-wakeup-while-not-running-monitor"></a>

## Wakeup While Not Running monitor

<!-- SPDX-License-Identifier: GPL-2.0 -->

**Manual section:** 1

<a id="rst-synopsis"></a>

## SYNOPSIS

**rv mon wip** \[*OPTIONS*\]

<a id="rst-description"></a>

## DESCRIPTION

The wakeup while not running (**wwnr**) is a per-task sample monitor.

See kernel documentation for further information about this monitor: &lt;[https://docs.kernel.org/trace/rv/monitor_wwnr.html](<https://docs.kernel.org/trace/rv/monitor_wwnr.html>)&gt;

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

<a id="rst-see-also"></a>

## SEE ALSO

**rv**(1), **rv-mon**(1)

Linux kernel *RV* documentation: &lt;[https://www.kernel.org/doc/html/latest/trace/rv/index.html](<https://www.kernel.org/doc/html/latest/trace/rv/index.html>)&gt;

<a id="rst-author"></a>

## AUTHOR

Written by Daniel Bristot de Oliveira &lt;[bristot@kernel.org](<mailto:bristot@kernel.org>)&gt;

<a id="rst-reporting-bugs"></a>

## REPORTING BUGS

Report bugs to &lt;[linux-kernel@vger.kernel.org](<mailto:linux-kernel@vger.kernel.org>)&gt; and &lt;[linux-trace-devel@vger.kernel.org](<mailto:linux-trace-devel@vger.kernel.org>)&gt;

<a id="rst-license"></a>

## LICENSE

**rv** is Free Software licensed under the GNU GPLv2

<a id="rst-copying"></a>

## COPYING

Copyright (C) 2022 Red Hat, Inc. Free use of this software is granted under the terms of the GNU Public License (GPL).
