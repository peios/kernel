---
title: "netns_ipv4 struct fast path usage breakdown"
type: reference
description: "Reference for netns_ipv4 struct fast path usage breakdown."
---

<a id="rst-netns-ipv4-struct-fast-path-usage-breakdown"></a>

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


struct_inet_timewait_death_row

</td>
<td>


tcp_death_row

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


struct_udp_table\*

</td>
<td>


udp_table

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


struct_ctl_table_header\*

</td>
<td>


forw_hdr

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


struct_ctl_table_header\*

</td>
<td>


frags_hdr

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


struct_ctl_table_header\*

</td>
<td>


ipv4_hdr

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


struct_ctl_table_header\*

</td>
<td>


route_hdr

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


struct_ctl_table_header\*

</td>
<td>


xfrm4_hdr

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


struct_ipv4_devconf\*

</td>
<td>


devconf_all

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


struct_ipv4_devconf\*

</td>
<td>


devconf_dflt

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


struct_ip_ra_chain

</td>
<td>


ra_chain

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


struct_mutex

</td>
<td>


ra_mutex

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


struct_fib_rules_ops\*

</td>
<td>


rules_ops

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


struct_fib_table

</td>
<td>


fib_main

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


struct_fib_table

</td>
<td>


fib_default

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


fib_rules_require_fldissect

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


fib_has_custom_rules

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


fib_has_custom_local_routes

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


fib_offload_disabled

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


fib_num_tclassid_users

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


struct_hlist_head\*

</td>
<td>


fib_table_hash

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


struct_sock\*

</td>
<td>


fibnl

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


struct_sock\*

</td>
<td>


mc_autojoin_sk

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


struct_inet_peer_base\*

</td>
<td>


peers

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


struct_fqdir\*

</td>
<td>


fqdir

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


sysctl_icmp_echo_ignore_all

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


sysctl_icmp_echo_enable_probe

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


sysctl_icmp_echo_ignore_broadcasts

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


sysctl_icmp_ignore_bogus_error_responses

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


sysctl_icmp_errors_use_inbound_ifaddr

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


sysctl_icmp_ratelimit

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


sysctl_icmp_ratemask

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


ip_rt_min_pmtu

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


ip_rt_mtu_expires

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


ip_rt_min_advmss

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


struct_local_ports

</td>
<td>


ip_local_ports

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


sysctl_tcp_ecn

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


sysctl_tcp_ecn_fallback

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


sysctl_ip_default_ttl

</td>
<td>




</td>
<td>




</td>
<td>


ip4_dst_hoplimit/ip_select_ttl

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


sysctl_ip_no_pmtu_disc

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


sysctl_ip_fwd_use_pmtu

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


ip_dst_mtu_maybe_forward/ip_skb_dst_mtu

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


sysctl_ip_fwd_update_priority

</td>
<td>




</td>
<td>




</td>
<td>


ip_forward

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


sysctl_ip_nonlocal_bind

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


sysctl_ip_autobind_reuse

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


sysctl_ip_dynaddr

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


sysctl_ip_early_demux

</td>
<td>




</td>
<td>


read_mostly

</td>
<td>


ip(6)\_rcv_finish_core

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


sysctl_raw_l3mdev_accept

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


sysctl_tcp_early_demux

</td>
<td>




</td>
<td>


read_mostly

</td>
<td>


ip(6)\_rcv_finish_core

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


sysctl_udp_early_demux

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


sysctl_nexthop_compat_mode

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


sysctl_fwmark_reflect

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


sysctl_tcp_fwmark_accept

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


sysctl_tcp_l3mdev_accept

</td>
<td>




</td>
<td>


read_mostly

</td>
<td>


\__inet6_lookup_established/inet_request_bound_dev_if

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


sysctl_tcp_mtu_probing

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


sysctl_tcp_mtu_probe_floor

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


sysctl_tcp_base_mss

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


sysctl_tcp_min_snd_mss

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


\__tcp_mtu_to_mss(tcp_write_xmit)

</td>
</tr>
<tr>
<td>


int

</td>
<td>


sysctl_tcp_probe_threshold

</td>
<td>




</td>
<td>




</td>
<td>


tcp_mtu_probe(tcp_write_xmit)

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


sysctl_tcp_probe_interval

</td>
<td>




</td>
<td>




</td>
<td>


tcp_mtu_check_reprobe(tcp_write_xmit)

</td>
</tr>
<tr>
<td>


int

</td>
<td>


sysctl_tcp_keepalive_time

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


sysctl_tcp_keepalive_intvl

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


sysctl_tcp_keepalive_probes

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


