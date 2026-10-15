---
title: "Enabling the driver and kconfig options"
type: reference
description: "CONFIG_MLX5_BRIDGE=(y/n)"
---

<a id="rst-enabling-the-driver-and-kconfig-options"></a>

<!-- SPDX-License-Identifier: GPL-2.0 OR Linux-OpenIB -->

<!-- This data file has been placed in the public domain. -->

<!-- Derived from the Unicode character mappings available from
<http://www.w3.org/2003/entities/xml/>.
Processed by unicode2rstsubs.py, part of Docutils:
<https://docutils.sourceforge.io>. -->

**Copyright:** © 2023, NVIDIA CORPORATION &amp; AFFILIATES. All rights reserved.

mlx5 core is modular and most of the major mlx5 core driver features can be selected (compiled in/out)<br>
at build time via kernel Kconfig flags.<br>
Basic features, ethernet net device rx/tx offloads and XDP, are available with the most basic flags<br>
CONFIG\_MLX5\_CORE=y/m and CONFIG\_MLX5\_CORE\_EN=y.<br>
For the list of advanced features, please see below.

<strong>CONFIG\_MLX5\_BRIDGE=(y/n)</strong>

Enable [Ethernet Bridging (BRIDGE) offloading support](<~kernel/internals/networking/device-drivers-ethernet-mellanox-mlx5/switchdev#rst-mlx5-bridge-offload>).<br>
This will provide the ability to add representors of mlx5 uplink and VF<br>
ports to Bridge and offloading rules for traffic between such ports.<br>
Supports VLANs (trunk and access modes).

<strong>CONFIG\_MLX5\_CORE=(y/m/n)</strong> (module mlx5\_core.ko)

The driver can be enabled by choosing CONFIG\_MLX5\_CORE=y/m in kernel config.<br>
This will provide mlx5 core driver for mlx5 ulps to interface with (mlx5e, mlx5\_ib).

<strong>CONFIG\_MLX5\_CORE\_EN=(y/n)</strong>

Choosing this option will allow basic ethernet netdevice support with all of the standard rx/tx offloads.<br>
mlx5e is the mlx5 ulp driver which provides netdevice kernel interface, when chosen, mlx5e will be<br>
built-in into mlx5\_core.ko.

<strong>CONFIG\_MLX5\_CORE\_EN\_DCB=(y/n)</strong>:

Enables [Data Center Bridging (DCB) Support](<https://enterprise-support.nvidia.com/s/article/howto-auto-config-pfc-and-ets-on-connectx-4-via-lldp-dcbx>)<a id="rst-data-center-bridging-dcb-support"></a>.

<strong>CONFIG\_MLX5\_CORE\_IPOIB=(y/n)</strong>

IPoIB offloads &amp; acceleration support.<br>
Requires CONFIG\_MLX5\_CORE\_EN to provide an accelerated interface for the rdma<br>
IPoIB ulp netdevice.

<strong>CONFIG\_MLX5\_CLS\_ACT=(y/n)</strong>

Enables offload support for TC classifier action (NET\_CLS\_ACT).<br>
Works in both native NIC mode and Switchdev SRIOV mode.<br>
Flow-based classifiers, such as those registered through<br>
`tc-flower(8)`, are processed by the device, rather than the<br>
host. Actions that would then overwrite matching classification<br>
results would then be instant due to the offload.

<strong>CONFIG\_MLX5\_EN\_ARFS=(y/n)</strong>

Enables Hardware-accelerated receive flow steering (arfs) support, and ntuple filtering.<br>
[https://enterprise-support.nvidia.com/s/article/howto-configure-arfs-on-connectx-4](<https://enterprise-support.nvidia.com/s/article/howto-configure-arfs-on-connectx-4>)

<strong>CONFIG\_MLX5\_EN\_IPSEC=(y/n)</strong>

Enables [IPSec XFRM cryptography-offload acceleration](<~kernel/internals/networking/xfrm/xfrm-device#rst-xfrm-device>).

<strong>CONFIG\_MLX5\_MACSEC=(y/n)</strong>

Build support for MACsec cryptography-offload acceleration in the NIC.

<strong>CONFIG\_MLX5\_EN\_RXNFC=(y/n)</strong>

Enables ethtool receive network flow classification, which allows user defined<br>
flow rules to direct traffic into arbitrary rx queue via ethtool set/get\_rxnfc API.

<strong>CONFIG\_MLX5\_EN\_TLS=(y/n)</strong>

TLS cryptography-offload acceleration.

<strong>CONFIG\_MLX5\_ESWITCH=(y/n)</strong>

Ethernet SRIOV E-Switch support in ConnectX NIC. E-Switch provides internal SRIOV packet steering<br>
and switching for the enabled VFs and PF in two available modes:<br>
&nbsp;&nbsp;&nbsp;&nbsp;1\) [Legacy SRIOV mode (L2 mac vlan steering based)](<https://enterprise-support.nvidia.com/s/article/HowTo-Configure-SR-IOV-for-ConnectX-4-ConnectX-5-ConnectX-6-with-KVM-Ethernet>)<a id="rst-legacy-sriov-mode-l2-mac-vlan-steering-based"></a>.<br>
&nbsp;&nbsp;&nbsp;&nbsp;2\) [Switchdev mode (eswitch offloads)](<~kernel/internals/networking/switchdev#rst-switchdev>).

<strong>CONFIG\_MLX5\_FPGA=(y/n)</strong>

Build support for the Innova family of network cards by Mellanox Technologies.<br>
Innova network cards are comprised of a ConnectX chip and an FPGA chip on one board.<br>
If you select this option, the mlx5\_core driver will include the Innova FPGA core and allow<br>
building sandbox-specific client drivers.

<strong>CONFIG\_MLX5\_INFINIBAND=(y/n/m)</strong> (module mlx5\_ib.ko)

Provides low-level InfiniBand/RDMA and [RoCE](<https://enterprise-support.nvidia.com/s/article/recommended-network-configuration-examples-for-roce-deployment>)<a id="rst-roce"></a> support.

<strong>CONFIG\_MLX5\_MPFS=(y/n)</strong>

Ethernet Multi-Physical Function Switch (MPFS) support in ConnectX NIC.<br>
MPFs is required for when [Multi-Host](<https://www.nvidia.com/en-us/networking/multi-host/>)<a id="rst-multi-host"></a> configuration is enabled to allow passing<br>
user configured unicast MAC addresses to the requesting PF.

<strong>CONFIG\_MLX5\_SF=(y/n)</strong>

Build support for subfunction.<br>
Subfunctons are more light weight than PCI SRIOV VFs. Choosing this option<br>
will enable support for creating subfunction devices.

<strong>CONFIG\_MLX5\_SF\_MANAGER=(y/n)</strong>

Build support for subfuction port in the NIC. A Mellanox subfunction<br>
port is managed through devlink.  A subfunction supports RDMA, netdevice<br>
and vdpa device. It is similar to a SRIOV VF but it doesn't require<br>
SRIOV support.

<strong>CONFIG\_MLX5\_SW\_STEERING=(y/n)</strong>

Build support for software-managed steering in the NIC.

<strong>CONFIG\_MLX5\_HW\_STEERING=(y/n)</strong>

Build support for hardware-managed steering in the NIC.

<strong>CONFIG\_MLX5\_TC\_CT=(y/n)</strong>

Support offloading connection tracking rules via tc ct action.

<strong>CONFIG\_MLX5\_TC\_SAMPLE=(y/n)</strong>

Support offloading sample rules via tc sample action.

<strong>CONFIG\_MLX5\_VDPA=(y/n)</strong>

Support library for Mellanox VDPA drivers. Provides code that is<br>
common for all types of VDPA drivers. The following drivers are planned:<br>
net, block.

<strong>CONFIG\_MLX5\_VDPA\_NET=(y/n)</strong>

VDPA network driver for ConnectX6 and newer. Provides offloading<br>
of virtio net datapath such that descriptors put on the ring will<br>
be executed by the hardware. It also supports a variety of stateless<br>
offloads depending on the actual device used and firmware version.

<strong>CONFIG\_MLX5\_VFIO\_PCI=(y/n)</strong>

This provides migration support for MLX5 devices using the VFIO framework.

<strong>External options</strong> ( Choose if the corresponding mlx5 feature is required )

- CONFIG\_MLXFW: When chosen, mlx5 firmware flashing support will be enabled (via devlink and ethtool).

- CONFIG\_PTP\_1588\_CLOCK: When chosen, mlx5 ptp support will be enabled

- CONFIG\_VXLAN: When chosen, mlx5 vxlan support will be enabled.
