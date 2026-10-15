---
title: "Device tree bindings for i2c-cbus-gpio driver"
type: reference
description: "Device-tree binding reference for Device tree bindings for i2c-cbus-gpio driver."
---

## Required properties:

- compatible = "i2c-cbus-gpio";
- gpios: clk, dat, sel
- #address-cells = &lt;1&gt;;
- #size-cells = &lt;0&gt;;

## Optional properties:

- child nodes conforming to i2c bus binding

## Example:

```dts
i2c@0 {
	compatible = "i2c-cbus-gpio";
	gpios = <&gpio 66 0 /* clk */
		 &gpio 65 0 /* dat */
		 &gpio 64 0 /* sel */
		>;
	#address-cells = <1>;
	#size-cells = <0>;

	retu: retu@1 {
		compatible = "nokia,retu";
		reg = <0x1>;
	};
};
```
