---
title: "The Linux Kernel API"
type: reference
description: "When writing drivers, you cannot in general use routines which are from the C Library. Some of the functions have been found generally useful and they are listed below. The behaviour of these functions may vary slightly from those defined…"
---

<a id="rst-the-linux-kernel-api"></a>

<a id="rst-basic-c-library-functions"></a>

## Basic C Library Functions

When writing drivers, you cannot in general use routines which are from the C Library. Some of the functions have been found generally useful and they are listed below. The behaviour of these functions may vary slightly from those defined by ANSI, and these deviations are noted in the text.

<a id="rst-string-conversions"></a>

### String Conversions

```{kernel-doc} lib/vsprintf.c
:export:
```

```{kernel-doc} include/linux/kstrtox.h
:functions: kstrtol kstrtoul
```

```{kernel-doc} lib/kstrtox.c
:export:
```

```{kernel-doc} lib/string_helpers.c
:export:
```

<a id="rst-string-manipulation"></a>

### String Manipulation

```{kernel-doc} include/linux/fortify-string.h
:internal:
```

```{kernel-doc} lib/string.c
:export:
```

```{kernel-doc} include/linux/string.h
:internal:
```

```{kernel-doc} mm/util.c
:functions: kstrdup kstrdup_const kstrndup kmemdup kmemdup_nul memdup_user vmemdup_user strndup_user memdup_user_nul
```

<a id="rst-basic-kernel-library-functions"></a>

## Basic Kernel Library Functions

The Linux kernel provides more basic utility functions.

<a id="rst-bit-operations"></a>

### Bit Operations

```{kernel-doc} include/asm-generic/bitops/instrumented-atomic.h
:internal:
```

```{kernel-doc} include/asm-generic/bitops/instrumented-non-atomic.h
:internal:
```

```{kernel-doc} include/asm-generic/bitops/instrumented-lock.h
:internal:
```

<a id="rst-bitmap-operations"></a>

### Bitmap Operations

```{kernel-doc} lib/bitmap.c
:doc: bitmap introduction
```

```{kernel-doc} include/linux/bitmap.h
:doc: declare bitmap
```

```{kernel-doc} include/linux/bitmap.h
:doc: bitmap overview
```

```{kernel-doc} include/linux/bitmap.h
:doc: bitmap bitops
```

```{kernel-doc} lib/bitmap.c
:export:
```

```{kernel-doc} lib/bitmap.c
:internal:
```

```{kernel-doc} include/linux/bitmap.h
:internal:
```

<a id="rst-command-line-parsing"></a>

### Command-line Parsing

```{kernel-doc} lib/cmdline.c
:export:
```

<a id="rst-error-pointers"></a>

### Error Pointers

```{kernel-doc} include/linux/err.h
:internal:
```

<a id="rst-sorting"></a>

### Sorting

```{kernel-doc} lib/sort.c
:export:
```

```{kernel-doc} lib/list_sort.c
:export:
```

<a id="rst-text-searching"></a>

### Text Searching

```{kernel-doc} lib/textsearch.c
:doc: ts_intro
```

```{kernel-doc} lib/textsearch.c
:export:
```

```{kernel-doc} include/linux/textsearch.h
:functions: textsearch_find textsearch_next textsearch_get_pattern textsearch_get_pattern_len
```

<a id="rst-crc-and-math-functions-in-linux"></a>

## CRC and Math Functions in Linux

<a id="rst-arithmetic-overflow-checking"></a>

### Arithmetic Overflow Checking

```{kernel-doc} include/linux/overflow.h
:internal:
```

<a id="rst-crc-functions"></a>

### CRC Functions

```{kernel-doc} lib/crc/crc4.c
:export:
```

```{kernel-doc} lib/crc/crc7.c
:export:
```

```{kernel-doc} lib/crc/crc8.c
:export:
```

```{kernel-doc} lib/crc/crc16.c
:export:
```

