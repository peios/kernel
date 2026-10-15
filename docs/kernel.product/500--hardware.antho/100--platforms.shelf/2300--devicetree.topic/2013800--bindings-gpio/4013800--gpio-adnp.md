---
title: "Avionic Design N-bit GPIO expander bindings"
type: reference
description: "Device-tree binding reference for Avionic Design N-bit GPIO expander bindings."
---

## Required properties:

```text
- compatible: should be "ad,gpio-adnp"
- reg: The I2C slave address for this device.
- interrupts: Interrupt specifier for the controllers interrupt.
- #gpio-cells: Should be 2. The first cell is the GPIO number and the
  second cell is used to specify optional parameters:
  - bit 0: polarity (0: normal, 1: inverted)
- gpio-controller: Marks the device as a GPIO controller
- nr-gpios: The number of pins supported by the controller.
```

The GPIO expander can optionally be used as an interrupt controller, in
which case it uses the default two cell specifier as described in
[Documentation/devicetree/bindings/interrupt-controller/interrupts.txt](<~kernel/hardware/devicetree/bindings-interrupt-controller/interrupts>).

## Example:

```dts
	gpioext: gpio-controller@41 {
		compatible = "ad,gpio-adnp";
		reg = <0x41>;

		interrupt-parent = <&gpio>;
		interrupts = <160 1>;

		gpio-controller;
		#gpio-cells = <2>;

		interrupt-controller;
		#interrupt-cells = <2>;

		nr-gpios = <64>;
	};
```
