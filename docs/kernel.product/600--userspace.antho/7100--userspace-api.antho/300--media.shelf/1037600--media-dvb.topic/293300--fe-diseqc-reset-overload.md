---
title: "ioctl FE_DISEQC_RESET_OVERLOAD"
type: reference
description: "FE_DISEQC_RESET_OVERLOAD - Restores the power to the antenna subsystem, if it was powered off due - to power overload."
---

<a id="rst-ioctl-fe-diseqc-reset-overload"></a>
<a id="rst-fe-diseqc-reset-overload"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.fe -->

<a id="rst-name"></a>

## Name

FE_DISEQC_RESET_OVERLOAD - Restores the power to the antenna subsystem, if it was powered off due - to power overload.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-FE_DISEQC_RESET_OVERLOAD"></a>

```c
FE_DISEQC_RESET_OVERLOAD
```

`int ioctl(int fd, FE_DISEQC_RESET_OVERLOAD, NULL)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

<a id="rst-description"></a>

## Description

If the bus has been automatically powered off due to power overload, this ioctl call restores the power to the bus. The call requires read/write access to the device. This call has no effect if the device is manually powered off. Not all Digital TV adapters support this ioctl.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned.

On error -1 is returned, and the `errno` variable is set appropriately.

Generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
