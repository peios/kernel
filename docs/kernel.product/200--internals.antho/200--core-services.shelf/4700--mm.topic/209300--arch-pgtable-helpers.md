---
title: "Architecture Page Table Helpers"
type: reference
description: "Generic MM expects architectures (with MMU) to provide helpers to create, access and modify page table entries at various level for different memory functions. These page table helpers need to conform to a common semantics across…"
---

<a id="rst-architecture-page-table-helpers"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

Generic MM expects architectures (with MMU) to provide helpers to create, access and modify page table entries at various level for different memory functions. These page table helpers need to conform to a common semantics across platforms. Following tables describe the expected semantics which can also be tested during boot via CONFIG_DEBUG_VM_PGTABLE option. All future changes in here or the debug test need to be in sync.

<a id="rst-pte-page-table-helpers"></a>

## PTE Page Table Helpers


<table>
<tbody>
<tr>
<td>


pte_same

</td>
<td>


Tests whether both PTE entries are the same

</td>
</tr>
<tr>
<td>


pte_present

</td>
<td>


Tests a valid mapped PTE

</td>
</tr>
<tr>
<td>


pte_young

</td>
<td>


Tests a young PTE

</td>
</tr>
<tr>
<td>


pte_dirty

</td>
<td>


Tests a dirty PTE

</td>
</tr>
<tr>
<td>


pte_write

</td>
<td>


Tests a writable PTE

</td>
</tr>
<tr>
<td>


pte_special

</td>
<td>


Tests a special PTE

</td>
</tr>
<tr>
<td>


pte_protnone

</td>
<td>


Tests a PROT_NONE PTE

</td>
</tr>
<tr>
<td>


pte_soft_dirty

</td>
<td>


Tests a soft dirty PTE

</td>
</tr>
<tr>
<td>


pte_swp_soft_dirty

</td>
<td>


Tests a soft dirty swapped PTE

</td>
</tr>
<tr>
<td>


pte_mkyoung

</td>
<td>


Creates a young PTE

</td>
</tr>
<tr>
<td>


pte_mkold

</td>
<td>


Creates an old PTE

</td>
</tr>
<tr>
<td>


pte_mkdirty

</td>
<td>


Creates a dirty PTE

</td>
</tr>
<tr>
<td>


pte_mkclean

</td>
<td>


Creates a clean PTE

</td>
</tr>
<tr>
<td>


pte_mkwrite

</td>
<td>


Creates a writable PTE of the type specified by the VMA.

</td>
</tr>
<tr>
<td>


pte_mkwrite_novma

</td>
<td>


Creates a writable PTE, of the conventional type of writable.

</td>
</tr>
<tr>
<td>


pte_wrprotect

</td>
<td>


Creates a write protected PTE

</td>
</tr>
<tr>
<td>


pte_mkspecial

</td>
<td>


Creates a special PTE

</td>
</tr>
<tr>
<td>


pte_mksoft_dirty

</td>
<td>


Creates a soft dirty PTE

</td>
</tr>
<tr>
<td>


pte_clear_soft_dirty

</td>
<td>


Clears a soft dirty PTE

</td>
</tr>
<tr>
<td>


pte_swp_mksoft_dirty

</td>
<td>


Creates a soft dirty swapped PTE

</td>
</tr>
<tr>
<td>


pte_swp_clear_soft_dirty

</td>
<td>


Clears a soft dirty swapped PTE

</td>
</tr>
<tr>
<td>


pte_mknotpresent

</td>
<td>


Invalidates a mapped PTE

</td>
</tr>
<tr>
<td>


ptep_clear

</td>
<td>


Clears a PTE

</td>
</tr>
<tr>
<td>


ptep_get_and_clear

</td>
<td>


Clears and returns PTE

</td>
</tr>
<tr>
<td>


ptep_get_and_clear_full

</td>
<td>


Clears and returns PTE (batched PTE unmap)

</td>
</tr>
<tr>
<td>


ptep_test_and_clear_young

</td>
<td>


Clears young from a PTE

</td>
</tr>
<tr>
<td>


ptep_set_wrprotect

</td>
<td>


Converts into a write protected PTE

</td>
</tr>
<tr>
<td>


ptep_set_access_flags

</td>
<td>


Converts into a more permissive PTE

</td>
</tr>
</tbody>
</table>

<a id="rst-pmd-page-table-helpers"></a>

## PMD Page Table Helpers


<table>
<tbody>
<tr>
<td>


pmd_same

</td>
<td>


Tests whether both PMD entries are the same

</td>
</tr>
<tr>
<td>


pmd_bad

</td>
<td>


Tests a non-table mapped PMD

</td>
</tr>
<tr>
<td>


pmd_leaf

</td>
<td>


