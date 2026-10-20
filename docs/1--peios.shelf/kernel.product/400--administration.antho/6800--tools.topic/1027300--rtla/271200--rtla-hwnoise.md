---
title: "rtla-hwnoise"
type: reference
description: "rtla hwnoise [OPTIONS]"
---

<a id="rst-rtla-hwnoise"></a>

<a id="rst-detect-and-quantify-hardware-related-noise"></a>

## Detect and quantify hardware-related noise

<!-- SPDX-License-Identifier: GPL-2.0 -->

**Manual section:** 1

<a id="rst-synopsis"></a>

## SYNOPSIS

**rtla hwnoise** \[*OPTIONS*\]

<a id="rst-description"></a>

## DESCRIPTION

**rtla hwnoise** collects the periodic summary from the *osnoise* tracer running with *interrupts disabled*. By disabling interrupts, and the scheduling of threads as a consequence, only non-maskable interrupts and hardware-related noise is allowed.

The tool also allows the configurations of the *osnoise* tracer and the collection of the tracer output.

<a id="rst-options"></a>

## OPTIONS

**-a**, **--auto** *us*

> Set the automatic trace mode. This mode sets some commonly used options while debugging the system. It is equivalent to use **-s** *us* **-T 1 -t**.

**-p**, **--period** *us*

> Set the *osnoise* tracer period in microseconds.

**-r**, **--runtime** *us*

> Set the *osnoise* tracer runtime in microseconds.

**-s**, **--stop** *us*

> Stop the trace if a single sample is higher than the argument in microseconds. If **-T** is set, it will also save the trace to the output.

**-S**, **--stop-total** *us*

> Stop the trace if the total sample is higher than the argument in microseconds. If **-T** is set, it will also save the trace to the output.

**-T**, **--threshold** *us*

> Specify the minimum delta between two time reads to be considered noise. The default threshold is *5 us*.

**-t**, **--trace** \[*file*\]

> Save the stopped trace to \[*file\|osnoise_trace.txt*\].

**-q**, **--quiet**

> Print only a summary at the end of the session.

**-c**, **--cpus** *cpu-list*

> Set the hwnoise tracer to run the sample threads in the cpu-list.
>
> By default, the hwnoise tracer runs the sample threads on all CPUs.

**-H**, **--house-keeping** *cpu-list*

> Run rtla control threads only on the given cpu-list.
>
> If omitted, rtla will attempt to auto-migrate its main thread to any CPU that is not running any workload threads.

**-d**, **--duration** *time\[s\|m\|h\|d\]*

> Set the duration of the session.

**-D**, **--debug**

> Print debug info.

**-e**, **--event** *sys:event*

> Enable an event in the trace (**-t**) session. The argument can be a specific event, e.g., **-e** *sched:sched_switch*, or all events of a system group, e.g., **-e** *sched*. Multiple **-e** are allowed. It is only active when **-t** or **-a** are set.

**--filter** *&lt;filter&gt;*

