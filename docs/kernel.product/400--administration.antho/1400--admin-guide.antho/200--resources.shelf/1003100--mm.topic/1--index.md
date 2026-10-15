---
title: "Memory Management"
type: reference
description: "Linux memory management subsystem is responsible, as the name implies, for managing the memory in the system. This includes implementation of virtual memory and demand paging, memory allocation both for kernel internal structures and user…"
---

<a id="rst-memory-management"></a>

Linux memory management subsystem is responsible, as the name implies, for managing the memory in the system. This includes implementation of virtual memory and demand paging, memory allocation both for kernel internal structures and user space programs, mapping of files into processes address space and many other cool things.

Linux memory management is a complex system with many configurable settings. Most of these settings are available via `/proc` filesystem and can be queried and adjusted using `sysctl`. These APIs are described in [Documentation/admin-guide/sysctl/vm.rst](~kernel/administration/admin-guide/sysctl/vm) and in [man 5 proc](<http://man7.org/linux/man-pages/man5/proc.5.html>).

<a id="rst-man-5-proc"></a>



Linux memory management has its own jargon and if you are not yet familiar with it, consider reading [Documentation/admin-guide/mm/concepts.rst](~kernel/administration/admin-guide/mm/concepts).

Here we document in detail how to interact with various mechanisms in the Linux memory management.

- [Concepts overview](<~kernel/administration/admin-guide/mm/concepts>)
- [CMA Debugfs Interface](<~kernel/administration/admin-guide/mm/cma-debugfs>)
- [DAMON: Data Access MONitoring and Access-aware System Operations](<~kernel/administration/admin-guide/mm-damon/index>)
- [HugeTLB Pages](<~kernel/administration/admin-guide/mm/hugetlbpage>)
- [Idle Page Tracking](<~kernel/administration/admin-guide/mm/idle-page-tracking>)
- [Kernel Samepage Merging](<~kernel/administration/admin-guide/mm/ksm>)
- [Memory Hot(Un)Plug](<~kernel/administration/admin-guide/mm/memory-hotplug>)
- [Multi-Gen LRU](<~kernel/administration/admin-guide/mm/multigen-lru>)
- [No-MMU memory mapping support](<~kernel/administration/admin-guide/mm/nommu-mmap>)
- [NUMA Memory Policy](<~kernel/administration/admin-guide/mm/numa-memory-policy>)
- [NUMA Memory Performance](<~kernel/administration/admin-guide/mm/numaperf>)
- [Examining Process Page Tables](<~kernel/administration/admin-guide/mm/pagemap>)
- [Shrinker Debugfs Interface](<~kernel/administration/admin-guide/mm/shrinker-debugfs>)
- [Short users guide for the slab allocator](<~kernel/administration/admin-guide/mm/slab>)
- [Soft-Dirty PTEs](<~kernel/administration/admin-guide/mm/soft-dirty>)
- [Transparent Hugepage Support](<~kernel/administration/admin-guide/mm/transhuge>)
- [Userfaultfd](<~kernel/administration/admin-guide/mm/userfaultfd>)
- [zswap](<~kernel/administration/admin-guide/mm/zswap>)
- [Kexec Handover Usage](<~kernel/administration/admin-guide/mm/kho>)
