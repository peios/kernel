---
title: "PCI NTB Endpoint Function"
type: reference
description: "Create a subdirectory to pci_epf_ntb directory in configfs."
---

<a id="rst-pci-ntb-endpoint-function"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

1. Create a subdirectory to pci_epf_ntb directory in configfs.

Standard EPF Configurable Fields:


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


should be 0xb00d for TI's J721E SoC

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


should be 0x00

</td>
</tr>
<tr>
<td>


baseclass_code

</td>
<td>


should be 0x5

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


don't care

</td>
</tr>
<tr>
<td>


msi_interrupts

</td>
<td>


don't care

</td>
</tr>
<tr>
<td>


msix_interrupts

</td>
<td>


don't care

</td>
</tr>
</tbody>
</table>

2. Create a subdirectory to directory created in 1

NTB EPF specific configurable fields:


<table>
<tbody>
<tr>
<td>


db_count

</td>
<td>


Number of doorbells; default = 4

</td>
</tr>
<tr>
<td>


mw1

</td>
<td>


size of memory window1

</td>
</tr>
<tr>
<td>


mw2

</td>
<td>


size of memory window2

</td>
</tr>
<tr>
<td>


mw3

</td>
<td>


size of memory window3

</td>
</tr>
<tr>
<td>


mw4

</td>
<td>


size of memory window4

</td>
</tr>
<tr>
<td>


num_mws

</td>
<td>


Number of memory windows; max = 4

</td>
</tr>
<tr>
<td>


spad_count

</td>
<td>


Number of scratchpad registers; default = 64

</td>
</tr>
</tbody>
</table>