```{kernel-doc} lib/crc/crc-ccitt.c
:export:
```

```{kernel-doc} lib/crc/crc-itu-t.c
:export:
```

```{kernel-doc} include/linux/crc32.h

```

```{kernel-doc} include/linux/crc64.h

```

<a id="rst-base-2-log-and-power-functions"></a>

### Base 2 log and power Functions

```{kernel-doc} include/linux/log2.h
:internal:
```

<a id="rst-integer-log-and-power-functions"></a>

### Integer log and power Functions

```{kernel-doc} include/linux/int_log.h

```

```{kernel-doc} lib/math/int_pow.c
:export:
```

```{kernel-doc} lib/math/int_sqrt.c
:export:
```

<a id="rst-division-functions"></a>

### Division Functions

```{kernel-doc} include/asm-generic/div64.h
:functions: do_div
```

```{kernel-doc} include/linux/math64.h
:internal:
```

```{kernel-doc} lib/math/gcd.c
:export:
```

<a id="rst-uuid-guid"></a>

### UUID/GUID

```{kernel-doc} lib/uuid.c
:export:
```

<a id="rst-kernel-ipc-facilities"></a>

## Kernel IPC facilities

<a id="rst-ipc-utilities"></a>

### IPC utilities

```{kernel-doc} ipc/util.c
:internal:
```

<a id="rst-fifo-buffer"></a>

## FIFO Buffer

<a id="rst-kfifo-interface"></a>

### kfifo interface

```{kernel-doc} include/linux/kfifo.h
:internal:
```

<a id="rst-relay-interface-support"></a>

## relay interface support

Relay interface support is designed to provide an efficient mechanism for tools and facilities to relay large amounts of data from kernel space to user space.

<a id="rst-relay-interface"></a>

### relay interface

```{kernel-doc} kernel/relay.c
:export:
```

```{kernel-doc} kernel/relay.c
:internal:
```

<a id="rst-module-support"></a>

## Module Support

<a id="rst-kernel-module-auto-loading"></a>

### Kernel module auto-loading

```{kernel-doc} kernel/module/kmod.c
:export:
```

<a id="rst-module-debugging"></a>

### Module debugging

```{kernel-doc} kernel/module/stats.c
:doc: module debugging statistics overview
```

<a id="rst-dup-failed-modules-tracks-duplicate-failed-modules"></a>

#### dup_failed_modules - tracks duplicate failed modules

```{kernel-doc} kernel/module/stats.c
:doc: dup_failed_modules - tracks duplicate failed modules
```

<a id="rst-module-statistics-debugfs-counters"></a>

#### module statistics debugfs counters

```{kernel-doc} kernel/module/stats.c
:doc: module statistics debugfs counters
```

<a id="rst-inter-module-support"></a>

### Inter Module support

Refer to the files in kernel/module/ for more information.

<a id="rst-hardware-interfaces"></a>

## Hardware Interfaces

<a id="rst-dma-channels"></a>

### DMA Channels

```{kernel-doc} kernel/dma.c
:export:
```

<a id="rst-resources-management"></a>

### Resources Management

```{kernel-doc} kernel/resource.c
:internal:
```

```{kernel-doc} kernel/resource.c
:export:
```

<a id="rst-mtrr-handling"></a>

### MTRR Handling

```{kernel-doc} arch/x86/kernel/cpu/mtrr/mtrr.c
:export:
```

<a id="rst-security-framework"></a>

## Security Framework

```{kernel-doc} security/security.c
:internal:
```

```{kernel-doc} security/inode.c
:export:
```

<a id="rst-audit-interfaces"></a>

## Audit Interfaces

```{kernel-doc} kernel/audit.c
:export:
```

```{kernel-doc} kernel/auditsc.c
:internal:
```

```{kernel-doc} kernel/auditfilter.c
:internal:
```

<a id="rst-accounting-framework"></a>

## Accounting Framework

