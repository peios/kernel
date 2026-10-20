---
title: "octeontx2 devlink support"
type: reference
description: "This document describes the devlink features implemented by the octeontx2 AF, PF and VF device drivers."
---

<a id="rst-octeontx2-devlink-support"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

This document describes the devlink features implemented by the `octeontx2 AF, PF and VF` device drivers.

<a id="rst-parameters"></a>

## Parameters

The `octeontx2 PF and VF` drivers implement the following driver-specific parameters.


<table>
<caption>Driver-specific parameters implemented</caption>
<tbody>
<tr>
<td>


Name

</td>
<td>


Type

</td>
<td>


Mode

</td>
<td>


Description

</td>
</tr>
<tr>
<td>


`mcam_count`

</td>
<td>


u16

</td>
<td>


runtime

</td>
<td>


Select number of match CAM entries to be allocated for an interface. The same is used for ntuple filters of the interface. Supported by PF and VF drivers.

</td>
</tr>
</tbody>
</table>

The `octeontx2 AF` driver implements the following driver-specific parameters.


<table>
<caption>Driver-specific parameters implemented</caption>
<tbody>
<tr>
<td>


Name

</td>
<td>


Type

</td>
<td>


Mode

</td>
<td>


Description

</td>
</tr>
<tr>
<td>


`dwrr_mtu`

</td>
<td>


u32

</td>
<td>


runtime

</td>
<td>


Use to set the quantum which hardware uses for scheduling among transmit queues. Hardware uses weighted DWRR algorithm to schedule among all transmit queues.

</td>
</tr>
<tr>
<td>


`npc_mcam_high_zone_percent`

</td>
<td>


u8

</td>
<td>


runtime

</td>
<td>


Use to set the number of high priority zone entries in NPC MCAM that can be allocated by a user, out of the three priority zone categories high, mid and low.

</td>
</tr>
<tr>
<td>


`npc_def_rule_cntr`

</td>
<td>


bool

</td>
<td>


runtime

</td>
<td>


Use to enable or disable hit counters for the default rules in NPC MCAM. Its not guaranteed that counters gets enabled and mapped to all the default rules, since the counters are scarce and driver follows a best effort approach. The default rule serves as the primary packet steering rule for a specific PF or VF, based on its DMAC address which is installed by AF driver as part of its initialization. Sample command to read hit counters for default rule from debugfs is as follows, cat /sys/kernel/debug/cn10k/npc/mcam_rules

</td>
</tr>
<tr>
<td>


`nix_maxlf`

</td>
<td>


u16

</td>
<td>


runtime

</td>
<td>


Use to set the maximum number of LFs in NIX hardware block. This would be useful to increase the availability of default resources allocated to enabled LFs like MCAM entries for example.

</td>
</tr>
</tbody>
</table>

The `octeontx2 PF` driver implements the following driver-specific parameters.


<table>
<caption>Driver-specific parameters implemented</caption>
<tbody>
<tr>
<td>


Name

</td>
<td>


Type

</td>
<td>


Mode

</td>
<td>


Description

</td>
</tr>
<tr>
<td>


`unicast_filter_count`

</td>
<td>


u8

</td>
<td>


runtime

</td>
<td>


Set the maximum number of unicast filters that can be programmed for the device. This can be used to achieve better device resource utilization, avoiding over consumption of unused MCAM table entries.

</td>
</tr>
</tbody>
</table>
