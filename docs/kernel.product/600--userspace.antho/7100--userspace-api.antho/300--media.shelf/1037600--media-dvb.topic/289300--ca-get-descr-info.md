---
title: "CA_GET_DESCR_INFO"
type: reference
description: "Duplicate implicit target name: \"ca_get_descr_info\"."
---

<a id="rst-ca-get-descr-info-1"></a>
<a id="rst-ca-get-descr-info"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.ca -->

<a id="rst-name"></a>

## Name

CA_GET_DESCR_INFO

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-CA_GET_DESCR_INFO"></a>

```c
CA_GET_DESCR_INFO
```

`int ioctl(fd, CA_GET_DESCR_INFO, struct ca_descr_info *desc)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by a previous call to `open()`.

- **`desc`**

  Pointer to struct `ca_descr_info`.

<a id="rst-description"></a>

## Description

Returns information about all descrambler slots.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, and `ca_descr_info` is filled.

On error -1 is returned, and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