```{kernel-doc} kernel/acct.c
:internal:
```

<a id="rst-block-devices"></a>

## Block Devices

```{kernel-doc} include/linux/bio.h

```

```{kernel-doc} block/blk-core.c
:export:
```

```{kernel-doc} block/blk-core.c
:internal:
```

```{kernel-doc} block/blk-map.c
:export:
```

```{kernel-doc} block/blk-sysfs.c
:internal:
```

```{kernel-doc} block/blk-settings.c
:export:
```

```{kernel-doc} block/blk-flush.c
:export:
```

```{kernel-doc} block/blk-lib.c
:export:
```

```{kernel-doc} block/blk-integrity.c
:export:
```

```{kernel-doc} kernel/trace/blktrace.c
:internal:
```

```{kernel-doc} block/genhd.c
:internal:
```

```{kernel-doc} block/genhd.c
:export:
```

```{kernel-doc} block/bdev.c
:export:
```

<a id="rst-char-devices"></a>

## Char devices

```{kernel-doc} fs/char_dev.c
:export:
```

<a id="rst-clock-framework"></a>

## Clock Framework

The clock framework defines programming interfaces to support software management of the system clock tree. This framework is widely used with System-On-Chip (SOC) platforms to support power management and various devices which may need custom clock rates. Note that these "clocks" don't relate to timekeeping or real time clocks (RTCs), each of which have separate frameworks. These `struct clk <clk>` instances may be used to manage for example a 96 MHz signal that is used to shift bits into and out of peripherals or busses, or otherwise trigger synchronous state machine transitions in system hardware.

Power management is supported by explicit software clock gating: unused clocks are disabled, so the system doesn't waste power changing the state of transistors that aren't in active use. On some systems this may be backed by hardware clock gating, where clocks are gated without being disabled in software. Sections of chips that are powered but not clocked may be able to retain their last state. This low power state is often called a *retention mode*. This mode still incurs leakage currents, especially with finer circuit geometries, but for CMOS circuits power is mostly used by clocked state changes.

Power-aware drivers only enable their clocks when the device they manage is in active use. Also, system sleep states often differ according to which clock domains are active: while a "standby" state may allow wakeup from several active domains, a "mem" (suspend-to-RAM) state may require a more wholesale shutdown of clocks derived from higher speed PLLs and oscillators, limiting the number of possible wakeup event sources. A driver's suspend method may need to be aware of system-specific clock constraints on the target sleep state.

Some platforms support programmable clock generators. These can be used by external chips of various kinds, such as other CPUs, multimedia codecs, and devices with strict requirements for interface clocking.

```{kernel-doc} include/linux/clk.h
:internal:
```

<a id="rst-synchronization-primitives"></a>

## Synchronization Primitives

<a id="rst-read-copy-update-rcu"></a>

### Read-Copy Update (RCU)

```{kernel-doc} include/linux/rcupdate.h

```

```{kernel-doc} kernel/rcu/tree.c

```

```{kernel-doc} kernel/rcu/tree_exp.h

```

```{kernel-doc} kernel/rcu/update.c

```

```{kernel-doc} include/linux/srcu.h

```

```{kernel-doc} kernel/rcu/srcutree.c

```

```{kernel-doc} include/linux/rculist_bl.h

```

```{kernel-doc} include/linux/rculist.h

```

```{kernel-doc} include/linux/rculist_nulls.h

```

```{kernel-doc} include/linux/rcu_sync.h

```

```{kernel-doc} kernel/rcu/sync.c

```

```{kernel-doc} kernel/rcu/tasks.h

```

```{kernel-doc} kernel/rcu/tree_stall.h

```

```{kernel-doc} include/linux/rcupdate_trace.h

```

```{kernel-doc} include/linux/rcupdate_wait.h

```

```{kernel-doc} include/linux/rcuref.h

```

```{kernel-doc} include/linux/rcutree.h

```