Tests a leaf mapped PMD

</td>
</tr>
<tr>
<td>


pmd_trans_huge

</td>
<td>


Tests a Transparent Huge Page (THP) at PMD

</td>
</tr>
<tr>
<td>


pmd_present

</td>
<td>


Tests whether pmd_page() points to valid memory

</td>
</tr>
<tr>
<td>


pmd_young

</td>
<td>


Tests a young PMD

</td>
</tr>
<tr>
<td>


pmd_dirty

</td>
<td>


Tests a dirty PMD

</td>
</tr>
<tr>
<td>


pmd_write

</td>
<td>


Tests a writable PMD

</td>
</tr>
<tr>
<td>


pmd_special

</td>
<td>


Tests a special PMD

</td>
</tr>
<tr>
<td>


pmd_protnone

</td>
<td>


Tests a PROT_NONE PMD

</td>
</tr>
<tr>
<td>


pmd_soft_dirty

</td>
<td>


Tests a soft dirty PMD

</td>
</tr>
<tr>
<td>


pmd_swp_soft_dirty

</td>
<td>


Tests a soft dirty swapped PMD

</td>
</tr>
<tr>
<td>


pmd_mkyoung

</td>
<td>


Creates a young PMD

</td>
</tr>
<tr>
<td>


pmd_mkold

</td>
<td>


Creates an old PMD

</td>
</tr>
<tr>
<td>


pmd_mkdirty

</td>
<td>


Creates a dirty PMD

</td>
</tr>
<tr>
<td>


pmd_mkclean

</td>
<td>


Creates a clean PMD

</td>
</tr>
<tr>
<td>


pmd_mkwrite

</td>
<td>


Creates a writable PMD of the type specified by the VMA.

</td>
</tr>
<tr>
<td>


pmd_mkwrite_novma

</td>
<td>


Creates a writable PMD, of the conventional type of writable.

</td>
</tr>
<tr>
<td>


pmd_wrprotect

</td>
<td>


Creates a write protected PMD

</td>
</tr>
<tr>
<td>


pmd_mkspecial

</td>
<td>


Creates a special PMD

</td>
</tr>
<tr>
<td>


pmd_mksoft_dirty

</td>
<td>


Creates a soft dirty PMD

</td>
</tr>
<tr>
<td>


pmd_clear_soft_dirty

</td>
<td>


Clears a soft dirty PMD

</td>
</tr>
<tr>
<td>


pmd_swp_mksoft_dirty

</td>
<td>


Creates a soft dirty swapped PMD

</td>
</tr>
<tr>
<td>


pmd_swp_clear_soft_dirty

</td>
<td>


Clears a soft dirty swapped PMD

</td>
</tr>
<tr>
<td>


pmd_mkinvalid

</td>
<td>


Invalidates a present PMD; do not call for non-present PMD \[1\]

</td>
</tr>
<tr>
<td>


pmd_set_huge

</td>
<td>


Creates a PMD huge mapping

</td>
</tr>
<tr>
<td>


pmd_clear_huge

</td>
<td>


Clears a PMD huge mapping

</td>
</tr>
<tr>
<td>


pmdp_get_and_clear

</td>
<td>


Clears a PMD

</td>
</tr>
<tr>
<td>


pmdp_get_and_clear_full

</td>
<td>


Clears a PMD

</td>
</tr>
<tr>
<td>


pmdp_test_and_clear_young

</td>
<td>


Clears young from a PMD

</td>
</tr>
<tr>
<td>


pmdp_set_wrprotect

</td>
<td>


Converts into a write protected PMD

</td>
</tr>
<tr>
<td>


pmdp_set_access_flags

</td>
<td>


Converts into a more permissive PMD

</td>
</tr>
</tbody>
</table>

<a id="rst-pud-page-table-helpers"></a>

## PUD Page Table Helpers


<table>
<tbody>
<tr>
<td>


pud_same

</td>
<td>


Tests whether both PUD entries are the same

</td>
</tr>
<tr>
<td>


pud_bad

</td>
<td>


Tests a non-table mapped PUD

</td>
</tr>
<tr>
<td>


pud_leaf

</td>
<td>


Tests a leaf mapped PUD

</td>
</tr>
<tr>
<td>


pud_trans_huge

</td>
<td>


Tests a Transparent Huge Page (THP) at PUD

</td>
</tr>
<tr>
<td>


pud_present

</td>
<td>


Tests a valid mapped PUD

</td>
</tr>
<tr>
<td>


pud_young

</td>
<td>


Tests a young PUD

</td>
</tr>
<tr>
<td>


pud_dirty

</td>
<td>


Tests a dirty PUD

</td>
</tr>
<tr>
<td>


pud_write

</td>
<td>


