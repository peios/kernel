---
title: "CA_GET_MSG"
type: reference
description: "Duplicate implicit target name: \"ca_get_msg\"."
---

<a id="rst-ca-get-msg-1"></a>
<a id="rst-ca-get-msg"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.ca -->

<a id="rst-name"></a>

## Name

CA_GET_MSG

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-CA_GET_MSG"></a>

```c
CA_GET_MSG
```

`int ioctl(fd, CA_GET_MSG, struct ca_msg *msg)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by a previous call to `open()`.

- **`msg`**

  Pointer to struct `ca_msg`.

<a id="rst-description"></a>

## Description

Receives a message via a CI CA module.

> [!NOTE]
>
> Please notice that, on most drivers, this is done by reading from the /dev/adapter?/ca? device node.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned.

On error -1 is returned, and the `errno` variable is set appropriately.

Generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
