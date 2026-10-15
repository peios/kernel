---
title: "Adaptrum Anarion ethernet controller"
type: reference
description: "Device-tree binding reference for Adaptrum Anarion ethernet controller."
---

This device is a platform glue layer for stmmac.
Please see [stmmac.txt](<~kernel/hardware/devicetree/bindings-net/stmmac>) for the other unchanged properties.

## Required properties:

- compatible:  Should be "adaptrum,anarion-gmac", "snps,dwmac"
- phy-mode:    Should be "rgmii". Other modes are not currently supported.

## Examples:

```dts
	gmac1: ethernet@f2014000 {
		compatible = "adaptrum,anarion-gmac", "snps,dwmac";
		reg = <0xf2014000 0x4000>, <0xf2018100 8>;

		interrupt-parent = <&core_intc>;
		interrupts = <21>;
		interrupt-names = "macirq";

		clocks = <&core_clk>;
		clock-names = "stmmaceth";

		phy-mode = "rgmii";
	};
```
