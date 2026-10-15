---
title: "ioctl NET_REMOVE_IF"
type: reference
description: "NET_REMOVE_IF - Removes a network interface."
---

<a id="rst-ioctl-net-remove-if"></a>
<a id="rst-net-remove-if"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.net -->

<a id="rst-name"></a>

## Name

NET_REMOVE_IF - Removes a network interface.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-NET_REMOVE_IF"></a>

```c
NET_REMOVE_IF
```

`int ioctl(int fd, NET_REMOVE_IF, int ifnum)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`net_if`**

  number of the interface to be removed

<a id="rst-description"></a>

## Description

The NET_REMOVE_IF ioctl deletes an interface previously created via [NET_ADD_IF](<~kernel/userspace/userspace-api/media-dvb/net#rst-net>).

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, and `ca_slot_info` is filled.

On error -1 is returned, and the `errno` variable is set appropriately.

The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
