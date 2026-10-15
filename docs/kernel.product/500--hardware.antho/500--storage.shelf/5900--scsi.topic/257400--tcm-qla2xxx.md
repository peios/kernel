---
title: "tcm_qla2xxx Driver Notes"
type: reference
description: "There is now a new module endpoint attribute called jam_host attribute:"
---

<a id="rst-tcm-qla2xxx-driver-notes"></a>

<a id="rst-tcm-qla2xxx-jam-host-attribute"></a>

## tcm_qla2xxx jam_host attribute

<!-- SPDX-License-Identifier: GPL-2.0 -->

There is now a new module endpoint attribute called jam_host attribute:



```text
jam_host: boolean=0/1
```

This attribute and accompanying code is only included if the Kconfig parameter TCM_QLA2XXX_DEBUG is set to Y

By default this jammer code and functionality is disabled

Use this attribute to control the discarding of SCSI commands to a selected host.

This may be useful for testing error handling and simulating slow drain and other fabric issues.

Setting a boolean of 1 for the jam_host attribute for a particular host will discard the commands for that host.

Reset back to 0 to stop the jamming.

Enable host 4 to be jammed:



```text
echo 1 > /sys/kernel/config/target/qla2xxx/21:00:00:24:ff:27:8f:ae/tpgt_1/attrib/jam_host
```

Disable jamming on host 4:



```text
echo 0 > /sys/kernel/config/target/qla2xxx/21:00:00:24:ff:27:8f:ae/tpgt_1/attrib/jam_host
```
