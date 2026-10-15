---
title: "ioctl FE_SET_FRONTEND_TUNE_MODE"
type: reference
description: "FE_SET_FRONTEND_TUNE_MODE - Allow setting tuner mode flags to the frontend."
---

<a id="rst-ioctl-fe-set-frontend-tune-mode"></a>
<a id="rst-fe-set-frontend-tune-mode"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.fe -->

<a id="rst-name"></a>

## Name

FE_SET_FRONTEND_TUNE_MODE - Allow setting tuner mode flags to the frontend.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-FE_SET_FRONTEND_TUNE_MODE"></a>

```c
FE_SET_FRONTEND_TUNE_MODE
```

`int ioctl(int fd, FE_SET_FRONTEND_TUNE_MODE, unsigned int flags)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`flags`**

  Valid flags:

  - 0 - normal tune mode

  - `FE_TUNE_MODE_ONESHOT` - When set, this flag will disable any zigzagging or other "normal" tuning behaviour. Additionally, there will be no automatic monitoring of the lock status, and hence no frontend events will be generated. If a frontend device is closed, this flag will be automatically turned off when the device is reopened read-write.

<a id="rst-description"></a>

## Description

Allow setting tuner mode flags to the frontend, between 0 (normal) or `FE_TUNE_MODE_ONESHOT` mode

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned.

On error -1 is returned, and the `errno` variable is set appropriately.

Generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