sysctl_tcp_syn_retries

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


sysctl_tcp_synack_retries

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


sysctl_tcp_syncookies

</td>
<td>




</td>
<td>




</td>
<td>


generated_on_syn

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


sysctl_tcp_migrate_req

</td>
<td>




</td>
<td>




</td>
<td>


reuseport

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


sysctl_tcp_comp_sack_nr

</td>
<td>




</td>
<td>




</td>
<td>


\__tcp_ack_snd_check

</td>
</tr>
<tr>
<td>


int

</td>
<td>


sysctl_tcp_reordering

</td>
<td>




</td>
<td>


read_mostly

</td>
<td>


tcp_may_raise_cwnd/tcp_cong_control

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


sysctl_tcp_retries1

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


sysctl_tcp_retries2

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


sysctl_tcp_orphan_retries

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


sysctl_tcp_tw_reuse

</td>
<td>




</td>
<td>




</td>
<td>


timewait_sock_ops

</td>
</tr>
<tr>
<td>


unsigned_int

</td>
<td>


sysctl_tcp_tw_reuse_delay

</td>
<td>




</td>
<td>




</td>
<td>


timewait_sock_ops

</td>
</tr>
<tr>
<td>


int

</td>
<td>


sysctl_tcp_fin_timeout

</td>
<td>




</td>
<td>




</td>
<td>


TCP_LAST_ACK/tcp_rcv_state_process

</td>
</tr>
<tr>
<td>


unsigned_int

</td>
<td>


sysctl_tcp_notsent_lowat

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


tcp_notsent_lowat/tcp_stream_memory_free

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


sysctl_tcp_sack

</td>
<td>




</td>
<td>




</td>
<td>


tcp_syn_options

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


sysctl_tcp_window_scaling

</td>
<td>




</td>
<td>




</td>
<td>


tcp_syn_options,tcp_parse_options

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


sysctl_tcp_timestamps

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


sysctl_tcp_early_retrans

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


tcp_schedule_loss_probe(tcp_write_xmit)

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


sysctl_tcp_rto_max_ms

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


sysctl_tcp_recovery

</td>
<td>




</td>
<td>




</td>
<td>


tcp_fastretrans_alert

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


sysctl_tcp_thin_linear_timeouts

</td>
<td>




</td>
<td>




</td>
<td>


tcp_retrans_timer(on_thin_streams)

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


sysctl_tcp_slow_start_after_idle

</td>
<td>




</td>
<td>




</td>
<td>


unlikely(tcp_cwnd_validate-network-not-starved)

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


sysctl_tcp_retrans_collapse

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


sysctl_tcp_stdurg

</td>
<td>




</td>
<td>




</td>
<td>


unlikely(tcp_check_urg)

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


sysctl_tcp_rfc1337

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


sysctl_tcp_abort_on_overflow

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


sysctl_tcp_fack

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


sysctl_tcp_max_reordering

</td>
<td>




</td>
<td>




</td>
<td>


tcp_check_sack_reordering

</td>
</tr>
<tr>
<td>


int

</td>
<td>


sysctl_tcp_adv_win_scale

</td>
<td>




</td>
<td>




</td>
<td>


tcp_init_buffer_space

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


sysctl_tcp_dsack

</td>
<td>




</td>
<td>




</td>
<td>


partial_packet_or_retrans_in_tcp_data_queue

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


sysctl_tcp_app_win

</td>
<td>




</td>
<td>




</td>
<td>


tcp_win_from_space

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


sysctl_tcp_frto

</td>
<td>




</td>
<td>




</td>
<td>


tcp_enter_loss

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


sysctl_tcp_nometrics_save

</td>
<td>




</td>
<td>




</td>
<td>


TCP_LAST_ACK/tcp_update_metrics

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


sysctl_tcp_no_ssthresh_metrics_save

</td>
<td>




</td>
<td>




</td>
<td>


TCP_LAST_ACK/tcp\_(update/init)\_metrics

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


sysctl_tcp_moderate_rcvbuf

</td>
<td>




</td>
<td>


read_mostly

</td>
<td>


tcp_rcvbuf_grow()

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


sysctl_tcp_rcvbuf_low_rtt

</td>
<td>




</td>
<td>


read_mostly

</td>
<td>


tcp_rcvbuf_grow()

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


sysctl_tcp_tso_win_divisor

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


tcp_tso_should_defer(tcp_write_xmit)

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


sysctl_tcp_workaround_signed_windows

</td>
<td>




</td>
<td>




</td>
<td>


tcp_select_window

</td>
</tr>
<tr>
<td>


int

</td>
<td>


