---
title: "Binding for the AXS10X I2S PLL clock"
type: reference
description: "Device-tree binding reference for Binding for the AXS10X I2S PLL clock."
---

This binding uses the common clock binding\[1\].

\[1\] [Documentation/devicetree/bindings/clock/clock-bindings.txt](<~kernel/hardware/devicetree/bindings-clock/clock-bindings>)

## Required properties:

- compatible: shall be "snps,axs10x-i2s-pll-clock"
- reg : address and length of the I2S PLL register set.
- clocks: shall be the input parent clock phandle for the PLL.
- #clock-cells: from common clock binding; Should always be set to 0.

## Example:

```dts
	pll_clock: pll_clock {
		compatible = "fixed-clock";
		clock-frequency = <27000000>;
		#clock-cells = <0>;
	};
```

```dts
	i2s_clock@100a0 {
		compatible = "snps,axs10x-i2s-pll-clock";
		reg = <0x100a0 0x10>;
		clocks = <&pll_clock>;
		#clock-cells = <0>;
	};
```
