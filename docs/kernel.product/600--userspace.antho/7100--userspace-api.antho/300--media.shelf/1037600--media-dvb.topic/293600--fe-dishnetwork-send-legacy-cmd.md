---
title: "FE_DISHNETWORK_SEND_LEGACY_CMD"
type: reference
description: "Duplicate implicit target name: \"fe_dishnetwork_send_legacy_cmd\"."
---

<a id="rst-fe-dishnetwork-send-legacy-cmd-1"></a>
<a id="rst-fe-dishnetwork-send-legacy-cmd"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.fe -->

<a id="rst-name"></a>

## Name

FE_DISHNETWORK_SEND_LEGACY_CMD

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-FE_DISHNETWORK_SEND_LEGACY_CMD"></a>

```c
FE_DISHNETWORK_SEND_LEGACY_CMD
```

`int ioctl(int fd, FE_DISHNETWORK_SEND_LEGACY_CMD, unsigned long cmd)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`cmd`**

  Sends the specified raw cmd to the dish via DISEqC.

<a id="rst-description"></a>

## Description

> [!WARNING]
>
> This is a very obscure legacy command, used only at stv0299 driver. Should not be used on newer drivers.

It provides a non-standard method for selecting Diseqc voltage on the frontend, for Dish Network legacy switches.

As support for this ioctl were added in 2004, this means that such dishes were already legacy in 2004.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned.

On error -1 is returned, and the `errno` variable is set appropriately.

Generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