> Filter the previous **-e** *sys:event* event with *&lt;filter&gt;*. For further information about event filtering see [https://www.kernel.org/doc/html/latest/trace/events.html\#event-filtering](<https://www.kernel.org/doc/html/latest/trace/events.html#event-filtering>).

- ****--trigger** *&lt;trigger&gt;***

  Enable a trace event trigger to the previous **-e** *sys:event*. If the *hist:* trigger is activated, the output histogram will be automatically saved to a file named *system_event_hist.txt*. For example, the command:

  rtla &lt;command&gt; &lt;mode&gt; -t -e osnoise:irq_noise --trigger="hist:key=desc,duration/1000:sort=desc,duration/1000:vals=hitcount"

  Will automatically save the content of the histogram associated to *osnoise:irq_noise* event in *osnoise_irq_noise_hist.txt*.

  For further information about event trigger see [https://www.kernel.org/doc/html/latest/trace/events.html\#event-triggers](<https://www.kernel.org/doc/html/latest/trace/events.html#event-triggers>).

**-P**, **--priority** *o:prio\|r:prio\|f:prio\|d:runtime:period*

> Set scheduling parameters to the hwnoise tracer threads, the format to set the priority are:
>
> - *o:prio* - use SCHED_OTHER with *prio*;
>
> - *r:prio* - use SCHED_RR with *prio*;
>
> - *f:prio* - use SCHED_FIFO with *prio*;
>
> - *d:runtime\[us\|ms\|s\]:period\[us\|ms\|s\]* - use SCHED_DEADLINE with *runtime* and *period* in nanoseconds.
>
> If not set, tracer threads keep their default priority. For rtla user threads, it is set to SCHED_FIFO with priority 95. For kernel threads, see *osnoise* and *timerlat* tracer documentation for the running kernel version.

**-C**, **--cgroup** \[*cgroup*\]

> Set a *cgroup* to the tracer's threads. If the **-C** option is passed without arguments, the tracer's thread will inherit **rtla**'s *cgroup*. Otherwise, the threads will be placed on the *cgroup* passed to the option.
>
> If not set, the behavior differs between workload types. User workloads created by rtla will inherit rtla's cgroup. Kernel workloads are assigned the root cgroup.

**--warm-up** *s*

> After starting the workload, let it run for *s* seconds before starting collecting the data, allowing the system to warm-up. Statistical data generated during warm-up is discarded.

- ****--trace-buffer-size** *kB***

  Set the per-cpu trace buffer size in kB for the tracing output.

  If not set, the default tracefs buffer size is used.

**--on-threshold** *action*

> Defines an action to be executed when tracing is stopped on a latency threshold specified by **-a/--auto**, **-s/--stop**, or **-S/--stop-total**.
>
> Multiple --on-threshold actions may be specified, and they will be executed in the order they are provided. If any action fails, subsequent actions in the list will not be executed.
>
> Supported actions are:
>
> - *trace\[,file=&lt;filename&gt;\]*
>
>   Saves trace output, optionally taking a filename. Alternative to -t/--trace. Note that unlike -t/--trace, specifying this multiple times will result in the trace being saved multiple times.
>
> - *signal,num=&lt;sig&gt;,pid=&lt;pid&gt;*
>
>   Sends signal to process. "parent" might be specified in place of pid to target the parent process of rtla.
>
> - *shell,command=&lt;command&gt;*
>
>   Execute shell command.
>
> - *continue*
>
>   Continue tracing after actions are executed instead of stopping.
>
> Example:
>
> $ rtla hwnoise -s 20 --on-threshold trace --on-threshold shell,command="grep ipi_send osnoise\_trace.txt" --on-threshold signal,num=2,pid=parent
>
> This will save a trace with the default filename "osnoise\_trace.txt", print its lines that contain the text "ipi_send" on standard output, and send signal 2 (SIGINT) to the parent process.
>
> Performance Considerations:
>
> Due to implementational limitations, actions might be delayed up to one second after tracing is stopped.

**--on-end** *action*

> Defines an action to be executed at the end of tracing.
>
> Multiple --on-end actions can be specified, and they will be executed in the order they are provided. If any action fails, subsequent actions in the list will not be executed.
>
> See the documentation for **--on-threshold** for the list of supported actions, with the exception that *continue* has no effect.
>
> Example:
>
> $ rtla hwnoise -d 5s --on-end trace
>
> This runs rtla with the default options, and saves trace output at the end.

**-h**, **--help**

> Print help menu.

<a id="rst-example"></a>

## EXAMPLE

In the example below, the **rtla hwnoise** tool is set to run on CPUs *1-7* on a system with 8 cores/16 threads with hyper-threading enabled.

The tool is set to detect any noise higher than *one microsecond*, to run for *ten minutes*, displaying a summary of the report at the end of the session:



```text
# rtla hwnoise -c 1-7 -T 1 -d 10m -q
                                        Hardware-related Noise
duration:   0 00:10:00 | time is in us
CPU Period       Runtime        Noise  % CPU Aval   Max Noise   Max Single          HW          NMI
  1 #599       599000000          138    99.99997           3            3           4           74
  2 #599       599000000           85    99.99998           3            3           4           75
  3 #599       599000000           86    99.99998           4            3           6           75
  4 #599       599000000           81    99.99998           4            4           2           75
  5 #599       599000000           85    99.99998           2            2           2           75
  6 #599       599000000           76    99.99998           2            2           0           75
  7 #599       599000000           77    99.99998           3            3           0           75
```

The first column shows the *CPU*, and the second column shows how many *Periods* the tool ran during the session. The *Runtime* is the time the tool effectively runs on the CPU. The *Noise* column is the sum of all noise that the tool observed, and the *% CPU Aval* is the relation between the *Runtime* and *Noise*.

The *Max Noise* column is the maximum hardware noise the tool detected in a single period, and the *Max Single* is the maximum single noise seen.

The *HW* and *NMI* columns show the total number of *hardware* and *NMI* noise occurrence observed by the tool.

For example, *CPU 3* ran *599* periods of *1 second Runtime*. The CPU received *86 us* of noise during the entire execution, leaving *99.99997 %* of CPU time for the application. In the worst single period, the CPU caused *4 us* of noise to the application, but it was certainly caused by more than one single noise, as the *Max Single* noise was of *3 us*. The CPU has *HW noise,* at a rate of *six occurrences*/*ten minutes*. The CPU also has *NMIs*, at a higher frequency: around *seven per second*.

The tool should report *0* hardware-related noise in the ideal situation. For example, by disabling hyper-threading to remove the hardware noise, and disabling the TSC watchdog to remove the NMI (it is possible to identify this using tracing options of **rtla hwnoise**), it was possible to reach the ideal situation in the same hardware:



```text
# rtla hwnoise -c 1-7 -T 1 -d 10m -q
                                        Hardware-related Noise
duration:   0 00:10:00 | time is in us
CPU Period       Runtime        Noise  % CPU Aval   Max Noise   Max Single          HW          NMI
  1 #599       599000000            0   100.00000           0            0           0            0
  2 #599       599000000            0   100.00000           0            0           0            0
  3 #599       599000000            0   100.00000           0            0           0            0
  4 #599       599000000            0   100.00000           0            0           0            0
  5 #599       599000000            0   100.00000           0            0           0            0
  6 #599       599000000            0   100.00000           0            0           0            0
  7 #599       599000000            0   100.00000           0            0           0            0
```

<a id="rst-see-also"></a>

## SEE ALSO

**rtla-osnoise**(1)

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
