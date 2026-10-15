---
title: "GPIO Error Codes"
type: reference
description: "Reference for GPIO Error Codes."
---

<a id="rst-gpio-error-codes"></a>
<a id="rst-gpio-errors"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-gpio-errors-1"></a>



<!-- tabularcolumns: |p{2.5cm}|p{15.0cm}| -->


<table>
<caption>Common GPIO error codes</caption>
<tbody>
<tr>
<td>


`EAGAIN` (aka `EWOULDBLOCK`)

</td>
<td>


The device was opened in non-blocking mode and a read can't be performed as there is no data available.

</td>
</tr>
<tr>
<td>


`EBADF`

</td>
<td>


The file descriptor is not valid.

</td>
</tr>
<tr>
<td>


`EBUSY`

</td>
<td>


The ioctl can't be handled because the device is busy. Typically returned when an ioctl attempts something that would require the usage of a resource that was already allocated. The ioctl must not be retried without performing another action to fix the problem first.

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


One or more of the ioctl parameters are invalid or out of the allowed range. This is a widely used error code.

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


`EPERM`

</td>
<td>


Permission denied. Typically returned in response to an attempt to perform an action incompatible with the current line configuration.

</td>
</tr>
<tr>
<td>


`EIO`

</td>
<td>


I/O error. Typically returned when there are problems communicating with a hardware device or requesting features that hardware does not support. This could indicate broken or flaky hardware. It's a 'Something is wrong, I give up\!' type of error.

</td>
</tr>
<tr>
<td>


`ENXIO`

</td>
<td>


Typically returned when a feature requiring interrupt support was requested, but the line does not support interrupts.

</td>
</tr>
</tbody>
</table>

> [!NOTE]
>
> 1. This list is not exhaustive; ioctls may return other error codes. Since errors may have side effects such as a driver reset, applications should abort on unexpected errors, or otherwise assume that the device is in a bad state.
>
> 2. Request-specific error codes are listed in the individual requests descriptions.
