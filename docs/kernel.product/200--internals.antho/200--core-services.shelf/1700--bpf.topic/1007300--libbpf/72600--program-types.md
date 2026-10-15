---
title: "Program Types and ELF Sections"
type: reference
description: "The table below lists the program types, their attach types where relevant and the ELF section names supported by libbpf for them. The ELF section names follow these rules:"
---

<a id="rst-program-types-and-elf-sections"></a>
<a id="rst-program-types-and-elf"></a>

<!-- SPDX-License-Identifier: (LGPL-2.1 OR BSD-2-Clause) -->

The table below lists the program types, their attach types where relevant and the ELF section names supported by libbpf for them. The ELF section names follow these rules:

- `type` is an exact match, e.g. `SEC("socket")`

- `type+` means it can be either exact `SEC("type")` or well-formed `SEC("type/extras")` with a '`/`' separator between `type` and `extras`.

When `extras` are specified, they provide details of how to auto-attach the BPF program.  The format of `extras` depends on the program type, e.g. `SEC("tracepoint/<category>/<name>")` for tracepoints or `SEC("usdt/<path>:<provider>:<name>")` for USDT probes. The extras are described in more detail in the footnotes.


<table>
<thead>
<tr>
<th>


Program Type

</th>
<th>


Attach Type

</th>
<th>


ELF Section Name

</th>
<th>


Sleepable

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


`BPF_PROG_TYPE_CGROUP_DEVICE`

</td>
<td>


`BPF_CGROUP_DEVICE`

</td>
<td>


`cgroup/dev`

</td>
<td>




</td>
</tr>
<tr>
<td rowspan="3">


`BPF_PROG_TYPE_CGROUP_SKB`

</td>
<td>




</td>
<td>


`cgroup/skb`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_CGROUP_INET_EGRESS`

</td>
<td>


`cgroup_skb/egress`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_CGROUP_INET_INGRESS`

</td>
<td>


`cgroup_skb/ingress`

</td>
<td>




</td>
</tr>
<tr>
<td rowspan="2">


`BPF_PROG_TYPE_CGROUP_SOCKOPT`

</td>
<td>


`BPF_CGROUP_GETSOCKOPT`

</td>
<td>


`cgroup/getsockopt`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_CGROUP_SETSOCKOPT`

</td>
<td>


`cgroup/setsockopt`

</td>
<td>




</td>
</tr>
<tr>
<td rowspan="17">


`BPF_PROG_TYPE_CGROUP_SOCK_ADDR`

</td>
<td>


`BPF_CGROUP_INET4_BIND`

</td>
<td>


`cgroup/bind4`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_CGROUP_INET4_CONNECT`

</td>
<td>


`cgroup/connect4`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_CGROUP_INET4_GETPEERNAME`

</td>
<td>


`cgroup/getpeername4`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_CGROUP_INET4_GETSOCKNAME`

</td>
<td>


`cgroup/getsockname4`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_CGROUP_INET6_BIND`

</td>
<td>


`cgroup/bind6`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_CGROUP_INET6_CONNECT`

</td>
<td>


`cgroup/connect6`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_CGROUP_INET6_GETPEERNAME`

</td>
<td>


`cgroup/getpeername6`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_CGROUP_INET6_GETSOCKNAME`

</td>
<td>


`cgroup/getsockname6`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_CGROUP_UDP4_RECVMSG`

</td>
<td>


`cgroup/recvmsg4`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_CGROUP_UDP4_SENDMSG`

</td>
<td>


`cgroup/sendmsg4`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_CGROUP_UDP6_RECVMSG`

</td>
<td>


`cgroup/recvmsg6`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_CGROUP_UDP6_SENDMSG`

</td>
<td>


`cgroup/sendmsg6`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_CGROUP_UNIX_CONNECT`

</td>
<td>


`cgroup/connect_unix`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_CGROUP_UNIX_SENDMSG`

</td>
<td>


`cgroup/sendmsg_unix`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_CGROUP_UNIX_RECVMSG`

</td>
<td>


`cgroup/recvmsg_unix`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_CGROUP_UNIX_GETPEERNAME`

