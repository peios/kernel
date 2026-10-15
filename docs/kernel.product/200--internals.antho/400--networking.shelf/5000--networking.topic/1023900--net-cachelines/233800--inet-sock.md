---
title: "inet_sock struct fast path usage breakdown"
type: reference
description: "Reference for inet_sock struct fast path usage breakdown."
---

<a id="rst-inet-sock-struct-fast-path-usage-breakdown"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<!-- Copyright (C) 2023 Google LLC -->


<table>
<thead>
<tr>
<th>


Type

</th>
<th>


Name

</th>
<th>


fastpath_tx_access

</th>
<th>


fastpath_rx_access

</th>
<th>


comment

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


struct sock

</td>
<td>


sk

</td>
<td>


read_mostly

</td>
<td>


read_mostly

</td>
<td>


tcp_init_buffer_space,tcp_init_transfer,tcp_finish_connect,tcp_connect,tcp_send_rcvq,tcp_send_syn_data

</td>
</tr>
<tr>
<td>


struct ipv6_pinfo\*

</td>
<td>


pinet6

</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


struct ipv6_fl_socklist\*

</td>
<td>


ipv6_fl_list

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


tcp_v6_connect,\__ip6_datagram_connect,udpv6_sendmsg,rawv6_sendmsg

</td>
</tr>
<tr>
<td>


be16

</td>
<td>


inet_sport

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


\__tcp_transmit_skb

</td>
</tr>
<tr>
<td>


be32

</td>
<td>


inet_daddr

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


ip_select_ident_segs

</td>
</tr>
<tr>
<td>


be32

</td>
<td>


inet_rcv_saddr

</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


be16

</td>
<td>


inet_dport

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


\__tcp_transmit_skb

</td>
</tr>
<tr>
<td>


u16

</td>
<td>


inet_num

</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


be32

</td>
<td>


inet_saddr

</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


s16

</td>
<td>


uc_ttl

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


\__ip_queue_xmit/ip_select_ttl

</td>
</tr>
<tr>
<td>


u16

</td>
<td>


cmsg_flags

</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


struct ip_options_rcu\*

</td>
<td>


inet_opt

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


\__ip_queue_xmit

</td>
</tr>
<tr>
<td>


u16

</td>
<td>


inet_id

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


ip_select_ident_segs

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


tos

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


ip_queue_xmit

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


min_ttl

</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


u8

</td>
<td>


mc_ttl

</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


u8

</td>
<td>


pmtudisc

</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


u8:1

</td>
<td>


recverr

</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


u8:1

</td>
<td>


is_icsk

</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


u8:1

</td>
<td>


freebind

</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


u8:1

</td>
<td>


hdrincl

</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


u8:1

</td>
<td>


mc_loop

</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


u8:1

</td>
<td>


transparent

</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


u8:1

</td>
<td>


mc_all

</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


u8:1

</td>
<td>


nodefrag

</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


u8:1

</td>
<td>


bind_address_no_port

</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


u8:1

</td>
<td>


recverr_rfc4884

</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


u8:1

</td>
<td>


defer_connect

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


tcp_sendmsg_fastopen

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


rcv_tos

</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


u8

</td>
<td>


convert_csum

</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


int

</td>
<td>


uc_index

</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


int

</td>
<td>


mc_index

</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


be32

</td>
<td>


mc_addr

</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


struct ip_mc_socklist\*

</td>
<td>


mc_list

</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


struct inet_cork_full

</td>
<td>


cork

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


\__tcp_transmit_skb

</td>
</tr>
<tr>
<td>


struct

</td>
<td>


local_port_range

</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
</tbody>
</table>
