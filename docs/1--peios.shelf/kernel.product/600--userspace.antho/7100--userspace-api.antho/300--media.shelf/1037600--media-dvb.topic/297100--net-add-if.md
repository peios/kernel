---
title: "ioctl NET_ADD_IF"
type: reference
description: "NET_ADD_IF - Creates a new network interface for a given Packet ID."
---

<a id="rst-ioctl-net-add-if"></a>
<a id="rst-net-add-if"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.net -->

<a id="rst-name"></a>

## Name

NET_ADD_IF - Creates a new network interface for a given Packet ID.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-NET_ADD_IF"></a>

```c
NET_ADD_IF
```

`int ioctl(int fd, NET_ADD_IF, struct dvb_net_if *net_if)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`net_if`**

  pointer to struct `dvb_net_if`

<a id="rst-description"></a>

## Description

The NET_ADD_IF ioctl system call selects the Packet ID (PID) that contains a TCP/IP traffic, the type of encapsulation to be used (MPE or ULE) and the interface number for the new interface to be created. When the system call successfully returns, a new virtual network interface is created.

The struct `dvb_net_if`::ifnum field will be filled with the number of the created interface.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, and `ca_slot_info` is filled.

On error -1 is returned, and the `errno` variable is set appropriately.

The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
