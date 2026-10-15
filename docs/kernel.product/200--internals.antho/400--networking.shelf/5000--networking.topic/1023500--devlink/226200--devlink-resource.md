---
title: "Devlink Resource"
type: reference
description: "devlink provides the ability for drivers to register resources, which can allow administrators to see the device restrictions for a given resource, as well as how much of the given resource is currently in use. Additionally, these…"
---

<a id="rst-devlink-resource"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

`devlink` provides the ability for drivers to register resources, which can allow administrators to see the device restrictions for a given resource, as well as how much of the given resource is currently in use. Additionally, these resources can optionally have configurable size. This could enable the administrator to limit the number of resources that are used.

For example, the `netdevsim` driver enables `/IPv4/fib` and `/IPv4/fib-rules` as resources to limit the number of IPv4 FIB entries and rules for a given device.

<a id="rst-resource-ids"></a>

## Resource Ids

Each resource is represented by an id, and contains information about its current size and related sub resources. To access a sub resource, you specify the path of the resource. For example `/IPv4/fib` is the id for the `fib` sub-resource under the `IPv4` resource.

<a id="rst-generic-resources"></a>

## Generic Resources

Generic resources are used to describe resources that can be shared by multiple device drivers and their description must be added to the following table:


<table>
<caption>List of Generic Resources</caption>
<tbody>
<tr>
<td>


Name

</td>
<td>


Description

</td>
</tr>
<tr>
<td>


`physical_ports`

</td>
<td>


A limited capacity of physical ports that the switch ASIC can support

</td>
</tr>
</tbody>
</table>

<a id="rst-example-usage"></a>

### example usage

The resources exposed by the driver can be observed, for example:



```shell
$devlink resource show pci/0000:03:00.0
pci/0000:03:00.0:
  name kvd size 245760 unit entry
    resources:
      name linear size 98304 occ 0 unit entry size_min 0 size_max 147456 size_gran 128
      name hash_double size 60416 unit entry size_min 32768 size_max 180224 size_gran 128
      name hash_single size 87040 unit entry size_min 65536 size_max 212992 size_gran 128
```

Some resource's size can be changed. Examples:



```shell
$devlink resource set pci/0000:03:00.0 path /kvd/hash_single size 73088
$devlink resource set pci/0000:03:00.0 path /kvd/hash_double size 74368
```

The changes do not apply immediately, this can be validated by the 'size_new' attribute, which represents the pending change in size. For example:



```shell
$devlink resource show pci/0000:03:00.0
pci/0000:03:00.0:
  name kvd size 245760 unit entry size_valid false
  resources:
    name linear size 98304 size_new 147456 occ 0 unit entry size_min 0 size_max 147456 size_gran 128
    name hash_double size 60416 unit entry size_min 32768 size_max 180224 size_gran 128
    name hash_single size 87040 unit entry size_min 65536 size_max 212992 size_gran 128
```

Note that changes in resource size may require a device reload to properly take effect.
