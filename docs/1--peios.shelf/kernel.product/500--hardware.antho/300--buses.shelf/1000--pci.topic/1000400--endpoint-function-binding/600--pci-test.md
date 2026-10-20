---
title: "PCI Test Endpoint Function"
type: reference
description: "name: Should be \"pci_epf_test\" to bind to the pci_epf_test driver."
---

<a id="rst-pci-test-endpoint-function"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

name: Should be "pci_epf_test" to bind to the pci_epf_test driver.

Configurable Fields:


<table>
<tbody>
<tr>
<td>


vendorid

</td>
<td>


should be 0x104c

</td>
</tr>
<tr>
<td>


deviceid

</td>
<td>


should be 0xb500 for DRA74x and 0xb501 for DRA72x

</td>
</tr>
<tr>
<td>


revid

</td>
<td>


don't care

</td>
</tr>
<tr>
<td>


progif_code

</td>
<td>


don't care

</td>
</tr>
<tr>
<td>


subclass_code

</td>
<td>


don't care

</td>
</tr>
<tr>
<td>


baseclass_code

</td>
<td>


should be 0xff

</td>
</tr>
<tr>
<td>


cache_line_size

</td>
<td>


don't care

</td>
</tr>
<tr>
<td>


subsys_vendor_id

</td>
<td>


don't care

</td>
</tr>
<tr>
<td>


subsys_id

</td>
<td>


don't care

</td>
</tr>
<tr>
<td>


interrupt_pin

</td>
<td>


Should be 1 - INTA, 2 - INTB, 3 - INTC, 4 -INTD

</td>
</tr>
<tr>
<td>


msi_interrupts

</td>
<td>


Should be 1 to 32 depending on the number of MSI interrupts to test

</td>
</tr>
<tr>
<td>


msix_interrupts

</td>
<td>


Should be 1 to 2048 depending on the number of MSI-X interrupts to test

</td>
</tr>
</tbody>
</table>
