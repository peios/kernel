---
title: "Debugging advice for Linux Kernel developers"
type: reference
description: "Depending on the issue, a different set of tools is available to track down the problem or even to realize whether there is one in the first place."
---

> **Peios:** This is inherited Linux development and upstream contribution guidance. For Peios repository changes, follow [Peios Standards and Conventions](https://learn.peios.org/psc/) and use [Building Peios](<~kernel/development/start-here/building-peios>). Upstream mailing lists, maintainer roles and release processes below apply when contributing to Linux upstream.


<a id="rst-debugging-advice-for-linux-kernel-developers"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-general-guides"></a>

## general guides

- [Debugging advice for driver development](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/process/debugging/driver_development_debugging_guide.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)
- [Debugging kernel and modules via gdb](<~kernel/development/process/debugging/gdb-kernel-debugging>)
- [Using kgdb, kdb and the kernel debugger internals](<~kernel/development/process/debugging/kgdb>)
- [Userspace debugging advice](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/process/debugging/userspace_debugging_guide.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)

<a id="rst-subsystem-specific-guides"></a>

## subsystem specific guides

- [Debugging and tracing in the media subsystem](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/process/debugging/media_specific_debugging_guide.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)

<a id="rst-general-debugging-advice"></a>

### General debugging advice

Depending on the issue, a different set of tools is available to track down the problem or even to realize whether there is one in the first place.

As a first step you have to figure out what kind of issue you want to debug. Depending on the answer, your methodology and choice of tools may vary.

<a id="rst-do-i-need-to-debug-with-limited-access"></a>

## Do I need to debug with limited access?

Do you have limited access to the machine or are you unable to stop the running execution?

In this case your debugging capability depends on built-in debugging support of provided distribution kernel. The [Userspace debugging advice](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/process/debugging/userspace_debugging_guide.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) provides a brief overview over a range of possible debugging tools in that situation. You can check the capability of your kernel, in most cases, by looking into config file within the /boot directory.

<a id="rst-do-i-have-root-access-to-the-system"></a>

## Do I have root access to the system?

Are you easily able to replace the module in question or to install a new kernel?

In that case your range of available tools is a lot bigger, you can find the tools in the [Debugging advice for driver development](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/process/debugging/driver_development_debugging_guide.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>).

<a id="rst-is-timing-a-factor"></a>

## Is timing a factor?

It is important to understand if the problem you want to debug manifests itself consistently (i.e. given a set of inputs you always get the same, incorrect output), or inconsistently. If it manifests itself inconsistently, some timing factor might be at play. If inserting delays into the code does change the behavior, then quite likely timing is a factor.

When timing does alter the outcome of the code execution using a simple printk() for debugging purposes may not work, a similar alternative is to use trace_printk() , which logs the debug messages to the trace file instead of the kernel log.

**Copyright** ©2024 : Collabora
