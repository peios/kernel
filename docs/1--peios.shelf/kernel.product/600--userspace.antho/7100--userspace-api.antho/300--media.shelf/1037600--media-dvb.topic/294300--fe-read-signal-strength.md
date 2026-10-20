---
title: "FE_READ_SIGNAL_STRENGTH"
type: reference
description: "Duplicate implicit target name: \"fe_read_signal_strength\"."
---

<a id="rst-fe-read-signal-strength-1"></a>
<a id="rst-fe-read-signal-strength"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.fe -->

<a id="rst-name"></a>

## Name

FE_READ_SIGNAL_STRENGTH

> [!NOTE]
>
> This ioctl is deprecated.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-FE_READ_SIGNAL_STRENGTH"></a>

```c
FE_READ_SIGNAL_STRENGTH
```

`int ioctl(int fd, FE_READ_SIGNAL_STRENGTH, uint16_t *strength)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`strength`**

  The signal strength value is stored into \*strength.

<a id="rst-description"></a>

## Description

This ioctl call returns the signal strength value for the signal currently received by the front-end. For this command, read-only access to the device is sufficient.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned.

On error -1 is returned, and the `errno` variable is set appropriately.

Generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