</td>
<td>


`cgroup/getpeername_unix`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_CGROUP_UNIX_GETSOCKNAME`

</td>
<td>


`cgroup/getsockname_unix`

</td>
<td>




</td>
</tr>
<tr>
<td rowspan="5">


`BPF_PROG_TYPE_CGROUP_SOCK`

</td>
<td>


`BPF_CGROUP_INET4_POST_BIND`

</td>
<td>


`cgroup/post_bind4`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_CGROUP_INET6_POST_BIND`

</td>
<td>


`cgroup/post_bind6`

</td>
<td>




</td>
</tr>
<tr>
<td rowspan="2">


`BPF_CGROUP_INET_SOCK_CREATE`

</td>
<td>


`cgroup/sock_create`

</td>
<td>




</td>
</tr>
<tr>
<td>


`cgroup/sock`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_CGROUP_INET_SOCK_RELEASE`

</td>
<td>


`cgroup/sock_release`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_PROG_TYPE_CGROUP_SYSCTL`

</td>
<td>


`BPF_CGROUP_SYSCTL`

</td>
<td>


`cgroup/sysctl`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_PROG_TYPE_EXT`

</td>
<td>




</td>
<td>


`freplace+` <a id="rst-footnote-reference-1"></a>[1](#rst-fentry)

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_PROG_TYPE_FLOW_DISSECTOR`

</td>
<td>


`BPF_FLOW_DISSECTOR`

</td>
<td>


`flow_dissector`

</td>
<td>




</td>
</tr>
<tr>
<td rowspan="19">


`BPF_PROG_TYPE_KPROBE`

</td>
<td rowspan="10">




</td>
<td>


