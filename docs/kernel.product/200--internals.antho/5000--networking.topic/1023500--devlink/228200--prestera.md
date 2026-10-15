---
title: "prestera devlink support"
type: reference
description: "This document describes the devlink features implemented by the prestera device driver."
---

<a id="rst-prestera-devlink-support"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

This document describes the devlink features implemented by the `prestera` device driver.

<a id="rst-driver-specific-traps"></a>

## Driver-specific Traps


<table>
<caption>List of Driver-specific Traps Registered by prestera</caption>
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
</tbody>
</table>


<table>
<caption>List of Driver-specific Traps Registered by prestera</caption>
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


`arp_bc`

</td>
<td>


`trap`

</td>
<td>


Traps ARP broadcast packets (both requests/responses)

</td>
</tr>
<tr>
<td>


`is_is`

</td>
<td>


`trap`

</td>
<td>


Traps IS-IS packets

</td>
</tr>
<tr>
<td>


`ospf`

</td>
<td>


`trap`

</td>
<td>


Traps OSPF packets

</td>
</tr>
<tr>
<td>


`ip_bc_mac`

</td>
<td>


`trap`

</td>
<td>


Traps IPv4 packets with broadcast DA Mac address

</td>
</tr>
<tr>
<td>


`stp`

</td>
<td>


`trap`

</td>
<td>


Traps STP BPDU

</td>
</tr>
<tr>
<td>


`lacp`

</td>
<td>


`trap`

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


`trap`

</td>
<td>


Traps LLDP packets

</td>
</tr>
<tr>
<td>


`router_mc`

</td>
<td>


`trap`

</td>
<td>


Traps multicast packets

</td>
</tr>
<tr>
<td>


`vrrp`

</td>
<td>


`trap`

</td>
<td>


Traps VRRP packets

</td>
</tr>
<tr>
<td>


`dhcp`

</td>
<td>


`trap`

</td>
<td>


Traps DHCP packets

</td>
</tr>
<tr>
<td>


`mtu_error`

</td>
<td>


`trap`

</td>
<td>


Traps (exception) packets that exceeded port's MTU

</td>
</tr>
<tr>
<td>


`mac_to_me`

</td>
<td>


`trap`

</td>
<td>


Traps packets with switch-port's DA Mac address

</td>
</tr>
<tr>
<td>


`ttl_error`

</td>
<td>


`trap`

</td>
<td>


Traps (exception) IPv4 packets whose TTL exceeded

</td>
</tr>
<tr>
<td>


`ipv4_options`

</td>
<td>


`trap`

</td>
<td>


Traps (exception) packets due to the malformed IPV4 header options

</td>
</tr>
<tr>
<td>


`ip_default_route`

</td>
<td>


`trap`

</td>
<td>


Traps packets that have no specific IP interface (IP to me) and no forwarding prefix

</td>
</tr>
<tr>
<td>


`local_route`

</td>
<td>


`trap`

</td>
<td>


Traps packets that have been send to one of switch IP interfaces addresses

</td>
</tr>
<tr>
<td>


`ipv4_icmp_redirect`

</td>
<td>


`trap`

</td>
<td>


Traps (exception) IPV4 ICMP redirect packets

</td>
</tr>
<tr>
<td>


`arp_response`

</td>
<td>


`trap`

</td>
<td>


Traps ARP replies packets that have switch-port's DA Mac address

</td>
</tr>
<tr>
<td>


`acl_code_0`

</td>
<td>


`trap`

</td>
<td>


Traps packets that have ACL priority set to 0 (tc pref 0)

</td>
</tr>
<tr>
<td>


`acl_code_1`

</td>
<td>


`trap`

</td>
<td>


Traps packets that have ACL priority set to 1 (tc pref 1)

</td>
</tr>
<tr>
<td>


`acl_code_2`

</td>
<td>


`trap`

</td>
<td>


Traps packets that have ACL priority set to 2 (tc pref 2)

</td>
</tr>
<tr>
<td>


`acl_code_3`

</td>
<td>


`trap`

</td>
<td>


Traps packets that have ACL priority set to 3 (tc pref 3)

</td>
</tr>
<tr>
<td>


`acl_code_4`

</td>
<td>


`trap`

</td>
<td>


Traps packets that have ACL priority set to 4 (tc pref 4)

</td>
</tr>
<tr>
<td>


`acl_code_5`

</td>
<td>


`trap`

</td>
<td>


Traps packets that have ACL priority set to 5 (tc pref 5)

</td>
</tr>
<tr>
<td>


`acl_code_6`

</td>
<td>


`trap`

</td>
<td>


Traps packets that have ACL priority set to 6 (tc pref 6)

</td>
</tr>
<tr>
<td>


`acl_code_7`

</td>
<td>


`trap`

</td>
<td>


Traps packets that have ACL priority set to 7 (tc pref 7)

</td>
</tr>
<tr>
<td>


`ipv4_bgp`

</td>
<td>


`trap`

</td>
<td>


Traps IPv4 BGP packets

</td>
</tr>
<tr>
<td>


`ssh`

</td>
<td>


`trap`

</td>
<td>


Traps SSH packets

</td>
</tr>
<tr>
<td>


`telnet`

</td>
<td>


`trap`

</td>
<td>


Traps Telnet packets

</td>
</tr>
<tr>
<td>


`icmp`

</td>
<td>


`trap`

</td>
<td>


Traps ICMP packets

</td>
</tr>
<tr>
<td>


`rxdma_drop`

</td>
<td>


`drop`

</td>
<td>


Drops packets (RxDMA) due to the lack of ingress buffers etc.

</td>
</tr>
<tr>
<td>


`port_no_vlan`

</td>
<td>


`drop`

</td>
<td>


Drops packets due to faulty-configured network or due to internal bug (config issue).

</td>
</tr>
<tr>
<td>


`local_port`

</td>
<td>


`drop`

</td>
<td>


Drops packets whose decision (FDB entry) is to bridge packet back to the incoming port/trunk.

</td>
</tr>
<tr>
<td>


`invalid_sa`

</td>
<td>


`drop`

</td>
<td>


Drops packets with multicast source MAC address.

</td>
</tr>
<tr>
<td>


`illegal_ip_addr`

</td>
<td>


`drop`

</td>
<td>


Drops packets with illegal SIP/DIP multicast/unicast addresses.

</td>
</tr>
<tr>
<td>


`illegal_ipv4_hdr`

</td>
<td>


`drop`

</td>
<td>


Drops packets with illegal IPV4 header.

</td>
</tr>
<tr>
<td>


`ip_uc_dip_da_mismatch`

</td>
<td>


`drop`

</td>
<td>


Drops packets with destination MAC being unicast, but destination IP address being multicast.

</td>
</tr>
<tr>
<td>


`ip_sip_is_zero`

</td>
<td>


`drop`

</td>
<td>


Drops packets with zero (0) IPV4 source address.

</td>
</tr>
<tr>
<td>


`met_red`

</td>
<td>


`drop`

</td>
<td>


Drops non-conforming packets (dropped by Ingress policer, metering drop), e.g. packet rate exceeded configured bandwidth.

</td>
</tr>
</tbody>
</table>
