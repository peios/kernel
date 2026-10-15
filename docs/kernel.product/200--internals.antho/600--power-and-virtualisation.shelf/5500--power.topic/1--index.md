---
title: "Power Management"
type: reference
description: "Reference for Power Management."
---

> **Peios:** The Peios profile forces integrity lockdown. Hibernation is unavailable under that policy, and kernel replacement must satisfy the kexec signature/lockdown path. The optional upstream mechanisms and test recipes below do not override those checks. Native privilege checks also apply. See [Peios kernel behaviour](<~kernel/introduction/peios-behaviour>).


<a id="rst-power-management"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

- [APM or ACPI?](<~kernel/internals/power/apm-acpi>)
- [Debugging hibernation and suspend](<~kernel/internals/power/basic-pm-debugging>)
- [Charger Manager](<~kernel/internals/power/charger-manager>)
- [Testing suspend and resume support in device drivers](<~kernel/internals/power/drivers-testing>)
- [Energy Model of devices](<~kernel/internals/power/energy-model>)
- [Freezing of tasks](<~kernel/internals/power/freezing-of-tasks>)
- [Operating Performance Points (OPP) Library](<~kernel/internals/power/opp>)
- [PCI Power Management](<~kernel/internals/power/pci>)
- [PM Quality Of Service Interface](<~kernel/internals/power/pm-qos-interface>)
- [Linux power supply class](<~kernel/internals/power/power-supply-class>)
- [Runtime Power Management Framework for I/O Devices](<~kernel/internals/power/runtime-pm>)
- [How to get s2ram working](<~kernel/internals/power/s2ram>)
- [Debugging Kernel Shutdown Hangs with pstore](<~kernel/internals/power/shutdown-debugging>)
- [Interaction of Suspend code (S3) with the CPU hotplug infrastructure](<~kernel/internals/power/suspend-and-cpuhotplug>)
- [System Suspend and Device Interrupts](<~kernel/internals/power/suspend-and-interrupts>)
- [Using swap files with software suspend (swsusp)](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/power/swsusp-and-swap-files.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)
- [How to use dm-crypt and swsusp together](<~kernel/internals/power/swsusp-dmcrypt>)
- [Swap suspend](<~kernel/internals/power/swsusp>)
- [Video issues with S3 resume](<~kernel/internals/power/video>)
- [swsusp/S3 tricks](<~kernel/internals/power/tricks>)
- [Documentation for userland software suspend interface](<~kernel/internals/power/userland-swsusp>)
- [Power Capping Framework](<~kernel/internals/power/powercap/powercap>)
- [Dynamic Thermal Power Management framework](<~kernel/internals/power/powercap/dtpm>)
- [Regulator Consumer Driver Interface](<~kernel/internals/power/regulator/consumer>)
- [Regulator API design notes](<~kernel/internals/power/regulator/design>)
- [Regulator Machine Driver Interface](<~kernel/internals/power/regulator/machine>)
- [Linux voltage and current regulator framework](<~kernel/internals/power/regulator/overview>)
- [Regulator Driver Interface](<~kernel/internals/power/regulator/regulator>)
