---
title: "Opera firmware"
type: reference
description: "Author: Marco Gittler <g.marco@freenet.de>"
---

<a id="rst-opera-firmware"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

Author: Marco Gittler &lt;[g.marco@freenet.de](<mailto:g.marco@freenet.de>)&gt;

To extract the firmware for the Opera DVB-S1 USB-Box you need to copy the files:

2830SCap2.sys 2830SLoad2.sys

from the windriver disk into this directory.

Then run:



```none
scripts/get_dvb_firmware opera1
```

and after that you have 2 files:

dvb-usb-opera-01.fw dvb-usb-opera1-fpga-01.fw

in here.

Copy them into /lib/firmware/ .

After that the driver can load the firmware (if you have enabled firmware loading in kernel config and have hotplug running).