Tests a writable PUD

</td>
</tr>
<tr>
<td>


pud_mkyoung

</td>
<td>


Creates a young PUD

</td>
</tr>
<tr>
<td>


pud_mkold

</td>
<td>


Creates an old PUD

</td>
</tr>
<tr>
<td>


pud_mkdirty

</td>
<td>


Creates a dirty PUD

</td>
</tr>
<tr>
<td>


pud_mkclean

</td>
<td>


Creates a clean PUD

</td>
</tr>
<tr>
<td>


pud_mkwrite

</td>
<td>


Creates a writable PUD

</td>
</tr>
<tr>
<td>


pud_wrprotect

</td>
<td>


Creates a write protected PUD

</td>
</tr>
<tr>
<td>


pud_mkinvalid

</td>
<td>


Invalidates a present PUD; do not call for non-present PUD \[1\]

</td>
</tr>
<tr>
<td>


pud_set_huge

</td>
<td>


Creates a PUD huge mapping

</td>
</tr>
<tr>
<td>


pud_clear_huge

</td>
<td>


Clears a PUD huge mapping

</td>
</tr>
<tr>
<td>


pudp_get_and_clear

</td>
<td>


Clears a PUD

</td>
</tr>
<tr>
<td>


pudp_get_and_clear_full

</td>
<td>


Clears a PUD

</td>
</tr>
<tr>
<td>


pudp_test_and_clear_young

</td>
<td>


Clears young from a PUD

</td>
</tr>
<tr>
<td>


pudp_set_wrprotect

</td>
<td>


Converts into a write protected PUD

</td>
</tr>
<tr>
<td>


pudp_set_access_flags

</td>
<td>


Converts into a more permissive PUD

</td>
</tr>
</tbody>
</table>

<a id="rst-hugetlb-page-table-helpers"></a>

## HugeTLB Page Table Helpers


<table>
<tbody>
<tr>
<td>


pte_huge

</td>
<td>


Tests a HugeTLB

</td>
</tr>
<tr>
<td>


arch_make_huge_pte

</td>
<td>


Creates a HugeTLB

</td>
</tr>
<tr>
<td>


huge_pte_dirty

</td>
<td>


Tests a dirty HugeTLB

</td>
</tr>
<tr>
<td>


huge_pte_write

</td>
<td>


Tests a writable HugeTLB

</td>
</tr>
<tr>
<td>


huge_pte_mkdirty

</td>
<td>


Creates a dirty HugeTLB

</td>
</tr>
<tr>
<td>


huge_pte_mkwrite

</td>
<td>


Creates a writable HugeTLB

</td>
</tr>
<tr>
<td>


huge_pte_wrprotect

</td>
<td>


Creates a write protected HugeTLB

</td>
</tr>
<tr>
<td>


huge_ptep_get_and_clear

</td>
<td>


Clears a HugeTLB

</td>
</tr>
<tr>
<td>


huge_ptep_set_wrprotect

</td>
<td>


Converts into a write protected HugeTLB

</td>
</tr>
<tr>
<td colspan="2">


huge_ptep_set_access_flags  \| Converts into a more permissive HugeTLB

</td>
</tr>
</tbody>
</table>

<a id="rst-swap-page-table-helpers"></a>

## SWAP Page Table Helpers


<table>
<tbody>
<tr>
<td>


\__pte_to_swp_entry

</td>
<td colspan="2">


Creates a swp_entry_t (arch) from a swap PTE

</td>
</tr>
<tr>
<td>


\__swp_entry_to_pte

</td>
<td colspan="2">


Creates a swap PTE from a swp_entry_t (arch)

</td>
</tr>
<tr>
<td>


\__pmd_to_swp_entry

</td>
<td colspan="2">


Creates a swp_entry_t (arch) from a swap PMD

</td>
</tr>
<tr>
<td>


\__swp_entry_to_pmd

</td>
<td colspan="2">


Creates a swap PMD from a swp_entry_t (arch)

</td>
</tr>
<tr>
<td colspan="3">


is_migration_entry        \| Tests a migration (read or write) swapped entry

</td>
</tr>
<tr>
<td colspan="2">


is_writable_migration_entry

</td>
<td>


Tests a write migration swapped entry

</td>
</tr>
<tr>
<td colspan="2">


make_readable_migration_entry

</td>
<td>


Creates a read migration swapped entry

</td>
</tr>
<tr>
<td colspan="2">


make_writable_migration_entry

</td>
<td>


Creates a write migration swapped entry

</td>
</tr>
</tbody>
</table>

\[1\] [https://lore.kernel.org/linux-mm/20181017020930.GN30832@redhat.com/](<https://lore.kernel.org/linux-mm/20181017020930.GN30832@redhat.com/>)
