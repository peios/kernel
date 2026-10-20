---
title: "PCI vDPA driver for the AMD/Pensando(R) DSC adapter family"
type: reference
description: "AMD/Pensando vDPA VF Device Driver"
---

<a id="rst-pci-vdpa-driver-for-the-amd-pensando-r-dsc-adapter-family"></a>

<!-- SPDX-License-Identifier: GPL-2.0+ -->

<!-- note: can be edited and viewed with /usr/bin/formiko-vim -->

AMD/Pensando vDPA VF Device Driver

Copyright(c) 2023 Advanced Micro Devices, Inc

<a id="rst-overview"></a>

## Overview

The `pds_vdpa` driver is an auxiliary bus driver that supplies a vDPA device for use by the virtio network stack.  It is used with the Pensando Virtual Function devices that offer vDPA and virtio queue services.  It depends on the `pds_core` driver and hardware for the PF and VF PCI handling as well as for device configuration services.

<a id="rst-using-the-device"></a>

## Using the device

The `pds_vdpa` device is enabled via multiple configuration steps and depends on the `pds_core` driver to create and enable SR-IOV Virtual Function devices.  After the VFs are enabled, we enable the vDPA service in the `pds_core` device to create the auxiliary devices used by pds_vdpa.

Example steps:



```bash
#!/bin/bash

modprobe pds_core
modprobe vdpa
modprobe pds_vdpa

PF_BDF=`ls /sys/module/pds_core/drivers/pci\:pds_core/*/sriov_numvfs | awk -F / '{print $7}'`

# Enable vDPA VF auxiliary device(s) in the PF
devlink dev param set pci/$PF_BDF name enable_vnet cmode runtime value true

# Create a VF for vDPA use
echo 1 > /sys/bus/pci/drivers/pds_core/$PF_BDF/sriov_numvfs

# Find the vDPA services/devices available
PDS_VDPA_MGMT=`vdpa mgmtdev show | grep vDPA | head -1 | cut -d: -f1`

# Create a vDPA device for use in virtio network configurations
vdpa dev add name vdpa1 mgmtdev $PDS_VDPA_MGMT mac 00:11:22:33:44:55

# Set up an ethernet interface on the vdpa device
modprobe virtio_vdpa
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
>       - **-&gt; Pensando devices**
>
>         -&gt; Pensando Ethernet PDS_VDPA Support

<a id="rst-support"></a>

## Support

For general Linux networking support, please use the netdev mailing list, which is monitored by Pensando personnel:



```text
netdev@vger.kernel.org
```

For more specific support needs, please use the Pensando driver support email:



```text
drivers@pensando.io
```
