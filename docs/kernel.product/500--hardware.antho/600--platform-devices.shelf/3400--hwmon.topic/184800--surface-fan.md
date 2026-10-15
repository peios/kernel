---
title: "Kernel driver surface_fan"
type: reference
description: "Supported Devices:"
---

<a id="rst-kernel-driver-surface-fan"></a>

<!-- SPDX-License-Identifier: GPL-2.0-or-later -->

Supported Devices:

> - Microsoft Surface Pro 9

Author: Ivor Wanders &lt;[ivor@iwanders.net](<mailto:ivor@iwanders.net>)&gt;

<a id="rst-description"></a>

## Description

This provides monitoring of the fan found in some Microsoft Surface Pro devices, like the Surface Pro 9. The fan is always controlled by the onboard controller.

<a id="rst-sysfs-interface"></a>

## Sysfs interface


<table>
<thead>
<tr>
<th>


Name

</th>
<th>


Perm

</th>
<th>


Description

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


`fan1_input`

</td>
<td>


RO

</td>
<td>


Current fan speed in RPM.

</td>
</tr>
</tbody>
</table>
