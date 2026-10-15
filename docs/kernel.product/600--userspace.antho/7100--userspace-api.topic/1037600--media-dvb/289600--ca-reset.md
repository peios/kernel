---
title: "CA_RESET"
type: reference
description: "Duplicate implicit target name: \"ca_reset\"."
---

<a id="rst-ca-reset-1"></a>
<a id="rst-ca-reset"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.ca -->

<a id="rst-name"></a>

## Name

CA_RESET

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-CA_RESET"></a>

```c
CA_RESET
```

`int ioctl(fd, CA_RESET)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by a previous call to `open()`.

<a id="rst-description"></a>

## Description

Puts the Conditional Access hardware on its initial state. It should be called before start using the CA hardware.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned.

On error -1 is returned, and the `errno` variable is set appropriately.

Generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
