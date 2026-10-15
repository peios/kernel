---
title: "Digital TV demux close()"
type: reference
description: "Digital TV demux close()"
---

<a id="rst-digital-tv-demux-close"></a>
<a id="rst-dmx-fclose"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.dmx -->

<a id="rst-name"></a>

## Name

Digital TV demux close()

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

This system call deactivates and deallocates a filter that was previously allocated via the `open()` call.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned.

On error, -1 is returned and the `errno` variable is set appropriately.

The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
