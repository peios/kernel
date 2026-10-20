---
title: "Binding for the AXS10X Generic PLL clock"
type: reference
description: "Device-tree binding reference for Binding for the AXS10X Generic PLL clock."
---

This binding uses the common clock binding\[1\].

\[1\] [Documentation/devicetree/bindings/clock/clock-bindings.txt](<~kernel/hardware/devicetree/bindings-clock/clock-bindings>)

## Required properties:

- compatible: should be "snps,axs10x-&lt;name&gt;-pll-clock"
  "snps,axs10x-arc-pll-clock"
  "snps,axs10x-pgu-pll-clock"
- reg: should always contain 2 pairs address - length: first for PLL config
  registers and second for corresponding LOCK CGU register.
- clocks: shall be the input parent clock phandle for the PLL.
- #clock-cells: from common clock binding; Should always be set to 0.

## Example:

```dts
	input-clk: input-clk {
		clock-frequency = <33333333>;
		compatible = "fixed-clock";
		#clock-cells = <0>;
	};
```

```dts
	core-clk: core-clk@80 {
		compatible = "snps,axs10x-arc-pll-clock";
		reg = <0x80 0x10>, <0x100 0x10>;
		#clock-cells = <0>;
		clocks = <&input-clk>;
	};
```
