---
title: "The Peios Kernel"
type: guide
description: "Find operating guides, development guidance and kernel reference."
---

The Peios kernel is based on Linux. It manages hardware and system resources,
and provides the fundamental services used by the rest of the Peios operating system.

Start with [Peios kernel behaviour](<~kernel/introduction/peios-behaviour>) for native authority, process access,
filesystems and network policy.

Choose a starting point for the work you are doing:

- **Operate a system:** [Administration](<~kernel/administration/admin-guide/overview/index>)
  covers boot configuration, resource controls, storage, diagnostics and recovery.
- **Build or change the kernel:** [Kernel development](<~kernel/development/start-here/overview>)
  brings together building, programming, testing, tracing and contribution guidance.
- **Understand how it works:** [Internals](<~kernel/internals/start-here/overview>)
  follows execution, memory, storage, networking and security through the kernel.
- **Work with hardware:** [Hardware and drivers](<~kernel/hardware/start-here/overview>)
  connects driver development with buses, devices, firmware and processor architectures.
- **Use an interface:** [Userspace interfaces](<~kernel/userspace/userspace-api/overview/index>)
  documents system calls, device interfaces and protocol ABIs.

Within each section, shelves group related topics. The device-tree binding
catalogue is a separate reference collection under Hardware and drivers, so it
can be browsed by device class without overwhelming the guides.

This collection includes documentation inherited from Linux. Architecture,
device and interface reference coverage does not by itself indicate which
features are enabled or qualified in a particular Peios build.

## Native Peios subsystems

[Kernel architecture and reading guide](<~kernel/introduction/architecture-and-reading-guide>) connects KACS, KMES, LCS, StrataFS and NTFE. For callers, start with [Native kernel interfaces](<~kernel/userspace/native/start-here/overview>).
