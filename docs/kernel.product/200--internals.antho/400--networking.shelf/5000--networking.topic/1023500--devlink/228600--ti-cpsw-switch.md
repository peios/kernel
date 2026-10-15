---
title: "ti-cpsw-switch devlink support"
type: reference
description: "This document describes the devlink features implemented by the ti-cpsw-switch device driver."
---

<a id="rst-ti-cpsw-switch-devlink-support"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

This document describes the devlink features implemented by the `ti-cpsw-switch` device driver.

<a id="rst-parameters"></a>

## Parameters

The `ti-cpsw-switch` driver implements the following driver-specific parameters.


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


`ale_bypass`

</td>
<td>


Boolean

</td>
<td>


runtime

</td>
<td>


Enables ALE_CONTROL(4).BYPASS mode for debugging purposes. In this mode, all packets will be sent to the host port only.

</td>
</tr>
<tr>
<td>


`switch_mode`

</td>
<td>


Boolean

</td>
<td>


runtime

</td>
<td>


Enable switch mode

</td>
</tr>
</tbody>
</table>
