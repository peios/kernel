---
title: "Seg6 Sysfs variables"
type: reference
description: "Accept or drop SR-enabled IPv6 packets on this interface."
---

<a id="rst-seg6-sysfs-variables"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-proc-sys-net-conf-iface-seg6-variables"></a>

## /proc/sys/net/conf/&lt;iface&gt;/seg6\_\* variables:

- **seg6_enabled - BOOL**

  Accept or drop SR-enabled IPv6 packets on this interface.

  Relevant packets are those with SRH present and DA = local.

  - 0 - disabled (default)

  - not 0 - enabled

- **seg6_require_hmac - INTEGER**

  Define HMAC policy for ingress SR-enabled packets on this interface.

  - -1 - Ignore HMAC field

  - 0 - Accept SR packets without HMAC, validate SR packets with HMAC

  - 1 - Drop SR packets without HMAC, validate SR packets with HMAC

  Default is 0.

<a id="rst-proc-sys-net-ipv6-seg6-variables"></a>

## /proc/sys/net/ipv6/seg6\_\* variables:

- **seg6_flowlabel - INTEGER**

  Controls the behaviour of computing the flowlabel of outer IPv6 header in case of SR T.encaps

  >
  > <table>
  > <tbody>
  > <tr>
  > <td>
  >
  >
  > -1
  >
  > </td>
  > <td>
  >
  >
  > set flowlabel to zero.
  >
  > </td>
  > </tr>
  > <tr>
  > <td>
  >
  >
  > 0
  >
  > </td>
  > <td>
  >
  >
  > copy flowlabel from Inner packet in case of Inner IPv6 (Set flowlabel to 0 in case IPv4/L2)
  >
  > </td>
  > </tr>
  > <tr>
  > <td>
  >
  >
  > 1
  >
  > </td>
  > <td>
  >
  >
  > Compute the flowlabel using seg6_make_flowlabel()
  >
  > </td>
  > </tr>
  > </tbody>
  > </table>

  Default is 0.
