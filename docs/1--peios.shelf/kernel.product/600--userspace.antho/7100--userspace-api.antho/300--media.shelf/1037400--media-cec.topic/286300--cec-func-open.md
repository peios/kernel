---
title: "cec open()"
type: reference
description: "cec-open - Open a cec device"
---

<a id="rst-cec-open"></a>
<a id="rst-cec-func-open"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: CEC -->

<a id="rst-name"></a>

## Name

cec-open - Open a cec device

<a id="rst-synopsis"></a>

## Synopsis



```c
#include <fcntl.h>
```





<a id="c-open"></a>

```c
int open( const char *device_name, int flags )
```

<a id="rst-arguments"></a>

## Arguments

- **`device_name`**

  Device to be opened.

- **`flags`**

  Open flags. Access mode must be `O_RDWR`.

  When the `O_NONBLOCK` flag is given, the [CEC_RECEIVE](<~kernel/userspace/userspace-api/media-cec/cec-ioc-receive#rst-cec-receive>) and [CEC_DQEVENT](<~kernel/userspace/userspace-api/media-cec/cec-ioc-dqevent#rst-cec-dqevent>) ioctls will return the `EAGAIN` error code when no message or event is available, and ioctls [CEC_TRANSMIT](<~kernel/userspace/userspace-api/media-cec/cec-ioc-receive#rst-cec-transmit>), [CEC_ADAP_S_PHYS_ADDR](<~kernel/userspace/userspace-api/media-cec/cec-ioc-adap-g-phys-addr#rst-cec-adap-s-phys-addr>) and [CEC_ADAP_S_LOG_ADDRS](<~kernel/userspace/userspace-api/media-cec/cec-ioc-adap-g-log-addrs#rst-cec-adap-s-log-addrs>) all return 0.

  Other flags have no effect.

<a id="rst-description"></a>

## Description

To open a cec device applications call `open()` with the desired device name. The function has no side effects; the device configuration remain unchanged.

When the device is opened in read-only mode, attempts to modify its configuration will result in an error, and `errno` will be set to EBADF.

<a id="rst-return-value"></a>

## Return Value

`open()` returns the new file descriptor on success. On error, -1 is returned, and `errno` is set appropriately. Possible error codes include:

- **`EACCES`**

  The requested access to the file is not allowed.

- **`EMFILE`**

  The process already has the maximum number of files open.

- **`ENFILE`**

  The system limit on the total number of open files has been reached.

- **`ENOMEM`**

  Insufficient kernel memory was available.

- **`ENODEV`**

  Device not found or was removed.
