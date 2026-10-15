---
title: "IOAM6 Sysfs variables"
type: reference
description: "Accept (= enabled) or ignore (= disabled) IPv6 IOAM options on ingress for this interface."
---

<a id="rst-ioam6-sysfs-variables"></a>

<a id="rst-proc-sys-net-conf-iface-ioam6-variables"></a>

## /proc/sys/net/conf/&lt;iface&gt;/ioam6\_\* variables:

<!-- SPDX-License-Identifier: GPL-2.0 -->

- **ioam6_enabled - BOOL**

  Accept (= enabled) or ignore (= disabled) IPv6 IOAM options on ingress for this interface.

  - 0 - disabled (default)

  - 1 - enabled

- **ioam6_id - SHORT INTEGER**

  Define the IOAM id of this interface.

  Default is \~0.

- **ioam6_id_wide - INTEGER**

  Define the wide IOAM id of this interface.

  Default is \~0.
