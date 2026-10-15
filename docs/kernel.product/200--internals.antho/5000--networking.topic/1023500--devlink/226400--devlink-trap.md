---
title: "Devlink Trap"
type: reference
description: "Devices capable of offloading the kernel's datapath and perform functions such as bridging and routing must also be able to send specific packets to the kernel (i.e., the CPU) for processing."
---

<a id="rst-devlink-trap"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-background"></a>

## Background

Devices capable of offloading the kernel's datapath and perform functions such as bridging and routing must also be able to send specific packets to the kernel (i.e., the CPU) for processing.

For example, a device acting as a multicast-aware bridge must be able to send IGMP membership reports to the kernel for processing by the bridge module. Without processing such packets, the bridge module could never populate its MDB.

As another example, consider a device acting as router which has received an IP packet with a TTL of 1. Upon routing the packet the device must send it to the kernel so that it will route it as well and generate an ICMP Time Exceeded error datagram. Without letting the kernel route such packets itself, utilities such as `traceroute` could never work.

The fundamental ability of sending certain packets to the kernel for processing is called "packet trapping".

<a id="rst-overview"></a>

## Overview

The `devlink-trap` mechanism allows capable device drivers to register their supported packet traps with `devlink` and report trapped packets to `devlink` for further analysis.

Upon receiving trapped packets, `devlink` will perform a per-trap packets and bytes accounting and potentially report the packet to user space via a netlink event along with all the provided metadata (e.g., trap reason, timestamp, input port). This is especially useful for drop traps (see [Trap Types](<#rst-trap-types>)) as it allows users to obtain further visibility into packet drops that would otherwise be invisible.

The following diagram provides a general overview of `devlink-trap`:



```text
                            Netlink event: Packet w/ metadata
                                           Or a summary of recent drops
                          ^
                          |
 Userspace                |
+---------------------------------------------------+
 Kernel                   |
                          |
                  +-------+--------+
                  |                |
                  |  drop_monitor  |
                  |                |
                  +-------^--------+
                          |
                          | Non-control traps
                          |
                     +----+----+
                     |         |      Kernel's Rx path
                     | devlink |      (non-drop traps)
                     |         |
                     +----^----+      ^
                          |           |
                          +-----------+
                          |
                  +-------+-------+
                  |               |
                  | Device driver |
                  |               |
                  +-------^-------+
 Kernel                   |
+---------------------------------------------------+
 Hardware                 |
                          | Trapped packet
                          |
                       +--+---+
                       |      |
                       | ASIC |
                       |      |
                       +------+
```

<a id="rst-trap-types-1"></a>
<a id="rst-trap-types"></a>

## Trap Types

The `devlink-trap` mechanism supports the following packet trap types:

> - `drop`: Trapped packets were dropped by the underlying device. Packets are only processed by `devlink` and not injected to the kernel's Rx path. The trap action (see [Trap Actions](<#rst-trap-actions>)) can be changed.
>
> - `exception`: Trapped packets were not forwarded as intended by the underlying device due to an exception (e.g., TTL error, missing neighbour entry) and trapped to the control plane for resolution. Packets are processed by `devlink` and injected to the kernel's Rx path. Changing the action of such traps is not allowed, as it can easily break the control plane.
>
> - `control`: Trapped packets were trapped by the device because these are control packets required for the correct functioning of the control plane. For example, ARP request and IGMP query packets. Packets are injected to the kernel's Rx path, but not reported to the kernel's drop monitor. Changing the action of such traps is not allowed, as it can easily break the control plane.

<a id="rst-trap-actions-1"></a>
<a id="rst-trap-actions"></a>

## Trap Actions

The `devlink-trap` mechanism supports the following packet trap actions:

> - `trap`: The sole copy of the packet is sent to the CPU.
>
> - `drop`: The packet is dropped by the underlying device and a copy is not sent to the CPU.
>
> - `mirror`: The packet is forwarded by the underlying device and a copy is sent to the CPU.

<a id="rst-generic-packet-traps"></a>

## Generic Packet Traps

Generic packet traps are used to describe traps that trap well-defined packets or packets that are trapped due to well-defined conditions (e.g., TTL error). Such traps can be shared by multiple device drivers and their description must be added to the following table:


<table>
<caption>List of Generic Packet Traps</caption>
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


`source_mac_is_multicast`

</td>
<td>


`drop`

</td>
<td>


Traps incoming packets that the device decided to drop because of a multicast source MAC

</td>
</tr>
<tr>
<td>


`vlan_tag_mismatch`

</td>
<td>


`drop`

</td>
<td>


Traps incoming packets that the device decided to drop in case of VLAN tag mismatch: The ingress bridge port is not configured with a PVID and the packet is untagged or prio-tagged

</td>
</tr>
<tr>
<td>


`ingress_vlan_filter`

</td>
<td>


`drop`

</td>
<td>


Traps incoming packets that the device decided to drop in case they are tagged with a VLAN that is not configured on the ingress bridge port

</td>
</tr>
<tr>
<td>


`ingress_spanning_tree_filter`

</td>
<td>


`drop`

</td>
<td>


Traps incoming packets that the device decided to drop in case the STP state of the ingress bridge port is not "forwarding"

</td>
</tr>
<tr>
<td>


`port_list_is_empty`

</td>
<td>


`drop`

</td>
<td>


Traps packets that the device decided to drop in case they need to be flooded (e.g., unknown unicast, unregistered multicast) and there are no ports the packets should be flooded to

</td>
</tr>
<tr>
<td>


`port_loopback_filter`

</td>
<td>


`drop`

</td>
<td>


Traps packets that the device decided to drop in case after layer 2 forwarding the only port from which they should be transmitted through is the port from which they were received

</td>
</tr>
<tr>
<td>


`blackhole_route`

</td>
<td>


`drop`

</td>
<td>


Traps packets that the device decided to drop in case they hit a blackhole route

</td>
</tr>
<tr>
<td>


`ttl_value_is_too_small`

</td>
<td>


`exception`

</td>
<td>


Traps unicast packets that should be forwarded by the device whose TTL was decremented to 0 or less

</td>
</tr>
<tr>
<td>


`tail_drop`

</td>
<td>


`drop`

</td>
<td>


Traps packets that the device decided to drop because they could not be enqueued to a transmission queue which is full

</td>
</tr>
<tr>
<td>


`non_ip`

</td>
<td>


`drop`

</td>
<td>


Traps packets that the device decided to drop because they need to undergo a layer 3 lookup, but are not IP or MPLS packets

</td>
</tr>
<tr>
<td>


`uc_dip_over_mc_dmac`

</td>
<td>


`drop`

</td>
<td>


Traps packets that the device decided to drop because they need to be routed and they have a unicast destination IP and a multicast destination MAC

</td>
</tr>
<tr>
<td>


`dip_is_loopback_address`

</td>
<td>


`drop`

</td>
<td>


Traps packets that the device decided to drop because they need to be routed and their destination IP is the loopback address (i.e., 127.0.0.0/8 and ::1/128)

</td>
</tr>
<tr>
<td>


`sip_is_mc`

</td>
<td>


`drop`

</td>
<td>


Traps packets that the device decided to drop because they need to be routed and their source IP is multicast (i.e., 224.0.0.0/8 and ff::/8)

</td>
</tr>
<tr>
<td>


`sip_is_loopback_address`

</td>
<td>


`drop`

</td>
<td>


Traps packets that the device decided to drop because they need to be routed and their source IP is the loopback address (i.e., 127.0.0.0/8 and ::1/128)

</td>
</tr>
<tr>
<td>


`ip_header_corrupted`

</td>
<td>


`drop`

</td>
<td>


Traps packets that the device decided to drop because they need to be routed and their IP header is corrupted: wrong checksum, wrong IP version or too short Internet Header Length (IHL)

</td>
</tr>
<tr>
<td>


`ipv4_sip_is_limited_bc`

</td>
<td>


`drop`

</td>
<td>


Traps packets that the device decided to drop because they need to be routed and their source IP is limited broadcast (i.e., 255.255.255.255/32)

</td>
</tr>
<tr>
<td>


`ipv6_mc_dip_reserved_scope`

</td>
<td>


`drop`

</td>
<td>


Traps IPv6 packets that the device decided to drop because they need to be routed and their IPv6 multicast destination IP has a reserved scope (i.e., ffx0::/16)

</td>
</tr>
<tr>
<td>


`ipv6_mc_dip_interface_local_scope`

</td>
<td>


`drop`

</td>
<td>


Traps IPv6 packets that the device decided to drop because they need to be routed and their IPv6 multicast destination IP has an interface-local scope (i.e., ffx1::/16)

</td>
</tr>
<tr>
<td>


`mtu_value_is_too_small`

</td>
<td>


`exception`

</td>
<td>


Traps packets that should have been routed by the device, but were bigger than the MTU of the egress interface

</td>
</tr>
<tr>
<td>


`unresolved_neigh`

</td>
<td>


`exception`

</td>
<td>


Traps packets that did not have a matching IP neighbour after routing

</td>
</tr>
<tr>
<td>


`mc_reverse_path_forwarding`

</td>
<td>


`exception`

</td>
<td>


Traps multicast IP packets that failed reverse-path forwarding (RPF) check during multicast routing

</td>
</tr>
<tr>
<td>


`reject_route`

</td>
<td>


`exception`

</td>
<td>


Traps packets that hit reject routes (i.e., "unreachable", "prohibit")

</td>
</tr>
<tr>
<td>


`ipv4_lpm_miss`

</td>
<td>


`exception`

</td>
<td>


Traps unicast IPv4 packets that did not match any route

</td>
</tr>
<tr>
<td>


`ipv6_lpm_miss`

</td>
<td>


`exception`

</td>
<td>


Traps unicast IPv6 packets that did not match any route

</td>
</tr>
<tr>
<td>


`non_routable_packet`

</td>
<td>


`drop`

</td>
<td>


Traps packets that the device decided to drop because they are not supposed to be routed. For example, IGMP queries can be flooded by the device in layer 2 and reach the router. Such packets should not be routed and instead dropped

</td>
</tr>
<tr>
<td>


`decap_error`

</td>
<td>


`exception`

</td>
<td>


Traps NVE and IPinIP packets that the device decided to drop because of failure during decapsulation (e.g., packet being too short, reserved bits set in VXLAN header)

</td>
</tr>
<tr>
<td>


`overlay_smac_is_mc`

</td>
<td>


`drop`

</td>
<td>


Traps NVE packets that the device decided to drop because their overlay source MAC is multicast

</td>
</tr>
<tr>
<td>


`ingress_flow_action_drop`

</td>
<td>


`drop`

</td>
<td>


Traps packets dropped during processing of ingress flow action drop

</td>
</tr>
<tr>
<td>


`egress_flow_action_drop`

</td>
<td>


`drop`

</td>
<td>


Traps packets dropped during processing of egress flow action drop

</td>
</tr>
<tr>
<td>


`stp`

</td>
<td>


`control`

</td>
<td>


Traps STP packets

</td>
</tr>
<tr>
<td>


`lacp`

</td>
<td>


`control`

</td>
<td>


Traps LACP packets

</td>
</tr>
<tr>
<td>


`lldp`

</td>
<td>


`control`

</td>
<td>


Traps LLDP packets

</td>
</tr>
<tr>
<td>


`igmp_query`

</td>
<td>


`control`

</td>
<td>


Traps IGMP Membership Query packets

</td>
</tr>
<tr>
<td>


`igmp_v1_report`

</td>
<td>


`control`

</td>
<td>


Traps IGMP Version 1 Membership Report packets

</td>
</tr>
<tr>
<td>


`igmp_v2_report`

</td>
<td>


`control`

</td>
<td>


Traps IGMP Version 2 Membership Report packets

</td>
</tr>
<tr>
<td>


`igmp_v3_report`

</td>
<td>


`control`

</td>
<td>


Traps IGMP Version 3 Membership Report packets

</td>
</tr>
<tr>
<td>


`igmp_v2_leave`

</td>
<td>


`control`

</td>
<td>


Traps IGMP Version 2 Leave Group packets

</td>
</tr>
<tr>
<td>


`mld_query`

</td>
<td>


`control`

</td>
<td>


Traps MLD Multicast Listener Query packets

</td>
</tr>
<tr>
<td>


`mld_v1_report`

</td>
<td>


`control`

</td>
<td>


Traps MLD Version 1 Multicast Listener Report packets

</td>
</tr>
<tr>
<td>


`mld_v2_report`

</td>
<td>


`control`

</td>
<td>


Traps MLD Version 2 Multicast Listener Report packets

</td>
</tr>
<tr>
<td>


`mld_v1_done`

</td>
<td>


`control`

</td>
<td>


Traps MLD Version 1 Multicast Listener Done packets

</td>
</tr>
<tr>
<td>


`ipv4_dhcp`

</td>
<td>


`control`

</td>
<td>


Traps IPv4 DHCP packets

</td>
</tr>
<tr>
<td>


`ipv6_dhcp`

</td>
<td>


`control`

</td>
<td>


Traps IPv6 DHCP packets

</td>
</tr>
<tr>
<td>


`arp_request`

</td>
<td>


`control`

</td>
<td>


Traps ARP request packets

</td>
</tr>
<tr>
<td>


`arp_response`

</td>
<td>


`control`

</td>
<td>


Traps ARP response packets

</td>
</tr>
<tr>
<td>


`arp_overlay`

</td>
<td>


`control`

</td>
<td>


Traps NVE-decapsulated ARP packets that reached the overlay network. This is required, for example, when the address that needs to be resolved is a local address

</td>
</tr>
<tr>
<td>


`ipv6_neigh_solicit`

</td>
<td>


`control`

</td>
<td>


Traps IPv6 Neighbour Solicitation packets

</td>
</tr>
<tr>
<td>


`ipv6_neigh_advert`

</td>
<td>


`control`

</td>
<td>


Traps IPv6 Neighbour Advertisement packets

</td>
</tr>
<tr>
<td>


`ipv4_bfd`

</td>
<td>


`control`

</td>
<td>


Traps IPv4 BFD packets

</td>
</tr>
<tr>
<td>


`ipv6_bfd`

</td>
<td>


`control`

</td>
<td>


Traps IPv6 BFD packets

</td>
</tr>
<tr>
<td>


`ipv4_ospf`

</td>
<td>


`control`

</td>
<td>


Traps IPv4 OSPF packets

</td>
</tr>
<tr>
<td>


`ipv6_ospf`

</td>
<td>


`control`

</td>
<td>


Traps IPv6 OSPF packets

</td>
</tr>
<tr>
<td>


`ipv4_bgp`

</td>
<td>


`control`

</td>
<td>


Traps IPv4 BGP packets

</td>
</tr>
<tr>
<td>


`ipv6_bgp`

</td>
<td>


`control`

</td>
<td>


Traps IPv6 BGP packets

</td>
</tr>
<tr>
<td>


`ipv4_vrrp`

</td>
<td>


`control`

</td>
<td>


Traps IPv4 VRRP packets

</td>
</tr>
<tr>
<td>


`ipv6_vrrp`

</td>
<td>


`control`

</td>
<td>


Traps IPv6 VRRP packets

</td>
</tr>
<tr>
<td>


`ipv4_pim`

</td>
<td>


`control`

</td>
<td>


Traps IPv4 PIM packets

</td>
</tr>
<tr>
<td>


`ipv6_pim`

</td>
<td>


`control`

</td>
<td>


Traps IPv6 PIM packets

</td>
</tr>
<tr>
<td>


`uc_loopback`

</td>
<td>


`control`

</td>
<td>


Traps unicast packets that need to be routed through the same layer 3 interface from which they were received. Such packets are routed by the kernel, but also cause it to potentially generate ICMP redirect packets

</td>
</tr>
<tr>
<td>


`local_route`

</td>
<td>


`control`

</td>
<td>


Traps unicast packets that hit a local route and need to be locally delivered

</td>
</tr>
<tr>
<td>


`external_route`

</td>
<td>


`control`

</td>
<td>


Traps packets that should be routed through an external interface (e.g., management interface) that does not belong to the same device (e.g., switch ASIC) as the ingress interface

</td>
</tr>
<tr>
<td>


`ipv6_uc_dip_link_local_scope`

</td>
<td>


`control`

</td>
<td>


Traps unicast IPv6 packets that need to be routed and have a destination IP address with a link-local scope (i.e., fe80::/10). The trap allows device drivers to avoid programming link-local routes, but still receive packets for local delivery

</td>
</tr>
<tr>
<td>


`ipv6_dip_all_nodes`

</td>
<td>


`control`

</td>
<td>


Traps IPv6 packets that their destination IP address is the "All Nodes Address" (i.e., ff02::1)

</td>
</tr>
<tr>
<td>


`ipv6_dip_all_routers`

</td>
<td>


`control`

</td>
<td>


Traps IPv6 packets that their destination IP address is the "All Routers Address" (i.e., ff02::2)

</td>
</tr>
<tr>
<td>


`ipv6_router_solicit`

</td>
<td>


`control`

</td>
<td>


Traps IPv6 Router Solicitation packets

</td>
</tr>
<tr>
<td>


`ipv6_router_advert`

</td>
<td>


`control`

</td>
<td>


Traps IPv6 Router Advertisement packets

</td>
</tr>
<tr>
<td>


`ipv6_redirect`

</td>
<td>


`control`

</td>
<td>


Traps IPv6 Redirect Message packets

</td>
</tr>
<tr>
<td>


`ipv4_router_alert`

</td>
<td>


`control`

</td>
<td>


Traps IPv4 packets that need to be routed and include the Router Alert option. Such packets need to be locally delivered to raw sockets that have the IP_ROUTER_ALERT socket option set

</td>
</tr>
<tr>
<td>


`ipv6_router_alert`

</td>
<td>


`control`

</td>
<td>


Traps IPv6 packets that need to be routed and include the Router Alert option in their Hop-by-Hop extension header. Such packets need to be locally delivered to raw sockets that have the IPV6_ROUTER_ALERT socket option set

</td>
</tr>
<tr>
<td>


`ptp_event`

</td>
<td>


`control`

</td>
<td>


Traps PTP time-critical event messages (Sync, Delay_req, Pdelay_Req and Pdelay_Resp)

</td>
</tr>
<tr>
<td>


`ptp_general`

</td>
<td>


`control`

</td>
<td>


Traps PTP general messages (Announce, Follow_Up, Delay_Resp, Pdelay_Resp_Follow_Up, management and signaling)

</td>
</tr>
<tr>
<td>


`flow_action_sample`

</td>
<td>


`control`

</td>
<td>


Traps packets sampled during processing of flow action sample (e.g., via tc's sample action)

</td>
</tr>
<tr>
<td>


`flow_action_trap`

</td>
<td>


`control`

</td>
<td>


Traps packets logged during processing of flow action trap (e.g., via tc's trap action)

</td>
</tr>
<tr>
<td>


`early_drop`

</td>
<td>


`drop`

</td>
<td>


Traps packets dropped due to the RED (Random Early Detection) algorithm (i.e., early drops)

</td>
</tr>
<tr>
<td>


`vxlan_parsing`

</td>
<td>


`drop`

</td>
<td>


Traps packets dropped due to an error in the VXLAN header parsing which might be because of packet truncation or the I flag is not set.

</td>
</tr>
<tr>
<td>


`llc_snap_parsing`

</td>
<td>


`drop`

</td>
<td>


Traps packets dropped due to an error in the LLC+SNAP header parsing

</td>
</tr>
<tr>
<td>


`vlan_parsing`

</td>
<td>


`drop`

</td>
<td>


Traps packets dropped due to an error in the VLAN header parsing. Could include unexpected packet truncation.

</td>
</tr>
<tr>
<td>


`pppoe_ppp_parsing`

</td>
<td>


`drop`

</td>
<td>


Traps packets dropped due to an error in the PPPoE+PPP header parsing. This could include finding a session ID of 0xFFFF (which is reserved and not for use), a PPPoE length which is larger than the frame received or any common error on this type of header

</td>
</tr>
<tr>
<td>


`mpls_parsing`

</td>
<td>


`drop`

</td>
<td>


Traps packets dropped due to an error in the MPLS header parsing which could include unexpected header truncation

</td>
</tr>
<tr>
<td>


`arp_parsing`

</td>
<td>


`drop`

</td>
<td>


Traps packets dropped due to an error in the ARP header parsing

</td>
</tr>
<tr>
<td>


`ip_1_parsing`

</td>
<td>


`drop`

</td>
<td>


Traps packets dropped due to an error in the first IP header parsing. This packet trap could include packets which do not pass an IP checksum check, a header length check (a minimum of 20 bytes), which might suffer from packet truncation thus the total length field exceeds the received packet length etc

</td>
</tr>
<tr>
<td>


`ip_n_parsing`

</td>
<td>


`drop`

</td>
<td>


Traps packets dropped due to an error in the parsing of the last IP header (the inner one in case of an IP over IP tunnel). The same common error checking is performed here as for the ip_1_parsing trap

</td>
</tr>
<tr>
<td>


`gre_parsing`

</td>
<td>


`drop`

</td>
<td>


Traps packets dropped due to an error in the GRE header parsing

</td>
</tr>
<tr>
<td>


`udp_parsing`

</td>
<td>


`drop`

</td>
<td>


Traps packets dropped due to an error in the UDP header parsing. This packet trap could include checksum errors, an improper UDP length detected (smaller than 8 bytes) or detection of header truncation.

</td>
</tr>
<tr>
<td>


`tcp_parsing`

</td>
<td>


`drop`

</td>
<td>


Traps packets dropped due to an error in the TCP header parsing. This could include TCP checksum errors, improper combination of SYN, FIN and/or RESET etc.

</td>
</tr>
<tr>
<td>


`ipsec_parsing`

</td>
<td>


`drop`

</td>
<td>


Traps packets dropped due to an error in the IPSEC header parsing

</td>
</tr>
<tr>
<td>


`sctp_parsing`

</td>
<td>


`drop`

</td>
<td>


Traps packets dropped due to an error in the SCTP header parsing. This would mean that port number 0 was used or that the header is truncated.

</td>
</tr>
<tr>
<td>


`dccp_parsing`

</td>
<td>


`drop`

</td>
<td>


Traps packets dropped due to an error in the DCCP header parsing

</td>
</tr>
<tr>
<td>


`gtp_parsing`

</td>
<td>


`drop`

</td>
<td>


Traps packets dropped due to an error in the GTP header parsing

</td>
</tr>
<tr>
<td>


`esp_parsing`

</td>
<td>


`drop`

</td>
<td>


Traps packets dropped due to an error in the ESP header parsing

</td>
</tr>
<tr>
<td>


`blackhole_nexthop`

</td>
<td>


`drop`

</td>
<td>


Traps packets that the device decided to drop in case they hit a blackhole nexthop

</td>
</tr>
<tr>
<td>


`dmac_filter`

</td>
<td>


`drop`

</td>
<td>


Traps incoming packets that the device decided to drop because the destination MAC is not configured in the MAC table and the interface is not in promiscuous mode

</td>
</tr>
<tr>
<td>


`eapol`

</td>
<td>


`control`

</td>
<td>


Traps "Extensible Authentication Protocol over LAN" (EAPOL) packets specified in IEEE 802.1X

</td>
</tr>
<tr>
<td>


`locked_port`

</td>
<td>


`drop`

</td>
<td>


Traps packets that the device decided to drop because they failed the locked bridge port check. That is, packets that were received via a locked port and whose \{SMAC, VID\} does not correspond to an FDB entry pointing to the port

</td>
</tr>
</tbody>
</table>

<a id="rst-driver-specific-packet-traps"></a>

## Driver-specific Packet Traps

Device drivers can register driver-specific packet traps, but these must be clearly documented. Such traps can correspond to device-specific exceptions and help debug packet drops caused by these exceptions. The following list includes links to the description of driver-specific traps registered by various device drivers:

> - [Documentation/networking/devlink/netdevsim.rst](~kernel/internals/networking/devlink/netdevsim)
>
> - [Documentation/networking/devlink/mlxsw.rst](~kernel/internals/networking/devlink/mlxsw)
>
> - [Documentation/networking/devlink/prestera.rst](~kernel/internals/networking/devlink/prestera)

<a id="rst-generic-packet-trap-groups-1"></a>
<a id="rst-generic-packet-trap-groups"></a>

## Generic Packet Trap Groups

Generic packet trap groups are used to aggregate logically related packet traps. These groups allow the user to batch operations such as setting the trap action of all member traps. In addition, `devlink-trap` can report aggregated per-group packets and bytes statistics, in case per-trap statistics are too narrow. The description of these groups must be added to the following table:


<table>
<caption>List of Generic Packet Trap Groups</caption>
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


`l2_drops`

</td>
<td>


Contains packet traps for packets that were dropped by the device during layer 2 forwarding (i.e., bridge)

</td>
</tr>
<tr>
<td>


`l3_drops`

</td>
<td>


Contains packet traps for packets that were dropped by the device during layer 3 forwarding

</td>
</tr>
<tr>
<td>


`l3_exceptions`

</td>
<td>


Contains packet traps for packets that hit an exception (e.g., TTL error) during layer 3 forwarding

</td>
</tr>
<tr>
<td>


`buffer_drops`

</td>
<td>


Contains packet traps for packets that were dropped by the device due to an enqueue decision

</td>
</tr>
<tr>
<td>


`tunnel_drops`

</td>
<td>


Contains packet traps for packets that were dropped by the device during tunnel encapsulation / decapsulation

</td>
</tr>
<tr>
<td>


`acl_drops`

</td>
<td>


Contains packet traps for packets that were dropped by the device during ACL processing

</td>
</tr>
<tr>
<td>


`stp`

</td>
<td>


Contains packet traps for STP packets

</td>
</tr>
<tr>
<td>


`lacp`

</td>
<td>


Contains packet traps for LACP packets

</td>
</tr>
<tr>
<td>


`lldp`

</td>
<td>


Contains packet traps for LLDP packets

</td>
</tr>
<tr>
<td>


`mc_snooping`

</td>
<td>


Contains packet traps for IGMP and MLD packets required for multicast snooping

</td>
</tr>
<tr>
<td>


`dhcp`

</td>
<td>


Contains packet traps for DHCP packets

</td>
</tr>
<tr>
<td>


`neigh_discovery`

</td>
<td>


Contains packet traps for neighbour discovery packets (e.g., ARP, IPv6 ND)

</td>
</tr>
<tr>
<td>


`bfd`

</td>
<td>


Contains packet traps for BFD packets

</td>
</tr>
<tr>
<td>


`ospf`

</td>
<td>


Contains packet traps for OSPF packets

</td>
</tr>
<tr>
<td>


`bgp`

</td>
<td>


Contains packet traps for BGP packets

</td>
</tr>
<tr>
<td>


`vrrp`

</td>
<td>


Contains packet traps for VRRP packets

</td>
</tr>
<tr>
<td>


`pim`

</td>
<td>


Contains packet traps for PIM packets

</td>
</tr>
<tr>
<td>


`uc_loopback`

</td>
<td>


Contains a packet trap for unicast loopback packets (i.e., `uc_loopback`). This trap is singled-out because in cases such as one-armed router it will be constantly triggered. To limit the impact on the CPU usage, a packet trap policer with a low rate can be bound to the group without affecting other traps

</td>
</tr>
<tr>
<td>


`local_delivery`

</td>
<td>


Contains packet traps for packets that should be locally delivered after routing, but do not match more specific packet traps (e.g., `ipv4_bgp`)

</td>
</tr>
<tr>
<td>


`external_delivery`

</td>
<td>


Contains packet traps for packets that should be routed through an external interface (e.g., management interface) that does not belong to the same device (e.g., switch ASIC) as the ingress interface

</td>
</tr>
<tr>
<td>


`ipv6`

</td>
<td>


Contains packet traps for various IPv6 control packets (e.g., Router Advertisements)

</td>
</tr>
<tr>
<td>


`ptp_event`

</td>
<td>


Contains packet traps for PTP time-critical event messages (Sync, Delay_req, Pdelay_Req and Pdelay_Resp)

</td>
</tr>
<tr>
<td>


`ptp_general`

</td>
<td>


Contains packet traps for PTP general messages (Announce, Follow_Up, Delay_Resp, Pdelay_Resp_Follow_Up, management and signaling)

</td>
</tr>
<tr>
<td>


`acl_sample`

</td>
<td>


Contains packet traps for packets that were sampled by the device during ACL processing

</td>
</tr>
<tr>
<td>


`acl_trap`

</td>
<td>


Contains packet traps for packets that were trapped (logged) by the device during ACL processing

</td>
</tr>
<tr>
<td>


`parser_error_drops`

</td>
<td>


Contains packet traps for packets that were marked by the device during parsing as erroneous

</td>
</tr>
<tr>
<td>


`eapol`

</td>
<td>


Contains packet traps for "Extensible Authentication Protocol over LAN" (EAPOL) packets specified in IEEE 802.1X

</td>
</tr>
</tbody>
</table>

<a id="rst-packet-trap-policers"></a>

## Packet Trap Policers

As previously explained, the underlying device can trap certain packets to the CPU for processing. In most cases, the underlying device is capable of handling packet rates that are several orders of magnitude higher compared to those that can be handled by the CPU.

Therefore, in order to prevent the underlying device from overwhelming the CPU, devices usually include packet trap policers that are able to police the trapped packets to rates that can be handled by the CPU.

The `devlink-trap` mechanism allows capable device drivers to register their supported packet trap policers with `devlink`. The device driver can choose to associate these policers with supported packet trap groups (see [Generic Packet Trap Groups](<#rst-generic-packet-trap-groups>)) during its initialization, thereby exposing its default control plane policy to user space.

Device drivers should allow user space to change the parameters of the policers (e.g., rate, burst size) as well as the association between the policers and trap groups by implementing the relevant callbacks.

If possible, device drivers should implement a callback that allows user space to retrieve the number of packets that were dropped by the policer because its configured policy was violated.

<a id="rst-testing"></a>

## Testing

See `tools/testing/selftests/drivers/net/netdevsim/devlink_trap.sh` for a test covering the core infrastructure. Test cases should be added for any new functionality.

Device drivers should focus their tests on device-specific functionality, such as the triggering of supported packet traps.
