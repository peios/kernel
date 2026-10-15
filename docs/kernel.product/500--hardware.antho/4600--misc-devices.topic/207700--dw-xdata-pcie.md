---
title: "Driver for Synopsys DesignWare PCIe traffic generator (also known as xData)"
type: reference
description: "Supported chips: Synopsys DesignWare PCIe prototype solution"
---

<a id="rst-driver-for-synopsys-designware-pcie-traffic-generator-also-known-as-xdata"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

Supported chips: Synopsys DesignWare PCIe prototype solution

Datasheet: Not freely available

Author: Gustavo Pimentel &lt;[gustavo.pimentel@synopsys.com](<mailto:gustavo.pimentel@synopsys.com>)&gt;

<a id="rst-description"></a>

## Description

This driver should be used as a host-side (Root Complex) driver and Synopsys DesignWare prototype that includes this IP.

The dw-xdata-pcie driver can be used to enable/disable PCIe traffic generator in either direction (mutual exclusion) besides allowing the PCIe link performance analysis.

The interaction with this driver is done through the module parameter and can be changed in runtime. The driver outputs the requested command state information to `/var/log/kern.log` or dmesg.

<a id="rst-example"></a>

## Example

<a id="rst-write-tlps-traffic-generation-root-complex-to-endpoint-direction"></a>

### Write TLPs traffic generation - Root Complex to Endpoint direction

Generate traffic:



```text
# echo 1 > /sys/class/misc/dw-xdata-pcie.0/write
```

Get link throughput in MB/s:



```text
# cat /sys/class/misc/dw-xdata-pcie.0/write
204
```

Stop traffic in any direction:



```text
# echo 0 > /sys/class/misc/dw-xdata-pcie.0/write
```

<a id="rst-read-tlps-traffic-generation-endpoint-to-root-complex-direction"></a>

### Read TLPs traffic generation - Endpoint to Root Complex direction

Generate traffic:



```text
# echo 1 > /sys/class/misc/dw-xdata-pcie.0/read
```

Get link throughput in MB/s:



```text
# cat /sys/class/misc/dw-xdata-pcie.0/read
199
```

Stop traffic in any direction:



```text
# echo 0 > /sys/class/misc/dw-xdata-pcie.0/read
```
