---
title: "HugeTLBpage on ARM64"
type: reference
description: "Hugepage relies on making efficient use of TLBs to improve performance of address translations. The benefit depends on both -"
---

<a id="rst-hugetlbpage-on-arm64"></a>
<a id="rst-hugetlbpage-index"></a>

Hugepage relies on making efficient use of TLBs to improve performance of address translations. The benefit depends on both -

> - the size of hugepages
>
> - size of entries supported by the TLBs

The ARM64 port supports two flavours of hugepages.

<a id="rst-block-mappings-at-the-pud-pmd-level"></a>

## 1) Block mappings at the pud/pmd level

These are regular hugepages where a pmd or a pud page table entry points to a block of memory. Regardless of the supported size of entries in TLB, block mappings reduce the depth of page table walk needed to translate hugepage addresses.

<a id="rst-using-the-contiguous-bit"></a>

## 2) Using the Contiguous bit

The architecture provides a contiguous bit in the translation table entries (D4.5.3, ARM DDI 0487C.a) that hints to the MMU to indicate that it is one of a contiguous set of entries that can be cached in a single TLB entry.

The contiguous bit is used in Linux to increase the mapping size at the pmd and pte (last) level. The number of supported contiguous entries varies by page size and level of the page table.

The following hugepage sizes are supported -

>
> <table>
> <thead>
> <tr>
> <th>
>
>
> - <!-- empty source list item -->
>
> </th>
> <th>
>
>
> CONT PTE
>
> </th>
> <th>
>
>
> PMD
>
> </th>
> <th>
>
>
> CONT PMD
>
> </th>
> <th>
>
>
> PUD
>
> </th>
> </tr>
> </thead>
> <tbody>
> <tr>
> <td>
>
>
> 4K:
>
> </td>
> <td>
>
>
> 64K
>
> </td>
> <td>
>
>
> 2M
>
> </td>
> <td>
>
>
> 32M
>
> </td>
> <td>
>
>
> 1G
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 16K:
>
> </td>
> <td>
>
>
> 2M
>
> </td>
> <td>
>
>
> 32M
>
> </td>
> <td>
>
>
> 1G
>
> </td>
> <td>
>
>
>
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 64K:
>
> </td>
> <td>
>
>
> 2M
>
> </td>
> <td>
>
>
> 512M
>
> </td>
> <td>
>
>
> 16G
>
> </td>
> <td>
>
>
>
>
> </td>
> </tr>
> </tbody>
> </table>
