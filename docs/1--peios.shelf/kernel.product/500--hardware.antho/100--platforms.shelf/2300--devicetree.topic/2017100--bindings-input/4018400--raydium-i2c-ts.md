---
title: "Raydium I2C touchscreen"
type: reference
description: "Device-tree binding reference for Raydium I2C touchscreen."
---

## Required properties:

- compatible: must be "raydium,rm32380"
- reg: The I2C address of the device
- interrupts: interrupt to which the chip is connected
  See [../interrupt-controller/interrupts.txt](<~kernel/hardware/devicetree/bindings-interrupt-controller/interrupts>)
  Optional properties:
- avdd-supply: analog power supply needed to power device
- vccio-supply: IO Power source
- reset-gpios: reset gpio the chip is connected to.

## Example:

```dts
	touchscreen@39 {
		compatible = "raydium,rm32380";
		reg = <0x39>;
		interrupt-parent = <&gpio>;
		interrupts = <0x0 IRQ_TYPE_EDGE_FALLING>;
	};
```
