---
title: "ioctl FE_ENABLE_HIGH_LNB_VOLTAGE"
type: reference
description: "FE_ENABLE_HIGH_LNB_VOLTAGE - Select output DC level between normal LNBf voltages or higher LNBf - voltages."
---

<a id="rst-ioctl-fe-enable-high-lnb-voltage"></a>
<a id="rst-fe-enable-high-lnb-voltage"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.fe -->

<a id="rst-name"></a>

## Name

FE_ENABLE_HIGH_LNB_VOLTAGE - Select output DC level between normal LNBf voltages or higher LNBf - voltages.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-FE_ENABLE_HIGH_LNB_VOLTAGE"></a>

```c
FE_ENABLE_HIGH_LNB_VOLTAGE
```

`int ioctl(int fd, FE_ENABLE_HIGH_LNB_VOLTAGE, unsigned int high)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`high`**

  Valid flags:

  - 0 - normal 13V and 18V.

  - &gt;0 - enables slightly higher voltages instead of 13/18V, in order to compensate for long antenna cables.

<a id="rst-description"></a>

## Description

Select output DC level between normal LNBf voltages or higher LNBf voltages between 0 (normal) or a value grater than 0 for higher voltages.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned.

On error -1 is returned, and the `errno` variable is set appropriately.

Generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
