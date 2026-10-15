---
title: "Debugging advice for driver development"
type: reference
description: "This document serves as a general starting point and lookup for debugging device drivers. While this guide focuses on debugging that requires re-compiling the module/kernel, the userspace debugging guide…"
---

<a id="rst-debugging-advice-for-driver-development"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

This document serves as a general starting point and lookup for debugging device drivers. While this guide focuses on debugging that requires re-compiling the module/kernel, the [userspace debugging guide](<~kernel/development/process/debugging/userspace-debugging-guide>) will guide you through tools like dynamic debug, ftrace and other tools useful for debugging issues and behavior. For general debugging advice, see the [general advice document](<~kernel/development/process/debugging/index>).

<a id="rst-contents"></a>



The following sections show you the available tools.

<a id="rst-printk-friends"></a>

## printk() &amp; friends

These are derivatives of printf() with varying destinations and support for being dynamically turned on or off, or lack thereof.

<a id="rst-simple-printk"></a>

### Simple printk()

The classic, can be used to great effect for quick and dirty development of new modules or to extract arbitrary necessary data for troubleshooting.

Prerequisite: `CONFIG_PRINTK` (usually enabled by default)

<strong>Pros</strong>:

- No need to learn anything, simple to use

- Easy to modify exactly to your needs (formatting of the data (See: [How to get printk format specifiers right](<~kernel/internals/core-api/printk-formats>)), visibility in the log)

- Can cause delays in the execution of the code (beneficial to confirm whether timing is a factor)

<strong>Cons</strong>:

- Requires rebuilding the kernel/module

- Can cause delays in the execution of the code (which can cause issues to be not reproducible)

For the full documentation see [Message logging with printk](<~kernel/internals/core-api/printk-basics>)

<a id="rst-trace-printk"></a>

### Trace\_printk

Prerequisite: `CONFIG_DYNAMIC_FTRACE` &amp; `#include <linux/ftrace.h>`

