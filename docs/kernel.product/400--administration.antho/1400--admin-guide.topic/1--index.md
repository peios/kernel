---
title: "The Linux kernel user's and administrator's guide"
type: reference
description: "The following is a collection of user-oriented documents that have been added to the kernel over time. There is, as yet, little overall order or organization here — this material was not written to be a single, coherent document! With luck…"
---

<a id="rst-the-linux-kernel-user-s-and-administrator-s-guide"></a>

The following is a collection of user-oriented documents that have been added to the kernel over time.  There is, as yet, little overall order or organization here — this material was not written to be a single, coherent document\!  With luck things will improve quickly over time.

<a id="rst-general-guides-to-kernel-administration"></a>

## General guides to kernel administration

This initial section contains overall information, including the README file describing the kernel as a whole, documentation on kernel parameters, etc.

- [Linux kernel release 6.x &lt;http://kernel.org/&gt;](<~kernel/administration/admin-guide/readme>)
- [Linux allocated devices (4.x+ version)](<~kernel/administration/admin-guide/devices>)
- [features](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/admin-guide/features.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)

A big part of the kernel's administrative interface is the /proc and sysfs virtual filesystems; these documents describe how to interact with tem

- [Rules on how to access information in sysfs](<~kernel/administration/admin-guide/sysfs-rules>)
- [Documentation for /proc/sys](<~kernel/administration/admin-guide/sysctl/index>)
- [How CPU topology info is exported via sysfs](<~kernel/administration/admin-guide/cputopology>)
- [abi](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/admin-guide/abi.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)

Security-related documentation:

- [Hardware vulnerabilities](<~kernel/administration/admin-guide/hw-vuln/index>)
- [Linux Security Module Usage](<~kernel/administration/admin-guide/lsm/index>)
- [Perf events and tool security](<~kernel/administration/admin-guide/perf-security>)

<a id="rst-booting-the-kernel"></a>

## Booting the kernel

- [Boot Configuration](<~kernel/administration/admin-guide/bootconfig>)
- [The kernel's command-line parameters](<~kernel/administration/admin-guide/kernel-parameters>)
- [The EFI Boot Stub](<~kernel/administration/admin-guide/efi-stub>)
- [Using the initial RAM disk (initrd)](<~kernel/administration/admin-guide/initrd>)

<a id="rst-tracking-down-and-identifying-problems"></a>

## Tracking down and identifying problems

Here is a set of documents aimed at users who are trying to track down problems and bugs in particular.

- [Reporting issues](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/admin-guide/reporting-issues.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)
- [Reporting regressions](<~kernel/administration/admin-guide/reporting-regressions>)
- [How to quickly build a trimmed Linux kernel](<~kernel/administration/admin-guide/quickly-build-trimmed-linux>)
- [How to verify bugs and bisect regressions](<~kernel/administration/admin-guide/verify-bugs-and-bisect-regressions>)
- [Bug hunting](<~kernel/administration/admin-guide/bug-hunting>)
- [Bisecting a regression](<~kernel/administration/admin-guide/bug-bisect>)
- [Tainted kernels](<~kernel/administration/admin-guide/tainted-kernels>)
- [Ramoops oops/panic logger](<~kernel/administration/admin-guide/ramoops>)
- [Dynamic debug](<~kernel/administration/admin-guide/dynamic-debug-howto>)
- [Explaining the "No working init found." boot hang message](<~kernel/administration/admin-guide/init>)
- [Documentation for Kdump - The kexec-based Crash Dumping Solution](<~kernel/administration/admin-guide/kdump/index>)
- [Performance monitor support](<~kernel/administration/admin-guide/perf/index>)
- [pstore block oops/panic logger](<~kernel/administration/admin-guide/pstore-blk>)
- [Clearing WARN_ONCE](<~kernel/administration/admin-guide/clearing-warn-once>)
- [Reducing OS jitter due to per-cpu kthreads](<~kernel/administration/admin-guide/kernel-per-cpu-kthreads>)
- [Softlockup detector and hardlockup detector (aka nmi_watchdog)](<~kernel/administration/admin-guide/lockup-watchdogs>)
- [index](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/admin-guide/RAS/index.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)
- [Linux Magic System Request Key Hacks](<~kernel/administration/admin-guide/sysrq>)

<a id="rst-core-kernel-subsystems"></a>

## Core-kernel subsystems

These documents describe core-kernel administration interfaces that are likely to be of interest on almost any system.

- [Control Group v2](<~kernel/administration/admin-guide/cgroup-v2>)
- [Control Groups version 1](<~kernel/administration/admin-guide/cgroup-v1/index>)
- [CPU load](<~kernel/administration/admin-guide/cpu-load>)
- [Memory Management](<~kernel/administration/admin-guide/mm/index>)
- [Kernel module signing facility](<~kernel/administration/admin-guide/module-signing>)
- [Namespaces](<~kernel/administration/admin-guide/namespaces/index>)
- [Numa policy hit/miss statistics](<~kernel/administration/admin-guide/numastat>)
- [Power Management](<~kernel/administration/admin-guide/pm/index>)
- [Syscall User Dispatch](<~kernel/administration/admin-guide/syscall-user-dispatch>)

Support for non-native binary formats.  Note that some of these documents are ... old ...

- [Kernel Support for miscellaneous Binary Formats (binfmt_misc)](<~kernel/administration/admin-guide/binfmt-misc>)
- [Java(tm) Binary Kernel Support for Linux v1.03](<~kernel/administration/admin-guide/java>)
- [Mono(tm) Binary Kernel Support for Linux](<~kernel/administration/admin-guide/mono>)

<a id="rst-block-layer-and-filesystem-administration"></a>

## Block-layer and filesystem administration

- [A block layer cache (bcache)](<~kernel/administration/admin-guide/bcache>)
- [The Android binderfs Filesystem](<~kernel/administration/admin-guide/binderfs>)
- [Block Devices](<~kernel/administration/admin-guide/blockdev/index>)
- [CIFS](<~kernel/administration/admin-guide/cifs/index>)
- [Device Mapper](<~kernel/administration/admin-guide/device-mapper/index>)
- [ext4 General Information](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/admin-guide/ext4.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)
- [File system Monitoring with fanotify](<~kernel/administration/admin-guide/filesystem-monitoring>)
- [NFS](<~kernel/administration/admin-guide/nfs/index>)
- [I/O statistics fields](<~kernel/administration/admin-guide/iostats>)
- [IBM's Journaled File System (JFS) for Linux](<~kernel/administration/admin-guide/jfs>)
- [RAID arrays](<~kernel/administration/admin-guide/md>)
- [Using UFS](<~kernel/administration/admin-guide/ufs>)
- [The SGI XFS Filesystem](<~kernel/administration/admin-guide/xfs>)

<a id="rst-device-specific-guides"></a>

## Device-specific guides

How to configure your hardware within your Linux system.

- [ACPI Support](<~kernel/administration/admin-guide/acpi/index>)
- [ATA over Ethernet (AoE)](<~kernel/administration/admin-guide/aoe/index>)
- [Auxiliary Display Support](<~kernel/administration/admin-guide/auxdisplay/index>)
- [Linux Braille Console](<~kernel/administration/admin-guide/braille-console>)
- [btmrvl driver](<~kernel/administration/admin-guide/btmrvl>)
- [Dell Remote BIOS Update driver (dell_rbu)](<~kernel/administration/admin-guide/dell-rbu>)
- [EDID](<~kernel/administration/admin-guide/edid>)
- [GPIO](<~kernel/administration/admin-guide/gpio/index>)
- [Hardware random number generators](<~kernel/administration/admin-guide/hw-random>)
- [Laptop Drivers](<~kernel/administration/admin-guide/laptops/index>)
- [Parallel port LCD/Keypad Panel support](<~kernel/administration/admin-guide/lcd-panel-cgram>)
- [Media subsystem admin and user guide](<~kernel/administration/admin-guide/media/index>)
- [Linux NVMe multipath](<~kernel/administration/admin-guide/nvme-multipath>)
- [Parport](<~kernel/administration/admin-guide/parport>)
- [Linux Plug and Play Documentation](<~kernel/administration/admin-guide/pnp>)
- [RapidIO Subsystem Guide](<~kernel/administration/admin-guide/rapidio>)
- [Real Time Clock (RTC) Drivers for Linux](<~kernel/administration/admin-guide/rtc>)
- [Linux Serial Console](<~kernel/administration/admin-guide/serial-console>)
- [Video Mode Selection Support 2.13](<~kernel/administration/admin-guide/svga>)
- [Thermal Subsystem](<~kernel/administration/admin-guide/thermal/index>)
- [USB4 and Thunderbolt](<~kernel/administration/admin-guide/thunderbolt>)
- [Software cursor for VGA](<~kernel/administration/admin-guide/vga-softcursor>)
- [Video Output Switcher Control](<~kernel/administration/admin-guide/video-output>)

<a id="rst-workload-analysis"></a>

## Workload analysis

This is the beginning of a section with information of interest to application developers and system integrators doing analysis of the Linux kernel for safety critical applications. Documents supporting analysis of kernel interactions with applications, and key kernel subsystems expectations will be found here.

- [Discovering Linux kernel subsystems used by a workload](<~kernel/administration/admin-guide/workload-tracing>)

<a id="rst-everything-else"></a>

## Everything else

A few hard-to-categorize and generally obsolete documents.

- [LDM - Logical Disk Manager (Dynamic Disks)](<~kernel/administration/admin-guide/ldm>)
- [Unicode support](<~kernel/administration/admin-guide/unicode>)
