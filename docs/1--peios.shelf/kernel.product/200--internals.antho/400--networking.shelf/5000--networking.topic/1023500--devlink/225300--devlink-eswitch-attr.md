---
title: "Devlink E-Switch Attribute"
type: reference
description: "Devlink E-Switch supports two modes of operation: legacy and switchdev. Legacy mode operates based on traditional MAC/VLAN steering rules. Switching decisions are made based on MAC addresses, VLANs, etc. There is limited ability to offload…"
---

<a id="rst-devlink-e-switch-attribute"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

Devlink E-Switch supports two modes of operation: legacy and switchdev. Legacy mode operates based on traditional MAC/VLAN steering rules. Switching decisions are made based on MAC addresses, VLANs, etc. There is limited ability to offload switching rules to hardware.

On the other hand, switchdev mode allows for more advanced offloading capabilities of the E-Switch to hardware. In switchdev mode, more switching rules and logic can be offloaded to the hardware switch ASIC. It enables representor netdevices that represent the slow path of virtual functions (VFs) or scalable-functions (SFs) of the device. See more information about [Documentation/networking/switchdev.rst](<~kernel/internals/networking/switchdev#rst-switchdev>) and [Documentation/networking/representors.rst](<~kernel/internals/networking/representors#rst-representors>).

In addition, the devlink E-Switch also comes with other attributes listed in the following section.

<a id="rst-attributes-description"></a>

## Attributes Description

The following is a list of E-Switch attributes.


<table>
<caption>E-Switch attributes</caption>
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


`mode`

</td>
<td>


enum

</td>
<td>


The mode of the device. The mode can be one of the following:

- `legacy` operates based on traditional MAC/VLAN steering rules.

- `switchdev` allows for more advanced offloading capabilities of the E-Switch to hardware.

- `switchdev_inactive` switchdev mode but starts inactive, doesn't allow traffic until explicitly activated. This mode is useful for orchestrators that want to prepare the device in switchdev mode but only activate it when all configurations are done.

</td>
</tr>
<tr>
<td>


`inline-mode`

</td>
<td>


enum

</td>
<td>


Some HWs need the VF driver to put part of the packet headers on the TX descriptor so the e-switch can do proper matching and steering. Support for both switchdev mode and legacy mode.

- `none` none.

- `link` L2 mode.

- `network` L3 mode.

- `transport` L4 mode.

</td>
</tr>
<tr>
<td>


`encap-mode`

</td>
<td>


enum

</td>
<td>


The encapsulation mode of the device. Support for both switchdev mode and legacy mode. The mode can be one of the following:

- `none` Disable encapsulation support.

- `basic` Enable encapsulation support.

</td>
</tr>
</tbody>
</table>

<a id="rst-example-usage"></a>

## Example Usage



```shell
# enable switchdev mode
$ devlink dev eswitch set pci/0000:08:00.0 mode switchdev

# set inline-mode and encap-mode
$ devlink dev eswitch set pci/0000:08:00.0 inline-mode none encap-mode basic

# display devlink device eswitch attributes
$ devlink dev eswitch show pci/0000:08:00.0
  pci/0000:08:00.0: mode switchdev inline-mode none encap-mode basic

# enable encap-mode with legacy mode
$ devlink dev eswitch set pci/0000:08:00.0 mode legacy inline-mode none encap-mode basic

# start switchdev mode in inactive state
$ devlink dev eswitch set pci/0000:08:00.0 mode switchdev_inactive

# setup switchdev configurations, representors, FDB entries, etc..
...

# activate switchdev mode to allow traffic
$ devlink dev eswitch set pci/0000:08:00.0 mode switchdev
```
