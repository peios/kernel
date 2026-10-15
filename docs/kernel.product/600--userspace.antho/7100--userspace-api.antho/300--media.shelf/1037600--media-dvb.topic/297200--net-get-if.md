---
title: "ioctl NET_GET_IF"
type: reference
description: "NET_GET_IF - Read the configuration data of an interface created via - NET_ADD_IF <net>."
---

<a id="rst-ioctl-net-get-if"></a>
<a id="rst-net-get-if"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.net -->

<a id="rst-name"></a>

## Name

NET_GET_IF - Read the configuration data of an interface created via - [NET_ADD_IF](<~kernel/userspace/userspace-api/media-dvb/net#rst-net>).

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-NET_GET_IF"></a>

```c
NET_GET_IF
```

`int ioctl(int fd, NET_GET_IF, struct dvb_net_if *net_if)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`net_if`**

  pointer to struct `dvb_net_if`

<a id="rst-description"></a>

## Description

The NET_GET_IF ioctl uses the interface number given by the struct `dvb_net_if`::ifnum field and fills the content of struct `dvb_net_if` with the packet ID and encapsulation type used on such interface. If the interface was not created yet with [NET_ADD_IF](<~kernel/userspace/userspace-api/media-dvb/net#rst-net>), it will return -1 and fill the `errno` with `EINVAL` error code.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, and `ca_slot_info` is filled.

On error -1 is returned, and the `errno` variable is set appropriately.

The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
