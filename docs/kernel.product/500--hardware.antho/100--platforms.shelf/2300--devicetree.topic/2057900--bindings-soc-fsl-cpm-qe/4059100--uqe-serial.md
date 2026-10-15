---
title: "Serial"
type: reference
description: "Device-tree binding reference for Serial."
---

## Required Properties:

compatible : must be "fsl,&lt;chip&gt;-ucc-uart". For t1040, must be
"fsl,t1040-ucc-uart".
port-number : port number of UCC-UART
tx/rx-clock-name : should be "brg1"-"brg16" for internal clock source,

```text
		   should be "clk1"-"clk28" for external clock source.
```

## Example:

```dts
	ucc_serial: ucc@2200 {
		compatible = "fsl,t1040-ucc-uart";
		port-number = <0>;
		rx-clock-name = "brg2";
		tx-clock-name = "brg2";
	};
```
