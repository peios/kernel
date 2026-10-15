---
title: "PXA3xx GCU Controller"
type: reference
description: "Device-tree binding reference for PXA3xx GCU Controller."
---

## Required properties:

- compatible : "marvell,pxa300-gcu"
- reg : should contain the register range (address and length).
- interrupts : Controller interrupt.
- clocks: phandle to the PXA specific input clock.

## Example for PXA300:

```dts
	display-controller@54000000 {
		compatible = "marvell,pxa300-gcu";
		reg = <0x54000000 0x1000>;
		interrupts = <39>;
		clocks = <&clks CLK_PXA300_GCU>;
	};
```
