---
title: "Texas Instruments K3 AM65 CPSW NUSS switchdev based ethernet driver"
type: reference
description: "In order to rename via udev:"
---

<a id="rst-texas-instruments-k3-am65-cpsw-nuss-switchdev-based-ethernet-driver"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

**Version:** 1.0

<a id="rst-port-renaming"></a>

## Port renaming

In order to rename via udev:



```text
ip -d link show dev sw0p1 | grep switchid

SUBSYSTEM=="net", ACTION=="add", ATTR{phys_switch_id}==<switchid>, \
        ATTR{phys_port_name}!="", NAME="sw0$attr{phys_port_name}"
```

<a id="rst-multi-mac-mode"></a>

## Multi mac mode

- The driver is operating in multi-mac mode by default, thus working as N individual network interfaces.

<a id="rst-devlink-configuration-parameters"></a>

## Devlink configuration parameters

See [Documentation/networking/devlink/am65-nuss-cpsw-switch.rst](~kernel/internals/networking/devlink/am65-nuss-cpsw-switch)

<a id="rst-enabling-switch"></a>

## Enabling "switch"

The Switch mode can be enabled by configuring devlink driver parameter "switch_mode" to 1/true:



```text
devlink dev param set platform/c000000.ethernet \
name switch_mode value true cmode runtime
```

This can be done regardless of the state of Port's netdev devices - UP/DOWN, but Port's netdev devices have to be in UP before joining to the bridge to avoid overwriting of bridge configuration as CPSW switch driver completely reloads its configuration when first port changes its state to UP.

When both interfaces have joined the bridge - CPSW switch driver will enable marking packets with offload_fwd_mark flag.

All configuration is implemented via switchdev API.

<a id="rst-bridge-setup"></a>

## Bridge setup



```text
devlink dev param set platform/c000000.ethernet \
name switch_mode value true cmode runtime

ip link add name br0 type bridge
ip link set dev br0 type bridge ageing_time 1000
ip link set dev sw0p1 up
ip link set dev sw0p2 up
ip link set dev sw0p1 master br0
ip link set dev sw0p2 master br0

[*] bridge vlan add dev br0 vid 1 pvid untagged self

[*] if vlan_filtering=1. where default_pvid=1

Note. Steps [*] are mandatory.
```

<a id="rst-on-off-stp"></a>

## On/off STP



```text
ip link set dev BRDEV type bridge stp_state 1/0
```

<a id="rst-vlan-configuration"></a>

## VLAN configuration



```text
bridge vlan add dev br0 vid 1 pvid untagged self <---- add cpu port to VLAN 1
```

Note. This step is mandatory for bridge/default_pvid.

<a id="rst-add-extra-vlans"></a>

## Add extra VLANs

> 1. untagged:
>
>
>
>    ```text
>    bridge vlan add dev sw0p1 vid 100 pvid untagged master
>    bridge vlan add dev sw0p2 vid 100 pvid untagged master
>    bridge vlan add dev br0 vid 100 pvid untagged self <---- Add cpu port to VLAN100
>    ```
>
> 2. tagged:
>
>
>
>    ```text
>    bridge vlan add dev sw0p1 vid 100 master
>    bridge vlan add dev sw0p2 vid 100 master
>    bridge vlan add dev br0 vid 100 pvid tagged self <---- Add cpu port to VLAN100
>    ```

<a id="rst-fdbs"></a>

### FDBs

FDBs are automatically added on the appropriate switch port upon detection

Manually adding FDBs:



```text
bridge fdb add aa:bb:cc:dd:ee:ff dev sw0p1 master vlan 100
bridge fdb add aa:bb:cc:dd:ee:fe dev sw0p2 master <---- Add on all VLANs
```

<a id="rst-mdbs"></a>

### MDBs

MDBs are automatically added on the appropriate switch port upon detection

Manually adding MDBs:



```text
bridge mdb add dev br0 port sw0p1 grp 239.1.1.1 permanent vid 100
bridge mdb add dev br0 port sw0p1 grp 239.1.1.1 permanent <---- Add on all VLANs
```

<a id="rst-multicast-flooding"></a>

## Multicast flooding

CPU port mcast_flooding is always on

Turning flooding on/off on switch ports: bridge link set dev sw0p1 mcast_flood on/off

<a id="rst-access-and-trunk-port"></a>

## Access and Trunk port



```text
bridge vlan add dev sw0p1 vid 100 pvid untagged master
bridge vlan add dev sw0p2 vid 100 master


bridge vlan add dev br0 vid 100 self
ip link add link br0 name br0.100 type vlan id 100
```

Note. Setting PVID on Bridge device itself works only for default VLAN (default_pvid).
