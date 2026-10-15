---
title: "Linux SCSI Disk Driver (sd) Parameters"
type: reference
description: "Enable/disable drive write & read cache."
---

<a id="rst-linux-scsi-disk-driver-sd-parameters"></a>

<a id="rst-cache-type-rw"></a>

## cache_type (RW)

<!-- SPDX-License-Identifier: GPL-2.0 -->

Enable/disable drive write &amp; read cache.


<table>
<thead>
<tr>
<th>


cache_type string

</th>
<th>


WCE

</th>
<th>


RCD

</th>
<th>


Write cache

</th>
<th>


Read cache

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


write through

</td>
<td>


0

</td>
<td>


0

</td>
<td>


off

</td>
<td>


on

</td>
</tr>
<tr>
<td>


none

</td>
<td>


0

</td>
<td>


1

</td>
<td>


off

</td>
<td>


off

</td>
</tr>
<tr>
<td>


write back

</td>
<td>


1

</td>
<td>


0

</td>
<td>


on

</td>
<td>


on

</td>
</tr>
<tr>
<td>


write back, no read (daft)

</td>
<td>


1

</td>
<td>


1

</td>
<td>


on

</td>
<td>


off

</td>
</tr>
</tbody>
</table>

To set cache type to "write back" and save this setting to the drive:



```text
# echo "write back" > cache_type
```

To modify the caching mode without making the change persistent, prepend "temporary " to the cache type string. E.g.:



```text
# echo "temporary write back" > cache_type
```
