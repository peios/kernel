---
title: "Digital TV CA close()"
type: reference
description: "Digital TV CA close()"
---

<a id="rst-digital-tv-ca-close"></a>
<a id="rst-ca-fclose"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.ca -->

<a id="rst-name"></a>

## Name

Digital TV CA close()

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-close"></a>

```c
int close(int fd)
```

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by a previous call to `open()`.

<a id="rst-description"></a>

## Description

This system call closes a previously opened CA device.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned.

On error -1 is returned, and the `errno` variable is set appropriately.

Generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
