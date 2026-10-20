---
title: "Data flows that Relate some functions, and write packets"
type: reference
description: "Reference for Data flows that Relate some functions, and write packets."
---

<!-- SPDX-License-Identifier: GPL-2.0 -->

<!-- The here included files are intended to help understand the implementation -->

<a id="rst-data-flows-that-relate-some-functions-and-write-packets"></a>

## Data flows that Relate some functions, and write packets

![DRBD-8.3-data-packets.svg](asset-5e49ee5f7722-drbd-8-3-data-packets.svg)

![DRBD-data-packets.svg](asset-1b44fc93f6cf-drbd-data-packets.svg)

<a id="rst-sub-graphs-of-drbd-s-state-transitions"></a>

## Sub graphs of DRBD's state transitions

```mermaid
flowchart TB
  n0(["StandAllone"])
  n1(["WFConnection"])
  n2(["Unconnected"])
  n3(["WFReportParams"])
  n4(["Connected"])
  n5(["WFBitMapS"])
  n6(["WFBitMapT"])
  n7(["SyncSource"])
  n8(["SyncTarget"])
  n9(["PausedSyncS"])
  n10(["PausedSyncT"])
  n0 -->|"ioctl_set_net()"| n1
  n1 -->|"unable to bind()"| n2
  n1 -->|"in connect() after accept"| n3
  n3 -->|"checks in receive_param()"| n0
  n3 -->|"in receive_param()"| n4
  n3 -->|"sync_handshake()"| n5
  n3 -->|"sync_handshake()"| n6
  n5 -->|"receive_bitmap()"| n7
  n6 -->|"receive_bitmap()"| n8
  n7 --> n4
  n8 --> n4
  n7 --> n9
  n8 --> n10
  n9 --> n7
  n10 --> n8
  n4 -->|"* on network error"| n1
```

conn-states-8.dot

```mermaid
flowchart TB
  n0(["Diskless"])
  n1(["Inconsistent"])
  n2(["Consistent"])
  n3(["Outdated"])
  n4(["UpToDate"])
  n5(["Failed"])
  n0 -->|"ioctl_set_disk()"| n1
  n0 -->|"ioctl_set_disk()"| n2
  n0 -->|"ioctl_set_disk()"| n3
  n2 -->|"receive_param()"| n3
  n2 -->|"receive_param()"| n4
  n2 -->|"start resync"| n1
  n3 -->|"start resync"| n1
  n4 -->|"ioctl_replicate"| n1
  n1 -->|"resync completed"| n4
  n2 -->|"io completion error"| n5
  n3 -->|"io completion error"| n5
  n4 -->|"io completion error"| n5
  n1 -->|"io completion error"| n5
  n5 -->|"sending notify to peer"| n0
```

disk-states-8.dot

```mermaid
flowchart TB
  n0(["Secondary"])
  n1(["Primary"])
  n2(["Unknown"])
  n0 -->|"recv state packet"| n1
  n1 -->|"recv state packet"| n0
  n1 -->|"connection lost"| n2
  n0 -->|"connection lost"| n2
  n2 -->|"connected"| n1
  n2 -->|"connected"| n0
```

peer-states-8.dot
