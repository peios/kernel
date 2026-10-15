---
title: "inet_connection_sock struct fast path usage breakdown"
type: reference
description: "Reference for inet_connection_sock struct fast path usage breakdown."
---

<a id="rst-inet-connection-sock-struct-fast-path-usage-breakdown"></a>

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


struct inet_sock

</td>
<td>


icsk_inet

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


struct request_sock_queue

</td>
<td>


icsk_accept_queue

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


struct inet_bind_bucket

</td>
<td>


icsk_bind_hash

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


tcp_set_state

</td>
</tr>
<tr>
<td>


struct inet_bind2_bucket

</td>
<td>


icsk_bind2_hash

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


tcp_set_state,inet_put_port

</td>
</tr>
<tr>
<td>


struct timer_list

</td>
<td>


icsk_delack_timer

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


inet_csk_reset_xmit_timer,tcp_connect

</td>
</tr>
<tr>
<td>


struct timer_list

</td>
<td>


icsk_keepalive_timer

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


icsk_rto

</td>
<td>


read_write

</td>
<td>




</td>
<td>


tcp_cwnd_validate,tcp_schedule_loss_probe,tcp_connect_init,tcp_connect,tcp_write_xmit,tcp_push_one

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


icsk_rto_min

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


icsk_rto_max

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


tcp_reset_xmit_timer

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


icsk_delack_max

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


icsk_pmtu_cookie

</td>
<td>


read_write

</td>
<td>




</td>
<td>


tcp_sync_mss,tcp_current_mss,tcp_send_syn_data,tcp_connect_init,tcp_connect

</td>
</tr>
<tr>
<td>


struct tcp_congestion_ops

</td>
<td>


icsk_ca_ops

</td>
<td>


read_write

</td>
<td>




</td>
<td>


tcp_cwnd_validate,tcp_tso_segs,tcp_ca_dst_init,tcp_connect_init,tcp_connect,tcp_write_xmit

</td>
</tr>
<tr>
<td>


struct inet_connection_sock_af_ops

</td>
<td>


icsk_af_ops

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


tcp_finish_connect,tcp_send_syn_data,tcp_mtup_init,tcp_mtu_check_reprobe,tcp_mtu_probe,tcp_connect_init,tcp_connect,\__tcp_transmit_skb

</td>
</tr>
<tr>
<td>


struct tcp_ulp_ops\*

</td>
<td>


icsk_ulp_ops

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


icsk_ulp_data

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


u8:5

</td>
<td>


icsk_ca_state

</td>
<td>


read_write

</td>
<td>




</td>
<td>


tcp_cwnd_application_limited,tcp_set_ca_state,tcp_enter_cwr,tcp_tso_should_defer,tcp_mtu_probe,tcp_schedule_loss_probe,tcp_write_xmit,\__tcp_transmit_skb

</td>
</tr>
<tr>
<td>


u8:1

</td>
<td>


icsk_ca_initialized

</td>
<td>


read_write

</td>
<td>




</td>
<td>


tcp_init_transfer,tcp_init_congestion_control,tcp_init_transfer,tcp_finish_connect,tcp_connect

</td>
</tr>
<tr>
<td>


u8:1

</td>
<td>


icsk_ca_setsockopt

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


icsk_ca_dst_locked

</td>
<td>


write_mostly

</td>
<td>




</td>
<td>


tcp_ca_dst_init,tcp_connect_init,tcp_connect

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


icsk_retransmits

</td>
<td>


write_mostly

</td>
<td>




</td>
<td>


tcp_connect_init,tcp_connect

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


icsk_pending

</td>
<td>


read_write

</td>
<td>




</td>
<td>


inet_csk_reset_xmit_timer,tcp_connect,tcp_check_probe_timer,\__tcp_push_pending_frames,tcp_rearm_rto,tcp_event_new_data_sent,tcp_event_new_data_sent

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


icsk_backoff

</td>
<td>


write_mostly

</td>
<td>




</td>
<td>


tcp_write_queue_purge,tcp_connect_init

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


icsk_syn_retries

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


