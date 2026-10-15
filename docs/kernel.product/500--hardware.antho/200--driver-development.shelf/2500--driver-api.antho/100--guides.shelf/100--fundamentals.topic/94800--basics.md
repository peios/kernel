---
title: "Driver Basics"
type: reference
description: "Reference for Driver Basics."
---

<a id="rst-driver-basics"></a>

<a id="rst-driver-entry-and-exit-points"></a>

## Driver Entry and Exit points

```{kernel-doc} include/linux/module.h
:internal:
```

<a id="rst-driver-device-table"></a>

## Driver device table

```{kernel-doc} include/linux/mod_devicetable.h
:internal:
:no-identifiers: pci_device_id
```

<a id="rst-delaying-and-scheduling-routines"></a>

## Delaying and scheduling routines

```{kernel-doc} include/linux/sched.h
:internal:
```

```{kernel-doc} kernel/sched/core.c
:export:
```

```{kernel-doc} kernel/sched/cpupri.c
:internal:
```

```{kernel-doc} kernel/sched/fair.c
:internal:
```

```{kernel-doc} include/linux/completion.h
:internal:
```

<a id="rst-time-and-timer-routines"></a>

## Time and timer routines

```{kernel-doc} include/linux/jiffies.h
:internal:
```

```{kernel-doc} kernel/time/time.c
:export:
```

```{kernel-doc} kernel/time/timer.c
:export:
```

<a id="rst-high-resolution-timers"></a>

## High-resolution timers

```{kernel-doc} include/linux/ktime.h
:internal:
```

```{kernel-doc} include/linux/hrtimer.h
:internal:
```

```{kernel-doc} kernel/time/hrtimer.c
:export:
```

<a id="rst-wait-queues-and-wake-events"></a>

## Wait queues and Wake events

```{kernel-doc} include/linux/wait.h
:internal:
```

```{kernel-doc} kernel/sched/wait.c
:export:
```

<a id="rst-internal-functions"></a>

## Internal Functions

```{kernel-doc} kernel/exit.c
:internal:
```

```{kernel-doc} kernel/signal.c
:internal:
```

```{kernel-doc} include/linux/kthread.h
:internal:
```

```{kernel-doc} kernel/kthread.c
:export:
```

<a id="rst-reference-counting"></a>

## Reference counting

```{kernel-doc} include/linux/refcount.h
:internal:
```

```{kernel-doc} lib/refcount.c
:export:
```

<a id="rst-atomics"></a>

## Atomics

```{kernel-doc} include/linux/atomic/atomic-instrumented.h
:internal:
```

```{kernel-doc} include/linux/atomic/atomic-arch-fallback.h
:internal:
```

```{kernel-doc} include/linux/atomic/atomic-long.h
:internal:
```

<a id="rst-kernel-objects-manipulation"></a>

## Kernel objects manipulation

```{kernel-doc} lib/kobject.c
:export:
```

```{kernel-doc} lib/kobject_uevent.c
:export:
```

<a id="rst-kernel-utility-functions"></a>

## Kernel utility functions

```{kernel-doc} include/linux/array_size.h
:internal:
```

```{kernel-doc} include/linux/container_of.h
:internal:
```

```{kernel-doc} include/linux/kstrtox.h
:internal:
:no-identifiers: kstrtol kstrtoul
```

```{kernel-doc} include/linux/stddef.h
:internal:
```

```{kernel-doc} include/linux/util_macros.h
:internal:
```

```{kernel-doc} include/linux/wordpart.h
:internal:
```

```{kernel-doc} kernel/printk/printk.c
:export:
:no-identifiers: printk
```

```{kernel-doc} kernel/panic.c
:export:
```

<a id="rst-device-resource-management"></a>

## Device Resource Management

```{kernel-doc} drivers/base/devres.c
:export:
```
