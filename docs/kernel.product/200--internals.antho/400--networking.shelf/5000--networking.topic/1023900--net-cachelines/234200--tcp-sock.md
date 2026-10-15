---
title: "tcp_sock struct fast path usage breakdown"
type: reference
description: "Reference for tcp_sock struct fast path usage breakdown."
---

<a id="rst-tcp-sock-struct-fast-path-usage-breakdown"></a>

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


struct inet_connection_sock

</td>
<td>


inet_conn

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


tcp_header_len

</td>
<td>


read_mostly

</td>
<td>


read_mostly

</td>
<td>


tcp_bound_to_half_wnd,tcp_current_mss(tx);tcp_rcv_established(rx)

</td>
</tr>
<tr>
<td>


u16

</td>
<td>


gso_segs

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


tcp_xmit_size_goal

</td>
</tr>
<tr>
<td>


\__be32

</td>
<td>


pred_flags

</td>
<td>


read_write

</td>
<td>


read_mostly

</td>
<td>


tcp_select_window(tx);tcp_rcv_established(rx)

</td>
</tr>
<tr>
<td>


u64

</td>
<td>


bytes_received

</td>
<td>




</td>
<td>


read_write

</td>
<td>


tcp_rcv_nxt_update(rx)

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


segs_in

</td>
<td>




</td>
<td>


read_write

</td>
<td>


tcp_v6_rcv(rx)

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


data_segs_in

</td>
<td>




</td>
<td>


read_write

</td>
<td>


tcp_v6_rcv(rx)

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


rcv_nxt

</td>
<td>


read_mostly

</td>
<td>


read_write

</td>
<td>


tcp_cleanup_rbuf,tcp_send_ack,tcp_inq_hint,tcp_transmit_skb,tcp_receive_window(tx);tcp_v6_do_rcv,tcp_rcv_established,tcp_data_queue,tcp_receive_window,tcp_rcv_nxt_update(write)(rx)

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


copied_seq

</td>
<td>




</td>
<td>


read_mostly

</td>
<td>


tcp_cleanup_rbuf,tcp_rcv_space_adjust,tcp_inq_hint

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


rcv_wup

</td>
<td>




</td>
<td>


read_write

</td>
<td>


\__tcp_cleanup_rbuf,tcp_receive_window,tcp_receive_established

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


snd_nxt

</td>
<td>


read_write

</td>
<td>


read_mostly

</td>
<td>


tcp_rate_check_app_limited,\__tcp_transmit_skb,tcp_event_new_data_sent(write)(tx);tcp_rcv_established,tcp_ack,tcp_clean_rtx_queue(rx)

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


segs_out

</td>
<td>


read_write

</td>
<td>




</td>
<td>


\__tcp_transmit_skb

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


data_segs_out

</td>
<td>


read_write

</td>
<td>




</td>
<td>


\__tcp_transmit_skb,tcp_update_skb_after_send

</td>
</tr>
<tr>
<td>


u64

</td>
<td>


bytes_sent

</td>
<td>


read_write

</td>
<td>




</td>
<td>


\__tcp_transmit_skb

</td>
</tr>
<tr>
<td>


u64

</td>
<td>


bytes_acked

</td>
<td>




</td>
<td>


read_write

</td>
<td>


tcp_snd_una_update/tcp_ack

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


dsack_dups

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


snd_una

</td>
<td>


read_mostly

</td>
<td>


read_write

</td>
<td>


tcp_wnd_end,tcp_urg_mode,tcp_minshall_check,tcp_cwnd_validate(tx);tcp_ack,tcp_may_update_window,tcp_clean_rtx_queue(write),tcp_ack_tstamp(rx)

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


snd_sml

</td>
<td>


read_write

</td>
<td>




</td>
<td>


tcp_minshall_check,tcp_minshall_update

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


rcv_tstamp

</td>
<td>


read_write

</td>
<td>


read_write

</td>
<td>


tcp_ack

</td>
</tr>
<tr>
<td>


void \*

</td>
<td>


tcp_clean_acked

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


tcp_ack

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


lsndtime

</td>
<td>


read_write

