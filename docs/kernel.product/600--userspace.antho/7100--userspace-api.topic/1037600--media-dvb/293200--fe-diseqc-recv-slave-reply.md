---
title: "ioctl FE_DISEQC_RECV_SLAVE_REPLY"
type: reference
description: "FE_DISEQC_RECV_SLAVE_REPLY - Receives reply from a DiSEqC 2.0 command"
---

<a id="rst-ioctl-fe-diseqc-recv-slave-reply"></a>
<a id="rst-fe-diseqc-recv-slave-reply"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.fe -->

<a id="rst-name"></a>

## Name

FE_DISEQC_RECV_SLAVE_REPLY - Receives reply from a DiSEqC 2.0 command

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-FE_DISEQC_RECV_SLAVE_REPLY"></a>

```c
FE_DISEQC_RECV_SLAVE_REPLY
```

`int ioctl(int fd, FE_DISEQC_RECV_SLAVE_REPLY, struct dvb_diseqc_slave_reply *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  pointer to struct `dvb_diseqc_slave_reply`.

<a id="rst-description"></a>

## Description

Receives reply from a DiSEqC 2.0 command.

The received message is stored at the buffer pointed by `argp`.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned.

On error -1 is returned, and the `errno` variable is set appropriately.

Generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
