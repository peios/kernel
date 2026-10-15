---
title: "Ethtool counters"
type: reference
description: "Overview"
---

<a id="rst-ethtool-counters"></a>

<!-- SPDX-License-Identifier: GPL-2.0 OR Linux-OpenIB -->

<!-- This data file has been placed in the public domain. -->

<!-- Derived from the Unicode character mappings available from
<http://www.w3.org/2003/entities/xml/>.
Processed by unicode2rstsubs.py, part of Docutils:
<https://docutils.sourceforge.io>. -->

**Copyright:** © 2023, NVIDIA CORPORATION &amp; AFFILIATES. All rights reserved.

<a id="rst-contents"></a>

## Contents

- [Overview](<#rst-overview>)

- [Groups](<#rst-groups>)

- [Types](<#rst-types>)

- [Descriptions](<#rst-descriptions>)

<a id="rst-overview"></a>

## Overview

There are several counter groups based on where the counter is being counted. In addition, each group of counters may have different counter types.

These counter groups are based on which component in a networking setup, illustrated below, that they describe:



```text
                                              ----------------------------------------
                                              |                                      |
----------------------------------------    ---------------------------------------- |
|              Hypervisor              |    |                  VM                  | |
|                                      |    |                                      | |
| -------------------  --------------- |    | -------------------  --------------- | |
| | Ethernet driver |  | RDMA driver | |    | | Ethernet driver |  | RDMA driver | | |
| -------------------  --------------- |    | -------------------  --------------- | |
|           |                 |        |    |           |                 |        | |
|           -------------------        |    |           -------------------        | |
|                   |                  |    |                   |                  |--
----------------------------------------    ----------------------------------------
                    |                                           |
        -------------               -----------------------------
        |                           |
     ------                      ------ ------ ------         ------      ------      ------
-----| PF |----------------------| VF |-| VF |-| VF |-----  --| PF |--- --| PF |--- --| PF |---
|    ------                      ------ ------ ------    |  | ------  | | ------  | | ------  |
|                                                        |  |         | |         | |         |
|                                                        |  |         | |         | |         |
|                                                        |  |         | |         | |         |
| eSwitch                                                |  | eSwitch | | eSwitch | | eSwitch |
----------------------------------------------------------  ----------- ----------- -----------
           -------------------------------------------------------------------------------
           |                                                                             |
           |                                                                             |
           | Uplink (no counters)                                                        |
           -------------------------------------------------------------------------------
                   ---------------------------------------------------------------
                   |                                                             |
                   |                                                             |
                   | MPFS (no counters)                                          |
                   ---------------------------------------------------------------
                                                 |
                                                 |
                                                 | Port
```

<a id="rst-groups"></a>

## Groups

- **Ring**

  Software counters populated by the driver stack.

- **Netdev**

  An aggregation of software ring counters.

- **vPort counters**

  Traffic counters and drops due to steering or no buffers. May indicate issues with NIC. These counters include Ethernet traffic counters (including Raw Ethernet) and RDMA/RoCE traffic counters.

- **Physical port counters**

  Counters that collect statistics about the PFs and VFs. May indicate issues with NIC, link, or network. This measuring point holds information on standardized counters like IEEE 802.3, RFC2863, RFC 2819, RFC 3635 and additional counters like flow control, FEC and more. Physical port counters are not exposed to virtual machines.

- **Priority Port Counters**

  A set of the physical port counters, per priority per port.

<a id="rst-types"></a>

## Types

Counters are divided into three types.

- **Traffic Informative Counters**

  Counters which count traffic. These counters can be used for load estimation or for general debug.

- **Traffic Acceleration Counters**

  Counters which count traffic that was accelerated by Mellanox driver or by hardware. The counters are an additional layer to the informative counter set, and the same traffic is counted in both informative and acceleration counters.

<a id="rst-accel"></a>



**[1]** Traffic acceleration counter.

- **Error Counters**

  Increment of these counters might indicate a problem. Each of these counters has an explanation and correction action.

Statistic can be fetched via the `ip link` or `ethtool` commands. `ethtool` provides more detailed information.:



```text
ip –s link show <if-name>
ethtool -S <if-name>
```

<a id="rst-descriptions"></a>

## Descriptions

XSK, PTP, and QoS counters that are similar to counters defined previously will not be separately listed. For example, `ptp_tx[i]_packets` will not be explicitly documented since `tx[i]_packets` describes the behavior of both counters, except `ptp_tx[i]_packets` is only counted when precision time protocol is used.

<a id="rst-ring-netdev-counter"></a>

### Ring / Netdev Counter

The following counters are available per ring or software port.

These counters provide information on the amount of traffic that was accelerated by the NIC. The counters are counting the accelerated traffic in addition to the standard counters which counts it (i.e. accelerated traffic is counted twice).

The counter names in the table below refers to both ring and port counters. The notation for ring counters includes the \[i\] index without the braces. The notation for port counters doesn't include the \[i\]. A counter name `rx[i]_packets` will be printed as `rx0_packets` for ring 0 and `rx_packets` for the software port.


<table>
<caption>Ring / Software Port Counter Table</caption>
<tbody>
<tr>
<td>


Counter

</td>
<td>


Description

</td>
<td>


Type

</td>
</tr>
<tr>
<td>


`rx[i]_packets`

</td>
<td>


The number of packets received on ring i.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx[i]_bytes`

</td>
<td>


The number of bytes received on ring i.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx[i]_packets`

</td>
<td>


The number of packets transmitted on ring i.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx[i]_bytes`

</td>
<td>


The number of bytes transmitted on ring i.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx[i]_recover`

</td>
<td>


The number of times the SQ was recovered.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`tx[i]_cqes`

</td>
<td>


Number of CQEs events on SQ issued on ring i.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx[i]_cqe_err`

</td>
<td>


The number of error CQEs encountered on the SQ for ring i.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`tx[i]_tso_packets`

</td>
<td>


The number of TSO packets transmitted on ring i <a id="rst-footnote-reference-1"></a>[1](#rst-accel).

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`tx[i]_tso_bytes`

</td>
<td>


The number of TSO bytes transmitted on ring i <a id="rst-footnote-reference-2"></a>[1](#rst-accel).

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`tx[i]_tso_inner_packets`

</td>
<td>


The number of TSO packets which are indicated to be carry internal encapsulation transmitted on ring i <a id="rst-footnote-reference-3"></a>[1](#rst-accel).

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`tx[i]_tso_inner_bytes`

</td>
<td>


The number of TSO bytes which are indicated to be carry internal encapsulation transmitted on ring i <a id="rst-footnote-reference-4"></a>[1](#rst-accel).

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`rx[i]_gro_packets`

</td>
<td>


Number of received packets processed using hardware-accelerated GRO. The number of hardware GRO offloaded packets received on ring i. Only true GRO packets are counted: only packets that are in an SKB with a GRO count &gt; 1.

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`rx[i]_gro_bytes`

</td>
<td>


Number of received bytes processed using hardware-accelerated GRO. The number of hardware GRO offloaded bytes received on ring i. Only true GRO packets are counted: only packets that are in an SKB with a GRO count &gt; 1.

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`rx[i]_gro_skbs`

</td>
<td>


The number of GRO SKBs constructed from hardware-accelerated GRO. Only SKBs with a GRO count &gt; 1 are counted.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx[i]_gro_large_hds`

</td>
<td>


Number of receive packets using hardware-accelerated GRO that have large headers that require additional memory to be allocated.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx[i]_hds_nodata_packets`

</td>
<td>


Number of header only packets in header/data split mode <a id="rst-footnote-reference-5"></a>[1](#rst-accel).

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx[i]_hds_nodata_bytes`

</td>
<td>


Number of bytes for header only packets in header/data split mode <a id="rst-footnote-reference-6"></a>[1](#rst-accel).

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx[i]_hds_nosplit_packets`

</td>
<td>


Number of packets that were not split in header/data split mode. A packet will not get split when the hardware does not support its protocol splitting. An example such a protocol is ICMPv4/v6. Currently TCP and UDP with IPv4/IPv6 are supported for header/data split <a id="rst-footnote-reference-7"></a>[1](#rst-accel).

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx[i]_hds_nosplit_bytes`

</td>
<td>


Number of bytes for packets that were not split in header/data split mode. A packet will not get split when the hardware does not support its protocol splitting. An example such a protocol is ICMPv4/v6. Currently TCP and UDP with IPv4/IPv6 are supported for header/data split <a id="rst-footnote-reference-8"></a>[1](#rst-accel).

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx[i]_lro_packets`

</td>
<td>


The number of LRO packets received on ring i <a id="rst-footnote-reference-9"></a>[1](#rst-accel).

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`rx[i]_lro_bytes`

</td>
<td>


The number of LRO bytes received on ring i <a id="rst-footnote-reference-10"></a>[1](#rst-accel).

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`rx[i]_ecn_mark`

</td>
<td>


The number of received packets where the ECN mark was turned on.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_oversize_pkts_buffer`

</td>
<td>


The number of dropped received packets due to length which arrived to RQ and exceed software buffer size allocated by the device for incoming traffic. It might imply that the device MTU is larger than the software buffers size.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`rx_oversize_pkts_sw_drop`

</td>
<td>


Number of received packets dropped in software because the CQE data is larger than the MTU size.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`rx[i]_csum_unnecessary`

</td>
<td>


Packets received with a `CHECKSUM_UNNECESSARY` on ring i <a id="rst-footnote-reference-11"></a>[1](#rst-accel).

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`rx[i]_csum_unnecessary_inner`

</td>
<td>


Packets received with inner encapsulation with a `CHECKSUM_UNNECESSARY` on ring i <a id="rst-footnote-reference-12"></a>[1](#rst-accel).

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`rx[i]_csum_none`

</td>
<td>


Packets received with a `CHECKSUM_NONE` on ring i <a id="rst-footnote-reference-13"></a>[1](#rst-accel).

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`rx[i]_csum_complete`

</td>
<td>


Packets received with a `CHECKSUM_COMPLETE` on ring i <a id="rst-footnote-reference-14"></a>[1](#rst-accel).

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`rx[i]_csum_complete_tail`

</td>
<td>


Number of received packets that had checksum calculation computed, potentially needed padding, and were able to do so with `CHECKSUM_PARTIAL`.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx[i]_csum_complete_tail_slow`

</td>
<td>


Number of received packets that need padding larger than eight bytes for the checksum.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx[i]_csum_partial`

</td>
<td>


Packets transmitted with a `CHECKSUM_PARTIAL` on ring i <a id="rst-footnote-reference-15"></a>[1](#rst-accel).

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`tx[i]_csum_partial_inner`

</td>
<td>


Packets transmitted with inner encapsulation with a `CHECKSUM_PARTIAL` on ring i <a id="rst-footnote-reference-16"></a>[1](#rst-accel).

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`tx[i]_csum_none`

</td>
<td>


Packets transmitted with no hardware checksum acceleration on ring i.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx[i]_stopped` / `tx_queue_stopped` <a id="rst-footnote-reference-17"></a>[2](#rst-ring-global)

</td>
<td>


Events where SQ was full on ring i. If this counter is increased, check the amount of buffers allocated for transmission.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx[i]_wake` / `tx_queue_wake` <a id="rst-footnote-reference-18"></a>[2](#rst-ring-global)

</td>
<td>


Events where SQ was full and has become not full on ring i.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx[i]_dropped` / `tx_queue_dropped` <a id="rst-footnote-reference-19"></a>[2](#rst-ring-global)

</td>
<td>


Packets transmitted that were dropped due to DMA mapping failure on ring i. If this counter is increased, check the amount of buffers allocated for transmission.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`tx[i]_nop`

</td>
<td>


The number of nop WQEs (empty WQEs) inserted to the SQ (related to ring i) due to the reach of the end of the cyclic buffer. When reaching near to the end of cyclic buffer the driver may add those empty WQEs to avoid handling a state the a WQE start in the end of the queue and ends in the beginning of the queue. This is a normal condition.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx[i]_timestamps`

</td>
<td>


Transmitted packets that were hardware timestamped at the device's DMA layer.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx[i]_added_vlan_packets`

</td>
<td>


The number of packets sent where vlan tag insertion was offloaded to the hardware.

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`rx[i]_removed_vlan_packets`

</td>
<td>


The number of packets received where vlan tag stripping was offloaded to the hardware.

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`rx[i]_wqe_err`

</td>
<td>


The number of wrong opcodes received on ring i.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`rx[i]_mpwqe_frag`

</td>
<td>


The number of WQEs that failed to allocate compound page and hence fragmented MPWQE’s (Multi Packet WQEs) were used on ring i. If this counter raise, it may suggest that there is no enough memory for large pages, the driver allocated fragmented pages. This is not abnormal condition.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx[i]_mpwqe_filler_cqes`

</td>
<td>


The number of filler CQEs events that were issued on ring i.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx[i]_mpwqe_filler_strides`

</td>
<td>


The number of strides consumed by filler CQEs on ring i.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx[i]_mpwqe_blks`

</td>
<td>


The number of send blocks processed from Multi-Packet WQEs (mpwqe).

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx[i]_mpwqe_pkts`

</td>
<td>


The number of send packets processed from Multi-Packet WQEs (mpwqe).

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx[i]_cqe_compress_blks`

</td>
<td>


The number of receive blocks with CQE compression on ring i <a id="rst-footnote-reference-20"></a>[1](#rst-accel).

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`rx[i]_cqe_compress_pkts`

</td>
<td>


The number of receive packets with CQE compression on ring i <a id="rst-footnote-reference-21"></a>[1](#rst-accel).

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`rx[i]_arfs_add`

</td>
<td>


The number of aRFS flow rules added to the device for direct RQ steering on ring i <a id="rst-footnote-reference-22"></a>[1](#rst-accel).

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`rx[i]_arfs_request_in`

</td>
<td>


Number of flow rules that have been requested to move into ring i for direct RQ steering <a id="rst-footnote-reference-23"></a>[1](#rst-accel).

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`rx[i]_arfs_request_out`

</td>
<td>


Number of flow rules that have been requested to move out of ring i <a id="rst-footnote-reference-24"></a>[1](#rst-accel).

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`rx[i]_arfs_expired`

</td>
<td>


Number of flow rules that have been expired and removed <a id="rst-footnote-reference-25"></a>[1](#rst-accel).

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`rx[i]_arfs_err`

</td>
<td>


Number of flow rules that failed to be added to the flow table.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`rx[i]_recover`

</td>
<td>


The number of times the RQ was recovered.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`tx[i]_xmit_more`

</td>
<td>


The number of packets sent with `xmit_more` indication set on the skbuff (no doorbell).

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`ch[i]_poll`

</td>
<td>


The number of invocations of NAPI poll of channel i.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`ch[i]_arm`

</td>
<td>


The number of times the NAPI poll function completed and armed the completion queues on channel i.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`ch[i]_aff_change`

</td>
<td>


The number of times the NAPI poll function explicitly stopped execution on a CPU due to a change in affinity, on channel i.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`ch[i]_events`

</td>
<td>


The number of hard interrupt events on the completion queues of channel i.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`ch[i]_eq_rearm`

</td>
<td>


The number of times the EQ was recovered.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`ch[i]_force_irq`

</td>
<td>


Number of times NAPI is triggered by XSK wakeups by posting a NOP to ICOSQ.

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`rx[i]_congst_umr`

</td>
<td>


The number of times an outstanding UMR request is delayed due to congestion, on ring i.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_pp_alloc_fast`

</td>
<td>


Number of successful fast path allocations.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_pp_alloc_slow`

</td>
<td>


Number of slow path order-0 allocations.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_pp_alloc_slow_high_order`

</td>
<td>


Number of slow path high order allocations.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_pp_alloc_empty`

</td>
<td>


Counter is incremented when ptr ring is empty, so a slow path allocation was forced.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_pp_alloc_refill`

</td>
<td>


Counter is incremented when an allocation which triggered a refill of the cache.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_pp_alloc_waive`

</td>
<td>


Counter is incremented when pages obtained from the ptr ring that cannot be added to the cache due to a NUMA mismatch.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_pp_recycle_cached`

</td>
<td>


Counter is incremented when recycling placed page in the page pool cache.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_pp_recycle_cache_full`

</td>
<td>


Counter is incremented when page pool cache was full.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_pp_recycle_ring`

</td>
<td>


Counter is incremented when page placed into the ptr ring.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_pp_recycle_ring_full`

</td>
<td>


Counter is incremented when page released from page pool because the ptr ring was full.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_pp_recycle_released_ref`

</td>
<td>


Counter is incremented when page released (and not recycled) because refcnt &gt; 1.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx[i]_xsk_buff_alloc_err`

</td>
<td>


The number of times allocating an skb or XSK buffer failed in the XSK RQ context.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`rx[i]_xdp_tx_xmit`

</td>
<td>


The number of packets forwarded back to the port due to XDP program `XDP_TX` action (bouncing). these packets are not counted by other software counters. These packets are counted by physical port and vPort counters.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx[i]_xdp_tx_mpwqe`

</td>
<td>


Number of multi-packet WQEs transmitted by the netdev and `XDP_TX`-ed by the netdev during the RQ context.

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`rx[i]_xdp_tx_inlnw`

</td>
<td>


Number of WQE data segments transmitted where the data could be inlined in the WQE and then `XDP_TX`-ed during the RQ context.

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`rx[i]_xdp_tx_nops`

</td>
<td>


Number of NOP WQEBBs (WQE building blocks) received posted to the XDP SQ.

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`rx[i]_xdp_tx_full`

</td>
<td>


The number of packets that should have been forwarded back to the port due to `XDP_TX` action but were dropped due to full tx queue. These packets are not counted by other software counters. These packets are counted by physical port and vPort counters. You may open more rx queues and spread traffic rx over all queues and/or increase rx ring size.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`rx[i]_xdp_tx_err`

</td>
<td>


The number of times an `XDP_TX` error such as frame too long and frame too short occurred on `XDP_TX` ring of RX ring.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`rx[i]_xdp_tx_cqes` / `rx_xdp_tx_cqe` <a id="rst-footnote-reference-26"></a>[2](#rst-ring-global)

</td>
<td>


The number of completions received on the CQ of the `XDP_TX` ring.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx[i]_xdp_drop`

</td>
<td>


The number of packets dropped due to XDP program `XDP_DROP` action. these packets are not counted by other software counters. These packets are counted by physical port and vPort counters.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx[i]_xdp_redirect`

</td>
<td>


The number of times an XDP redirect action was triggered on ring i.

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`tx[i]_xdp_xmit`

</td>
<td>


The number of packets redirected to the interface(due to XDP redirect). These packets are not counted by other software counters. These packets are counted by physical port and vPort counters.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx[i]_xdp_full`

</td>
<td>


The number of packets redirected to the interface(due to XDP redirect), but were dropped due to full tx queue. these packets are not counted by other software counters. you may enlarge tx queues.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx[i]_xdp_mpwqe`

</td>
<td>


Number of multi-packet WQEs offloaded onto the NIC that were `XDP_REDIRECT`-ed from other netdevs.

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`tx[i]_xdp_inlnw`

</td>
<td>


Number of WQE data segments where the data could be inlined in the WQE where the data segments were `XDP_REDIRECT`-ed from other netdevs.

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`tx[i]_xdp_nops`

</td>
<td>


Number of NOP WQEBBs (WQE building blocks) posted to the SQ that were `XDP_REDIRECT`-ed from other netdevs.

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`tx[i]_xdp_err`

</td>
<td>


The number of packets redirected to the interface(due to XDP redirect) but were dropped due to error such as frame too long and frame too short.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`tx[i]_xdp_cqes`

</td>
<td>


The number of completions received for packets redirected to the interface(due to XDP redirect) on the CQ.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx[i]_xsk_xmit`

</td>
<td>


The number of packets transmitted using XSK zerocopy functionality.

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`tx[i]_xsk_mpwqe`

</td>
<td>


Number of multi-packet WQEs offloaded onto the NIC that were `XDP_REDIRECT`-ed from other netdevs.

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`tx[i]_xsk_inlnw`

</td>
<td>


Number of WQE data segments where the data could be inlined in the WQE that are transmitted using XSK zerocopy.

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`tx[i]_xsk_full`

</td>
<td>


Number of times doorbell is rung in XSK zerocopy mode when SQ is full.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`tx[i]_xsk_err`

</td>
<td>


Number of errors that occurred in XSK zerocopy mode such as if the data size is larger than the MTU size.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`tx[i]_xsk_cqes`

</td>
<td>


Number of CQEs processed in XSK zerocopy mode.

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`tx_tls_ctx`

</td>
<td>


Number of TLS TX HW offload contexts added to device for encryption.

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`tx_tls_del`

</td>
<td>


Number of TLS TX HW offload contexts removed from device (connection closed).

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`tx_tls_pool_alloc`

</td>
<td>


Number of times a unit of work is successfully allocated in the TLS HW offload pool.

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`tx_tls_pool_free`

</td>
<td>


Number of times a unit of work is freed in the TLS HW offload pool.

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`rx_tls_ctx`

</td>
<td>


Number of TLS RX HW offload contexts added to device for decryption.

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`rx_tls_del`

</td>
<td>


Number of TLS RX HW offload contexts deleted from device (connection has finished).

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`rx[i]_tls_decrypted_packets`

</td>
<td>


Number of successfully decrypted RX packets which were part of a TLS stream.

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`rx[i]_tls_decrypted_bytes`

</td>
<td>


Number of TLS payload bytes in RX packets which were successfully decrypted.

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`rx[i]_tls_resync_req_pkt`

</td>
<td>


Number of received TLS packets with a resync request.

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`rx[i]_tls_resync_req_start`

</td>
<td>


Number of times the TLS async resync request was started.

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`rx[i]_tls_resync_req_end`

</td>
<td>


Number of times the TLS async resync request properly ended with providing the HW tracked tcp-seq.

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`rx[i]_tls_resync_req_skip`

</td>
<td>


Number of times the TLS async resync request procedure was started but not properly ended.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`rx[i]_tls_resync_res_ok`

</td>
<td>


Number of times the TLS resync response call to the driver was successfully handled.

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`rx[i]_tls_resync_res_retry`

</td>
<td>


Number of times the TLS resync response call to the driver was reattempted when ICOSQ is full.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`rx[i]_tls_resync_res_skip`

</td>
<td>


Number of times the TLS resync response call to the driver was terminated unsuccessfully.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`rx[i]_tls_err`

</td>
<td>


Number of times when CQE TLS offload was problematic.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`tx[i]_tls_encrypted_packets`

</td>
<td>


The number of send packets that are TLS encrypted by the kernel.

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`tx[i]_tls_encrypted_bytes`

</td>
<td>


The number of send bytes that are TLS encrypted by the kernel.

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`tx[i]_tls_ooo`

</td>
<td>


Number of times out of order TLS SQE fragments were handled on ring i.

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`tx[i]_tls_dump_packets`

</td>
<td>


Number of TLS decrypted packets copied over from NIC over DMA.

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`tx[i]_tls_dump_bytes`

</td>
<td>


Number of TLS decrypted bytes copied over from NIC over DMA.

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`tx[i]_tls_resync_bytes`

</td>
<td>


Number of TLS bytes requested to be resynchronized in order to be decrypted.

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`tx[i]_tls_skip_no_sync_data`

</td>
<td>


Number of TLS send data that can safely be skipped / do not need to be decrypted.

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`tx[i]_tls_drop_no_sync_data`

</td>
<td>


Number of TLS send data that were dropped due to retransmission of TLS data.

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`ptp_cq[i]_abort`

</td>
<td>


Number of times a CQE has to be skipped in precision time protocol due to a skew between the port timestamp and CQE timestamp being greater than 128 seconds.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`ptp_cq[i]_abort_abs_diff_ns`

</td>
<td>


Accumulation of time differences between the port timestamp and CQE timestamp when the difference is greater than 128 seconds in precision time protocol.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`ptp_cq[i]_late_cqe`

</td>
<td>


Number of times a CQE has been delivered on the PTP timestamping CQ when the CQE was not expected since a certain amount of time had elapsed where the device typically ensures not posting the CQE.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`ptp_cq[i]_lost_cqe`

</td>
<td>


Number of times a CQE is expected to not be delivered on the PTP timestamping CQE by the device due to a time delta elapsing. If such a CQE is somehow delivered, `ptp_cq[i]_late_cqe` is incremented.

</td>
<td>


Error

</td>
</tr>
</tbody>
</table>

<a id="rst-ring-global"></a>



**[2]** The corresponding ring and global counters do not share the same name (i.e. do not follow the common naming scheme).

<a id="rst-vport-counters"></a>

### vPort Counters

Counters on the NIC port that is connected to a eSwitch.


<table>
<caption>vPort Counter Table</caption>
<tbody>
<tr>
<td>


Counter

</td>
<td>


Description

</td>
<td>


Type

</td>
</tr>
<tr>
<td>


`rx_vport_unicast_packets`

</td>
<td>


Unicast packets received, steered to a port including Raw Ethernet QP/DPDK traffic, excluding RDMA traffic.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_vport_unicast_bytes`

</td>
<td>


Unicast bytes received, steered to a port including Raw Ethernet QP/DPDK traffic, excluding RDMA traffic.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx_vport_unicast_packets`

</td>
<td>


Unicast packets transmitted, steered from a port including Raw Ethernet QP/DPDK traffic, excluding RDMA traffic.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx_vport_unicast_bytes`

</td>
<td>


Unicast bytes transmitted, steered from a port including Raw Ethernet QP/DPDK traffic, excluding RDMA traffic.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_vport_multicast_packets`

</td>
<td>


Multicast packets received, steered to a port including Raw Ethernet QP/DPDK traffic, excluding RDMA traffic.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_vport_multicast_bytes`

</td>
<td>


Multicast bytes received, steered to a port including Raw Ethernet QP/DPDK traffic, excluding RDMA traffic.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx_vport_multicast_packets`

</td>
<td>


Multicast packets transmitted, steered from a port including Raw Ethernet QP/DPDK traffic, excluding RDMA traffic.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx_vport_multicast_bytes`

</td>
<td>


Multicast bytes transmitted, steered from a port including Raw Ethernet QP/DPDK traffic, excluding RDMA traffic.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_vport_broadcast_packets`

</td>
<td>


Broadcast packets received, steered to a port including Raw Ethernet QP/DPDK traffic, excluding RDMA traffic.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_vport_broadcast_bytes`

</td>
<td>


Broadcast bytes received, steered to a port including Raw Ethernet QP/DPDK traffic, excluding RDMA traffic.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx_vport_broadcast_packets`

</td>
<td>


Broadcast packets transmitted, steered from a port including Raw Ethernet QP/DPDK traffic, excluding RDMA traffic.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx_vport_broadcast_bytes`

</td>
<td>


Broadcast bytes transmitted, steered from a port including Raw Ethernet QP/DPDK traffic, excluding RDMA traffic.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_vport_rdma_unicast_packets`

</td>
<td>


RDMA unicast packets received, steered to a port (counters counts RoCE/UD/RC traffic) <a id="rst-footnote-reference-27"></a>[1](#rst-accel).

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`rx_vport_rdma_unicast_bytes`

</td>
<td>


RDMA unicast bytes received, steered to a port (counters counts RoCE/UD/RC traffic) <a id="rst-footnote-reference-28"></a>[1](#rst-accel).

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`tx_vport_rdma_unicast_packets`

</td>
<td>


RDMA unicast packets transmitted, steered from a port (counters counts RoCE/UD/RC traffic) <a id="rst-footnote-reference-29"></a>[1](#rst-accel).

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`tx_vport_rdma_unicast_bytes`

</td>
<td>


RDMA unicast bytes transmitted, steered from a port (counters counts RoCE/UD/RC traffic) <a id="rst-footnote-reference-30"></a>[1](#rst-accel).

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`rx_vport_rdma_multicast_packets`

</td>
<td>


RDMA multicast packets received, steered to a port (counters counts RoCE/UD/RC traffic) <a id="rst-footnote-reference-31"></a>[1](#rst-accel).

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`rx_vport_rdma_multicast_bytes`

</td>
<td>


RDMA multicast bytes received, steered to a port (counters counts RoCE/UD/RC traffic) <a id="rst-footnote-reference-32"></a>[1](#rst-accel).

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`tx_vport_rdma_multicast_packets`

</td>
<td>


RDMA multicast packets transmitted, steered from a port (counters counts RoCE/UD/RC traffic) <a id="rst-footnote-reference-33"></a>[1](#rst-accel).

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`tx_vport_rdma_multicast_bytes`

</td>
<td>


RDMA multicast bytes transmitted, steered from a port (counters counts RoCE/UD/RC traffic) <a id="rst-footnote-reference-34"></a>[1](#rst-accel).

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`vport_loopback_packets`

</td>
<td>


Unicast, multicast and broadcast packets that were loop-back (received and transmitted), IB/Eth  <a id="rst-footnote-reference-35"></a>[1](#rst-accel).

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`vport_loopback_bytes`

</td>
<td>


Unicast, multicast and broadcast bytes that were loop-back (received and transmitted), IB/Eth  <a id="rst-footnote-reference-36"></a>[1](#rst-accel).

</td>
<td>


Acceleration

</td>
</tr>
<tr>
<td>


`rx_steer_missed_packets`

</td>
<td>


Number of packets that was received by the NIC, however was discarded because it did not match any flow in the NIC flow table.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`rx_packets`

</td>
<td>


Representor only: packets received, that were handled by the hypervisor.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_bytes`

</td>
<td>


Representor only: bytes received, that were handled by the hypervisor.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx_packets`

</td>
<td>


Representor only: packets transmitted, that were handled by the hypervisor.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx_bytes`

</td>
<td>


Representor only: bytes transmitted, that were handled by the hypervisor.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`dev_internal_queue_oob`

</td>
<td>


The number of dropped packets due to lack of receive WQEs for an internal device RQ.

</td>
<td>


Error

</td>
</tr>
</tbody>
</table>

<a id="rst-physical-port-counters"></a>

### Physical Port Counters

The physical port counters are the counters on the external port connecting the adapter to the network. This measuring point holds information on standardized counters like IEEE 802.3, RFC2863, RFC 2819, RFC 3635 and additional counters like flow control, FEC and more.


<table>
<caption>Physical Port Counter Table</caption>
<tbody>
<tr>
<td>


Counter

</td>
<td>


Description

</td>
<td>


Type

</td>
</tr>
<tr>
<td>


`rx_packets_phy`

</td>
<td>


The number of packets received on the physical port. This counter doesn’t include packets that were discarded due to FCS, frame size and similar errors.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx_packets_phy`

</td>
<td>


The number of packets transmitted on the physical port.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_bytes_phy`

</td>
<td>


The number of bytes received on the physical port, including Ethernet header and FCS.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx_bytes_phy`

</td>
<td>


The number of bytes transmitted on the physical port.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_multicast_phy`

</td>
<td>


The number of multicast packets received on the physical port.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx_multicast_phy`

</td>
<td>


The number of multicast packets transmitted on the physical port.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_broadcast_phy`

</td>
<td>


The number of broadcast packets received on the physical port.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx_broadcast_phy`

</td>
<td>


The number of broadcast packets transmitted on the physical port.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_crc_errors_phy`

</td>
<td>


The number of dropped received packets due to FCS (Frame Check Sequence) error on the physical port. If this counter is increased in high rate, check the link quality using `rx_symbol_error_phy` and `rx_corrected_bits_phy` counters below.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`rx_in_range_len_errors_phy`

</td>
<td>


The number of received packets dropped due to length/type errors on a physical port.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`rx_out_of_range_len_phy`

</td>
<td>


The number of received packets dropped due to length greater than allowed on a physical port. If this counter is increasing, it implies that the peer connected to the adapter has a larger MTU configured. Using same MTU configuration shall resolve this issue.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`rx_oversize_pkts_phy`

</td>
<td>


The number of dropped received packets due to length which exceed MTU size on a physical port. If this counter is increasing, it implies that the peer connected to the adapter has a larger MTU configured. Using same MTU configuration shall resolve this issue.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`rx_symbol_err_phy`

</td>
<td>


The number of received packets dropped due to physical coding errors (symbol errors) on a physical port.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`rx_mac_control_phy`

</td>
<td>


The number of MAC control packets received on the physical port.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx_mac_control_phy`

</td>
<td>


The number of MAC control packets transmitted on the physical port.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_pause_ctrl_phy`

</td>
<td>


The number of link layer pause packets received on a physical port. If this counter is increasing, it implies that the network is congested and cannot absorb the traffic coming from to the adapter.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx_pause_ctrl_phy`

</td>
<td>


The number of link layer pause packets transmitted on a physical port. If this counter is increasing, it implies that the NIC is congested and cannot absorb the traffic coming from the network.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_unsupported_op_phy`

</td>
<td>


The number of MAC control packets received with unsupported opcode on a physical port.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`rx_discards_phy`

</td>
<td>


The number of received packets dropped due to lack of buffers on a physical port. If this counter is increasing, it implies that the adapter is congested and cannot absorb the traffic coming from the network.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`tx_discards_phy`

</td>
<td>


The number of packets which were discarded on transmission, even no errors were detected. the drop might occur due to link in down state, head of line drop, pause from the network, etc.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`tx_errors_phy`

</td>
<td>


The number of transmitted packets dropped due to a length which exceed MTU size on a physical port.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`rx_undersize_pkts_phy`

</td>
<td>


The number of received packets dropped due to length which is shorter than 64 bytes on a physical port. If this counter is increasing, it implies that the peer connected to the adapter has a non-standard MTU configured or malformed packet had arrived.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`rx_fragments_phy`

</td>
<td>


The number of received packets dropped due to a length which is shorter than 64 bytes and has FCS error on a physical port. If this counter is increasing, it implies that the peer connected to the adapter has a non-standard MTU configured.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`rx_jabbers_phy`

</td>
<td>


The number of received packets d due to a length which is longer than 64 bytes and had FCS error on a physical port.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`rx_64_bytes_phy`

</td>
<td>


The number of packets received on the physical port with size of 64 bytes.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_65_to_127_bytes_phy`

</td>
<td>


The number of packets received on the physical port with size of 65 to 127 bytes.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_128_to_255_bytes_phy`

</td>
<td>


The number of packets received on the physical port with size of 128 to 255 bytes.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_256_to_511_bytes_phy`

</td>
<td>


The number of packets received on the physical port with size of 256 to 512 bytes.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_512_to_1023_bytes_phy`

</td>
<td>


The number of packets received on the physical port with size of 512 to 1023 bytes.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_1024_to_1518_bytes_phy`

</td>
<td>


The number of packets received on the physical port with size of 1024 to 1518 bytes.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_1519_to_2047_bytes_phy`

</td>
<td>


The number of packets received on the physical port with size of 1519 to 2047 bytes.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_2048_to_4095_bytes_phy`

</td>
<td>


The number of packets received on the physical port with size of 2048 to 4095 bytes.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_4096_to_8191_bytes_phy`

</td>
<td>


The number of packets received on the physical port with size of 4096 to 8191 bytes.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_8192_to_10239_bytes_phy`

</td>
<td>


The number of packets received on the physical port with size of 8192 to 10239 bytes.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`link_down_events_phy`

</td>
<td>


The number of times where the link operative state changed to down. In case this counter is increasing it may imply on port flapping. You may need to replace the cable/transceiver.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`total_success_recovery_phy`

</td>
<td>


The number of total successful recovery events of any type during ports reset cycle.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`rx_out_of_buffer`

</td>
<td>


Number of times receive queue had no software buffers allocated for the adapter's incoming traffic.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`module_bus_stuck`

</td>
<td>


The number of times that module's I<sup>2</sup>C bus (data or clock) short-wire was detected. You may need to replace the cable/transceiver.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`module_high_temp`

</td>
<td>


The number of times that the module temperature was too high. If this issue persist, you may need to check the ambient temperature or replace the cable/transceiver module.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`module_bad_shorted`

</td>
<td>


The number of times that the module cables were shorted. You may need to replace the cable/transceiver module.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`module_unplug`

</td>
<td>


The number of times that module was ejected.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_buffer_passed_thres_phy`

</td>
<td>


The number of events where the port receive buffer was over 85% full.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx_pause_storm_warning_events`

</td>
<td>


The number of times the device was sending pauses for a long period of time.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx_pause_storm_error_events`

</td>
<td>


The number of times the device was sending pauses for a long period of time, reaching time out and disabling transmission of pause frames. on the period where pause frames were disabled, drop could have been occurred.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`rx[i]_buff_alloc_err`

</td>
<td>


Failed to allocate a buffer to received packet (or SKB) on ring i.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`rx_bits_phy`

</td>
<td>


This counter provides information on the total amount of traffic that could have been received and can be used as a guideline to measure the ratio of errored traffic in `rx_pcs_symbol_err_phy` and `rx_corrected_bits_phy`.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_pcs_symbol_err_phy`

</td>
<td>


This counter counts the number of symbol errors that wasn’t corrected by FEC correction algorithm or that FEC algorithm was not active on this interface. If this counter is increasing, it implies that the link between the NIC and the network is suffering from high BER, and that traffic is lost. You may need to replace the cable/transceiver. The error rate is the number of `rx_pcs_symbol_err_phy` divided by the number of `rx_bits_phy` on a specific time frame.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`rx_corrected_bits_phy`

</td>
<td>


The number of corrected bits on this port according to active FEC (RS/FC). If this counter is increasing, it implies that the link between the NIC and the network is suffering from high BER. The corrected bit rate is the number of `rx_corrected_bits_phy` divided by the number of `rx_bits_phy` on a specific time frame.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`rx_err_lane_[l]_phy`

</td>
<td>


This counter counts the number of physical raw errors per lane l index. The counter counts errors before FEC corrections. If this counter is increasing, it implies that the link between the NIC and the network is suffering from high BER, and that traffic might be lost. You may need to replace the cable/transceiver. Please check in accordance with `rx_corrected_bits_phy`.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`rx_global_pause`

</td>
<td>


The number of pause packets received on the physical port. If this counter is increasing, it implies that the network is congested and cannot absorb the traffic coming from the adapter. Note: This counter is only enabled when global pause mode is enabled.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_global_pause_duration`

</td>
<td>


The duration of pause received (in microSec) on the physical port. The counter represents the time the port did not send any traffic. If this counter is increasing, it implies that the network is congested and cannot absorb the traffic coming from the adapter. Note: This counter is only enabled when global pause mode is enabled.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx_global_pause`

</td>
<td>


The number of pause packets transmitted on a physical port. If this counter is increasing, it implies that the adapter is congested and cannot absorb the traffic coming from the network. Note: This counter is only enabled when global pause mode is enabled.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx_global_pause_duration`

</td>
<td>


The duration of pause transmitter (in microSec) on the physical port. Note: This counter is only enabled when global pause mode is enabled.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_global_pause_transition`

</td>
<td>


The number of times a transition from Xoff to Xon on the physical port has occurred. Note: This counter is only enabled when global pause mode is enabled.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_if_down_packets`

</td>
<td>


The number of received packets that were dropped due to interface down.

</td>
<td>


Informative

</td>
</tr>
</tbody>
</table>

<a id="rst-priority-port-counters"></a>

### Priority Port Counters

The following counters are physical port counters that are counted per L2 priority (0-7).

**Note:** `p` in the counter name represents the priority.


<table>
<caption>Priority Port Counter Table</caption>
<tbody>
<tr>
<td>


Counter

</td>
<td>


Description

</td>
<td>


Type

</td>
</tr>
<tr>
<td>


`rx_prio[p]_bytes`

</td>
<td>


The number of bytes received with priority p on the physical port.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_prio[p]_packets`

</td>
<td>


The number of packets received with priority p on the physical port.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx_prio[p]_bytes`

</td>
<td>


The number of bytes transmitted on priority p on the physical port.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx_prio[p]_packets`

</td>
<td>


The number of packets transmitted on priority p on the physical port.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_prio[p]_pause`

</td>
<td>


The number of pause packets received with priority p on a physical port. If this counter is increasing, it implies that the network is congested and cannot absorb the traffic coming from the adapter. Note: This counter is available only if PFC was enabled on priority p.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_prio[p]_pause_duration`

</td>
<td>


The duration of pause received (in microSec) on priority p on the physical port. The counter represents the time the port did not send any traffic on this priority. If this counter is increasing, it implies that the network is congested and cannot absorb the traffic coming from the adapter. Note: This counter is available only if PFC was enabled on priority p.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_prio[p]_pause_transition`

</td>
<td>


The number of times a transition from Xoff to Xon on priority p on the physical port has occurred. Note: This counter is available only if PFC was enabled on priority p.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx_prio[p]_pause`

</td>
<td>


The number of pause packets transmitted on priority p on a physical port. If this counter is increasing, it implies that the adapter is congested and cannot absorb the traffic coming from the network. Note: This counter is available only if PFC was enabled on priority p.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`tx_prio[p]_pause_duration`

</td>
<td>


The duration of pause transmitter (in microSec) on priority p on the physical port. Note: This counter is available only if PFC was enabled on priority p.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_prio[p]_buf_discard`

</td>
<td>


The number of packets discarded by device due to lack of per host receive buffers.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_prio[p]_cong_discard`

</td>
<td>


The number of packets discarded by device due to per host congestion.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_prio[p]_marked`

</td>
<td>


The number of packets ecn marked by device due to per host congestion.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`rx_prio[p]_discards`

</td>
<td>


The number of packets discarded by device due to lack of receive buffers.

</td>
<td>


Informative

</td>
</tr>
</tbody>
</table>

<a id="rst-device-counters"></a>

### Device Counters


<table>
<caption>Device Counter Table</caption>
<tbody>
<tr>
<td>


Counter

</td>
<td>


Description

</td>
<td>


Type

</td>
</tr>
<tr>
<td>


`rx_pci_signal_integrity`

</td>
<td>


Counts physical layer PCIe signal integrity errors, the number of transitions to recovery due to Framing errors and CRC (dlp and tlp). If this counter is raising, try moving the adapter card to a different slot to rule out a bad PCI slot. Validate that you are running with the latest firmware available and latest server BIOS version.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`tx_pci_signal_integrity`

</td>
<td>


Counts physical layer PCIe signal integrity errors, the number of transition to recovery initiated by the other side (moving to recovery due to getting TS/EIEOS). If this counter is raising, try moving the adapter card to a different slot to rule out a bad PCI slot. Validate that you are running with the latest firmware available and latest server BIOS version.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`outbound_pci_buffer_overflow`

</td>
<td>


The number of packets dropped due to pci buffer overflow. If this counter is raising in high rate, it might indicate that the receive traffic rate for a host is larger than the PCIe bus and therefore a congestion occurs.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`outbound_pci_stalled_rd`

</td>
<td>


The percentage (in the range 0...100) of time within the last second that the NIC had outbound non-posted reads requests but could not perform the operation due to insufficient posted credits.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`outbound_pci_stalled_wr`

</td>
<td>


The percentage (in the range 0...100) of time within the last second that the NIC had outbound posted writes requests but could not perform the operation due to insufficient posted credits.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`outbound_pci_stalled_rd_events`

</td>
<td>


The number of seconds where `outbound_pci_stalled_rd` was above 30%.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`outbound_pci_stalled_wr_events`

</td>
<td>


The number of seconds where `outbound_pci_stalled_wr` was above 30%.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`dev_out_of_buffer`

</td>
<td>


The number of times the device owned queue had not enough buffers allocated.

</td>
<td>


Error

</td>
</tr>
<tr>
<td>


`pci_bw_inbound_high`

</td>
<td>


The number of times the device crossed the high inbound pcie bandwidth threshold. To be compared to pci_bw_inbound_low to check if the device is in a congested state. If pci_bw_inbound_high == pci_bw_inbound_low then the device is not congested. If pci_bw_inbound_high &gt; pci_bw_inbound_low then the device is congested.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`pci_bw_inbound_low`

</td>
<td>


The number of times the device crossed the low inbound PCIe bandwidth threshold. To be compared to pci_bw_inbound_high to check if the device is in a congested state. If pci_bw_inbound_high == pci_bw_inbound_low then the device is not congested. If pci_bw_inbound_high &gt; pci_bw_inbound_low then the device is congested.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`pci_bw_outbound_high`

</td>
<td>


The number of times the device crossed the high outbound pcie bandwidth threshold. To be compared to pci_bw_outbound_low to check if the device is in a congested state. If pci_bw_outbound_high == pci_bw_outbound_low then the device is not congested. If pci_bw_outbound_high &gt; pci_bw_outbound_low then the device is congested.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`pci_bw_outbound_low`

</td>
<td>


The number of times the device crossed the low outbound PCIe bandwidth threshold. To be compared to pci_bw_outbound_high to check if the device is in a congested state. If pci_bw_outbound_high == pci_bw_outbound_low then the device is not congested. If pci_bw_outbound_high &gt; pci_bw_outbound_low then the device is congested.

</td>
<td>


Informative

</td>
</tr>
<tr>
<td>


`pci_bw_stale_event`

</td>
<td>


The number of times the device fired a PCIe congestion event but on query there was no change in state.

</td>
<td>


Informative

</td>
</tr>
</tbody>
</table>
