---
title: "Spear PCIe Gadget Driver"
type: reference
description: "Pratyush Anand (pratyush.anand@gmail.com)"
---

<a id="rst-spear-pcie-gadget-driver"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-author"></a>

## Author

Pratyush Anand ([pratyush.anand@gmail.com](<mailto:pratyush.anand@gmail.com>))

<a id="rst-location"></a>

## Location

driver/misc/spear13xx_pcie_gadget.c

<a id="rst-supported-chip"></a>

## Supported Chip:

SPEAr1300 SPEAr1310

<a id="rst-menuconfig-option"></a>

## Menuconfig option:

- **Device Drivers**

  - **Misc devices**

    PCIe gadget support for SPEAr13XX platform

<a id="rst-purpose"></a>

## purpose

This driver has several nodes which can be read/written by configfs interface. Its main purpose is to configure selected dual mode PCIe controller as device and then program its various registers to configure it as a particular device type. This driver can be used to show spear's PCIe device capability.

<a id="rst-description-of-different-nodes"></a>

## Description of different nodes:

<a id="rst-read-behavior-of-nodes"></a>

### read behavior of nodes:


<table>
<tbody>
<tr>
<td>


link

</td>
<td>


gives ltssm status.

</td>
</tr>
<tr>
<td>


int_type

</td>
<td>


type of supported interrupt

</td>
</tr>
<tr>
<td>


no_of_msi

</td>
<td>


zero if MSI is not enabled by host. A positive value is the number of MSI vector granted.

</td>
</tr>
<tr>
<td>


vendor_id

</td>
<td>


returns programmed vendor id (hex)

</td>
</tr>
<tr>
<td>


device_id

</td>
<td>


returns programmed device id(hex)

</td>
</tr>
<tr>
<td>


bar0_size:

</td>
<td>


returns size of bar0 in hex.

</td>
</tr>
<tr>
<td>


bar0_address

</td>
<td>


returns address of bar0 mapped area in hex.

</td>
</tr>
<tr>
<td>


bar0_rw_offset

</td>
<td>


returns offset of bar0 for which bar0_data will return value.

</td>
</tr>
<tr>
<td>


bar0_data

</td>
<td>


returns data at bar0_rw_offset.

</td>
</tr>
</tbody>
</table>

<a id="rst-write-behavior-of-nodes"></a>

### write behavior of nodes:


<table>
<tbody>
<tr>
<td>


link

</td>
<td>


write UP to enable ltsmm DOWN to disable

</td>
</tr>
<tr>
<td>


int_type

</td>
<td>


write interrupt type to be configured and (int_type could be INTA, MSI or NO_INT). Select MSI only when you have programmed no_of_msi node.

</td>
</tr>
<tr>
<td>


no_of_msi

</td>
<td>


number of MSI vector needed.

</td>
</tr>
<tr>
<td>


inta

</td>
<td>


write 1 to assert INTA and 0 to de-assert.

</td>
</tr>
<tr>
<td>


send_msi

</td>
<td>


write MSI vector to be sent.

</td>
</tr>
<tr>
<td>


vendor_id

</td>
<td>


write vendor id(hex) to be programmed.

</td>
</tr>
<tr>
<td>


device_id

</td>
<td>


write device id(hex) to be programmed.

</td>
</tr>
<tr>
<td>


bar0_size

</td>
<td>


write size of bar0 in hex. default bar0 size is 1000 (hex) bytes.

</td>
</tr>
<tr>
<td>


bar0_address

</td>
<td>


write   address of bar0 mapped area in hex. (default mapping of bar0 is SYSRAM1(E0800000). Always program bar size before bar address. Kernel might modify bar size and address for alignment, so read back bar size and address after writing to cross check.

</td>
</tr>
<tr>
<td>


bar0_rw_offset

</td>
<td>


write offset of bar0 for which  bar0_data will write value.

</td>
</tr>
<tr>
<td>


bar0_data

</td>
<td>


write data to be written at bar0_rw_offset.

</td>
</tr>
</tbody>
</table>

<a id="rst-node-programming-example"></a>

## Node programming example

Program all PCIe registers in such a way that when this device is connected to the PCIe host, then host sees this device as 1MB RAM.



```text
#mount -t configfs none /Config
```

For nth PCIe Device Controller:



```text
# cd /config/pcie_gadget.n/
```

Now you have all the nodes in this directory. program vendor id as 0x104a:



```text
# echo 104A >> vendor_id
```

program device id as 0xCD80:



```text
# echo CD80 >> device_id
```

program BAR0 size as 1MB:



```text
# echo 100000 >> bar0_size
```

check for programmed bar0 size:



```text
# cat bar0_size
```

Program BAR0 Address as DDR (0x2100000). This is the physical address of memory, which is to be made visible to PCIe host. Similarly any other peripheral can also be made visible to PCIe host. E.g., if you program base address of UART as BAR0 address then when this device will be connected to a host, it will be visible as UART.



```text
# echo 2100000 >> bar0_address
```

program interrupt type : INTA:



```text
# echo INTA >> int_type
```

go for link up now:



```text
# echo UP >> link
```

It will have to be insured that, once link up is done on gadget, then only host is initialized and start to search PCIe devices on its port.



```text
/*wait till link is up*/
# cat link
```

Wait till it returns UP.

To assert INTA:



```text
# echo 1 >> inta
```

To de-assert INTA:



```text
# echo 0 >> inta
```

if MSI is to be used as interrupt, program no of msi vector needed (say4):



```text
# echo 4 >> no_of_msi
```

select MSI as interrupt type:



```text
# echo MSI >> int_type
```

go for link up now:



```text
# echo UP >> link
```

wait till link is up:



```text
# cat link
```

An application can repetitively read this node till link is found UP. It can sleep between two read.

wait till msi is enabled:



```text
# cat no_of_msi
```

Should return 4 (number of requested MSI vector)

to send msi vector 2:



```text
# echo 2 >> send_msi
# cd -
```