</td>
<td>




</td>
<td>


tcp_slow_start_after_idle_check,tcp_event_data_sent

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


last_oow_ack_time

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


compressed_ack_rcv_nxt

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


tsoffset

</td>
<td>


read_mostly

</td>
<td>


read_mostly

</td>
<td>


tcp_established_options(tx);tcp_fast_parse_options(rx)

</td>
</tr>
<tr>
<td>


struct list_head

</td>
<td>


tsq_node

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


tsorted_sent_queue

</td>
<td>


read_write

</td>
<td>




</td>
<td>


tcp_update_skb_after_send

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


snd_wl1

</td>
<td>




</td>
<td>


read_mostly

</td>
<td>


tcp_may_update_window

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


snd_wnd

</td>
<td>


read_mostly

</td>
<td>


read_mostly

</td>
<td>


tcp_wnd_end,tcp_tso_should_defer(tx);tcp_fast_path_on(rx)

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


max_window

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


tcp_bound_to_half_wnd,forced_push

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


mss_cache

</td>
<td>


read_mostly

</td>
<td>


read_mostly

</td>
<td>


tcp_rate_check_app_limited,tcp_current_mss,tcp_sync_mss,tcp_sndbuf_expand,tcp_tso_should_defer(tx);tcp_update_pacing_rate,tcp_clean_rtx_queue(rx)

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


window_clamp

</td>
<td>


read_mostly

</td>
<td>


read_write

</td>
<td>


tcp_rcv_space_adjust,\__tcp_select_window

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


rcv_ssthresh

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


\__tcp_select_window

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


scaling_ratio

</td>
<td>


read_mostly

</td>
<td>


read_mostly

</td>
<td>


tcp_win_from_space

</td>
</tr>
<tr>
<td>


struct

</td>
<td>


tcp_rack

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


advmss

</td>
<td>




</td>
<td>


read_mostly

</td>
<td>


tcp_rcv_space_adjust

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


compressed_ack

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


u8:2

</td>
<td>


dup_ack_counter

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


tlp_retrans

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


tcp_usec_ts

</td>
<td>


read_mostly

</td>
<td>


read_mostly

</td>
<td>




</td>
</tr>
<tr>
<td>


u32

</td>
<td>


chrono_start

</td>
<td>


read_write

</td>
<td>




</td>
<td>


tcp_chrono_start/stop(tcp_write_xmit,tcp_cwnd_validate,tcp_send_syn_data)

</td>
</tr>
<tr>
<td>


u32\[3\]

</td>
<td>


chrono_stat

</td>
<td>


read_write

</td>
<td>




</td>
<td>


tcp_chrono_start/stop(tcp_write_xmit,tcp_cwnd_validate,tcp_send_syn_data)

</td>
</tr>
<tr>
<td>


u8:2

</td>
<td>


chrono_type

</td>
<td>


read_write

</td>
<td>




</td>
<td>


tcp_chrono_start/stop(tcp_write_xmit,tcp_cwnd_validate,tcp_send_syn_data)

</td>
</tr>
<tr>
<td>


u8:1

</td>
<td>


rate_app_limited

</td>
<td>




</td>
<td>


read_write

</td>
<td>


tcp_rate_gen

</td>
</tr>
<tr>
<td>


u8:1

</td>
<td>


fastopen_connect

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


fastopen_no_cookie

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


is_sack_reneg

</td>
<td>




</td>
<td>


read_mostly

</td>
<td>


tcp_skb_entail,tcp_ack

</td>
</tr>
<tr>
<td>


u8:2

</td>
<td>


fastopen_client_fail

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


u8:4

</td>
<td>


nonagle

</td>
<td>


read_write

</td>
<td>




</td>
<td>


tcp_skb_entail,tcp_push_pending_frames

</td>
</tr>
<tr>
<td>


u8:1

</td>
<td>


thin_lto

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


recvmsg_inq

</td>
<td>




</td>
<td>


read_mostly

</td>
<td>


tcp_recvmsg

</td>
</tr>
<tr>
<td>


u8:1

</td>
<td>


repair

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


tcp_write_xmit

