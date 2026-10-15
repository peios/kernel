---
title: "The Linux Kernel Tracepoint API"
type: reference
description: "Tracepoints are static probe points that are located in strategic points throughout the kernel. 'Probes' register/unregister with tracepoints via a callback mechanism. The 'probes' are strictly typed functions that are passed a unique set…"
---

<a id="rst-the-linux-kernel-tracepoint-api"></a>

**Author:** Jason Baron

**Author:** William Cohen

<a id="rst-introduction"></a>

## Introduction

Tracepoints are static probe points that are located in strategic points throughout the kernel. 'Probes' register/unregister with tracepoints via a callback mechanism. The 'probes' are strictly typed functions that are passed a unique set of parameters defined by each tracepoint.

From this simple callback mechanism, 'probes' can be used to profile, debug, and understand kernel behavior. There are a number of tools that provide a framework for using 'probes'. These tools include Systemtap, ftrace, and LTTng.

Tracepoints are defined in a number of header files via various macros. Thus, the purpose of this document is to provide a clear accounting of the available tracepoints. The intention is to understand not only what tracepoints are available but also to understand where future tracepoints might be added.

The API presented has functions of the form: `trace_tracepointname(function parameters)`. These are the tracepoints callbacks that are found throughout the code. Registering and unregistering probes with these callback sites is covered in the `Documentation/trace/*` directory.

<a id="rst-irq"></a>

## IRQ

```{kernel-doc} include/trace/events/irq.h
:internal:
```

<a id="rst-signal"></a>

## SIGNAL

```{kernel-doc} include/trace/events/signal.h
:internal:
```

<a id="rst-block-io"></a>

## Block IO

```{kernel-doc} include/trace/events/block.h
:internal:
```

<a id="rst-workqueue"></a>

## Workqueue

```{kernel-doc} include/trace/events/workqueue.h
:internal:
```