It is a tiny bit less comfortable to use than printk(), because you will have to read the messages from the trace file (See: [Reading the ftrace log](<~kernel/development/process/debugging/userspace-debugging-guide#rst-read-ftrace-log>) instead of from the kernel log, but very useful when printk() adds unwanted delays into the code execution, causing issues to be flaky or hidden.)

If the processing of this still causes timing issues then you can try trace\_puts().

For the full Documentation see trace\_printk()

<a id="rst-dev-dbg"></a>

### dev\_dbg

Print statement, which can be targeted by [Dynamic debug](<~kernel/development/process/debugging/userspace-debugging-guide#rst-dynamic-debug>) that contains additional information about the device used within the context.

<strong>When is it appropriate to leave a debug print in the code?</strong>

Permanent debug statements have to be useful for a developer to troubleshoot driver misbehavior. Judging that is a bit more of an art than a science, but some guidelines are in the [Coding style guidelines](<~kernel/development/process/coding-style#rst-printing-kernel-messages>). In almost all cases the debug statements shouldn't be upstreamed, as a working driver is supposed to be silent.

<a id="rst-custom-printk"></a>

### Custom printk

Example:



```text
#define core_dbg(fmt, arg...) do { \
        if (core_debug) \
                printk(KERN_DEBUG pr_fmt("core: " fmt), ## arg); \
        } while (0)
```

<strong>When should you do this?</strong>

It is better to just use a pr\_debug(), which can later be turned on/off with dynamic debug. Additionally, a lot of drivers activate these prints via a variable like `core_debug` set by a module parameter. However, Module parameters [are not recommended anymore](<https://lore.kernel.org/all/2024032757-surcharge-grime-d3dd@gregkh>)<a id="rst-are-not-recommended-anymore"></a>.

<a id="rst-ftrace"></a>

## Ftrace

<a id="rst-creating-a-custom-ftrace-tracepoint"></a>

### Creating a custom Ftrace tracepoint

A tracepoint adds a hook into your code that will be called and logged when the tracepoint is enabled. This can be used, for example, to trace hitting a conditional branch or to dump the internal state at specific points of the code flow during a debugging session.

Here is a basic description of [how to implement new tracepoints](<~kernel/development/trace/tracepoints#rst-usage>).

For the full event tracing documentation see [Event Tracing](<~kernel/development/trace/events>)

For the full Ftrace documentation see [ftrace - Function Tracer](<~kernel/development/trace/ftrace>)

<a id="rst-debugfs"></a>

## DebugFS

Prerequisite: ``CONFIG_DEBUG_FS` & `#include <linux/debugfs.h>``

DebugFS differs from the other approaches of debugging, as it doesn't write messages to the kernel log nor add traces to the code. Instead it allows the developer to handle a set of files. With these files you can either store values of variables or make register/memory dumps or you can make these files writable and modify values/settings in the driver.

Possible use-cases among others:

- Store register values

- Keep track of variables

- Store errors

- Store settings

- Toggle a setting like debug on/off

- Error injection

This is especially useful, when the size of a data dump would be hard to digest as part of the general kernel log (for example when dumping raw bitstream data) or when you are not interested in all the values all the time, but with the possibility to inspect them.

The general idea is:

- Create a directory during probe (`struct dentry *parent = debugfs_create_dir("my_driver", NULL);`)

- Create a file (`debugfs_create_u32("my_value", 444, parent, &my_variable);`)

  - In this example the file is found in `/sys/kernel/debug/my_driver/my_value` (with read permissions for user/group/all)

  - any read of the file will return the current contents of the variable `my_variable`

- Clean up the directory when removing the device (`debugfs_remove(parent);`)

For the full documentation see [DebugFS](<~kernel/internals/filesystems/debugfs>).

<a id="rst-kasan-ubsan-lockdep-and-other-error-checkers"></a>

## KASAN, UBSAN, lockdep and other error checkers

<a id="rst-kasan-kernel-address-sanitizer"></a>

### KASAN (Kernel Address Sanitizer)

Prerequisite: `CONFIG_KASAN`

KASAN is a dynamic memory error detector that helps to find use-after-free and out-of-bounds bugs. It uses compile-time instrumentation to check every memory access.

For the full documentation see [Kernel Address Sanitizer (KASAN)](<~kernel/development/dev-tools/kasan>).

<a id="rst-ubsan-undefined-behavior-sanitizer"></a>

### UBSAN (Undefined Behavior Sanitizer)

Prerequisite: `CONFIG_UBSAN`

UBSAN relies on compiler instrumentation and runtime checks to detect undefined behavior. It is designed to find a variety of issues, including signed integer overflow, array index out of bounds, and more.

For the full documentation see [Undefined Behavior Sanitizer - UBSAN](<~kernel/development/dev-tools/ubsan>)

<a id="rst-lockdep-lock-dependency-validator"></a>

### lockdep (Lock Dependency Validator)

Prerequisite: `CONFIG_DEBUG_LOCKDEP`

lockdep is a runtime lock dependency validator that detects potential deadlocks and other locking-related issues in the kernel. It tracks lock acquisitions and releases, building a dependency graph that is analyzed for potential deadlocks. lockdep is especially useful for validating the correctness of lock ordering in the kernel.

<a id="rst-psi-pressure-stall-information-tracking"></a>

### PSI (Pressure stall information tracking)

Prerequisite: `CONFIG_PSI`

PSI is a measurement tool to identify excessive overcommits on hardware resources, that can cause performance disruptions or even OOM kills.

<a id="rst-device-coredump"></a>

## device coredump

Prerequisite: `CONFIG_DEV_COREDUMP` &amp; `#include <linux/devcoredump.h>`

Provides the infrastructure for a driver to provide arbitrary data to userland. It is most often used in conjunction with udev or similar userland application to listen for kernel uevents, which indicate that the dump is ready. Udev has rules to copy that file somewhere for long-term storage and analysis, as by default, the data for the dump is automatically cleaned up after a default 5 minutes. That data is analyzed with driver-specific tools or GDB.

A device coredump can be created with a vmalloc area, with read/free methods, or as a scatter/gather list.

You can find an example implementation at: [drivers/media/platform/qcom/venus/core.c](<https://elixir.bootlin.com/linux/v6.11.6/source/drivers/media/platform/qcom/venus/core.c#L30>), in the Bluetooth HCI layer, in several wireless drivers, and in several DRM drivers.

<a id="rst-devcoredump-interfaces"></a>

### devcoredump interfaces

```{kernel-doc} include/linux/devcoredump.h

```

```{kernel-doc} drivers/base/devcoredump.c

```

<strong>Copyright</strong> ©2024 : Collabora