</td>
</tr>
<tr>
<td>


u8:1

</td>
<td>


frto

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


repair_queue

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


u8:2

</td>
<td>


save_syn

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


syn_data

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


syn_fastopen

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


syn_fastopen_exp

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


syn_fastopen_ch

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


syn_data_acked

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


is_cwnd_limited

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


tcp_cwnd_validate,tcp_is_cwnd_limited

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


tlp_high_seq

</td>
<td>




</td>
<td>


read_mostly

</td>
<td>


tcp_ack

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


tcp_tx_delay

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


tcp_wstamp_ns

</td>
<td>


read_write

</td>
<td>




</td>
<td>


tcp_pacing_check,tcp_tso_should_defer,tcp_update_skb_after_send

</td>
</tr>
<tr>
<td>


u64

</td>
<td>


tcp_clock_cache

</td>
<td>


read_write

</td>
<td>


read_write

</td>
<td>


tcp_mstamp_refresh(tcp_write_xmit/tcp_rcv_space_adjust),\__tcp_transmit_skb,tcp_tso_should_defer;timer

</td>
</tr>
<tr>
<td>


u64

</td>
<td>


tcp_mstamp

</td>
<td>


read_write

</td>
<td>


read_write

</td>
<td>


tcp_mstamp_refresh(tcp_write_xmit/tcp_rcv_space_adjust)(tx);tcp_rcv_space_adjust,tcp_rate_gen,tcp_clean_rtx_queue,tcp_ack_update_rtt/tcp_time_stamp(rx);timer

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


srtt_us

</td>
<td>


read_mostly

</td>
<td>


read_write

</td>
<td>


tcp_tso_should_defer(tx);tcp_update_pacing_rate,\__tcp_set_rto,tcp_rtt_estimator(rx)

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


mdev_us

</td>
<td>


read_write

</td>
<td>




</td>
<td>


tcp_rtt_estimator

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


mdev_max_us

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


rttvar_us

</td>
<td>




</td>
<td>


read_mostly

</td>
<td>


\__tcp_set_rto

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


rtt_seq

</td>
<td>


read_write

</td>
<td>




</td>
<td>


tcp_rtt_estimator

</td>
</tr>
<tr>
<td>


struct minmax

</td>
<td>


rtt_min

</td>
<td>




</td>
<td>


read_mostly

</td>
<td>


tcp_min_rtt/tcp_rate_gen,tcp_min_rtttcp_update_rtt_min

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


packets_out

</td>
<td>


read_write

</td>
<td>


read_write

</td>
<td>


tcp_packets_in_flight(tx/rx);tcp_slow_start_after_idle_check,tcp_nagle_check,tcp_rate_skb_sent,tcp_event_new_data_sent,tcp_cwnd_validate,tcp_write_xmit(tx);tcp_ack,tcp_clean_rtx_queue,tcp_update_pacing_rate(rx)

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


retrans_out

</td>
<td>




</td>
<td>


read_mostly

</td>
<td>


tcp_packets_in_flight,tcp_rate_check_app_limited

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


max_packets_out

</td>
<td>




</td>
<td>


read_write

</td>
<td>


tcp_cwnd_validate

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


cwnd_usage_seq

</td>
<td>




</td>
<td>


read_write

</td>
<td>


tcp_cwnd_validate

</td>
</tr>
<tr>
<td>


u16

</td>
<td>


urg_data

</td>
<td>




</td>
<td>


read_mostly

</td>
<td>


tcp_fast_path_check

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


ecn_flags

</td>
<td>


read_write

</td>
<td>




</td>
<td>


tcp_ecn_send

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


keepalive_probes

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


reordering

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


tcp_sndbuf_expand

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


reord_seen

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


snd_up

</td>
<td>


read_write

</td>
<td>


read_mostly

</td>
<td>


tcp_mark_urg,tcp_urg_mode,\__tcp_transmit_skb(tx);tcp_clean_rtx_queue(rx)

</td>
</tr>
<tr>
<td>


struct tcp_options_received

</td>
<td>


rx_opt

</td>
<td>


read_mostly

</td>
<td>


read_write

