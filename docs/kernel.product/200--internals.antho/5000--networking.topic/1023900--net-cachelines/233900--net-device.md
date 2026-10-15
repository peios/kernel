---
title: "net_device struct fast path usage breakdown"
type: reference
description: "Reference for net_device struct fast path usage breakdown."
---

<a id="rst-net-device-struct-fast-path-usage-breakdown"></a>

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


Comments

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


unsigned_long:32

</td>
<td>


priv_flags

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


\__dev_queue_xmit(tx)

</td>
</tr>
<tr>
<td>


unsigned_long:1

</td>
<td>


lltx

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


HARD_TX_LOCK,HARD_TX_TRYLOCK,HARD_TX_UNLOCK(tx)

</td>
</tr>
<tr>
<td>


unsigned long:1

</td>
<td>


netmem_tx:1;

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


char

</td>
<td>


name\[16\]

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


struct netdev_name_node\*

</td>
<td>


name_node

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


struct dev_ifalias\*

</td>
<td>


ifalias

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


unsigned_long

</td>
<td>


mem_end

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


unsigned_long

</td>
<td>


mem_start

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


unsigned_long

</td>
<td>


base_addr

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


unsigned_long

</td>
<td>


state

</td>
<td>


read_mostly

</td>
<td>


read_mostly

</td>
<td>


netif_running(dev)

</td>
</tr>
<tr>
<td>


struct list_head

</td>
<td>


dev_list

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


struct list_head

</td>
<td>


napi_list

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


struct list_head

</td>
<td>


unreg_list

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


struct list_head

</td>
<td>


close_list

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


struct list_head

</td>
<td>


ptype_all

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


dev_nit_active(tx)

</td>
</tr>
<tr>
<td>


struct list_head

</td>
<td>


ptype_specific

</td>
<td>




</td>
<td>


read_mostly

</td>
<td>


deliver_ptype_list_skb/\__netif_receive_skb_core(rx)

</td>
</tr>
<tr>
<td>


struct

</td>
<td>


adj_list

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


unsigned_int

</td>
<td>


flags

</td>
<td>


read_mostly

</td>
<td>


read_mostly

</td>
<td>


\__dev_queue_xmit,\__dev_xmit_skb,ip6_output,\__ip6_finish_output(tx);ip6_rcv_core(rx)

</td>
</tr>
<tr>
<td>


xdp_features_t

</td>
<td>


xdp_features

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


struct net_device_ops\*

</td>
<td>


netdev_ops

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


netdev_core_pick_tx,netdev_start_xmit(tx)

</td>
</tr>
<tr>
<td>


struct xdp_metadata_ops\*

</td>
<td>


xdp_metadata_ops

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


ifindex

</td>
<td>




</td>
<td>


read_mostly

</td>
<td>


ip6_rcv_core

</td>
</tr>
<tr>
<td>


unsigned_short

</td>
<td>


gflags

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


unsigned_short

</td>
<td>


hard_header_len

</td>
<td>


read_mostly

</td>
<td>


read_mostly

</td>
<td>


ip6_xmit(tx);gro_list_prepare(rx)

</td>
</tr>
<tr>
<td>


unsigned_int

</td>
<td>


mtu

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


ip_finish_output2

</td>
</tr>
<tr>
<td>


unsigned_short

</td>
<td>


needed_headroom

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


LL_RESERVED_SPACE/ip_finish_output2

</td>
</tr>
<tr>
<td>


unsigned_short

</td>
<td>


needed_tailroom

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


netdev_features_t

</td>
<td>


features

</td>
<td>


read_mostly

</td>
<td>


read_mostly

</td>
<td>


HARD_TX_LOCK,netif_skb_features,sk_setup_caps(tx);netif_elide_gro(rx)

</td>
</tr>
<tr>
<td>


netdev_features_t

</td>
<td>


hw_features

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


netdev_features_t

</td>
<td>


wanted_features

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


netdev_features_t

</td>
<td>


vlan_features

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


netdev_features_t

</td>
<td>


hw_enc_features

</td>
<td>




</td>
<td>




</td>
<td>


netif_skb_features

</td>
</tr>
<tr>
<td>


netdev_features_t

</td>
<td>


mpls_features

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


