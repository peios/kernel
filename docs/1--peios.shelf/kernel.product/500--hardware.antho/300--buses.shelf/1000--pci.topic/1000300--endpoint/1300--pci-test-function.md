---
title: "PCI Test Function"
type: reference
description: "Traditionally PCI RC has always been validated by using standard PCI cards like ethernet PCI cards or USB PCI cards or SATA PCI cards. However with the addition of EP-core in linux kernel, it is possible to configure a PCI controller that…"
---

<a id="rst-pci-test-function"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

**Author:** Kishon Vijay Abraham I &lt;[kishon@ti.com](<mailto:kishon@ti.com>)&gt;

Traditionally PCI RC has always been validated by using standard PCI cards like ethernet PCI cards or USB PCI cards or SATA PCI cards. However with the addition of EP-core in linux kernel, it is possible to configure a PCI controller that can operate in EP mode to work as a test device.

The PCI endpoint test device is a virtual device (defined in software) used to test the endpoint functionality and serve as a sample driver for other PCI endpoint devices (to use the EP framework).

The PCI endpoint test device has the following registers:

> 1. PCI_ENDPOINT_TEST_MAGIC
>
> 2. PCI_ENDPOINT_TEST_COMMAND
>
> 3. PCI_ENDPOINT_TEST_STATUS
>
> 4. PCI_ENDPOINT_TEST_SRC_ADDR
>
> 5. PCI_ENDPOINT_TEST_DST_ADDR
>
> 6. PCI_ENDPOINT_TEST_SIZE
>
> 7. PCI_ENDPOINT_TEST_CHECKSUM
>
> 8. PCI_ENDPOINT_TEST_IRQ_TYPE
>
> 9. PCI_ENDPOINT_TEST_IRQ_NUMBER

- PCI_ENDPOINT_TEST_MAGIC

This register will be used to test BAR0. A known pattern will be written and read back from MAGIC register to verify BAR0.

- PCI_ENDPOINT_TEST_COMMAND

This register will be used by the host driver to indicate the function that the endpoint device must perform.


<table>
<thead>
<tr>
<th>


Bitfield

</th>
<th>


Description

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


Bit 0

</td>
<td>


raise legacy IRQ

</td>
</tr>
<tr>
<td>


Bit 1

</td>
<td>


raise MSI IRQ

</td>
</tr>
<tr>
<td>


Bit 2

</td>
<td>


raise MSI-X IRQ

</td>
</tr>
<tr>
<td>


Bit 3

</td>
<td>


read command (read data from RC buffer)

</td>
</tr>
<tr>
<td>


Bit 4

</td>
<td>


write command (write data to RC buffer)

</td>
</tr>
<tr>
<td>


Bit 5

</td>
<td>


copy command (copy data from one RC buffer to another RC buffer)

</td>
</tr>
</tbody>
</table>

- PCI_ENDPOINT_TEST_STATUS

This register reflects the status of the PCI endpoint device.


<table>
<thead>
<tr>
<th>


Bitfield

</th>
<th>


Description

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


Bit 0

</td>
<td>


read success

</td>
</tr>
<tr>
<td>


Bit 1

</td>
<td>


read fail

</td>
</tr>
<tr>
<td>


Bit 2

</td>
<td>


write success

</td>
</tr>
<tr>
<td>


Bit 3

</td>
<td>


write fail

</td>
</tr>
<tr>
<td>


Bit 4

</td>
<td>


copy success

</td>
</tr>
<tr>
<td>


Bit 5

</td>
<td>


copy fail

</td>
</tr>
<tr>
<td>


Bit 6

</td>
<td>


IRQ raised

</td>
</tr>
<tr>
<td>


Bit 7

</td>
<td>


source address is invalid

</td>
</tr>
<tr>
<td>


Bit 8

</td>
<td>


destination address is invalid

</td>
</tr>
</tbody>
</table>

- PCI_ENDPOINT_TEST_SRC_ADDR

This register contains the source address (RC buffer address) for the COPY/READ command.

- PCI_ENDPOINT_TEST_DST_ADDR

This register contains the destination address (RC buffer address) for the COPY/WRITE command.

- PCI_ENDPOINT_TEST_IRQ_TYPE

This register contains the interrupt type (Legacy/MSI) triggered for the READ/WRITE/COPY and raise IRQ (Legacy/MSI) commands.

Possible types:


<table>
<tbody>
<tr>
<td>


Legacy

</td>
<td>


0

</td>
</tr>
<tr>
<td>


MSI

</td>
<td>


1

</td>
</tr>
<tr>
<td>


MSI-X

</td>
<td>


2

</td>
</tr>
</tbody>
</table>

- PCI_ENDPOINT_TEST_IRQ_NUMBER

This register contains the triggered ID interrupt.

Admissible values:


<table>
<tbody>
<tr>
<td>


Legacy

</td>
<td>


0

</td>
</tr>
<tr>
<td>


MSI

</td>
<td>


\[1 .. 32\]

</td>
</tr>
<tr>
<td>


MSI-X

</td>
<td>


\[1 .. 2048\]

</td>
</tr>
</tbody>
</table>
