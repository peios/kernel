---
title: "CA_SET_DESCR"
type: reference
description: "Duplicate implicit target name: \"ca_set_descr\"."
---

<a id="rst-ca-set-descr-1"></a>
<a id="rst-ca-set-descr"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.ca -->

<a id="rst-name"></a>

## Name

CA_SET_DESCR

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-CA_SET_DESCR"></a>

```c
CA_SET_DESCR
```

`int ioctl(fd, CA_SET_DESCR, struct ca_descr *desc)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by a previous call to `open()`.

- **`msg`**

  Pointer to struct `ca_descr`.

<a id="rst-description"></a>

## Description

CA_SET_DESCR is used for feeding descrambler CA slots with descrambling keys (referred as control words).

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned.

On error -1 is returned, and the `errno` variable is set appropriately.

Generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