netdev_features_t

</td>
<td>


gso_partial_features

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


gso_features_check

</td>
</tr>
<tr>
<td>


unsigned_int

</td>
<td>


min_mtu

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


unsigned_int

</td>
<td>


max_mtu

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


unsigned_short

</td>
<td>


type

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


unsigned_char

</td>
<td>


min_header_len

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


unsigned_char

</td>
<td>


name_assign_type

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


group

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


struct net_device_stats

</td>
<td>


stats

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


struct net_device_core_stats\*

</td>
<td>


core_stats

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


atomic_t

</td>
<td>


carrier_up_count

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


atomic_t

</td>
<td>


carrier_down_count

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


struct iw_handler_def\*

</td>
<td>


wireless_handlers

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


struct ethtool_ops\*

</td>
<td>


ethtool_ops

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


struct l3mdev_ops\*

</td>
<td>


l3mdev_ops

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


struct ndisc_ops\*

</td>
<td>


ndisc_ops

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


struct xfrmdev_ops\*

</td>
<td>


xfrmdev_ops

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


struct tlsdev_ops\*

</td>
<td>


tlsdev_ops

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


struct header_ops\*

</td>
<td>


header_ops

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


ip_finish_output2,ip6_finish_output2(tx)

</td>
</tr>
<tr>
<td>


unsigned_char

</td>
<td>


operstate

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


unsigned_char

</td>
<td>


link_mode

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


unsigned_char

</td>
<td>


if_port

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


unsigned_char

</td>
<td>


dma

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


unsigned_char

</td>
<td>


perm_addr\[32\]

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


unsigned_char

</td>
<td>


addr_assign_type

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


unsigned_char

</td>
<td>


addr_len

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


unsigned_char

</td>
<td>


upper_level

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


unsigned_char

</td>
<td>


lower_level

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


threaded

</td>
<td>




</td>
<td>




</td>
<td>


napi_poll(napi_enable,netif_set_threaded)

</td>
</tr>
<tr>
<td>


unsigned_short

</td>
<td>


neigh_priv_len

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


unsigned_short

</td>
<td>


padded

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


unsigned_short

</td>
<td>


dev_id

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


unsigned_short

</td>
<td>


dev_port

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


spinlock_t

</td>
<td>


addr_list_lock

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


irq

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


struct netdev_hw_addr_list

</td>
<td>


uc

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


struct netdev_hw_addr_list

</td>
<td>


mc

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


struct netdev_hw_addr_list

</td>
<td>


dev_addrs

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


struct kset\*

</td>
<td>


queues_kset

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


struct list_head

</td>
<td>


unlink_list

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


unsigned_int

</td>
<td>


promiscuity

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


unsigned_int

</td>
<td>


allmulti

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


bool

</td>
<td>


uc_promisc

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


unsigned_char

</td>
<td>


nested_level

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


struct in_device\*

</td>
<td>


ip_ptr

</td>
<td>


read_mostly

</td>
<td>


read_mostly

</td>
<td>


\__in_dev_get

</td>
</tr>
<tr>
<td>


struct hlist_head

</td>
<td>


fib_nh_head

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


struct inet6_dev\*

</td>
<td>


ip6_ptr

</td>
<td>


read_mostly

</td>
<td>


read_mostly

</td>
<td>


\__in6_dev_get

</td>
</tr>
<tr>
<td>


struct vlan_info\*

</td>
<td>


vlan_info

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


struct dsa_port\*

</td>
<td>


dsa_ptr

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


struct tipc_bearer\*

</td>
<td>


tipc_ptr

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


void\*

</td>
<td>


atalk_ptr

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


void\*

</td>
<td>


ax25_ptr

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


struct wireless_dev\*

</td>
<td>


ieee80211_ptr

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


struct wpan_dev\*

</td>
<td>


ieee802154_ptr

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


struct mpls_dev\*

</td>
<td>


mpls_ptr

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


struct mctp_dev\*

</td>
<td>


mctp_ptr

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


unsigned_char\*

</td>
<td>


dev_addr

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


struct netdev_queue\*

</td>
<td>


\_rx

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


netdev_get_rx_queue(rx)

</td>
</tr>
<tr>
<td>


unsigned_int

</td>
<td>


