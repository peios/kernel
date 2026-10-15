---
title: "Freescale MX25 ADC/TSC MultiFunction Device (MFD)"
type: reference
description: "Device-tree binding reference for Freescale MX25 ADC/TSC MultiFunction Device (MFD)."
---

This device combines two general purpose conversion queues one used for general
ADC and the other used for touchscreens.

## Required properties:

- compatible:			Should be "fsl,imx25-tsadc".
- reg:				Start address and size of the memory area of
  the device
- interrupts:			Interrupt for this device
  (See: [../interrupt-controller/interrupts.txt](<~kernel/hardware/devicetree/bindings-interrupt-controller/interrupts>))
- clocks:			An 'ipg' clock (See: [../clock/clock-bindings.txt](<~kernel/hardware/devicetree/bindings-clock/clock-bindings>))
- interrupt-controller:	This device is an interrupt controller. It
  controls the interrupts of both
  conversion queues.
- #interrupt-cells:		Should be '&lt;1&gt;'.
- #address-cells:		Should be '&lt;1&gt;'.
- #size-cells:			Should be '&lt;1&gt;'.

This device includes two conversion queues which can be added as subnodes.
The first queue is for the touchscreen, the second for general purpose ADC.

## Example:

```dts
	tscadc: tscadc@50030000 {
		compatible = "fsl,imx25-tsadc";
		reg = <0x50030000 0xc>;
		interrupts = <46>;
		clocks = <&clks 119>;
		clock-names = "ipg";
		interrupt-controller;
		#interrupt-cells = <1>;
		#address-cells = <1>;
		#size-cells = <1>;
		ranges;

		tsc: tcq@50030400 {
			compatible = "fsl,imx25-tcq";
			reg = <0x50030400 0x60>;
			...
		};

		adc: gcq@50030800 {
			compatible = "fsl,imx25-gcq";
			reg = <0x50030800 0x60>;
			...
		};
	};
```
