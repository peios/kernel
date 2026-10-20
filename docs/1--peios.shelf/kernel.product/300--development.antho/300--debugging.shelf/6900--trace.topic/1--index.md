---
title: "Linux Tracing Technologies Guide"
type: reference
description: "Tracing in the Linux kernel is a powerful mechanism that allows developers and system administrators to analyze and debug system behavior. This guide provides documentation on various tracing frameworks and tools available in the Linux…"
---

<a id="rst-linux-tracing-technologies-guide"></a>

Tracing in the Linux kernel is a powerful mechanism that allows developers and system administrators to analyze and debug system behavior. This guide provides documentation on various tracing frameworks and tools available in the Linux kernel.

<a id="rst-introduction-to-tracing"></a>

## Introduction to Tracing

This section provides an overview of Linux tracing mechanisms and debugging approaches.

- [Using the tracer for debugging](<~kernel/development/trace/debugging>)
- [Using the Linux Kernel Tracepoints](<~kernel/development/trace/tracepoints>)
- [Notes on Analysing Behaviour Using Events and Tracepoints](<~kernel/development/trace/tracepoint-analysis>)
- [Tracefs ring-buffer memory mapping](<~kernel/development/trace/ring-buffer-map>)

<a id="rst-core-tracing-frameworks"></a>

## Core Tracing Frameworks

The following are the primary tracing frameworks integrated into the Linux kernel.

- [ftrace - Function Tracer](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/trace/ftrace.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)
- [Function Tracer Design](<~kernel/development/trace/ftrace-design>)
- [Using ftrace to hook to functions](<~kernel/development/trace/ftrace-uses>)
- [Kernel Probes (Kprobes)](<~kernel/development/trace/kprobes>)
- [Kprobe-based Event Tracing](<~kernel/development/trace/kprobetrace>)
- [Fprobe-based Event Tracing](<~kernel/development/trace/fprobetrace>)
- [Eprobe - Event-based Probe Tracing](<~kernel/development/trace/eprobetrace>)
- [Fprobe - Function entry/exit probe](<~kernel/development/trace/fprobe>)
- [Lockless Ring Buffer Design](<~kernel/development/trace/ring-buffer-design>)

<a id="rst-event-tracing-and-analysis"></a>

## Event Tracing and Analysis

A detailed explanation of event tracing mechanisms and their applications.

- [Event Tracing](<~kernel/development/trace/events>)
- [Subsystem Trace Points: kmem](<~kernel/development/trace/events-kmem>)
- [Subsystem Trace Points: power](<~kernel/development/trace/events-power>)
- [NMI Trace Events](<~kernel/development/trace/events-nmi>)
- [MSR Trace Events](<~kernel/development/trace/events-msr>)
- [Subsystem Trace Points: PCI](<~kernel/development/trace/events-pci>)
- [Boot-time tracing](<~kernel/development/trace/boottime-trace>)
- [Event Histograms](<~kernel/development/trace/histogram>)
- [Histogram Design Notes](<~kernel/development/trace/histogram-design>)

<a id="rst-hardware-and-performance-tracing"></a>

## Hardware and Performance Tracing

This section covers tracing features that monitor hardware interactions and system performance.

- [Intel(R) Trace Hub (TH)](<~kernel/development/trace/intel-th>)
- [System Trace Module](<~kernel/development/trace/stm>)
- [MIPI SyS-T over STP](<~kernel/development/trace/sys-t>)
- [CoreSight - ARM Hardware Trace](<~kernel/development/trace/coresight/index>)
- [Runtime Verification](<~kernel/development/trace/rv/index>)
- [HiSilicon PCIe Tune and Trace device](<~kernel/development/trace/hisi-ptt>)
- [In-kernel memory-mapped I/O tracing](<~kernel/development/trace/mmiotrace>)
- [Hardware Latency Detector](<~kernel/development/trace/hwlat-detector>)
- [OSNOISE Tracer](<~kernel/development/trace/osnoise-tracer>)
- [Timerlat tracer](<~kernel/development/trace/timerlat-tracer>)

<a id="rst-user-space-tracing"></a>

## User-Space Tracing

These tools allow tracing user-space applications and interactions.

- [user_events: User-based Event Tracing](<~kernel/development/trace/user-events>)
- [Uprobe-tracer: Uprobe-based Event Tracing](<~kernel/development/trace/uprobetracer>)

<a id="rst-additional-resources"></a>

## Additional Resources

For more details, refer to the respective documentation of each tracing tool and framework.
