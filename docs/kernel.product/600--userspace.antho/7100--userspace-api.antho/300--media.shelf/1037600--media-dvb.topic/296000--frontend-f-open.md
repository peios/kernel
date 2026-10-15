---
title: "Digital TV frontend open()"
type: reference
description: "fe-open - Open a frontend device"
---

<a id="rst-digital-tv-frontend-open"></a>
<a id="rst-frontend-f-open"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.fe -->

<a id="rst-name"></a>

## Name

fe-open - Open a frontend device

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

  Open flags. Access can either be `O_RDWR` or `O_RDONLY`.

  Multiple opens are allowed with `O_RDONLY`. In this mode, only query and read ioctls are allowed.

  Only one open is allowed in `O_RDWR`. In this mode, all ioctls are allowed.

  When the `O_NONBLOCK` flag is given, the system calls may return `EAGAIN` error code when no data is available or when the device driver is temporarily busy.

  Other flags have no effect.

<a id="rst-description"></a>

## Description

This system call opens a named frontend device (`/dev/dvb/adapter?/frontend?`) for subsequent use. Usually the first thing to do after a successful open is to find out the frontend type with [ioctl FE_GET_INFO](<~kernel/userspace/userspace-api/media-dvb/fe-get-info#rst-fe-get-info>).

The device can be opened in read-only mode, which only allows monitoring of device status and statistics, or read/write mode, which allows any kind of use (e.g. performing tuning operations.)

In a system with multiple front-ends, it is usually the case that multiple devices cannot be open in read/write mode simultaneously. As long as a front-end device is opened in read/write mode, other open() calls in read/write mode will either fail or block, depending on whether non-blocking or blocking mode was specified. A front-end device opened in blocking mode can later be put into non-blocking mode (and vice versa) using the F_SETFL command of the fcntl system call. This is a standard system call, documented in the Linux manual page for fcntl. When an open() call has succeeded, the device will be ready for use in the specified mode. This implies that the corresponding hardware is powered up, and that other front-ends may have been powered down to make that possible.

<a id="rst-return-value"></a>

## Return Value

On success `open()` returns the new file descriptor. On error, -1 is returned, and the `errno` variable is set appropriately.

Possible error codes are:

On success 0 is returned, and `ca_slot_info` is filled.

On error -1 is returned, and the `errno` variable is set appropriately.

<!-- tabularcolumns: |p{2.5cm}|p{15.0cm}| -->


<table>
<tbody>
<tr>
<td>


`EPERM`

</td>
<td>


The caller has no permission to access the device.

</td>
</tr>
<tr>
<td>


`EBUSY`

</td>
<td>


The device driver is already in use.

</td>
</tr>
<tr>
<td>


`EMFILE`

</td>
<td>


The process already has the maximum number of files open.

</td>
</tr>
<tr>
<td>


`ENFILE`

</td>
<td>


The limit on the total number of files open on the system has been reached.

</td>
</tr>
</tbody>
</table>

The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
