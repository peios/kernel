---
title: "Bus lock detection and handling"
type: reference
description: "A split lock is any atomic operation whose operand crosses two cache lines. Since the operand spans two cache lines and the operation must be atomic, the system locks the bus while the CPU accesses the two cache lines."
---

<a id="rst-bus-lock-detection-and-handling"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<!-- This data file has been placed in the public domain. -->

<!-- Derived from the Unicode character mappings available from
<http://www.w3.org/2003/entities/xml/>.
Processed by unicode2rstsubs.py, part of Docutils:
<https://docutils.sourceforge.io>. -->

**Copyright:** © 2021 Intel Corporation

**Authors:** - Fenghua Yu &lt;[fenghua.yu@intel.com](<mailto:fenghua.yu@intel.com>)&gt;

- Tony Luck &lt;[tony.luck@intel.com](<mailto:tony.luck@intel.com>)&gt;

<a id="rst-problem"></a>

## Problem

A split lock is any atomic operation whose operand crosses two cache lines. Since the operand spans two cache lines and the operation must be atomic, the system locks the bus while the CPU accesses the two cache lines.

A bus lock is acquired through either split locked access to writeback (WB) memory or any locked access to non-WB memory. This is typically thousands of cycles slower than an atomic operation within a cache line. It also disrupts performance on other cores and brings the whole system to its knees.

<a id="rst-detection"></a>

## Detection

Intel processors may support either or both of the following hardware mechanisms to detect split locks and bus locks. Some AMD processors also support bus lock detect.

<a id="rst-ac-exception-for-split-lock-detection"></a>

### \#AC exception for split lock detection

Beginning with the Tremont Atom CPU split lock operations may raise an Alignment Check (\#AC) exception when a split lock operation is attempted.

<a id="rst-db-exception-for-bus-lock-detection"></a>

### \#DB exception for bus lock detection

Some CPUs have the ability to notify the kernel by an \#DB trap after a user instruction acquires a bus lock and is executed. This allows the kernel to terminate the application or to enforce throttling.

<a id="rst-software-handling"></a>

## Software handling

The kernel \#AC and \#DB handlers handle bus lock based on the kernel parameter "split_lock_detect". Here is a summary of different options:


<table>
<tbody>
<tr>
<td>


split_lock_detect=

</td>
<td>


\#AC for split lock

</td>
<td>


\#DB for bus lock

</td>
</tr>
<tr>
<td>


off

</td>
<td>


Do nothing

</td>
<td>


Do nothing

</td>
</tr>
<tr>
<td>


warn (default)

</td>
<td>


Kernel OOPs Warn once per task, add a delay, add synchronization to prevent more than one core from executing a split lock in parallel. sysctl split_lock_mitigate can be used to avoid the delay and synchronization When both features are supported, warn in \#AC

</td>
<td>


Warn once per task and and continues to run.

</td>
</tr>
<tr>
<td>


fatal

</td>
<td>


Kernel OOPs Send SIGBUS to user When both features are supported, fatal in \#AC

</td>
<td>


Send SIGBUS to user.

</td>
</tr>
<tr>
<td>


ratelimit:N (0 &lt; N &lt;= 1000)

</td>
<td>


Do nothing

</td>
<td>


Limit bus lock rate to N bus locks per second system wide and warn on bus locks.

</td>
</tr>
</tbody>
</table>

<a id="rst-usages"></a>

## Usages

Detecting and handling bus lock may find usages in various areas:

It is critical for real time system designers who build consolidated real time systems. These systems run hard real time code on some cores and run "untrusted" user processes on other cores. The hard real time cannot afford to have any bus lock from the untrusted processes to hurt real time performance. To date the designers have been unable to deploy these solutions as they have no way to prevent the "untrusted" user code from generating split lock and bus lock to block the hard real time code to access memory during bus locking.

It's also useful for general computing to prevent guests or user applications from slowing down the overall system by executing instructions with bus lock.

<a id="rst-guidance"></a>

## Guidance

<a id="rst-off"></a>

### off

Disable checking for split lock and bus lock. This option can be useful if there are legacy applications that trigger these events at a low rate so that mitigation is not needed.

<a id="rst-warn"></a>

### warn

A warning is emitted when a bus lock is detected which allows to identify the offending application. This is the default behavior.

<a id="rst-fatal"></a>

### fatal

In this case, the bus lock is not tolerated and the process is killed.

<a id="rst-ratelimit"></a>

### ratelimit

A system wide bus lock rate limit N is specified where 0 &lt; N &lt;= 1000. This allows a bus lock rate up to N bus locks per second. When the bus lock rate is exceeded then any task which is caught via the buslock \#DB exception is throttled by enforced sleeps until the rate goes under the limit again.

This is an effective mitigation in cases where a minimal impact can be tolerated, but an eventual Denial of Service attack has to be prevented. It allows to identify the offending processes and analyze whether they are malicious or just badly written.

Selecting a rate limit of 1000 allows the bus to be locked for up to about seven million cycles each second (assuming 7000 cycles for each bus lock). On a 2 GHz processor that would be about 0.35% system slowdown.
