---
title: "Understanding the kernel"
type: guide
description: "A reading path through the kernel implementation."
---

Start with the subsystem you are investigating. The shelves group mechanisms
that commonly need to be understood together.

- **Concurrency and synchronisation:** begin with [Locking](<~kernel/internals/locking/overview>),
  then explore [Scheduling](<~kernel/internals/scheduler/index>) and [RCU](<~kernel/internals/rcu/index>).
- **Core services and memory:** use [Core APIs](<~kernel/internals/core-api/index>) for
  shared facilities and [Memory management](<~kernel/internals/mm/index>) for allocation,
  address spaces and reclaim. [BPF](<~kernel/internals/bpf/index>) covers in-kernel programs.
- **Storage and filesystems:** follow the [Block layer](<~kernel/internals/block/index>)
  and [Filesystem interfaces](<~kernel/internals/filesystems/index>).
- **Networking:** start with [Networking](<~kernel/internals/networking/index>), then
  use [Netlink](<~kernel/internals/netlink/specs/index>) for protocol specifications and messaging.
- **Security and cryptography:** see [Security](<~kernel/internals/security/index>)
  and [Cryptographic APIs](<~kernel/internals/crypto/index>).
- **Power and virtualisation:** see [Power management](<~kernel/internals/power/index>)
  and [Virtualisation](<~kernel/internals/virt/index>).

For tuning a running system, use [Administration](<~kernel/administration/admin-guide/overview/index>).
For implementing or testing a change, use [Kernel development](<~kernel/development/start-here/overview>).
