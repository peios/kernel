---
title: "Generic Error Codes"
type: reference
description: "Reference for Generic Error Codes."
---

<a id="rst-generic-error-codes"></a>
<a id="rst-gen-errors"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<a id="rst-gen-errors-1"></a>



<!-- tabularcolumns: |p{2.5cm}|p{15.0cm}| -->


<table>
<caption>Generic error codes</caption>
<tbody>
<tr>
<td>


`EAGAIN` (aka `EWOULDBLOCK`)

</td>
<td>


The ioctl can't be handled because the device is in state where it can't perform it. This could happen for example in case where device is sleeping and ioctl is performed to query statistics. It is also returned when the ioctl would need to wait for an event, but the device was opened in non-blocking mode.

</td>
</tr>
<tr>
<td>


`EBADF`

</td>
<td>


The file descriptor is not a valid.

</td>
</tr>
<tr>
<td>


`EBUSY`

</td>
<td>


The ioctl can't be handled because the device is busy. This is typically return while device is streaming, and an ioctl tried to change something that would affect the stream, or would require the usage of a hardware resource that was already allocated. The ioctl must not be retried without performing another action to fix the problem first (typically: stop the stream before retrying).

</td>
</tr>
<tr>
<td>


`EFAULT`

</td>
<td>


There was a failure while copying data from/to userspace, probably caused by an invalid pointer reference.

</td>
</tr>
<tr>
<td>


`EINVAL`

</td>
<td>


One or more of the ioctl parameters are invalid or out of the allowed range. This is a widely used error code. See the individual ioctl requests for specific causes.

</td>
</tr>
<tr>
<td>


`ENODEV`

</td>
<td>


Device not found or was removed.

</td>
</tr>
<tr>
<td>


`ENOMEM`

</td>
<td>


There's not enough memory to handle the desired operation.

</td>
</tr>
<tr>
<td>


`ENOTTY`

</td>
<td>


The ioctl is not supported by the file descriptor.

</td>
</tr>
<tr>
<td>


`ENOSPC`

</td>
<td>


On USB devices, the stream ioctl's can return this error, meaning that this request would overcommit the usb bandwidth reserved for periodic transfers (up to 80% of the USB bandwidth).

</td>
</tr>
<tr>
<td>


`EPERM`

</td>
<td>


Permission denied. Can be returned if the device needs write permission, or some special capabilities is needed (e. g. root)

</td>
</tr>
<tr>
<td>


`EIO`

</td>
<td>


I/O error. Typically used when there are problems communicating with a hardware device. This could indicate broken or flaky hardware. It's a 'Something is wrong, I give up\!' type of error.

</td>
</tr>
<tr>
<td>


`ENXIO`

</td>
<td>


No device corresponding to this device special file exists.

</td>
</tr>
</tbody>
</table>

> [!NOTE]
>
> 1. This list is not exhaustive; ioctls may return other error codes. Since errors may have side effects such as a driver reset, applications should abort on unexpected errors, or otherwise assume that the device is in a bad state.
>
> 2. Request-specific error codes are listed in the individual requests descriptions.