sysctl_tcp_limit_output_bytes

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


tcp_small_queue_check(tcp_write_xmit)

</td>
</tr>
<tr>
<td>


int

</td>
<td>


sysctl_tcp_challenge_ack_limit

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


sysctl_tcp_min_rtt_wlen

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


tcp_ack_update_rtt

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


sysctl_tcp_min_tso_segs

</td>
<td>




</td>
<td>




</td>
<td>


unlikely(icsk_ca_ops-written)

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


sysctl_tcp_tso_rtt_log

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


tcp_tso_autosize

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


sysctl_tcp_autocorking

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


tcp_push/tcp_should_autocork

</td>
</tr>
<tr>
<td>


u8

</td>
<td>


sysctl_tcp_reflect_tos

</td>
<td>




</td>
<td>




</td>
<td>


tcp_v(4/6)\_send_synack

</td>
</tr>
<tr>
<td>


int

</td>
<td>


sysctl_tcp_invalid_ratelimit

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


sysctl_tcp_pacing_ss_ratio

</td>
<td>




</td>
<td>




</td>
<td>


default_cong_cont(tcp_update_pacing_rate)

</td>
</tr>
<tr>
<td>


int

</td>
<td>


sysctl_tcp_pacing_ca_ratio

</td>
<td>




</td>
<td>




</td>
<td>


default_cong_cont(tcp_update_pacing_rate)

</td>
</tr>
<tr>
<td>


int

</td>
<td>


sysctl_tcp_wmem\[3\]

</td>
<td>


read_mostly

</td>
<td>




</td>
<td>


tcp_wmem_schedule(sendmsg/sendpage)

</td>
</tr>
<tr>
<td>


int

</td>
<td>


sysctl_tcp_rmem\[3\]

</td>
<td>




</td>
<td>


read_mostly

</td>
<td>


\__tcp_grow_window(tx),tcp_rcv_space_adjust(rx)

</td>
</tr>
<tr>
<td>


unsigned_int

</td>
<td>


sysctl_tcp_child_ehash_entries

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


sysctl_tcp_comp_sack_delay_ns

</td>
<td>




</td>
<td>




</td>
<td>


\__tcp_ack_snd_check

</td>
</tr>
<tr>
<td>


unsigned_long

</td>
<td>


sysctl_tcp_comp_sack_slack_ns

</td>
<td>




</td>
<td>




</td>
<td>


\__tcp_ack_snd_check

</td>
</tr>
<tr>
<td>


int

</td>
<td>


sysctl_max_syn_backlog

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


sysctl_tcp_fastopen

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


struct_tcp_congestion_ops

</td>
<td>


tcp_congestion_control

</td>
<td>




</td>
<td>




</td>
<td>


init_cc

</td>
</tr>
<tr>
<td>


struct_tcp_fastopen_context

</td>
<td>


tcp_fastopen_ctx

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


sysctl_tcp_fastopen_blackhole_timeout

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


tfo_active_disable_times

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


tfo_active_disable_stamp

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


tcp_challenge_timestamp

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


tcp_challenge_count

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


sysctl_tcp_plb_enabled

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


sysctl_tcp_plb_idle_rehash_rounds

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


sysctl_tcp_plb_rehash_rounds

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


sysctl_tcp_plb_suspend_rto_sec

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


sysctl_tcp_plb_cong_thresh

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


sysctl_udp_wmem_min

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


sysctl_udp_rmem_min

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


sysctl_fib_notify_on_flag_change

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


sysctl_udp_l3mdev_accept

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


sysctl_igmp_llm_reports

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


sysctl_igmp_max_memberships

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


sysctl_igmp_max_msf

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


sysctl_igmp_qrv

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


struct_ping_group_range

</td>
<td>


ping_group_range

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


dev_addr_genid

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


sysctl_udp_child_hash_entries

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


unsigned_long\*

</td>
<td>


sysctl_local_reserved_ports

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


sysctl_ip_prot_sock

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


struct_mr_table\*

</td>
<td>


mrt

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


struct_list_head

</td>
<td>


mr_tables

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


struct_fib_rules_ops\*

</td>
<td>


mr_rules_ops

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


sysctl_fib_multipath_hash_fields

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


sysctl_fib_multipath_use_neigh

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


sysctl_fib_multipath_hash_policy

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


struct_fib_notifier_ops\*

</td>
<td>


notifier_ops

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


fib_seq

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


struct_fib_notifier_ops\*

</td>
<td>


ipmr_notifier_ops

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


ipmr_seq

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


rt_genid

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


siphash_key_t

</td>
<td>


ip_id_key

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