num_rx_queues

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


unsigned_int

</td>
<td>


real_num_rx_queues

</td>
<td>




</td>
<td>


read_mostly

</td>
<td>


get_rps_cpu

</td>
</tr>
<tr>
<td>


struct bpf_prog\*

</td>
<td>


xdp_prog

</td>
<td>




</td>
<td>


read_mostly

</td>
<td>


netif_elide_gro()

</td>
</tr>
<tr>
<td>


unsigned_long

</td>
<td>


gro_flush_timeout

</td>
<td>




</td>
<td>


read_mostly

</td>
<td>


napi_complete_done

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


napi_defer_hard_irqs

</td>
<td>




</td>
<td>


read_mostly

</td>
<td>


napi_complete_done

</td>
</tr>
<tr>
<td>


unsigned_int

</td>
<td>


gro_max_size

</td>
<td>




</td>
<td>


read_mostly

</td>
<td>


skb_gro_receive

</td>
</tr>
<tr>
<td>


unsigned_int

</td>
<td>


gro_ipv4_max_size

</td>
<td>




</td>
<td>


read_mostly

</td>
<td>


skb_gro_receive

</td>
</tr>
<tr>
<td>


rx_handler_func_t\*

</td>
<td>


rx_handler

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


\__netif_receive_skb_core

</td>
</tr>
<tr>
<td>


void\*

</td>
<td>


rx_handler_data

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


struct netdev_queue\*

</td>
<td>


ingress_queue

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


struct bpf_mprog_entry

</td>
<td>


tcx_ingress

</td>
<td>




</td>
<td>


read_mostly

</td>
<td>


sch_handle_ingress

</td>
</tr>
<tr>
<td>


struct nf_hook_entries\*

</td>
<td>


nf_hooks_ingress

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


unsigned_char

</td>
<td>


broadcast\[32\]

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


struct cpu_rmap\*

</td>
<td>


rx_cpu_rmap

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


struct hlist_node

</td>
<td>


index_hlist

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


struct netdev_queue\*

</td>
<td>


\_tx

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


netdev_get_tx_queue(tx)

</td>
</tr>
<tr>
<td>


unsigned_int

</td>
<td>


num_tx_queues

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


unsigned_int

</td>
<td>


real_num_tx_queues

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


skb_tx_hash,netdev_core_pick_tx(tx)

</td>
</tr>
<tr>
<td>


unsigned_int

</td>
<td>


tx_queue_len

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


spinlock_t

</td>
<td>


tx_global_lock

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


struct xdp_dev_bulk_queue__percpu\*

</td>
<td>


xdp_bulkq

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


struct xps_dev_maps\*

</td>
<td>


xps_maps\[2\]

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


\__netif_set_xps_queue

</td>
</tr>
<tr>
<td>


struct bpf_mprog_entry

</td>
<td>


tcx_egress

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


sch_handle_egress

</td>
</tr>
<tr>
<td>


struct nf_hook_entries\*

</td>
<td>


nf_hooks_egress

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


struct hlist_head

</td>
<td>


qdisc_hash\[16\]

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


struct timer_list

</td>
<td>


watchdog_timer

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


watchdog_timeo

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


u32

</td>
<td>


proto_down_reason

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


struct list_head

</td>
<td>


todo_list

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


int__percpu\*

</td>
<td>


pcpu_refcnt

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


refcount_t

</td>
<td>


dev_refcnt

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


struct ref_tracker_dir

</td>
<td>


refcnt_tracker

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


struct list_head

</td>
<td>


link_watch_list

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


enum:8

</td>
<td>


reg_state

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


bool

</td>
<td>


dismantle

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


bool

</td>
<td>


rtnl_link_initilizing

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


bool

</td>
<td>


needs_free_netdev

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


void\*priv_destructor

</td>
<td>


struct net_device

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


struct netpoll_info\*

</td>
<td>


npinfo

</td>
<td>




</td>
<td>


read_mostly

</td>
<td>


napi_poll/napi_poll_lock

</td>
</tr>
<tr>
<td>


possible_net_t

</td>
<td>


nd_net

</td>
<td>




</td>
<td>


read_mostly

</td>
<td>


