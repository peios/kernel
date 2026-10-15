---
title: "Palmas 32KHz clocks *"
type: reference
description: "Device-tree binding reference for Palmas 32KHz clocks *."
---

Palmas device has two clock output pins for 32KHz, KG and KG\_AUDIO.

This binding uses the common clock binding [./clock-bindings.txt](<~kernel/hardware/devicetree/bindings-clock/clock-bindings>).

## Required properties:

- compatible :	"ti,palmas-clk32kg" for clk32kg clock
  "ti,palmas-clk32kgaudio" for clk32kgaudio clock
- #clock-cells : shall be set to 0.

## Optional property:

- ti,external-sleep-control: The external enable input pins controlled the
  enable/disable of clocks.  The external enable input pins ENABLE1,
  ENABLE2 and NSLEEP. The valid values for the external pins are:
  PALMAS\_EXT\_CONTROL\_PIN\_ENABLE1 for ENABLE1 pin
  PALMAS\_EXT\_CONTROL\_PIN\_ENABLE2 for ENABLE2 pin
  PALMAS\_EXT\_CONTROL\_PIN\_NSLEEP for NSLEEP pin
  Option 0 or missing this property means the clock is enabled/disabled
  via register access and these pins do not have any control.
  The macros of external control pins for DTS is defined at
  dt-bindings/mfd/palmas.h

## Example:

```dts
	#include <dt-bindings/mfd/palmas.h>
	...
	palmas: tps65913@58 {
		...
		clk32kg: palmas_clk32k@0 {
			compatible = "ti,palmas-clk32kg";
			#clock-cells = <0>;
			ti,external-sleep-control = <PALMAS_EXT_CONTROL_PIN_NSLEEP>;
		};
		...
	};
```
