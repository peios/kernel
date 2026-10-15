---
title: "GPIO controller on CE4100 / Sodaville SoCs"
type: reference
description: "Device-tree binding reference for GPIO controller on CE4100 / Sodaville SoCs."
---

The bindings for CE4100's GPIO controller match the generic description
which is covered by the [gpio.txt](<~kernel/hardware/devicetree/bindings-gpio/gpio>) file in this folder.

The only additional property is the intel,muxctl property which holds the
value which is written into the MUXCNTL register.

There is no compatible property for now because the driver is probed via
PCI id (vendor 0x8086 device 0x2e67).

The interrupt specifier consists of two cells encoded as follows:

- &lt;1st cell&gt;: The interrupt-number that identifies the interrupt source.
- &lt;2nd cell&gt;: The level-sense information, encoded as follows:
  4 - active high level-sensitive
  8 - active low level-sensitive

## Example of the GPIO device and one user:

```dts
	pcigpio: gpio@b,1 {
			/* two cells for GPIO and interrupt */
			#gpio-cells = <2>;
			#interrupt-cells = <2>;
			compatible = "pci8086,2e67.2",
					   "pci8086,2e67",
					   "pciclassff0000",
					   "pciclassff00";

			reg = <0x15900 0x0 0x0 0x0 0x0>;
			/* Interrupt line of the gpio device */
			interrupts = <15 1>;
			/* It is an interrupt and GPIO controller itself */
			interrupt-controller;
			gpio-controller;
			intel,muxctl = <0>;
	};
```

```dts
	testuser@20 {
			compatible = "example,testuser";
			/* User the 11th GPIO line as an active high triggered
			 * level interrupt
			 */
			interrupts = <11 8>;
			interrupt-parent = <&pcigpio>;
			/* Use this GPIO also with the gpio functions */
			gpios = <&pcigpio 11 0>;
	};
```
