---
title: "Conexant Digicolor I2C controller"
type: reference
description: "Device-tree binding reference for Conexant Digicolor I2C controller."
---

## Required properties:

- compatible: must be "cnxt,cx92755-i2c"
- reg: physical address and length of the device registers
- interrupts: a single interrupt specifier
- clocks: clock for the device
- #address-cells: should be &lt;1&gt;
- #size-cells: should be &lt;0&gt;

## Optional properties:

- clock-frequency: the desired I2C bus clock frequency in Hz; in
  absence of this property the default value is used (100 kHz).

## Example:

```dts
	i2c: i2c@f0000120 {
		compatible = "cnxt,cx92755-i2c";
		reg = <0xf0000120 0x10>;
		interrupts = <28>;
		clocks = <&main_clk>;
		clock-frequency = <100000>;
		#address-cells = <1>;
		#size-cells = <0>;
	};
```
