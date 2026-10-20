---
title: "Native kernel interfaces"
description: "Syscalls, handles and device interfaces provided by the Peios kernel."
type: guide
---

These references describe the native kernel interfaces used by applications and
system services. Generated tables give the values and layouts defined by this
kernel's UAPI headers; the accompanying articles explain validation, authority,
lifetime and error semantics.

- [KMES](<~kernel/userspace/native/kmes/overview>): event emission and ring attachment.
- [KACS](<~kernel/userspace/native/kacs/overview>): tokens, access checks, process and file authority.
- [LCS](<~kernel/userspace/native/lcs/overview>): registry keys, transactions, watches and source interfaces.
- [NTFE](<~kernel/userspace/native/ntfe/overview>): the packet engine's device, events and inspection ioctls.

For subsystem relationships, read [Kernel architecture](<~kernel/introduction/architecture-and-reading-guide>).
For SDK wrappers and application development guidance, use
[Developing for Peios](https://learn.peios.org/peios/developing-for-peios).
