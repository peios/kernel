---
title: "netdevsim devlink support"
type: reference
description: "This document describes the devlink features supported by the netdevsim device driver."
---

<a id="rst-netdevsim-devlink-support"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

This document describes the `devlink` features supported by the `netdevsim` device driver.

<a id="rst-parameters"></a>

## Parameters


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
</tr>
<tr>
<td>


`max_macs`

</td>
<td>


driverinit

</td>
</tr>
</tbody>
</table>

The `netdevsim` driver also implements the following driver-specific parameters.


<table>
<caption>Driver-specific parameters implemented</caption>
<tbody>
<tr>
<td>


Name

</td>
<td>


Type

</td>
<td>


Mode

</td>
<td>


Description

</td>
</tr>
<tr>
<td>


`test1`

</td>
<td>


Boolean

</td>
<td>


driverinit

</td>
<td>


Test parameter used to show how a driver-specific devlink parameter can be implemented.

</td>
</tr>
</tbody>
</table>

The `netdevsim` driver supports reloading via `DEVLINK_CMD_RELOAD`

<a id="rst-regions"></a>

## Regions

The `netdevsim` driver exposes a `dummy` region as an example of how the devlink-region interfaces work. A snapshot is taken whenever the `take_snapshot` debugfs file is written to.

<a id="rst-resources"></a>

## Resources

The `netdevsim` driver exposes resources to control the number of FIB entries, FIB rule entries and nexthops that the driver will allow.



```shell
$ devlink resource set netdevsim/netdevsim0 path /IPv4/fib size 96
$ devlink resource set netdevsim/netdevsim0 path /IPv4/fib-rules size 16
$ devlink resource set netdevsim/netdevsim0 path /IPv6/fib size 64
$ devlink resource set netdevsim/netdevsim0 path /IPv6/fib-rules size 16
$ devlink resource set netdevsim/netdevsim0 path /nexthops size 16
$ devlink dev reload netdevsim/netdevsim0
```

<a id="rst-rate-objects"></a>

## Rate objects

The `netdevsim` driver supports rate objects management, which includes:

- registering/unregistering leaf rate objects per VF devlink port;

- creation/deletion node rate objects;

- setting tx_share and tx_max rate values for any rate object type;

- setting parent node for any rate object type.

Rate nodes and their parameters are exposed in `netdevsim` debugfs in RO mode. For example created rate node with name `some_group`:



```shell
$ ls /sys/kernel/debug/netdevsim/netdevsim0/rate_groups/some_group
rate_parent  tx_max  tx_share
```

Same parameters are exposed for leaf objects in corresponding ports directories. For ex.:



```shell
$ ls /sys/kernel/debug/netdevsim/netdevsim0/ports/1
dev  ethtool  rate_parent  tx_max  tx_share
```

<a id="rst-driver-specific-traps"></a>

## Driver-specific Traps


<table>
<caption>List of Driver-specific Traps Registered by netdevsim</caption>
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


`fid_miss`

</td>
<td>


`exception`

</td>
<td>


When a packet enters the device it is classified to a filtering identifier (FID) based on the ingress port and VLAN. This trap is used to trap packets for which a FID could not be found

</td>
</tr>
</tbody>
</table>
