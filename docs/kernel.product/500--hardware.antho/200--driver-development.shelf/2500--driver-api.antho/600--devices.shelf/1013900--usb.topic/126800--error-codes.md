---
title: "USB Error codes"
type: reference
description: "This is the documentation of (hopefully) all possible error codes (and their interpretation) that can be returned from usbcore."
---

<a id="rst-usb-error-codes-1"></a>
<a id="rst-usb-error-codes"></a>

**Revised:** 2004-Oct-21

This is the documentation of (hopefully) all possible error codes (and their interpretation) that can be returned from usbcore.

Some of them are returned by the Host Controller Drivers (HCDs), which device drivers only see through usbcore.  As a rule, all the HCDs should behave the same except for transfer speed dependent behaviors and the way certain faults are reported.

<a id="rst-error-codes-returned-by-usb-submit-urb"></a>

## Error codes returned by `usb_submit_urb()`

Non-USB-specific:


<table>
<tbody>
<tr>
<td>


0

</td>
<td>


URB submission went fine

</td>
</tr>
<tr>
<td>


`-ENOMEM`

</td>
<td>


no memory for allocation of internal structures

</td>
</tr>
</tbody>
</table>

USB-specific:


<table>
<tbody>
<tr>
<td>


`-EBUSY`

</td>
<td>


The URB is already active.

</td>
</tr>
<tr>
<td>


`-ENODEV`

</td>
<td>


specified USB-device or bus doesn't exist

</td>
</tr>
<tr>
<td>


`-ENOENT`

</td>
<td>


specified interface or endpoint does not exist or is not enabled

</td>
</tr>
<tr>
<td>


`-ENXIO`

</td>
<td>


host controller driver does not support queuing of this type of urb.  (treat as a host controller bug.)

</td>
</tr>
<tr>
<td>


`-EINVAL`

</td>
<td>


- **a)** Invalid transfer type specified (or not supported)

- **b)** Invalid or unsupported periodic transfer interval

- **c)** ISO: attempted to change transfer interval

- **d)** ISO: `number_of_packets` is &lt; 0

- **e)** various other cases

</td>
</tr>
<tr>
<td>


`-EXDEV`

</td>
<td>


ISO: `URB_ISO_ASAP` wasn't specified and all the frames the URB would be scheduled in have already expired.

</td>
</tr>
<tr>
<td>


`-EFBIG`

</td>
<td>


Host controller driver can't schedule that many ISO frames.

</td>
</tr>
<tr>
<td>


`-EPIPE`

</td>
<td>


The pipe type specified in the URB doesn't match the endpoint's actual type.

</td>
</tr>
<tr>
<td>


`-EMSGSIZE`

</td>
<td>


- **(a)** endpoint maxpacket size is zero; it is not usable in the current interface altsetting.

- **(b)** ISO packet is larger than the endpoint maxpacket.

- **(c)** requested data transfer length is invalid: negative or too large for the host controller.

</td>
</tr>
<tr>
<td>


`-EBADR`

</td>
<td>


The wLength value in a control URB's setup packet does not match the URB's transfer_buffer_length.

</td>
</tr>
<tr>
<td>


`-ENOSPC`

</td>
<td>


This request would overcommit the usb bandwidth reserved for periodic transfers (interrupt, isochronous).

</td>
</tr>
<tr>
<td>


`-ESHUTDOWN`

</td>
<td>


The device or host controller has been disabled due to some problem that could not be worked around.

</td>
</tr>
<tr>
<td>


`-EPERM`

</td>
<td>


Submission failed because `urb->reject` was set.

</td>
</tr>
<tr>
<td>


`-EHOSTUNREACH`

</td>
<td>


URB was rejected because the device is suspended.

</td>
</tr>
<tr>
<td>


`-ENOEXEC`

</td>
<td>


A control URB doesn't contain a Setup packet.

</td>
</tr>
</tbody>
</table>

<a id="rst-error-codes-returned-by-in-urb-status-or-in-iso-frame-desc-n-status-for-iso"></a>

## Error codes returned by `in urb->status` or in `iso_frame_desc[n].status` (for ISO)

USB device drivers may only test urb status values in completion handlers. This is because otherwise there would be a race between HCDs updating these values on one CPU, and device drivers testing them on another CPU.

A transfer's actual_length may be positive even when an error has been reported.  That's because transfers often involve several packets, so that one or more packets could finish before an error stops further endpoint I/O.

For isochronous URBs, the urb status value is non-zero only if the URB is unlinked, the device is removed, the host controller is disabled, or the total transferred length is less than the requested length and the `URB_SHORT_NOT_OK` flag is set.  Completion handlers for isochronous URBs should only see `urb->status` set to zero, `-ENOENT`, `-ECONNRESET`, `-ESHUTDOWN`, or `-EREMOTEIO`. Individual frame descriptor status fields may report more status codes.