`kprobe+` <a id="rst-footnote-reference-2"></a>[2](#rst-kprobe)

</td>
<td>




</td>
</tr>
<tr>
<td>


`kretprobe+` <a id="rst-footnote-reference-3"></a>[2](#rst-kprobe)

</td>
<td>




</td>
</tr>
<tr>
<td>


`ksyscall+` <a id="rst-footnote-reference-4"></a>[3](#rst-ksyscall)

</td>
<td>




</td>
</tr>
<tr>
<td>


`kretsyscall+` <a id="rst-footnote-reference-5"></a>[3](#rst-ksyscall)

</td>
<td>




</td>
</tr>
<tr>
<td>


`uprobe+` <a id="rst-footnote-reference-6"></a>[4](#rst-uprobe)

</td>
<td>




</td>
</tr>
<tr>
<td>


`uprobe.s+` <a id="rst-footnote-reference-7"></a>[4](#rst-uprobe)

</td>
<td>


Yes

</td>
</tr>
<tr>
<td>


`uretprobe+` <a id="rst-footnote-reference-8"></a>[4](#rst-uprobe)

</td>
<td>




</td>
</tr>
<tr>
<td>


`uretprobe.s+` <a id="rst-footnote-reference-9"></a>[4](#rst-uprobe)

</td>
<td>


Yes

</td>
</tr>
<tr>
<td>


`usdt+` <a id="rst-footnote-reference-10"></a>[6](#rst-usdt)

</td>
<td>




</td>
</tr>
<tr>
<td>


`usdt.s+` <a id="rst-footnote-reference-11"></a>[6](#rst-usdt)

</td>
<td>


Yes

</td>
</tr>
<tr>
<td rowspan="2">


`BPF_TRACE_KPROBE_MULTI`

</td>
<td>


`kprobe.multi+` <a id="rst-footnote-reference-12"></a>[7](#rst-kpmulti)

</td>
<td>




</td>
</tr>
<tr>
<td>


`kretprobe.multi+` <a id="rst-footnote-reference-13"></a>[7](#rst-kpmulti)

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_TRACE_KPROBE_SESSION`

</td>
<td>


`kprobe.session+` <a id="rst-footnote-reference-14"></a>[7](#rst-kpmulti)

</td>
<td>




</td>
</tr>
<tr>
<td rowspan="4">


`BPF_TRACE_UPROBE_MULTI`

</td>
<td>


`uprobe.multi+` <a id="rst-footnote-reference-15"></a>[5](#rst-upmul)

</td>
<td>




</td>
</tr>
<tr>
<td>


`uprobe.multi.s+` <a id="rst-footnote-reference-16"></a>[5](#rst-upmul)

</td>
<td>


Yes

</td>
</tr>
<tr>
<td>


`uretprobe.multi+` <a id="rst-footnote-reference-17"></a>[5](#rst-upmul)

</td>
<td>




</td>
</tr>
<tr>
<td>


`uretprobe.multi.s+` <a id="rst-footnote-reference-18"></a>[5](#rst-upmul)

</td>
<td>


Yes

</td>
</tr>
<tr>
<td rowspan="2">


`BPF_TRACE_UPROBE_SESSION`

</td>
<td>


`uprobe.session+` <a id="rst-footnote-reference-19"></a>[5](#rst-upmul)

</td>
<td>




</td>
</tr>
<tr>
<td>


`uprobe.session.s+` <a id="rst-footnote-reference-20"></a>[5](#rst-upmul)

</td>
<td>


Yes

</td>
</tr>
<tr>
<td>


`BPF_PROG_TYPE_LIRC_MODE2`

</td>
<td>


`BPF_LIRC_MODE2`

</td>
<td>


`lirc_mode2`

</td>
<td>




</td>
</tr>
<tr>
<td rowspan="3">


`BPF_PROG_TYPE_LSM`

</td>
<td>


`BPF_LSM_CGROUP`

</td>
<td>


`lsm_cgroup+`

</td>
<td>




</td>
</tr>
<tr>
<td rowspan="2">


`BPF_LSM_MAC`

</td>
<td>


`lsm+` <a id="rst-footnote-reference-21"></a>[8](#rst-lsm)

</td>
<td>




</td>
</tr>
<tr>
<td>


`lsm.s+` <a id="rst-footnote-reference-22"></a>[8](#rst-lsm)

</td>
<td>


Yes

</td>
</tr>
<tr>
<td>


`BPF_PROG_TYPE_LWT_IN`

</td>
<td>




</td>
<td>


`lwt_in`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_PROG_TYPE_LWT_OUT`

</td>
<td>




</td>
<td>


`lwt_out`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_PROG_TYPE_LWT_SEG6LOCAL`

</td>
<td>




</td>
<td>


`lwt_seg6local`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_PROG_TYPE_LWT_XMIT`

</td>
<td>




</td>
<td>


`lwt_xmit`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_PROG_TYPE_NETFILTER`

</td>
<td>




</td>
<td>


`netfilter`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_PROG_TYPE_PERF_EVENT`

</td>
<td>




</td>
<td>


`perf_event`

</td>
<td>




</td>
</tr>
<tr>
<td rowspan="2">


`BPF_PROG_TYPE_RAW_TRACEPOINT_WRITABLE`

</td>
<td rowspan="2">




</td>
<td>


`raw_tp.w+` <a id="rst-footnote-reference-23"></a>[9](#rst-rawtp)

</td>
<td>




</td>
</tr>
<tr>
<td>


`raw_tracepoint.w+`

</td>
<td>




</td>
</tr>
<tr>
<td rowspan="2">


`BPF_PROG_TYPE_RAW_TRACEPOINT`

</td>
<td rowspan="2">




</td>
<td>


`raw_tp+` <a id="rst-footnote-reference-24"></a>[9](#rst-rawtp)

</td>
<td>




</td>
</tr>
<tr>
<td>


`raw_tracepoint+`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_PROG_TYPE_SCHED_ACT`

</td>
<td>




</td>
<td>


`action` <a id="rst-footnote-reference-25"></a>[10](#rst-tc-legacy)

</td>
<td>




</td>
</tr>
<tr>
<td rowspan="8">


`BPF_PROG_TYPE_SCHED_CLS`

</td>
<td rowspan="2">




</td>
<td>


`classifier` <a id="rst-footnote-reference-26"></a>[10](#rst-tc-legacy)

</td>
<td>




</td>
</tr>
<tr>
<td>


`tc` <a id="rst-footnote-reference-27"></a>[10](#rst-tc-legacy)

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_NETKIT_PRIMARY`

</td>
<td>


`netkit/primary`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_NETKIT_PEER`

</td>
<td>


`netkit/peer`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_TCX_INGRESS`

</td>
<td>


`tc/ingress`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_TCX_EGRESS`

</td>
<td>


`tc/egress`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_TCX_INGRESS`

</td>
<td>


`tcx/ingress`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_TCX_EGRESS`

</td>
<td>


`tcx/egress`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_PROG_TYPE_SK_LOOKUP`

</td>
<td>


`BPF_SK_LOOKUP`

</td>
<td>


`sk_lookup`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_PROG_TYPE_SK_MSG`

</td>
<td>


`BPF_SK_MSG_VERDICT`

</td>
<td>


`sk_msg`

</td>
<td>




</td>
</tr>
<tr>
<td rowspan="2">


`BPF_PROG_TYPE_SK_REUSEPORT`

</td>
<td>


`BPF_SK_REUSEPORT_SELECT_OR_MIGRATE`

</td>
<td>


`sk_reuseport/migrate`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_SK_REUSEPORT_SELECT`

</td>
<td>


`sk_reuseport`

</td>
<td>




</td>
</tr>
<tr>
<td rowspan="3">


`BPF_PROG_TYPE_SK_SKB`

</td>
<td>




</td>
<td>


`sk_skb`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_SK_SKB_STREAM_PARSER`

</td>
<td>


`sk_skb/stream_parser`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_SK_SKB_STREAM_VERDICT`

</td>
<td>


`sk_skb/stream_verdict`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_PROG_TYPE_SOCKET_FILTER`

</td>
<td>




</td>
<td>


`socket`

</td>
<td>




</td>
</tr>
<tr>
<td>


`BPF_PROG_TYPE_SOCK_OPS`

</td>
<td>


`BPF_CGROUP_SOCK_OPS`

</td>
<td>


`sockops`

</td>
<td>




</td>
</tr>
<tr>
<td rowspan="2">


`BPF_PROG_TYPE_STRUCT_OPS`

</td>
<td rowspan="2">




</td>
<td>


`struct_ops+` <a id="rst-footnote-reference-28"></a>[11](#rst-struct-ops)

</td>
<td>




</td>
</tr>
<tr>
<td>


`struct_ops.s+` <a id="rst-footnote-reference-29"></a>[11](#rst-struct-ops)

</td>
<td>


Yes

</td>
</tr>
<tr>
<td>


`BPF_PROG_TYPE_SYSCALL`

</td>
<td>




</td>
<td>


`syscall`

</td>
<td>


Yes

</td>
</tr>
<tr>
<td rowspan="2">


`BPF_PROG_TYPE_TRACEPOINT`

</td>
<td rowspan="2">




</td>
<td>


`tp+` <a id="rst-footnote-reference-30"></a>[12](#rst-tp)

</td>
<td>




</td>
</tr>
<tr>
<td>


`tracepoint+` <a id="rst-footnote-reference-31"></a>[12](#rst-tp)

</td>
<td>




</td>
</tr>
<tr>
<td rowspan="9">


`BPF_PROG_TYPE_TRACING`

</td>
<td rowspan="2">


`BPF_MODIFY_RETURN`

</td>
<td>


`fmod_ret+` <a id="rst-footnote-reference-32"></a>[1](#rst-fentry)

</td>
<td>




</td>
</tr>
<tr>
<td>


`fmod_ret.s+` <a id="rst-footnote-reference-33"></a>[1](#rst-fentry)

</td>
<td>


Yes

</td>
</tr>
<tr>
<td rowspan="2">


`BPF_TRACE_FENTRY`

</td>
<td>


`fentry+` <a id="rst-footnote-reference-34"></a>[1](#rst-fentry)

</td>
<td>




</td>
</tr>
<tr>
<td>


`fentry.s+` <a id="rst-footnote-reference-35"></a>[1](#rst-fentry)

</td>
<td>


Yes

</td>
</tr>
<tr>
<td rowspan="2">


`BPF_TRACE_FEXIT`

</td>
<td>


`fexit+` <a id="rst-footnote-reference-36"></a>[1](#rst-fentry)

</td>
<td>




</td>
</tr>
<tr>
<td>


`fexit.s+` <a id="rst-footnote-reference-37"></a>[1](#rst-fentry)

</td>
<td>


Yes

</td>
</tr>
<tr>
<td rowspan="2">


`BPF_TRACE_ITER`

</td>
<td>


`iter+` <a id="rst-footnote-reference-38"></a>[13](#rst-iter)

</td>
<td>




</td>
</tr>
<tr>
<td>


`iter.s+` <a id="rst-footnote-reference-39"></a>[13](#rst-iter)

</td>
<td>


Yes

</td>
</tr>
<tr>
<td>


`BPF_TRACE_RAW_TP`

</td>
<td>


`tp_btf+` <a id="rst-footnote-reference-40"></a>[1](#rst-fentry)

</td>
<td>




</td>
</tr>
<tr>
<td rowspan="6">


`BPF_PROG_TYPE_XDP`

</td>
<td rowspan="2">


`BPF_XDP_CPUMAP`

</td>
<td>


`xdp.frags/cpumap`

</td>
<td>




</td>
</tr>
<tr>
<td>


`xdp/cpumap`

</td>
<td>




</td>
</tr>
<tr>
<td rowspan="2">


`BPF_XDP_DEVMAP`

</td>
<td>


`xdp.frags/devmap`

</td>
<td>




</td>
</tr>
<tr>
<td>


`xdp/devmap`

</td>
<td>




</td>
</tr>
<tr>
<td rowspan="2">


`BPF_XDP`

</td>
<td>


`xdp.frags`

</td>
<td>




</td>
</tr>
<tr>
<td>


`xdp`

</td>
<td>




</td>
</tr>
</tbody>
</table>

**Footnotes**

<a id="rst-fentry"></a>



**[1]** The `fentry` attach format is `fentry[.s]/<function>`.

<a id="rst-kprobe"></a>



**[2]** The `kprobe` attach format is `kprobe/<function>[+<offset>]`. Valid characters for `function` are `a-zA-Z0-9_.` and `offset` must be a valid non-negative integer.

<a id="rst-ksyscall"></a>



**[3]** The `ksyscall` attach format is `ksyscall/<syscall>`.

<a id="rst-uprobe"></a>



**[4]** The `uprobe` attach format is `uprobe[.s]/<path>:<function>[+<offset>]`.

<a id="rst-upmul"></a>



**[5]** The `uprobe.multi` attach format is `uprobe.multi[.s]/<path>:<function-pattern>` where `function-pattern` supports `*` and `?` wildcards.

<a id="rst-usdt"></a>



**[6]** The `usdt` attach format is `usdt/<path>:<provider>:<name>`.

<a id="rst-kpmulti"></a>



**[7]** The `kprobe.multi` attach format is `kprobe.multi/<pattern>` where `pattern` supports `*` and `?` wildcards. Valid characters for pattern are `a-zA-Z0-9_.*?`.

<a id="rst-lsm"></a>



**[8]** The `lsm` attachment format is `lsm[.s]/<hook>`.

<a id="rst-rawtp"></a>



**[9]** The `raw_tp` attach format is `raw_tracepoint[.w]/<tracepoint>`.

<a id="rst-tc-legacy"></a>



**[10]** The `tc`, `classifier` and `action` attach types are deprecated, use `tcx/*` instead.

<a id="rst-struct-ops"></a>



**[11]** The `struct_ops` attach format supports `struct_ops[.s]/<name>` convention, but `name` is ignored and it is recommended to just use plain `SEC("struct_ops[.s]")`. The attachments are defined in a struct initializer that is tagged with `SEC(".struct_ops[.link]")`.

<a id="rst-tp"></a>



**[12]** The `tracepoint` attach format is `tracepoint/<category>/<name>`.

<a id="rst-iter"></a>



**[13]** The `iter` attach format is `iter[.s]/<struct-name>`.