</td>
<td>


tcp_established_options(tx);tcp_fast_path_on,tcp_ack_update_window,tcp_is_sack,tcp_data_queue,tcp_rcv_established,tcp_ack_update_rtt(rx)

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


snd_ssthresh

</td>
<td>




</td>
<td>


read_mostly

</td>
<td>


tcp_update_pacing_rate

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


snd_cwnd

</td>
<td>


read_mostly

</td>
<td>


read_mostly

</td>
<td>


tcp_snd_cwnd,tcp_rate_check_app_limited,tcp_tso_should_defer(tx);tcp_update_pacing_rate

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


snd_cwnd_cnt

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


snd_cwnd_clamp

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


snd_cwnd_used

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


snd_cwnd_stamp

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


prior_cwnd

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


prr_delivered

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


prr_out

</td>
<td>


read_mostly

</td>
<td>


read_mostly

</td>
<td>


tcp_rate_skb_sent,tcp_newly_delivered(tx);tcp_ack,tcp_rate_gen,tcp_clean_rtx_queue(rx)

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


delivered

</td>
<td>


read_mostly

</td>
<td>


read_write

</td>
<td>


tcp_rate_skb_sent, tcp_newly_delivered(tx);tcp_ack, tcp_rate_gen, tcp_clean_rtx_queue (rx)

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


delivered_ce

</td>
<td>


read_mostly

</td>
<td>


read_write

</td>
<td>


tcp_rate_skb_sent(tx);tcp_rate_gen(rx)

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


received_ce

</td>
<td>


read_mostly

</td>
<td>


read_write

</td>
<td>




</td>
</tr>
<tr>
<td>


u32\[3\]

</td>
<td>


received_ecn_bytes

</td>
<td>


read_mostly

</td>
<td>


read_write

</td>
<td>




</td>
</tr>
<tr>
<td>


u8:4

</td>
<td>


received_ce_pending

</td>
<td>


read_mostly

</td>
<td>


read_write

</td>
<td>




</td>
</tr>
<tr>
<td>


u32\[3\]

</td>
<td>


delivered_ecn_bytes

</td>
<td>




</td>
<td>


read_write

</td>
<td>




</td>
</tr>
<tr>
<td>


u16

</td>
<td>


pkts_acked_ewma

</td>
<td>




</td>
<td>


read_write

</td>
<td>




</td>
</tr>
<tr>
<td>


u8:2

</td>
<td>


syn_ect_snt

</td>
<td>


write_mostly

</td>
<td>


read_write

</td>
<td>




</td>
</tr>
<tr>
<td>


u8:2

</td>
<td>


syn_ect_rcv

</td>
<td>


read_mostly

</td>
<td>


read_write

</td>
<td>




</td>
</tr>
<tr>
<td>


u8:2

</td>
<td>


accecn_minlen

</td>
<td>


write_mostly

</td>
<td>


read_write

</td>
<td>




</td>
</tr>
<tr>
<td>


u8:2

</td>
<td>


est_ecnfield

</td>
<td>




</td>
<td>


read_write

</td>
<td>




</td>
</tr>
<tr>
<td>


u8:2

</td>
<td>


accecn_opt_demand

</td>
<td>


read_mostly

</td>
<td>


read_write

</td>
<td>




</td>
</tr>
<tr>
<td>


u8:2

</td>
<td>


prev_ecnfield

</td>
<td>




</td>
<td>


read_write

</td>
<td>




</td>
</tr>
<tr>
<td>


u64

</td>
<td>


accecn_opt_tstamp

</td>
<td>


read_write

</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


u8:4

</td>
<td>


accecn_fail_mode

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


lost

</td>
<td>




</td>
<td>


read_mostly

</td>
<td>


tcp_ack

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


app_limited

</td>
<td>


read_write

</td>
<td>


read_mostly

</td>
<td>


tcp_rate_check_app_limited,tcp_rate_skb_sent(tx);tcp_rate_gen(rx)

</td>
</tr>
<tr>
<td>


u64

</td>
<td>


first_tx_mstamp

</td>
<td>


read_write

</td>
<td>




