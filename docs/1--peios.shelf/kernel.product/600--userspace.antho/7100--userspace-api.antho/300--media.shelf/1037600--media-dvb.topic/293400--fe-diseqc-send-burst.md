---
title: "ioctl FE_DISEQC_SEND_BURST"
type: reference
description: "FE_DISEQC_SEND_BURST - Sends a 22KHz tone burst for 2x1 mini DiSEqC satellite selection."
---

<a id="rst-ioctl-fe-diseqc-send-burst"></a>
<a id="rst-fe-diseqc-send-burst"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.fe -->

<a id="rst-name"></a>

## Name

FE_DISEQC_SEND_BURST - Sends a 22KHz tone burst for 2x1 mini DiSEqC satellite selection.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-FE_DISEQC_SEND_BURST"></a>

```c
FE_DISEQC_SEND_BURST
```

`int ioctl(int fd, FE_DISEQC_SEND_BURST, enum fe_sec_mini_cmd tone)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`tone`**

  An integer enumerated value described at `fe_sec_mini_cmd`.

<a id="rst-description"></a>

## Description

This ioctl is used to set the generation of a 22kHz tone burst for mini DiSEqC satellite selection for 2x1 switches. This call requires read/write permissions.

It provides support for what's specified at [Digital Satellite Equipment Control (DiSEqC) - Simple "ToneBurst" Detection Circuit specification.](<http://www.eutelsat.com/files/contributed/satellites/pdf/Diseqc/associated%20docs/simple_tone_burst_detec.pdf>)

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned.

On error -1 is returned, and the `errno` variable is set appropriately.

Generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