<table>
<tbody>
<tr>
<td>


0

</td>
<td>


Transfer completed successfully

</td>
</tr>
<tr>
<td>


`-ENOENT`

</td>
<td>


URB was synchronously unlinked by `usb_unlink_urb()`

</td>
</tr>
<tr>
<td>


`-EINPROGRESS`

</td>
<td>


URB still pending, no results yet (That is, if drivers see this it's a bug.)

</td>
</tr>
<tr>
<td>


`-EPROTO` <a id="rst-footnote-reference-1"></a>[1](#rst-f1), <a id="rst-footnote-reference-2"></a>[2](#rst-f2)

</td>
<td>


- **a)** bitstuff error

- **b)** no response packet received within the prescribed bus turn-around time

- **c)** unknown USB error

</td>
</tr>
<tr>
<td>


`-EILSEQ` <a id="rst-footnote-reference-3"></a>[1](#rst-f1), <a id="rst-footnote-reference-4"></a>[2](#rst-f2)

</td>
<td>


- **a)** CRC mismatch

- **b)** no response packet received within the prescribed bus turn-around time

- **c)** unknown USB error

Note that often the controller hardware does not distinguish among cases a), b), and c), so a driver cannot tell whether there was a protocol error, a failure to respond (often caused by device disconnect), or some other fault.

</td>
</tr>
<tr>
<td>


`-ETIME` <a id="rst-footnote-reference-5"></a>[2](#rst-f2)

</td>
<td>


No response packet received within the prescribed bus turn-around time.  This error may instead be reported as `-EPROTO` or `-EILSEQ`.

</td>
</tr>
<tr>
<td>


`-ETIMEDOUT`

</td>
<td>


Synchronous USB message functions use this code to indicate timeout expired before the transfer completed, and no other error was reported by HC.

</td>
</tr>
<tr>
<td>


`-EPIPE` <a id="rst-footnote-reference-6"></a>[2](#rst-f2)

</td>
<td>


Endpoint stalled.  For non-control endpoints, reset this status with `usb_clear_halt()`.

</td>
</tr>
<tr>
<td>


`-ECOMM`

</td>
<td>


During an IN transfer, the host controller received data from an endpoint faster than it could be written to system memory

</td>
</tr>
<tr>
<td>


`-ENOSR`

</td>
<td>


During an OUT transfer, the host controller could not retrieve data from system memory fast enough to keep up with the USB data rate

</td>
</tr>
<tr>
<td>


`-EOVERFLOW` <a id="rst-footnote-reference-7"></a>[1](#rst-f1)

</td>
<td>


The amount of data returned by the endpoint was greater than either the max packet size of the endpoint or the remaining buffer size. "Babble".

</td>
</tr>
<tr>
<td>


`-EREMOTEIO`

</td>
<td>


The data read from the endpoint did not fill the specified buffer, and `URB_SHORT_NOT_OK` was set in `urb->transfer_flags`.

</td>
</tr>
<tr>
<td>


`-ENODEV`

</td>
<td>


Device was removed.  Often preceded by a burst of other errors, since the hub driver doesn't detect device removal events immediately.

</td>
</tr>
<tr>
<td>


`-EXDEV`

</td>
<td>


ISO transfer only partially completed (only set in `iso_frame_desc[n].status`, not `urb->status`)

</td>
</tr>
<tr>
<td>


`-EINVAL`

</td>
<td>


ISO madness, if this happens: Log off and go home

</td>
</tr>
<tr>
<td>


`-ECONNRESET`

</td>
<td>


URB was asynchronously unlinked by `usb_unlink_urb()`

</td>
</tr>
<tr>
<td>


`-ESHUTDOWN`

</td>
<td>


The device or host controller has been disabled due to some problem that could not be worked around, such as a physical disconnect.

</td>
</tr>
</tbody>
</table>

<a id="rst-f1"></a>



**[1]** Error codes like `-EPROTO`, `-EILSEQ` and `-EOVERFLOW` normally indicate hardware problems such as bad devices (including firmware) or cables.

<a id="rst-f2"></a>



**[2]** This is also one of several codes that different kinds of host controller use to indicate a transfer has failed because of device disconnect.  In the interval before the hub driver starts disconnect processing, devices may receive such fault reports for every request.

<a id="rst-error-codes-returned-by-usbcore-functions"></a>

## Error codes returned by usbcore-functions

> [!NOTE]
>
> expect also other submit and transfer status codes

`usb_register()`:


<table>
<tbody>
<tr>
<td>


`-EINVAL`

</td>
<td>


error during registering new driver

</td>
</tr>
</tbody>
</table>

`usb_get_*/usb_set_*()`, `usb_control_msg()`, `usb_bulk_msg()`:


<table>
<tbody>
<tr>
<td>


`-ETIMEDOUT`

</td>
<td>


Timeout expired before the transfer completed.

</td>
</tr>
</tbody>
</table>
