---
title: "Intel INT3496 ACPI device extcon driver documentation"
type: reference
description: "The Intel INT3496 ACPI device extcon driver is a driver for ACPI devices with an acpi-id of INT3496, such as found for example on Intel Baytrail and Cherrytrail tablets."
---

<a id="rst-intel-int3496-acpi-device-extcon-driver-documentation"></a>

The Intel INT3496 ACPI device extcon driver is a driver for ACPI devices with an acpi-id of INT3496, such as found for example on Intel Baytrail and Cherrytrail tablets.

This ACPI device describes how the OS can read the id-pin of the devices' USB-otg port, as well as how it optionally can enable Vbus output on the otg port and how it can optionally control the muxing of the data pins between an USB host and an USB peripheral controller.

The ACPI devices exposes this functionality by returning an array with up to 3 gpio descriptors from its ACPI \_CRS (Current Resource Settings) call:


<table>
<tbody>
<tr>
<td>


Index 0

</td>
<td>


The input gpio for the id-pin, this is always present and valid

</td>
</tr>
<tr>
<td>


Index 1

</td>
<td>


The output gpio for enabling Vbus output from the device to the otg port, write 1 to enable the Vbus output (this gpio descriptor may be absent or invalid)

</td>
</tr>
<tr>
<td>


Index 2

</td>
<td>


The output gpio for muxing of the data pins between the USB host and the USB peripheral controller, write 1 to mux to the peripheral controller

</td>
</tr>
</tbody>
</table>

There is a mapping between indices and GPIO connection IDs as follows

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> id
>
> </td>
> <td>
>
>
> index 0
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> vbus
>
> </td>
> <td>
>
>
> index 1
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> mux
>
> </td>
> <td>
>
>
> index 2
>
> </td>
> </tr>
> </tbody>
> </table>