icsk_probes_out

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


icsk_ext_hdr_len

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


\__tcp_mtu_to_mss,tcp_mtu_to_rss,tcp_mtu_probe,tcp_write_xmit,tcp_mtu_to_mss,

</td>
</tr>
<tr>
<td>


struct icsk_ack_u8

</td>
<td>


pending

</td>
<td>


read_write

</td>
<td>


read_write

</td>
<td>


inet_csk_ack_scheduled,\__tcp_cleanup_rbuf,tcp_cleanup_rbuf,inet_csk_clear_xmit_timer,tcp_event_ack-sent,inet_csk_reset_xmit_timer

</td>
</tr>
<tr>
<td>


struct icsk_ack_u8

</td>
<td>


quick

</td>
<td>


read_write

</td>
<td>


write_mostly

</td>
<td>


tcp_dec_quickack_mode,tcp_event_ack_sent,\__tcp_transmit_skb,\__tcp_select_window,\__tcp_cleanup_rbuf

</td>
</tr>
<tr>
<td>


struct icsk_ack_u8

</td>
<td>


pingpong

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


struct icsk_ack_u8

</td>
<td>


retry

</td>
<td>


write_mostly

</td>
<td>


read_write

</td>
<td>


inet_csk_clear_xmit_timer,tcp_rearm_rto,tcp_event_new_data_sent,tcp_write_xmit,\__tcp_send_ack,tcp_send_ack,

</td>
</tr>
<tr>
<td>


struct icsk_ack_u8

</td>
<td>


ato

</td>
<td>


read_mostly

</td>
<td>


write_mostly

</td>
<td>


tcp_dec_quickack_mode,tcp_event_ack_sent,\__tcp_transmit_skb,\__tcp_send_ack,tcp_send_ack

</td>
</tr>
<tr>
<td>


struct icsk_ack_u32

</td>
<td>


lrcvtime

</td>
<td>


read_write

</td>
<td>




</td>
<td>


tcp_finish_connect,tcp_connect,tcp_event_data_sent,\__tcp_transmit_skb

</td>
</tr>
<tr>
<td>


struct icsk_ack_u16

</td>
<td>


rcv_mss

</td>
<td>


write_mostly

</td>
<td>


read_mostly

</td>
<td>


\__tcp_select_window,\__tcp_cleanup_rbuf,tcp_initialize_rcv_mss,tcp_connect_init

</td>
</tr>
<tr>
<td>


struct icsk_mtup_int

</td>
<td>


search_high

</td>
<td>


read_write

</td>
<td>




</td>
<td>


tcp_mtup_init,tcp_sync_mss,tcp_connect_init,tcp_mtu_check_reprobe,tcp_write_xmit

</td>
</tr>
<tr>
<td>


struct icsk_mtup_int

</td>
<td>


search_low

</td>
<td>


read_write

</td>
<td>




</td>
<td>


tcp_mtu_probe,tcp_mtu_check_reprobe,tcp_write_xmit,tcp_sync_mss,tcp_connect_init,tcp_mtup_init

</td>
</tr>
<tr>
<td>


struct icsk_mtup_u32:31

</td>
<td>


probe_size

</td>
<td>


read_write

</td>
<td>




</td>
<td>


tcp_mtup_init,tcp_connect_init,\__tcp_transmit_skb

</td>
</tr>
<tr>
<td>


struct icsk_mtup_u32:1

</td>
<td>


enabled

</td>
<td>


read_write

</td>
<td>




</td>
<td>


tcp_mtup_init,tcp_sync_mss,tcp_connect_init,tcp_mtu_probe,tcp_write_xmit

</td>
</tr>
<tr>
<td>


struct icsk_mtup_u32

</td>
<td>


probe_timestamp

</td>
<td>


read_write

</td>
<td>




</td>
<td>


tcp_mtup_init,tcp_connect_init,tcp_mtu_check_reprobe,tcp_mtu_probe

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


icsk_probes_tstamp

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


icsk_user_timeout

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


u64\[104/sizeof(u64)\]

</td>
<td>


icsk_ca_priv

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