(dev_net)napi_busy_loop,tcp_v(4/6)\_rcv,ip(v6)\_rcv,ip(6)\_input,ip(6)\_input_finish

</td>
</tr>
<tr>
<td>


void\*

</td>
<td>


ml_priv

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


enum_netdev_ml_priv_type

</td>
<td>


ml_priv_type

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


struct pcpu_lstats__percpu\*

</td>
<td>


lstats

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


dev_lstats_add()

</td>
</tr>
<tr>
<td>


struct pcpu_sw_netstats__percpu\*

</td>
<td>


tstats

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


dev_sw_netstats_tx_add()

</td>
</tr>
<tr>
<td>


struct pcpu_dstats__percpu\*

</td>
<td>


dstats

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


struct garp_port\*

</td>
<td>


garp_port

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


struct mrp_port\*

</td>
<td>


mrp_port

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


struct dm_hw_stat_delta\*

</td>
<td>


dm_private

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


struct device

</td>
<td>


dev

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


struct attribute_group\*

</td>
<td>


sysfs_groups\[4\]

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


struct attribute_group\*

</td>
<td>


sysfs_rx_queue_group

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


struct rtnl_link_ops\*

</td>
<td>


rtnl_link_ops

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


unsigned_int

</td>
<td>


gso_max_size

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


sk_dst_gso_max_size

</td>
</tr>
<tr>
<td>


unsigned_int

</td>
<td>


tso_max_size

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


u16

</td>
<td>


gso_max_segs

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


gso_max_segs

</td>
</tr>
<tr>
<td>


u16

</td>
<td>


tso_max_segs

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


unsigned_int

</td>
<td>


gso_ipv4_max_size

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


sk_dst_gso_max_size

</td>
</tr>
<tr>
<td>


struct dcbnl_rtnl_ops\*

</td>
<td>


dcbnl_ops

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


num_tc

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


skb_tx_hash

</td>
</tr>
<tr>
<td>


struct netdev_tc_txq

</td>
<td>


tc_to_txq\[16\]

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


skb_tx_hash

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


prio_tc_map\[16\]

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


unsigned_int

</td>
<td>


fcoe_ddp_xid

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


struct netprio_map\*

</td>
<td>


priomap

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


struct phy_device\*

</td>
<td>


phydev

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


struct sfp_bus\*

</td>
<td>


sfp_bus

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


struct lock_class_key\*

</td>
<td>


qdisc_tx_busylock

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


bool

</td>
<td>


proto_down

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


unsigned:1

</td>
<td>


wol_enabled

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


unsigned_long:1

</td>
<td>


see_all_hwtstamp_requests

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


unsigned_long:1

</td>
<td>


change_proto_down

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


unsigned_long:1

</td>
<td>


netns_immutable

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


unsigned_long:1

</td>
<td>


fcoe_mtu

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


struct list_head

</td>
<td>


net_notifier_list

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


struct macsec_ops\*

</td>
<td>


macsec_ops

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


struct udp_tunnel_nic_info\*

</td>
<td>


udp_tunnel_nic_info

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


struct udp_tunnel_nic\*

</td>
<td>


udp_tunnel_nic

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


unsigned_int

</td>
<td>


xdp_zc_max_segs

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


struct bpf_xdp_entity

</td>
<td>


xdp_state\[3\]

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


dev_addr_shadow\[32\]

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


netdevice_tracker

</td>
<td>


linkwatch_dev_tracker

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


netdevice_tracker

</td>
<td>


watchdog_dev_tracker

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


netdevice_tracker

</td>
<td>


dev_registered_tracker

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


struct rtnl_hw_stats64\*

</td>
<td>


offload_xstats_l3

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


struct devlink_port\*

</td>
<td>


devlink_port

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


struct dpll_pin\*

</td>
<td>


dpll_pin

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


struct hlist_head

</td>
<td>


page_pools

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


struct dim_irq_moder\*

</td>
<td>


irq_moder

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


u64

</td>
<td>


max_pacing_offload_horizon

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


struct_napi_config\*

</td>
<td>


napi_config

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


unsigned_long

</td>
<td>


gro_flush_timeout

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


u32

</td>
<td>


napi_defer_hard_irqs

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


struct hlist_head

</td>
<td>


neighbours\[2\]

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
