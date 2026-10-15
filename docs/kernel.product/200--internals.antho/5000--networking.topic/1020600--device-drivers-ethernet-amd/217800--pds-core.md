---
title: "Linux Driver for the AMD/Pensando(R) DSC adapter family"
type: reference
description: "Copyright(c) 2023 Advanced Micro Devices, Inc"
---

<a id="rst-linux-driver-for-the-amd-pensando-r-dsc-adapter-family"></a>

<!-- SPDX-License-Identifier: GPL-2.0+ -->

Copyright(c) 2023 Advanced Micro Devices, Inc

<a id="rst-identifying-the-adapter"></a>

## Identifying the Adapter

To find if one or more AMD/Pensando PCI Core devices are installed on the host, check for the PCI devices:



```text
# lspci -d 1dd8:100c
b5:00.0 Processing accelerators: Pensando Systems Device 100c
b6:00.0 Processing accelerators: Pensando Systems Device 100c
```

If such devices are listed as above, then the pds_core.ko driver should find and configure them for use.  There should be log entries in the kernel messages such as these:



```text
$ dmesg | grep pds_core
pds_core 0000:b5:00.0: 252.048 Gb/s available PCIe bandwidth (16.0 GT/s PCIe x16 link)
pds_core 0000:b5:00.0: FW: 1.60.0-73
pds_core 0000:b6:00.0: 252.048 Gb/s available PCIe bandwidth (16.0 GT/s PCIe x16 link)
pds_core 0000:b6:00.0: FW: 1.60.0-73
```

Driver and firmware version information can be gathered with devlink:



```text
$ devlink dev info pci/0000:b5:00.0
pci/0000:b5:00.0:
  driver pds_core
  serial_number FLM18420073
  versions:
      fixed:
        asic.id 0x0
        asic.rev 0x0
      running:
        fw 1.51.0-73
      stored:
        fw.goldfw 1.15.9-C-22
        fw.mainfwa 1.60.0-73
        fw.mainfwb 1.60.0-57
```

<a id="rst-info-versions"></a>

## Info versions

The `pds_core` driver reports the following versions


<table>
<caption>devlink info versions implemented</caption>
<tbody>
<tr>
<td>


Name

</td>
<td>


Type

</td>
<td>


Description

</td>
</tr>
<tr>
<td>


`fw`

</td>
<td>


running

</td>
<td>


Version of firmware running on the device

</td>
</tr>
<tr>
<td>


`fw.goldfw`

</td>
<td>


stored

</td>
<td>


Version of firmware stored in the goldfw slot

</td>
</tr>
<tr>
<td>


`fw.mainfwa`

</td>
<td>


stored

</td>
<td>


Version of firmware stored in the mainfwa slot

</td>
</tr>
<tr>
<td>


`fw.mainfwb`

</td>
<td>


stored

</td>
<td>


Version of firmware stored in the mainfwb slot

</td>
</tr>
<tr>
<td>


`asic.id`

</td>
<td>


fixed

</td>
<td>


The ASIC type for this device

</td>
</tr>
<tr>
<td>


`asic.rev`

</td>
<td>


fixed

</td>
<td>


The revision of the ASIC for this device

</td>
</tr>
</tbody>
</table>

<a id="rst-parameters"></a>

## Parameters

The `pds_core` driver implements the following generic parameters for controlling the functionality to be made available as auxiliary_bus devices.


<table>
<caption>Generic parameters implemented</caption>
<tbody>
<tr>
<td>


Name

</td>
<td>


Mode

</td>
<td>


Type

</td>
<td>


Description

</td>
</tr>
<tr>
<td>


`enable_vnet`

</td>
<td>


runtime

</td>
<td>


Boolean

</td>
<td>


Enables vDPA functionality through an auxiliary_bus device

</td>
</tr>
</tbody>
</table>

<a id="rst-firmware-management"></a>

## Firmware Management

The `flash` command can update a the DSC firmware.  The downloaded firmware will be saved into either of firmware bank 1 or bank 2, whichever is not currently in use, and that bank will used for the next boot:



```text
# devlink dev flash pci/0000:b5:00.0 \
          file pensando/dsc_fw_1.63.0-22.tar
```

<a id="rst-health-reporters"></a>

## Health Reporters

The driver supports a devlink health reporter for FW status:



```text
# devlink health show pci/0000:2b:00.0 reporter fw
pci/0000:2b:00.0:
  reporter fw
    state healthy error 0 recover 0
# devlink health diagnose pci/0000:2b:00.0 reporter fw
 Status: healthy State: 1 Generation: 0 Recoveries: 0
```

<a id="rst-enabling-the-driver"></a>

## Enabling the driver

The driver is enabled via the standard kernel configuration system, using the make command:



```text
make oldconfig/menuconfig/etc.
```

The driver is located in the menu structure at:

> - **-&gt; Device Drivers**
>
>   - **-&gt; Network device support (NETDEVICES \[=y\])**
>
>     - **-&gt; Ethernet driver support**
>
>       - **-&gt; AMD devices**
>
>         -&gt; AMD/Pensando Ethernet PDS_CORE Support

<a id="rst-support"></a>

## Support

For general Linux networking support, please use the netdev mailing list, which is monitored by AMD/Pensando personnel:



```text
netdev@vger.kernel.org
```
