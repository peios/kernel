---
title: "Memory Management Documentation"
type: reference
description: "This is a guide to understanding the memory management subsystem of Linux. If you are looking for advice on simply allocating memory, see the memory_allocation. For controlling and tuning guides, see the admin guide…"
---

<a id="rst-memory-management-documentation"></a>

This is a guide to understanding the memory management subsystem of Linux.  If you are looking for advice on simply allocating memory, see the [Memory Allocation Guide](<~kernel/internals/core-api/memory-allocation#rst-memory-allocation>).  For controlling and tuning guides, see the [admin guide](<~kernel/administration/admin-guide/mm/index>).

- [Physical Memory](<~kernel/internals/mm/physical-memory>)
- [Page Tables](<~kernel/internals/mm/page-tables>)
- [Process Addresses](<~kernel/internals/mm/process-addrs>)
- [Boot Memory](<~kernel/internals/mm/bootmem>)
- [Page Allocation](<~kernel/internals/mm/page-allocation>)
- [Virtually Contiguous Memory Allocation](<~kernel/internals/mm/vmalloc>)
- [Slab Allocation](<~kernel/internals/mm/slab>)
- [High Memory Handling](<~kernel/internals/mm/highmem>)
- [Page Reclaim](<~kernel/internals/mm/page-reclaim>)
- [Swap](<~kernel/internals/mm/swap>)
- [Swap Table](<~kernel/internals/mm/swap-table>)
- [Page Cache](<~kernel/internals/mm/page-cache>)
- [Shared Memory Filesystem](<~kernel/internals/mm/shmfs>)
- [Out Of Memory Handling](<~kernel/internals/mm/oom>)

<a id="rst-unsorted-documentation"></a>

## Unsorted Documentation

This is a collection of unsorted documents about the Linux memory management (MM) subsystem internals with different level of details ranging from notes and mailing list responses for elaborating descriptions of data structures and algorithms.  It should all be integrated nicely into the above structured documentation, or deleted if it has served its purpose.

- [Active MM](<~kernel/internals/mm/active-mm>)
- [MEMORY ALLOCATION PROFILING](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/mm/allocation-profiling.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)
- [Architecture Page Table Helpers](<~kernel/internals/mm/arch-pgtable-helpers>)
- [Memory Balancing](<~kernel/internals/mm/balance>)
- [DAMON: Data Access MONitoring and Access-aware System Operations](<~kernel/internals/mm/damon/index>)
- [Free Page Reporting](<~kernel/internals/mm/free-page-reporting>)
- [Heterogeneous Memory Management (HMM)](<~kernel/internals/mm/hmm>)
- [hwpoison](<~kernel/internals/mm/hwpoison>)
- [Hugetlbfs Reservation](<~kernel/internals/mm/hugetlbfs-reserv>)
- [Kernel Samepage Merging](<~kernel/internals/mm/ksm>)
- [Physical Memory Model](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/mm/memory-model.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)
- [Memfd Preservation via LUO](<~kernel/internals/mm/memfd-preservation>)
- [When do you need to notify inside page table lock ?](<~kernel/internals/mm/mmu-notifier>)
- [Multi-Gen LRU](<~kernel/internals/mm/multigen-lru>)
- [What is NUMA?](<~kernel/internals/mm/numa>)
- [Overcommit Accounting](<~kernel/internals/mm/overcommit-accounting>)
- [Page migration](<~kernel/internals/mm/page-migration>)
- [Page fragments](<~kernel/internals/mm/page-frags>)
- [page owner: Tracking about who allocated each page](<~kernel/internals/mm/page-owner>)
- [Page Table Check](<~kernel/internals/mm/page-table-check>)
- [remap_file_pages() system call](<~kernel/internals/mm/remap-file-pages>)
- [Split page table lock](<~kernel/internals/mm/split-page-table-lock>)
- [Transparent Hugepage Support](<~kernel/internals/mm/transhuge>)
- [Unevictable LRU Infrastructure](<~kernel/internals/mm/unevictable-lru>)
- [Virtually Mapped Kernel Stack Support](<~kernel/internals/mm/vmalloced-kernel-stacks>)
- [A vmemmap diet for HugeTLB and Device DAX](<~kernel/internals/mm/vmemmap-dedup>)
- [zsmalloc](<~kernel/internals/mm/zsmalloc>)
