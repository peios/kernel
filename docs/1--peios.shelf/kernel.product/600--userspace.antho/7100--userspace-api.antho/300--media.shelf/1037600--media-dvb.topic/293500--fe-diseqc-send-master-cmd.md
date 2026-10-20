---
title: "ioctl FE_DISEQC_SEND_MASTER_CMD"
type: reference
description: "FE_DISEQC_SEND_MASTER_CMD - Sends a DiSEqC command"
---

<a id="rst-ioctl-fe-diseqc-send-master-cmd"></a>
<a id="rst-fe-diseqc-send-master-cmd"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.fe -->

<a id="rst-name"></a>

## Name

FE_DISEQC_SEND_MASTER_CMD - Sends a DiSEqC command

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-FE_DISEQC_SEND_MASTER_CMD"></a>

```c
FE_DISEQC_SEND_MASTER_CMD
```

`int ioctl(int fd, FE_DISEQC_SEND_MASTER_CMD, struct dvb_diseqc_master_cmd *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  pointer to struct `dvb_diseqc_master_cmd`

<a id="rst-description"></a>

## Description

Sends the DiSEqC command pointed by `dvb_diseqc_master_cmd` to the antenna subsystem.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned.

On error -1 is returned, and the `errno` variable is set appropriately.

Generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
