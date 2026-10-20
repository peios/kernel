---
title: "CA_GET_CAP"
type: reference
description: "Duplicate implicit target name: \"ca_get_cap\"."
---

<a id="rst-ca-get-cap-1"></a>
<a id="rst-ca-get-cap"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.ca -->

<a id="rst-name"></a>

## Name

CA_GET_CAP

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-CA_GET_CAP"></a>

```c
CA_GET_CAP
```

`int ioctl(fd, CA_GET_CAP, struct ca_caps *caps)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by a previous call to `open()`.

- **`caps`**

  Pointer to struct `ca_caps`.

<a id="rst-description"></a>

## Description

Queries the Kernel for information about the available CA and descrambler slots, and their types.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned and `ca_caps` is filled.

On error, -1 is returned and the `errno` variable is set appropriately.

The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
