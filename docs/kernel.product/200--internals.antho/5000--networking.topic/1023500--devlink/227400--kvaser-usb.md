---
title: "kvaser_usb devlink support"
type: reference
description: "This document describes the devlink features implemented by the kvaser_usb device driver."
---

<a id="rst-kvaser-usb-devlink-support"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

This document describes the devlink features implemented by the `kvaser_usb` device driver.

<a id="rst-info-versions"></a>

## Info versions

The `kvaser_usb` driver reports the following versions


<table>
<caption>devlink info versions implemented</caption>
<tbody>
<tr>
<td>


Name

</td>
<td>


Type

</td>
<td>


Description

</td>
</tr>
<tr>
<td>


`fw`

</td>
<td>


running

</td>
<td>


Version of the firmware running on the device. Also available through `ethtool -i` as `firmware-version`.

</td>
</tr>
<tr>
<td>


`board.rev`

</td>
<td>


fixed

</td>
<td>


The device hardware revision.

</td>
</tr>
<tr>
<td>


`board.id`

</td>
<td>


fixed

</td>
<td>


The device EAN (product number).

</td>
</tr>
<tr>
<td>


`serial_number`

</td>
<td>


fixed

</td>
<td>


The device serial number.

</td>
</tr>
</tbody>
</table>