</td>
<td>


tcp_rate_skb_sent

</td>
</tr>
<tr>
<td>


u64

</td>
<td>


delivered_mstamp

</td>
<td>


read_write

</td>
<td>




</td>
<td>


tcp_rate_skb_sent

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


rate_delivered

</td>
<td>




</td>
<td>


read_mostly

</td>
<td>


tcp_rate_gen

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


rate_interval_us

</td>
<td>




</td>
<td>


read_mostly

</td>
<td>


rate_delivered,rate_app_limited

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


rcv_wnd

</td>
<td>


read_write

</td>
<td>


read_mostly

</td>
<td>


tcp_select_window,tcp_receive_window,tcp_fast_path_check

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


write_seq

</td>
<td>


read_write

</td>
<td>




</td>
<td>


tcp_rate_check_app_limited,tcp_write_queue_empty,tcp_skb_entail,forced_push,tcp_mark_push

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


notsent_lowat

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


tcp_stream_memory_free

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


pushed_seq

</td>
<td>


read_write

</td>
<td>




</td>
<td>


tcp_mark_push,forced_push

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


lost_out

</td>
<td>


read_mostly

</td>
<td>


read_mostly

</td>
<td>


tcp_left_out(tx);tcp_packets_in_flight(tx/rx);tcp_rate_check_app_limited(rx)

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


sacked_out

</td>
<td>


read_mostly

</td>
<td>


read_mostly

</td>
<td>


tcp_left_out(tx);tcp_packets_in_flight(tx/rx);tcp_clean_rtx_queue(rx)

</td>
</tr>
<tr>
<td>


struct hrtimer

</td>
<td>


pacing_timer

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


struct hrtimer

</td>
<td>


compressed_ack_timer

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


struct sk_buff\*

</td>
<td>


retransmit_skb_hint

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


tcp_clean_rtx_queue

</td>
</tr>
<tr>
<td>


struct rb_root

</td>
<td>


out_of_order_queue

</td>
<td>




</td>
<td>


read_mostly

</td>
<td>


tcp_data_queue,tcp_fast_path_check

</td>
</tr>
<tr>
<td>


struct sk_buff\*

</td>
<td>


ooo_last_skb

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


struct tcp_sack_block\[1\]

</td>
<td>


duplicate_sack

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


struct tcp_sack_block\[4\]

</td>
<td>


selective_acks

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


struct tcp_sack_block\[4\]

</td>
<td>


recv_sack_cache

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


struct sk_buff\*

</td>
<td>


highest_sack

</td>
<td>


read_write

</td>
<td>




</td>
<td>


tcp_event_new_data_sent

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


prior_ssthresh

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


high_seq

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


retrans_stamp

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


undo_marker

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


undo_retrans

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


bytes_retrans

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


total_retrans

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


rto_stamp

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


total_rto

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


total_rto_recoveries

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


total_rto_time

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


urg_seq

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


keepalive_time

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


keepalive_intvl

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


linger2

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


bpf_sock_ops_cb_flags

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


bpf_chg_cc_inprogress

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


timeout_rehash

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


rcv_ooopack

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


rcv_rtt_last_tsecr

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


struct

</td>
<td>


rcv_rtt_est

</td>
<td>




</td>
<td>


read_write

</td>
<td>


tcp_rcv_space_adjust,tcp_rcv_established

</td>
</tr>
<tr>
<td>


struct

</td>
<td>


rcvq_space

</td>
<td>




</td>
<td>


read_write

</td>
<td>


tcp_rcv_space_adjust

</td>
</tr>
<tr>
<td>


struct

</td>
<td>


mtu_probe

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


plb_rehash

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


mtu_info

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


is_mptcp

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


smc_hs_congested

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


syn_smc

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


struct tcp_sock_af_ops\*

</td>
<td>


af_specific

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


struct tcp_md5sig_info\*

</td>
<td>


md5sig_info

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


struct tcp_fastopen_request\*

</td>
<td>


fastopen_req

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


struct request_sock\*

</td>
<td>


fastopen_rsk

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


struct saved_syn\*

</td>
<td>


saved_syn

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
